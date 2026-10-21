# ============================================================
# tests/test_accuracy_validation.py  –  Comprehensive Automated Tests
# ============================================================
"""
Automated unit and integration test suite validating:
1. Invalid transportation routes and non-rail destinations.
2. Authentic train numbers and Indian Railways schedules.
3. Commercial flight schedules and airport-less destinations.
4. Verified bus schedules, official tariffs, and no fake seats.
5. Hotel price validation and facility localization.
6. Centralized ISO 4217 currency conversions and timestamps.
7. Image fetcher and URL validation.
8. Unsupported destinations and graceful handling.
9. Stale exchange rates and API failure fallbacks.
10. Data provenance layer rejecting NaN, null, and undefined.
11. Smart Trip Budget engine (nights = days - 1, verified vs estimated, emergency buffer).
12. Connecting railway journeys via verified junctions.
13. Travel-date validation and Open-Meteo weather horizon.
"""

import unittest
import math
from datetime import date, timedelta

from utils.provenance import (
    validate_numeric, validate_text, validate_transport_item,
    create_provenance_meta, ProvenanceLevel, sanitize_price
)
from utils.currency import (
    convert_currency, get_rate_for_currency, get_currency_info,
    get_all_exchange_rates, CURRENCY_REGISTRY
)
from utils.train_service import (
    search_verified_trains, get_train_options, resolve_station,
    NO_RAIL_DESTINATIONS, VERIFIED_TRAINS
)
from utils.flight_service import (
    search_verified_flights, get_flight_options, resolve_airport,
    NO_AIRPORT_CITIES, AIRPORT_DIRECTORY
)
from utils.bus_service import (
    get_verified_bus_options, OPERATORS, TERMINALS
)
from utils.weather_service import (
    get_weather_forecast, SEASONAL_NORMALS
)
from utils.budget_engine import (
    calculate_comprehensive_budget
)
from utils.hotel_generator import generate_hotels
from utils.hotel_apps import get_country_hotel_apps
from utils.rides import generate_ride_options


class TestDataValidationAndProvenance(unittest.TestCase):
    """Test Requirement 11: Data Validation & Provenance Layer"""

    def test_numeric_sanitizer_rejects_nan_and_null(self):
        self.assertEqual(validate_numeric(None, default=100), 100)
        self.assertEqual(validate_numeric(float('nan'), default=50), 50)
        self.assertEqual(validate_numeric(float('inf'), default=0), 0)
        self.assertEqual(validate_numeric("invalid_str", default=25), 25)
        self.assertEqual(validate_numeric(-500, min_val=0, default=0), 0)
        self.assertEqual(validate_numeric("1250.50"), 1250.5)

    def test_text_sanitizer_rejects_undefined_and_null_strings(self):
        self.assertEqual(validate_text(None, default="N/A"), "N/A")
        self.assertEqual(validate_text("null", default="Missing"), "Missing")
        self.assertEqual(validate_text("undefined", default="Unknown"), "Unknown")
        self.assertEqual(validate_text("NaN", default="Valid"), "Valid")
        self.assertEqual(validate_text("  Real Train Name  "), "Real Train Name")

    def test_transport_item_validator(self):
        raw_item = {
            "name": "12727 Godavari Express",
            "mode": "train",
            "price": "1450",
            "legs": [{"origin": "Hyderabad", "destination": "Visakhapatnam", "price": 1450}]
        }
        validated = validate_transport_item(raw_item)
        self.assertIsNotNone(validated)
        self.assertEqual(validated["price"], 1450)
        self.assertEqual(validated["mode"], "train")
        self.assertIn("provenance", validated)


class TestCurrencyConversion(unittest.TestCase):
    """Test Requirement 9: Centralized Currency Conversion"""

    def test_iso_4217_currencies_registered(self):
        for code in ["INR", "USD", "EUR", "GBP", "JPY", "VND", "AED", "SGD"]:
            self.assertIn(code, CURRENCY_REGISTRY)

    def test_currency_conversion_inr_to_usd(self):
        res = convert_currency(10000, from_curr="INR", to_curr="USD")
        self.assertEqual(res["from_currency"], "INR")
        self.assertEqual(res["to_currency"], "USD")
        self.assertGreater(res["converted_amount"], 50)
        self.assertLess(res["converted_amount"], 200)
        self.assertIsNotNone(res["timestamp"])

    def test_currency_conversion_vietnam_dong(self):
        res = convert_currency(1000, from_curr="INR", to_curr="VND")
        self.assertEqual(res["to_currency"], "VND")
        self.assertGreater(res["converted_amount"], 200000)

    def test_destination_currency_detection(self):
        info_vietnam = get_currency_info("Da Nang, Vietnam")
        self.assertEqual(info_vietnam["code"], "VND")
        self.assertEqual(info_vietnam["symbol"], "₫")

        info_japan = get_currency_info("Tokyo, Japan")
        self.assertEqual(info_japan["code"], "JPY")
        self.assertEqual(info_japan["symbol"], "¥")

        info_india = get_currency_info("Andhra Pradesh")
        self.assertEqual(info_india["code"], "INR")
        self.assertEqual(info_india["symbol"], "₹")


class TestTrainService(unittest.TestCase):
    """Test Requirement 3: Indian Railways Train Service"""

    def test_authentic_train_numbers_and_names(self):
        # Hyderabad to Visakhapatnam must have real trains like Godavari or Vande Bharat
        res = search_verified_trains("Hyderabad", "Visakhapatnam")
        self.assertTrue(res["is_rail_connected"])
        direct = res["direct_trains"]
        self.assertGreater(len(direct), 0)

        for train in direct:
            # Must have real 5-digit train number
            self.assertEqual(len(train["train_number"]), 5)
            self.assertTrue(train["train_number"].isdigit())
            # Train must not have fabricated AVL-xx seats
            self.assertNotIn("AVL-", str(train["vacancy"]["text"]))

    def test_non_rail_hill_stations(self):
        # Munnar has no railway station
        res = search_verified_trains("Bengaluru", "Munnar")
        self.assertFalse(res["is_rail_connected"])
        self.assertIn("no railway station", res["route_message"].lower())

    def test_railway_connecting_journeys(self):
        # Araku to Hyderabad has no direct train, connects via Visakhapatnam Junction
        res = search_verified_trains("Araku", "Hyderabad")
        self.assertTrue(res["is_rail_connected"])
        self.assertEqual(len(res["direct_trains"]), 0)
        self.assertGreater(len(res["connecting_trains"]), 0)
        connecting = res["connecting_trains"][0]
        self.assertEqual(len(connecting["legs"]), 2)


class TestFlightService(unittest.TestCase):
    """Test Requirement 2: Commercial Flight Service"""

    def test_commercial_flight_between_airports(self):
        res = search_verified_flights("Visakhapatnam", "Delhi")
        self.assertTrue(res["has_direct_flight"])
        self.assertGreater(len(res["flights"]), 0)
        first_flight = res["flights"][0]
        self.assertIn(first_flight["airline"], ["IndiGo", "Air India"])
        self.assertTrue(first_flight["booking_url"].startswith("https://www.google.com/travel/flights"))

    def test_airport_less_destination(self):
        # Araku has no commercial airport
        res = search_verified_flights("Hyderabad", "Araku")
        self.assertFalse(res["has_direct_flight"])
        self.assertIn("does not have a commercial airport", res["route_message"])

    def test_short_distance_flight_restriction(self):
        # Visakhapatnam to Rajahmundry or same city
        res = search_verified_flights("Visakhapatnam", "Visakhapatnam")
        self.assertFalse(res["has_direct_flight"])


class TestBusService(unittest.TestCase):
    """Test Requirement 4: Bus Transport Service"""

    def test_verified_rtc_corridors(self):
        buses = get_verified_bus_options("Hyderabad", "Vijayawada")
        self.assertGreater(len(buses), 0)
        first_bus = buses[0]
        self.assertIn(first_bus["operator"], ["TSRTC", "APSRTC", "Orange Travels"])
        self.assertGreater(first_bus["price"], 200)
        self.assertNotIn("AVL-", first_bus["seat_availability"])
        self.assertTrue(first_bus["booking_url"].startswith("http"))

    def test_impossible_water_route(self):
        # Bus to Andaman islands is impossible
        buses = get_verified_bus_options("Chennai", "Port Blair")
        self.assertEqual(len(buses), 0)


class TestWeatherService(unittest.TestCase):
    """Test Requirement 10: Weather Forecast & Climate Horizon"""

    def test_live_forecast_within_14_days(self):
        # Today's weather
        today_str = date.today().strftime("%Y-%m-%d")
        w = get_weather_forecast("Visakhapatnam", target_date_str=today_str)
        self.assertTrue(w["is_live_forecast"])
        self.assertIn("°C", w["summary"])
        self.assertEqual(w["provenance"]["verification_level"], ProvenanceLevel.VERIFIED_LIVE)

    def test_seasonal_climate_beyond_14_days(self):
        # Date 180 days in future must use seasonal normal, NOT fabricated day-by-day forecast
        future_date = (date.today() + timedelta(days=180)).strftime("%Y-%m-%d")
        w = get_weather_forecast("Visakhapatnam", target_date_str=future_date, best_season="Winter")
        self.assertFalse(w["is_live_forecast"])
        self.assertEqual(w["type"], "Historical Seasonal Climate Normal")
        self.assertEqual(w["provenance"]["verification_level"], ProvenanceLevel.INDICATIVE_ESTIMATE)


class TestSmartTripBudgetEngine(unittest.TestCase):
    """Test Requirement 12: Smart Trip Budget Engine"""

    def test_nights_calculation_days_minus_one(self):
        # A 3-day trip is 2 nights
        b3 = calculate_comprehensive_budget(days=3, travelers=2, user_budget=20000)
        self.assertEqual(b3["nights"], 2)

        # A 1-day trip is 0 nights (day excursion)
        b1 = calculate_comprehensive_budget(days=1, travelers=2, user_budget=5000)
        self.assertEqual(b1["nights"], 0)

    def test_verified_vs_estimated_separation(self):
        verified_outbound = {
            "price": 1200,
            "provenance": {"is_verified": True, "verification_level": ProvenanceLevel.VERIFIED_SCHEDULE, "source_provider": "IRCTC"}
        }
        verified_return = {
            "price": 1200,
            "provenance": {"is_verified": True, "verification_level": ProvenanceLevel.VERIFIED_SCHEDULE, "source_provider": "IRCTC"}
        }
        budget = calculate_comprehensive_budget(
            days=3,
            travelers=2,
            user_budget=30000,
            outbound_option=verified_outbound,
            return_option=verified_return
        )
        # Verified transport: 1200*2 + 1200*2 = 4800
        self.assertEqual(budget["verified_amount"], 4800)
        self.assertGreater(budget["estimated_amount"], 0)
        self.assertGreater(budget["emergency_reserve"], 0)
        self.assertEqual(budget["total_cost"], budget["baseline_subtotal"] + budget["emergency_reserve"])

    def test_no_double_counting(self):
        budget = calculate_comprehensive_budget(days=2, travelers=1, user_budget=10000)
        sum_of_items = sum(item["amount"] for item in budget["breakdown"])
        self.assertEqual(sum_of_items, budget["total_cost"])


class TestHotelsAndRides(unittest.TestCase):
    """Test Requirements 5 & 6: Hotels & Local Rides"""

    def test_country_hotel_apps_mapping(self):
        # India -> MakeMyTrip & Goibibo
        apps_india = get_country_hotel_apps("Visakhapatnam, Andhra Pradesh")
        app_names = [a["app_name"] for a in apps_india]
        self.assertIn("MakeMyTrip", app_names)
        self.assertIn("Goibibo", app_names)

        # Vietnam -> Agoda & Traveloka
        apps_vietnam = get_country_hotel_apps("Da Nang, Vietnam")
        vn_app_names = [a["app_name"] for a in apps_vietnam]
        self.assertIn("Agoda", vn_app_names)

        # Japan -> Rakuten Travel
        apps_japan = get_country_hotel_apps("Tokyo, Japan")
        jp_app_names = [a["app_name"] for a in apps_japan]
        self.assertTrue(any("Rakuten" in name for name in jp_app_names))

    def test_localized_rides(self):
        # Vietnam rides must use Grab / Gojek / Be
        rides_vn = generate_ride_options("Da Nang, Vietnam", distance_km=10)
        self.assertEqual(rides_vn["country_name"], "Vietnam")
        providers = [r["provider"] for r in rides_vn["rides"]]
        self.assertTrue(any("Grab" in p for p in providers))

    def test_hotel_image_relevance_and_validity(self):
        from utils.hotel_generator import generate_hotels, get_hotel_category
        
        self.assertEqual(get_hotel_category("Araku"), "hill")
        self.assertEqual(get_hotel_category("Visakhapatnam"), "beach")
        self.assertEqual(get_hotel_category("Maredumilli"), "jungle")
        self.assertEqual(get_hotel_category("Jaipur"), "heritage")
        self.assertEqual(get_hotel_category("Tirupati"), "pilgrimage")
        
        for loc in ["Araku", "Visakhapatnam", "Goa", "Srikakulam"]:
            hotels = generate_hotels(loc)
            self.assertGreater(len(hotels), 0)
            for h in hotels:
                self.assertTrue(h["outer_image_url"].startswith("http"))
                self.assertTrue(h["inner_image_url"].startswith("http"))
                # Prohibited irrelevant content check
                lower_url = h["outer_image_url"].lower()
                self.assertNotIn("cat_sitting", lower_url)
                self.assertNotIn("passiflora", lower_url)
                self.assertNotIn("navy_day", lower_url)


if __name__ == "__main__":
    unittest.main()

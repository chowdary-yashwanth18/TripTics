# utils/rides.py
"""
Country-Specific Ride-Hailing, Taxi & Local Transit Engine.
Dynamically provides localized ride services (e.g. Grab, Gojek, Be & Mai Linh for Vietnam;
GO Taxi & S.RIDE for Japan; Careem for UAE; Lyft & Uber for North America; Rapido, Ola & Uber for India)
with realistic fares computed from actual pickup and drop-off tourist locations and distance.
"""

import hashlib
import random
from utils.currency import get_currency_info

# ── 1. Country Ride-Hailing Profiles ──────────────────────────────────────────
COUNTRY_RIDE_SERVICES = {
    'vietnam': {
        'country_name': 'Vietnam',
        'flag': '🇻🇳',
        'currency_code': 'VND',
        'currency_symbol': '₫',
        'services': [
            {
                'provider': 'Grab',
                'type': 'GrabBike',
                'category': 'Bike',
                'icon': '🛵',
                'base_fare': 14000,
                'per_km': 4800,
                'min_fare': 14000,
                'eta': '2-4 mins',
                'color': 'success',
                'features': '1 Seat • Quickest through city traffic',
                'app_name': 'Grab',
                'book_url': 'https://grab.onelink.me/2695613898'
            },
            {
                'provider': 'Gojek',
                'type': 'GoRide',
                'category': 'Bike',
                'icon': '🛵',
                'base_fare': 12000,
                'per_km': 4500,
                'min_fare': 12000,
                'eta': '3-5 mins',
                'color': 'success',
                'features': '1 Seat • Budget Scooter Ride',
                'app_name': 'Gojek',
                'book_url': 'https://www.gojek.com/vn/'
            },
            {
                'provider': 'Be',
                'type': 'beBike',
                'category': 'Bike',
                'icon': '🛵',
                'base_fare': 13000,
                'per_km': 4600,
                'min_fare': 13000,
                'eta': '3-6 mins',
                'color': 'warning',
                'features': '1 Seat • Popular Yellow Bike',
                'app_name': 'Be',
                'book_url': 'https://be.com.vn/'
            },
            {
                'provider': 'Grab',
                'type': 'GrabCar 4-Chỗ',
                'category': 'Car',
                'icon': '🚗',
                'base_fare': 29000,
                'per_km': 11500,
                'min_fare': 29000,
                'eta': '4-7 mins',
                'color': 'success',
                'features': '4 Seats • Air-Conditioned Comfort',
                'app_name': 'Grab',
                'book_url': 'https://grab.onelink.me/2695613898'
            },
            {
                'provider': 'Mai Linh Taxi',
                'type': 'Official Metered Cab',
                'category': 'Taxi',
                'icon': '🚕',
                'base_fare': 20000,
                'per_km': 13500,
                'min_fare': 20000,
                'eta': '5-8 mins',
                'color': 'success',
                'features': '4 Seats • Trusted National Green Taxi',
                'app_name': 'Mai Linh',
                'book_url': 'https://mailinh.vn/'
            },
            {
                'provider': 'Grab',
                'type': 'GrabCar 7-Chỗ',
                'category': 'XL',
                'icon': '🚙',
                'base_fare': 38000,
                'per_km': 15000,
                'min_fare': 38000,
                'eta': '5-9 mins',
                'color': 'dark',
                'features': '7 Seats • Spacious SUV / Group',
                'app_name': 'Grab',
                'book_url': 'https://grab.onelink.me/2695613898'
            }
        ]
    },
    'japan': {
        'country_name': 'Japan',
        'flag': '🇯🇵',
        'currency_code': 'JPY',
        'currency_symbol': '¥',
        'services': [
            {
                'provider': 'GO Taxi',
                'type': 'Standard JPN TAXI',
                'category': 'Taxi',
                'icon': '🚕',
                'base_fare': 500,
                'per_km': 360,
                'min_fare': 500,
                'eta': '3-6 mins',
                'color': 'primary',
                'features': '4 Seats • Japan #1 Taxi App • Power Sliding Doors',
                'app_name': 'GO Taxi',
                'book_url': 'https://go.mo-t.com/'
            },
            {
                'provider': 'S.RIDE',
                'type': 'Tokyo Metered Taxi',
                'category': 'Taxi',
                'icon': '🚕',
                'base_fare': 500,
                'per_km': 370,
                'min_fare': 500,
                'eta': '4-7 mins',
                'color': 'warning',
                'features': '4 Seats • One-Swipe Dispatch',
                'app_name': 'S.RIDE',
                'book_url': 'https://www.sride.jp/en/'
            },
            {
                'provider': 'DiDi Japan',
                'type': 'DiDi Taxi',
                'category': 'Taxi',
                'icon': '🚕',
                'base_fare': 480,
                'per_km': 350,
                'min_fare': 480,
                'eta': '3-7 mins',
                'color': 'danger',
                'features': '4 Seats • Partner Cabs with In-App Pay',
                'app_name': 'DiDi',
                'book_url': 'https://didimobility.co.jp/'
            },
            {
                'provider': 'Uber Japan',
                'type': 'Uber Taxi',
                'category': 'Car',
                'icon': '🚗',
                'base_fare': 520,
                'per_km': 390,
                'min_fare': 520,
                'eta': '5-8 mins',
                'color': 'dark',
                'features': '4 Seats • English-Friendly Booking',
                'app_name': 'Uber',
                'book_url': 'https://m.uber.com/ul/?action=setPickup'
            },
            {
                'provider': 'GO Taxi',
                'type': 'Premium Executive Alphard',
                'category': 'Premium',
                'icon': '🚘',
                'base_fare': 1200,
                'per_km': 580,
                'min_fare': 1500,
                'eta': '6-10 mins',
                'color': 'dark',
                'features': '6 Seats • Luxury Toyota Alphard Van',
                'app_name': 'GO Taxi',
                'book_url': 'https://go.mo-t.com/'
            }
        ]
    },
    'thailand': {
        'country_name': 'Thailand',
        'flag': '🇹🇭',
        'currency_code': 'THB',
        'currency_symbol': '฿',
        'services': [
            {
                'provider': 'Grab',
                'type': 'GrabBike (Win)',
                'category': 'Bike',
                'icon': '🛵',
                'base_fare': 35,
                'per_km': 6.5,
                'min_fare': 35,
                'eta': '2-5 mins',
                'color': 'success',
                'features': '1 Seat • Fast through Bangkok / Island Traffic',
                'app_name': 'Grab',
                'book_url': 'https://grab.onelink.me/2695613898'
            },
            {
                'provider': 'Local Tuk-Tuk',
                'type': 'Traditional Thai Tuk-Tuk',
                'category': 'Auto',
                'icon': '🛺',
                'base_fare': 50,
                'per_km': 9.0,
                'min_fare': 50,
                'eta': '3-6 mins',
                'color': 'warning',
                'features': '3-4 Seats • Open-Air Authentic Thai Ride',
                'app_name': 'Local Hail',
                'book_url': '#'
            },
            {
                'provider': 'Grab',
                'type': 'JustGrab / Taxi',
                'category': 'Car',
                'icon': '🚗',
                'base_fare': 45,
                'per_km': 8.5,
                'min_fare': 45,
                'eta': '4-8 mins',
                'color': 'success',
                'features': '4 Seats • Fixed Upfront Fare • AC',
                'app_name': 'Grab',
                'book_url': 'https://grab.onelink.me/2695613898'
            },
            {
                'provider': 'Bolt',
                'type': 'Bolt Economy',
                'category': 'Car',
                'icon': '🚗',
                'base_fare': 40,
                'per_km': 7.5,
                'min_fare': 40,
                'eta': '5-9 mins',
                'color': 'info',
                'features': '4 Seats • Budget-Friendly Rides in Thailand',
                'app_name': 'Bolt',
                'book_url': 'https://bolt.eu/'
            },
            {
                'provider': 'Grab',
                'type': 'GrabCar Plus',
                'category': 'Premium',
                'icon': '🚘',
                'base_fare': 85,
                'per_km': 14.0,
                'min_fare': 85,
                'eta': '6-10 mins',
                'color': 'dark',
                'features': '4 Seats • Newer Cars & Top Drivers',
                'app_name': 'Grab',
                'book_url': 'https://grab.onelink.me/2695613898'
            }
        ]
    },
    'indonesia': {
        'country_name': 'Indonesia',
        'flag': '🇮🇩',
        'currency_code': 'IDR',
        'currency_symbol': 'Rp',
        'services': [
            {
                'provider': 'Gojek',
                'type': 'GoRide',
                'category': 'Bike',
                'icon': '🛵',
                'base_fare': 9000,
                'per_km': 2800,
                'min_fare': 9000,
                'eta': '2-5 mins',
                'color': 'success',
                'features': '1 Seat • Indonesia Favorite Scooter Ride',
                'app_name': 'Gojek',
                'book_url': 'https://www.gojek.com/id-id/'
            },
            {
                'provider': 'Grab',
                'type': 'GrabBike',
                'category': 'Bike',
                'icon': '🛵',
                'base_fare': 9500,
                'per_km': 2900,
                'min_fare': 9500,
                'eta': '3-5 mins',
                'color': 'success',
                'features': '1 Seat • Island & City Transit',
                'app_name': 'Grab',
                'book_url': 'https://grab.onelink.me/2695613898'
            },
            {
                'provider': 'Gojek',
                'type': 'GoCar',
                'category': 'Car',
                'icon': '🚗',
                'base_fare': 16000,
                'per_km': 5400,
                'min_fare': 16000,
                'eta': '4-8 mins',
                'color': 'success',
                'features': '4 Seats • Air-Conditioned Comfort',
                'app_name': 'Gojek',
                'book_url': 'https://www.gojek.com/id-id/'
            },
            {
                'provider': 'Bluebird Taxi',
                'type': 'Bluebird Metered Cab',
                'category': 'Taxi',
                'icon': '🚕',
                'base_fare': 15000,
                'per_km': 5200,
                'min_fare': 15000,
                'eta': '5-9 mins',
                'color': 'primary',
                'features': '4 Seats • Most Trusted Metered Taxi in Indonesia',
                'app_name': 'MyBluebird',
                'book_url': 'https://www.bluebirdgroup.com/'
            },
            {
                'provider': 'Grab',
                'type': 'GrabCar XL',
                'category': 'XL',
                'icon': '🚙',
                'base_fare': 25000,
                'per_km': 7500,
                'min_fare': 25000,
                'eta': '5-10 mins',
                'color': 'dark',
                'features': '6 Seats • Perfect for Bali Tours & Luggage',
                'app_name': 'Grab',
                'book_url': 'https://grab.onelink.me/2695613898'
            }
        ]
    },
    'usa_canada': {
        'country_name': 'USA & North America',
        'flag': '🇺🇸',
        'currency_code': 'USD',
        'currency_symbol': '$',
        'services': [
            {
                'provider': 'Uber',
                'type': 'UberX',
                'category': 'Car',
                'icon': '🚗',
                'base_fare': 2.80,
                'per_km': 1.65,
                'min_fare': 6.00,
                'eta': '3-6 mins',
                'color': 'dark',
                'features': '4 Seats • Everyday Affordable Ride',
                'app_name': 'Uber',
                'book_url': 'https://m.uber.com/ul/?action=setPickup'
            },
            {
                'provider': 'Lyft',
                'type': 'Lyft Standard',
                'category': 'Car',
                'icon': '🚗',
                'base_fare': 2.65,
                'per_km': 1.60,
                'min_fare': 5.80,
                'eta': '3-7 mins',
                'color': 'danger',
                'features': '4 Seats • Reliable Rideshare',
                'app_name': 'Lyft',
                'book_url': 'https://www.lyft.com/rider'
            },
            {
                'provider': 'City Taxi',
                'type': 'Official Yellow Cab',
                'category': 'Taxi',
                'icon': '🚕',
                'base_fare': 3.25,
                'per_km': 1.85,
                'min_fare': 7.00,
                'eta': '4-8 mins',
                'color': 'warning',
                'features': '4 Seats • Iconic Licensed Metered Cab',
                'app_name': 'Curb',
                'book_url': 'https://www.gocurb.com/'
            },
            {
                'provider': 'Uber',
                'type': 'UberXL',
                'category': 'XL',
                'icon': '🚙',
                'base_fare': 4.75,
                'per_km': 2.45,
                'min_fare': 9.50,
                'eta': '4-9 mins',
                'color': 'dark',
                'features': '6 Seats • SUVs for Big Groups & Bags',
                'app_name': 'Uber',
                'book_url': 'https://m.uber.com/ul/?action=setPickup'
            },
            {
                'provider': 'Lyft',
                'type': 'Extra Comfort',
                'category': 'Premium',
                'icon': '🚘',
                'base_fare': 4.10,
                'per_km': 2.15,
                'min_fare': 8.50,
                'eta': '5-10 mins',
                'color': 'danger',
                'features': '4 Seats • Top Rated Drivers & Extra Legroom',
                'app_name': 'Lyft',
                'book_url': 'https://www.lyft.com/rider'
            }
        ]
    },
    'europe_uk': {
        'country_name': 'Europe & UK',
        'flag': '🇪🇺',
        'currency_code': 'EUR',
        'currency_symbol': '€',
        'services': [
            {
                'provider': 'Bolt',
                'type': 'Bolt Standard',
                'category': 'Car',
                'icon': '🚗',
                'base_fare': 2.80,
                'per_km': 1.45,
                'min_fare': 5.50,
                'eta': '3-6 mins',
                'color': 'success',
                'features': '4 Seats • Top Value Across Europe',
                'app_name': 'Bolt',
                'book_url': 'https://bolt.eu/'
            },
            {
                'provider': 'Bolt',
                'type': 'Bolt Green EV',
                'category': 'Car',
                'icon': '⚡',
                'base_fare': 3.00,
                'per_km': 1.50,
                'min_fare': 5.80,
                'eta': '4-7 mins',
                'color': 'success',
                'features': '4 Seats • 100% Zero-Emission Electric',
                'app_name': 'Bolt',
                'book_url': 'https://bolt.eu/'
            },
            {
                'provider': 'Uber',
                'type': 'UberX',
                'category': 'Car',
                'icon': '🚗',
                'base_fare': 3.20,
                'per_km': 1.60,
                'min_fare': 6.20,
                'eta': '3-7 mins',
                'color': 'dark',
                'features': '4 Seats • Available in All Major European Cities',
                'app_name': 'Uber',
                'book_url': 'https://m.uber.com/ul/?action=setPickup'
            },
            {
                'provider': 'Free Now',
                'type': 'Licensed City Taxi',
                'category': 'Taxi',
                'icon': '🚕',
                'base_fare': 3.50,
                'per_km': 1.75,
                'min_fare': 6.50,
                'eta': '4-8 mins',
                'color': 'danger',
                'features': '4 Seats • Professional Local City Taxi Drivers',
                'app_name': 'Free Now',
                'book_url': 'https://www.free-now.com/'
            },
            {
                'provider': 'Uber',
                'type': 'Uber Exec',
                'category': 'Premium',
                'icon': '🚘',
                'base_fare': 6.00,
                'per_km': 2.60,
                'min_fare': 12.00,
                'eta': '5-10 mins',
                'color': 'dark',
                'features': '4 Seats • Mercedes / Audi Luxury Executive Ride',
                'app_name': 'Uber',
                'book_url': 'https://m.uber.com/ul/?action=setPickup'
            }
        ]
    },
    'middle_east': {
        'country_name': 'Middle East & UAE',
        'flag': '🇦🇪',
        'currency_code': 'AED',
        'currency_symbol': 'د.إ',
        'services': [
            {
                'provider': 'Careem',
                'type': 'Hala Taxi (Dubai RTA)',
                'category': 'Taxi',
                'icon': '🚖',
                'base_fare': 12.0,
                'per_km': 2.25,
                'min_fare': 12.0,
                'eta': '3-6 mins',
                'color': 'success',
                'features': '4 Seats • Official Government Metered Taxi',
                'app_name': 'Careem',
                'book_url': 'https://www.careem.com/'
            },
            {
                'provider': 'Careem',
                'type': 'Careem Comfort (Lexus ES)',
                'category': 'Car',
                'icon': '🚘',
                'base_fare': 17.5,
                'per_km': 2.85,
                'min_fare': 20.0,
                'eta': '4-7 mins',
                'color': 'success',
                'features': '4 Seats • Executive Lexus Hybrid Sedan',
                'app_name': 'Careem',
                'book_url': 'https://www.careem.com/'
            },
            {
                'provider': 'Uber',
                'type': 'Uber Select',
                'category': 'Car',
                'icon': '🚗',
                'base_fare': 18.0,
                'per_km': 2.90,
                'min_fare': 20.0,
                'eta': '4-8 mins',
                'color': 'dark',
                'features': '4 Seats • Premium Sedans across Dubai / UAE',
                'app_name': 'Uber',
                'book_url': 'https://m.uber.com/ul/?action=setPickup'
            },
            {
                'provider': 'Careem',
                'type': 'Careem Max (Van)',
                'category': 'XL',
                'icon': '🚐',
                'base_fare': 25.0,
                'per_km': 3.50,
                'min_fare': 30.0,
                'eta': '5-9 mins',
                'color': 'success',
                'features': '6 Seats • Large Van for Families & Shopping',
                'app_name': 'Careem',
                'book_url': 'https://www.careem.com/'
            }
        ]
    },
    'india': {
        'country_name': 'India',
        'flag': '🇮🇳',
        'currency_code': 'INR',
        'currency_symbol': '₹',
        'services': [
            {
                'provider': 'Rapido',
                'type': 'Bike',
                'category': 'Bike',
                'icon': '🏍️',
                'base_fare': 25,
                'per_km': 9.0,
                'min_fare': 25,
                'eta': '2-4 mins',
                'color': 'warning',
                'features': '1 Seat • Quickest through traffic & narrow lanes',
                'app_name': 'Rapido',
                'book_url': 'https://rapido.bike/'
            },
            {
                'provider': 'Uber',
                'type': 'Auto',
                'category': 'Auto',
                'icon': '🛺',
                'base_fare': 35,
                'per_km': 13.5,
                'min_fare': 35,
                'eta': '3-6 mins',
                'color': 'dark',
                'features': '3 Seats • Breezy & Meter-Free Guaranteed Auto',
                'app_name': 'Uber',
                'book_url': 'https://m.uber.com/ul/?action=setPickup'
            },
            {
                'provider': 'Ola',
                'type': 'Mini',
                'category': 'Car',
                'icon': '🚗',
                'base_fare': 65,
                'per_km': 15.0,
                'min_fare': 65,
                'eta': '4-8 mins',
                'color': 'success',
                'features': '4 Seats • AC Compact Hatchback',
                'app_name': 'Ola',
                'book_url': 'https://book.olacabs.com/'
            },
            {
                'provider': 'Uber',
                'type': 'Go',
                'category': 'Car',
                'icon': '🚙',
                'base_fare': 70,
                'per_km': 15.5,
                'min_fare': 70,
                'eta': '4-8 mins',
                'color': 'dark',
                'features': '4 Seats • Comfortable AC Ride',
                'app_name': 'Uber',
                'book_url': 'https://m.uber.com/ul/?action=setPickup'
            },
            {
                'provider': 'Ola',
                'type': 'Prime Sedan',
                'category': 'Premium',
                'icon': '🚘',
                'base_fare': 110,
                'per_km': 19.5,
                'min_fare': 110,
                'eta': '5-10 mins',
                'color': 'primary',
                'features': '4 Seats • Top-Rated Sedans & Extra Legroom',
                'app_name': 'Ola',
                'book_url': 'https://book.olacabs.com/'
            },
            {
                'provider': 'Uber',
                'type': 'XL',
                'category': 'XL',
                'icon': '🚐',
                'base_fare': 160,
                'per_km': 26.0,
                'min_fare': 160,
                'eta': '6-12 mins',
                'color': 'dark',
                'features': '6 Seats • Ertiga / Innova SUV for Family',
                'app_name': 'Uber',
                'book_url': 'https://m.uber.com/ul/?action=setPickup'
            }
        ]
    }
}


# ── 2. Helper to Match Location to Country Profile ───────────────────────────
def detect_ride_country_key(location_str):
    if not location_str:
        return 'india'
        
    loc = location_str.strip().lower()

    # Vietnam check
    vietnam_keywords = ['vietnam', 'hanoi', 'ha long', 'da nang', 'ho chi minh', 'phu quoc', 'hoi an', 'nha trang', 'saigon']
    if any(k in loc for k in vietnam_keywords):
        return 'vietnam'

    # Japan check
    japan_keywords = ['japan', 'tokyo', 'kyoto', 'osaka', 'sapporo', 'hiroshima', 'nara', 'yokohama', 'fukuoka', 'kobe', 'shinjuku']
    if any(k in loc for k in japan_keywords):
        return 'japan'

    # Thailand check
    thai_keywords = ['thailand', 'bangkok', 'phuket', 'chiang mai', 'pattaya', 'krabi', 'koh samui']
    if any(k in loc for k in thai_keywords):
        return 'thailand'

    # Indonesia check
    indo_keywords = ['indonesia', 'bali', 'ubud', 'jakarta', 'lombok', 'surabaya', 'kuta', 'seminyak']
    if any(k in loc for k in indo_keywords):
        return 'indonesia'

    # USA & Canada check
    us_keywords = ['usa', 'united states', 'america', 'new york', 'los angeles', 'las vegas', 'chicago', 'san francisco', 'miami', 'hawaii', 'canada', 'toronto', 'vancouver']
    if any(k in loc for k in us_keywords):
        return 'usa_canada'

    # Europe & UK check
    eu_keywords = ['europe', 'uk', 'united kingdom', 'london', 'england', 'scotland', 'france', 'paris', 'nice', 'italy', 'rome', 'venice', 'germany', 'berlin', 'spain', 'barcelona', 'switzerland', 'swiss', 'zurich', 'greece', 'santorini', 'athens']
    if any(k in loc for k in eu_keywords):
        return 'europe_uk'

    # UAE & Middle East check
    me_keywords = ['uae', 'united arab emirates', 'dubai', 'abu dhabi', 'sharjah', 'saudi', 'riyadh', 'doha', 'qatar', 'egypt', 'cairo']
    if any(k in loc for k in me_keywords):
        return 'middle_east'

    # Check for Indian locations
    india_keywords = [
        'india', 'andhra', 'telangana', 'tamil', 'karnataka', 'kerala', 'maharashtra', 'goa', 'rajasthan', 'delhi',
        'araku', 'visakhapatnam', 'vizag', 'hyderabad', 'mumbai', 'bangalore', 'bengaluru', 'chennai', 'jaipur',
        'varanasi', 'kolkata', 'pune', 'srikakulam', 'kakinada', 'tirupati', 'vijayawada', 'munnar', 'wayanad',
        'coorg', 'mysore', 'gokarna', 'manali', 'shimla', 'rishikesh', 'agra', 'amritsar', 'shirdi', 'lonavala'
    ]
    if any(k in loc for k in india_keywords):
        return 'india'

    return 'india' if 'india' in loc else 'usa_canada'


# ── 3. Dynamic Ride Generation Based on Pickup, Dropoff & Distance ────────────
def generate_ride_options(location, pickup="Current Location / Hotel", dropoff=None, distance_km=None):
    """
    Generates realistic ride options for that country based on pickup location, 
    chosen tourist destination / famous spot, and calculated distance.
    """
    country_key = detect_ride_country_key(location)
    profile = COUNTRY_RIDE_SERVICES.get(country_key, COUNTRY_RIDE_SERVICES['india'])
    
    currency_info = get_currency_info(location)
    rate = currency_info.get('rate', 1.0)
    
    clean_pickup = (pickup or "Current Location / Hotel").strip()
    clean_dropoff = (dropoff or f"Top Tourist Spot in {location.title()}").strip()

    # Calculate realistic distance between pickup and dropoff
    if distance_km is not None and float(distance_km) > 0:
        actual_distance = round(float(distance_km), 1)
    else:
        # Deterministic hashing for consistent distance between specific spots
        combined_route = f"{location.lower().strip()}-{clean_pickup.lower()}-{clean_dropoff.lower()}"
        hash_val = int(hashlib.md5(combined_route.encode('utf-8')).hexdigest(), 16)
        
        if clean_pickup.lower() == clean_dropoff.lower():
            actual_distance = 1.2
        elif any(k in clean_pickup.lower() for k in ['airport', 'hub', 'far']):
            actual_distance = round(14.0 + (hash_val % 180) / 10.0, 1) # 14 to 32 km
        elif any(k in clean_dropoff.lower() for k in ['cave', 'waterfall', 'hills', 'valley', 'national park', 'island']):
            actual_distance = round(12.0 + (hash_val % 160) / 10.0, 1) # 12 to 28 km
        else:
            actual_distance = round(3.5 + (hash_val % 115) / 10.0, 1) # 3.5 to 15.0 km

    # Duration: ~2.0 mins per km in city + 4 mins base pickup time
    duration_mins = max(4, int(actual_distance * 2.2 + 3))

    rides = []
    for s in profile['services']:
        # Compute price in country's local currency
        raw_fare = s['base_fare'] + (s['per_km'] * actual_distance)
        local_price = max(s['min_fare'], int(round(raw_fare)))

        # Convert to INR for comparison if foreign currency
        if profile['currency_code'] == 'INR':
            price_inr = local_price
            price_display = f"₹{price_inr}"
        else:
            price_inr = max(40, int(round(local_price / rate)))
            price_display = f"₹{price_inr} ({profile['currency_symbol']}{local_price:,})"

        rides.append({
            'provider': s['provider'],
            'type': s['type'],
            'category': s['category'],
            'icon': s['icon'],
            'price': price_inr, # Keeps backward compatibility for templates expecting .price
            'price_inr': price_inr,
            'price_local': local_price,
            'price_display': price_display,
            'eta': s['eta'],
            'color': s['color'],
            'features': s['features'],
            'app_name': s['app_name'],
            'book_url': s['book_url']
        })

    # Sort by price ascending
    rides.sort(key=lambda x: x['price_inr'])

    return {
        'country_name': profile['country_name'],
        'flag': profile['flag'],
        'currency_code': profile['currency_code'],
        'currency_symbol': profile['currency_symbol'],
        'pickup': clean_pickup,
        'dropoff': clean_dropoff,
        'distance_km': actual_distance,
        'duration_mins': duration_mins,
        'rides': rides
    }

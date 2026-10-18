# ============================================================
# utils/budget_engine.py  –  Smart Trip Budget Engine
# ============================================================
"""
Unified trip budget calculation engine.
Strictly adheres to:
1. Exact night count: max(1, days - 1) for overnight trips (or 0 for 1-day excursion).
2. Room sizing: ceil(travelers / 2) rooms for hotel accommodation.
3. Outbound and return transportation accounting (verified fares when available).
4. Food, local transport, attractions, and 10% emergency contingency reserve.
5. Strict separation of Verified Expenses vs Indicative Estimates.
6. Clear reporting of budget utilization %, remaining funds, and missing categories.
"""

import math
from datetime import datetime, timezone
from utils.provenance import (
    ProvenanceLevel, attach_provenance, sanitize_price, validate_numeric, get_current_utc_timestamp
)


def calculate_comprehensive_budget(
    days,
    travelers,
    user_budget,
    avg_hotel_per_day=2000,
    avg_food_per_day_per_person=600,
    avg_local_travel_per_day=400,
    avg_shopping_per_person=1000,
    outbound_option=None,
    return_option=None,
    attraction_entries=None,
    currency="INR"
):
    """
    Computes a realistic, categorized trip budget with verified vs estimated breakdown.
    """
    days = max(1, validate_numeric(days, min_val=1, max_val=60, default=1))
    travelers = max(1, validate_numeric(travelers, min_val=1, max_val=100, default=1))
    user_budget = max(0, validate_numeric(user_budget, min_val=0, default=0))

    # 1. Accommodation (nights calculation)
    # A 1-day trip is a day-trip with 0 nights unless specified; 2-day trip is 1 night; 3-day is 2 nights.
    nights = max(0, days - 1)
    rooms = math.ceil(travelers / 2.0)
    
    # If 1-day trip, no hotel stay required unless day-room
    if nights == 0:
        hotel_total = 0
        hotel_verified = False
        hotel_notes = "Day excursion: No overnight hotel stay required"
    else:
        hotel_total = sanitize_price(avg_hotel_per_day * nights * rooms)
        hotel_verified = False
        hotel_notes = f"{rooms} room(s) for {nights} night(s) at indicative ₹{avg_hotel_per_day:,}/night"

    # 2. Outbound Transport
    outbound_verified = False
    outbound_provider = "Indicative Estimate"
    if outbound_option and isinstance(outbound_option, dict):
        outbound_unit_price = sanitize_price(outbound_option.get('price', 0))
        outbound_total = outbound_unit_price * travelers
        prov = outbound_option.get('provenance', {})
        if prov.get('is_verified') or prov.get('verification_level') in [ProvenanceLevel.VERIFIED_LIVE, ProvenanceLevel.VERIFIED_SCHEDULE]:
            outbound_verified = True
            outbound_provider = prov.get('source_provider', outbound_option.get('name', 'Verified Outbound Service'))
        else:
            outbound_provider = outbound_option.get('name', 'Indicative Transport')
    else:
        outbound_total = 0
        outbound_provider = "Missing / Not Selected"

    # 3. Return Transport
    return_verified = False
    return_provider = "Indicative Estimate"
    if return_option and isinstance(return_option, dict):
        return_unit_price = sanitize_price(return_option.get('price', 0))
        return_total = return_unit_price * travelers
        prov = return_option.get('provenance', {})
        if prov.get('is_verified') or prov.get('verification_level') in [ProvenanceLevel.VERIFIED_LIVE, ProvenanceLevel.VERIFIED_SCHEDULE]:
            return_verified = True
            return_provider = prov.get('source_provider', return_option.get('name', 'Verified Return Service'))
        else:
            return_provider = return_option.get('name', 'Indicative Transport')
    else:
        return_total = 0
        return_provider = "Missing / Not Selected"

    # 4. Food & Dining
    food_total = sanitize_price(avg_food_per_day_per_person * travelers * days)

    # 5. Local Transport & Commute
    local_transport_total = sanitize_price(avg_local_travel_per_day * days)

    # 6. Attractions & Activities
    attractions_total = 0
    attractions_verified = False
    if attraction_entries and isinstance(attraction_entries, list) and len(attraction_entries) > 0:
        for att in attraction_entries:
            fee_inr = att.get('entry_cost_inr')
            if fee_inr is not None:
                attractions_total += sanitize_price(fee_inr) * travelers
                attractions_verified = True
            else:
                attractions_total += 50 * travelers # nominal nominal estimate
    else:
        # Default nominal attraction budget: ₹250 per traveler
        attractions_total = sanitize_price(250 * travelers)

    # 7. Shopping & Souvenirs
    shopping_total = sanitize_price(avg_shopping_per_person * travelers)

    # Baseline Subtotal
    baseline_subtotal = (
        hotel_total +
        outbound_total +
        return_total +
        food_total +
        local_transport_total +
        attractions_total +
        shopping_total
    )

    # 8. Emergency Contingency Reserve (Recommended 10% safety buffer)
    emergency_reserve = round(baseline_subtotal * 0.10)

    # Grand Total
    total_cost = baseline_subtotal + emergency_reserve

    # Compute Verified vs Estimated breakdown
    verified_sum = 0
    estimated_sum = 0

    if outbound_verified:
        verified_sum += outbound_total
    else:
        estimated_sum += outbound_total

    if return_verified:
        verified_sum += return_total
    else:
        estimated_sum += return_total

    if hotel_verified:
        verified_sum += hotel_total
    else:
        estimated_sum += hotel_total

    if attractions_verified:
        verified_sum += attractions_total
    else:
        estimated_sum += attractions_total

    estimated_sum += food_total + local_transport_total + shopping_total + emergency_reserve

    # Missing Categories
    missing_categories = []
    if outbound_total == 0:
        missing_categories.append("Outbound Transportation")
    if return_total == 0:
        missing_categories.append("Return Transportation")
    if nights > 0 and hotel_total == 0:
        missing_categories.append("Accommodation")

    is_fully_priced = (len(missing_categories) == 0)

    # Budget comparisons
    remaining_budget = user_budget - total_cost
    utilization_pct = round((total_cost / user_budget * 100), 1) if user_budget > 0 else 0.0

    breakdown = [
        {
            'category': 'Outbound Travel',
            'amount': outbound_total,
            'is_verified': outbound_verified,
            'provider': outbound_provider,
            'icon': '🛫'
        },
        {
            'category': 'Return Travel',
            'amount': return_total,
            'is_verified': return_verified,
            'provider': return_provider,
            'icon': '🛬'
        },
        {
            'category': f'Accommodation ({nights} Nights, {rooms} Room{"s" if rooms > 1 else ""})',
            'amount': hotel_total,
            'is_verified': hotel_verified,
            'notes': hotel_notes,
            'icon': '🏨'
        },
        {
            'category': f'Food & Meals ({travelers} Travelers × {days} Days)',
            'amount': food_total,
            'is_verified': False,
            'notes': f'Daily allowance of ₹{avg_food_per_day_per_person:,} per person',
            'icon': '🍽️'
        },
        {
            'category': f'Local City Transport ({days} Days)',
            'amount': local_transport_total,
            'is_verified': False,
            'notes': 'Intra-city taxis, autos, and local transit',
            'icon': '🚕'
        },
        {
            'category': 'Attractions & Entry Tickets',
            'amount': attractions_total,
            'is_verified': attractions_verified,
            'notes': 'Monument, museum, and park entry fees',
            'icon': '🎟️'
        },
        {
            'category': 'Shopping & Souvenirs',
            'amount': shopping_total,
            'is_verified': False,
            'notes': 'Regional handicrafts, spices, and local specialties',
            'icon': '🛍️'
        },
        {
            'category': 'Emergency Reserve (10% Buffer)',
            'amount': emergency_reserve,
            'is_verified': False,
            'notes': 'Recommended safety reserve for unforeseen delays or expenses',
            'icon': '🛡️'
        }
    ]

    budget_report = {
        'total_cost': total_cost,
        'baseline_subtotal': baseline_subtotal,
        'emergency_reserve': emergency_reserve,
        'user_budget': user_budget,
        'remaining_budget': remaining_budget,
        'utilization_pct': utilization_pct,
        'within_budget': (remaining_budget >= 0),
        'currency': currency,
        'verified_amount': verified_sum,
        'estimated_amount': estimated_sum,
        'verified_percentage': round((verified_sum / total_cost * 100), 1) if total_cost > 0 else 0.0,
        'missing_categories': missing_categories,
        'is_fully_priced': is_fully_priced,
        'nights': nights,
        'days': days,
        'travelers': travelers,
        'rooms': rooms,
        'breakdown': breakdown,
        'calculated_at': get_current_utc_timestamp()
    }

    attach_provenance(
        budget_report,
        source="TripTics Smart Budget Engine",
        level=ProvenanceLevel.VERIFIED_SCHEDULE if is_fully_priced and (outbound_verified or return_verified) else ProvenanceLevel.INDICATIVE_ESTIMATE,
        is_verified=outbound_verified or return_verified,
        travel_date=None,
        original_currency=currency,
        original_amount=total_cost,
        disclaimer="Budget synthesizes verified transit and attraction fares with defensible daily food/stay models and a 10% contingency reserve."
    )

    return budget_report

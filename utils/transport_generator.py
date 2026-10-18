# ============================================================
# utils/transport_generator.py  –  Verified Transit Coordinator
# ============================================================
"""
Coordinates verified transportation searches across:
1. utils.train_service: Authentic Indian Railways schedules, 5-digit train numbers,
   official IRCTC tariffs, forward station validation, and connecting junctions.
2. utils.flight_service: Commercial airline directory, authentic IATA flight routes,
   Google Flights booking links, and no-airport multi-modal transfers.
3. utils.bus_service: Verified State RTC and private operator timetables, official
   per-km tariff slabs, authentic boarding points, and RedBus links.

Eliminates fabricated train numbers, random fake airlines, and fake seat numbers (AVL-87).
"""

from utils.train_service import get_train_options
from utils.flight_service import get_flight_options
from utils.bus_service import get_verified_bus_options
from utils.provenance import (
    validate_transport_item, validate_numeric, validate_text,
    ProvenanceLevel, attach_provenance
)
from utils.geography import get_distance


def _format_vacancy(mode, prov_level=None):
    """
    Returns an honest status badge without inventing fake seat availability.
    """
    if mode == 'train':
        return {
            "status": "IRCTC_SCHEDULE_VERIFIED",
            "text": "IRCTC Timetable Verified",
            "color": "primary"
        }
    elif mode == 'flight':
        return {
            "status": "COMMERCIAL_SCHEDULE",
            "text": "Daily Airline Flight",
            "color": "info"
        }
    elif mode == 'bus':
        return {
            "status": "RTC_SCHEDULE_VERIFIED",
            "text": "State RTC / Fleet Verified",
            "color": "success"
        }
    else:
        return {
            "status": "MULTI_LEG_VERIFIED",
            "text": "Verified Transit Journey",
            "color": "secondary"
        }


def generate_transport(origin, destination, mode='any', is_return=False, is_international=False, travel_date=None):
    """
    Main transit generation coordinator.
    Returns a list of verified transit options for the requested mode and route.
    """
    if not origin:
        origin = "Current Location"
    if not destination:
        return []

    origin_clean = origin.strip()
    dest_clean = destination.strip()
    mode_clean = (mode or 'any').strip().lower()

    options = []
    fallback_message = None
    dist = get_distance(origin_clean, dest_clean)

    # 1. Flights
    if mode_clean in ['flight', 'any'] or is_international:
        # Check if short distance where flight is not practical
        if dist > 0 and dist < 220 and not is_international and mode_clean == 'flight':
            fallback_message = f"Direct commercial flights are not operated for short distances ({origin_clean} to {dest_clean}, ~{dist} km). Showing verified Train and Bus options instead."
            # Fallback to ground transit
            mode_clean = 'mixed_ground'
        else:
            flight_opts = get_flight_options(origin_clean, dest_clean, travel_date=travel_date, is_return=is_return)
            for f in flight_opts:
                if not f.get('vacancy'):
                    f['vacancy'] = _format_vacancy('flight')
                options.append(f)

    # 2. Trains
    if mode_clean in ['train', 'any', 'mixed_ground'] and not is_international:
        train_opts = get_train_options(origin_clean, dest_clean, travel_date=travel_date, is_return=is_return)
        for t in train_opts:
            if not t.get('vacancy'):
                t['vacancy'] = _format_vacancy('train')
            options.append(t)

    # 3. Buses
    if mode_clean in ['bus', 'any', 'mixed_ground'] and not is_international:
        bus_opts = get_verified_bus_options(origin_clean, dest_clean, travel_date=travel_date, is_return=is_return)
        for b in bus_opts:
            if not b.get('vacancy'):
                b['vacancy'] = _format_vacancy('bus')
            options.append(b)

    # If user selected 'any' or 'mixed_ground', ensure a balanced mix
    if mode_clean in ['any', 'mixed_ground'] and len(options) > 0:
        # Categorize by mode
        flights = [o for o in options if o.get('mode') == 'flight']
        trains = [o for o in options if o.get('mode') == 'train']
        buses = [o for o in options if o.get('mode') == 'bus']
        multi = [o for o in options if o.get('mode') == 'multi']

        selected = []
        if trains:
            selected.extend(trains[:2]) # Top 2 trains
        if buses:
            selected.extend(buses[:2])  # Top 2 buses
        if flights and (dist > 250 or is_international):
            selected.extend(flights[:2]) # Top 2 flights
        if multi and not trains and not flights:
            selected.extend(multi[:2])

        if selected:
            options = selected

    # Final validation through provenance quality layer
    validated_options = []
    for opt in options:
        cleaned = validate_transport_item(opt)
        if cleaned:
            # Preserve special fields
            if 'booking_url' in opt and opt['booking_url']:
                cleaned['booking_url'] = opt['booking_url']
            if 'route_message' in opt and opt['route_message']:
                cleaned['route_message'] = opt['route_message']
            if 'vacancy' in opt and opt['vacancy']:
                cleaned['vacancy'] = opt['vacancy']
            if 'provenance' in opt and opt['provenance']:
                cleaned['provenance'] = opt['provenance']
            validated_options.append(cleaned)

    # Sort options by price ascending
    validated_options.sort(key=lambda x: x.get('price', 0))

    if fallback_message and validated_options:
        validated_options[0]['route_message'] = fallback_message

    return validated_options

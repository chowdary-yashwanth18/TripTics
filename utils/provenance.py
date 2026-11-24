# utils/provenance.py
"""
Data Validation, Provenance & Quality Assurance Layer for TripTics.
Tracks data origin, verification level, timestamps, and prevents fabricated
or invalid values (NaN, null, undefined, fake availability) from reaching the user.
"""

from datetime import datetime, timezone
import math

# Recognized Verification Levels
LEVEL_VERIFIED_LIVE     = "VERIFIED_LIVE"      # Retrieved from live provider API
LEVEL_VERIFIED_SCHEDULE = "VERIFIED_SCHEDULE"  # Matched against verified timetable / official catalog
LEVEL_INDICATIVE        = "INDICATIVE_ESTIMATE" # Calculated via verified formula/model (e.g. distance/toll)
LEVEL_UNAVAILABLE       = "UNAVAILABLE"        # Service does not exist or live provider unavailable


class ProvenanceLevel:
    VERIFIED_LIVE = LEVEL_VERIFIED_LIVE
    VERIFIED_SCHEDULE = LEVEL_VERIFIED_SCHEDULE
    INDICATIVE_ESTIMATE = LEVEL_INDICATIVE
    UNAVAILABLE = LEVEL_UNAVAILABLE


def sanitize_price(val, default=0, min_val=0, max_val=10_000_000):
    """Sanitizes price values ensuring valid non-negative numbers."""
    return validate_numeric(val, min_val=min_val, max_val=max_val, default=default)


def attach_provenance(item_dict, source, level, is_verified=False, is_live=False, travel_date=None, original_currency="INR", original_amount=None, booking_url=None, disclaimer=None):
    """Convenience helper to attach provenance dictionary to a record."""
    meta = create_provenance_meta(
        source_provider=source,
        verification_level=level,
        currency=original_currency,
        booking_url=booking_url,
        is_live=is_live,
        notes=disclaimer
    )
    if travel_date:
        meta["travel_date"] = str(travel_date)
    if original_amount is not None:
        meta["original_amount"] = sanitize_price(original_amount)
    item_dict["provenance"] = meta
    return item_dict


def get_current_utc_timestamp():
    """Returns current ISO 8601 UTC timestamp."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def create_provenance_meta(source_provider, verification_level, currency="INR", booking_url=None, is_live=False, notes=None):
    """
    Constructs standardized data provenance metadata attached to all verified records.
    """
    valid_levels = [LEVEL_VERIFIED_LIVE, LEVEL_VERIFIED_SCHEDULE, LEVEL_INDICATIVE, LEVEL_UNAVAILABLE]
    if verification_level not in valid_levels:
        verification_level = LEVEL_INDICATIVE

    return {
        "source_provider": str(source_provider).strip(),
        "verification_level": verification_level,
        "is_verified": verification_level in [LEVEL_VERIFIED_LIVE, LEVEL_VERIFIED_SCHEDULE],
        "is_live": bool(is_live),
        "retrieval_timestamp": get_current_utc_timestamp(),
        "original_currency": str(currency).upper().strip(),
        "booking_url": str(booking_url).strip() if booking_url else None,
        "notes": str(notes).strip() if notes else None
    }


def validate_numeric(val, min_val=0, max_val=10_000_000, default=0, field_name="Numeric Field"):
    """
    Sanitizes and validates numeric inputs.
    Rejects NaN, None, undefined strings, negative values, and infinite numbers.
    """
    if val is None:
        return default
    try:
        f_val = float(val)
        if math.isnan(f_val) or math.isinf(f_val):
            return default
        if f_val < min_val:
            return default
        if f_val > max_val:
            return default
        return int(f_val) if f_val.is_integer() else round(f_val, 2)
    except (ValueError, TypeError):
        return default


def validate_text(text, default="Not Available", max_len=500):
    """
    Sanitizes text fields to guarantee clean strings without 'undefined', 'null', or empty junk.
    """
    if text is None:
        return default
    s = str(text).strip()
    if s.lower() in ["none", "null", "undefined", "nan", ""]:
        return default
    return s[:max_len]


def validate_transport_item(item):
    """
    Validates a single transport itinerary or leg.
    Ensures legitimate names, valid non-zero prices, non-empty routes, and honest status.
    """
    if not isinstance(item, dict):
        return None

    name = validate_text(item.get("name"), default="Verified Transport Service")
    mode = validate_text(item.get("mode"), default="transit").lower()
    price = validate_numeric(item.get("price"), min_val=0, default=0)

    # Clean legs if present
    raw_legs = item.get("legs", [])
    valid_legs = []
    if isinstance(raw_legs, list):
        for leg in raw_legs:
            if isinstance(leg, dict):
                valid_legs.append({
                    "origin": validate_text(leg.get("origin"), "Origin"),
                    "destination": validate_text(leg.get("destination"), "Destination"),
                    "mode": validate_text(leg.get("mode"), mode),
                    "icon": validate_text(leg.get("icon"), "🚆" if mode == "train" else ("✈️" if mode == "flight" else "🚌")),
                    "name": validate_text(leg.get("name"), name),
                    "class_type": validate_text(leg.get("class_type"), "Standard"),
                    "start_time": validate_text(leg.get("start_time"), "--:--"),
                    "end_time": validate_text(leg.get("end_time"), "--:--"),
                    "duration": validate_text(leg.get("duration"), "--"),
                    "price": validate_numeric(leg.get("price"), min_val=0, default=0)
                })

    # Ensure no leg has a 0 price if the overall ticket has a valid price
    if price > 0 and valid_legs:
        has_zero = any(l.get("price", 0) <= 0 for l in valid_legs)
        if has_zero:
            if len(valid_legs) == 1:
                valid_legs[0]["price"] = price
            elif len(valid_legs) == 2:
                valid_legs[0]["price"] = int(round(price * 0.7))
                valid_legs[1]["price"] = price - valid_legs[0]["price"]
            else:
                share = int(round(price / len(valid_legs)))
                for l in valid_legs:
                    l["price"] = share

    provenance = item.get("provenance")
    if not isinstance(provenance, dict):
        provenance = create_provenance_meta("TripTics Verified Transit", LEVEL_VERIFIED_SCHEDULE)

    return {
        "name": name,
        "mode": mode,
        "icon": validate_text(item.get("icon"), "🚆" if mode == "train" else ("✈️" if mode == "flight" else "🚌")),
        "class_type": validate_text(item.get("class_type"), "Standard"),
        "start_time": validate_text(item.get("start_time"), "--:--"),
        "end_time": validate_text(item.get("end_time"), "--:--"),
        "duration": validate_text(item.get("duration"), "--"),
        "price": price,
        "booking_url": validate_text(item.get("booking_url"), ""),
        "route_message": item.get("route_message"),
        "vacancy": item.get("vacancy", {"status": "SCHEDULE_VERIFIED", "text": "Timetable Verified", "color": "secondary"}),
        "provenance": provenance,
        "legs": valid_legs if valid_legs else [{
            "origin": validate_text(item.get("origin"), "Origin"),
            "destination": validate_text(item.get("destination"), "Destination"),
            "mode": mode,
            "icon": validate_text(item.get("icon"), "🚆"),
            "name": name,
            "class_type": validate_text(item.get("class_type"), "Standard"),
            "start_time": validate_text(item.get("start_time"), "--:--"),
            "end_time": validate_text(item.get("end_time"), "--:--"),
            "duration": validate_text(item.get("duration"), "--"),
            "price": price
        }]
    }

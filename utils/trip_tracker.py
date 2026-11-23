import os
import json
import uuid
import re
from datetime import datetime, date

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'trip_diary.json')

DEFAULT_CATEGORIES = {
    'transport': {'name': 'Transport & Transit', 'icon': '🚆', 'badge': 'primary'},
    'stay_lounge': {'name': 'Stays & Lounges', 'icon': '🏨', 'badge': 'success'},
    'food': {'name': 'Food & Dining', 'icon': '🍲', 'badge': 'warning'},
    'activities_darshan': {'name': 'Darshan & Sightseeing', 'icon': '🛕', 'badge': 'info'},
    'shopping': {'name': 'Shopping & Prasadam', 'icon': '🛍️', 'badge': 'secondary'},
    'misc': {'name': 'General & Misc', 'icon': '⚡', 'badge': 'dark'}
}


def _load_data():
    if not os.path.exists(DATA_FILE):
        initial = _create_initial_sample_data()
        _save_data(initial)
        return initial
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        initial = _create_initial_sample_data()
        _save_data(initial)
        return initial


def _save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _create_initial_sample_data():
    sample_trip_id = "tirupati-nov24"
    return {
        "trips": [
            {
                "id": sample_trip_id,
                "destination": "Tirupati",
                "origin": "Bengaluru",
                "start_date": "2026-11-24",
                "end_date": "2026-11-27",
                "travelers": 2,
                "notes": "Door-to-door Tirupati pilgrimage and Talakona waterfalls trip with family.",
                "created_at": "2026-11-22T10:00:00"
            }
        ],
        "expenses": [
            # ── Pre-Booked Commitments (Stays, Lounges, Trains) ──
            {
                "id": str(uuid.uuid4())[:8],
                "trip_id": sample_trip_id,
                "title": "IRCTC Express Train Tickets (KSR Bengaluru ➔ Tirupati)",
                "amount": 1240.0,
                "category": "transport",
                "is_prebooked": True,
                "payment_mode": "IRCTC Online",
                "date": "2026-11-20",
                "time": "14:30",
                "notes": "Confirmed AC Chair Car tickets for 2 travelers"
            },
            {
                "id": str(uuid.uuid4())[:8],
                "trip_id": sample_trip_id,
                "title": "Hotel Bhimas Deluxe (2 Nights Stay, Tirupati City)",
                "amount": 4200.0,
                "category": "stay_lounge",
                "is_prebooked": True,
                "payment_mode": "MakeMyTrip Pre-Paid",
                "date": "2026-11-20",
                "time": "16:00",
                "notes": "Deluxe AC Room pre-booked near Railway Station"
            },
            {
                "id": str(uuid.uuid4())[:8],
                "trip_id": sample_trip_id,
                "title": "IRCTC Executive Railway Lounge Access (Waiting Pass)",
                "amount": 350.0,
                "category": "stay_lounge",
                "is_prebooked": True,
                "payment_mode": "Online Banking",
                "date": "2026-11-21",
                "time": "11:15",
                "notes": "2 hours lounge access before boarding with buffet breakfast"
            },
            {
                "id": str(uuid.uuid4())[:8],
                "trip_id": sample_trip_id,
                "title": "TTD ₹300 Special Entry Darshan Passes",
                "amount": 600.0,
                "category": "activities_darshan",
                "is_prebooked": True,
                "payment_mode": "TTD Official Portal",
                "date": "2026-11-21",
                "time": "10:00",
                "notes": "Slot confirmed for 25th Nov 09:00 AM"
            },
            {
                "id": str(uuid.uuid4())[:8],
                "trip_id": sample_trip_id,
                "title": "KSRTC Airavat Multi-Axle Volvo Return Bus Tickets",
                "amount": 1600.0,
                "category": "transport",
                "is_prebooked": True,
                "payment_mode": "RedBus Online",
                "date": "2026-11-21",
                "time": "19:00",
                "notes": "Night sleeper return to Bengaluru"
            },

            # ── On-Trip Live Expenses (From Doorstep Onwards) ──
            {
                "id": str(uuid.uuid4())[:8],
                "trip_id": sample_trip_id,
                "title": "Doorstep Auto to Bengaluru Railway Station",
                "amount": 180.0,
                "category": "transport",
                "is_prebooked": False,
                "payment_mode": "PhonePe UPI",
                "date": "2026-11-24",
                "time": "05:45",
                "notes": "Doorstep morning pickup"
            },
            {
                "id": str(uuid.uuid4())[:8],
                "trip_id": sample_trip_id,
                "title": "Station Morning Hot Filter Coffee & Idli",
                "amount": 120.0,
                "category": "food",
                "is_prebooked": False,
                "payment_mode": "GPay UPI",
                "date": "2026-11-24",
                "time": "06:30",
                "notes": "Platform 1 refresh counter"
            },
            {
                "id": str(uuid.uuid4())[:8],
                "trip_id": sample_trip_id,
                "title": "Auto from Tirupati Station to Hotel Bhimas",
                "amount": 100.0,
                "category": "transport",
                "is_prebooked": False,
                "payment_mode": "Cash",
                "date": "2026-11-24",
                "time": "12:15",
                "notes": "Local auto drop"
            },
            {
                "id": str(uuid.uuid4())[:8],
                "trip_id": sample_trip_id,
                "title": "Authentic Rayalaseema Veg Thali Lunch",
                "amount": 380.0,
                "category": "food",
                "is_prebooked": False,
                "payment_mode": "PhonePe UPI",
                "date": "2026-11-24",
                "time": "13:30",
                "notes": "Banana leaf lunch with hot ghee & gongura"
            },
            {
                "id": str(uuid.uuid4())[:8],
                "trip_id": sample_trip_id,
                "title": "APSRTC Electric Ghat Bus to Tirumala Hilltop",
                "amount": 180.0,
                "category": "transport",
                "is_prebooked": False,
                "payment_mode": "UPI / PhonePe",
                "date": "2026-11-24",
                "time": "16:30",
                "notes": "Tickets for 2 travelers up the Seven Hills"
            },
            {
                "id": str(uuid.uuid4())[:8],
                "trip_id": sample_trip_id,
                "title": "Sacred Camphor, Garland & Puja Flowers",
                "amount": 150.0,
                "category": "activities_darshan",
                "is_prebooked": False,
                "payment_mode": "Cash",
                "date": "2026-11-24",
                "time": "18:00",
                "notes": "Tirumala Sanctum flower stall"
            },
            {
                "id": str(uuid.uuid4())[:8],
                "trip_id": sample_trip_id,
                "title": "Extra Tirupati Laddu Prasadam Tokens (5 Laddus)",
                "amount": 250.0,
                "category": "shopping",
                "is_prebooked": False,
                "payment_mode": "Debit Card",
                "date": "2026-11-25",
                "time": "11:30",
                "notes": "Official TTD laddu counters"
            },
            {
                "id": str(uuid.uuid4())[:8],
                "trip_id": sample_trip_id,
                "title": "Talakona Waterfalls Eco-Park Entry & Canopy Walk",
                "amount": 350.0,
                "category": "activities_darshan",
                "is_prebooked": False,
                "payment_mode": "PhonePe UPI",
                "date": "2026-11-26",
                "time": "10:30",
                "notes": "Waterfall nature trail & hanging ropewalk tickets"
            },
            {
                "id": str(uuid.uuid4())[:8],
                "trip_id": sample_trip_id,
                "title": "Tirupati Handicrafts & Red Sanders Wood Souvenirs",
                "amount": 650.0,
                "category": "shopping",
                "is_prebooked": False,
                "payment_mode": "GPay UPI",
                "date": "2026-11-26",
                "time": "17:00",
                "notes": "Lepakshi Emporium Gandhi Road"
            }
        ]
    }


def get_all_trips():
    """Returns list of trips with summary financials."""
    data = _load_data()
    trips = data.get("trips", [])
    expenses = data.get("expenses", [])

    results = []
    for t in trips:
        t_id = t["id"]
        trip_exps = [e for e in expenses if e.get("trip_id") == t_id]
        
        prebooked_total = sum(e["amount"] for e in trip_exps if e.get("is_prebooked", False))
        on_trip_total = sum(e["amount"] for e in trip_exps if not e.get("is_prebooked", False))
        grand_total = prebooked_total + on_trip_total

        # Status determination: check explicit status first, otherwise date-based
        status = t.get("status")
        if not status:
            today_str = date.today().isoformat()
            if t.get("start_date") and t.get("end_date"):
                if today_str < t["start_date"]:
                    status = "Upcoming"
                elif t["start_date"] <= today_str <= t["end_date"]:
                    status = "In-Transit (Live)"
                else:
                    status = "Completed"
            else:
                status = "Planned"

        results.append({
            **t,
            "prebooked_total": round(prebooked_total, 2),
            "on_trip_total": round(on_trip_total, 2),
            "grand_total": round(grand_total, 2),
            "expense_count": len(trip_exps),
            "status": status
        })

    return results


def get_trip_details(trip_id):
    """Returns trip info, list of expenses, category breakdown and group split."""
    data = _load_data()
    trip = next((t for t in data.get("trips", []) if t["id"] == trip_id), None)
    if not trip:
        # Fallback to first trip if any
        if data.get("trips"):
            trip = data["trips"][0]
            trip_id = trip["id"]
        else:
            return None

    trip_exps = [e for e in data.get("expenses", []) if e.get("trip_id") == trip_id]
    
    # Sort expenses: Pre-booked first (by date), then On-trip (by date & time)
    def sort_key(e):
        return (0 if e.get("is_prebooked") else 1, e.get("date", ""), e.get("time", ""))
    
    sorted_exps = sorted(trip_exps, key=sort_key)

    prebooked_list = [e for e in sorted_exps if e.get("is_prebooked", False)]
    on_trip_list = [e for e in sorted_exps if not e.get("is_prebooked", False)]

    prebooked_total = sum(e["amount"] for e in prebooked_list)
    on_trip_total = sum(e["amount"] for e in on_trip_list)
    grand_total = prebooked_total + on_trip_total

    # Category breakdown
    cat_totals = {}
    for cat_k in DEFAULT_CATEGORIES.keys():
        cat_totals[cat_k] = 0.0

    for e in sorted_exps:
        c = e.get("category", "misc")
        if c not in cat_totals:
            cat_totals[c] = 0.0
        cat_totals[c] += e.get("amount", 0.0)

    category_breakdown = []
    for cat_k, cat_amt in cat_totals.items():
        if cat_amt > 0:
            pct = (cat_amt / grand_total * 100) if grand_total > 0 else 0
            info = DEFAULT_CATEGORIES.get(cat_k, {'name': cat_k.title(), 'icon': '📌', 'badge': 'secondary'})
            category_breakdown.append({
                'key': cat_k,
                'name': info['name'],
                'icon': info['icon'],
                'badge': info['badge'],
                'amount': round(cat_amt, 2),
                'percent': round(pct, 1)
            })

    category_breakdown.sort(key=lambda x: x['amount'], reverse=True)

    travelers = max(1, int(trip.get("travelers", 1)))
    per_person_share = round(grand_total / travelers, 2)

    status = trip.get("status")
    if not status:
        today_str = date.today().isoformat()
        if trip.get("start_date") and trip.get("end_date"):
            if today_str < trip["start_date"]:
                status = "Upcoming"
            elif trip["start_date"] <= today_str <= trip["end_date"]:
                status = "In-Transit (Live)"
            else:
                status = "Completed"
        else:
            status = "Planned"

    return {
        "trip": {**trip, "status": status},
        "prebooked_expenses": prebooked_list,
        "on_trip_expenses": on_trip_list,
        "all_expenses": sorted_exps,
        "prebooked_total": round(prebooked_total, 2),
        "on_trip_total": round(on_trip_total, 2),
        "grand_total": round(grand_total, 2),
        "travelers": travelers,
        "per_person_share": per_person_share,
        "category_breakdown": category_breakdown,
        "categories_meta": DEFAULT_CATEGORIES
    }


def create_or_update_trip(destination, start_date, end_date, origin="", travelers=1, notes=""):
    """Creates a new trip and returns the new trip ID."""
    data = _load_data()
    trip_id = f"{destination.lower().replace(' ', '-')}-{start_date}"
    # Ensure unique trip ID
    if any(t["id"] == trip_id for t in data["trips"]):
        trip_id = f"{trip_id}-{str(uuid.uuid4())[:4]}"

    new_trip = {
        "id": trip_id,
        "destination": destination.strip().title(),
        "origin": (origin or "").strip().title(),
        "start_date": start_date,
        "end_date": end_date,
        "travelers": max(1, int(travelers)),
        "notes": notes.strip(),
        "created_at": datetime.now().isoformat()
    }

    data["trips"].append(new_trip)
    _save_data(data)
    return trip_id


def add_expense(trip_id, title, amount, category='misc', is_prebooked=False, payment_mode='UPI / PhonePe', notes='', date_val=None, time_val=None):
    """Adds a single expense entry to the trip diary."""
    data = _load_data()
    now = datetime.now()
    
    exp_date = date_val or now.strftime("%Y-%m-%d")
    exp_time = time_val or now.strftime("%H:%M")

    new_exp = {
        "id": str(uuid.uuid4())[:8],
        "trip_id": trip_id,
        "title": title.strip(),
        "amount": round(float(amount), 2),
        "category": category if category in DEFAULT_CATEGORIES else "misc",
        "is_prebooked": bool(is_prebooked),
        "payment_mode": (payment_mode or "UPI / PhonePe").strip(),
        "date": exp_date,
        "time": exp_time,
        "notes": notes.strip()
    }

    data["expenses"].append(new_exp)
    _save_data(data)
    return new_exp


def delete_expense(expense_id):
    """Deletes an expense item by ID."""
    data = _load_data()
    initial_len = len(data["expenses"])
    data["expenses"] = [e for e in data["expenses"] if e.get("id") != expense_id]
    if len(data["expenses"]) != initial_len:
        _save_data(data)
        return True
    return False


def delete_trip(trip_id):
    """Deletes a trip and all its associated expenses."""
    data = _load_data()
    data["trips"] = [t for t in data["trips"] if t.get("id") != trip_id]
    data["expenses"] = [e for e in data["expenses"] if e.get("trip_id") != trip_id]
    _save_data(data)
    return True


def update_trip_status(trip_id, new_status):
    """Updates the explicit trip status (Planned, In-Transit (Live), Completed)."""
    data = _load_data()
    now_str = datetime.now().strftime("%d-%b %I:%M %p")
    for t in data.get("trips", []):
        if t["id"] == trip_id:
            t["status"] = new_status
            if new_status == "In-Transit (Live)":
                t["started_at"] = now_str
            elif new_status == "Completed":
                t["ended_at"] = now_str
            _save_data(data)
            return True
    return False


# ==============================================================================
# SMART UPI / PHONEPE / GPAY / BANK SMS TEXT PARSER
# ==============================================================================
def parse_upi_sms_or_text(raw_text):
    """
    Parses bank transaction SMS / PhonePe / GPay confirmation text.
    Extracts Amount, Vendor/Title, Category, Payment Mode, and Date.
    """
    text = (raw_text or "").strip()
    if not text:
        return None

    # 1. Amount Extraction
    # Matches Rs. 240, Rs 240, INR 350.50, ₹1,200, 240.00 debited
    amt_match = re.search(r'(?:Rs\.?|INR|₹)\s*([\d,]+(?:\.\d{1,2})?)', text, re.IGNORECASE)
    if not amt_match:
        amt_match = re.search(r'([\d,]+(?:\.\d{1,2})?)\s*(?:debited|paid|sent)', text, re.IGNORECASE)

    amount = 0.0
    if amt_match:
        try:
            amount = float(amt_match.group(1).replace(',', ''))
        except Exception:
            amount = 0.0

    # 2. Payee / Vendor Extraction
    # Looks for 'to <vendor>', 'at <vendor>', 'VPA <vendor>'
    title = ""
    vendor_match = re.search(r'(?:to|at|VPA|paid to|sent to)\s+([A-Za-z0-9\s&.\'\-]{2,40}?)(?:\s+(?:on|via|ref|UPI|using|dated|through|from|\.|\n|$))', text, re.IGNORECASE)
    if vendor_match:
        candidate = vendor_match.group(1).strip()
        # Clean up any trailing bank noise
        candidate = re.sub(r'\b(VPA|UPI|Ref|A/c|Acct|INR|Rs)\b.*', '', candidate, flags=re.IGNORECASE).strip()
        if candidate and len(candidate) >= 3:
            title = candidate

    if not title:
        # Fallback: first 5-6 words
        words = text.split()[:5]
        title = " ".join(words) if words else "Travel Expense"

    title = title.title()

    # 3. Category Detection
    lower_text = text.lower()
    cat = 'misc'

    if any(k in lower_text for k in ['restaurant', 'cafe', 'tiffin', 'meals', 'food', 'lunch', 'dinner', 'breakfast', 'snack', 'swiggy', 'zomato', 'bakery', 'juice', 'bhavan', 'mess', 'biryani', 'idli', 'dosa', 'chai', 'tea', 'coffee']):
        cat = 'food'
    elif any(k in lower_text for k in ['hotel', 'lodge', 'resort', 'lounge', 'dharamshala', 'inn', 'residency', 'stay', 'oyo', 'room']):
        cat = 'stay_lounge'
    elif any(k in lower_text for k in ['auto', 'cab', 'taxi', 'ola', 'uber', 'rapido', 'bus', 'train', 'irctc', 'flight', 'indigo', 'rtc', 'apsrtc', 'ksrtc', 'toll', 'metro', 'petrol', 'diesel', 'fuel', 'fastag']):
        cat = 'transport'
    elif any(k in lower_text for k in ['temple', 'devasthanam', 'darshan', 'ttd', 'entry', 'ticket', 'pass', 'museum', 'safari', 'zoo', 'waterfall', 'ropewalk', 'puja', 'pooja', 'archana', 'abhishekam', 'boating']):
        cat = 'activities_darshan'
    elif any(k in lower_text for k in ['shopping', 'bazaar', 'mall', 'market', 'mart', 'store', 'silks', 'saree', 'handicraft', 'prasadam', 'sweet', 'laddu', 'gift', 'souvenir']):
        cat = 'shopping'

    # 4. Payment Mode Detection
    mode = 'UPI / Online'
    if 'phonepe' in lower_text:
        mode = 'PhonePe UPI'
    elif 'gpay' in lower_text or 'google pay' in lower_text:
        mode = 'Google Pay (GPay)'
    elif 'paytm' in lower_text:
        mode = 'Paytm UPI'
    elif 'card' in lower_text or 'debit' in lower_text:
        mode = 'Debit Card'
    elif 'credit' in lower_text:
        mode = 'Credit Card'
    elif 'net banking' in lower_text or 'imps' in lower_text or 'neft' in lower_text:
        mode = 'Net Banking'
    elif 'cash' in lower_text:
        mode = 'Cash'

    return {
        'amount': amount,
        'title': title,
        'category': cat,
        'category_name': DEFAULT_CATEGORIES[cat]['name'],
        'category_icon': DEFAULT_CATEGORIES[cat]['icon'],
        'payment_mode': mode,
        'date': date.today().isoformat(),
        'time': datetime.now().strftime("%H:%M")
    }

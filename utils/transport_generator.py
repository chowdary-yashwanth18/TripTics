import random
import hashlib
from datetime import datetime, timedelta

def get_train_names():
    return ["Vande Bharat Express", "Rajdhani Express", "Shatabdi Express", "Duronto Express", "Garib Rath Express", "Sampark Kranti Express", "Intercity Express", "Superfast Express"]

def get_airlines():
    return ["IndiGo", "Air India", "SpiceJet", "Vistara", "Akasa Air"]

def get_bus_operators():
    return ["Orange Travels", "Kaveri Travels", "SRS Travels", "VRL Travels", "IntrCity SmartBus", "APSRTC Garuda", "TSRTC Rajadhani"]

def generate_time(seed_val, is_return=False):
    random.seed(seed_val)
    # Outbound usually leaves morning/afternoon, return usually leaves afternoon/evening
    start_hour = random.randint(5, 14) if not is_return else random.randint(14, 22)
    start_minute = random.choice([0, 15, 30, 45])
    duration_hours = random.randint(1, 14) # Depends on mode, but we keep it simple here. Later adjusted.
    duration_minutes = random.choice([0, 10, 20, 30, 40, 50])
    
    start_time = f"{start_hour:02d}:{start_minute:02d}"
    
    end_hour = (start_hour + duration_hours) % 24
    end_minute = (start_minute + duration_minutes) % 60
    end_time = f"{end_hour:02d}:{end_minute:02d}"
    
    duration = f"{duration_hours}h {duration_minutes}m"
    return start_time, end_time, duration

def generate_vacancy(mode):
    if mode == 'train':
        statuses = [
            ("AVAILABLE", lambda: f"AVL-{random.randint(10, 150)}"),
            ("WAITLIST", lambda: f"WL-{random.randint(1, 100)}"),
            ("RAC", lambda: f"RAC-{random.randint(1, 40)}")
        ]
    elif mode == 'flight':
        statuses = [
            ("AVAILABLE", lambda: f"{random.randint(2, 20)} Seats Left"),
            ("SOLD OUT", lambda: "Sold Out")
        ]
    else: # bus
        statuses = [
            ("AVAILABLE", lambda: f"{random.randint(5, 35)} Seats"),
            ("FILLING FAST", lambda: f"Only {random.randint(1, 4)} Seats Left")
        ]
    
    status, text_gen = random.choices(statuses, weights=[0.7, 0.2, 0.1] if mode == 'train' else [0.9, 0.1])[0]
    
    # Assign color class based on status
    if status == "AVAILABLE":
        color = "success"
    elif status in ["WAITLIST", "SOLD OUT"]:
        color = "danger"
    else:
        color = "warning"
        
    return {"status": status, "text": text_gen(), "color": color}

def generate_complex_route(origin, destination, is_return, hash_val, nearest_airport_info=None):
    random.seed(hash_val)
    
    origin_lower = origin.lower().strip()
    dest_lower = destination.lower().strip()
    
    # Specific mock for Kakinada -> London
    if (origin_lower == 'kakinada' and dest_lower == 'london') or (origin_lower == 'london' and dest_lower == 'kakinada'):
        legs = []
        if origin_lower == 'kakinada':
            legs_data = [
                {'orig': 'Kakinada', 'dest': 'Rajahmundry', 'mode': 'bus', 'icon': '🚌', 'price': 150, 'dur': '1h 30m', 'name': 'APSRTC Garuda'},
                {'orig': 'Rajahmundry', 'dest': 'Hyderabad', 'mode': 'flight', 'icon': '✈️', 'price': 3500, 'dur': '1h 10m', 'name': 'IndiGo 6E-241'},
                {'orig': 'Hyderabad', 'dest': 'Delhi', 'mode': 'flight', 'icon': '✈️', 'price': 5200, 'dur': '2h 15m', 'name': 'Vistara UK-832'},
                {'orig': 'Delhi', 'dest': 'Abu Dhabi', 'mode': 'flight', 'icon': '✈️', 'price': 15000, 'dur': '4h 00m', 'name': 'Etihad EY-211'},
                {'orig': 'Abu Dhabi', 'dest': 'London', 'mode': 'flight', 'icon': '✈️', 'price': 32000, 'dur': '7h 30m', 'name': 'British Airways BA-104'}
            ]
        else:
            legs_data = [
                {'orig': 'London', 'dest': 'Abu Dhabi', 'mode': 'flight', 'icon': '✈️', 'price': 31000, 'dur': '7h 15m', 'name': 'British Airways BA-105'},
                {'orig': 'Abu Dhabi', 'dest': 'Delhi', 'mode': 'flight', 'icon': '✈️', 'price': 14500, 'dur': '3h 45m', 'name': 'Etihad EY-212'},
                {'orig': 'Delhi', 'dest': 'Hyderabad', 'mode': 'flight', 'icon': '✈️', 'price': 5100, 'dur': '2h 10m', 'name': 'Vistara UK-833'},
                {'orig': 'Hyderabad', 'dest': 'Rajahmundry', 'mode': 'flight', 'icon': '✈️', 'price': 3400, 'dur': '1h 05m', 'name': 'IndiGo 6E-242'},
                {'orig': 'Rajahmundry', 'dest': 'Kakinada', 'mode': 'bus', 'icon': '🚌', 'price': 150, 'dur': '1h 30m', 'name': 'APSRTC Garuda'}
            ]
            
        current_hour = random.randint(5, 10) if not is_return else random.randint(12, 18)
        current_minute = random.choice([0, 15, 30, 45])
        
        total_price = 0
        built_legs = []
        for l in legs_data:
            start_time_str = f"{current_hour:02d}:{current_minute:02d}"
            dur_h, dur_m = int(l['dur'].split('h')[0]), int(l['dur'].split('h')[1].strip('m '))
            
            end_hour = (current_hour + dur_h) % 24
            end_minute = (current_minute + dur_m) % 60
            if end_minute >= 60:
                end_hour = (end_hour + 1) % 24
                end_minute %= 60
                
            end_time_str = f"{end_hour:02d}:{end_minute:02d}"
            
            built_legs.append({
                "origin": l['orig'],
                "destination": l['dest'],
                "mode": l['mode'],
                "icon": l['icon'],
                "name": l['name'],
                "class_type": "Economy" if l['mode'] == 'flight' else "A/C Seater",
                "start_time": start_time_str,
                "end_time": end_time_str,
                "duration": l['dur'],
                "price": l['price']
            })
            total_price += l['price']
            
            layover_h = random.randint(2, 4)
            current_hour = (end_hour + layover_h) % 24
            current_minute = end_minute
            
        return [{
            "mode": "multi",
            "icon": "🗺️",
            "name": f"Multi-Leg via {built_legs[1]['origin'] if origin_lower == 'kakinada' else built_legs[-2]['destination']}",
            "class_type": "Mixed",
            "start_time": built_legs[0]['start_time'],
            "end_time": built_legs[-1]['end_time'],
            "duration": "24h+",
            "price": total_price,
            "rating": 4.5,
            "vacancy": {"status": "AVAILABLE", "text": "Available", "color": "success"},
            "legs": built_legs
        }]
    return []

def generate_transport(origin, destination, mode, is_return=False, is_international=False):
    """
    Generates mock realistic travel options for a given route and mode.
    Mode can be 'flight', 'train', 'bus', 'multi', or 'any'.
    """
    if not origin:
        origin = "Current Location"
        
    loc_str = f"{origin}-{destination}-{is_return}"
    hash_val = int(hashlib.md5(loc_str.encode('utf-8')).hexdigest(), 16)
    random.seed(hash_val)
    
    # ── Multi-leg Intercept ──
    from utils.geography import get_nearest_airport
    origin_lower = origin.lower().strip()
    dest_lower = destination.lower().strip()
    
    if (origin_lower == 'kakinada' and dest_lower == 'london') or (origin_lower == 'london' and dest_lower == 'kakinada'):
        return generate_complex_route(origin, destination, is_return, hash_val)
        
    # Check if origin has no airport, but we need a flight
    nearest_airport_info = get_nearest_airport(origin)
    if nearest_airport_info and (is_international or mode in ['flight', 'any']):
        # If destination is london, generate a complex route
        if dest_lower == 'london':
             return generate_complex_route(origin, destination, is_return, hash_val)
    
    if is_international:
        mode = 'flight'
    elif mode == 'any':
        route_places = origin.lower() + " " + destination.lower()
        available_modes = ['flight', 'train', 'bus']
        if any(place in route_places for place in ['araku', 'aruku', 'srikakulam', 'munnar', 'coorg', 'wayanad']):
            if 'flight' in available_modes: available_modes.remove('flight')
        if any(place in route_places for place in ['munnar', 'wayanad', 'coorg', 'andaman']):
            if 'train' in available_modes: available_modes.remove('train')
        mode = random.choice(available_modes) if available_modes else 'bus'
        
    # Simulate lack of transport to certain places
    route_places = origin.lower() + " " + destination.lower()
    if mode == 'flight' and any(place in route_places for place in ['araku', 'aruku', 'srikakulam', 'munnar', 'coorg', 'wayanad']):
        return []
    
    if mode == 'train' and any(place in route_places for place in ['munnar', 'wayanad', 'coorg', 'andaman']):
        return []
        
    options = []
    num_options = random.randint(2, 4)
    
    for i in range(num_options):
        opt_seed = hash_val + i
        random.seed(opt_seed)
        
        start_time, end_time, base_duration = generate_time(opt_seed, is_return)
        
        if mode == 'flight':
            if is_international:
                airlines = ["Emirates", "Lufthansa", "Qatar Airways", "British Airways", "Air France", "Singapore Airlines", "Etihad"]
                operator = random.choice(airlines)
                name = f"{operator} {random.choice(['EK', 'LH', 'QR', 'BA', 'AF', 'SQ'])}-{random.randint(100, 999)}"
                price = random.randint(350, 1500) * 100 + random.choice([0, 50, 99])
                duration_hours = random.randint(6, 24)
            else:
                operator = random.choice(get_airlines())
                name = f"{operator} {random.choice(['6E', 'AI', 'SG', 'UK'])}-{random.randint(100, 999)}"
                price = random.randint(35, 120) * 100 + random.choice([15, 25, 50, 75, 99])
                duration_hours = random.randint(1, 3)
                
            icon = "✈️"
            duration_minutes = random.choice([15, 30, 45, 0])
            start_hour = int(start_time.split(':')[0])
            end_hour = (start_hour + duration_hours) % 24
            end_time = f"{end_hour:02d}:{duration_minutes:02d}"
            duration = f"{duration_hours}h {duration_minutes}m"
            class_type = random.choice(["Economy", "Premium Economy"])
        elif mode == 'train':
            name = random.choice(get_train_names())
            train_no = random.randint(11000, 22999)
            name = f"{train_no} {name}"
            price = random.randint(8, 35) * 100 + random.choice([5, 25, 45, 65, 85])
            icon = "🚆"
            duration = base_duration
            class_type = random.choice(["3A", "2A", "1A", "CC", "EC", "SL"])
        else: # bus
            operator = random.choice(get_bus_operators())
            name = f"{operator} {random.choice(['Volvo A/C Sleeper', 'Scania Multi-Axle', 'Non A/C Seater'])}"
            price = random.randint(5, 25) * 100 + random.choice([0, 49, 99])
            icon = "🚌"
            duration = base_duration
            class_type = "Sleeper/Seater"
            
        rating = round(random.uniform(3.5, 4.9), 1)
        vacancy = generate_vacancy(mode)
        
        # Convert standard single-leg option into the new structure
        options.append({
            "mode": mode,
            "icon": icon,
            "name": name,
            "class_type": class_type,
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
            "price": price,
            "rating": rating,
            "vacancy": vacancy,
            "legs": [{
                "origin": origin,
                "destination": destination,
                "mode": mode,
                "icon": icon,
                "name": name,
                "class_type": class_type,
                "start_time": start_time,
                "end_time": end_time,
                "duration": duration,
                "price": price
            }]
        })
        
    options.sort(key=lambda x: x['price'])
    return options

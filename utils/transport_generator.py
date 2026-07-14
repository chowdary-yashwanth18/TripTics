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

def generate_transport(origin, destination, mode, is_return=False):
    """
    Generates mock realistic travel options for a given route and mode.
    Mode can be 'flight', 'train', 'bus', or 'any'.
    """
    if not origin:
        origin = "Current Location"
        
    loc_str = f"{origin}-{destination}-{is_return}"
    hash_val = int(hashlib.md5(loc_str.encode('utf-8')).hexdigest(), 16)
    random.seed(hash_val)
    
    if mode == 'any':
        mode = random.choice(['flight', 'train', 'bus'])
        
    options = []
    num_options = random.randint(2, 4)
    
    for i in range(num_options):
        # Unique seed for each option
        opt_seed = hash_val + i
        random.seed(opt_seed)
        
        start_time, end_time, base_duration = generate_time(opt_seed, is_return)
        
        if mode == 'flight':
            operator = random.choice(get_airlines())
            name = f"{operator} {random.choice(['6E', 'AI', 'SG', 'UK'])}-{random.randint(100, 999)}"
            price = random.randint(3500, 12000)
            icon = "✈️"
            # Flights are faster
            duration_hours = random.randint(1, 3)
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
            price = random.randint(800, 3500)
            icon = "🚆"
            duration = base_duration
            class_type = random.choice(["3A", "2A", "1A", "CC", "EC", "SL"])
        else: # bus
            operator = random.choice(get_bus_operators())
            name = f"{operator} {random.choice(['Volvo A/C Sleeper', 'Scania Multi-Axle', 'Non A/C Seater'])}"
            price = random.randint(500, 2500)
            icon = "🚌"
            duration = base_duration
            class_type = "Sleeper/Seater"
            
        rating = round(random.uniform(3.5, 4.9), 1)
        vacancy = generate_vacancy(mode)
        
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
            "vacancy": vacancy
        })
        
    # Sort by price
    options.sort(key=lambda x: x['price'])
    return options

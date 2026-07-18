import hashlib
import random

def get_distance(origin, destination):
    """
    Returns the distance between two cities in kilometers.
    Uses mocked deterministic distances, with a hardcoded override for Bengaluru-London.
    """
    if not origin or not destination:
        return 0
        
    origin_lower = origin.lower().strip()
    dest_lower = destination.lower().strip()
    
    if (origin_lower == 'bengaluru' and dest_lower == 'london') or (origin_lower == 'london' and dest_lower == 'bengaluru'):
        return 8030
        
    # Generate a deterministic distance based on the strings
    hash_str = f"{origin_lower}-{dest_lower}"
    hash_val = int(hashlib.md5(hash_str.encode('utf-8')).hexdigest(), 16)
    random.seed(hash_val)
    
    return random.randint(200, 5000)

def get_nearest_airport(city):
    """
    Returns the nearest airport for a city that doesn't have one.
    Returns None if the city is assumed to have an airport.
    """
    if not city:
        return None
        
    city_lower = city.lower().strip()
    
    NO_AIRPORT_MAPPING = {
        'kakinada': {'airport': 'Rajahmundry', 'distance': 65, 'mode': 'bus', 'price': 150},
        'araku': {'airport': 'Visakhapatnam', 'distance': 114, 'mode': 'train', 'price': 120},
        'araku valley': {'airport': 'Visakhapatnam', 'distance': 114, 'mode': 'train', 'price': 120},
        'munnar': {'airport': 'Cochin', 'distance': 110, 'mode': 'bus', 'price': 300},
        'coorg': {'airport': 'Mangalore', 'distance': 135, 'mode': 'bus', 'price': 350},
        'wayanad': {'airport': 'Calicut', 'distance': 85, 'mode': 'bus', 'price': 250},
        'srikakulam': {'airport': 'Visakhapatnam', 'distance': 116, 'mode': 'train', 'price': 100}
    }
    
    return NO_AIRPORT_MAPPING.get(city_lower)

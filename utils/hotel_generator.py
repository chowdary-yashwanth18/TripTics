import hashlib
import random

def generate_hotels(location):
    """
    Generates a mock list of hotels for a given location, sorted from low to high price.
    Ensures that if location is Arasavilli or Srikakulam, "Hotel Nagavali" is included.
    """
    loc_clean = location.strip().lower()
    loc_title = location.strip().title()
    
    # Deterministic generation so same location gives same hotels
    hash_val = int(hashlib.md5(loc_clean.encode('utf-8')).hexdigest(), 16)
    random.seed(hash_val)
    
    base_names = [
        f"{loc_title} Grand",
        f"The {loc_title} Resort",
        f"{loc_title} Inn",
        "Royal Palace Lodge",
        "Comfort Stay",
        "Budget Inn",
        "Luxury Suites",
        "Sunrise Guest House",
        "Moonlight Hotel",
        "Oasis Lodge"
    ]
    
    selected_names = random.sample(base_names, k=random.randint(5, 8))
    
    # Force add Hotel Nagavali if specific location is searched
    if 'srikakulam' in loc_clean or 'arasavilli' in loc_clean or 'arasavalli' in loc_clean:
        if "Hotel Nagavali" not in selected_names:
            selected_names.append("Hotel Nagavali (Famous Lodge & Restaurant)")
            
    hotels = []
    for name in selected_names:
        price = random.randint(500, 8000)
        rating = round(random.uniform(3.0, 5.0), 1)
        amenities = random.sample(['Free WiFi', 'Breakfast Included', 'AC', 'Pool', 'Gym', 'Restaurant', 'Parking', 'Room Service'], k=random.randint(3, 6))
        
        # Give Nagavali a specific realistic price and rating if we want
        if "Nagavali" in name:
            price = random.randint(800, 2500)
            rating = round(random.uniform(4.2, 4.8), 1)
            amenities = ['Restaurant', 'AC', 'Free WiFi', 'Parking', 'Room Service']
            
        hotels.append({
            'name': name,
            'price': price,
            'rating': rating,
            'amenities': amenities,
            'image_url': f"https://picsum.photos/400/300?random={random.randint(1, 1000)}"
        })
        
    # Sort hotels from low to high price
    hotels.sort(key=lambda x: x['price'])
    
    return hotels

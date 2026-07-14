import hashlib
import random
import urllib.request
import urllib.parse
import re
import json

def fetch_exact_image(query):
    """Fetches an exact image URL from the web based on the query."""
    try:
        req = urllib.request.Request(f"https://duckduckgo.com/?q={urllib.parse.quote(query)}&ia=images", headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=3).read().decode('utf-8')
        vqd_match = re.search(r'vqd=([\d-]+)', html)
        if vqd_match:
            req2 = urllib.request.Request(f"https://duckduckgo.com/i.js?q={urllib.parse.quote(query)}&o=json&vqd={vqd_match.group(1)}", headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req2, timeout=3).read().decode('utf-8')
            data = json.loads(res)
            if data.get('results'):
                return data['results'][0]['image']
    except Exception:
        pass
    return None

REAL_HOTELS = {
    'araku': [
        {"name": "Araku Haritha Hill Resort", "address": "Araku Valley, Andhra Pradesh"},
        {"name": "Tyda Jungle Bells Nature Camp", "address": "Tyda, Araku Valley, Andhra Pradesh"},
        {"name": "Ushasree Residency", "address": "Araku Main Road, Andhra Pradesh"},
        {"name": "Natures Nest Araku", "address": "Near Tribal Museum, Araku, Andhra Pradesh"},
        {"name": "SRK Resort", "address": "Padmapuram Junction, Araku, Andhra Pradesh"},
        {"name": "Bamboo Chicken Point (Restaurant)", "address": "Chaparai Waterfalls Road, Araku"},
        {"name": "Star Annapurna Restaurant", "address": "Araku Main Bazaar, Andhra Pradesh"},
        {"name": "Araku Tribal Food Court", "address": "Near Coffee Museum, Araku Valley"}
    ],
    'araku valley': [
        {"name": "Araku Haritha Hill Resort", "address": "Araku Valley, Andhra Pradesh"},
        {"name": "Tyda Jungle Bells Nature Camp", "address": "Tyda, Araku Valley, Andhra Pradesh"},
        {"name": "Ushasree Residency", "address": "Araku Main Road, Andhra Pradesh"},
        {"name": "Natures Nest Araku", "address": "Near Tribal Museum, Araku, Andhra Pradesh"},
        {"name": "SRK Resort", "address": "Padmapuram Junction, Araku, Andhra Pradesh"},
        {"name": "Bamboo Chicken Point (Restaurant)", "address": "Chaparai Waterfalls Road, Araku"},
        {"name": "Star Annapurna Restaurant", "address": "Araku Main Bazaar, Andhra Pradesh"},
        {"name": "Araku Tribal Food Court", "address": "Near Coffee Museum, Araku Valley"}
    ],
    'aruku': [
        {"name": "Araku Haritha Hill Resort", "address": "Araku Valley, Andhra Pradesh"},
        {"name": "Tyda Jungle Bells Nature Camp", "address": "Tyda, Araku Valley, Andhra Pradesh"},
        {"name": "Ushasree Residency", "address": "Araku Main Road, Andhra Pradesh"},
        {"name": "Natures Nest Araku", "address": "Near Tribal Museum, Araku, Andhra Pradesh"},
        {"name": "SRK Resort", "address": "Padmapuram Junction, Araku, Andhra Pradesh"},
        {"name": "Bamboo Chicken Point (Restaurant)", "address": "Chaparai Waterfalls Road, Araku"},
        {"name": "Star Annapurna Restaurant", "address": "Araku Main Bazaar, Andhra Pradesh"},
        {"name": "Araku Tribal Food Court", "address": "Near Coffee Museum, Araku Valley"}
    ],
    'rajahmundry': [
        {"name": "Shelton Rajahmundry", "address": "Ayyappa Nagar, Rajahmundry, Andhra Pradesh"},
        {"name": "Manjeera Sarovar Premiere", "address": "NH16, Rajahmundry, Andhra Pradesh"},
        {"name": "Anand Regency", "address": "Jampeta, Rajahmundry, Andhra Pradesh"},
        {"name": "Leela Pavilion", "address": "Danavaipeta, Rajahmundry, Andhra Pradesh"}
    ],
    'visakhapatnam': [
        {"name": "Novotel Visakhapatnam Varun Beach", "address": "Beach Road, Visakhapatnam, Andhra Pradesh"},
        {"name": "The Park Visakhapatnam", "address": "Beach Road, Visakhapatnam, Andhra Pradesh"},
        {"name": "Dolphin Hotel", "address": "Daba Gardens, Visakhapatnam, Andhra Pradesh"},
        {"name": "Gateway Hotel", "address": "Beach Road, Visakhapatnam, Andhra Pradesh"},
        {"name": "Bheemili Resort", "address": "Bheemili Beach, Visakhapatnam, Andhra Pradesh"}
    ],
    'srikakulam': [
        {"name": "Hotel Nagavali (Famous Lodge & Restaurant)", "address": "Seven Roads Junction, Srikakulam, Andhra Pradesh"},
        {"name": "Varam Residency", "address": "Day and Night Junction, Srikakulam, Andhra Pradesh"},
        {"name": "Hotel Blue Earth", "address": "GT Road, Srikakulam, Andhra Pradesh"}
    ]
}

def generate_hotels(location):
    """
    Generates a list of hotels for a given location, using real ones if available,
    and dynamically fetching exact images from the web.
    """
    loc_clean = location.strip().lower()
    loc_title = location.strip().title()
    
    hash_val = int(hashlib.md5(loc_clean.encode('utf-8')).hexdigest(), 16)
    random.seed(hash_val)
    
    # Use real hotels if we have them, else generate mock ones
    if loc_clean in REAL_HOTELS:
        selected_hotels = REAL_HOTELS[loc_clean]
    else:
        base_names = [
            f"{loc_title} Grand", f"The {loc_title} Resort", f"{loc_title} Inn",
            "Royal Palace Lodge", "Comfort Stay", "Budget Inn", "Luxury Suites"
        ]
        # Max 4 to keep image fetching fast
        selected_names = random.sample(base_names, k=random.randint(3, 4))
        selected_hotels = [{"name": name, "address": f"Central Area, {loc_title}"} for name in selected_names]
            
    hotels = []
    for h in selected_hotels:
        name = h['name']
        address = h['address']
        price = random.randint(1500, 8000)
        rating = round(random.uniform(3.8, 4.9), 1)
        amenities = random.sample(['Free WiFi', 'Breakfast Included', 'AC', 'Pool', 'Gym', 'Restaurant', 'Parking', 'Room Service'], k=random.randint(4, 6))
        
        # Try to fetch the EXACT image for this hotel, fallback to loremflickr
        exact_img = fetch_exact_image(f"{name} {loc_title} hotel exterior")
        outer_img = exact_img if exact_img else f"https://loremflickr.com/400/300/hotel,exterior/all?lock={random.randint(1, 1000)}"
        
        # Room image can be generic or exact if we want to risk it, generic is usually fine for interiors
        # but let's try exact for room too
        exact_room = fetch_exact_image(f"{name} {loc_title} hotel room interior")
        inner_img = exact_room if exact_room else f"https://loremflickr.com/400/300/hotel,room/all?lock={random.randint(1001, 2000)}"
        
        if "Nagavali" in name:
            price = random.randint(800, 2500)
            rating = round(random.uniform(4.2, 4.8), 1)
            
        hotels.append({
            'name': name,
            'address': address,
            'price': price,
            'rating': rating,
            'amenities': amenities,
            'outer_image_url': outer_img,
            'inner_image_url': inner_img
        })
        
    hotels.sort(key=lambda x: x['price'])
    return hotels

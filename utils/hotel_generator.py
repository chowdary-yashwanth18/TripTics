import hashlib
import random
import urllib.request
import urllib.parse
import re
import json
from utils.currency import get_currency_info

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
            "Royal Palace Lodge", "Comfort Stay", "Budget Inn", "Luxury Suites",
            f"{loc_title} Heritage Palace", f"{loc_title} Sunrise Retreat", f"{loc_title} Premium Stay",
            f"{loc_title} Eco-Camp", "Backpackers Hostel", f"{loc_title} Boutique Hotel"
        ]
        # Provide an exhaustive list of generated hotels
        selected_names = random.sample(base_names, k=random.randint(7, 10))
        selected_hotels = [{"name": name, "address": f"Central Area, {loc_title}"} for name in selected_names]
            
    hotels = []
    
    currency = get_currency_info(loc_clean)
    
    for h in selected_hotels:
        name = h['name']
        address = h['address']
        
        if currency['code'] in ['USD', 'EUR', 'GBP', 'CHF']:
            price = random.randint(8000, 35000)
        elif currency['code'] in ['AED', 'SGD', 'AUD', 'CAD', 'JPY']:
            price = random.randint(6000, 25000)
        elif currency['code'] != 'INR':
            price = random.randint(4000, 15000)
        else:
            price = random.randint(1500, 8000)
            
        rating = round(random.uniform(3.8, 4.9), 1)
        amenities = random.sample(['Free WiFi', 'Breakfast Included', 'AC', 'Pool', 'Gym', 'Restaurant', 'Parking', 'Room Service'], k=random.randint(4, 6))
        
        # Curated high-quality fallbacks to ensure relevance
        fallback_exteriors = [
            "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1551882547-ff40c0d129df?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1542314831-c6a4d27ece50?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=600&q=80"
        ]
        fallback_interiors = [
            "https://images.unsplash.com/photo-1611892440504-42a792e24d32?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?auto=format&fit=crop&w=600&q=80"
        ]
        
        # Use curated images exclusively to prevent broken hotlinked images
        outer_img = random.choice(fallback_exteriors)
        inner_img = random.choice(fallback_interiors)
        
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

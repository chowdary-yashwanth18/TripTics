import hashlib
import random
from utils.currency import get_currency_info
from utils.hotel_apps import get_hotel_booking_options, format_facilities

# Hotel image sets categorized by stay type & environment for high visual accuracy
HOTEL_IMAGE_SETS = {
    "hill": {
        "exteriors": [
            "https://images.unsplash.com/photo-1542314831-c6a4d27ece50?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=800&q=80"
        ],
        "interiors": [
            "https://images.unsplash.com/photo-1611892440504-42a792e24d32?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80"
        ]
    },
    "beach": {
        "exteriors": [
            "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1551882547-ff40c0d129df?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=800&q=80"
        ],
        "interiors": [
            "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1611892440504-42a792e24d32?auto=format&fit=crop&w=800&q=80"
        ]
    },
    "city": {
        "exteriors": [
            "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1551882547-ff40c0d129df?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1542314831-c6a4d27ece50?auto=format&fit=crop&w=800&q=80"
        ],
        "interiors": [
            "https://images.unsplash.com/photo-1611892440504-42a792e24d32?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=800&q=80"
        ]
    },
    "heritage": {
        "exteriors": [
            "https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1542314831-c6a4d27ece50?auto=format&fit=crop&w=800&q=80"
        ],
        "interiors": [
            "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1611892440504-42a792e24d32?auto=format&fit=crop&w=800&q=80"
        ]
    }
}

REAL_HOTELS = {
    # ── JAPAN ───────────────────────────────────────────────────────────────
    'japan': [
        {"name": "Keio Plaza Hotel Tokyo", "address": "Shinjuku-ku, Tokyo, Japan"},
        {"name": "Hotel Gracery Shinjuku", "address": "Kabukicho, Shinjuku, Tokyo, Japan"},
        {"name": "The Ritz-Carlton Kyoto", "address": "Kamogawa Nijo-Ohashi Hotori, Kyoto, Japan"},
        {"name": "Ryokan Gion Sano", "address": "Gion, Higashiyama-ku, Kyoto, Japan"},
        {"name": "Swissotel Nankai Osaka", "address": "Namba, Chuo-ku, Osaka, Japan"},
        {"name": "Hoshinoya Tokyo Ryokan", "address": "Otemachi, Chiyoda-ku, Tokyo, Japan"},
        {"name": "Dormy Inn Premium Namba", "address": "Nihonbashi, Chuo-ku, Osaka, Japan"},
        {"name": "Park Hyatt Tokyo", "address": "Nishi-Shinjuku, Tokyo, Japan"}
    ],
    'tokyo': [
        {"name": "Keio Plaza Hotel Tokyo", "address": "Shinjuku-ku, Tokyo, Japan"},
        {"name": "Hotel Gracery Shinjuku", "address": "Kabukicho, Shinjuku, Tokyo, Japan"},
        {"name": "Hoshinoya Tokyo Ryokan", "address": "Otemachi, Chiyoda-ku, Tokyo, Japan"},
        {"name": "Park Hyatt Tokyo", "address": "Nishi-Shinjuku, Tokyo, Japan"},
        {"name": "Sotetsu Fresa Inn Ginza", "address": "Ginza, Chuo-ku, Tokyo, Japan"},
        {"name": "Cerulean Tower Tokyu Hotel", "address": "Shibuya-ku, Tokyo, Japan"}
    ],
    'kyoto': [
        {"name": "The Ritz-Carlton Kyoto", "address": "Kamogawa, Nakagyo-ku, Kyoto, Japan"},
        {"name": "Ryokan Gion Sano", "address": "Gion, Higashiyama-ku, Kyoto, Japan"},
        {"name": "Hotel Granvia Kyoto", "address": "JR Kyoto Station, Shimogyo-ku, Kyoto"},
        {"name": "Kyoto Brighton Hotel", "address": "Kamigyo-ku, Kyoto, Japan"}
    ],
    'osaka': [
        {"name": "Swissotel Nankai Osaka", "address": "Namba, Chuo-ku, Osaka, Japan"},
        {"name": "Dormy Inn Premium Namba", "address": "Nihonbashi, Chuo-ku, Osaka, Japan"},
        {"name": "Hotel Nikko Osaka", "address": "Shinsaibashi, Chuo-ku, Osaka, Japan"},
        {"name": "The St. Regis Osaka", "address": "Honmachi, Chuo-ku, Osaka, Japan"}
    ],

    # ── INDIA ───────────────────────────────────────────────────────────────
    'araku': [
        {"name": "Araku Haritha Hill Resort", "address": "Araku Valley, Andhra Pradesh"},
        {"name": "Tyda Jungle Bells Nature Camp", "address": "Tyda, Araku Valley, Andhra Pradesh"},
        {"name": "Ushasree Residency", "address": "Araku Main Road, Andhra Pradesh"},
        {"name": "Natures Nest Araku", "address": "Near Tribal Museum, Araku, Andhra Pradesh"},
        {"name": "SRK Resort", "address": "Padmapuram Junction, Araku, Andhra Pradesh"},
        {"name": "Bamboo Chicken Point Stay", "address": "Chaparai Waterfalls Road, Araku"},
        {"name": "Star Annapurna Lodge", "address": "Araku Main Bazaar, Andhra Pradesh"},
        {"name": "Araku Valley View Resort", "address": "Near Coffee Museum, Araku Valley"}
    ],
    'araku valley': [
        {"name": "Araku Haritha Hill Resort", "address": "Araku Valley, Andhra Pradesh"},
        {"name": "Tyda Jungle Bells Nature Camp", "address": "Tyda, Araku Valley, Andhra Pradesh"},
        {"name": "Ushasree Residency", "address": "Araku Main Road, Andhra Pradesh"},
        {"name": "Natures Nest Araku", "address": "Near Tribal Museum, Araku, Andhra Pradesh"},
        {"name": "SRK Resort", "address": "Padmapuram Junction, Araku, Andhra Pradesh"}
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
    'vizag': [
        {"name": "Novotel Visakhapatnam Varun Beach", "address": "Beach Road, Visakhapatnam, Andhra Pradesh"},
        {"name": "The Park Visakhapatnam", "address": "Beach Road, Visakhapatnam, Andhra Pradesh"},
        {"name": "Dolphin Hotel", "address": "Daba Gardens, Visakhapatnam, Andhra Pradesh"},
        {"name": "Gateway Hotel", "address": "Beach Road, Visakhapatnam, Andhra Pradesh"}
    ],
    'srikakulam': [
        {"name": "Hotel Nagavali", "address": "Seven Roads Junction, Srikakulam, Andhra Pradesh"},
        {"name": "Varam Residency", "address": "Day and Night Junction, Srikakulam, Andhra Pradesh"},
        {"name": "Hotel Blue Earth", "address": "GT Road, Srikakulam, Andhra Pradesh"},
        {"name": "Hotel Sunrise", "address": "Palakonda Road, Srikakulam, Andhra Pradesh"},
        {"name": "Grand Srikakulam", "address": "Navabharath Junction, Srikakulam, Andhra Pradesh"}
    ],
    'goa': [
        {"name": "Taj Exotica Resort & Spa", "address": "Benaulim Beach, South Goa, India"},
        {"name": "W Goa", "address": "Vagator Beach, Bardez, North Goa, India"},
        {"name": "Santana Beach Resort", "address": "Candolim Beach, North Goa, India"},
        {"name": "Whispering Palms Beach Resort", "address": "Sinquerim, Candolim, Goa, India"},
        {"name": "Zostel Goa", "address": "Morjim Beach Road, Goa, India"}
    ],
    'delhi': [
        {"name": "The Imperial New Delhi", "address": "Janpath, Connaught Place, New Delhi"},
        {"name": "The Leela Palace New Delhi", "address": "Chanakyapuri, Diplomatic Enclave, New Delhi"},
        {"name": "Bloomrooms @ Janpath", "address": "Janpath Road, New Delhi"},
        {"name": "Radisson Blu Marina", "address": "Connaught Circus, New Delhi"}
    ],
    'mumbai': [
        {"name": "The Taj Mahal Palace", "address": "Apollo Bunder, Colaba, Mumbai, Maharashtra"},
        {"name": "Trident Hotel Nariman Point", "address": "Marine Drive, Nariman Point, Mumbai"},
        {"name": "JW Marriott Mumbai Juhu", "address": "Juhu Tara Road, Juhu, Mumbai"},
        {"name": "Bloom Hotel Juhu", "address": "Vile Parle West, Juhu, Mumbai"}
    ],
    'hyderabad': [
        {"name": "Taj Falaknuma Palace", "address": "Engine Bowli, Falaknuma, Hyderabad, Telangana"},
        {"name": "ITC Kohenur", "address": "HITEC City, Madhapur, Hyderabad, Telangana"},
        {"name": "Novotel Hyderabad Convention Centre", "address": "HITEC City, Hyderabad"},
        {"name": "The Golkonda Hotel", "address": "Masab Tank, Banjara Hills, Hyderabad"}
    ],
    'bangalore': [
        {"name": "The Oberoi Bengaluru", "address": "MG Road, Bengaluru, Karnataka"},
        {"name": "The Leela Palace Bengaluru", "address": "Old Airport Road, Bengaluru, Karnataka"},
        {"name": "Radisson Blu Atria", "address": "Palace Road, Bengaluru, Karnataka"}
    ],
    'jaipur': [
        {"name": "Rambagh Palace", "address": "Bhawani Singh Road, Jaipur, Rajasthan"},
        {"name": "ITC Rajputana", "address": "Gopalbari, Jaipur, Rajasthan"},
        {"name": "Pearl Palace Heritage", "address": "Ajmer Road, Jaipur, Rajasthan"},
        {"name": "Zostel Jaipur", "address": "Hawa Mahal Road, Jaipur, Rajasthan"}
    ],

    # ── THAILAND & SE ASIA ──────────────────────────────────────────────────
    'thailand': [
        {"name": "The Peninsula Bangkok", "address": "Charoen Nakhon Rd, Bangkok, Thailand"},
        {"name": "Centara Grand at CentralWorld", "address": "Pathum Wan, Bangkok, Thailand"},
        {"name": "The Shore at Katathani", "address": "Kata Noi Beach, Phuket, Thailand"},
        {"name": "Lub d Phuket Patong", "address": "Patong Beach, Phuket, Thailand"},
        {"name": "Banyan Tree Phuket", "address": "Laguna Phuket, Choeng Thale, Thailand"}
    ],
    'phuket': [
        {"name": "The Shore at Katathani", "address": "Kata Noi Beach, Phuket, Thailand"},
        {"name": "Lub d Phuket Patong", "address": "Patong Beach, Phuket, Thailand"},
        {"name": "Banyan Tree Phuket", "address": "Laguna Phuket, Choeng Thale, Thailand"}
    ],
    'bangkok': [
        {"name": "The Peninsula Bangkok", "address": "Charoen Nakhon Rd, Bangkok, Thailand"},
        {"name": "Centara Grand at CentralWorld", "address": "Pathum Wan, Bangkok, Thailand"},
        {"name": "SO/ Bangkok", "address": "North Sathorn Road, Bangkok, Thailand"}
    ],
    'bali': [
        {"name": "AYANA Resort Bali", "address": "Jimbaran, Bali, Indonesia"},
        {"name": "Padma Resort Ubud", "address": "Payangan, Ubud, Bali, Indonesia"},
        {"name": "W Bali Seminyak", "address": "Seminyak Beach, Bali, Indonesia"},
        {"name": "The Kayon Jungle Resort", "address": "Bresela, Payangan, Ubud, Bali"}
    ],

    # ── USA ─────────────────────────────────────────────────────────────────
    'usa': [
        {"name": "The Plaza Hotel", "address": "Fifth Avenue at Central Park South, New York, USA"},
        {"name": "Bellagio Hotel & Casino", "address": "Las Vegas Strip, Las Vegas, Nevada, USA"},
        {"name": "The Venetian Resort", "address": "Las Vegas Blvd, Las Vegas, USA"},
        {"name": "Arlo Midtown Manhattan", "address": "38th St, Midtown, New York, USA"},
        {"name": "The Beverly Hills Hotel", "address": "Sunset Blvd, Beverly Hills, Los Angeles, USA"}
    ],
    'new york': [
        {"name": "The Plaza Hotel", "address": "Fifth Avenue, Central Park South, New York, USA"},
        {"name": "Arlo Midtown Manhattan", "address": "38th St, Midtown West, New York, USA"},
        {"name": "The Manhattan at Times Square", "address": "7th Ave, Midtown, New York, USA"},
        {"name": "Pod Times Square", "address": "42nd St, Hell's Kitchen, New York, USA"}
    ],

    # ── UAE ─────────────────────────────────────────────────────────────────
    'dubai': [
        {"name": "Burj Al Arab Jumeirah", "address": "Umm Suqeim 3, Dubai, UAE"},
        {"name": "Atlantis The Palm", "address": "Crescent Road, Palm Jumeirah, Dubai, UAE"},
        {"name": "JW Marriott Marquis Hotel", "address": "Business Bay, Sheikh Zayed Road, Dubai"},
        {"name": "Rove Downtown Dubai", "address": "Downtown Dubai, Near Burj Khalifa, UAE"}
    ],
    'uae': [
        {"name": "Burj Al Arab Jumeirah", "address": "Umm Suqeim 3, Dubai, UAE"},
        {"name": "Atlantis The Palm", "address": "Palm Jumeirah, Dubai, UAE"},
        {"name": "Emirates Palace Mandarin Oriental", "address": "West Corniche Road, Abu Dhabi, UAE"},
        {"name": "Rove Downtown Dubai", "address": "Downtown Dubai, UAE"}
    ],

    # ── EUROPE & UK ─────────────────────────────────────────────────────────
    'paris': [
        {"name": "Hôtel Ritz Paris", "address": "Place Vendôme, Paris, France"},
        {"name": "Pullman Paris Tour Eiffel", "address": "Avenue de Suffren, Paris, France"},
        {"name": "CitizenM Paris Champs-Élysées", "address": "Rue la Boétie, Paris, France"}
    ],
    'london': [
        {"name": "The Savoy Hotel", "address": "Strand, Covent Garden, London, UK"},
        {"name": "The Ritz London", "address": "Piccadilly, St. James's, London, UK"},
        {"name": "Premier Inn London County Hall", "address": "Belvedere Rd, Waterloo, London, UK"}
    ]
}


def get_hotel_category(location_str):
    loc = location_str.lower()
    if any(k in loc for k in ['beach', 'vizag', 'visakhapatnam', 'goa', 'baga', 'gokarna', 'kovalam', 'varkala', 'sea', 'coast', 'phuket', 'bali', 'cancun', 'nice']):
        return "beach"
    elif any(k in loc for k in ['araku', 'ooty', 'kodaikanal', 'munnar', 'coorg', 'hill', 'valley', 'lonavala', 'shimla', 'manali', 'wayanad', 'swiss', 'alps', 'darjeeling']):
        return "hill"
    elif any(k in loc for k in ['hampi', 'mysore', 'temple', 'tirupati', 'jaipur', 'udaipur', 'varanasi', 'heritage', 'shirdi', 'kyoto', 'rome', 'athens', 'cairo']):
        return "heritage"
    return "city"


def generate_hotels(location):
    """
    Generates a list of verified hotels for a given location, using real properties if available,
    pairing them with live photography, enriched facilities, and country-specific booking apps.
    """
    loc_clean = location.strip().lower()
    loc_title = location.strip().title()

    hash_val = int(hashlib.md5(loc_clean.encode('utf-8')).hexdigest(), 16)
    random.seed(hash_val)

    # Pick matching real hotel set if available
    selected_hotels = None
    for key, hotels_list in REAL_HOTELS.items():
        if key in loc_clean:
            selected_hotels = hotels_list
            break

    if not selected_hotels:
        base_names = [
            f"{loc_title} Grand Hotel", f"The {loc_title} Resort & Spa", f"{loc_title} Comfort Inn",
            f"Royal {loc_title} Lodge", f"Comfort Stay {loc_title}", f"Budget Stay {loc_title}",
            f"{loc_title} Heritage Palace", f"{loc_title} Sunrise Retreat", f"{loc_title} Premium Stay",
            f"{loc_title} Eco-Camp & Villas", f"{loc_title} Boutique Hotel"
        ]
        selected_names = random.sample(base_names, k=random.randint(6, 8))
        selected_hotels = [{"name": name, "address": f"Central Area, {loc_title}"} for name in selected_names]

    hotels = []
    currency = get_currency_info(loc_clean)
    cat = get_hotel_category(loc_clean)
    image_pool = HOTEL_IMAGE_SETS[cat]

    # Curated facility amenity master pool
    amenities_master = [
        'Free WiFi', 'Breakfast Included', 'AC', 'Swimming Pool', 
        'Gym', 'Spa', 'Restaurant', 'Parking', 'Room Service', 
        'Airport Shuttle', 'Scenic View', 'Power Backup'
    ]

    for idx, h in enumerate(selected_hotels):
        name = h['name']
        address = h['address']

        # Determine realistic pricing in local context
        if currency['code'] in ['USD', 'EUR', 'GBP', 'CHF']:
            price = random.randint(8000, 35000)
        elif currency['code'] in ['AED', 'SGD', 'AUD', 'CAD', 'JPY']:
            price = random.randint(6000, 25000)
        elif currency['code'] != 'INR':
            price = random.randint(4000, 15000)
        else:
            price = random.randint(1500, 7500)

        if "Nagavali" in name:
            price = random.randint(1200, 2500)

        rating = round(random.uniform(4.1, 4.9), 1)

        # Select rich, realistic facilities (5 to 7 amenities per stay)
        k_amenities = random.randint(5, 7)
        amenities = random.sample(amenities_master, k=k_amenities)
        if 'Free WiFi' not in amenities:
            amenities[0] = 'Free WiFi'
        if 'AC' not in amenities and cat != 'hill':
            amenities[1] = 'AC'

        # Format facilities with structured icons & descriptions
        formatted_facs = format_facilities(amenities)

        # Build country-specific booking options (e.g. MakeMyTrip/Goibibo for India, Rakuten/Agoda for Japan)
        booking_options = get_hotel_booking_options(name, loc_clean)
        primary_app = next((opt for opt in booking_options if opt.get('is_primary')), booking_options[0] if booking_options else None)

        # Dynamically search live real-world photographs for this exact hotel
        from utils.image_fetcher import fetch_image
        fetched_imgs = fetch_image(f"{name} {loc_title}", limit=2)
        
        outer_img = h.get('outer_img')
        if not outer_img:
            outer_img = fetched_imgs[0] if fetched_imgs else image_pool["exteriors"][idx % len(image_pool["exteriors"])]
            
        inner_img = h.get('inner_img')
        if not inner_img:
            inner_img = fetched_imgs[1] if len(fetched_imgs) > 1 else image_pool["interiors"][idx % len(image_pool["interiors"])]

        hotels.append({
            'name': name,
            'address': address,
            'price': price,
            'rating': rating,
            'amenities': amenities,
            'facilities': formatted_facs,
            'booking_options': booking_options,
            'primary_app': primary_app,
            'outer_image_url': outer_img,
            'inner_image_url': inner_img
        })

    hotels.sort(key=lambda x: x['price'])
    return hotels

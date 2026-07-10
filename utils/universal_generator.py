import urllib.request
import urllib.parse
import json
import hashlib
import random

def generate_universal_destination(place_name):
    """
    Attempts to generate a realistic destination profile for ANY place on Earth 
    using the Wikipedia API and deterministic hashing.
    """
    # Clean up place name
    place_name = place_name.strip().title()
    formatted_place = place_name.replace(' ', '_')
    
    # Ping Wikipedia API
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(formatted_place)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'TripTics/1.0'})
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            if data.get('type') in ['disambiguation', 'no-extract']:
                return None
            
            title = data.get('title', place_name)
            extract = data.get('extract', f"A beautiful destination located in {title}.")
            
            # Deterministic pseudo-random generation based on place name hash
            # This ensures if they search "Greenland" twice, costs remain the same
            hash_val = int(hashlib.md5(title.encode('utf-8')).hexdigest(), 16)
            random.seed(hash_val)
            
            # Generate costs (realistic ranges)
            travel = random.randint(1500, 15000)
            hotel = random.randint(1000, 10000)
            food = random.randint(500, 3000)
            local_transport = random.randint(200, 2000)
            shopping = random.randint(500, 5000)
            
            dest_type = random.choice(['City', 'Nature', 'Historical', 'Beach', 'Adventure'])
            crowd = random.choice(['Low', 'Medium', 'High'])
            family = random.choice(['Yes', 'No'])
            accom_type = random.choice(['Boutique Hotel', 'Standard Hotel', 'Resort', 'Guesthouse', 'Homestay'])
            
            # Base DataFrame row
            dest_row = {
                'Destination': f"Downtown {title}",
                'State': title,
                'Type': dest_type,
                'Avg_Travel_Cost': travel,
                'Avg_Hotel_Per_Day': hotel,
                'Avg_Food_Per_Day_Per_Person': food,
                'Avg_Local_Travel_Per_Day': local_transport,
                'Avg_Shopping_Cost': shopping,
                'Attractions': f"The central hub of {title}, vibrant local markets, and historic landmarks.",
                'Crowd_Level': crowd,
                'Family_Friendly': family,
                'Accommodation_Type': accom_type,
                'Shopping_Items': "Local souvenirs, postcards, and regional specialties"
            }
            
            # Three destinations to give them options
            dest_row_2 = dest_row.copy()
            dest_row_2['Destination'] = f"Scenic Outskirts of {title}"
            dest_row_2['Type'] = 'Nature'
            dest_row_2['Avg_Travel_Cost'] = travel + random.randint(100, 500)
            dest_row_2['Avg_Hotel_Per_Day'] = hotel - random.randint(100, 500)
            dest_row_2['Attractions'] = f"Beautiful natural landscapes and trails surrounding {title}."
            dest_row_2['Accommodation_Type'] = 'Eco-Resort / Cabin'
            
            dest_row_3 = dest_row.copy()
            dest_row_3['Destination'] = f"Historic District of {title}"
            dest_row_3['Type'] = 'Historical'
            dest_row_3['Avg_Hotel_Per_Day'] = hotel + random.randint(100, 1000)
            dest_row_3['Attractions'] = f"Museums, old town architecture, and cultural heritage sites of {title}."
            dest_row_3['Accommodation_Type'] = 'Heritage Hotel'
            
            # Fetch exact location banner image using DuckDuckGo Images Search
            image_url = ""
            try:
                import re, json
                ddg_query = urllib.parse.quote(f"{title} landscape travel photography")
                
                req = urllib.request.Request(
                    f"https://duckduckgo.com/?q={ddg_query}&ia=images",
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
                vqd_match = re.search(r'vqd=([\d-]+)', html)
                if vqd_match:
                    vqd = vqd_match.group(1)
                    req2 = urllib.request.Request(
                        f"https://duckduckgo.com/i.js?q={ddg_query}&o=json&vqd={vqd}",
                        headers={'User-Agent': 'Mozilla/5.0'}
                    )
                    res = urllib.request.urlopen(req2, timeout=5).read().decode('utf-8')
                    data = json.loads(res)
                    if data.get('results'):
                        image_url = data['results'][0]['image']
            except Exception as e:
                print("DDG image fetch error in generator:", e)

            # Dynamic State Info
            dynamic_state_info = {
                "title": f"Discover {title}",
                "description": extract,
                "color": random.choice(["primary", "success", "info", "warning", "dark"]),
                "must_visit": [f"{title} Central Plaza", f"{title} Museum", f"Scenic Viewpoint of {title}", f"Historic {title} Quarter"],
                "image_url": image_url
            }
            
            return {
                'rows': [dest_row, dest_row_2, dest_row_3],
                'state_info': dynamic_state_info
            }
            
    except Exception as e:
        print("Universal Generator Error:", e)
        return None

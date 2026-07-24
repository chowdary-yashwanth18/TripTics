import os
import urllib.request
import urllib.parse
import json

def get_google_api_key():
    key = os.environ.get('GOOGLE_PLACES_API_KEY', '')
    if key: return key
    
    # Custom fallback to read .env file since python-dotenv might not be installed
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    try:
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    k, v = line.strip().split('=', 1)
                    if k.strip() == 'GOOGLE_PLACES_API_KEY':
                        return v.strip().strip('"').strip("'")
    except Exception:
        pass
    return ""

def get_place_photo_url(photo_reference, max_width=400):
    """
    Returns a secure backend proxy URL for the photo.
    This completely bypasses frontend CORS and API Key IP restrictions.
    """
    api_key = get_google_api_key()
    if not photo_reference or not api_key:
        return ""
    
    # We pass the reference to our Flask backend which will fetch and proxy the image securely
    return f"/api/photo?photoreference={photo_reference}&maxwidth={max_width}"

def get_tourist_attractions(location, limit=20):
    """
    Fetches the top tourist attractions for a given location using Google Places API.
    Returns (attractions_list, diagnostics_dict).
    """
    api_key = get_google_api_key()
    diagnostics = {
        "api_key_present": bool(api_key),
        "text_search_status": "Not Attempted",
        "raw_response": None,
        "error": None
    }
    
    def get_fallback_attractions(error_message):
        # Fallback if API fails or key is missing: Generate mock cards but with REAL images from Wikimedia
        import utils.image_fetcher as img_fetch
        
        fallback_attractions = []
        # Generate some generic but real-sounding attraction names
        places = [f"Downtown {location}", f"{location} Historical Center", f"Famous Landmark in {location}", f"{location} Museum"]
        
        for i, place_name in enumerate(places[:limit]):
            photo = img_fetch.fetch_image(place_name) or "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=1200&q=80"
            fallback_attractions.append({
                "place_id": f"mock_id_{i}",
                "name": place_name,
                "rating": 4.5,
                "address": f"Central {location}",
                "description": "Live data currently unavailable. Showing fallback attractions.",
                "photo_url": photo,
                "duration": "2 hours",
                "entry_fee": "Free"
            })
        return (fallback_attractions, diagnostics)

    if not api_key:
        return get_fallback_attractions("API Key is missing")

    # 1. Text Search for top attractions
    query = f"famous places, beaches, and attractions in {location}"
    search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={urllib.parse.quote(query)}&key={api_key}"
    
    try:
        req = urllib.request.Request(search_url)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            diagnostics['raw_response'] = data
            diagnostics['text_search_status'] = data.get('status', 'UNKNOWN')
            if data.get('status') != 'OK':
                error_msg = data.get('error_message', f"API Status: {data.get('status')}")
                diagnostics['error'] = error_msg
                return get_fallback_attractions(error_msg)
            
        results = data.get('results', [])[:limit]
        attractions = []
        
        for place in results:
            place_id = place.get('place_id')
            name = place.get('name')
            rating = place.get('rating', 'N/A')
            address = place.get('formatted_address', '')
            
            photo_url = ""
            photos = place.get('photos', [])
            if photos:
                photo_url = get_place_photo_url(photos[0].get('photo_reference'))
                
            # We can optionally call Place Details here to get editorial_summary.
            # To save API calls and latency, we'll try to use a fallback description from types.
            types = place.get('types', [])
            clean_types = [t.replace('_', ' ').title() for t in types if t not in ['point_of_interest', 'establishment']]
            type_desc = ", ".join(clean_types[:2]) if clean_types else "Tourist Attraction"
            description = f"Popular {type_desc.lower()} located in {location}."
            
            attractions.append({
                "place_id": place_id,
                "name": name,
                "rating": rating,
                "address": address,
                "description": description,
                "photo_url": photo_url,
                "duration": "1-3 hours", # Generic placeholder as Google API lacks this
                "entry_fee": "Check Official Site" # Generic placeholder
            })
            
        return (attractions, diagnostics)
    except urllib.error.HTTPError as e:
        error_msg = f"HTTP Error {e.code}: {e.read().decode()}"
        diagnostics['error'] = error_msg
        print(f"Error fetching Google Places: {diagnostics['error']}")
        return get_fallback_attractions(error_msg)
    except Exception as e:
        error_msg = str(e)
        diagnostics['error'] = error_msg
        print(f"Error fetching Google Places: {e}")
        return get_fallback_attractions(error_msg)

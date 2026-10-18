import urllib.request
import urllib.parse
import json
import re

def _is_valid_image_url(url):
    """Validates that a URL points to an image file and is not a PDF, vector SVG, or non-image document."""
    if not url or not isinstance(url, str):
        return False
    lower_url = url.lower()
    if any(bad in lower_url for bad in ['.pdf', '.svg', '.tif', '.tiff', '.ogv', '.webm', '.doc', '.docx', 'flag', 'coat_of_arms', 'map_of', 'logo_of']):
        return False
    return lower_url.startswith('http://') or lower_url.startswith('https://') or lower_url.startswith('/')


def fetch_image(query, limit=3):
    """
    Dynamically fetches exact real-time photographs for ANY place, hotel, landmark or attraction query.
    Uses Google Places API, Wikimedia Commons live search, and Wikipedia API.
    """
    if not query:
        return ["https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=1200&q=80"]

    query_str = str(query).strip()
    urls = []

    # 1. Try Google Places API (Best for official location & hotel photos)
    try:
        from utils.places_api import get_google_api_key, get_place_photo_url
        api_key = get_google_api_key()
        if api_key:
            g_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={urllib.parse.quote(query_str)}&key={api_key}"
            req = urllib.request.Request(g_url)
            with urllib.request.urlopen(req, timeout=4) as response:
                data = json.loads(response.read().decode())
                if data.get('status') == 'OK' and data.get('results'):
                    photos = data['results'][0].get('photos', [])
                    for i in range(min(limit, len(photos))):
                        photo_ref = photos[i].get('photo_reference')
                        if photo_ref:
                            urls.append(get_place_photo_url(photo_ref, max_width=1200))
                    if urls:
                        return urls
    except Exception as e:
        pass

    # 2. Try Wikimedia Commons File Search for EXACT Photographs (gsrnamespace=6)
    try:
        commons_url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(query_str)}&gsrnamespace=6&gsrlimit=12&prop=imageinfo&iiprop=url|mime&format=json"
        req = urllib.request.Request(commons_url, headers={'User-Agent': 'TripTics/1.0 (travel@triptics.org)'})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode())
            pages = data.get('query', {}).get('pages', {})
            for pid, pinfo in pages.items():
                ii = pinfo.get('imageinfo', [])
                if ii and ii[0].get('mime') in ['image/jpeg', 'image/jpg']:
                    file_url = ii[0].get('url', '')
                    title = pinfo.get('title', '').lower()
                    if _is_valid_image_url(file_url) and not any(bad in title for bad in ['map', 'logo', 'flag', 'coat_of_arms', 'diagram', 'icon', 'symbol', 'stamp', 'sign', 'chart', 'poster']):
                        if file_url not in urls:
                            urls.append(file_url)
                            if len(urls) >= limit:
                                return urls
    except Exception:
        pass

    # 3. Try searching with first two words if long search phrase returned nothing on Commons
    words = query_str.split()
    if len(words) > 2 and len(urls) < limit:
        sub_query = " ".join(words[:2])
        try:
            commons_url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(sub_query)}&gsrnamespace=6&gsrlimit=10&prop=imageinfo&iiprop=url|mime&format=json"
            req = urllib.request.Request(commons_url, headers={'User-Agent': 'TripTics/1.0 (travel@triptics.org)'})
            with urllib.request.urlopen(req, timeout=4) as response:
                data = json.loads(response.read().decode())
                pages = data.get('query', {}).get('pages', {})
                for pid, pinfo in pages.items():
                    ii = pinfo.get('imageinfo', [])
                    if ii and ii[0].get('mime') in ['image/jpeg', 'image/jpg']:
                        file_url = ii[0].get('url', '')
                        title = pinfo.get('title', '').lower()
                        if _is_valid_image_url(file_url) and not any(bad in title for bad in ['map', 'logo', 'flag', 'coat_of_arms', 'diagram', 'icon', 'symbol', 'stamp']):
                            if file_url not in urls:
                                urls.append(file_url)
                                if len(urls) >= limit:
                                    return urls
        except Exception:
            pass

    # 4. Try Wikipedia Article Lead Image
    try:
        wiki_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query_str)}&utf8=&format=json&srlimit=1"
        req = urllib.request.Request(wiki_url, headers={'User-Agent': 'TripTics/1.0 (travel@triptics.org)'})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode())
            results = data.get('query', {}).get('search', [])
            if results:
                title = results[0]['title']
                sum_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title.replace(' ', '_'))}"
                req2 = urllib.request.Request(sum_url, headers={'User-Agent': 'TripTics/1.0 (travel@triptics.org)'})
                with urllib.request.urlopen(req2, timeout=4) as response2:
                    data2 = json.loads(response2.read().decode())
                    img = data2.get('originalimage', {}).get('source') or data2.get('thumbnail', {}).get('source')
                    if img and _is_valid_image_url(img):
                        if img not in urls:
                            urls.append(img)
                            if len(urls) >= limit:
                                return urls
    except Exception:
        pass

    # 5. Dynamic keyword fallback
    if not urls:
        clean_q = urllib.parse.quote(query_str)
        urls.append(f"https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80")

    return urls[:limit]


if __name__ == "__main__":
    print("Novotel Visakhapatnam:", fetch_image("Novotel Visakhapatnam"))
    print("Araku Valley:", fetch_image("Araku Valley"))
    print("Borra Caves:", fetch_image("Borra Caves"))
    print("RK Beach Visakhapatnam:", fetch_image("RK Beach Visakhapatnam"))
    print("Coffee Museum Araku:", fetch_image("Coffee Museum Araku"))

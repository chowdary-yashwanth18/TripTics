import urllib.request
import urllib.parse
import json
import re

def fetch_image(query):
    # Adjust query based on location type for better imagery
    lower_query = query.lower()
    search_query = query
    
    if 'beach' in lower_query:
        search_query = query + " aerial view"
    elif any(kw in lower_query for kw in ['hotel', 'restaurant', 'cafe', 'resort', 'novotel']):
        search_query = query + " exterior building architecture"
        
    # 1. Try Google Places API (Best for accurate location photos)
    try:
        from utils.places_api import get_google_api_key, get_place_photo_url
        api_key = get_google_api_key()
        if api_key:
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={urllib.parse.quote(search_query)}&key={api_key}"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                if data.get('status') == 'OK' and data.get('results'):
                    photos = data['results'][0].get('photos', [])
                    if photos:
                        urls = []
                        for i in range(min(3, len(photos))):
                            urls.append(get_place_photo_url(photos[i]['photo_reference'], max_width=1200))
                        return urls
    except Exception as e:
        print(f"Google Places Image Fetch Error for {query}:", e)

    # 2. Try Wikimedia Commons Search API (Best for specific places like 'Coffee Museum')
    try:
        search_url = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=File:{urllib.parse.quote(query)}&utf8=&format=json&srlimit=3"
        req = urllib.request.Request(search_url, headers={'User-Agent': 'TripTics/1.0 (test@example.com)'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            search_results = data.get('query', {}).get('search', [])
            if search_results:
                titles = "|".join([urllib.parse.quote(res['title']) for res in search_results])
                info_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={titles}&prop=imageinfo&iiprop=url&format=json"
                req2 = urllib.request.Request(info_url, headers={'User-Agent': 'TripTics/1.0 (test@example.com)'})
                with urllib.request.urlopen(req2, timeout=5) as response2:
                    data2 = json.loads(response2.read().decode())
                    pages = data2.get('query', {}).get('pages', {})
                    urls = []
                    for page_id, page_info in pages.items():
                        if 'imageinfo' in page_info:
                            urls.append(page_info['imageinfo'][0]['url'])
                    if urls:
                        return urls
    except Exception:
        pass

    # 2. Try Wikipedia Article Search API (Best for major cities/states)
    try:
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&utf8=&format=json&srlimit=1"
        req = urllib.request.Request(search_url, headers={'User-Agent': 'TripTics/1.0 (test@example.com)'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            search_results = data.get('query', {}).get('search', [])
            if search_results:
                title = search_results[0]['title']
                summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title.replace(' ', '_'))}"
                req2 = urllib.request.Request(summary_url, headers={'User-Agent': 'TripTics/1.0 (test@example.com)'})
                with urllib.request.urlopen(req2, timeout=5) as response2:
                    data2 = json.loads(response2.read().decode())
                    if 'originalimage' in data2:
                        return data2['originalimage']['source']
                    elif 'thumbnail' in data2:
                        return data2['thumbnail']['source']
    except Exception:
        pass

    # 4. Try Commons with just the first part of the query
    try:
        first_part = query.split(',')[0].split('-')[0].strip()
        search_url = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=File:{urllib.parse.quote(first_part)}&utf8=&format=json&srlimit=3"
        req = urllib.request.Request(search_url, headers={'User-Agent': 'TripTics/1.0 (test@example.com)'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            search_results = data.get('query', {}).get('search', [])
            if search_results:
                titles = "|".join([urllib.parse.quote(res['title']) for res in search_results])
                info_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={titles}&prop=imageinfo&iiprop=url&format=json"
                req2 = urllib.request.Request(info_url, headers={'User-Agent': 'TripTics/1.0 (test@example.com)'})
                with urllib.request.urlopen(req2, timeout=5) as response2:
                    data2 = json.loads(response2.read().decode())
                    pages = data2.get('query', {}).get('pages', {})
                    urls = []
                    for page_id, page_info in pages.items():
                        if 'imageinfo' in page_info:
                            urls.append(page_info['imageinfo'][0]['url'])
                    if urls:
                        return urls
    except Exception:
        pass

    # 5. Try Wikipedia for just the last word (usually the city/state) using Wikimedia Commons to get scenery
    try:
        last_part = query.split()[-1].strip()
        search_url = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=File:{urllib.parse.quote(last_part)}&utf8=&format=json&srlimit=3"
        req = urllib.request.Request(search_url, headers={'User-Agent': 'TripTics/1.0 (test@example.com)'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            search_results = data.get('query', {}).get('search', [])
            if search_results:
                titles = "|".join([urllib.parse.quote(res['title']) for res in search_results])
                info_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={titles}&prop=imageinfo&iiprop=url&format=json"
                req2 = urllib.request.Request(info_url, headers={'User-Agent': 'TripTics/1.0 (test@example.com)'})
                with urllib.request.urlopen(req2, timeout=5) as response2:
                    data2 = json.loads(response2.read().decode())
                    pages = data2.get('query', {}).get('pages', {})
                    urls = []
                    for page_id, page_info in pages.items():
                        if 'imageinfo' in page_info:
                            urls.append(page_info['imageinfo'][0]['url'])
                    if urls:
                        return urls
    except Exception:
        pass

    # 6. Final Fallback (Generic Beautiful Travel Image)
    return ["https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=1200&q=80"]

if __name__ == "__main__":
    print("Italy:", fetch_image("Italy"))
    print("Amalfi Coast:", fetch_image("Amalfi Coast"))
    print("Araku Valley:", fetch_image("Araku Valley"))
    print("RandomGibberish:", fetch_image("RandomGibberishxyz"))

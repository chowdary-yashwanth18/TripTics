import urllib.request
import urllib.parse
import json
import re

def fetch_image(query):
    # 1. Try Wikipedia API (Best for accuracy and high quality)
    try:
        # Try exact query first
        formatted = urllib.parse.quote(query.strip().title().replace(' ', '_'))
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted}"
        req = urllib.request.Request(url, headers={'User-Agent': 'TripTics/1.0 (test@example.com)'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            if 'originalimage' in data:
                return data['originalimage']['source']
            elif 'thumbnail' in data:
                return data['thumbnail']['source']
    except Exception:
        pass

    # Try Wikipedia with just the first part of the query (e.g. "Amalfi Coast Italy" -> "Amalfi Coast")
    try:
        first_part = query.split(',')[0].split('-')[0].strip()
        formatted = urllib.parse.quote(first_part.title().replace(' ', '_'))
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted}"
        req = urllib.request.Request(url, headers={'User-Agent': 'TripTics/1.0 (test@example.com)'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            if 'originalimage' in data:
                return data['originalimage']['source']
            elif 'thumbnail' in data:
                return data['thumbnail']['source']
    except Exception:
        pass

    # 2. Fallback to a highly constrained DDG search if Wikipedia fails
    try:
        ddg_query = urllib.parse.quote(f"{query} famous landmark travel photography")
        req = urllib.request.Request(
            f"https://duckduckgo.com/?q={ddg_query}&ia=images",
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        vqd_match = re.search(r'vqd=([\d-]+)', html)
        if vqd_match:
            vqd = vqd_match.group(1)
            url2 = f"https://duckduckgo.com/i.js?q={ddg_query}&o=json&vqd={vqd}"
            req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req2, timeout=5).read().decode('utf-8')
            data = json.loads(res)
            if data.get('results'):
                return data['results'][0]['image']
    except Exception as e:
        pass

    # 3. Final Fallback (Generic Beautiful Travel Image from Wikimedia)
    return "https://upload.wikimedia.org/wikipedia/commons/e/ec/World_map_blank_with_blue_sea.png"

if __name__ == "__main__":
    print("Italy:", fetch_image("Italy"))
    print("Amalfi Coast:", fetch_image("Amalfi Coast"))
    print("Araku Valley:", fetch_image("Araku Valley"))
    print("RandomGibberish:", fetch_image("RandomGibberishxyz"))

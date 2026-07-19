import sys
sys.path.append('.')
from app import app

client = app.test_client()

data = {
    'budget': '50000',
    'days': '5',
    'travelers': '2',
    'target_state': 'florida',
    'budget_currency': 'INR',
    'outbound_transport': 'any',
    'return_transport': 'any'
}

response = client.post('/planner', data=data)
html = response.data.decode('utf-8')

if "No destinations found!" in html:
    print("Found 'No destinations found!'")
elif "No destinations available" in html:
    print("Found 'No destinations available'")
else:
    print("Neither found. Success?")

from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
danger_text = soup.find_all(class_='text-danger')
for dt in danger_text:
    print("Danger text:", dt.text.strip())
cards = soup.find_all(class_='card-title')
print(f"Cards found: {len(cards)}")
for c in cards:
    print("Card:", c.text.strip())

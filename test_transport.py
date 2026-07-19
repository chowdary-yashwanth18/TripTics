from utils.transport_generator import generate_transport
import json

options = generate_transport('Araku', 'Florida', 'flight', is_international=True)
print(json.dumps(options, indent=2))

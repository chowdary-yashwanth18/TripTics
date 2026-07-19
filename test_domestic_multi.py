from utils.transport_generator import generate_transport
import json

options = generate_transport('Araku', 'Delhi', 'flight', is_international=False)
print(json.dumps(options, indent=2))

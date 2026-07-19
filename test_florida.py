import sys
sys.path.append('.')
from utils.universal_generator import generate_universal_destination

try:
    res = generate_universal_destination('florida')
    print("Result:")
    print(res)
except Exception as e:
    print("Exception:")
    print(e)

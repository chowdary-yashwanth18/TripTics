import sys
import pandas as pd
sys.path.append('.')
from utils.recommender import recommend_destinations
from utils.data_loader import load_destinations

df = load_destinations()
budget = 50000
days = 3
travelers = 2
trip_type = 'all'
budget_style = 'all'
target_state = 'florida'
starting_city = ''
outbound_transport = 'any'
return_transport = 'any'

res = recommend_destinations(df, budget, days, travelers, trip_type, budget_style, target_state, starting_city, outbound_transport, return_transport)
print(f"Matches: {len(res['matches'])}")
print(f"Alternatives: {len(res['alternatives'])}")
if 'dynamic_state_info' in res:
    print(f"Dynamic State Info: {'Yes' if res['dynamic_state_info'] else 'No'}")

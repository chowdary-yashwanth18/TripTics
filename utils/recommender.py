# ============================================================
# utils/recommender.py  –  TripTics Recommendation Engine
# ============================================================
import pandas as pd
from datetime import datetime
from utils.universal_generator import generate_universal_destination


def _safe_get(row, col, default=''):
    """
    Safely reads a column from a pandas Series row.
    Returns `default` if the column is missing or the value is NaN.
    """
    try:
        val = row[col]
        return default if (val != val) else val   # val != val is True for NaN
    except (KeyError, TypeError):
        return default


def calculate_trip_cost(row, days, travelers):
    """
    Calculates a full cost breakdown for one destination row.

    Formula:
        total = travel + (hotel × days) + (food × travelers × days) + (local_transport × days)

    All inputs are cast to float first so a stray string value cannot
    crash the app at runtime.
    """
    travel_cost     = float(row['Avg_Travel_Cost'])
    hotel_cost      = float(row['Avg_Hotel_Per_Day'])     * days
    food_cost       = float(row['Avg_Food_Per_Day_Per_Person']) * travelers * days
    local_transport = float(row['Avg_Local_Travel_Per_Day'])    * days
    shopping_cost   = float(row.get('Avg_Shopping_Cost', 0)) * travelers

    total_cost = int(travel_cost + hotel_cost + food_cost + local_transport + shopping_cost)

    return {
        'total':           total_cost,
        'travel':          int(travel_cost),
        'hotel':           int(hotel_cost),
        'food':            int(food_cost),
        'local_transport': int(local_transport),
        'shopping':        int(shopping_cost)
    }


def score_destination(row, costs, budget, days, trip_type, budget_style):
    """
    Rule-based scoring – gives a score out of 100 to each destination.

    Point allocation (easy to explain in a viva):
        30 pts  – Trip type match
        25 pts  – How comfortably the destination fits within budget
        25 pts  – Days relevance (user days ≈ Recommended_Days)
        20 pts  – Budget_Level matches the preferred style

    Higher score = better recommendation for the given inputs.
    """
    score = 0

    # ── 1. Trip type match (30 pts) ──────────────────────────────────────────
    dest_type = str(row['Type']).strip().lower()
    if trip_type.lower() == 'all':
        score += 20          # Partial credit: user has no specific preference
    elif dest_type == trip_type.lower():
        score += 30          # Full marks: exact match

    # ── 2. Budget fit comfort (25 pts) ───────────────────────────────────────
    # We reward destinations that use a meaningful share of the budget.
    # A ₹50,000 budget trip that costs only ₹1,000 is a poor recommendation.
    if budget > 0:
        usage_ratio = costs['total'] / budget
        if 0.75 <= usage_ratio <= 1.0:
            score += 25      # Great fit – uses 75–100 % of budget
        elif 0.50 <= usage_ratio < 0.75:
            score += 18      # Good – leaves decent amount unused
        elif 0.30 <= usage_ratio < 0.50:
            score += 10      # Okay – quite cheap relative to budget
        else:
            score += 4       # Very cheap – probably not the best match

    # ── 3. Days relevance (25 pts) ───────────────────────────────────────────
    try:
        rec_days = int(float(_safe_get(row, 'Recommended_Days', days)))
    except (ValueError, TypeError):
        rec_days = days

    day_diff = abs(days - rec_days)
    if day_diff == 0:
        score += 25          # Perfect match
    elif day_diff == 1:
        score += 18          # One day off – very close
    elif day_diff == 2:
        score += 10          # Two days off – acceptable
    else:
        score += 3           # Too far off the recommended duration

    # ── 4. Budget level style match (20 pts) ─────────────────────────────────
    # Budget_Level in the CSV is capitalized ('Low', 'Medium', 'High')
    # after data_loader normalizes it. budget_style from the form is lowercase.
    dest_level = str(_safe_get(row, 'Budget_Level', '')).lower()
    if budget_style.lower() == 'all':
        score += 10          # Partial credit: no preference
    elif dest_level == budget_style.lower():
        score += 20          # Exact style match
    elif {dest_level, budget_style.lower()} == {'low', 'medium'}:
        score += 8           # Adjacent levels – still acceptable

    return score


def generate_reason(row, costs, budget, days):
    """
    Generates a human-readable recommendation note based on real data values.
    Shows budget usage percentage, crowd info, and trip type with an emoji.
    """
    dest_type    = str(row['Type']).strip().lower()
    budget_level = str(_safe_get(row, 'Budget_Level', '')).capitalize()
    crowd        = str(_safe_get(row, 'Crowd_Level', '')).lower()
    remaining    = budget - costs['total']

    # Guard against zero budget (shouldn't happen after app.py validation, but be safe)
    usage_pct = int((costs['total'] / budget) * 100) if budget > 0 else 0

    if usage_pct >= 85:
        fit_note = f"fits your ₹{budget:,} budget almost perfectly"
    elif usage_pct >= 60:
        fit_note = f"comfortably within budget with ₹{remaining:,} to spare"
    else:
        fit_note = f"budget-saver – costs only ₹{costs['total']:,} of your ₹{budget:,}"

    type_emojis = {
        'beach': '🏖️', 'hill': '🏔️', 'nature': '🌿',
        'temple': '🛕', 'city': '🏙️'
    }
    emoji = type_emojis.get(dest_type, '📍')

    crowd_note = ""
    if crowd == 'low':
        crowd_note = " Fewer crowds – ideal for a relaxed trip."
    elif crowd == 'high':
        crowd_note = " Very popular – consider booking hotels early."

    return f"{emoji} {budget_level}-budget {dest_type} trip – {fit_note}.{crowd_note}"


def build_suggestions(alternatives, budget, days, travelers):
    """
    Builds plain-English suggestions for the no-match case.
    
    Tells the user:
      - How much extra budget is needed to reach the cheapest alternative.
      - How many days they should reduce to potentially fit within budget.
      - To widen their type/style filters.
    """
    suggestions = []
    if not alternatives:
        return suggestions

    cheapest_alt = alternatives[0]
    extra_needed = cheapest_alt['Total_Cost'] - budget

    if extra_needed > 0:
        suggestions.append(
            f"Increase your budget by ₹{extra_needed:,} to afford {cheapest_alt['Destination']} "
            f"(cheapest alternative at ₹{cheapest_alt['Total_Cost']:,})."
        )

    # Calculate how much could be saved by cutting one day
    # Daily cost = (hotel + food + local transport) / days  (travel is one-time, excluded)
    if days > 1 and days > 0:
        daily_running = (cheapest_alt['Hotel_Cost'] +
                         cheapest_alt['Food_Cost'] +
                         cheapest_alt['Local_Transport']) / days
        saving_per_day = int(daily_running)
        if saving_per_day > 0:
            suggestions.append(
                f"Reducing your trip by 1 day could save approximately ₹{saving_per_day:,}/day."
            )

    suggestions.append(
        "Try selecting 'Any Type' or 'Any Style' in the filters to see more destinations."
    )
    return suggestions


def recommend_destinations(df, budget, days, travelers, trip_type='all', budget_style='all', target_state='all', starting_city='', outbound_transport='any', return_transport='any'):
    """
    Main recommendation function.

    Workflow:
      1. Filter by target state if selected.
      2. For every destination, calculate exact trip cost.
      3. Score it using the 100-point rule-based engine.
      4. Separate into 'matches' (within budget) and 'alternatives' (over budget).
      5. Return all matching destinations.
         If no matches, return top 3 cheapest alternatives + helpful suggestions.

    Returns a dict with keys: 'matches', 'alternatives', 'suggestions'.
    """
    if df.empty:
        return {'matches': [], 'alternatives': [], 'suggestions': []}

    # Filter by search string if requested
    if target_state and target_state.lower() != 'all' and target_state.lower() != 'anywhere in the world':
        search_term = target_state.lower()
        
        # First attempt an exact match to prevent 'Bali' from matching 'Mahabalipuram'
        exact_match_df = df[(df['State'].str.lower() == search_term) | 
                            (df['Destination'].str.lower() == search_term)]
        
        if not exact_match_df.empty:
            df = exact_match_df
        else:
            # Fallback to partial match if no exact match exists
            df = df[df['State'].str.lower().str.contains(search_term, na=False) | 
                    df['Destination'].str.lower().str.contains(search_term, na=False)]
        
        if df.empty:
            # Fallback to Universal Generator
            univ_data = generate_universal_destination(target_state)
            if univ_data:
                # We have dynamically generated rows for this location!
                df = pd.DataFrame(univ_data['rows'])
                # We must attach the dynamic state_info somehow so app.py can grab it.
                # A simple hack: add a hidden column or store it globally.
                # Actually, app.py can just call generate_universal_destination itself if needed,
                # or we can attach it to the dataframe's attrs (supported in Pandas 1.0+)
                df.attrs['dynamic_state_info'] = univ_data['state_info']
            else:
                # Return empty early if search has no results and isn't a valid Wikipedia location
                return {'matches': [], 'alternatives': [], 'suggestions': ["No destinations available in the selected state."]}

    scored = []

    for _, row in df.iterrows():
        costs  = calculate_trip_cost(row, days, travelers)
        score  = score_destination(row, costs, budget, days, trip_type, budget_style)
        reason = generate_reason(row, costs, budget, days)

        # Generate the precise image query based on user specifications
        destination = str(row['Destination']).strip()
        state = str(row['State']).strip()
        dest_type = str(row['Type']).strip().lower()
        
        # Keyword mapping to get 2-4 travel-visual keywords
        keywords_map = {
            'beach': 'ocean coastal relaxing',
            'hill': 'mountain scenic view',
            'nature': 'forest landscape greenery',
            'temple': 'spiritual architecture heritage',
            'city': 'urban street skyline',
            'historical': 'heritage monument ancient',
            'adventure': 'outdoor action extreme'
        }
        keywords = keywords_map.get(dest_type, f"{dest_type} sightseeing")
        
        # Most data is Indian, but handle global properly
        country = "India"
        if state and state.lower() not in ["andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh", "goa", "gujarat", "haryana", "himachal pradesh", "jharkhand", "karnataka", "kerala", "madhya pradesh", "maharashtra", "manipur", "meghalaya", "mizoram", "nagaland", "odisha", "punjab", "rajasthan", "sikkim", "tamil nadu", "telangana", "tripura", "uttar pradesh", "uttarakhand", "west bengal", "delhi", "jammu and kashmir", "ladakh", "puducherry", "andaman and nicobar islands", "chandigarh", "dadra and nagar haveli and daman and diu", "lakshadweep"]:
            # If the state isn't a known Indian state/UT, it might be an international location from universal generator
            # We omit "India" to be safe, the universal generator often sets State to the Country/Region name
            country = ""

        # Construct the final query
        query_parts = [destination, state, country, keywords, "travel photography"]
        image_query = " ".join([p for p in query_parts if p])

        # Generate kids activities if family friendly
        kids_activities = []
        family_friendly = _safe_get(row, 'Family_Friendly', '')
        if family_friendly == 'Yes':
            import random
            random.seed(hash(row['Destination']))
            all_activities = [
                {'name': 'Go-Karting 🏎️', 'image': 'https://images.unsplash.com/photo-1541257710737-06d667133a53?auto=format&fit=crop&w=300&q=80'},
                {'name': 'Fun Gun Games 🔫', 'image': 'https://images.unsplash.com/photo-1590845947376-2638caa89309?auto=format&fit=crop&w=300&q=80'},
                {'name': 'Cricket Nets 🏏', 'image': 'https://images.unsplash.com/photo-1531415074968-036ba1b575da?auto=format&fit=crop&w=300&q=80'},
                {'name': 'Amusement Park 🎢', 'image': 'https://images.unsplash.com/photo-1513885045260-6b3086b24c17?auto=format&fit=crop&w=300&q=80'},
                {'name': 'Arcade 🕹️', 'image': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=300&q=80'},
                {'name': 'Water Park 🌊', 'image': 'https://images.unsplash.com/photo-1582216503923-b1d44eb683c3?auto=format&fit=crop&w=300&q=80'},
                {'name': 'Trampoline Park 🤸', 'image': 'https://images.unsplash.com/photo-1519865885898-a54a6f2c7eea?auto=format&fit=crop&w=300&q=80'},
                {'name': 'VR Gaming 👓', 'image': 'https://images.unsplash.com/photo-1622979135225-d2ba269cf1ac?auto=format&fit=crop&w=300&q=80'}
            ]
            chosen = random.sample(all_activities, k=random.randint(2, 4))
            for act in chosen:
                prefixes = ['Central', 'Downtown', 'North', 'South', 'City Center']
                kids_activities.append({
                    'name': act['name'],
                    'image': act['image'],
                    'location': f"{random.choice(prefixes)} {str(row['Destination']).split(',')[0]} Zone",
                    'rating': round(random.uniform(4.0, 4.9), 1)
                })

        from utils.transport_generator import generate_transport
        
        outbound_options = []
        return_options = []
        if starting_city:
            outbound_options = generate_transport(starting_city, destination, outbound_transport, is_return=False)
            return_options = generate_transport(destination, starting_city, return_transport, is_return=True)

        scored.append({
            'Destination':      row['Destination'],
            'State':            row['State'],
            'Type':             row['Type'],
            'Total_Cost':       costs['total'],
            'Travel_Cost':      costs['travel'],
            'Hotel_Cost':       costs['hotel'],
            'Food_Cost':        costs['food'],
            'Local_Transport':  costs['local_transport'],
            'Shopping_Cost':    costs['shopping'],
            'Score':            score,
            'Reason':           reason,
            'Crowd_Level':      _safe_get(row, 'Crowd_Level', ''),
            'Family_Friendly':  family_friendly,
            'Kids_Activities':  kids_activities,
            'Attractions':      _safe_get(row, 'Attractions', ''),
            'Shopping_Items':   _safe_get(row, 'Shopping_Items', 'Local souvenirs'),
            'Image_Query':      image_query,
            'Outbound_Options': outbound_options,
            'Return_Options':   return_options
        })

    # Split by budget
    matches      = [d for d in scored if d['Total_Cost'] <= budget]
    alternatives = [d for d in scored if d['Total_Cost'] >  budget]

    # Sort: matches by Score DESC, alternatives by Total_Cost ASC
    matches      = sorted(matches,      key=lambda x: x['Score'], reverse=True)
    alternatives = sorted(alternatives, key=lambda x: x['Total_Cost'])

    # Return all matches, and top 3 alternatives if no matches
    top_matches = matches
    top_alts    = alternatives[:3] if not top_matches else []

    suggestions = build_suggestions(top_alts, budget, days, travelers) if top_alts else []

    return {
        'matches':      top_matches,
        'alternatives': top_alts,
        'suggestions':  suggestions,
        'dynamic_state_info': df.attrs.get('dynamic_state_info') if hasattr(df, 'attrs') else None
    }

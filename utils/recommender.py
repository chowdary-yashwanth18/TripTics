# ============================================================
# utils/recommender.py  –  TripTics Recommendation Engine
# ============================================================


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

    total_cost = int(travel_cost + hotel_cost + food_cost + local_transport)

    return {
        'total':           total_cost,
        'travel':          int(travel_cost),
        'hotel':           int(hotel_cost),
        'food':            int(food_cost),
        'local_transport': int(local_transport)
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


def recommend_destinations(df, budget, days, travelers, trip_type='all', budget_style='all', target_state='all'):
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

    # Filter by state if requested
    if target_state.lower() != 'all':
        df = df[df['State'].str.lower() == target_state.lower()]
        
        if df.empty:
            # Return empty early if state has no destinations
            return {'matches': [], 'alternatives': [], 'suggestions': ["No destinations available in the selected state."]}

    scored = []

    for _, row in df.iterrows():
        costs  = calculate_trip_cost(row, days, travelers)
        score  = score_destination(row, costs, budget, days, trip_type, budget_style)
        reason = generate_reason(row, costs, budget, days)

        scored.append({
            'Destination':      row['Destination'],
            'State':            row['State'],
            'Type':             row['Type'],
            'Total_Cost':       costs['total'],
            'Travel_Cost':      costs['travel'],
            'Hotel_Cost':       costs['hotel'],
            'Food_Cost':        costs['food'],
            'Local_Transport':  costs['local_transport'],
            'Score':            score,
            'Reason':           reason,
            'Crowd_Level':      _safe_get(row, 'Crowd_Level', ''),
            'Family_Friendly':  _safe_get(row, 'Family_Friendly', ''),
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
        'suggestions':  suggestions
    }

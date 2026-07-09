from flask import Flask, render_template, request, url_for
import os
from utils.data_loader import load_destinations
from utils.recommender import recommend_destinations
from utils.analytics import generate_analytics_charts, get_kpi_metrics, get_key_insights
from utils.state_info import STATE_INFO

app = Flask(__name__)

# ── Load dataset once at startup ─────────────────────────────────────────────
destinations_df = load_destinations()


@app.route('/')
def index():
    """Home page – renders the landing page."""
    return render_template('index.html')


@app.route('/planner', methods=['GET', 'POST'])
def planner():
    """
    GET  → render the trip planner form.
    POST → validate inputs, run recommendation engine, render results.
    """
    if request.method == 'POST':
        states = sorted(destinations_df['State'].unique().tolist())

        # ── Read and sanitize form values ─────────────────────────────────
        try:
            budget    = int(float(request.form.get('budget', 0)))
            days      = int(request.form.get('days', 1))
            travelers = int(request.form.get('travelers', 1))
        except (ValueError, TypeError):
            # If the user somehow bypasses HTML validation, show a friendly error
            return render_template('planner.html',
                                   error="Please enter valid numbers for budget, days, and travelers.",
                                   states=states)

        trip_type    = request.form.get('trip_type', 'all').strip()
        budget_style = request.form.get('budget_style', 'all').strip()
        target_state = request.form.get('target_state', 'all').strip()

        # ── Server-side guard against impossible inputs ───────────────────
        if budget < 500:
            return render_template('planner.html',
                                   error="Budget must be at least ₹500 to get useful recommendations.",
                                   states=states)
        if days < 1 or days > 30:
            return render_template('planner.html',
                                   error="Number of days must be between 1 and 30.",
                                   states=states)
        if travelers < 1 or travelers > 100:
            return render_template('planner.html',
                                   error="Number of travelers must be between 1 and 100.",
                                   states=states)

        # ── Run recommendation engine ─────────────────────────────────────
        recommendation_data = recommend_destinations(
            destinations_df, budget, days, travelers, trip_type, budget_style, target_state
        )

        # ── State Information ─────────────────────────────────────────────
        # Get the actual state/country from the top result to handle city searches
        actual_state = None
        if target_state and target_state.lower() not in ['all', 'anywhere in the world']:
            if recommendation_data['matches']:
                actual_state = recommendation_data['matches'][0]['State']
            elif recommendation_data['alternatives']:
                actual_state = recommendation_data['alternatives'][0]['State']
                
        # If the recommendation engine dynamically generated this location, use its dynamic state info!
        if recommendation_data.get('dynamic_state_info'):
            state_info = recommendation_data['dynamic_state_info']
        else:
            state_info = STATE_INFO.get(actual_state) if actual_state else None

        return render_template('results.html',
                               recommendations=recommendation_data['matches'],
                               alternatives=recommendation_data['alternatives'],
                               suggestions=recommendation_data['suggestions'],
                               budget=budget,
                               days=days,
                               travelers=travelers,
                               state_info=state_info,
                               trip_type=trip_type)

    states = sorted(destinations_df['State'].unique().tolist())
    destinations = sorted(destinations_df['Destination'].unique().tolist())
    all_locations = sorted(list(set(states + destinations)))
    return render_template('planner.html', error=None, locations=all_locations)


@app.route('/dashboard')
def dashboard():
    """Analytics dashboard – generates charts, KPI cards, and key insights."""
    charts   = generate_analytics_charts(destinations_df)
    kpis     = get_kpi_metrics(destinations_df)
    insights = get_key_insights(destinations_df)
    return render_template('dashboard.html', charts=charts, kpis=kpis, insights=insights)


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, url_for
import os
from utils.data_loader import load_destinations
from utils.recommender import recommend_destinations
from utils.analytics import generate_analytics_charts, get_kpi_metrics, get_key_insights
from utils.state_info import STATE_INFO
from utils.state_districts import STATE_DISTRICTS
from utils.hotel_generator import generate_hotels
from utils.currency import get_currency_info

app = Flask(__name__)

# Register generate_hotels for use inside Jinja templates
app.jinja_env.globals.update(generate_hotels=generate_hotels)

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
                                   states=states, state_districts=STATE_DISTRICTS)

        trip_type    = request.form.get('trip_type', 'all').strip()
        budget_style = request.form.get('budget_style', 'all').strip()
        target_state = request.form.get('target_state', 'all').strip()
        starting_city = request.form.get('starting_city', '').strip()
        outbound_transport = request.form.get('outbound_transport', 'any').strip()
        return_transport = request.form.get('return_transport', 'any').strip()

        # ── Server-side guard against impossible inputs ───────────────────
        if budget < 500:
            return render_template('planner.html',
                                   error="Budget must be at least ₹500 to get useful recommendations.",
                                   states=states, state_districts=STATE_DISTRICTS)
        if days < 1 or days > 30:
            return render_template('planner.html',
                                   error="Number of days must be between 1 and 30.",
                                   states=states, state_districts=STATE_DISTRICTS)
        if travelers < 1 or travelers > 100:
            return render_template('planner.html',
                                   error="Number of travelers must be between 1 and 100.",
                                   states=states, state_districts=STATE_DISTRICTS)

        # ── Run recommendation engine ─────────────────────────────────────
        recommendation_data = recommend_destinations(
            destinations_df, budget, days, travelers, trip_type, budget_style, target_state, starting_city, outbound_transport, return_transport
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
        elif target_state and target_state.lower() not in ['all', 'anywhere in the world']:
            # Check if user searched for a State
            if any(target_state.lower() == s.lower() for s in STATE_INFO.keys()):
                state_info = next((v for k, v in STATE_INFO.items() if k.lower() == target_state.lower()), None)
            else:
                # It's a city search! Fetch specific info and image for the city using universal generator.
                from utils.universal_generator import generate_universal_destination
                univ_data = generate_universal_destination(target_state)
                if univ_data and univ_data.get('state_info'):
                    state_info = univ_data['state_info']
                    # Overwrite the title to be exact city name
                    state_info['title'] = f"Discover {target_state.title()}"
                    # Use actual attractions from DB if available!
                    if recommendation_data['matches']:
                        att = recommendation_data['matches'][0].get('Attractions')
                        if att:
                            state_info['must_visit'] = [a.strip() for a in att.split(',') if a.strip()]
                else:
                    # Fallback to state info if city fetch fails, BUT customize it for the city!
                    base_state_info = STATE_INFO.get(actual_state)
                    if base_state_info:
                        state_info = base_state_info.copy()
                        state_info['title'] = f"Explore {target_state.title()}"
                        state_info['description'] = f"Discover the unique culture, heritage, and scenic beauty of {target_state.title()}, a wonderful destination located in {actual_state}."
                        state_info['must_visit'] = [f"{target_state.title()} City Center", f"Local Markets of {target_state.title()}", f"Historic Sites of {target_state.title()}"]
                        # Try to get an image for the city at least!
                        from utils.image_fetcher import fetch_image
                        img_url = fetch_image(f"{target_state} {actual_state}")
                        if img_url:
                            state_info['image_url'] = img_url
                            
                        # Use actual attractions from DB if available!
                        if recommendation_data['matches']:
                            att = recommendation_data['matches'][0].get('Attractions')
                            if att:
                                state_info['must_visit'] = [a.strip() for a in att.split(',') if a.strip()]
                    else:
                        state_info = None
        else:
            state_info = STATE_INFO.get(actual_state) if actual_state else None
            
        display_location = target_state if target_state and target_state.lower() not in ['all', 'anywhere in the world'] else actual_state

        return render_template('results.html',
                               recommendations=recommendation_data['matches'],
                               alternatives=recommendation_data['alternatives'],
                               suggestions=recommendation_data['suggestions'],
                               budget=budget,
                               days=days,
                               travelers=travelers,
                               state_info=state_info,
                               trip_type=trip_type,
                               target_location=display_location,
                               starting_city=starting_city,
                               currency_info=get_currency_info(actual_state))

    states = sorted(destinations_df['State'].unique().tolist())
    destinations = sorted(destinations_df['Destination'].unique().tolist())
    all_locations = sorted(list(set(states + destinations)))
    return render_template('planner.html', error=None, locations=all_locations, states_list=states, state_districts=STATE_DISTRICTS)


@app.route('/dashboard')
def dashboard():
    """Analytics dashboard – generates charts, KPI cards, and key insights."""
    charts   = generate_analytics_charts(destinations_df)
    kpis     = get_kpi_metrics(destinations_df)
    insights = get_key_insights(destinations_df)
    return render_template('dashboard.html', charts=charts, kpis=kpis, insights=insights)


@app.route('/hotels', methods=['GET', 'POST'])
def hotels():
    """Route to search and recommend hotels for a specific location."""
    if request.method == 'POST':
        location = request.form.get('location', '').strip()
        if not location:
            return render_template('hotels.html', error="Please enter a valid location.")
        
        hotel_results = generate_hotels(location)
        return render_template('hotels.html', location=location.title(), hotels=hotel_results)
        
    return render_template('hotels.html', location=None, hotels=None)


@app.route('/api/image')
def api_image():
    """Internal API to reliably fetch a single high-resolution image URL."""
    from utils.image_fetcher import fetch_image
    query = request.args.get('q', '')
    if not query:
        return {'url': ''}, 400
        
    img_url = fetch_image(query)
    if img_url:
        return {'url': img_url}
        
    return {'url': ''}, 404

if __name__ == '__main__':
    app.run(debug=True)

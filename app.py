from flask import Flask, render_template, request, url_for, flash, redirect
import os
from datetime import date, datetime
from utils.data_loader import load_destinations
from utils.recommender import recommend_destinations
from utils.analytics import generate_analytics_charts, get_kpi_metrics, get_key_insights
from utils.state_info import STATE_INFO
from utils.state_districts import STATE_DISTRICTS
from utils.hotel_generator import generate_hotels
from utils.currency import get_currency_info

app = Flask(__name__)
app.secret_key = 'triptics_secret_key_123'

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
        destinations = sorted(destinations_df['Destination'].unique().tolist())
        all_locations = sorted(list(set(states + destinations)))

        # ── Read and sanitize form values ─────────────────────────────────
        try:
            raw_budget    = int(float(request.form.get('budget', 0)))
            days      = int(request.form.get('days', 1))
            travelers = int(request.form.get('travelers', 1))
        except (ValueError, TypeError):
            return render_template('planner.html',
                                   error="Please enter valid numbers for budget, days, and travelers.",
                                   locations=all_locations, states_list=states, state_districts=STATE_DISTRICTS)

        budget_currency = request.form.get('budget_currency', 'INR').strip()
        from utils.currency import get_rate_for_currency
        rate = get_rate_for_currency(budget_currency)
        budget = int(raw_budget / rate) # Convert input budget to INR for the engine

        trip_type    = 'all'
        budget_style = 'all'
        target_state = request.form.get('target_state', 'all').strip()
        starting_city = request.form.get('starting_city', '').strip()
        travel_date = request.form.get('travel_date', '').strip()
        outbound_transport = (request.form.get('outbound_transport') or 'any').strip() or 'any'
        return_transport = (request.form.get('return_transport') or 'any').strip() or 'any'

        # ── Server-side guard against impossible inputs ───────────────────
        if budget < 500:
            return render_template('planner.html',
                                   error="Converted budget must be at least ₹500 to get useful recommendations.",
                                   locations=all_locations, states_list=states, state_districts=STATE_DISTRICTS)
        if days < 1 or days > 30:
            return render_template('planner.html',
                                   error="Number of days must be between 1 and 30.",
                                   locations=all_locations, states_list=states, state_districts=STATE_DISTRICTS)
        if travelers < 1 or travelers > 100:
            return render_template('planner.html',
                                   error="Number of travelers must be between 1 and 100.",
                                   locations=all_locations, states_list=states, state_districts=STATE_DISTRICTS)

        # ── Run recommendation engine ─────────────────────────────────────
        recommendation_data = recommend_destinations(
            destinations_df, budget, days, travelers, trip_type, budget_style, target_state, starting_city, outbound_transport, return_transport, travel_date=travel_date
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
                            from utils.universal_generator import categorize_places
                            state_info['must_visit'] = categorize_places([a.strip() for a in att.split(',') if a.strip()])
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
                        img_urls = fetch_image(f"{target_state} {actual_state}")
                        if img_urls:
                            state_info['image_url'] = img_urls[0] if isinstance(img_urls, list) else img_urls
                            
                        # Use actual attractions from DB if available!
                        if recommendation_data['matches']:
                            att = recommendation_data['matches'][0].get('Attractions')
                            if att:
                                from utils.universal_generator import categorize_places
                                state_info['must_visit'] = categorize_places([a.strip() for a in att.split(',') if a.strip()])
                    else:
                        state_info = None
        else:
            state_info = STATE_INFO.get(actual_state) if actual_state else None
            
        display_location = target_state if target_state and target_state.lower() not in ['all', 'anywhere in the world'] else actual_state

        # ── Attach Destination Master Guide (Route map, all categorized spots, stays, dishes, culture, celebrations, ATMs) ──
        from utils.destination_guide import get_destination_master_guide
        for rec in recommendation_data.get('matches', []):
            rec['master_guide'] = get_destination_master_guide(rec.get('Destination', ''), rec.get('State', ''), days)
            rec['atms'] = rec['master_guide'].get('atms', {})
        for rec in recommendation_data.get('alternatives', []):
            rec['master_guide'] = get_destination_master_guide(rec.get('Destination', ''), rec.get('State', ''), days)
            rec['atms'] = rec['master_guide'].get('atms', {})

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
                               travel_date=travel_date,
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
    location = request.form.get('location', '').strip() if request.method == 'POST' else request.args.get('location', '').strip()
    
    if location:
        hotel_results = generate_hotels(location)
        from utils.currency import get_currency_info
        from utils.hotel_apps import get_country_hotel_info
        currency_info = get_currency_info(location)
        country_info = get_country_hotel_info(location)
        return render_template('hotels.html', location=location.title(), hotels=hotel_results, currency_info=currency_info, country_info=country_info)
        
    if request.method == 'POST' and not location:
        return render_template('hotels.html', error="Please enter a valid location.")
        
    return render_template('hotels.html', location=None, hotels=None)


@app.route('/api/image')
def api_image():
    """Fetches an image URL from Wikimedia/Wikipedia based on a search query."""
    from utils.image_fetcher import fetch_image
    query = request.args.get('q')
    if not query:
        return {'urls': []}, 400
        
    img_urls = fetch_image(query)
    if img_urls:
        if isinstance(img_urls, str):
            img_urls = [img_urls]
        return {'urls': img_urls}
        
    return {'urls': []}, 404

@app.route('/book')
def book():
    """Route to show the booking page for hotels and travel."""
    item_type = request.args.get('type', 'Unknown')
    item_name = request.args.get('name', 'Unknown')
    price = request.args.get('price', '0')
    location = request.args.get('location', '')
    return render_template('booking.html', item_type=item_type, item_name=item_name, price=price, location=location)


@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    """Endpoint to process booking confirmation."""
    item_name = request.form.get('item_name', '')
    flash(f'Successfully booked {item_name}! Check your email for confirmation.', 'success')
    return redirect(url_for('index'))

@app.route('/api/attractions')
def api_attractions():
    """Fetches real-world attractions using Google Places API."""
    from utils.places_api import get_tourist_attractions
    location = request.args.get('location', '')
    if not location:
        return {'attractions': [], 'error': 'No location provided'}, 400
        
    attractions, diagnostics = get_tourist_attractions(location, limit=20)
    if diagnostics.get('error'):
        app.logger.error(f"Google Places API Error for {location}: {diagnostics['error']}")
    return {'attractions': attractions, 'diagnostics': diagnostics}

@app.route('/api/photo')
def api_photo():
    """Proxies the Google Places Photo API to bypass frontend CORS and API restrictions."""
    import urllib.request
    from flask import Response
    from utils.places_api import get_google_api_key
    
    photo_reference = request.args.get('photoreference')
    max_width = request.args.get('maxwidth', '400')
    api_key = get_google_api_key()
    
    if not photo_reference or not api_key:
        return "Missing parameters", 400
        
    url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={max_width}&photoreference={photo_reference}&key={api_key}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'TripTics Backend'})
        resp = urllib.request.urlopen(req, timeout=10)
        # Read the binary image data and stream it back
        image_data = resp.read()
        return Response(image_data, mimetype=resp.headers.get('Content-Type', 'image/jpeg'))
    except Exception as e:
        app.logger.error(f"Failed to proxy photo: {str(e)}")
        return "Error fetching photo", 500


@app.route('/api/rides')
def api_rides():
    """Generates localized ride options and distance-based prices for a location."""
    from utils.rides import generate_ride_options
    location = request.args.get('location', '')
    pickup = request.args.get('pickup', 'Current Location / Hotel')
    dropoff = request.args.get('dropoff', '')
    distance_km = request.args.get('distance_km', None)
    
    if not location:
        return {'rides': [], 'error': 'No location provided'}, 400
    
    result = generate_ride_options(location, pickup=pickup, dropoff=dropoff, distance_km=distance_km)
    return result


@app.route('/api/weather')
def api_weather():
    """Fetches genuine weather forecast or historical seasonal climate normals."""
    from utils.weather_service import get_weather_forecast
    location = request.args.get('location', '').strip()
    target_date = request.args.get('date', '').strip()
    if not location:
        return {'error': 'Location is required'}, 400
    res = get_weather_forecast(location, target_date_str=target_date)
    return res


@app.route('/api/currency')
def api_currency():
    """Returns verified ISO 4217 exchange rates and provenance timestamp."""
    from utils.currency import get_all_exchange_rates, CURRENCY_REGISTRY
    rates, timestamp, is_live = get_all_exchange_rates()
    return {
        'base': 'INR',
        'rates': rates,
        'currencies': CURRENCY_REGISTRY,
        'timestamp': timestamp,
        'is_live': is_live
    }


@app.route('/api/atms')
def api_atms():
    """Returns nearby ATMs for railway stations, bus stands, and airports."""
    from utils.atm_service import get_nearby_atms
    dest = request.args.get('location', '').strip()
    state = request.args.get('state', '').strip()
    return get_nearby_atms(dest, state)


@app.route('/api/destination-guide')
def api_destination_guide():
    """Returns complete destination master guide, route map, spots, dishes, culture, and celebration venues."""
    from utils.destination_guide import get_destination_master_guide
    dest = request.args.get('location', '').strip()
    state = request.args.get('state', '').strip()
    days = int(request.args.get('days', 3) or 3)
    return get_destination_master_guide(dest, state, days)


@app.route('/api/chatbot', methods=['POST'])
def api_chatbot():
    """
    AI Travel Concierge & Day Planner API.
    Helps tourists plan their day, order of visiting sights, chill spots, and party/celebration venues.
    """
    data = request.get_json(silent=True) or request.form
    user_message = data.get('message', '').strip()
    destination = data.get('destination', '').strip()
    days = int(data.get('days', 1) or 1)
    travelers = int(data.get('travelers', 1) or 1)
    budget = int(data.get('budget', 0) or 0)
    history = data.get('history', [])
    
    if not user_message:
        return {'reply': 'Please type a question to get travel assistance!', 'suggestions': []}, 400
        
    from utils.ai_chatbot import get_ai_chat_response
    response = get_ai_chat_response(
        user_message=user_message,
        destination=destination,
        days=days,
        travelers=travelers,
        budget=budget,
        history=history
    )
    return response


# ==============================================================================
# DOOR-TO-DOOR TRIP DIARY & TRAVEL EXPENSE MANAGER ROUTES
# ==============================================================================
@app.route('/trip-diary')
def trip_diary():
    """Door-to-door trip diary and real-time travel expense tracker page."""
    from utils.trip_tracker import get_all_trips, get_trip_details
    trip_id = request.args.get('trip_id', '').strip()
    all_trips = get_all_trips()
    
    if not trip_id and all_trips:
        trip_id = all_trips[0]['id']
        
    details = get_trip_details(trip_id) if trip_id else None
    today_date = date.today().isoformat()
    
    return render_template('trip_diary.html', all_trips=all_trips, details=details, today_date=today_date)


@app.route('/trip-diary/create', methods=['POST'])
def trip_create():
    """Create a new trip timeline."""
    from utils.trip_tracker import create_or_update_trip
    dest = request.form.get('destination', '').strip()
    origin = request.form.get('origin', '').strip()
    start_date = request.form.get('start_date', '').strip()
    end_date = request.form.get('end_date', '').strip()
    travelers = int(request.form.get('travelers', 1) or 1)
    notes = request.form.get('notes', '').strip()
    
    if not dest or not start_date or not end_date:
        flash('Please provide Destination and Travel Dates.', 'warning')
        return redirect(url_for('trip_diary'))
        
    new_id = create_or_update_trip(dest, start_date, end_date, origin=origin, travelers=travelers, notes=notes)
    flash(f'Trip diary started for {dest}! Add pre-booked stays or start logging live expenses.', 'success')
    return redirect(url_for('trip_diary', trip_id=new_id))


@app.route('/trip-diary/add-expense', methods=['POST'])
def trip_add_expense():
    """Add a pre-booked or live in-transit expense."""
    from utils.trip_tracker import add_expense
    trip_id = request.form.get('trip_id', '').strip()
    title = request.form.get('title', '').strip()
    amount = float(request.form.get('amount', 0) or 0)
    category = request.form.get('category', 'misc').strip()
    is_prebooked = request.form.get('is_prebooked', 'false').lower() in ['true', '1', 'yes']
    payment_mode = request.form.get('payment_mode', 'UPI / PhonePe').strip()
    notes = request.form.get('notes', '').strip()
    
    if not trip_id or not title or amount <= 0:
        flash('Please enter a valid expense title and amount.', 'warning')
        return redirect(url_for('trip_diary', trip_id=trip_id))
        
    add_expense(trip_id, title, amount, category=category, is_prebooked=is_prebooked, payment_mode=payment_mode, notes=notes)
    flash(f'Added ₹{amount:.2f} for "{title}" to your trip diary!', 'success')
    return redirect(url_for('trip_diary', trip_id=trip_id))


@app.route('/trip-diary/delete-expense', methods=['POST'])
def trip_delete_expense():
    """Remove an expense entry."""
    from utils.trip_tracker import delete_expense
    exp_id = request.form.get('expense_id', '').strip()
    trip_id = request.form.get('trip_id', '').strip()
    if exp_id:
        delete_expense(exp_id)
        flash('Expense removed from diary.', 'info')
    return redirect(url_for('trip_diary', trip_id=trip_id))


@app.route('/api/trip-diary/parse-sms', methods=['POST'])
def trip_parse_sms():
    """API endpoint to parse PhonePe / UPI / Bank SMS text."""
    from utils.trip_tracker import parse_upi_sms_or_text
    data = request.get_json(silent=True) or request.form
    raw_sms = data.get('sms', '').strip()
    if not raw_sms:
        return {'error': 'No SMS text provided'}, 400
    parsed = parse_upi_sms_or_text(raw_sms)
    return parsed or {'error': 'Could not parse transaction SMS'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

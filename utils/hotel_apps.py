# utils/hotel_apps.py
"""
Country-Specific Hotel Booking & Accommodation Finder Apps Directory.
Provides accurate mappings between countries/regions and their leading local & regional 
hotel booking applications (e.g., MakeMyTrip & Goibibo for India, Rakuten Travel & Jalan for Japan, 
Traveloka & Agoda for Southeast Asia, Expedia & Hotels.com for North America, etc.)
along with rich facilities metadata and pre-filled search URLs.
"""

import urllib.parse
import re

# ── 1. Facilities Catalog with Semantic Bootstrap Icons & Badges ──────────────
FACILITY_CATALOG = {
    'Free WiFi': {
        'name': 'Free High-Speed WiFi',
        'icon': 'bi-wifi',
        'badge_class': 'bg-primary-subtle text-primary border border-primary-subtle',
        'desc': 'Complimentary high-speed wireless internet in all rooms and public areas'
    },
    'Breakfast Included': {
        'name': 'Breakfast Included',
        'icon': 'bi-cup-hot-fill',
        'badge_class': 'bg-warning-subtle text-warning-emphasis border border-warning-subtle',
        'desc': 'Daily gourmet buffet breakfast included with your stay'
    },
    'Swimming Pool': {
        'name': 'Swimming Pool',
        'icon': 'bi-water',
        'badge_class': 'bg-info-subtle text-info-emphasis border border-info-subtle',
        'desc': 'Outdoor / heated swimming pool with sun loungers'
    },
    'AC': {
        'name': 'Climate Control / AC',
        'icon': 'bi-snow',
        'badge_class': 'bg-primary-subtle text-primary-emphasis border border-primary-subtle',
        'desc': 'Individual climate control and air conditioning'
    },
    'Gym': {
        'name': 'Fitness Gym',
        'icon': 'bi-heart-pulse-fill',
        'badge_class': 'bg-danger-subtle text-danger border border-danger-subtle',
        'desc': 'Well-equipped gym with cardio & strength machines'
    },
    'Spa': {
        'name': 'Luxury Spa & Wellness',
        'icon': 'bi-flower1',
        'badge_class': 'bg-purple-subtle text-purple border',
        'desc': 'Full-service wellness spa, sauna, and massage therapies'
    },
    'Restaurant': {
        'name': 'Multi-Cuisine Restaurant',
        'icon': 'bi-egg-fried',
        'badge_class': 'bg-success-subtle text-success border border-success-subtle',
        'desc': 'In-house restaurant offering local delicacies and international cuisine'
    },
    'Parking': {
        'name': 'Free Valet Parking',
        'icon': 'bi-p-circle-fill',
        'badge_class': 'bg-light text-dark border',
        'desc': 'Secure, complimentary on-site parking and valet service'
    },
    'Room Service': {
        'name': '24/7 Room Service',
        'icon': 'bi-bell-fill',
        'badge_class': 'bg-warning-subtle text-dark border border-warning-subtle',
        'desc': 'Round-the-clock in-room dining and concierge assistance'
    },
    'Airport Shuttle': {
        'name': 'Airport Shuttle Service',
        'icon': 'bi-car-front-fill',
        'badge_class': 'bg-secondary-subtle text-secondary-emphasis border border-secondary-subtle',
        'desc': 'Dedicated airport pick-up and drop-off transfers'
    },
    'Scenic View': {
        'name': 'Scenic View Balcony',
        'icon': 'bi-image-fill',
        'badge_class': 'bg-success-subtle text-success border border-success-subtle',
        'desc': 'Private balcony with scenic panoramic mountain, sea, or skyline views'
    },
    'Bar & Lounge': {
        'name': 'Cocktail Bar & Lounge',
        'icon': 'bi-cup-straw',
        'badge_class': 'bg-danger-subtle text-danger border border-danger-subtle',
        'desc': 'Stylish lounge and cocktail bar for evening drinks'
    },
    'Power Backup': {
        'name': '24/7 Power Backup',
        'icon': 'bi-lightning-charge-fill',
        'badge_class': 'bg-warning-subtle text-dark border border-warning-subtle',
        'desc': 'Full generator backup ensuring uninterrupted electricity'
    },
    'Pet Friendly': {
        'name': 'Pet Friendly',
        'icon': 'bi-emoji-smile-fill',
        'badge_class': 'bg-success-subtle text-success border border-success-subtle',
        'desc': 'Welcomes pets with dedicated pet beds and walking areas'
    }
}


# ── 2. Country & Region Specific Hotel Booking Applications ───────────────────
COUNTRY_HOTEL_APPS_DATABASE = {
    'india': {
        'country_name': 'India',
        'flag': '🇮🇳',
        'currency_code': 'INR',
        'primary_app': 'MakeMyTrip',
        'description': "For traveling in India, MakeMyTrip and Goibibo are the top local market leaders offering exclusive domestic deals, couple-friendly filters, and instant room confirmation.",
        'apps': [
            {
                'id': 'makemytrip',
                'name': 'MakeMyTrip',
                'badge': "India's #1 Travel App",
                'tagline': "Largest selection of Indian hotels, resorts & homestays",
                'color': '#eb2026',
                'bg_gradient': 'linear-gradient(135deg, #eb2026 0%, #ff5252 100%)',
                'icon_class': 'bi-building-fill-check',
                'is_primary': True,
                'search_hotel': lambda hotel, loc: f"https://www.makemytrip.com/hotels/hotel-listing/?city={urllib.parse.quote(loc)}&searchText={urllib.parse.quote(hotel)}",
                'search_city': lambda loc: f"https://www.makemytrip.com/hotels/hotel-listing/?city={urllib.parse.quote(loc)}"
            },
            {
                'id': 'goibibo',
                'name': 'Goibibo',
                'badge': "Top Budget & Flash Deals",
                'tagline': "goCash discounts, verified reviews & couple-friendly stays",
                'color': '#ff6d00',
                'bg_gradient': 'linear-gradient(135deg, #ff6d00 0%, #ffa000 100%)',
                'icon_class': 'bi-tags-fill',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.goibibo.com/hotels/find-hotels-in-{urllib.parse.quote(loc.lower().replace(' ', '-'))}/?searchQuery={urllib.parse.quote(hotel)}",
                'search_city': lambda loc: f"https://www.goibibo.com/hotels/find-hotels-in-{urllib.parse.quote(loc.lower().replace(' ', '-'))}/"
            },
            {
                'id': 'oyorooms',
                'name': 'OYO Rooms',
                'badge': "Pocket-Friendly Stays",
                'tagline': "Sanitized, budget-friendly hotels & Townhouses across India",
                'color': '#ee2a24',
                'bg_gradient': 'linear-gradient(135deg, #d32f2f 0%, #ee2a24 100%)',
                'icon_class': 'bi-house-heart-fill',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.oyorooms.com/search?location={urllib.parse.quote(loc)}&searchType=city",
                'search_city': lambda loc: f"https://www.oyorooms.com/search?location={urllib.parse.quote(loc)}&searchType=city"
            },
            {
                'id': 'cleartrip',
                'name': 'Cleartrip',
                'badge': "Zero Hidden Charges",
                'tagline': "Simple, transparent pricing with Flipkart travel rewards",
                'color': '#3366cc',
                'bg_gradient': 'linear-gradient(135deg, #1e88e5 0%, #1565c0 100%)',
                'icon_class': 'bi-shield-check',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.cleartrip.com/hotels/results?city={urllib.parse.quote(loc)}&q={urllib.parse.quote(hotel)}",
                'search_city': lambda loc: f"https://www.cleartrip.com/hotels/results?city={urllib.parse.quote(loc)}"
            },
            {
                'id': 'booking_in',
                'name': 'Booking.com India',
                'badge': "Free Cancellation",
                'tagline': "Top international luxury and boutique properties in India",
                'color': '#003580',
                'bg_gradient': 'linear-gradient(135deg, #003580 0%, #0056b3 100%)',
                'icon_class': 'bi-globe-americas',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.booking.com/searchresults.html?ss={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.booking.com/searchresults.html?ss={urllib.parse.quote(loc)}"
            }
        ]
    },
    'japan': {
        'country_name': 'Japan',
        'flag': '🇯🇵',
        'currency_code': 'JPY',
        'primary_app': 'Rakuten Travel',
        'description': "In Japan, domestic platforms Rakuten Travel (楽天トラベル) and Jalan (じゃらん) are unmatched for authentic Japanese Ryokans, Onsen hot-spring retreats, and modern business hotels.",
        'apps': [
            {
                'id': 'rakuten',
                'name': 'Rakuten Travel (楽天トラベル)',
                'badge': "Japan's #1 Hotel App",
                'tagline': "Leading Japanese platform for hotels, onsens & ryokans with Rakuten points",
                'color': '#bf0000',
                'bg_gradient': 'linear-gradient(135deg, #bf0000 0%, #e60000 100%)',
                'icon_class': 'bi-star-fill',
                'is_primary': True,
                'search_hotel': lambda hotel, loc: f"https://travel.rakuten.com/search/?query={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://travel.rakuten.com/search/?query={urllib.parse.quote(loc)}"
            },
            {
                'id': 'jalan',
                'name': 'Jalan (じゃらん)',
                'badge': "Top Ryokan & Onsen Finder",
                'tagline': "Japan's favorite portal for traditional hot-spring ryokan retreats",
                'color': '#ff7a00',
                'bg_gradient': 'linear-gradient(135deg, #ff7a00 0%, #ff9800 100%)',
                'icon_class': 'bi-flower1',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.jalan.net/en/japan_hotels_ryokan/?keyword={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.jalan.net/en/japan_hotels_ryokan/?keyword={urllib.parse.quote(loc)}"
            },
            {
                'id': 'agoda_jp',
                'name': 'Agoda Japan',
                'badge': "Deep Discounts in Japan",
                'tagline': "Most popular app for international travelers visiting Tokyo, Kyoto & Osaka",
                'color': '#2a64c5',
                'bg_gradient': 'linear-gradient(135deg, #2a64c5 0%, #4a90e2 100%)',
                'icon_class': 'bi-percent',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.agoda.com/search?text={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.agoda.com/search?text={urllib.parse.quote(loc)}"
            },
            {
                'id': 'booking_jp',
                'name': 'Booking.com Japan',
                'badge': "English-Friendly Stays",
                'tagline': "Instant confirmation, multi-currency pricing & central city stays",
                'color': '#003580',
                'bg_gradient': 'linear-gradient(135deg, #003580 0%, #0056b3 100%)',
                'icon_class': 'bi-building-fill',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.booking.com/searchresults.html?ss={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.booking.com/searchresults.html?ss={urllib.parse.quote(loc)}"
            },
            {
                'id': 'google_hotels_jp',
                'name': 'Google Hotels Japan',
                'badge': "Price Comparison",
                'tagline': "Compare live rates across all Japanese booking agents",
                'color': '#4285f4',
                'bg_gradient': 'linear-gradient(135deg, #4285f4 0%, #34a853 100%)',
                'icon_class': 'bi-google',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.google.com/travel/hotels?q={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.google.com/travel/hotels?q={urllib.parse.quote(loc)}"
            }
        ]
    },
    'southeast_asia': {
        'country_name': 'Southeast Asia (Thailand, Indonesia, Singapore, Malaysia)',
        'flag': '🏝️',
        'currency_code': 'USD',
        'primary_app': 'Agoda',
        'description': "Across Southeast Asia (Thailand, Indonesia/Bali, Singapore, Vietnam, Malaysia), Agoda and Traveloka dominate the market with local flash deals and exclusive resort discounts.",
        'apps': [
            {
                'id': 'agoda',
                'name': 'Agoda',
                'badge': "Southeast Asia's #1 Hotel App",
                'tagline': "Exclusive VIP discounts, beach villas, and resort promos",
                'color': '#2a64c5',
                'bg_gradient': 'linear-gradient(135deg, #2a64c5 0%, #4a90e2 100%)',
                'icon_class': 'bi-percent',
                'is_primary': True,
                'search_hotel': lambda hotel, loc: f"https://www.agoda.com/search?text={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.agoda.com/search?text={urllib.parse.quote(loc)}"
            },
            {
                'id': 'traveloka',
                'name': 'Traveloka',
                'badge': "Southeast Asia's Superapp",
                'tagline': "Leading regional app for luxury villas, boutique hotels & experiences",
                'color': '#1ba0e2',
                'bg_gradient': 'linear-gradient(135deg, #1ba0e2 0%, #0077b6 100%)',
                'icon_class': 'bi-send-fill',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.traveloka.com/en-en/hotel/search?spec={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.traveloka.com/en-en/hotel/search?spec={urllib.parse.quote(loc)}"
            },
            {
                'id': 'tiket',
                'name': 'Tiket.com',
                'badge': "Villas & Island Resorts",
                'tagline': "Favorite holiday & staycation booking app across Bali & ASEAN",
                'color': '#fbc02d',
                'bg_gradient': 'linear-gradient(135deg, #fbc02d 0%, #f57f17 100%)',
                'icon_class': 'bi-ticket-perforated-fill',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.tiket.com/hotel/search?q={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.tiket.com/hotel/search?q={urllib.parse.quote(loc)}"
            },
            {
                'id': 'booking_sea',
                'name': 'Booking.com',
                'badge': "Global Traveler Favorite",
                'tagline': "Verified guest reviews and flexible cancel-anytime reservations",
                'color': '#003580',
                'bg_gradient': 'linear-gradient(135deg, #003580 0%, #0056b3 100%)',
                'icon_class': 'bi-globe-americas',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.booking.com/searchresults.html?ss={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.booking.com/searchresults.html?ss={urllib.parse.quote(loc)}"
            }
        ]
    },
    'usa_canada': {
        'country_name': 'USA & North America',
        'flag': '🇺🇸',
        'currency_code': 'USD',
        'primary_app': 'Expedia',
        'description': "In the United States and Canada, Expedia and Hotels.com lead the market for hotel rooms, casino resorts in Las Vegas, city boutique hotels, and national park lodges.",
        'apps': [
            {
                'id': 'expedia',
                'name': 'Expedia',
                'badge': "North America's Leading App",
                'tagline': "Expedia Rewards, flight-hotel bundle savings, and VIP stays",
                'color': '#00355f',
                'bg_gradient': 'linear-gradient(135deg, #00355f 0%, #0056b3 100%)',
                'icon_class': 'bi-airplane-engines-fill',
                'is_primary': True,
                'search_hotel': lambda hotel, loc: f"https://www.expedia.com/Hotel-Search?destination={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.expedia.com/Hotel-Search?destination={urllib.parse.quote(loc)}"
            },
            {
                'id': 'hotels_com',
                'name': 'Hotels.com',
                'badge': "One Key™ Rewards",
                'tagline': "Collect OneKeyCash and unlock secret member prices",
                'color': '#d32f2f',
                'bg_gradient': 'linear-gradient(135deg, #d32f2f 0%, #ff5252 100%)',
                'icon_class': 'bi-key-fill',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.hotels.com/Hotel-Search?destination={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.hotels.com/Hotel-Search?destination={urllib.parse.quote(loc)}"
            },
            {
                'id': 'booking_us',
                'name': 'Booking.com US',
                'badge': "Instant Booking",
                'tagline': "Extensive selection from Manhattan penthouses to roadside motels",
                'color': '#003580',
                'bg_gradient': 'linear-gradient(135deg, #003580 0%, #0056b3 100%)',
                'icon_class': 'bi-building-fill',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.booking.com/searchresults.html?ss={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.booking.com/searchresults.html?ss={urllib.parse.quote(loc)}"
            },
            {
                'id': 'priceline',
                'name': 'Priceline',
                'badge': "VIP Express Deals",
                'tagline': "Exclusive flash discounts on 4-star and 5-star American stays",
                'color': '#0066cc',
                'bg_gradient': 'linear-gradient(135deg, #0066cc 0%, #0099ff 100%)',
                'icon_class': 'bi-lightning-fill',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.priceline.com/hotel-deals/?q={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.priceline.com/hotel-deals/?q={urllib.parse.quote(loc)}"
            }
        ]
    },
    'europe_uk': {
        'country_name': 'Europe & United Kingdom',
        'flag': '🇪🇺',
        'currency_code': 'EUR',
        'primary_app': 'Booking.com',
        'description': "Across the UK and Europe, Booking.com and Trivago are the gold standard for historic city-centre hotels, Swiss chalets, French châteaux, and Italian coastal villas.",
        'apps': [
            {
                'id': 'booking_eu',
                'name': 'Booking.com',
                'badge': "Europe's #1 Accommodation Portal",
                'tagline': "The benchmark booking platform across all 27 European countries & UK",
                'color': '#003580',
                'bg_gradient': 'linear-gradient(135deg, #003580 0%, #0056b3 100%)',
                'icon_class': 'bi-globe-americas',
                'is_primary': True,
                'search_hotel': lambda hotel, loc: f"https://www.booking.com/searchresults.html?ss={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.booking.com/searchresults.html?ss={urllib.parse.quote(loc)}"
            },
            {
                'id': 'trivago',
                'name': 'Trivago',
                'badge': "Compare 100+ European Sites",
                'tagline': "Metasearch comparing deals from Expedia, Hotels.com, and local chains",
                'color': '#007fac',
                'bg_gradient': 'linear-gradient(135deg, #007fac 0%, #00a896 100%)',
                'icon_class': 'bi-bar-chart-fill',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.trivago.com/en-US/srl/{urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.trivago.com/en-US/srl/{urllib.parse.quote(loc)}"
            },
            {
                'id': 'expedia_eu',
                'name': 'Expedia Europe',
                'badge': "Curated Packages",
                'tagline': "Trusted flights + stays combo for Parisian and London escapes",
                'color': '#00355f',
                'bg_gradient': 'linear-gradient(135deg, #00355f 0%, #0056b3 100%)',
                'icon_class': 'bi-airplane-engines-fill',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.expedia.com/Hotel-Search?destination={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.expedia.com/Hotel-Search?destination={urllib.parse.quote(loc)}"
            },
            {
                'id': 'lastminute',
                'name': 'Lastminute.com',
                'badge': "Boutique & Luxury Deals",
                'tagline': "Secret hotel deals and top-tier luxury getaways across Europe",
                'color': '#e83e8c',
                'bg_gradient': 'linear-gradient(135deg, #e83e8c 0%, #ff6b8b 100%)',
                'icon_class': 'bi-clock-history',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.lastminute.com/hotels/search?destination={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.lastminute.com/hotels/search?destination={urllib.parse.quote(loc)}"
            }
        ]
    },
    'middle_east': {
        'country_name': 'Middle East & UAE',
        'flag': '🇦🇪',
        'currency_code': 'AED',
        'primary_app': 'Almosafer',
        'description': "In the UAE and Middle East (Dubai, Abu Dhabi, Saudi Arabia), Almosafer (المسافر) and Wego lead regional bookings alongside international luxury portals.",
        'apps': [
            {
                'id': 'almosafer',
                'name': 'Almosafer (المسافر)',
                'badge': "Middle East's Leading App",
                'tagline': "Top travel app in GCC for luxury suites, beach resorts & chalets",
                'color': '#009688',
                'bg_gradient': 'linear-gradient(135deg, #009688 0%, #4db6ac 100%)',
                'icon_class': 'bi-moon-stars-fill',
                'is_primary': True,
                'search_hotel': lambda hotel, loc: f"https://www.almosafer.com/en/hotels/{urllib.parse.quote(loc)}",
                'search_city': lambda loc: f"https://www.almosafer.com/en/hotels/{urllib.parse.quote(loc)}"
            },
            {
                'id': 'wego',
                'name': 'Wego Hotels',
                'badge': "MENA Rate Comparison",
                'tagline': "Real-time hotel price engine trusted across the Arab world",
                'color': '#2e7d32',
                'bg_gradient': 'linear-gradient(135deg, #2e7d32 0%, #4caf50 100%)',
                'icon_class': 'bi-compass-fill',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.wego.com/hotels/{urllib.parse.quote(loc)}",
                'search_city': lambda loc: f"https://www.wego.com/hotels/{urllib.parse.quote(loc)}"
            },
            {
                'id': 'booking_me',
                'name': 'Booking.com Arabia',
                'badge': "Luxury 5-Star Suites",
                'tagline': "Direct bookings for Burj Al Arab, Palm Jumeirah & luxury retreats",
                'color': '#003580',
                'bg_gradient': 'linear-gradient(135deg, #003580 0%, #0056b3 100%)',
                'icon_class': 'bi-gem',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.booking.com/searchresults.html?ss={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.booking.com/searchresults.html?ss={urllib.parse.quote(loc)}"
            }
        ]
    },
    'global': {
        'country_name': 'International / Global',
        'flag': '🌍',
        'currency_code': 'USD',
        'primary_app': 'Booking.com',
        'description': "For international destinations, travelers rely on premier global booking engines to discover verified rooms, compare prices, and read verified traveler reviews.",
        'apps': [
            {
                'id': 'booking_global',
                'name': 'Booking.com',
                'badge': "World's #1 Hotel App",
                'tagline': "Over 28 million listings worldwide with free cancellation",
                'color': '#003580',
                'bg_gradient': 'linear-gradient(135deg, #003580 0%, #0056b3 100%)',
                'icon_class': 'bi-globe-americas',
                'is_primary': True,
                'search_hotel': lambda hotel, loc: f"https://www.booking.com/searchresults.html?ss={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.booking.com/searchresults.html?ss={urllib.parse.quote(loc)}"
            },
            {
                'id': 'agoda_global',
                'name': 'Agoda',
                'badge': "Best Price Guarantee",
                'tagline': "Global hotels and accommodations with exclusive mobile rates",
                'color': '#2a64c5',
                'bg_gradient': 'linear-gradient(135deg, #2a64c5 0%, #4a90e2 100%)',
                'icon_class': 'bi-percent',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.agoda.com/search?text={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.agoda.com/search?text={urllib.parse.quote(loc)}"
            },
            {
                'id': 'expedia_global',
                'name': 'Expedia',
                'badge': "Global Travel Giant",
                'tagline': "Full vacation packages and hotel reservations worldwide",
                'color': '#00355f',
                'bg_gradient': 'linear-gradient(135deg, #00355f 0%, #0056b3 100%)',
                'icon_class': 'bi-airplane-engines-fill',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.expedia.com/Hotel-Search?destination={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.expedia.com/Hotel-Search?destination={urllib.parse.quote(loc)}"
            },
            {
                'id': 'google_hotels_global',
                'name': 'Google Hotels',
                'badge': "Universal Price Comparison",
                'tagline': "Compare rates across all travel agencies and direct hotel websites",
                'color': '#4285f4',
                'bg_gradient': 'linear-gradient(135deg, #4285f4 0%, #34a853 100%)',
                'icon_class': 'bi-google',
                'is_primary': False,
                'search_hotel': lambda hotel, loc: f"https://www.google.com/travel/hotels?q={urllib.parse.quote(hotel + ' ' + loc)}",
                'search_city': lambda loc: f"https://www.google.com/travel/hotels?q={urllib.parse.quote(loc)}"
            }
        ]
    }
}


# ── 3. Intelligent Location-to-Country Matcher ────────────────────────────────
def detect_country_key(location_str):
    """
    Determines the appropriate country or regional key from a location string.
    Works for country names, state names, and city names.
    """
    if not location_str:
        return 'india'
        
    loc = location_str.strip().lower()

    # Japan check
    japan_keywords = ['japan', 'tokyo', 'kyoto', 'osaka', 'sapporo', 'hiroshima', 'nara', 
                      'yokohama', 'fukuoka', 'nagoya', 'okinawa', 'kobe', 'hakone', 'shinjuku', 'shibuya', 'ginza']
    if any(k in loc for k in japan_keywords):
        return 'japan'

    # Southeast Asia check
    sea_keywords = ['thailand', 'bangkok', 'phuket', 'chiang mai', 'pattaya', 'krabi', 'koh samui',
                    'indonesia', 'bali', 'ubud', 'jakarta', 'lombok', 'surabaya',
                    'singapore', 'malaysia', 'kuala lumpur', 'penang', 'langkawi',
                    'vietnam', 'hanoi', 'ha long', 'da nang', 'ho chi minh', 'phu quoc', 'philippines', 'manila']
    if any(k in loc for k in sea_keywords):
        return 'southeast_asia'

    # USA & Canada check
    us_keywords = ['usa', 'united states', 'america', 'new york', 'los angeles', 'las vegas', 
                   'chicago', 'san francisco', 'miami', 'orlando', 'grand canyon', 'hawaii', 
                   'california', 'texas', 'seattle', 'boston', 'canada', 'toronto', 'vancouver', 'montreal']
    if any(k in loc for k in us_keywords):
        return 'usa_canada'

    # Middle East & UAE check
    me_keywords = ['uae', 'united arab emirates', 'dubai', 'abu dhabi', 'sharjah', 
                   'saudi', 'riyadh', 'jeddah', 'qatar', 'doha', 'egypt', 'cairo', 'giza']
    if any(k in loc for k in me_keywords):
        return 'middle_east'

    # Europe & UK check
    eu_keywords = ['europe', 'uk', 'united kingdom', 'england', 'scotland', 'london', 'edinburgh',
                   'france', 'paris', 'nice', 'lyon', 'cannes',
                   'italy', 'rome', 'venice', 'florence', 'milan', 'amalfi',
                   'germany', 'berlin', 'munich', 'frankfurt',
                   'spain', 'barcelona', 'madrid', 'ibiza', 'seville',
                   'switzerland', 'swiss alps', 'zurich', 'geneva', 'lucerne', 'zermatt',
                   'greece', 'santorini', 'athens', 'mykonos']
    if any(k in loc for k in eu_keywords):
        return 'europe_uk'

    # Indian locations check (States and major cities)
    india_keywords = [
        'india', 'andhra pradesh', 'telangana', 'tamil nadu', 'karnataka', 'kerala', 'maharashtra',
        'goa', 'rajasthan', 'delhi', 'new delhi', 'uttar pradesh', 'west bengal', 'punjab', 'gujarat',
        'himachal', 'uttarakhand', 'madhya pradesh', 'odisha', 'bihar', 'assam', 'meghalaya',
        'araku', 'visakhapatnam', 'vizag', 'hyderabad', 'mumbai', 'bangalore', 'bengaluru', 'chennai',
        'jaipur', 'udaipur', 'varanasi', 'kolkata', 'pune', 'srikakulam', 'kakinada', 'tirupati',
        'vijayawada', 'munnar', 'wayanad', 'coorg', 'mysore', 'gokarna', 'manali', 'shimla', 'rishikesh',
        'agra', 'amritsar', 'shirdi', 'lonavala', 'rajahmundry', 'suryalanka', 'ahobilam', 'yaganti',
        'lepakshi', 'kurnool', 'maredumilli', 'nallamala', 'pulicat', 'coringa', 'talakona', 'bhadrachalam',
        'warangal', 'kuntala', 'ramappa', 'basara', 'yercaud', 'kodaikanal', 'thanjavur', 'trichy',
        'chidambaram', 'vellore', 'yelagiri', 'kumbakonam', 'dandeli', 'bandipur', 'kabini', 'aihole',
        'pattadakal', 'belur', 'halebidu', 'alleppey', 'thekkady', 'kovalam', 'thrissur', 'guruvayur',
        'varkala', 'calangute', 'baga', 'dudhsagar', 'panaji', 'palolem', 'ajanta', 'aurangabad',
        'nashik', 'kolhapur', 'tarkarli', 'jaisalmer', 'khajuraho', 'darjeeling', 'konark', 'puri',
        'cherrapunji', 'kaziranga', 'hampi', 'kanyakumari', 'mahabalipuram', 'rameswaram', 'madurai'
    ]
    if any(k in loc for k in india_keywords):
        return 'india'

    # Default to global if international and not explicitly in India
    return 'india' if 'india' in loc else 'global'


def get_country_hotel_info(location_str):
    """
    Returns the rich metadata and app definitions for the country corresponding to the location.
    Includes country name, flag, primary app, description, and list of regional booking apps.
    """
    key = detect_country_key(location_str)
    country_data = COUNTRY_HOTEL_APPS_DATABASE.get(key, COUNTRY_HOTEL_APPS_DATABASE['global'])
    
    # Customize country name if specific city was searched (e.g. "Japan" vs "Tokyo, Japan")
    loc_title = location_str.strip().title() if location_str else "Destination"

    # Compute pre-filled search URLs for the overall city across each app
    rendered_apps = []
    for app in country_data['apps']:
        app_copy = app.copy()
        app_copy['city_search_url'] = app['search_city'](loc_title)
        rendered_apps.append(app_copy)

    return {
        'country_key': key,
        'country_name': country_data['country_name'],
        'flag': country_data['flag'],
        'currency_code': country_data['currency_code'],
        'primary_app': country_data['primary_app'],
        'description': country_data['description'],
        'apps': rendered_apps
    }


def get_country_hotel_apps(location_str):
    """Convenience alias returning the list of booking apps for the location's country."""
    apps = get_country_hotel_info(location_str)['apps']
    for a in apps:
        if 'name' in a and 'app_name' not in a:
            a['app_name'] = a['name']
    return apps


def get_hotel_booking_options(hotel_name, location_str):
    """
    Builds direct hotel-specific search & booking links for all relevant apps in that country.
    """
    key = detect_country_key(location_str)
    country_data = COUNTRY_HOTEL_APPS_DATABASE.get(key, COUNTRY_HOTEL_APPS_DATABASE['global'])
    loc_title = location_str.strip().title() if location_str else ""
    
    booking_options = []
    for app in country_data['apps']:
        booking_options.append({
            'app_id': app['id'],
            'app_name': app['name'],
            'badge': app['badge'],
            'color': app['color'],
            'bg_gradient': app['bg_gradient'],
            'icon_class': app['icon_class'],
            'is_primary': app['is_primary'],
            'url': app['search_hotel'](hotel_name, loc_title)
        })
        
    return booking_options


def format_facilities(amenities_list):
    """
    Enriches a simple list of amenity strings into detailed facility objects with icons and descriptions.
    """
    formatted = []
    for item in amenities_list:
        clean_item = item.strip()
        matched = None
        for cat_key, cat_val in FACILITY_CATALOG.items():
            if cat_key.lower() in clean_item.lower():
                matched = cat_val.copy()
                break
        
        if not matched:
            matched = {
                'name': clean_item,
                'icon': 'bi-check-circle-fill',
                'badge_class': 'bg-light text-secondary border',
                'desc': clean_item
            }
        formatted.append(matched)
        
    return formatted

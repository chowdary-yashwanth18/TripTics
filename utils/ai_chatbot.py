# ============================================================
# utils/ai_chatbot.py – AI Travel Concierge & Day Planner
# ============================================================
"""
Provides intelligent day-by-day and hour-by-hour travel planning,
sequencing ('where to go first'), relaxing chill-out spots, and
birthday party / celebration recommendations for any destination.
Always specifies real, named spots, exact venues, and addresses.
Comprehensive multi-day plans cover ALL categories: temples & heritage,
scenic viewpoints & hill stations, waterfalls, trekking trails, zoos & wildlife,
botanical gardens & farms, and waterparks / fun zones.
Supports traveler personas (nature lover, devotional/temple pilgrim, family/friends, adventure).
Includes nearby transit ATMs for Railway Stations, Bus Stands, and Airports.
"""

import os
import re
import json
import urllib.parse
from utils.atm_service import get_nearby_atms
from utils.destination_guide import get_destination_master_guide

# Try loading Gemini if available
def _call_gemini_if_configured(prompt, system_instruction):
    gemini_key = os.environ.get('GEMINI_API_KEY', '')
    if not gemini_key:
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith('GEMINI_API_KEY'):
                        gemini_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                        break

    if not gemini_key:
        return None

    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=system_instruction
        )
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
    except Exception:
        pass
    return None


# ==============================================================================
# COMPREHENSIVE CURATED DESTINATIONS (ALL CATEGORIES & REAL NAMED SPOTS)
# ==============================================================================
CURATED_DESTINATIONS = {
    # ── GUJARAT ───────────────────────────────────────────────────────────────
    'gujarat': {
        'name': 'Gujarat',
        'title': 'Gujarat, India',
        'categories': {
            'temples': [
                "🛕 **Somnath Jyotirlinga Temple** (Prabhas Patan, Veraval): The first among the twelve sacred Shiva Jyotirlingas, overlooking the Arabian Sea with grand evening sound-and-light show.",
                "🛕 **Dwarkadhish Temple (Jagat Mandir)** (Dwarka): 2,200-year-old 5-story temple dedicated to Lord Krishna on the sacred Gomti River confluence.",
                "🛕 **Akshardham Temple & Water Show** (Sector 20, Gandhinagar): Magnificent pink sandstone cultural complex with sprawling gardens and the 'Sat-Chit-Anand' musical water fountain.",
                "🛕 **Sun Temple Modhera** (Mehsana): 11th-century Solanki architectural marvel dedicated to Surya, featuring the stunning Surya Kund stepped tank.",
                "🛕 **Hutheesing Jain Temple** (Shahibaug, Ahmedabad): Intricately carved white marble Jain architectural gem built in 1848."
            ],
            'viewpoints_hills': [
                "🌄 **Saputara Hill Station (Governor's Hill & Sunrise Point)**: Gujarat's only hill station at 3,000 ft in the Sahyadri range with cool mountain mist, pine groves, and panoramic sunset views.",
                "🚠 **Girnar Hill & Ropeway** (Junagadh): Asia's highest and longest passenger ropeway ascending 2,800 ft to ancient Hindu and Jain summit shrines.",
                "🌌 **Kala Dungar (Black Hill, Kutch)**: Highest peak in Kutch offering uninterrupted vistas across the white expanse of the Great Rann horizon."
            ],
            'waterfalls': [
                "🌊 **Gira Waterfalls** (Waghai, Dang): 30-meter high spectacular seasonal waterfall cascading into the Ambika River surrounded by dense teak forests.",
                "🌊 **Zarwani Waterfalls** (Shoolpaneshwar Wildlife Sanctuary, near Statue of Unity, Kevadia): Deep forest cascading waterfall with natural rock pools.",
                "🌊 **Hathni Mata Waterfall** (Pojar, Panchmahal): Lush 100-meter drop cascade nestled in verdant green valleys near Pavagadh."
            ],
            'trekking': [
                "🥾 **Polo Forest & Harnav Riverbed Trek** (Vijaynagar, Sabarkantha): Scenic 10 km hiking trails through deciduous forests and ancient 15th-century temple ruins.",
                "🥾 **Girnar 9,999 Steps Pilgrim Trek** (Junagadh): Legendary stone stair hike to the peak of Mount Girnar through historic gateways.",
                "🥾 **White Desert Full Moon Night Walk** (Dhordo, Kutch): Mesmerizing trek across the glistening white salt crust under moonlight."
            ],
            'wildlife_zoo': [
                "🦁 **Sasan Gir National Park & Lion Safari** (Junagadh/Amreli): The sole global refuge of the wild Asiatic Lion. Book the 06:00 AM or 03:00 PM open-top Jeep safari.",
                "🦓 **Wild Ass Sanctuary** (Little Rann of Kutch, Dhrangadhra): 4,953 sq km desert sanctuary home to the endangered Indian Wild Ass (Khur) and desert foxes.",
                "🦩 **Nalsarovar Bird Sanctuary** (Sanand): Expansive 120 sq km wetland lake hosting 250+ migratory bird species, rosy pelicans, and flamingos.",
                "🐾 **Kamla Nehru Zoological Garden** (Kankaria, Ahmedabad): Historic 117-acre green zoo housing rare albino animals, leopards, and crocodiles."
            ],
            'botanical_farms': [
                "🌸 **Sabarmati Riverfront Flower Park** (Ahmedabad): Manicured seasonal floral exhibition park along the breezy riverbank with vibrant blossoms.",
                "🌿 **Waghai Botanical Garden & Bio-Diversity Center** (Dang): 24-hectare nature sanctuary featuring 1,400+ exotic floral species, bamboo arboretum, and medicinal plant nursery.",
                "🌾 **Anand Agro-Tourism Farms & Charotar Fields** (Kheda/Anand): Scenic countryside tours rolling through lush tobacco, cotton, mustard, and organic dairy farm fields."
            ],
            'fun_zones_waterparks': [
                "🎢 **Shankus Water Park & Resort** (Ahmedabad-Mehsana Highway): One of India's pioneer water theme parks with massive tsunami wave pools, spiral thrill slides, and lazy rivers.",
                "🎢 **Swapna Srushti Water Park** (Gram Bharati Cross Road, Gandhinagar): Themed fun park with adventure rides, snow fall zone, and rain dance.",
                "🧪 **Gujarat Science City** (Sola, Ahmedabad): World-class entertainment hub with IMAX 3D Theatre, Robotic Gallery, Nature Park, and India's largest Aquatic Gallery.",
                "🎡 **Kankaria Lakefront Fun World** (Ahmedabad): Toy Train (Atal Express), Tethered Hot Air Balloon (Ahmedabad Eye), Speed Boating, and mirror maze."
            ]
        },

        'nature_lover': """### 🌿 Nature & Countryside Experience for Gujarat
* **🌾 Rolling Fields & Countryside Farms (Charotar Valley & Anand Agro-Farms):**
  * Drive through the lush rural belts of Anand, Kheda, and Mehsana lined with rolling green mustard, millet, and cotton fields. Experience authentic farm-to-table Kathiyawadi dining under neem canopies.
* **🌲 Polo Forest & Harnav Riverbed (Sabarkantha):**
  * Pristine deciduous forest with crystal-clear river walkways, chirping kingfishers, ancient Jain temple ruins, and tranquil picnic groves.
* **🏞️ Saputara Valley (Dang):**
  * Rolling Sahyadri hill slopes covered in dense bamboo forests, herbal gardens at Waghai, and cascading streams of Gira Falls.
* **🌌 Desert Silence at Kala Dungar (Kutch):**
  * Escape all city noise at the highest ridge overlooking the vast Great Rann horizon with panoramic wind breezes.""",

        'devotional_person': """### 🛕 Sacred Temple & Devotional Journey in Gujarat
* **1. Somnath Jyotirlinga (Veraval):**
  * **Timing:** Morning Darshan (06:00 AM – 11:30 AM) & Evening Aarti (07:00 PM).
  * **Experience:** The first Shiva Jyotirlinga on the roaring Arabian Sea coast. Witness the mesmerizing light-and-sound show recounting its eternal resilience.
* **2. Dwarkadhish Temple (Jagat Mandir, Dwarka):**
  * **Timing:** Mangla Aarti at 06:30 AM, Shringar at 10:30 AM, Sandhya Aarti at 07:30 PM.
  * **Experience:** Experience the grand 52-yard flag hoisting (Dhwajaji) atop the 78-meter spire overlooking the Gomti River confluence.
* **3. Sun Temple Modhera (Mehsana):**
  * Architectural marvel designed so the sun's first rays illuminate the sanctum on equinoxes. Stroll the 108 miniature shrines of Surya Kund.
* **4. Akshardham Cultural Temple Complex (Gandhinagar):**
  * Breathtaking pink sandstone carvings, peaceful prayer halls, and the evening 'Sat-Chit-Anand' spiritual water show at 07:30 PM.
* **5. Hutheesing Jain Temple (Ahmedabad):**
  * Serene 19th-century white marble sanctum with 52 intricately carved devotional shrines.""",

        'family_friends': """### 👨‍👩‍👧‍👦 Family & Friends Fun, Waterparks & Chill Out in Gujarat
* **🎢 Premier Fun Zones & Waterparks:**
  * **Shankus Water Park (Mehsana Highway):** Thrilling multi-lane racer slides, wave pools, and lazy river tubes for group fun.
  * **Gujarat Science City (Ahmedabad):** Walk through India's largest Aquatic Gallery shark tunnel, see dancing humanoid robots in Robotic Gallery, and experience IMAX 3D space shows.
  * **Kankaria Lakefront:** Ride the Atal Express toy train, go speed-boating, fly on the helium balloon, and stroll Nagina Wadi.
* **☕ Chill Hangouts & Aesthetic Cafes:**
  * **Sabarmati Riverfront Promenade & Flower Park:** Rent a group bicycle along the illuminated 11 km riverfront walkway.
  * **Zen Cafe & Amdavad ni Gufa:** Shaded open-air cafe under neem trees with stone cave artwork by M.F. Husain.
* **🎉 Birthday & Celebration Venues:**
  * **Whistling Meadows Resort & Club (Sanand-Bopal Road):** Private party lawns, poolside cabanas, personal DJ setups, and open-air catering.
  * **Makeba The Lounge Cafe & Rooftop (SG Highway):** High-energy open-air rooftop with private cabanas and city skyline views.
  * **Rann Utsav Luxury Tent City (Dhordo):** Campfire circles, Kutchi folk dances, and midnight cake cutting on the white desert.""",

        'adventure_trekker': """### 🥾 Adventure, Trekking & Wildlife Safari in Gujarat
* **🦁 Sasan Gir Asiatic Lion Dawn Safari (06:00 AM – 09:00 AM):**
  * Book the early morning open-top Jeep safari inside Gir National Park to spot wild Asiatic lions, leopards, sambar deer, and marsh crocodiles.
* **🥾 Mount Girnar Peak Trek (Junagadh):**
  * Climb the famous 9,999 stone steps or take Asia's longest ropeway to reach Guru Dattatreya and Ambaji summit peaks at 3,660 ft.
* **🌊 Gira & Zarwani Waterfalls Trek (Dang & Narmada):**
  * Hike through the lush forest reserves of Shoolpaneshwar to reach hidden rock pools and natural waterfalls.
* **🥾 Polo Forest Riverside Trail (Sabarkantha):**
  * 10 km nature trek crossing wooden river bridges, boulder-hopping along the Harnav riverbed, and exploring 15th-century ruins."""
    },

    # ── ARAKU VALLEY ─────────────────────────────────────────────────────────
    'araku': {
        'name': 'Araku Valley',
        'title': 'Araku Valley, Andhra Pradesh',
        'categories': {
            'temples': [
                "🛕 **Matsyagundam Shiva Temple** (Near Paderu, Araku): Sacred freshwater pool filled with revered giant Mahseer fish that devotees feed by hand; dedicated to Lord Matsya and Shiva.",
                "🛕 **Simhachalam Temple (Varaha Lakshmi Narasimha)** (En route via Vizag): 11th-century hill shrine covered in sandalwood paste year-round.",
                "🛕 **Modamamba Temple** (Paderu, 45 km from Araku): Celebrated tribal deity shrine set amidst rolling hills."
            ],
            'viewpoints_hills': [
                "🌄 **Galikonda Viewpoint**: Highest peak in Visakhapatnam district at 3,800 ft; panoramic view of Eastern Ghats, cloud valleys, and railway bridges.",
                "🌄 **Lambasingi (Kashmir of Andhra Pradesh)**: 85 km from Araku, famous for sub-zero winter temperatures, apple orchards, and misty pine valleys.",
                "🌄 **Sunkarimetta Ridge & View Deck**: Quiet hill vantage point with rolling coffee estate views."
            ],
            'waterfalls': [
                "🌊 **Katiki Waterfalls**: Exhilarating 50-ft cascade fed by the Gosthani River; reached via thrilling 4x4 Jeep stream-crossing and 15-min nature hike.",
                "🌊 **Chaparai Water Cascade (Dumbriguda)**: Sloping flat rocky riverbed with perennial cool streams, forest shade, and roasted bamboo chicken stalls.",
                "🌊 **Kothapalli Waterfalls**: Multi-tiered cascading falls surrounded by lush greenery, ideal for relaxing foot soaks."
            ],
            'trekking': [
                "🥾 **Katiki Waterfall Forest Hike**: Rocky stream-crossing trek through dense forest groves.",
                "🥾 **Tyda Jungle Camp Nature Trail**: Guided tribal biodiversity trail spotting regional birds and flora.",
                "🥾 **Borra Caves Subterranean Trail**: 1.5-hour trek through million-year-old limestone stalactites and stalagmites."
            ],
            'wildlife_zoo': [
                "🐾 **Tyda Jungle Bells Wildlife Zone**: Eco-tourism sanctuary with barking deer, flying squirrels, and 100+ bird species.",
                "🐾 **Indira Gandhi Zoological Park** (Vizag foothills en route): 625-acre natural forest zoo housing tigers, leopards, and wild ungulates."
            ],
            'botanical_farms': [
                "🌺 **Padmapuram Botanical Gardens**: 1942 historic garden with rare exotic trees, hanging wooden treehouses, and miniature toy train.",
                "☕ **Ananthagiri Arabica Coffee Plantations**: Shaded silver-oak estates with fragrant coffee blossoms and organic berry harvesting.",
                "🌻 **Susan Garden (Lambasingi Yellow Fields)**: Vast seasonal yellow flower fields rolling across mountain slopes."
            ],
            'fun_zones_waterparks': [
                "🎢 **Chaparai Water Slide Rocks**: Natural smooth water sliding over river boulders.",
                "☕ **Araku Coffee Museum & Activity Zone**: Interactive coffee processing, bean roasting, and homemade chocolate sampling.",
                "🏹 **Araku Tribal Museum Cultural Center**: Traditional archery, Dhimsa tribal dance workshops, and handicraft emporium."
            ]
        },

        'nature_lover': """### 🌿 Nature & Countryside Lover Experience in Araku
* **☕ Ananthagiri Shaded Coffee & Spice Plantations:**
  * Walk beneath giant silver-oak canopies draped with black pepper vines and fragrant organic Arabica coffee shrubs. Sample fresh espresso at the Coffee Museum.
* **🌊 Chaparai Water Cascades (Dumbriguda):**
  * Flat sloping riverbed with crystal-clear cool waters. Dip your feet, sit beneath the dense sal forest, and enjoy steaming roasted Bamboo Chicken.
* **🌾 Rolling Fields of Susan Garden & Lambasingi:**
  * Expansive seasonal yellow flower fields and mist-shrouded valleys offering countryside tranquility.""",

        'devotional_person': """### 🛕 Temple & Devotional Itinerary in Araku Valley
* **1. Matsyagundam Sacred Stream & Shiva Temple:**
  * Natural rock pool where sacred Mahseer fish are protected and fed by pilgrims in reverence to Lord Vishnu's Matsya avatar.
* **2. Borra Caves Natural Shiva Lingam (Dhyan Mandir):**
  * Deep inside the 1-million-year-old limestone caves sits a naturally formed stalagmite Shiva Lingam with perennial mineral water droplets.
* **3. Modamamba Temple (Paderu):**
  * Highly revered regional tribal shrine set against forested hill peaks.""",

        'family_friends': """### 👨‍👩‍👧‍👦 Family & Friends Fun & Celebrations in Araku
* **🎢 Padmapuram Botanical Gardens & Treehouses:**
  * Ride the garden toy train, stay in hanging wooden treehouses, and stroll flower-lined pathways.
* **🎉 Haritha Valley & Mayuri Resort (Araku Main Road):**
  * Private celebration lawns, poolside cabanas, personal DJ setups, and campfire BBQ night arrangements for birthday parties.
* **🏕️ Tyda Jungle Bells Camp:**
  * Wooden log cabins set in deep forest with private bonfire circles and acoustic guitar jamming under starry skies.""",

        'adventure_trekker': """### 🥾 Adventure & Waterfalls Trek in Araku
* **🌊 Katiki Waterfalls 4x4 Jeep Safari & Hike:**
  * Thrilling off-road drive through rocky riverbeds, followed by a 20-minute boulder hike to the thunderous cascade.
* **🦇 Borra Caves Underground Exploration:**
  * Trek 80 meters deep into subterranean chambers of stalactites, stalagmites, and subterranean river channels."""
    },

    # ── VISAKHAPATNAM (VIZAG, Andhra Pradesh) ─────────────────────────────────
    'visakhapatnam': {
        'name': 'Visakhapatnam',
        'title': 'Visakhapatnam (Vizag), Andhra Pradesh',
        'categories': {
            'waterfalls': [
                "🌊 **Devarapalli Waterfalls (Bahuda River Cascades)** (Near Devarapalli, ~55 km from Vizag center via Sambhuvanipalem / Anandapuram): Natural cascading waterfall tumbling over stepped rock formations into pristine freshwater swimming pools; peaceful green valley picnic setting.",
                "🌊 **Lothugedda / Lothapalli Waterfalls** (Near Chintapalli / Lothugedda forest belt, ~90 km from Vizag): Breathtaking hidden cascade cutting through rocky boulder canyons with natural freshwater plunge pools and lush Eastern Ghats forest trails.",
                "🌊 **Katiki Waterfalls** (Near Borra Caves / Gosthani riverbed, ~95 km from Vizag): A roaring 50-ft natural cascade fed by mountain streams, reached via exciting 4x4 Jeep stream-crossing ride and short jungle hike; stalls serve hot bamboo chicken.",
                "🌊 **Chaparai Water Cascades (Dumbriguda)** (~115 km from Vizag): Broad, smooth sloping river rocks where crystal-clear mountain streams flow gently amidst pine and teak canopies; famous for forest wading and roasted bamboo chicken.",
                "🌊 **Kothapalli Waterfalls** (Near G.Madugula / Paderu, ~110 km from Vizag): Multi-tiered cascading waterfall framed by verdant terraced agricultural hills and tribal settlements.",
                "🌊 **Thatipudi Reservoir & Spillway Cascades** (Near S.Kota foothills, ~65 km from Vizag): Scenic freshwater lake nestled in mountain valleys with picturesque spillway cascades and boating facilities."
            ],
            'trekking': [
                "🥾 **Kambalakonda Wildlife Sanctuary Eco-Trek** (National Highway 16): 5 km guided forest trek, canopy suspension bridge, night camping and spotted deer sanctuary.",
                "🥾 **Dolphin's Nose & Lighthouse Clifftop Hike**: Dramatic 358-meter sea-cliff overlook above the historic harbor entrance, Port, and deep blue Bay of Bengal.",
                "🥾 **Lambasingi Misty Ridge & Cheruvula Venam Trek**: High altitude hill trek through cloud-covered pine valleys in the 'Kashmir of Andhra Pradesh'.",
                "🏄 **Rushikonda Coast & Beach Water Sports**: Certified surfing lessons, sea kayaking, jet-skiing, speedboats, and beach trekking along golden sands."
            ],
            'temples': [
                "🛕 **Sri Varaha Lakshmi Narasimha Temple (Simhachalam)** (Simhachalam Hilltop, 16 km from Vizag Station): Celebrated 11th-century hill shrine where the deity remains enveloped in sacred sandalwood paste year-round.",
                "🛕 **Sri Kanaka Mahalakshmi Temple** (Burujupeta, Old Town): Ancient wish-fulfilling presiding goddess of Visakhapatnam; unique open-air sanctum without roof or doors, accessible 24/7.",
                "🛕 **Sri Sampath Vinayagar Temple** (Asilmetta Junction): Famed wish-fulfilling Ganesha temple where locals and travelers break coconuts for auspicious journeys.",
                "⛪ **Ross Hill Multifaith Mount**: Tri-hill sanctuary housing Ross Hill Catholic Church, Dargah of Ishaq Madina, and Sri Venkateswara Swamy Temple overlooking the harbor.",
                "🛕 **Bojjannakonda & Lingalakonda Buddhist Heritage Stupas** (Sankaram, Anakapalle): 4th–9th century monolithic rock-cut Buddhist stupas, meditative caves, and rock-carved reliefs."
            ],
            'botanical_farms': [
                "🌸 **Kondakarla Ava Freshwater Lake & Bird Sanctuary** (Near Atchutapuram, ~48 km from Vizag): Vast freshwater wetland lake blooming with pink lotus flowers and water lilies; country catamaran raft rides among pelicans and herons.",
                "🌾 **Lambasingi Organic Apple, Strawberry & Coffee Farms**: High-altitude organic fruit orchards and mist-shrouded yellow flower fields.",
                "🌿 **Thotlakonda & Bavikonda Coastal Hill Plateaus**: Elevated sea-facing green hill plateaus with ancient Buddhist monastic ruins and continuous sea breezes.",
                "🌴 **Mudasarlova Reservoir & Valley Park**: Shaded mango orchards, palm groves, and perennial streams nestled in a quiet green valley."
            ],
            'wildlife_zoo': [
                "🦁 **Indira Gandhi Zoological Park** (Marine Drive, Yendada): 625-acre natural forest zoo housing white tigers, Asiatic lions, leopards, primates, and aviary in open-moated habitats.",
                "🐾 **Kambalakonda Wildlife Reserve** (NH-16): Dry evergreen forest sanctuary home to Indian leopards, barking deer, pangolins, and peacocks."
            ],
            'fun_zones_waterparks': [
                "🎢 **Kailasagiri Hilltop Fun Zone & Ropeway**: Titanic viewpoint, circular toy train, and 40-ft Shiva-Parvathi statue overlooking the coastal curve.",
                "🚢 **INS Kursura Submarine & TU-142 Aircraft Museum** (RK Beach): Real walk-through naval submarine and maritime reconnaissance bomber aircraft directly on the beach.",
                "✈️ **Sea Harrier Museum** (RK Beach Promenade): Real supersonic naval fighter jet on oceanfront glass observation deck.",
                "🏄 **Rushikonda Beach Water Adventure Sports**: Jet-skiing, speedboats, banana rides, kayaking, and certified surfing school.",
                "⛲ **VMRDA City Central Park & VUDA Park**: Musical dancing fountain, roller skating rink, and bonsai garden."
            ],
            'shopping_malls': [
                "🛍️ **Inorbit Mall Visakhapatnam (Onorbit Mall)** (Salagramapuram / Kailasapuram, Port Area): Mega 600,000+ sq ft landmark shopping and entertainment hub with 150+ international/national stores, luxury hypermarket, grand food court, and multiplex.",
                "🛍️ **CMR Central Mall** (Maddilapalem, NH-16): Premier 5-story shopping mall with INOX multiplex, bowling alley, food court, and fashion brands.",
                "🛍️ **Visakhapatnam Central (Central Mall)** (Suryabagh / Jagadamba): Multi-floor department store with leading national apparel and lifestyle labels.",
                "🛍️ **Chitralaya Mall & INOX** (Suryabagh, Jagadamba): Central city mall with multi-screen INOX movie halls and family dining.",
                "🛍️ **Lepakshi Andhra Handicrafts Emporium** (Near Jagadamba Junction): Authentic GI-tagged Kondapalli toys, Kalamkari hand-printed textiles, and sandalwood artifacts.",
                "🛍️ **Kurupam Market & Jagadamba Bazaars**: Centuries-old bazaar lane famous for pure gold jewelry and authentic Uppada Jamdani silk sarees."
            ]
        },

        'waterfalls_specific': """### 🌊 Spectacular Nearby Waterfalls in & around Visakhapatnam

* **🌊 Devarapalli Waterfalls (Bahuda River Cascades)**
  * 📍 **Exact Location:** Near Devarapalli village, ~55 km from Vizag city center (accessible via Anandapuram / Sambhuvanipalem road).
  * ✨ **What to Expect:** A stunning multi-tiered cascade where the Bahuda River flows over natural rock steps into clean freshwater swimming pools.
  * 💡 **Traveler Tips:** Perfect for a peaceful half-day nature escape with friends or family; safe for foot wading and rock-pool dips. Best visited post-monsoon and in winter.

* **🌊 Lothugedda / Lothapalli Waterfalls**
  * 📍 **Exact Location:** Near Chintapalli / Lothugedda forest belt (~90 km from Visakhapatnam towards Eastern Ghats).
  * ✨ **What to Expect:** A hidden, pristine mountain waterfall tumbling through rocky boulder canyons into deep natural freshwater plunge pools.
  * 💡 **Traveler Tips:** Untouched wilderness surrounded by dense forest canopy. Wear trekking shoes for boulder hopping and bring a change of clothes for swimming.

* **🌊 Katiki Waterfalls**
  * 📍 **Exact Location:** Near Borra Caves, ~95 km from Vizag (accessed via 4x4 Jeep trail and Gosthani riverbed).
  * ✨ **What to Expect:** Spectacular 50-ft natural cascade plunging down steep green hillocks; reached via an adventurous 4x4 stream-crossing ride and short jungle hike.
  * 💡 **Traveler Tips:** Stalls at the trailhead serve freshly roasted tribal Bamboo Chicken and hot ginger tea.

* **🌊 Chaparai Water Cascades (Dumbriguda)**
  * 📍 **Exact Location:** 15 km past Araku town towards Paderu (~115 km from Vizag).
  * ✨ **What to Expect:** Broad, flat smooth sloping river rocks where crystal-clear mountain streams flow gently amidst dense pine and teak canopies.
  * 💡 **Traveler Tips:** Very popular for safe family water sliding along smooth rocks and picnic dining beneath shade trees.

* **🌊 Kothapalli Waterfalls**
  * 📍 **Exact Location:** Near G. Madugula / Paderu (~110 km from Vizag).
  * ✨ **What to Expect:** Picturesque multi-tier cascade framed by verdant terraced agricultural hills and tribal villages.

* **🌊 Thatipudi Reservoir & Spillway Cascades**
  * 📍 **Exact Location:** Near S.Kota foothills (~65 km from Vizag).
  * ✨ **What to Expect:** Scenic lake nestled in mountain valleys with picturesque spillway cascades, lush green hillocks, and boating facilities.""",

        'nature_lover': """### 🌿 Nature & Countryside Lover Experience in Visakhapatnam
* **🌾 Rolling Fields & Countryside Farms (Lambasingi & Chintapalli):**
  * Drive up into the misty Eastern Ghats where rolling yellow flower fields (Susan Garden) and organic strawberry & apple farms spread across high-altitude slopes.
* **🛶 Kondakarla Ava Freshwater Lake & Catamaran Safari:**
  * Glide across peaceful freshwater wetlands in traditional palm-log catamarans through blooming pink lotus ponds while watching pelicans and herons.
* **🌊 Thotlakonda & Bavikonda Coastal Hill Plateaus:**
  * Elevated sea-facing green hill plateaus offering unbroken ocean panoramas, ancient Buddhist stupas, and soothing sea breezes.
* **🌴 Mudasarlova Reservoir & Palm Valley:**
  * Shaded mango orchards, palm groves, and perennial mountain streams nestled in a quiet green valley.""",

        'devotional_person': """### 🛕 Most Famous & Visited Temples in & around Visakhapatnam

Here are the most sacred, famous, and widely visited temples for pilgrims visiting **Visakhapatnam**:

* **1. 🛕 Sri Varaha Lakshmi Narasimha Swamy Temple (Simhachalam Hilltop):**
  * 📍 **Exact Location:** Simhachalam Hilltop, ~16 km from Visakhapatnam Central Railway Station (frequent ghat road RTC buses and taxis).
  * ⏰ **Darshan Timings:** Morning (07:00 AM – 11:30 AM), Afternoon (12:00 PM – 04:00 PM), Evening Aarti (06:00 PM – 09:00 PM).
  * 🙏 **Sacred Significance:** The premier 11th-century hill shrine of Lord Narasimha in Andhra Pradesh. The deity remains covered with thick sandalwood paste throughout the year and is seen in His real "Nijaroopa" form only for 12 hours during the annual Chandanotsavam festival.
  * 💡 **Pilgrim Tip:** Famous for Simhachalam Appanna Laddu and Pulihara prasadam. Early morning darshan minimizes queue times.

* **2. 🛕 Sri Veera Venkata Satyanarayana Swamy Temple (Annavaram Hilltop / Ratnagiri):**
  * 📍 **Exact Location:** Ratnagiri Hilltop, Annavaram (~110 km from Vizag center via NH-16, ~2 hrs by express train or road).
  * ⏰ **Darshan Timings:** Sarva Darshanam: 06:00 AM – 12:30 PM & 01:00 PM – 09:00 PM; Sri Satyanarayana Swamy Vrathams take place continuously from 06:00 AM to 06:00 PM.
  * 🙏 **Sacred Significance:** One of the most famous and highly visited Vishnu pilgrimage destinations in India. Hundreds of thousands of devotees travel here to perform the sacred Satyanarayana Swamy Vratham for marriage, health, and family prosperity.
  * 💡 **Pilgrim Tip:** Famous for authentic Annavaram Godhumai (wheat rava) prasadam. Vratham halls on the hill accommodate both individual and group ceremonies with priest assistance.

* **3. 🛕 Sri Kanaka Mahalakshmi Temple (Burujupeta, Old Town):**
  * 📍 **Exact Location:** Burujupeta, Old Town area, Visakhapatnam (~4 km from Station).
  * ⏰ **Darshan Timings:** Open 24 Hours continuously (Special Panchamrutha Abhishekam every Thursday).
  * 🙏 **Sacred Significance:** The ancient presiding guardian goddess of Visakhapatnam. Uniquely, the sanctum sanctorum has no roof or doors, allowing devotees to pray and offer flowers directly to the deity at any hour of the day or night.

* **4. 🛕 Sri Sampath Vinayagar Temple (Asilmetta Junction):**
  * 📍 **Exact Location:** Asilmetta Junction, near RTC Bus Complex, Visakhapatnam.
  * ⏰ **Darshan Timings:** 06:00 AM – 11:30 AM & 05:30 PM – 09:00 PM.
  * 🙏 **Sacred Significance:** Renowned wish-fulfilling Ganesha temple where devotees and travelers break coconuts for auspicious beginnings and safe journeys.

* **5. 🛕 Ross Hill Multifaith Mount & Sri Venkateswara Swamy Temple:**
  * 📍 **Exact Location:** Port Area, South Channel, Visakhapatnam.
  * ⏰ **Darshan Timings:** 06:00 AM – 06:30 PM.
  * 🙏 **Sacred Significance:** Tri-hill spiritual harmony overlook housing Sri Venkateswara Swamy Temple (dating back to 1866) on one hill, Ross Hill Church on the second, and Dargah of Ishaq Madina on the third with sweeping ocean views.

* **6. 🛕 Bojjannakonda & Lingalakonda Buddhist Rock-Cut Heritage Stupas:**
  * 📍 **Exact Location:** Sankaram village, near Anakapalle (~35 km from Vizag).
  * ⏰ **Visiting Hours:** 09:00 AM – 05:00 PM.
  * 🙏 **Sacred Significance:** 4th–9th century monolithic rock-cut Buddhist stupas, meditative caves, and rock-carved Buddha reliefs.""",

        'family_friends': """### 👨‍👩‍👧‍👦 Family & Friends Fun, Waterparks & Chill Out in Visakhapatnam
* **🎢 High-Energy Fun Zones & Museums:**
  * **Kailasagiri Hilltop Park:** Ride the passenger ropeway cable car, take the circular toy train, and soak in 360-degree views from Titanic viewpoint.
  * **INS Kursura Submarine & TU-142 Aircraft Museum (RK Beach):** Walk inside a real Russian-built naval submarine and anti-submarine bomber aircraft directly on the beach promenade.
  * **Rushikonda Water Sports Zone:** Jet-skiing, banana boat rides, sea kayaking, and certified surfing lessons.
  * **Indira Gandhi Zoological Park:** 625-acre natural forest zoo with open-moated habitats for white tigers, lions, and battery buggy tours.
* **🎉 Birthday & Celebration Spots (with exact landmarks):**
  * **Novotel Varun Beach (Vue Lounge & Lawns):** Beach Road, opposite Submarine Museum — luxury sea-facing rooftop terrace with customized cake cutting.
  * **The Park Visakhapatnam (Aqua Lawns):** Beach Road, Pandurangapuram — private oceanfront lawns, beach barbecue, and personal DJ setups.
  * **Sai Priya Beach Resort:** Rushikonda Marine Drive — green beach lawns and campfire circles.
  * **Ironhill Brewery & Sky Lounge:** Siripuram VIP Road — rooftop skyline views and craft food platters.""",

        'adventure_trekker': """### 🥾 Adventure, Trekking & Waterfalls in Visakhapatnam
* **🌊 Spectacular Waterfalls:**
  * **Devarapalli Waterfalls:** ~55 km from Vizag center via Anandapuram — stepped rock cascade with natural swimming rock pools.
  * **Lothugedda / Lothapalli Waterfalls:** ~90 km from Vizag near Chintapalli — pristine hidden cascade in dense Eastern Ghats forest canyon.
  * **Katiki Waterfalls:** ~95 km from Vizag near Borra Caves — 50-ft thunderous cascade with 4x4 Jeep stream-crossing ride and bamboo chicken.
  * **Chaparai Water Cascades:** ~115 km from Vizag — smooth sloping river rocks for gentle water sliding and wading.
* **🥾 Trekking Trails & Outdoor Sports:**
  * **Kambalakonda Wildlife Sanctuary Eco-Trek (NH-16):** 5 km guided jungle trail, canopy suspension bridge, and deer sanctuary.
  * **Dolphin's Nose & Lighthouse Clifftop Hike:** Dramatic sea-cliff overlook above Vizag harbor and port.
  * **Lambasingi Cloud Ridge Trek:** High-altitude mountain hike through pine forests and cloud-shrouded peaks.
  * **Rushikonda Coastal Adventure:** Sea kayaking, scuba diving, and surfing lessons along the golden beach."""
    },

    # ── TIRUPATI (TIRUMALA, Andhra Pradesh) ───────────────────────────────────
    'tirupati': {
        'name': 'Tirupati',
        'title': 'Tirupati & Tirumala, Andhra Pradesh',
        'categories': {
            'waterfalls': [
                "🌊 **Talakona Waterfalls (Sri Venkateswara National Park)** (~45 km from Tirupati): Highest waterfall in AP (270 ft cascade) with crystal-clear medicinal freshwater pools, canopy ropewalk, and dense jungle trek.",
                "🌊 **Kapila Theertham Waterfalls** (Alipiri foothills, Tirupati): Sacred mountain cascade tumbling directly into the temple pushkarini rock pool at the base of Tirumala Hills.",
                "🌊 **Kailasakona Waterfalls** (~40 km near Narayanavanam): Perennial 40-ft cascade pouring clear spring waters into a safe rock pond.",
                "🌊 **Ubbalamadugu / Tada Falls** (~75 km near Varadaiahpalem): Multi-tiered cascades, natural swimming pools, and rocky canyon hike.",
                "🌊 **Chakra Theertham & Papavinasanam Falls** (Tirumala Hills): Mountain stream cascades in the sacred Tirumala forest."
            ],
            'trekking': [
                "🥾 **Srivari Mettu & Alipiri Footstep Pilgrimage Treks**: Historic 3,550 stone steps up the sacred Seshachalam Hills amidst chantings and deers.",
                "🥾 **Talakona Canopy Ropewalk & Forest Trail**: 240-meter canopy walk suspended 35 ft high, followed by deep jungle waterfall hike.",
                "🥾 **Silathoranam & Chakra Theertham Walk**: Rare natural rock arch formation (1.5 billion years old) and quiet woodland trail in Tirumala."
            ],
            'temples': [
                "🛕 **Sri Venkateswara Swamy Temple (Tirumala)**: The world-famous Seven Hills shrine of Lord Balaji.",
                "🛕 **Sri Padmavathi Ammavari Temple (Tiruchanur)**: Presiding consort temple, essential completion of Tirumala pilgrimage.",
                "🛕 **Sri Govindaraja Swamy Temple**: Grand 12th-century temple in Tirupati city.",
                "🛕 **Sri Kapileswara Swamy Temple (Kapila Theertham)**: Ancient Shiva rock-cut temple with sacred waterfall pool.",
                "🛕 **Sri Kalahasteeswara Temple (Srikalahasti)** (~36 km): Celebrated Vayu Lingam and Rahu-Ketu Kshetram."
            ],
            'botanical_farms': [
                "🦁 **Sri Venkateswara Zoological Park** (Asia's largest zoo, ~5,500 acres, open safari)",
                "🌾 **Regional Agricultural Research Station & Mango Orchards** (Tirupati rural belt)",
                "🌴 **Kalyani Dam & Forest Reservoir** (Picturesque lake surrounded by forested hillocks)"
            ]
        },
        'waterfalls_specific': """### 🌊 Spectacular Waterfalls in & around Tirupati

Here are verified natural waterfalls and cascades situated in and around **Tirupati**:

* **1. 🌊 Talakona Waterfalls (Sri Venkateswara National Park):**
  * 📍 **Exact Location:** Nerabailu village, ~45 km from Tirupati center (accessible via Bakarapeta / SV National Park road).
  * ✨ **What to Expect:** The highest waterfall in Andhra Pradesh (270 ft cascade) plunging through dense evergreen forests. The crystal-clear water passes through rare medicinal herbs into natural freshwater swimming pools.
  * 💡 **Traveler Tips:** Safe rock pools for swimming; includes a thrilling 240-meter canopy ropewalk suspended 35 ft high in the tree canopy and nature trails. Best visited post-monsoon and in winter.

* **2. 🌊 Kapila Theertham Waterfalls:**
  * 📍 **Exact Location:** Northern base of Tirumala Hills, Alipiri bypass, Tirupati.
  * ✨ **What to Expect:** Sacred mountain cascade tumbling over steep granite cliffs directly into the temple pushkarini / rock pool.
  * 💡 **Traveler Tips:** Magnificent sight during and after monsoon rains; holy ablution point before climbing the hill.

* **3. 🌊 Kailasakona Waterfalls:**
  * 📍 **Exact Location:** Near Narayanavanam & Puttur, ~40 km from Tirupati (via Chennai highway).
  * ✨ **What to Expect:** Perennial 40-foot cascade pouring clear spring waters into a safe rock pond with adjacent ancient Shiva-Parvati shrine.
  * 💡 **Traveler Tips:** Ideal for family picnics and weekend relaxation.

* **4. 🌊 Ubbalamadugu / Tada Falls (Siddulaiah Kona):**
  * 📍 **Exact Location:** Varadaiahpalem border, ~75 km from Tirupati.
  * ✨ **What to Expect:** Multi-tiered cascades, crystal-clear rock pools, and a 7 km adventurous boulder-hopping forest trek.
  * 💡 **Traveler Tips:** Very popular with trekkers. Wear high-grip trekking shoes and carry drinking water.

* **5. 🌊 Chakra Theertham & Papavinasanam Waterfalls:**
  * 📍 **Exact Location:** Inside Tirumala forest ridge (~5 km from Tirumala main temple).
  * ✨ **What to Expect:** Pristine mountain stream cascades nestled in sacred woodland."""
    },

    # ── GOA ───────────────────────────────────────────────────────────────────
    'goa': {
        'name': 'Goa',
        'title': 'Goa, India',
        'categories': {
            'waterfalls': [
                "🌊 **Dudhsagar Waterfalls (Bhagwan Mahavir Wildlife Sanctuary)**: India's 5th highest waterfall (310m 4-tiered cascade) plunging below the colonial railway arch bridge.",
                "🌊 **Harvalem / Arvalem Waterfalls** (~32 km from Panaji, Sanquelim): 50-meter scenic cascade pouring into a tranquil emerald pool beside ancient 6th-century rock-cut Pandava Caves.",
                "🌊 **Tambdi Surla Waterfalls** (Deep inside Mollem National Park): Secret rainforest waterfall reached via a scenic 90-minute jungle stream trek starting at the 12th-century Mahadev Temple.",
                "🌊 **Netravali / Savari Falls** (Netravali Sanctuary, South Goa): Twin secluded forest cascades with natural rock pools and bubbly lake phenomenon."
            ],
            'trekking': [
                "🥾 **Dudhsagar Railway & Forest Trail Trek**: Iconic scenic hike through tropical deciduous forests and misty mountain ravines in Mollem.",
                "🥾 **Tambdi Surla Rainforest Hike**: Pristine jungle trail traversing river crossings and virgin Western Ghats biodiversity.",
                "🥾 **Devil's Canyon Jungle Walk**: Unique rock formations and rushing mountain river canyon trail in Mollem.",
                "🥾 **Aguada to Sinquerim Coastal Clifftop Hike**: Breathtaking Arabian Sea cliff trail overlooking crashing waves and ancient ramparts."
            ],
            'temples': [
                "🛕 **Shri Mangueshi Temple (Priol, Ponda)**: Iconic 400-year-old Shiva shrine famous for its 7-story Deepastambha lamp tower.",
                "🛕 **Shri Shanta Durga Temple (Kavlem)**: Revered peaceful Goddess temple featuring Indo-Portuguese arched architecture.",
                "🛕 **Tambdi Surla Mahadev Temple**: Oldest surviving temple in Goa (12th century Kadamba black basalt architecture).",
                "🛕 **Shri Mahalaxmi Temple (Bandora)**: Sacred ancestral deity shrine with historic wooden galleries."
            ],
            'botanical_farms': [
                "🌿 **Sahakari Spice Farm** (Curti, Ponda — 130-acre organic spice plantation with guided tours & elephant baths)",
                "🌴 **Pascoal Spice Village** (Picturesque spice estate along the Mandovi tributary river)",
                "🦜 **Dr. Salim Ali Bird Sanctuary** (Mangrove swamp forest island accessed by ferry)"
            ]
        },
        'waterfalls_specific': """### 🌊 Spectacular Waterfalls in & around Goa

Here are verified natural waterfalls and cascades in and around **Goa**:

* **1. 🌊 Dudhsagar Waterfalls (The Sea of Milk):**
  * 📍 **Exact Location:** Bhagwan Mahavir Wildlife Sanctuary, Mollem (Western Ghats border).
  * 🚙 **Access:** 4x4 open safari jeeps from Kulem / Collem base, followed by a short walk through fresh water streams.
  * ✨ **What to Expect:** A colossal 310-meter four-tiered white water cataract crashing through dense jungle beneath the iconic railway bridge.
  * 💡 **Traveler Tips:** Life jackets are mandatory for swimming in the crystal-clear plunge pool. Visit during or right after monsoons for thunderous volume.

* **2. 🌊 Harvalem / Arvalem Waterfalls:**
  * 📍 **Exact Location:** Near Sanquelim, North Goa (~32 km from Panaji).
  * ✨ **What to Expect:** 50-meter scenic cascade plunging into a freshwater lake beside ancient 6th-century rock-cut Pandava Caves.
  * 💡 **Traveler Tips:** Peaceful family picnic spot with paved steps and viewing decks.

* **3. 🌊 Tambdi Surla Waterfalls:**
  * 📍 **Exact Location:** Deep inside Mollem National Park.
  * ✨ **What to Expect:** Hidden 90-minute jungle trek starting from the 12th-century Kadamba Mahadev Temple through dense Western Ghats canopy.

* **4. 🌊 Netravali / Savari Waterfalls:**
  * 📍 **Exact Location:** Netravali Wildlife Sanctuary, South Goa (~50 km from Margao).
  * ✨ **What to Expect:** Untouched double-tier forest cascade with secluded plunge pools and the nearby mysterious Bubbly Lake."""
    },

    # ── HYDERABAD (Telangana) ────────────────────────────────────────────────
    'hyderabad': {
        'name': 'Hyderabad',
        'title': 'Hyderabad, Telangana',
        'categories': {
            'temples': [
                "🛕 **Birla Mandir (Sri Venkateswara Swamy Temple)** (Naubat Pahad, Hill Fort Road): Exquisite pure white Rajasthani Makrana marble temple perched on a 280-ft hill offering serene meditation, evening chants, and panoramic views of Hussain Sagar Lake.",
                "🛕 **Chilkur Balaji Temple ('Visa Balaji')** (Chilkur Village, Gandipet): Historic 500-year-old temple where devotees complete 11 and 108 sacred pradakshinas; strictly accepts zero cash or hundi donations.",
                "🛕 **Yadadri Sri Lakshmi Narasimha Swamy Temple** (Yadagirigutta Hill, ~60 km): Massive all-granite sculpted Dravidian architectural wonder carved from Krishna Shila stone dedicated to Lord Narasimha.",
                "🛕 **Shri Jagannath Temple** (Road No. 12, Banjara Hills): Exquisite red sandstone Kalinga architectural shrine replicating the sacred Puri Jagannath Temple with serene evening aarti.",
                "🛕 **Karmanghat Hanuman Temple** (Inner Ring Road, Karmanghat): Ancient 12th-century Kakatiya-era shrine deeply revered for Tuesday and Saturday Hanuman pujas and peaceful meditation.",
                "🛕 **Peddamma Gudi** (Road No. 36, Jubilee Hills): Famous Mother Goddess temple and vibrant spiritual center of Hyderabad's traditional annual Bonalu festival."
            ],
            'heritage_monuments': [
                "🏛️ **Charminar** (Old City, Hyderabad): World-renowned 1591 CE Indo-Islamic monument with four soaring 56-meter minarets, surrounded by the vibrant bangle markets of Laad Bazaar.",
                "🏰 **Golconda Fort & Sound & Light Show** (Ibrahim Bagh): Majestic medieval fort citadel famous for acoustic engineering (Fateh Darwaza clap), royal palaces, and diamond heritage.",
                "👑 **Chowmahalla Palace** (Motigalli, near Charminar): Opulent 18th-century palace of the Nizams featuring the grand Khilwat Mubarak Durbar Hall and vintage car collection.",
                "🕌 **Qutub Shahi Tombs** (Ibrahim Bagh): Exquisite domed royal mausoleums set in landscaped Persian gardens."
            ],
            'viewpoints_hills': [
                "🌄 **Naubat Pahad & Birla Mandir Viewpoint**: 360-degree hilltop overlook of Hussain Sagar, the Secretariat, and twin cities skyline.",
                "🌄 **Golconda Bala Hissar Summit**: Highest point of Golconda Fort offering a 400-ft elevated terrace view across Hyderabad.",
                "🌊 **Tank Bund & Necklace Road (Hussain Sagar Lake)**: Scenic lake promenade with views of the giant monolithic Buddha statue."
            ],
            'waterfalls': [
                "🌊 **Mallela Theertham Waterfalls** (Nallamala Forest, ~175 km): Breathtaking 150-ft cascade tumbling into a serene rocky pool surrounded by lush forest.",
                "🌊 **Ethipothala Waterfalls** (near Nagarjuna Sagar, ~150 km): 70-ft scenic cascade on Chandravanka River with crocodile breeding sanctuary.",
                "🌊 **Kuntala Waterfalls** (Adilabad/Nirmal, ~260 km): Highest waterfall in Telangana (150 ft) gushing through Sahyadri mountain ravines."
            ],
            'trekking': [
                "🥾 **Ananthagiri Hills Forest Trek** (Vikarabad, ~75 km): Dense deciduous forest trails, ancient Anantha Padmanabha Swamy shrine, and stream walks.",
                "🥾 **Khajaguda Rock Formations Trail** (Financial District/Gachibowli): Scenic sunset bouldering amidst 2.5-billion-year-old natural granite rock formations.",
                "🥾 **Bhongir Fort Monolith Climb** (Bhuvanagiri, ~48 km): Thrilling trek climbing a single monolithic egg-shaped rock 500 feet high topped by an ancient hilltop citadel."
            ],
            'wildlife_zoo': [
                "🦁 **Nehru Zoological Park** (Mir Alam Tank, Bahadurpura): 380-acre premier zoo featuring Lion & Tiger Safari, Nocturnal Animal House, and battery-operated trams.",
                "🦌 **Mahavir Harina Vanasthali National Park** (Vanasthalipuram): Sprawling 3,700-acre protected sanctuary for endangered Blackbuck deer.",
                "🦅 **KBR National Park** (Jubilee Hills): Lush 390-acre urban protected forest with peacocks, spotted deer, and scenic 5 km perimeter walking trails."
            ],
            'botanical_farms': [
                "🌸 **Kotla Vijayabhaskara Reddy Botanical Garden** (Kothaguda, Hitec City): 120-acre botanical haven with bamboo groves, butterfly park, and medicinal plants.",
                "🌾 **Wild Waters Farm & Agritourism Resorts** (Shankarpally Road): Rural agritourism farm with mango orchards, tractor rides, pottery, and organic Telangana food."
            ],
            'fun_zones_waterparks': [
                "🎬 **Ramoji Film City** (Abdullahpurmet, Hayathnagar): Guinness World Record holder as world's largest film studio complex (2,000 acres) with live stunts, movie sets, and rides.",
                "🎢 **Wonderla Amusement Park** (Ravirala, Exit 13 ORR): World-class high-thrill amusement park featuring Equinox, Recoil roller coaster, and giant wave pools.",
                "❄️ **Snow World** (Lower Tank Bund): India's first indoor snow park maintained at -5°C with snow slides and ice sculptures."
            ]
        },
        'waterfalls_specific': """### 🌊 Waterfalls & Cascades in & around Hyderabad

Here are the most scenic waterfalls located within a weekend drive from **Hyderabad**:

* **1. 🌊 Mallela Theertham Waterfalls:**
  * 📍 **Location:** Nallamala Forest range (~175 km from Hyderabad along the Srisailam Highway).
  * ✨ **What to Expect:** A stunning 150-foot natural waterfall cascading over rock steps into a serene natural pool amidst dense teak forests.
  * 💡 **Traveler Tips:** Descend 350 stone steps to reach the pool; visit between July and January for full flow.

* **2. 🌊 Ethipothala Waterfalls:**
  * 📍 **Location:** Near Nagarjuna Sagar (~150 km from Hyderabad).
  * ✨ **What to Expect:** A majestic 70-foot cascade formed by three streams tumbling into a lagoon with a crocodile breeding center.

* **3. 🌊 Kuntala Waterfalls:**
  * 📍 **Location:** Neredigonda, Adilabad district (~260 km from Hyderabad on NH-44).
  * ✨ **What to Expect:** The highest waterfall in Telangana state (148 feet) cascading through the lush Sahyadri mountain ranges.""",

        'devotional_person': """### 🛕 Most Famous & Visited Temples in & around Hyderabad

Here are the most sacred, authentic, and widely visited temples for pilgrims visiting **Hyderabad**:

* **1. 🛕 Birla Mandir (Sri Venkateswara Swamy Temple):**
  * 📍 **Exact Location:** Perched atop the 280-foot Naubat Pahad hill, Hill Fort Road, Khairatabad (overlooking Hussain Sagar Lake).
  * ⏰ **Darshan Timings:** 07:00 AM – 12:00 PM & 03:00 PM – 09:00 PM (Best visited at sunrise or sunset).
  * 🙏 **Sacred Significance:** Breathtaking temple carved entirely from 2,000 tonnes of pure white Rajasthani Makrana marble. Dedicated to Lord Venkateswara with an 11-foot granite deity, offering a sublime atmosphere free of traditional loud temple bells to foster quiet meditation, alongside panoramic 360-degree views of the twin cities.
  * 💡 **Pilgrim Tip:** Mobile phones and cameras must be deposited in safe lockers before entering the marble sanctum.

* **2. 🛕 Chilkur Balaji Temple ("Visa Balaji"):**
  * 📍 **Exact Location:** Chilkur Village, Gandipet (~25 km from Mehdipatnam along scenic Osman Sagar lake).
  * ⏰ **Darshan Timings:** 06:00 AM – 08:00 PM (Heavy devotee footfall on weekends; weekdays or early morning recommended).
  * 🙏 **Sacred Significance:** Renowned 500-year-old temple of Lord Balaji. It strictly accepts **zero money, donations, or VIP privilege passes**. Devotees make 11 pradakshinas (circumambulations) with their heartfelt prayers and return to complete 108 pradakshinas upon fulfillment.
  * 💡 **Pilgrim Tip:** Wear comfortable walking footwear for the traditional 11 or 108 holy pradakshinas.

* **3. 🛕 Yadadri Sri Lakshmi Narasimha Swamy Temple:**
  * 📍 **Exact Location:** Yadagirigutta Hill (~60 km from Uppal, Hyderabad on the Warangal Highway NH-163).
  * ⏰ **Darshan Timings:** 04:00 AM – 09:30 PM.
  * 🙏 **Sacred Significance:** Telangana's supreme spiritual landmark and architectural wonder, sculpted entirely from solid Krishna Shila black granite in classical Dravidian temple architecture. The ancient natural cave shrine houses five forms of Lord Narasimha Swamy.

* **4. 🛕 Shri Jagannath Temple (Banjara Hills):**
  * 📍 **Exact Location:** Road No. 12, Banjara Hills, Hyderabad.
  * ⏰ **Darshan Timings:** 06:00 AM – 12:00 PM & 05:00 PM – 09:00 PM.
  * 🙏 **Sacred Significance:** Spectacular modern temple constructed from red sandstone in authentic Kalinga shikhara architecture, replicating the world-famous Puri Jagannath Temple. Celebrated for serene morning pujas and the annual grand Ratha Yatra procession.

* **5. 🛕 Karmanghat Hanuman Temple:**
  * 📍 **Exact Location:** Inner Ring Road, Karmanghat, Hyderabad (~12 km from city center).
  * ⏰ **Darshan Timings:** 06:00 AM – 12:00 PM & 04:30 PM – 08:30 PM (Special extended hours on Tuesdays & Saturdays).
  * 🙏 **Sacred Significance:** Historic 12th-century Kakatiya-era shrine consecrated by King Prola II. Devotees revere this sanctum for deep spiritual protection, continuous Hanuman Chalisa chants, and resolving life hurdles.

* **6. 🛕 Peddamma Gudi (Mother Goddess Temple):**
  * 📍 **Exact Location:** Road No. 36, Jubilee Hills, Hyderabad (right beside Peddamma Gudi Metro Station).
  * ⏰ **Darshan Timings:** 06:00 AM – 01:00 PM & 03:00 PM – 08:30 PM.
  * 🙏 **Sacred Significance:** One of the most cherished and visited goddess shrines in Hyderabad, serving as the cultural epicenter for the historic annual Bonalu festival in Ashada masam."""
    },
    # ── SRIKAKULAM (Andhra Pradesh) ──────────────────────────────────────────
    'srikakulam': {
        'name': 'Srikakulam',
        'title': 'Srikakulam, Andhra Pradesh',
        'categories': {
            'temples': [
                "🛕 **Sri Suryanarayana Swamy Temple (Arasavalli Sun Temple)** (Arasavalli, ~3 km from town): Ancient 7th-century Sun God temple where morning sunlight illuminates the feet of the Lord twice a year.",
                "🛕 **Sri Kurmanatha Swamy Temple (Srikurmam)** (~14 km from town): The only temple in the world dedicated to Lord Vishnu in His Kurma (Tortoise) Avatar, featuring a sacred tortoise sanctuary lake.",
                "🛕 **Sri Mukhalingeswara Swamy Temple (Mukhalingam)** (Jalumuru, on Vamsadhara River, ~45 km): Historic 8th-century temple complex built by Eastern Ganga kings with exquisite stone carvings.",
                "🛕 **Sri Endala Mallikarjuna Swamy Temple (Ravivalasa)** (~40 km): Unique open-sky Shiva temple worshiped directly under the sun without a roof."
            ],
            'viewpoints_hills': [
                "🌊 **Kalingapatnam Beach & Historic British Lighthouse** (~28 km): Scenic coastal confluence where Vamsadhara River meets the Bay of Bengal with a 19th-century lighthouse.",
                "🏛️ **Salihundam Buddhist Hillock & Stupas** (~30 km): 2nd-century BC Buddhist heritage hillock with panoramic river views and ancient stupas.",
                "🌄 **Baruva Sea Beach & Confluence Point** (Sompeta coastline): Pristine beach with golden sand dunes and swaying coconut groves."
            ],
            'waterfalls': [
                "🌊 **Sangam Nagavali River Cascades** (~28 km from Srikakulam): Natural river cascades and picturesque rocky riverbed at the confluence of Nagavali, Suvarnamukhi, and Vegavathi rivers.",
                "🌊 **Narayanapuram Anicut & Countryside Streams** (Burja Mandal): Scenic water spillways and lush green streams."
            ],
            'trekking': [
                "🥾 **Salihundam Buddhist Hill Walk**: Stone-step nature hike to summit stupas with uninterrupted green valley views.",
                "🥾 **Kalingapatnam Coastal Sand Dunes Hike**: Scenic sea-breeze walking trail along the ocean."
            ],
            'wildlife_zoo': [
                "🐢 **Srikurmam Sacred Tortoise Sanctuary & Lake**: Conservation lake inside Srikurmam temple caring for hundreds of revered Star Tortoises.",
                "🦜 **Telineelapuram Bird Sanctuary** (Near Tekkali, ~65 km): Famous seasonal home for thousands of migratory pelicans and painted storks from Siberia."
            ],
            'botanical_farms': [
                "🌾 **Nagavali & Vamsadhara River Green Valleys**: Fertile agricultural valleys with green paddy fields, coconut groves, and banana plantations.",
                "🌴 **Baruva Coconut Groves & Countryside**: Broad coconut farms along quiet seaside roads."
            ],
            'fun_zones_waterparks': [
                "🏖️ **Kalingapatnam Beach Park & Promenade**: Sandy beach with evening sea-breeze walks and beachside snack stalls.",
                "🏛️ **Srikakulam Town Municipal Park & Lake**: Green park with walking paths and children's play area."
            ]
        },
        'waterfalls_specific': """### 🌊 Waterfalls & Natural Cascades in & around Srikakulam

Here are scenic natural waterfalls and river cascades situated in and around **Srikakulam**:

* **1. 🌊 Sangam Nagavali River Cascades:**
  * 📍 **Location:** Sangam village, ~28 km from Srikakulam town (accessible via Amadalavalasa / Rajam road).
  * ✨ **What to Expect:** A picturesque rocky riverbed and natural water cascades where three sacred rivers meet (Nagavali, Suvarnamukhi, and Vegavathi).
  * 💡 **Tips:** Safe for foot wading along shallow rocky streams; popular for relaxing family picnics and scenic photos.

* **2. 🌊 Narayanapuram Anicut & Countryside Cascades:**
  * 📍 **Location:** Burja Mandal (~35 km from Srikakulam).
  * ✨ **What to Expect:** Rushing water spillways over stone anicuts surrounded by lush green countryside and palm trees.""",

        'devotional_person': """### 🛕 Most Famous & Visited Temples in & around Srikakulam

Here are the most famous, sacred, and widely visited temples in **Srikakulam**:

* **1. 🛕 Sri Suryanarayana Swamy Temple (Arasavalli Sun Temple):**
  * 📍 **Exact Location:** Arasavalli, ~3 km from Srikakulam town center (autos and town buses available).
  * ⏰ **Darshan Timings:** 06:00 AM – 12:30 PM & 03:30 PM – 08:00 PM.
  * 🙏 **Sacred Significance:** Built in the 7th century, this is the premier living Sun God temple in India. The temple is designed so the sun's morning rays directly touch the Lord's feet twice each year (in March and October).
  * 💡 **Pilgrim Tip:** Sunday is the most auspicious day; morning Aditya Hrudayam prayers are very peaceful.

* **2. 🛕 Sri Kurmanatha Swamy Temple (Srikurmam):**
  * 📍 **Exact Location:** Srikurmam village, ~14 km from Srikakulam town (frequent RTC buses and autos).
  * ⏰ **Darshan Timings:** 06:00 AM – 12:30 PM & 03:00 PM – 08:00 PM.
  * 🙏 **Sacred Significance:** The only temple in the entire world dedicated to Lord Vishnu in His Kurma (Tortoise) Avatar. Features a sacred tortoise sanctuary lake (Swetha Pushkarini) where rare Star Tortoises are fed by pilgrims.
  * 💡 **Pilgrim Tip:** Rare Kurma Avatar darshan and feeding the sacred tortoises in the pushkarini.

* **3. 🛕 Sri Mukhalingeswara Swamy Temple (Mukhalingam):**
  * 📍 **Exact Location:** Jalumuru, on the banks of Vamsadhara River (~45 km from Srikakulam).
  * ⏰ **Darshan Timings:** 06:00 AM – 07:30 PM.
  * 🙏 **Sacred Significance:** Ancient 8th-century stone temple built by Eastern Ganga kings with intricate carvings, sculptures, and a peaceful riverside setting.

* **4. 🛕 Sri Endala Mallikarjuna Swamy Temple (Ravivalasa):**
  * 📍 **Exact Location:** Ravivalasa, near Tekkali (~40 km from Srikakulam).
  * ⏰ **Darshan Timings:** 06:30 AM – 06:30 PM.
  * 🙏 **Sacred Significance:** Unique open-sky Shiva temple where the deity is worshipped directly under the sun without a roof."""
    }
}

# Aliases
DESTINATION_ALIASES = {
    'goa': 'goa',
    'panaji': 'goa',
    'madgaon': 'goa',
    'margao': 'goa',
    'vasco': 'goa',
    'calangute': 'goa',
    'baga': 'goa',
    'anjuna': 'goa',
    'candolim': 'goa',
    'vagator': 'goa',
    'siolim': 'goa',
    'tirupati': 'tirupati',
    'tirumala': 'tirupati',
    'tirupathi': 'tirupati',
    'renigunta': 'tirupati',
    'gujarat': 'gujarat',
    'ahmedabad': 'gujarat',
    'kutch': 'gujarat',
    'gir': 'gujarat',
    'sasan gir': 'gujarat',
    'surat': 'gujarat',
    'vadodara': 'gujarat',
    'saputara': 'gujarat',
    'kevadia': 'gujarat',
    'somnath': 'gujarat',
    'dwarka': 'gujarat',
    'polo forest': 'gujarat',

    'araku': 'araku',
    'araku valley': 'araku',
    'borra': 'araku',

    'srikakulam': 'srikakulam',
    'arasavilli': 'srikakulam',
    'arasavalli': 'srikakulam',
    'srikurmam': 'srikakulam',
    'kurmam': 'srikakulam',
    'mukhalingam': 'srikakulam',

    'visakhapatnam': 'visakhapatnam',
    'vishakapatnam': 'visakhapatnam',
    'vishakhapatnam': 'visakhapatnam',
    'vizag': 'visakhapatnam',
    'visakha': 'visakhapatnam',
    'waltair': 'visakhapatnam',

    'hyderabad': 'hyderabad',
    'secunderabad': 'hyderabad',
    'telangana': 'hyderabad',

    'bangalore': 'bangalore',
    'bengaluru': 'bangalore',
    'karnataka': 'bangalore',

    'mumbai': 'mumbai',
    'bombay': 'mumbai',
    'maharashtra': 'mumbai',
    'lonavala': 'mumbai',
    'pune': 'mumbai',

    'goa': 'goa',
    'north goa': 'goa',
    'south goa': 'goa',

    'munnar': 'munnar',
    'kerala': 'munnar',

    'jaipur': 'jaipur',
    'rajasthan': 'jaipur',

    'delhi': 'delhi',
    'new delhi': 'delhi',
    'ncr': 'delhi'
}


def _generate_comprehensive_multiday_itinerary(dest_clean, days=3, travelers=2, budget=15000):
    """
    Generates a clear, simple everyday English multi-day plan (3, 4, 5, or X days)
    that systematically covers all categories:
    Temples, Scenic Viewpoints, Waterfalls, Trekking, Wildlife/Zoo,
    Botanical Gardens/Farms, Fun Zones/Waterparks, and Stays.
    """
    dest_clean_key = dest_clean.lower()
    profile = None
    for k, v in CURATED_DESTINATIONS.items():
        if k in dest_clean_key or dest_clean_key in k:
            profile = v
            break

    dest_title = dest_clean.title()
    days_count = max(1, min(days, 7))

    lines = [
        f"### 🗺️ Easy {days_count}-Day Trip Plan for {dest_title}",
        f"**What This Plan Covers:** 🛕 Famous Temples • 🌄 Hill Points • 🌊 Waterfalls • 🥾 Nature Walks • 🦁 Zoo & Animals • 🌺 Gardens & Parks • 🎢 Fun Zones & Waterparks\n",
        f"*This plan is arranged in simple morning-to-night order so you don't waste time in traffic or travel during the hot midday hours:*\n"
    ]

    if profile and 'categories' in profile:
        cats = profile['categories']
        temples = cats.get('temples', [])
        views = cats.get('viewpoints_hills', [])
        falls = cats.get('waterfalls', [])
        treks = cats.get('trekking', [])
        wildlife = cats.get('wildlife_zoo', [])
        botanical = cats.get('botanical_farms', [])
        fun = cats.get('fun_zones_waterparks', [])

        for d in range(1, days_count + 1):
            lines.append(f"#### 📅 Day {d}:")
            if d == 1:
                t1 = temples[0] if temples else "Famous Historic Temple"
                b1 = botanical[0] if botanical else "Central Park & Gardens"
                v1 = views[0] if views else "Sunset Point"
                lines.append(f"* **🌅 Morning (08:30 AM – 11:30 AM): Visit the Main Famous Temple**")
                lines.append(f"  * {t1} — Go early in the morning so you avoid long lines and can pray peacefully.")
                lines.append(f"* **🍽️ Afternoon (12:00 PM – 02:30 PM): Good Local Lunch & Rest**")
                lines.append(f"  * Enjoy tasty local lunch at a good nearby restaurant and rest during the hot midday hours.")
                lines.append(f"* **🌺 Late Afternoon (03:00 PM – 04:30 PM): Green Gardens & Walk**")
                lines.append(f"  * {b1} — Take a pleasant walk among green trees and flowers.")
                lines.append(f"* **🌇 Sunset & Evening (05:00 PM – 07:30 PM): Sunset Point or Beach**")
                lines.append(f"  * {v1} — Enjoy the cool evening breeze and watch the sunset view with your family or friends.")
                lines.append(f"* **🌙 Night (08:00 PM onwards): Dinner & Relax**")
                lines.append(f"  * Relaxed dinner at a popular nearby restaurant.")

            elif d == 2:
                f1 = falls[0] if falls else "Beautiful Waterfalls"
                tr1 = treks[0] if treks else "Nature Forest Trail"
                v2 = views[1] if len(views) > 1 else (views[0] if views else "Hill Ridge")
                lines.append(f"* **🌄 Morning (08:00 AM – 12:30 PM): Beautiful Waterfalls & Nature**")
                lines.append(f"  * {f1} — Visit the waterfalls in the morning when the air is fresh. Take photos and dip your feet in the cool water.")
                lines.append(f"* **🥾 Lunch & Nature Walk (12:30 PM – 02:30 PM): Walk & Food**")
                lines.append(f"  * {tr1} — Take an easy walk along the trail and enjoy a fresh hot meal.")
                lines.append(f"* **☕ Afternoon (03:30 PM – 05:30 PM): Hill Viewpoint & Hot Tea/Coffee**")
                lines.append(f"  * {v2} — Sit back and sip hot tea or coffee while looking out at the hills.")
                lines.append(f"* **🔥 Evening (06:30 PM – 09:30 PM): Campfire & Dinner**")
                lines.append(f"  * Campfire, music, and a tasty dinner with family or friends.")

            elif d == 3:
                w1 = wildlife[0] if wildlife else "Zoo or Wildlife Sanctuary"
                b2 = botanical[1] if len(botanical) > 1 else (botanical[0] if botanical else "Green Countryside Farms")
                lines.append(f"* **🦁 Morning (06:30 AM – 10:30 AM): Zoo & Wildlife Park**")
                lines.append(f"  * {w1} — Visit early in the morning when animals and birds are active and easy to spot.")
                lines.append(f"* **🌾 Afternoon (11:30 AM – 03:00 PM): Countryside Farms & Green Fields**")
                lines.append(f"  * {b2} — Take a calm walk through green farm fields, gardens, and countryside spots.")
                lines.append(f"* **🏛️ Evening (04:30 PM – 07:00 PM): Historic Fort or Monument**")
                lines.append(f"  * Explore the old fort or heritage site and see the sunset.")

            elif d == 4:
                fn1 = fun[0] if fun else "Waterpark & Fun Rides"
                fn2 = fun[1] if len(fun) > 1 else "Boating & Lake Park"
                lines.append(f"* **🎢 Morning to Afternoon (10:00 AM – 03:30 PM): Waterpark & Fun Zone**")
                lines.append(f"  * {fn1} — Have fun on the water slides, wave pool, and rides with family and friends.")
                lines.append(f"* **🎡 Late Afternoon (04:00 PM – 06:30 PM): Boating & Lake Park**")
                lines.append(f"  * {fn2} — Enjoy a toy train ride, boating in the lake, or an easy stroll.")
                lines.append(f"* **🌆 Night (07:30 PM onwards): Celebration & Group Dinner**")
                lines.append(f"  * Enjoy a special dinner together. If you are celebrating a birthday or anniversary, this is a great spot for cake cutting and fun.")

            elif d == 5:
                t2 = temples[1] if len(temples) > 1 else "Second Sacred Shrine"
                v3 = views[2] if len(views) > 2 else "Final Scenic Viewpoint"
                lines.append(f"* **🛕 Morning (08:30 AM – 11:30 AM): Second Sacred Temple or Shrine**")
                lines.append(f"  * {t2} — Morning prayers and quiet, peaceful darshan.")
                lines.append(f"* **🛍️ Afternoon (01:00 PM – 04:00 PM): Shopping for Local Clothes & Sweets**")
                lines.append(f"  * Buy local famous clothes, traditional items, sweets, and gifts to take home.")
                lines.append(f"* **🌅 Sunset (05:00 PM – 07:30 PM): Final Sunset Viewpoint & Photos**")
                lines.append(f"  * {v3} — Take group photos, enjoy the sunset, and complete your trip happily.")
            else:
                lines.append(f"* **🌿 Day {d}: Relaxed Day & Local Spots:**")
                lines.append(f"  * Visit quiet gardens, try local snacks, and enjoy an easy pace.")
            lines.append("")
    else:
        # Dynamic generic fallback with categorized spots
        from utils.hotel_generator import generate_hotels
        hotels = generate_hotels(dest_clean) or [{'name': f'{dest_title} Hotel', 'address': f'Central {dest_title}'}]
        h1 = hotels[0]
        
        for d in range(1, days_count + 1):
            lines.append(f"#### 📅 Day {d}:")
            if d == 1:
                lines.append(f"* **🛕 Morning (08:30 AM – 11:30 AM): Visit the Main Famous Temple**")
                lines.append(f"  * Visit the principal historic temple or landmark in {dest_title} before midday heat.")
                lines.append(f"* **🍽️ Afternoon (12:00 PM – 02:30 PM): Tasty Local Lunch near {h1['name']}**")
                lines.append(f"  * Savor delicious local food and rest during the afternoon.")
                lines.append(f"* **🌄 Sunset (04:30 PM – 06:30 PM): Sunset Point or Beach**")
                lines.append(f"  * Enjoy the evening breeze and watch the sunset view.")
            elif d == 2:
                lines.append(f"* **🌊 Morning (08:30 AM – 12:30 PM): Beautiful Waterfalls & Nature**")
                lines.append(f"  * Explore scenic waterfalls or green nature spots near {dest_title}.")
                lines.append(f"* **🌾 Afternoon (02:00 PM – 04:30 PM): Green Gardens & Walk**")
                lines.append(f"  * Walk through pleasant gardens and countryside areas.")
                lines.append(f"* **🔥 Evening (06:00 PM onwards): Dinner & Music**")
                lines.append(f"  * Have a fun dinner with friends or family.")
            elif d == 3:
                lines.append(f"* **🦁 Morning (08:00 AM – 11:30 AM): Zoo or Wildlife Park**")
                lines.append(f"  * See animals, birds, and nature in the morning.")
                lines.append(f"* **🥾 Afternoon (02:00 PM – 05:00 PM): Easy Hill Walk or Sightseeing**")
                lines.append(f"  * Visit scenic hill spots and viewpoints.")
            elif d == 4:
                lines.append(f"* **🎢 Full Day (10:00 AM – 05:00 PM): Waterpark, Fun Rides & Shopping**")
                lines.append(f"  * Spend the day having fun on water slides, amusement rides, and visiting local shops.")
            else:
                lines.append(f"* **🛍️ Day {d}: Shopping for Local Specialties & Final Viewpoint**")
                lines.append(f"  * Pick up famous local clothes and sweets, and take final memorable photos.")
            lines.append("")

    return "\n".join(lines)


FAMOUS_WATERFALLS_DIRECTORY = {
    'tirupati': """### 🌊 Spectacular Waterfalls in & around Tirupati

Here are verified natural waterfalls and cascades situated in and around **Tirupati**:

* **1. 🌊 Talakona Waterfalls (Sri Venkateswara National Park):**
  * 📍 **Exact Location:** Nerabailu village, ~45 km from Tirupati (via Bakarapeta road, inside S.V. Biosphere Reserve).
  * ✨ **What to Expect:** The highest waterfall in Andhra Pradesh, tumbling 270 feet down sheer cliffs into crystal-clear freshwater swimming pools. The mountain stream flows through rare medicinal herbs and dense evergreen red sanders forests.
  * 💡 **Traveler Tips:** Safe, pristine freshwater rock pools for swimming and foot wading. Includes a thrilling 240-meter canopy ropewalk suspended 35 feet high in the tree canopy.

* **2. 🌊 Kapila Theertham Waterfalls:**
  * 📍 **Exact Location:** At the northern base of Tirumala Hills, Alipiri bypass, Tirupati foothills.
  * ✨ **What to Expect:** A sacred perennial mountain cascade that flows down steep granite cliffs of the Seshachalam range, plunging directly into the temple pushkarini / rock reservoir.
  * 💡 **Traveler Tips:** Spectacular natural sight; sacred ablution spot for devotees before beginning the hill ascent.

* **3. 🌊 Kailasakona Waterfalls:**
  * 📍 **Exact Location:** Near Narayanavanam & Puttur, ~40 km from Tirupati (via Chennai highway).
  * ✨ **What to Expect:** A scenic 40-foot perennial natural cascade pouring clear mineral-rich spring waters into a shallow, safe rock pond.
  * 💡 **Traveler Tips:** Ideal for relaxing family day-outings and picnics; small ancient Shiva-Parvati shrine located beside the cascade.

* **4. 🌊 Ubbalamadugu Falls (Tada Falls / Siddulaiah Kona):**
  * 📍 **Exact Location:** Varadaiahpalem border, ~75 km from Tirupati.
  * ✨ **What to Expect:** Multi-tiered mountain cascades cutting through rocky boulder canyons, featuring crystal-clear natural plunge pools and a 7 km adventurous boulder-hopping forest trek.
  * 💡 **Traveler Tips:** Very popular with trekkers and youth groups. Wear high-grip trekking shoes and carry drinking water.

* **5. 🌊 Chakra Theertham & Papavinasanam Waterfalls (Tirumala Hills):**
  * 📍 **Exact Location:** Inside Tirumala forest ridge, ~5 km from Tirumala main temple.
  * ✨ **What to Expect:** Pristine mountain streams and natural cascades flowing through tranquil forest canopies with holy ablution pools.""",

    'visakhapatnam': """### 🌊 Spectacular Nearby Waterfalls in & around Visakhapatnam

* **1. 🌊 Devarapalli Waterfalls (Bahuda River Cascades):**
  * 📍 **Location:** Near Devarapalli, ~55 km from Vizag center via Sambhuvanipalem / Anandapuram road.
  * ✨ **Experience:** Multi-tiered natural cascade tumbling over stepped rock formations into clean freshwater swimming pools; peaceful green valley picnic setting.

* **2. 🌊 Lothugedda / Lothapalli Waterfalls:**
  * 📍 **Location:** Near Chintapalli / Lothugedda forest valley (~90 km from Visakhapatnam).
  * ✨ **Experience:** Hidden cascade cutting through rocky boulder canyons with natural freshwater plunge pools and lush Eastern Ghats forest trails.

* **3. 🌊 Katiki Waterfalls:**
  * 📍 **Location:** Near Borra Caves, ~95 km from Vizag (accessed via 4x4 Jeep trail and Gosthani riverbed).
  * ✨ **Experience:** 50-ft natural cascade with adventurous stream crossings; stalls serve authentic hot bamboo chicken.

* **4. 🌊 Chaparai Water Cascades (Dumbriguda):**
  * 📍 **Location:** ~115 km from Vizag (15 km past Araku towards Paderu).
  * ✨ **Experience:** Broad, smooth sloping river rocks where crystal-clear mountain streams flow gently amidst pine and teak canopies.

* **5. 🌊 Kothapalli Waterfalls:**
  * 📍 **Location:** Near G. Madugula / Paderu (~110 km from Vizag).
  * ✨ **Experience:** Picturesque multi-tiered cascading waterfall framed by verdant terraced agricultural hills.

* **6. 🌊 Thatipudi Reservoir & Spillway Cascades:**
  * 📍 **Location:** Near S.Kota foothills (~65 km from Vizag).
  * ✨ **Experience:** Scenic mountain valley reservoir with spillway cascades, gardens, and pedal boating.""",

    'araku': """### 🌊 Spectacular Waterfalls in & around Araku Valley

* **1. 🌊 Katiki Waterfalls:**
  * 📍 **Location:** Near Borra Caves (~90 km from Vizag, 35 km from Araku center).
  * ✨ **Experience:** 50-ft thunderous mountain cascade reached via 4x4 Jeep stream-crossing ride and bamboo chicken stalls.

* **2. 🌊 Chaparai Water Cascades (Dumbriguda):**
  * 📍 **Location:** 15 km from Araku on Paderu road.
  * ✨ **Experience:** Smooth flat rocks with gentle mountain stream flow, perfect for foot dipping and wading.

* **3. 🌊 Tatiguda Waterfalls (Ananthagiri):**
  * 📍 **Location:** Ananthagiri Ghats, 25 km before Araku.
  * ✨ **Experience:** Picturesque cascade nestled amidst coffee plantations and mist-covered hills.

* **4. 🌊 Kothapalli Waterfalls:**
  * 📍 **Location:** Near Paderu (~40 km from Araku).
  * ✨ **Experience:** Multi-tiered stepped cascade framed by terraced tribal hills.""",

    'goa': """### 🌊 Spectacular Waterfalls in Goa

* **1. 🌊 Dudhsagar Waterfalls (Mollem National Park):**
  * 📍 **Location:** Bhagwan Mahaveer Sanctuary, Goa-Karnataka border (~60 km from Panaji).
  * ✨ **Experience:** One of India's tallest 4-tiered waterfalls (310 meters) cascading down sheer western ghat cliffs like a "sea of milk", traversed by a dramatic railway viaduct.
  * 💡 **Tips:** Reached via open-top 4x4 Jeep jungle safari from Kulem through river streams.

* **2. 🌊 Arvalem Waterfalls (Harvalem):**
  * 📍 **Location:** Sanquelim, North Goa (~30 km from Panaji).
  * ✨ **Experience:** 50-meter scenic cascade plunging into a freshwater lake beside ancient 6th-century rock-cut Pandava Caves.

* **3. 🌊 Tambdi Surla Waterfalls:**
  * 📍 **Location:** Inside Mollem National Park.
  * ✨ **Experience:** Hidden 90-minute jungle trek starting from the 12th-century Kadamba Mahadev Temple through dense Western Ghats canopy.""",

    'srikakulam': """### 🌊 Waterfalls & Natural Cascades in & around Srikakulam

Here are scenic natural waterfalls and river cascades situated in and around **Srikakulam**:

* **1. 🌊 Sangam Nagavali River Cascades:**
  * 📍 **Location:** Sangam village, ~28 km from Srikakulam town (accessible via Amadalavalasa / Rajam road).
  * ✨ **What to Expect:** A picturesque rocky riverbed and natural water cascades where three sacred rivers meet (Nagavali, Suvarnamukhi, and Vegavathi).
  * 💡 **Tips:** Safe for foot wading along shallow rocky streams; popular for relaxing family picnics and scenic photos.

* **2. 🌊 Narayanapuram Anicut & Countryside Cascades:**
  * 📍 **Location:** Burja Mandal (~35 km from Srikakulam).
  * ✨ **What to Expect:** Rushing water spillways over stone anicuts surrounded by lush green countryside and palm trees."""
}


def _format_waterfalls_for_chatbot(destination, guide=None, profile=None):
    """Formats verified waterfalls and natural cascades for the destination."""
    dest_title = (destination or 'Your Destination').title()
    dest_lower = (destination or '').lower().strip()
    
    # 1. If curated waterfalls_specific exists in profile, use it
    if profile and profile.get('waterfalls_specific'):
        return profile['waterfalls_specific']

    # 2. Check if destination matches any curated registry of famous waterfalls
    for key, content in FAMOUS_WATERFALLS_DIRECTORY.items():
        if key in dest_lower or dest_lower in key:
            return content
        
    # 3. Or if guide has curated waterfalls
    if guide and guide.get('tourist_spots', {}).get('waterfalls'):
        falls = guide['tourist_spots']['waterfalls']
        lines = [
            f"### 🌊 Spectacular Waterfalls in & around {dest_title}\n",
            f"Here are verified waterfalls and natural cascades situated in and around **{dest_title}**:\n"
        ]
        for f in falls:
            lines.append(f"* **🌊 {f['name']}**")
            if f.get('landmark'):
                lines.append(f"  * 📍 **Location:** {f['landmark']}")
            if f.get('desc'):
                lines.append(f"  * ✨ **Experience:** {f['desc']}")
            if f.get('highlight'):
                lines.append(f"  * 💡 **Highlight:** {f['highlight']}")
            lines.append("")
        return "\n".join(lines)
        
    # 4. Or if profile has categories.waterfalls
    if profile and profile.get('categories', {}).get('waterfalls'):
        falls = profile['categories']['waterfalls']
        lines = [
            f"### 🌊 Spectacular Waterfalls in & around {dest_title}\n",
            f"Here are verified waterfalls situated in and around **{dest_title}**:\n"
        ]
        for f in falls:
            lines.append(f"* {f}\n")
        return "\n".join(lines)
        
    # 5. Fallback generic waterfalls
    return f"""### 🌊 Spectacular Waterfalls in & around {dest_title}

Here are recommended natural waterfalls and cascades around **{dest_title}**:
* **🌊 Mountain Cascades & Valley Falls:**
  * Visit cascading forest waterfalls within 1–2 hours scenic driving distance.
  * Perfect for rock-pool foot wading, forest trails, and fresh mountain breezes.
* 💡 **Traveler Tips:** Wear sturdy trekking shoes for wet rocks and visit during morning hours for best natural lighting."""


def _format_trekking_adventure_for_chatbot(destination, guide=None, profile=None):
    """Formats verified trekking trails, wildlife safari and adventure outdoor activities."""
    dest_title = (destination or 'Your Destination').title()
    if profile and profile.get('adventure_trekker'):
        return profile['adventure_trekker']
        
    spots = (guide or {}).get('tourist_spots', {})
    treks = spots.get('hills_viewpoints', [])
    zoo = spots.get('zoo_wildlife', [])
    
    lines = [f"### 🥾 Top Trekking Trails, Outdoor Adventure & Wildlife in {dest_title}\n"]
    if treks:
        lines.append("#### ⛰️ Trekking Trails & Scenic Hill Viewpoints:")
        for t in treks:
            lines.append(f"* **🥾 {t['name']}** ({t.get('landmark', '')})")
            if t.get('desc'):
                lines.append(f"  * {t['desc']}")
        lines.append("")
    if zoo:
        lines.append("#### 🦁 Wildlife Sanctuaries & Safaris:")
        for z in zoo:
            lines.append(f"* **🐾 {z['name']}** ({z.get('landmark', '')})")
            if z.get('desc'):
                lines.append(f"  * {z['desc']}")
        lines.append("")
    return "\n".join(lines)


FAMOUS_TEMPLES_DIRECTORY = {
    'hyderabad': """### 🛕 Most Famous & Visited Temples in & around Hyderabad

Here are the most sacred, authentic, and widely visited temples for pilgrims visiting **Hyderabad**:

* **1. 🛕 Birla Mandir (Sri Venkateswara Swamy Temple):**
  * 📍 **Exact Location:** Perched atop the 280-foot Naubat Pahad hill, Hill Fort Road, Khairatabad (overlooking Hussain Sagar Lake).
  * ⏰ **Darshan Timings:** 07:00 AM – 12:00 PM & 03:00 PM – 09:00 PM.
  * 🙏 **Sacred Significance:** Breathtaking temple carved entirely from 2,000 tonnes of pure white Rajasthani Makrana marble. Dedicated to Lord Venkateswara with an 11-foot granite deity, offering a serene atmosphere for quiet meditation, alongside panoramic 360-degree views of the twin cities.
  * 💡 **Pilgrim Tip:** Mobile phones and cameras must be deposited in safe lockers before entering the marble sanctum.

* **2. 🛕 Chilkur Balaji Temple ("Visa Balaji"):**
  * 📍 **Exact Location:** Chilkur Village, Gandipet (~25 km from Mehdipatnam along scenic Osman Sagar lake).
  * ⏰ **Darshan Timings:** 06:00 AM – 08:00 PM.
  * 🙏 **Sacred Significance:** Renowned 500-year-old temple of Lord Balaji. It strictly accepts **zero money, donations, or VIP privilege passes**. Devotees make 11 pradakshinas (circumambulations) with their heartfelt prayers and return to complete 108 pradakshinas upon fulfillment.
  * 💡 **Pilgrim Tip:** Wear comfortable walking footwear for the traditional 11 or 108 holy pradakshinas.

* **3. 🛕 Yadadri Sri Lakshmi Narasimha Swamy Temple:**
  * 📍 **Exact Location:** Yadagirigutta Hill (~60 km from Uppal, Hyderabad on the Warangal Highway NH-163).
  * ⏰ **Darshan Timings:** 04:00 AM – 09:30 PM.
  * 🙏 **Sacred Significance:** Telangana's supreme spiritual landmark and architectural wonder, sculpted entirely from solid Krishna Shila black granite in classical Dravidian temple architecture. The ancient natural cave shrine houses five forms of Lord Narasimha Swamy.

* **4. 🛕 Shri Jagannath Temple (Banjara Hills):**
  * 📍 **Exact Location:** Road No. 12, Banjara Hills, Hyderabad.
  * ⏰ **Darshan Timings:** 06:00 AM – 12:00 PM & 05:00 PM – 09:00 PM.
  * 🙏 **Sacred Significance:** Spectacular modern temple constructed from red sandstone in authentic Kalinga shikhara architecture, replicating the world-famous Puri Jagannath Temple. Celebrated for serene morning pujas and the annual grand Ratha Yatra procession.

* **5. 🛕 Karmanghat Hanuman Temple:**
  * 📍 **Exact Location:** Inner Ring Road, Karmanghat, Hyderabad (~12 km from city center).
  * ⏰ **Darshan Timings:** 06:00 AM – 12:00 PM & 04:30 PM – 08:30 PM.
  * 🙏 **Sacred Significance:** Historic 12th-century Kakatiya-era shrine consecrated by King Prola II. Devotees revere this sanctum for deep spiritual protection, continuous Hanuman Chalisa chants, and resolving life hurdles.

* **6. 🛕 Peddamma Gudi (Mother Goddess Temple):**
  * 📍 **Exact Location:** Road No. 36, Jubilee Hills, Hyderabad (right beside Peddamma Gudi Metro Station).
  * ⏰ **Darshan Timings:** 06:00 AM – 01:00 PM & 03:00 PM – 08:30 PM.
  * 🙏 **Sacred Significance:** One of the most cherished and visited goddess shrines in Hyderabad, serving as the cultural epicenter for the historic annual Bonalu festival in Ashada masam.""",

    'delhi': """### 🛕 Most Famous & Visited Temples in & around Delhi

Here are the most sacred, authentic, and widely visited temples in **Delhi**:

* **1. 🛕 Swaminarayan Akshardham Temple:**
  * 📍 **Exact Location:** NH 24, Pramukh Swami Maharaj Marg, New Delhi.
  * ⏰ **Darshan Timings:** 09:30 AM – 08:00 PM (Closed on Mondays).
  * 🙏 **Sacred Significance:** World's largest comprehensive Hindu temple complex, carved from Rajasthani pink sandstone and Italian Carrara marble. Features the Sahaj Anand water show and thematic gardens.

* **2. 🛕 Shri Laxmi Narayan Temple (Birla Mandir):**
  * 📍 **Exact Location:** Mandir Marg, Near Connaught Place, New Delhi.
  * ⏰ **Darshan Timings:** 06:00 AM – 01:30 PM & 02:30 PM – 09:00 PM.
  * 🙏 **Sacred Significance:** Famous 1939 temple inaugurated by Mahatma Gandhi on the condition that all castes be allowed entry. Dedicated to Lord Vishnu and Goddess Lakshmi.

* **3. 🛕 Lotus Temple (Bahá'í House of Worship):**
  * 📍 **Exact Location:** Bahapur, Kalkaji, New Delhi.
  * ⏰ **Timings:** 09:00 AM – 05:30 PM (Closed on Mondays).
  * 🙏 **Sacred Significance:** World-famous lotus-shaped marble sanctum open to all faiths for quiet contemplation and meditation.

* **4. 🛕 ISKCON Temple Delhi (Sri Sri Radha Parthasarathi Mandir):**
  * 📍 **Exact Location:** Hare Krishna Hills, Sant Nagar, East of Kailash, New Delhi.
  * ⏰ **Darshan Timings:** 04:30 AM – 01:00 PM & 04:00 PM – 09:00 PM.
  * 🙏 **Sacred Significance:** Grand spiritual center with magnificent deities, Vedic cultural museum, and melodious evening kirtans.

* **5. 🛕 Chhatarpur Temple (Shree Adya Katyayani Shaktipeeth):**
  * 📍 **Exact Location:** Chhatarpur, South Delhi (~4 km from Qutub Minar).
  * ⏰ **Darshan Timings:** 06:00 AM – 10:00 PM.
  * 🙏 **Sacred Significance:** Sprawling 70-acre marble temple complex dedicated to Goddess Katyayani with massive 101-foot Hanuman statue.""",

    'mumbai': """### 🛕 Most Famous & Visited Temples in & around Mumbai

Here are the most sacred and widely visited temples in **Mumbai**:

* **1. 🛕 Shree Siddhivinayak Ganapati Temple:**
  * 📍 **Exact Location:** SK Bole Marg, Prabhadevi, Mumbai.
  * ⏰ **Darshan Timings:** 05:30 AM – 10:00 PM (Tuesdays 03:15 AM – 11:00 PM).
  * 🙏 **Sacred Significance:** Mumbai's supreme landmark temple dedicated to Lord Ganesha with a 2.5-foot black stone idol and gold-plated dome.

* **2. 🛕 Mahalakshmi Temple:**
  * 📍 **Exact Location:** Bhulabhai Desai Road, Mahalaxmi, Mumbai (overlooking the Arabian Sea).
  * ⏰ **Darshan Timings:** 06:00 AM – 10:00 PM.
  * 🙏 **Sacred Significance:** Historic sea-facing temple housing the tridevi murtis of Mahalakshmi, Mahakali, and Mahasaraswati adorned with gold jewelry.

* **3. 🛕 ISKCON Temple Juhu (Sri Sri Radha Rasabihariji):**
  * 📍 **Exact Location:** Hare Krishna Land, Juhu Church Road, Juhu, Mumbai.
  * ⏰ **Darshan Timings:** 04:30 AM – 01:00 PM & 04:30 PM – 09:00 PM.
  * 🙏 **Sacred Significance:** Spiritual oasis near Juhu Beach with marble temple, Govinda's restaurant, and soul-stirring evening aartis.

* **4. 🛕 Babulnath Temple:**
  * 📍 **Exact Location:** Babulnath Road, Malabar Hill, Mumbai (~150 ft above sea level).
  * ⏰ **Darshan Timings:** 05:00 AM – 10:00 PM.
  * 🙏 **Sacred Significance:** 12th-century Shiva lingam temple perched on a small hillock with panoramic sea breeze.""",

    'jaipur': """### 🛕 Most Famous & Visited Temples in & around Jaipur

Here are the most sacred and widely visited temples in **Jaipur**:

* **1. 🛕 Govind Dev Ji Temple:**
  * 📍 **Exact Location:** City Palace Complex, Jalebi Chowk, Jaipur.
  * ⏰ **Darshan Timings:** 04:30 AM – 12:00 PM & 05:45 PM – 09:00 PM (7 daily aartis).
  * 🙏 **Sacred Significance:** Historic presiding deity of the royal Kachhwaha dynasty of Jaipur. The sacred Krishna murti was brought directly from Vrindavan by Raja Man Singh.

* **2. 🛕 Birla Mandir (Laxmi Narayan Temple):**
  * 📍 **Exact Location:** Jawahar Lal Nehru Marg, Tilak Nagar, Jaipur (below Moti Dungri Fort).
  * ⏰ **Darshan Timings:** 06:00 AM – 12:00 PM & 04:00 PM – 09:00 PM.
  * 🙏 **Sacred Significance:** Modern architectural marvel built completely of pristine white Makrana marble against the green backdrop of Moti Dungri hill.

* **3. 🛕 Moti Dungri Ganesh Ji Temple:**
  * 📍 **Exact Location:** Foot of Moti Dungri Hill, Jaipur.
  * ⏰ **Darshan Timings:** 05:00 AM – 09:30 PM.
  * 🙏 **Sacred Significance:** Highly venerated Ganesha temple housing a 500-year-old vermilion sindoor idol, popular for Wednesday prayers and vehicle blessings.

* **4. 🛕 Galtaji Temple (The Monkey Temple & Sacred Springs):**
  * 📍 **Exact Location:** Galta Gorge, Khania-Balaji (~10 km east of Jaipur).
  * ⏰ **Darshan Timings:** 05:00 AM – 07:00 PM.
  * 🙏 **Sacred Significance:** Ancient pre-historic Hindu pilgrimage retreat set between natural mountain cliffs, featuring 7 holy natural spring water kunds (tanks).""",

    'bangalore': """### 🛕 Most Famous & Visited Temples in & around Bengaluru

Here are the most sacred and widely visited temples in **Bengaluru**:

* **1. 🛕 Sri Radha Krishna Temple (ISKCON Bangalore):**
  * 📍 **Exact Location:** Hare Krishna Hill, Chord Road, Rajajinagar, Bengaluru.
  * ⏰ **Darshan Timings:** 04:15 AM – 05:00 AM, 07:15 AM – 01:00 PM & 04:00 PM – 08:30 PM.
  * 🙏 **Sacred Significance:** Grand neo-classical Dravidian temple complex dedicated to Sri Radha Krishna with majestic gopurams, musical fountains, and clean spiritual atmosphere.

* **2. 🛕 Bull Temple & Dodda Ganesha (Nandi Temple):**
  * 📍 **Exact Location:** Bull Temple Road, Basavanagudi, Bengaluru.
  * ⏰ **Darshan Timings:** 06:00 AM – 08:00 PM.
  * 🙏 **Sacred Significance:** 16th-century Vijayanagara-era temple housing a monolithic granite Nandi bull (4.5m high) and adjacent Dodda Ganesha shrine with a massive butter-covered idol (Benne Alankara).

* **3. 🛕 Gavi Gangadhareshwara Temple:**
  * 📍 **Exact Location:** Gavipuram, Kempegowda Nagar, Bengaluru.
  * ⏰ **Darshan Timings:** 06:00 AM – 12:30 PM & 05:00 PM – 08:30 PM.
  * 🙏 **Sacred Significance:** Unique natural rock-cut cave temple of Lord Shiva where sunlight passes between Nandi's horns to illuminate the inner Shiva Lingam on Makar Sankranti day.""",


    'tirupati': """### 🛕 Most Famous & Visited Temples in & around Tirupati

Here are the most sacred, famous, and widely visited temples for pilgrims visiting **Tirupati**:

* **1. 🛕 Sri Venkateswara Swamy Temple (Tirumala Hilltop):**
  * 📍 **Exact Location:** Tirumala Seven Hills (~22 km from Tirupati foothills via scenic ghat road).
  * ⏰ **Darshan Timings:** Suprabhata Seva (03:00 AM) to Ekantha Seva (11:30 PM); Sarva Darshan open throughout the day.
  * 🙏 **Sacred Significance:** The world's most revered and visited Hindu temple dedicated to Lord Venkateswara (Balaji / Govinda). Famed for the divine Tirupati Laddu prasadam, sacred tonsuring (Kalyanakatta), and supreme spiritual energy.
  * 💡 **Pilgrim Tip:** Book ₹300 Special Entry Darshan online in advance via the TTD official portal (ttdevasthanams.ap.gov.in).

* **2. 🛕 Sri Padmavathi Ammavari Temple (Tiruchanur):**
  * 📍 **Exact Location:** Tiruchanur (~5 km from Tirupati railway station).
  * ⏰ **Darshan Timings:** 06:30 AM – 11:30 AM & 04:00 PM – 08:30 PM.
  * 🙏 **Sacred Significance:** Presiding consort of Lord Venkateswara; custom holds that a pilgrimage to Tirumala is complete only after seeking blessings from Mother Padmavathi.

* **3. 🛕 Sri Govindaraja Swamy Temple:**
  * 📍 **Exact Location:** Near Tirupati Railway Station in the heart of Tirupati city.
  * ⏰ **Darshan Timings:** 05:00 AM – 12:30 PM & 04:30 PM – 09:00 PM.
  * 🙏 **Sacred Significance:** Grand 12th-century temple consecrated by Saint Ramanujacharya housing Lord Vishnu in yoga-nidra reclining posture.

* **4. 🛕 Sri Kapileswara Swamy Temple (Kapila Theertham):**
  * 📍 **Exact Location:** At the base of Tirumala Hills, Alipiri bypass.
  * ⏰ **Darshan Timings:** 06:00 AM – 12:00 PM & 04:30 PM – 08:30 PM.
  * 🙏 **Sacred Significance:** Ancient rock-carved Shiva temple set beside a sacred natural mountain waterfall pool.

* **5. 🛕 Sri Kalahasteeswara Temple (Srikalahasti):**
  * 📍 **Exact Location:** Srikalahasti (~36 km from Tirupati on the Swarnamukhi River).
  * ⏰ **Darshan Timings:** 06:00 AM – 09:00 PM.
  * 🙏 **Sacred Significance:** Celebrated Pancha Bhoota Sthalam (Vayu Lingam / Wind Element) and premier Rahu-Ketu Sarpa Dosha Nivarana temple in India.""",

    'srikakulam': """### 🛕 Most Famous & Visited Temples in & around Srikakulam

Here are the most sacred, famous, and widely visited temples for pilgrims visiting **Srikakulam**:

* **1. 🛕 Sri Suryanarayana Swamy Temple (Arasavalli Sun Temple):**
  * 📍 **Exact Location:** Arasavalli, ~3 km from Srikakulam town center (autos and town buses available).
  * ⏰ **Darshan Timings:** 06:00 AM – 12:30 PM & 03:30 PM – 08:00 PM.
  * 🙏 **Sacred Significance:** Built in the 7th century by Kalinga King Devendra Varma, this is the premier living Sun God temple in India. The temple is designed so the sun's morning rays directly illuminate the deity's feet twice each year (in March and October).
  * 💡 **Pilgrim Tip:** Sunday is the most popular day for worship; morning Aditya Hrudayam prayers are peaceful.

* **2. 🛕 Sri Kurmanatha Swamy Temple (Srikurmam):**
  * 📍 **Exact Location:** Srikurmam village, ~14 km from Srikakulam town (frequent RTC buses and autos).
  * ⏰ **Darshan Timings:** 06:00 AM – 12:30 PM & 03:00 PM – 08:00 PM.
  * 🙏 **Sacred Significance:** The only temple in the entire world dedicated to Lord Vishnu in His Kurma (Tortoise) Avatar. Features a sacred tortoise sanctuary lake (Swetha Pushkarini) where rare Star Tortoises live and are fed by pilgrims.
  * 💡 **Pilgrim Tip:** Rare Kurma Avatar darshan and feeding the sacred tortoises in the pushkarini.

* **3. 🛕 Sri Mukhalingeswara Swamy Temple (Mukhalingam):**
  * 📍 **Exact Location:** Jalumuru, on the banks of Vamsadhara River (~45 km from Srikakulam).
  * ⏰ **Darshan Timings:** 06:00 AM – 07:30 PM.
  * 🙏 **Sacred Significance:** Ancient 8th-century stone temple complex built by Eastern Ganga kings with intricate carvings, sculptures, and a peaceful riverside setting.

* **4. 🛕 Sri Endala Mallikarjuna Swamy Temple (Ravivalasa):**
  * 📍 **Exact Location:** Ravivalasa, near Tekkali (~40 km from Srikakulam).
  * ⏰ **Darshan Timings:** 06:30 AM – 06:30 PM.
  * 🙏 **Sacred Significance:** Unique open-sky Shiva temple where the deity is worshipped directly under the sun without a roof.""",

    'varanasi': """### 🛕 Most Famous & Visited Temples in Varanasi (Kashi)

* **1. 🛕 Kashi Vishwanath Temple (Golden Temple of Shiva & Vishwanath Corridor):**
  * 📍 **Location:** Lahori Tola, Dashashwamedh Ghat area, Varanasi.
  * ⏰ **Timings:** Mangala Aarti (03:00 AM), Darshan (04:00 AM – 11:00 PM).
  * 🙏 **Significance:** One of the 12 sacred Jyotirlingas, the spiritual epicenter of Hinduism. Newly renovated corridor connects the temple directly to the sacred Ganga River.

* **2. 🛕 Sankat Mochan Hanuman Temple:**
  * 📍 **Location:** Saket Nagar, near Assi Ghat (~3 km from BHU).
  * ⏰ **Timings:** 05:00 AM – 10:00 PM.
  * 🙏 **Significance:** Established by Goswami Tulsidas, renowned for removing life's planetary hurdles and obstacles.

* **3. 🛕 Sri Annapurna Devi Temple:**
  * 📍 **Location:** Adjacent to Kashi Vishwanath Temple.
  * ⏰ **Timings:** 05:00 AM – 10:30 PM.
  * 🙏 **Significance:** Goddess of nourishment and abundance; traditional belief holds that no one remains hungry in Kashi under Mother Annapurna's gaze.

* **4. 🛕 Kaal Bhairav Temple:**
  * 📍 **Location:** Bharonath, Kashi.
  * ⏰ **Timings:** 05:00 AM – 01:30 PM & 04:30 PM – 09:30 PM.
  * 🙏 **Significance:** The fierce Kotwal (guardian protector) of Kashi; pilgrims visit Kaal Bhairav to seek permission before entering and leaving the holy city.""",

    'puri': """### 🛕 Most Famous & Visited Temples in Puri & Konark

* **1. 🛕 Jagannath Temple Puri (Char Dham Mahakshetra):**
  * 📍 **Location:** Grand Road (Bada Danda), Puri.
  * ⏰ **Timings:** 05:30 AM – 10:00 PM.
  * 🙏 **Significance:** One of the supreme Char Dham pilgrimage shrines dedicated to Lord Jagannath, Balabhadra, and Subhadra. Famous for the world-renowned Ratha Yatra and the sacred Mahaprasad (56 Bhog) prepared in earthen pots.

* **2. 🛕 Gundicha Temple (Mausi Maa Temple):**
  * 📍 **Location:** North end of Bada Danda (~3 km from Jagannath Temple).
  * ⏰ **Timings:** 06:00 AM – 09:00 PM.
  * 🙏 **Significance:** Holy garden sanctuary where the Deities reside during the 9 days of annual Ratha Yatra.

* **3. 🛕 Sun Temple Konark (Surya Devalaya):**
  * 📍 **Location:** Marine Drive (~35 km from Puri).
  * ⏰ **Timings:** 06:00 AM – 08:00 PM.
  * 🙏 **Significance:** UNESCO World Heritage architectural masterpiece shaped as a colossal 24-wheeled chariot of the Sun God drawn by seven horses.""",

    'madurai': """### 🛕 Most Famous & Visited Temples in Madurai

* **1. 🛕 Arulmigu Meenakshi Sundareswarar Temple:**
  * 📍 **Location:** City Center, Madurai.
  * ⏰ **Timings:** 05:00 AM – 12:30 PM & 04:00 PM – 10:00 PM.
  * 🙏 **Significance:** Architectural marvel of Dravidian heritage with 14 towering, colorfully sculpted gopurams, the sacred Golden Lotus tank, and the Hall of Thousand Pillars.

* **2. 🛕 Koodal Azhagar Temple:**
  * 📍 **Location:** Perumal Koil Street (~1 km from Meenakshi Temple).
  * ⏰ **Timings:** 06:00 AM – 12:00 PM & 04:30 PM – 09:00 PM.
  * 🙏 **Significance:** Ancient Divya Desam dedicated to Lord Vishnu portrayed in three sacred postures: sitting, standing, and reclining across three tiered sanctums.

* **3. 🛕 Thiruparankundram Murugan Temple:**
  * 📍 **Location:** Thiruparankundram (~8 km from Madurai).
  * ⏰ **Timings:** 05:30 AM – 01:00 PM & 04:00 PM – 09:00 PM.
  * 🙏 **Significance:** The first of the six sacred battle camps (Arupadaiveedu) of Lord Murugan, featuring remarkable 8th-century rock-cut cave sanctums.""",

    'amritsar': """### 🛕 Most Famous & Sacred Shrines in Amritsar

* **1. 🛕 Sri Harmandir Sahib (The Golden Temple / Sachkhand):**
  * 📍 **Location:** Golden Temple Road, Amritsar.
  * ⏰ **Timings:** Open 24/7 (Palki Sahib ceremony 04:00 AM & 10:00 PM).
  * 🙏 **Significance:** The holiest Gurdwara of Sikhism surrounded by the sacred Amrit Sarovar. The Guru Ka Langar serves over 100,000 free hot meals daily with radical equality and seva.

* **2. 🛕 Durgiana Temple (Lakshmi Narayan Temple):**
  * 📍 **Location:** Near Hathi Gate, Amritsar.
  * ⏰ **Timings:** 06:00 AM – 10:00 PM.
  * 🙏 **Significance:** Historic 16th-century temple built in the middle of a sacred lake, dedicated to Goddess Durga and Lord Krishna.""",

    'haridwar': """### 🛕 Most Famous & Visited Temples in Haridwar & Rishikesh

* **1. 🛕 Mansa Devi Temple (Bilwa Parvat):**
  * 📍 **Location:** Bilwa Parvat hilltop (accessed via ropeway/Udan Khatola or foot trek).
  * ⏰ **Timings:** 05:00 AM – 09:00 PM.
  * 🙏 **Significance:** Wish-fulfilling Goddess temple overlooking Haridwar and the meandering Ganga River.

* **2. 🛕 Chandi Devi Temple (Neel Parvat):**
  * 📍 **Location:** Neel Parvat hilltop on opposite bank of Ganga (ropeway available).
  * ⏰ **Timings:** 06:00 AM – 08:00 PM.
  * 🙏 **Significance:** Ancient Siddh Peetha established by Adi Shankaracharya.

* **3. 🛕 Har Ki Pauri & Ganga Aarti:**
  * 📍 **Location:** Har Ki Pauri Ghat, Haridwar.
  * ⏰ **Timings:** 06:00 PM – 07:30 PM every evening.
  * 🙏 **Significance:** Famed evening Ganga Aarti where thousands of lit brass lamps and floating marigold diyas illuminate the sacred river.""",

    'gujarat': """### 🛕 Most Famous & Visited Temples in Gujarat

* **1. 🛕 Somnath Jyotirlinga Temple (Prabhas Patan, Veraval):**
  * 📍 **Location:** Prabhas Patan, right on the Arabian Sea coast.
  * ⏰ **Timings:** 06:00 AM – 10:00 PM (Sound & Light show at 08:00 PM).
  * 🙏 **Significance:** The first of the 12 sacred Shiva Jyotirlingas, revered as the "Eternal Shrine" that has stood through millennia.

* **2. 🛕 Dwarkadhish Temple (Jagat Mandir, Dwarka):**
  * 📍 **Location:** Gomti Creek, Dwarka.
  * ⏰ **Timings:** 06:30 AM – 01:00 PM & 05:00 PM – 09:30 PM.
  * 🙏 **Significance:** One of the sacred Char Dham temples dedicated to Lord Krishna ("King of Dwarka"), featuring a 72-pillared spire and 52-yard sacred flag.

* **3. 🛕 Nageshwar Jyotirlinga Temple:**
  * 📍 **Location:** 15 km from Dwarka on the coastal road.
  * ⏰ **Timings:** 06:00 AM – 12:30 PM & 05:00 PM – 09:30 PM.
  * 🙏 **Significance:** Ancient Jyotirlinga shrine featuring a magnificent 80-ft seated Lord Shiva statue visible for miles.

* **4. 🛕 Ambaji Shakti Peeth Temple:**
  * 📍 **Location:** Gabbar Hill, Banaskantha.
  * ⏰ **Timings:** 07:00 AM – 11:30 AM & 07:00 PM – 09:00 PM.
  * 🙏 **Significance:** Premier Shakti Peeth where the heart of Goddess Sati is believed to have fallen; worshiped through the sacred Viso Yantra.""",

    'visakhapatnam': """### 🛕 Most Famous & Visited Temples in & around Visakhapatnam

Here are the most sacred, famous, and widely visited temples for pilgrims visiting **Visakhapatnam**:

* **1. 🛕 Sri Varaha Lakshmi Narasimha Swamy Temple (Simhachalam Hilltop):**
  * 📍 **Exact Location:** Simhachalam Hill, ~18 km from Visakhapatnam railway station (direct RTC ghat buses available).
  * ⏰ **Darshan Timings:** 07:00 AM – 11:30 AM, 12:30 PM – 02:30 PM & 03:30 PM – 07:00 PM.
  * 🙏 **Sacred Significance:** The 11th-century lion-incarnation shrine of Lord Vishnu and one of the 32 Narasimha Kshetras. The deity is continuously covered in sandalwood paste (Chandanotsavam) appearing like a Shiva Lingam.
  * 💡 **Pilgrim Tip:** ₹100 & ₹300 Special Darshan tickets save time during weekends.

* **2. 🛕 Sri Veera Venkata Satyanarayana Swamy Temple (Annavaram):**
  * 📍 **Exact Location:** Ratnagiri Hill, Annavaram (~110 km from Vizag on NH-16, frequent direct express trains & RTC buses).
  * ⏰ **Darshan Timings:** 06:00 AM – 12:30 PM & 01:00 PM – 09:00 PM.
  * 🙏 **Sacred Significance:** The second most visited pilgrimage destination in Andhra Pradesh after Tirupati. Renowned across South India for performing the holy Satyanarayana Vratham ceremony for family prosperity and health.
  * 💡 **Pilgrim Tip:** Devotees can book Vratham tickets online or at the hill counters; the famous Annavaram Godhuma Prasadam (wheat halwa in sal leaves) is world-famous.

* **3. 🛕 Sri Kanaka Maha Lakshmi Temple (Burujupeta):**
  * 📍 **Exact Location:** Burujupeta, Heritage Old Vizag area (~3 km from Vizag port/station).
  * ⏰ **Darshan Timings:** Open 24 Hours on Thursdays; 05:00 AM – 11:00 PM on other days.
  * 🙏 **Sacred Significance:** The presiding guardian deity of Visakhapatnam. The sanctum sanctorum has no roof (open to the sky) and devotees can directly perform Sparsha Darshan (touching the feet of Ammavaru).

* **4. 🛕 Sri Sampath Vinayagar Temple (Asilmetta):**
  * 📍 **Exact Location:** Waltair Uplands Road, Asilmetta, central Vizag.
  * ⏰ **Darshan Timings:** 06:00 AM – 11:00 AM & 05:30 PM – 08:30 PM.
  * 🙏 **Sacred Significance:** Revered wish-fulfilling Lord Ganesha temple where locals, travelers, and transport operators seek blessings before starting any new journey or vehicle purchase.

* **5. 🛕 Ross Hill Sacred Trio (Hilltop Inter-Faith Sanctuary):**
  * 📍 **Exact Location:** Port area overlook, South Vizag harbor.
  * ⏰ **Timings:** 06:00 AM – 06:30 PM.
  * 🙏 **Sacred Significance:** Unique tri-hill harmony featuring Ross Hill Church, Dargah Konda (Sayed Ali Ishaq Madina Dargah), and Sri Venkateswara Temple overlooking the bustling harbor.""",

    'goa': """### 🛕 Most Famous & Visited Temples & Shrines in Goa

Here are the most sacred, famous, and widely visited temples and shrines in **Goa**:

* **1. 🛕 Shri Mangueshi Temple (Priol, Ponda):**
  * 📍 **Exact Location:** Mangeshi village, Priol, Ponda (~21 km from Panaji).
  * ⏰ **Darshan Timings:** 06:00 AM – 10:00 PM.
  * 🙏 **Sacred Significance:** 400-year-old Shiva temple showcasing distinctive Goan-Hindu architecture with a magnificent seven-story Deepastambha (lamp tower) illuminated with oil lamps.

* **2. 🛕 Shri Shanta Durga Temple (Kavlem, Ponda):**
  * 📍 **Exact Location:** Foothills of Kavalem village, Ponda (~28 km from Panaji).
  * ⏰ **Darshan Timings:** 06:00 AM – 09:30 PM.
  * 🙏 **Sacred Significance:** Revered temple dedicated to Goddess Durga in her peaceful (Shanta) form who mediated peace between Vishnu and Shiva; features a grand golden palanquin (Palkhi).

* **3. 🛕 Tambdi Surla Mahadev Temple (Mollem National Park):**
  * 📍 **Exact Location:** Dense rainforest foothills, Mollem (~65 km from Panaji).
  * ⏰ **Darshan Timings:** 07:00 AM – 06:00 PM.
  * 🙏 **Sacred Significance:** The oldest intact temple in Goa (12th century Kadamba-Yadava dynasty), exquisitely hand-chiseled from black basalt stone surviving centuries in the rainforest.

* **4. 🛕 Shri Mahalaxmi Temple (Bandora, Ponda):**
  * 📍 **Exact Location:** Bandivade, Ponda.
  * ⏰ **Darshan Timings:** 06:30 AM – 08:30 PM.
  * 🙏 **Sacred Significance:** Ancient goddess shrine with 24 wooden carved panels depicting scenes from the Bhagavata Purana.

* **5. ⛪ Basilica of Bom Jesus & Se Cathedral (Old Goa):**
  * 📍 **Exact Location:** Old Goa Heritage Complex (~10 km from Panaji).
  * ⏰ **Timings:** 09:00 AM – 06:30 PM.
  * 🙏 **Sacred Significance:** UNESCO World Heritage Site housing the sacred mortal remains of St. Francis Xavier in a silver casket inside a baroque masterpiece."""
}


def is_non_temple_landmark(name):
    low = (name or '').lower()
    sacred_words = ['temple', 'mandir', 'gudi', 'shrine', 'swamy', 'devasthanam', 'kovil', 'jyotirlinga', 'dargah', 'cathedral', 'basilica', 'gurudwara', 'matha', 'peeth']
    if any(sw in low for sw in sacred_words):
        if not any(re.search(rf'\b{b}\b', low) for b in ['mall', 'circus', 'amusement', 'resort', 'hotel', 'restaurant']):
            return False
            
    non_temple_patterns = [
        r'\bcharminar\b', r'\bfort\b', r'\bpalace\b', r'\bmonument\b', r'\bmuseum\b',
        r'\bfilm city\b', r'\bgate\b', r'\bminar\b', r'\bmemorial\b', r'\bbridge\b',
        r'\btower\b', r'\bplanetarium\b', r'\blake\b', r'\bsagar\b', r'\bdam\b',
        r'\bbeach\b', r'\bfalls?\b', r'\bwaterfalls?\b', r'\bpark\b', r'\bzoo\b',
        r'\bmarket\b', r'\bbazaar\b', r'\bmall\b', r'\bcircus\b', r'\baquarium\b',
        r'\bstadium\b', r'\bstudio\b', r'\bpromenade\b', r'\bdrive\b', r'\bpoint\b',
        r'\bgarden\b', r'\bresort\b', r'\bsafari\b', r'\bsanctuary\b', r'\bridge\b',
        r'\bvalley\b', r'\btaj mahal\b', r'\bindia gate\b', r'\bgateway of india\b',
        r'\bred fort\b', r'\bhawa mahal\b', r'\bamber fort\b'
    ]
    return any(re.search(p, low) for p in non_temple_patterns)

def _format_temples_for_chatbot(destination, guide=None, profile=None):
    """Formats verified temples, sacred shrines and devotional pilgrimage details."""
    dest_title = (destination or 'Your Destination').title()
    dest_lower = (destination or '').lower().strip()
    
    # 1. If curated devotional_person exists in profile, use it
    if profile and profile.get('devotional_person'):
        return profile['devotional_person']

    # 2. Check if destination matches any curated registry of famous temples
    for key, content in FAMOUS_TEMPLES_DIRECTORY.items():
        if key in dest_lower or dest_lower in key:
            return content
        
    raw_temples = (guide or {}).get('tourist_spots', {}).get('temples', [])
    temples = []
    for t in raw_temples:
        t_name = t.get('name', '')
        if not is_non_temple_landmark(t_name):
            temples.append(t)

    # 3. If temples is empty or filtered out, check NATIONWIDE_TEMPLE_DATABASE
    if not temples:
        try:
            from utils.destination_guide import NATIONWIDE_TEMPLE_DATABASE
            for k, shrine_list in NATIONWIDE_TEMPLE_DATABASE.items():
                if k in dest_lower or dest_lower in k:
                    temples = shrine_list
                    break
        except Exception:
            pass

    lines = [f"### 🛕 Most Famous & Visited Temples in & around {dest_title}\n"]
    if temples:
        for idx, t in enumerate(temples[:6], 1):
            landmark_str = f" • 📍 {t.get('landmark', '')}" if t.get('landmark') else ""
            lines.append(f"* **{idx}. 🛕 {t['name']}**{landmark_str}")
            if t.get('timing'):
                lines.append(f"  * ⏰ **Darshan Timings:** {t['timing']}")
            if t.get('desc'):
                lines.append(f"  * 🙏 **Sacred Significance:** {t['desc']}")
            if t.get('highlight'):
                lines.append(f"  * 💡 **Pilgrim Tip:** {t['highlight']}")
            lines.append("")
        return "\n".join(lines)

    return f"""### 🛕 Most Famous & Sacred Temples in & around {dest_title}

* **1. 🛕 Historic Presiding City Devasthanam:**
  * 📍 **Location:** Central Heritage District of {dest_title}.
  * ⏰ **Darshan Timings:** 06:00 AM – 12:00 PM & 04:30 PM – 08:30 PM.
  * 🙏 **Sacred Significance:** Ancient sanctum renowned for morning aarti, peaceful architecture, and devotional darshan.
* **2. 🛕 Local Hilltop / Riverbank Pilgrimage Shrine:**
  * 📍 **Location:** Scenic spiritual ridge near {dest_title}.
  * ⏰ **Darshan Timings:** 06:30 AM – 07:30 PM.
  * 🙏 **Sacred Significance:** Sacred hill deity where devotees perform traditional pradakshinas and enjoy serene surroundings."""


def _format_nature_farms_for_chatbot(destination, guide=None, profile=None):
    """Formats countryside, organic farms, valleys, and nature lover spots."""
    dest_title = (destination or 'Your Destination').title()
    if profile and profile.get('nature_lover'):
        return profile['nature_lover']
        
    parks = (guide or {}).get('tourist_spots', {}).get('parks_botanical', [])
    lines = [f"### 🌿 Nature Spots, Countryside & Green Farms in {dest_title}\n"]
    if parks:
        for p in parks:
            lines.append(f"* **🌸 {p['name']}** ({p.get('landmark', '')})")
            if p.get('desc'):
                lines.append(f"  * {p['desc']}")
            lines.append("")
    return "\n".join(lines)


def _format_family_fun_for_chatbot(destination, guide=None, profile=None):
    """Formats waterparks, fun zones, group entertainment and celebrations."""
    dest_title = (destination or 'Your Destination').title()
    if profile and profile.get('family_friends'):
        return profile['family_friends']
        
    fun = (guide or {}).get('tourist_spots', {}).get('fun_zones_waterparks', [])
    lines = [f"### 👨‍👩‍👧‍👦 Friends & Family Fun Zones & Waterparks in {dest_title}\n"]
    if fun:
        for f in fun:
            lines.append(f"* **🎢 {f['name']}** ({f.get('landmark', '')})")
            if f.get('desc'):
                lines.append(f"  * {f['desc']}")
            lines.append("")
    return "\n".join(lines)


def _format_atms_for_chatbot(destination):
    """Formats verified transit ATM details for Railway Stations, Bus Stands, and Airports."""
    atms_data = get_nearby_atms(destination)
    lines = [
        f"### 🏧 Available 24/7 ATMs Near Transit Hubs in {destination.title()}\n",
        f"Here are verified ATM locations situated directly at or adjacent to transit hubs in **{destination.title()}** for convenient cash withdrawal:\n"
    ]

    if atms_data.get('railway'):
        lines.append("#### 🚉 Railway Station ATMs:")
        for a in atms_data['railway']:
            lines.append(f"* **🏦 {a['bank']}**")
            lines.append(f"  * **Location:** {a['location']}")
            lines.append(f"  * **Proximity:** {a['proximity']} • 🟢 {a['open_hours']}")
            lines.append(f"  * **Services:** {', '.join(a.get('features', []))}")
            lines.append(f"  * 🗺️ [Get Directions on Google Maps]({a['maps_url']})")
        lines.append("")

    if atms_data.get('bus'):
        lines.append("#### 🚌 Bus Stand / ISBT ATMs:")
        for a in atms_data['bus']:
            lines.append(f"* **🏦 {a['bank']}**")
            lines.append(f"  * **Location:** {a['location']}")
            lines.append(f"  * **Proximity:** {a['proximity']} • 🟢 {a['open_hours']}")
            lines.append(f"  * 🗺️ [Get Directions on Google Maps]({a['maps_url']})")
        lines.append("")

    if atms_data.get('airport'):
        lines.append("#### ✈️ Airport Terminal ATMs:")
        for a in atms_data['airport']:
            lines.append(f"* **🏦 {a['bank']}**")
            lines.append(f"  * **Location:** {a['location']}")
            lines.append(f"  * **Proximity:** {a['proximity']} • 🟢 {a['open_hours']}")
            lines.append(f"  * 🗺️ [Get Directions on Google Maps]({a['maps_url']})")
        lines.append("")

    lines.append("*💡 Pro-Tip: Railway station and airport ATMs operate 24/7 with continuous armed security and accept all domestic and international Visa, Mastercard, and RuPay debit/credit cards.*")
    return "\n".join(lines)


def _format_dining_for_chatbot(guide):
    dining = guide.get('dining_cuisine', {})
    lines = [f"### 🍽️ Best Traditional Dishes to Try & Dining in {guide.get('destination', 'Your Destination')}\n"]
    if dining.get('must_try_dishes'):
        lines.append("#### 🍲 Signature Dishes to Try:")
        for d in dining['must_try_dishes']:
            badge = "🟢 Veg" if "Veg" in d.get('type', '') else "🔴 Non-Veg"
            lines.append(f"* **{d['name']}** ({badge} • {d.get('type', '')})")
            lines.append(f"  * {d['desc']}")
            lines.append(f"  * 📍 **Best enjoyed at:** {d.get('best_at', 'Heritage eateries')}")
        lines.append("")
    if dining.get('famous_food_streets'):
        lines.append("#### 🍢 Iconic Food Streets & Night Chowks:")
        for s in dining['famous_food_streets']:
            lines.append(f"* **{s['name']}** ({s.get('landmark', '')})")
            lines.append(f"  * **Specialties:** {s.get('specialties', '')}")
        lines.append("")
    return "\n".join(lines)


def _format_culture_for_chatbot(guide):
    culture = guide.get('culture_traditions', {})
    lines = [f"### 🎭 Tradition, Culture, Festivals & Rituals in {guide.get('destination', 'Your Destination')}\n"]
    if culture.get('summary'):
        lines.append(f"{culture['summary']}\n")
    if culture.get('festivals_rituals'):
        lines.append("#### 🎉 Major Festivals & Sacred Rituals:")
        for f in culture['festivals_rituals']:
            lines.append(f"* **{f['name']}**")
            lines.append(f"  * **Celebration:** {f.get('importance', '')}")
            lines.append(f"  * **Rituals & Customs:** {f.get('rituals', '')}")
        lines.append("")
    if culture.get('art_crafts'):
        lines.append(f"#### 🎨 Traditional Arts & Crafts:\n* {culture['art_crafts']}\n")
    return "\n".join(lines)


def _format_malls_for_chatbot(guide):
    spots = guide.get('tourist_spots', {})
    malls = spots.get('shopping_malls', [])
    lines = [f"### 🛍️ Best Shopping Malls & Traditional Bazaars in {guide.get('destination', 'Your Destination')}\n"]
    for m in malls:
        lines.append(f"* **🏬 {m['name']}**")
        lines.append(f"  * **Exact Landmark:** {m.get('landmark', '')}")
        lines.append(f"  * **Experience:** {m.get('desc', '')}")
        lines.append(f"  * **Highlights:** {m.get('highlight', '')}")
    return "\n".join(lines)


def _format_celebrations_with_landmarks(guide):
    venues = guide.get('celebrations_venues', [])
    lines = [f"### 🎂 Birthday Parties & Celebration Spots in {guide.get('destination', 'Your Destination')}\n"]
    lines.append("*Here are premier celebration venues with exact map-style street landmarks (near landmarks / across main roads) for seamless navigation:*\n")
    for v in venues:
        phone_str = f" • 📞 Reception: {v['phone']}" if v.get('phone') else ""
        lines.append(f"* **🎉 {v['name']}**{phone_str}")
        lines.append(f"  * 🗺️ **Exact Map Landmark:** {v.get('map_landmark', '')}")
        lines.append(f"  * 🎈 **Party Vibe:** {v.get('vibe', '')}")
        lines.append(f"  * ✨ **Party Setup:** {v.get('features', '')}")
    return "\n".join(lines)


def _format_all_tourist_spots(guide):
    spots = guide.get('tourist_spots', {})
    lines = [f"### 📍 Complete Directory of Visiting Spots in {guide.get('destination', 'Your Destination')}\n"]
    category_titles = {
        'temples': '🛕 Temples & Sacred Shrines',
        'heritage_monuments': '🏛️ Heritage Monuments & Historic Forts',
        'hills_viewpoints': '🌄 Hill Stations & Scenic Viewpoints',
        'waterfalls': '🌊 Waterfalls & Natural Cascades',
        'parks_botanical': '🌳 Botanical Gardens & Nature Parks',
        'zoo_wildlife': '🦁 Zoo, Wildlife & National Parks',
        'shopping_malls': '🛍️ Shopping Malls & Traditional Bazaars',
        'fun_zones_waterparks': '🎢 Waterparks & High-Energy Fun Zones'
    }
    for cat_key, cat_title in category_titles.items():
        items = spots.get(cat_key, [])
        if items:
            lines.append(f"#### {cat_title}:")
            for item in items:
                lines.append(f"* **{item['name']}** — *{item.get('landmark', '')}*")
                if item.get('desc'):
                    lines.append(f"  * {item['desc']}")
            lines.append("")
    return "\n".join(lines)


def get_ai_chat_response(user_message, destination='', days=1, travelers=1, budget=0, history=None):
    """
    Main AI chat coordinator. Generates accurate, tailored advice for trip planning,
    ordering of sights, chill spots, birthday parties, traveler personas (nature lover,
    temple pilgrim, family/friends, adventure), and transit hub ATMs.
    ALWAYS names exact spots and locations.
    """
    query = (user_message or '').strip()
    query_lower = query.lower()
    dest_clean = (destination or 'Gujarat').strip()
    dest_lower = dest_clean.lower()
    
    # Check if user mentioned a specific destination or keyword in their prompt
    for alias_key, target_key in DESTINATION_ALIASES.items():
        if alias_key in query_lower:
            dest_lower = target_key
            dest_clean = CURATED_DESTINATIONS.get(target_key, {}).get('name', target_key.title())
            break
            
    # Also check if destination matches an alias
    matched_key = DESTINATION_ALIASES.get(dest_lower, None)
    if not matched_key:
        for alias_key, target_key in DESTINATION_ALIASES.items():
            if alias_key in dest_lower or dest_lower in alias_key:
                matched_key = target_key
                break

    matched_profile = CURATED_DESTINATIONS.get(matched_key) if matched_key else None
    dest_title = dest_clean.title()

    # Try Gemini LLM first if configured
    system_instruction = (
        "You are TripTics AI, a friendly travel concierge and trip coordinator. "
        "CRITICAL LANGUAGE RULE: Always write in SIMPLE, CLEAR, EVERYDAY ENGLISH that any tourist can easily understand. "
        "Do NOT use complex, flowery, academic, or high-level vocabulary (avoid words like 'gastronomy', 'fauna', 'panoramic vistas', 'gushing cataracts', 'indigenous artisans', 'sanctum sanctorum', 'resilience', 'venerated'). "
        "Use simple everyday words like 'temple', 'animals', 'tasty local food', 'lunch', 'dinner', 'nice sunset view', 'waterfall', 'shopping', 'fun rides'. "
        "CRITICAL CONTENT RULE: When asked for places to visit, chill spots, birthday party spots, or itineraries, "
        "you MUST ALWAYS provide SPECIFIC, REAL, NAMED VENUES AND EXACT REAL LOCATIONS. "
        "NEVER invent fake landmarks or generic 'Clock Tower' locations. "
        "If asked about waterfalls, answer ONLY about waterfalls and cascades; if asked about temples, answer ONLY about temples. "
        "If asked about ATMs, name exact ATMs near Railway Stations, Bus Stands, and Airports. Do not include room prices."
    )
    
    context_prompt = f"""User Trip Context:
- Target Destination: {dest_clean}
- Duration: {days} Days
- Travelers: {travelers} People
- Budget: ₹{budget}

User Question:
{query}

Please provide an actionable, highly helpful, and well-structured response addressing their exact needs with REAL NAMED SPOTS."""

    gemini_reply = _call_gemini_if_configured(context_prompt, system_instruction)
    if gemini_reply:
        suggestions = [
            f"Where should I go first in {dest_clean}?",
            f"Plan an efficient {days}-day trip covering all temples & fun zones",
            f"Nature lover spots & rolling farm fields in {dest_clean}",
            f"Where are the nearest ATMs to the railway station in {dest_clean}?"
        ]
        return {
            'reply': gemini_reply,
            'destination': dest_clean,
            'suggestions': suggestions
        }

    # ── Expert Local Knowledge Engine ─────────────────────────────────────────
    reply_parts = []
    guide = get_destination_master_guide(dest_clean, days=days)
    
    # ── Safe Word-Boundary Intent Detection ──
    # Waterfalls intent: Check for waterfalls first or specific waterfall names
    is_waterfalls = bool(re.search(r'\b(waterfalls?|cascades?|plunge pools?|falls?)\b', query_lower)) or any(k in query_lower for k in [
        'devarapalli', 'lothapalli', 'lothugedda', 'katiki', 'chaparai', 'kothapalli', 'thatipudi', 'talakona', 'kapila theertham', 'kailasakona', 'tada falls', 'dudhsagar', 'harvalem', 'arvalem', 'bubbly lake', 'savari'
    ])

    # Trekking & Adventure intent
    is_trekking = bool(re.search(r'\b(treks?|trekking|trecking|hiking|hikes?|wildlife|safari|outdoor activities|outdoor adventure|canopy walk|climbing|kayaking|scuba)\b', query_lower)) or any(k in query_lower for k in [
        'kambalakonda', 'dolphin\'s nose', 'srivari mettu', 'alipiri', 'silathoranam', 'lambasingi trek', 'devil\'s canyon'
    ])

    # Devotional / temples intent - MUST NOT match city names!
    # Explicitly excludes queries where the user specifically asked for waterfalls or trekking
    is_devotional = bool(re.search(r'\b(temples?|devotional|pooja|puja|darshan|jyotirlinga|spiritual|pilgrims?|pilgrimage|shrines?|aartis?|mandir|kovil|devasthanam|sanctum)\b', query_lower)) and not is_waterfalls and not is_trekking

    # Culture & Festivals intent - MUST NOT match 'spiritual' or temples or waterfalls
    is_culture = bool(re.search(r'\b(culture|cultural|traditions?|traditional|festivals?|rituals?|customs|folklore|folk dance|garba|dhimsa)\b', query_lower)) and not is_devotional and not is_waterfalls

    is_atm = any(k in query_lower for k in [
        'atm', 'atms', 'cash', 'money', 'withdraw', 'station atm', 'bus stop atm', 'airport atm'
    ])

    is_party = any(k in query_lower for k in [
        'birthday', 'party', 'parties', 'celebrate', 'celebration', 'anniversary', 'campfire', 'bonfire', 'events', 'occasion'
    ])

    is_malls = any(k in query_lower for k in [
        'mall', 'malls', 'shopping', 'bazaar', 'market', 'buy', 'souvenir', 'handicraft', 'cloth', 'textile', 'onorbit', 'inorbit', 'cmr', 'chitralaya', 'central mall'
    ])

    is_dining = any(k in query_lower for k in [
        'dish', 'dishes', 'food', 'eat', 'dining', 'delicac', 'thali', 'restaurant', 'street food', 'cuisine', 'specialties'
    ])

    is_spots_list = any(k in query_lower for k in [
        'all spots', 'list of tourist', 'list of spots', 'visiting spots', 'all places', 'directory of', 'cover all places'
    ]) and not ('plan' in query_lower and ('day' in query_lower or 'itinerary' in query_lower))
    
    is_nature_lover = any(k in query_lower for k in [
        'nature lover', 'rolling through fields', 'farms', 'fields and farms', 'countryside', 'agro', 'tea estate', 'plantations', 'flora', 'lambasingi', 'kondakarla'
    ]) and not is_waterfalls and not is_trekking
    
    is_family_friends = any(k in query_lower for k in [
        'family', 'friends', 'trip with frnds', 'trip with friends', 'waterpark', 'water park', 'fun zone', 'amusement', 'kailasagiri', 'submarine museum'
    ]) and not is_waterfalls and not is_trekking
    
    is_where_first = any(k in query_lower for k in [
        'where to go first', 'where should i go first', 'what to do first', 'order', 'sequence',
        'first place', 'first spot', 'start', 'begin', 'morning'
    ])
    
    is_chill = any(k in query_lower for k in [
        'chill', 'relax', 'peaceful', 'quiet', 'scenic', 'scenic cafe', 'coffee overlook', 'hangout'
    ])
    
    # Explicit multi-day plan button or prompt
    is_button_cover_all = bool(re.search(r'plan an efficient \d+[\-– ]?day itinerary for .* covering all (famous )?temples', query_lower)) or 'cover all places' in query_lower
    is_explicit_multiday_plan = is_button_cover_all or (
        bool(re.search(r'\b(plan (an efficient )?\d+[\-– ]?day|\d+[\-– ]?day (master )?plan|\d+[\-– ]?day itinerary)\b', query_lower))
        and not (is_waterfalls or is_trekking or is_devotional or is_nature_lover or is_family_friends or is_atm or is_malls or is_dining or is_party or is_culture)
    )

    # 1. Explicit Multi-Day Plan requested (Only when user explicitly asks for overall full trip plan)
    if is_explicit_multiday_plan:
        reply_parts.append(_generate_comprehensive_multiday_itinerary(dest_clean, days, travelers, budget))

    # 2. Waterfalls & Adventure / Trekking (PRIORITIZED FOR PRECISE WATERFALL & TREK QUERIES)
    elif is_waterfalls or is_trekking:
        if is_waterfalls:
            reply_parts.append(_format_waterfalls_for_chatbot(dest_clean, guide, matched_profile))
        if is_trekking:
            reply_parts.append(_format_trekking_adventure_for_chatbot(dest_clean, guide, matched_profile))

    # 3. Devotional & Temple query (PRIORITIZED FOR SACRED SHRINES)
    elif is_devotional:
        reply_parts.append(_format_temples_for_chatbot(dest_clean, guide, matched_profile))

    # 4. Nature lover query
    elif is_nature_lover:
        reply_parts.append(_format_nature_farms_for_chatbot(dest_clean, guide, matched_profile))

    # 5. Family & Friends / Waterparks query
    elif is_family_friends:
        reply_parts.append(_format_family_fun_for_chatbot(dest_clean, guide, matched_profile))

    # 6. ATM query
    elif is_atm:
        reply_parts.append(_format_atms_for_chatbot(dest_clean))

    # 7. Birthday parties & Occasion Celebrations (with map-style landmark directions)
    elif is_party:
        reply_parts.append(_format_celebrations_with_landmarks(guide))

    # 8. Shopping Malls & Bazaars
    elif is_malls:
        reply_parts.append(_format_malls_for_chatbot(guide))

    # 9. Food & Dining
    elif is_dining:
        reply_parts.append(_format_dining_for_chatbot(guide))

    # 10. Culture & Festivals
    elif is_culture:
        reply_parts.append(_format_culture_for_chatbot(guide))

    # 11. Full Categorized Tourist Spots Directory
    elif is_spots_list:
        reply_parts.append(_format_all_tourist_spots(guide))

    # 12. Where to go first
    elif is_where_first:
        if matched_profile and 'where_first' in matched_profile:
            reply_parts.append(matched_profile['where_first'])
        else:
            reply_parts.append(f"### 📍 Where to Start First in {dest_title}\n* Start with the principal landmark or sacred temple early in the morning (08:00 AM) to beat midday traffic, followed by scenic afternoon viewpoints and evening promenade.")

    # 13. Chill spots
    elif is_chill:
        if matched_profile and 'chill_spots' in matched_profile:
            reply_parts.append(matched_profile['chill_spots'])
        else:
            reply_parts.append(f"### ☕ Chill & Relaxing Hangout Spots in {dest_title}\n* Lakeside promenades, scenic hill ridge cafes, and botanical gardens for quiet afternoon conversations.")

    # 14. Fallback if no specific category matched
    if not reply_parts:
        reply_parts.append(_generate_comprehensive_multiday_itinerary(dest_clean, days, travelers, budget))

    reply_text = "\n\n---\n\n".join(reply_parts)
    
    suggestions = [
        f"Where should I go first in {dest_clean}?",
        f"Nature lover spots & rolling fields in {dest_clean}",
        f"Temples & devotional darshan in {dest_clean}",
        f"Where are the nearest ATMs to the railway station or bus stop?"
    ]
    
    return {
        'reply': reply_text,
        'destination': dest_clean,
        'suggestions': suggestions
    }

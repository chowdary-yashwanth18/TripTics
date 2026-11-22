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
                "🚢 **INS Kursura Submarine Museum & TU-142 Aircraft Museum** (RK Beach): Real walk-through naval submarine and maritime reconnaissance bomber aircraft directly on the beach.",
                "🏄 **Rushikonda Beach Water Adventure Sports**: Jet-skiing, speedboats, banana rides, kayaking, and certified surfing school.",
                "⛲ **VMRDA City Central Park**: 22-acre urban botanical garden with musical dancing fountain and bonsai park."
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
    }
}

# Aliases
DESTINATION_ALIASES = {
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
    Generates a rich, highly efficient multi-day plan (3, 4, 5, or X days)
    that systematically covers ALL categories:
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
        f"### 🗺️ Comprehensive {days_count}-Day Master Plan for {dest_title}",
        f"**Balanced Route Covering:** 🛕 Temples • 🌄 Scenic Viewpoints • 🌊 Waterfalls • 🥾 Trekking • 🦁 Zoo & Wildlife • 🌺 Botanical Gardens & Farms • 🎢 Waterparks & Fun Zones\n",
        f"*This itinerary is logically sequenced by time and geography to eliminate traffic delays and beat peak midday temperatures:*\n"
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
                t1 = temples[0] if temples else "Iconic Historic Temple"
                b1 = botanical[0] if botanical else "Central Botanical Park"
                v1 = views[0] if views else "Scenic Sunset Viewpoint"
                lines.append(f"* **🌅 Morning (08:30 AM – 11:30 AM): Spiritual Heritage & Sacred Darshan**")
                lines.append(f"  * {t1} — Start early when queues are short and morning aarti ambiance is peaceful.")
                lines.append(f"* **🍽️ Midday & Lunch (12:00 PM – 02:30 PM): Authentic Regional Thali & Culture**")
                lines.append(f"  * Move indoors to the heritage center to savor authentic regional cuisine and browse indigenous artisan handicrafts.")
                lines.append(f"* **🌺 Afternoon (03:00 PM – 04:30 PM): Botanical Gardens & Shaded Walks**")
                lines.append(f"  * {b1} — Peaceful stroll through exotic plant nurseries and flowerbeds.")
                lines.append(f"* **🌇 Sunset & Evening (05:00 PM – 07:30 PM): Panoramic Vistas & Waterfront Chill**")
                lines.append(f"  * {v1} — Unwind during golden hour with soothing evening breezes and panoramic views.")
                lines.append(f"* **🌙 Night (08:00 PM onwards): Leisure Dining & Celebration Deck**")
                lines.append(f"  * Group dinner at a rooftop garden restaurant with live music.")

            elif d == 2:
                f1 = falls[0] if falls else "Cascading Waterfalls"
                tr1 = treks[0] if treks else "Nature Forest Trail"
                v2 = views[1] if len(views) > 1 else (views[0] if views else "Hill Ridge")
                lines.append(f"* **🌄 Morning (08:00 AM – 12:30 PM): Gushing Waterfalls & Mountain Adventure**")
                lines.append(f"  * {f1} — Experience the cascading falls in the fresh morning air; dip feet in natural rock pools.")
                lines.append(f"* **🥾 Midday Adventure (12:30 PM – 02:30 PM): Trekking Trail & Shaded Picnic**")
                lines.append(f"  * {tr1} — Hike through forested canopies followed by authentic regional lunch.")
                lines.append(f"* **☕ Late Afternoon (03:30 PM – 05:30 PM): Hill Station Ridge & Coffee/Tea Overlook**")
                lines.append(f"  * {v2} — Savor freshly brewed local coffee/tea looking out over rolling mountain ridges.")
                lines.append(f"* **🔥 Evening & Campfire (06:30 PM – 09:30 PM): Resort Lawn Celebration**")
                lines.append(f"  * Open-air campfire, live barbecue, music, and stargazing.")

            elif d == 3:
                w1 = wildlife[0] if wildlife else "National Wildlife Park"
                b2 = botanical[1] if len(botanical) > 1 else (botanical[0] if botanical else "Agro-Farms")
                lines.append(f"* **🦁 Dawn Safari (06:00 AM – 09:30 AM): Wildlife Sanctuary & Zoological Park**")
                lines.append(f"  * {w1} — Early morning safari slot when lions, tigers, deer, and birds are active near waterholes.")
                lines.append(f"* **🌾 Midday & Afternoon (11:00 AM – 03:00 PM): Rolling Green Farms & Countryside Agro-Tour**")
                lines.append(f"  * {b2} — Walk through rolling farm fields, organic fruit orchards, and pastoral countryside.")
                lines.append(f"* **🏛️ Sunset Culture (04:30 PM – 07:00 PM): Ancient Stepwells or Fort Heritage**")
                lines.append(f"  * Explore centuries-old architecture and watch the illuminated heritage monuments at dusk.")

            elif d == 4:
                fn1 = fun[0] if fun else "Premier Theme & Waterpark"
                fn2 = fun[1] if len(fun) > 1 else "Fun Zone & Lakefront"
                lines.append(f"* **🎢 Morning to Mid-Afternoon (10:00 AM – 03:30 PM): Waterparks & High-Energy Fun Zones**")
                lines.append(f"  * {fn1} — Thrilling wave pools, spiral water slides, rain dance, and adventure rides.")
                lines.append(f"* **🎡 Late Afternoon (04:00 PM – 06:30 PM): Interactive Science, IMAX & Lake Rides**")
                lines.append(f"  * {fn2} — Toy train, speed-boating, or immersive exhibits.")
                lines.append(f"* **🌆 Night (07:30 PM onwards): Celebratory Rooftop Lounge & Party Cabanas**")
                lines.append(f"  * Reserve a private celebration terrace for gourmet platters and signature drinks.")

            elif d == 5:
                t2 = temples[1] if len(temples) > 1 else "Sacred Confluence Shrine"
                v3 = views[2] if len(views) > 2 else "Lakeside Sunset Point"
                lines.append(f"* **🛕 Morning (08:30 AM – 11:30 AM): Sacred Shrine & Architectural Wonder**")
                lines.append(f"  * {t2} — Peaceful morning prayers and architectural exploration.")
                lines.append(f"* **🛍️ Afternoon (01:00 PM – 04:00 PM): Handloom Textiles & Craft Emporiums**")
                lines.append(f"  * Pick up authentic regional fabrics, handicrafts, spices, and keepsakes directly from artisan clusters.")
                lines.append(f"* **🌅 Sunset Golden Hour (05:00 PM – 07:30 PM): Farewell Scenic Overlook**")
                lines.append(f"  * {v3} — Commemorative group photography and sunset reflection.")
            else:
                lines.append(f"* **🌿 Day {d} Leisure Exploration:**")
                lines.append(f"  * Off-the-beaten-path village excursions, secluded nature trails, and slow cafe conversations.")
            lines.append("")
    else:
        # Dynamic generic fallback with categorized spots
        from utils.hotel_generator import generate_hotels
        hotels = generate_hotels(dest_clean) or [{'name': f'{dest_title} Heritage Stay', 'address': f'Central {dest_title}'}]
        h1 = hotels[0]
        
        for d in range(1, days_count + 1):
            lines.append(f"#### 📅 Day {d}:")
            if d == 1:
                lines.append(f"* **🛕 Morning (08:30 AM – 11:30 AM): Signature Sacred Temples & Historic Shrines**")
                lines.append(f"  * Visit the principal historic temple or monument in {dest_title} before midday heat.")
                lines.append(f"* **🍽️ Midday (12:00 PM – 02:30 PM): Heritage Gastronomy near {h1['name']}**")
                lines.append(f"  * Savor authentic local delicacies and browse traditional craft bazars.")
                lines.append(f"* **🌄 Sunset (04:30 PM – 06:30 PM): Panoramic Viewpoint & Lakefront Chill**")
                lines.append(f"  * Watch golden hour reflections with gentle evening breezes.")
            elif d == 2:
                lines.append(f"* **🌊 Morning (08:30 AM – 12:30 PM): Cascading Waterfalls, Nature Trails & Hill Stations**")
                lines.append(f"  * Explore lush waterfalls or scenic mountain roads just outside the city center.")
                lines.append(f"* **🌾 Afternoon (02:00 PM – 04:30 PM): Countryside Farms & Botanical Gardens**")
                lines.append(f"  * Stroll through landscaped gardens and rolling agricultural fields.")
                lines.append(f"* **🔥 Evening (06:00 PM onwards): Campfire BBQ & Leisure Celebration**")
            elif d == 3:
                lines.append(f"* **🦁 Morning (08:00 AM – 11:30 AM): Zoological Garden or Wildlife Sanctuary**")
                lines.append(f"  * Discover regional fauna, deer parks, and bird sanctuaries.")
                lines.append(f"* **🥾 Afternoon (02:00 PM – 05:00 PM): Trekking Trails or Cave Exploration**")
            elif d == 4:
                lines.append(f"* **🎢 Full Day (10:00 AM – 05:00 PM): Waterparks, Theme Parks & Family Fun Zones**")
                lines.append(f"  * Spend the day on water slides, wave pools, and adventure sports.")
            else:
                lines.append(f"* **🛍️ Day {d}: Cultural Villages, Handloom Shopping & Farewell Viewpoint**")
            lines.append("")

    return "\n".join(lines)


def _format_waterfalls_for_chatbot(destination, guide=None, profile=None):
    """Formats verified waterfalls and natural cascades for the destination."""
    dest_title = (destination or 'Your Destination').title()
    
    # 1. If curated waterfalls_specific exists in profile, use it
    if profile and profile.get('waterfalls_specific'):
        return profile['waterfalls_specific']
        
    # 2. Or if guide has curated waterfalls
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
        
    # 3. Or if profile has categories.waterfalls
    if profile and profile.get('categories', {}).get('waterfalls'):
        falls = profile['categories']['waterfalls']
        lines = [
            f"### 🌊 Spectacular Waterfalls in & around {dest_title}\n",
            f"Here are verified waterfalls situated in and around **{dest_title}**:\n"
        ]
        for f in falls:
            lines.append(f"* {f}\n")
        return "\n".join(lines)
        
    # 4. Fallback generic waterfalls
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
  * 🙏 **Significance:** Premier Shakti Peeth where the heart of Goddess Sati is believed to have fallen; worshiped through the sacred Viso Yantra."""
}


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
        
    temples = (guide or {}).get('tourist_spots', {}).get('temples', [])
    lines = [f"### 🛕 Most Famous & Visited Temples in & around {dest_title}\n"]
    if temples:
        for idx, t in enumerate(temples[:5], 1):
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

* **1. 🛕 Historic Presiding City Shrine:**
  * 📍 **Location:** Central Heritage District of {dest_title}.
  * ⏰ **Darshan Timings:** 06:30 AM – 11:30 AM & 05:30 PM – 08:30 PM.
  * 🙏 **Sacred Significance:** Ancient sanctum renowned for morning aarti, peaceful architecture, and devotional darshan.
* **2. 🛕 Hilltop Pilgrimage & Panoramic View Shrine:**
  * 📍 **Location:** Scenic hilltop overlook (~15–30 mins from city center).
  * ⏰ **Darshan Timings:** 07:00 AM – 06:00 PM.
  * 🙏 **Sacred Significance:** Sacred hill deity where devotees perform traditional pradakshina and enjoy peaceful valley vistas."""


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
        "You are TripTics AI, an expert travel concierge and trip coordinator. "
        "CRITICAL INSTRUCTION: When asked for places to visit, chill spots, birthday celebration venues, "
        "or multi-day itineraries, you MUST ALWAYS provide SPECIFIC, REAL, NAMED VENUES AND EXACT LOCATIONS (e.g., 'Whistling Meadows Resort & Club, Sanand-Bopal Road, Ahmedabad', "
        "'Makeba The Lounge Cafe, SG Highway', 'Rann Utsav Luxury Tent City, Dhordo', 'Sabarmati Riverfront Promenade'). "
        "Cover temples, waterfalls, hill stations, viewpoints, trekking trails, zoos/wildlife, botanical gardens/farms, and waterparks/fun zones. "
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
    # Devotional / temples intent - prioritized to prevent culture/general hijacking
    is_devotional = bool(re.search(r'\b(temple|temples|devotional|pooja|puja|darshan|jyotirlinga|spiritual|pilgrim|pilgrimage|shrine|shrines|aarti|simhachalam|annavaram|shrikalahasti|srikalahasti|tirupati|tirumala)\b', query_lower))

    # Culture & Festivals intent - MUST NOT match 'spiritual' or temples
    is_culture = bool(re.search(r'\b(culture|cultural|traditions?|traditional|festivals?|rituals?|customs|folklore|folk dance|garba|dhimsa)\b', query_lower)) and not is_devotional

    is_atm = any(k in query_lower for k in [
        'atm', 'atms', 'cash', 'money', 'withdraw', 'station atm', 'bus stop atm', 'airport atm'
    ])

    is_party = any(k in query_lower for k in [
        'birthday', 'party', 'parties', 'celebrate', 'celebration', 'anniversary', 'campfire', 'bonfire', 'events', 'occasion'
    ])

    is_malls = any(k in query_lower for k in [
        'mall', 'malls', 'shopping', 'bazaar', 'market', 'buy', 'souvenir', 'handicraft', 'cloth', 'textile'
    ])

    is_dining = any(k in query_lower for k in [
        'dish', 'dishes', 'food', 'eat', 'dining', 'delicac', 'thali', 'restaurant', 'street food', 'cuisine', 'specialties'
    ])

    is_spots_list = any(k in query_lower for k in [
        'all spots', 'list of tourist', 'list of spots', 'visiting spots', 'all places', 'directory of', 'cover all places'
    ]) and not ('plan' in query_lower and ('day' in query_lower or 'itinerary' in query_lower))
    
    is_waterfalls = any(k in query_lower for k in [
        'waterfall', 'waterfalls', 'cascade', 'cascades', 'devarapalli', 'lothapalli', 'lothugedda', 'katiki', 'chaparai', 'kothapalli', 'thatipudi', 'plunge pool'
    ])

    is_trekking = any(k in query_lower for k in [
        'trek', 'treks', 'trekking', 'trecking', 'hike', 'hiking', 'wildlife', 'safari', 'outdoor activities', 'kambalakonda', 'dolphin\'s nose', 'adventure'
    ])
    
    is_nature_lover = any(k in query_lower for k in [
        'nature lover', 'rolling through fields', 'farms', 'fields and farms', 'countryside', 'agro', 'tea estate', 'plantations', 'flora', 'lambasingi', 'kondakarla'
    ])
    
    is_family_friends = any(k in query_lower for k in [
        'family', 'friends', 'trip with frnds', 'trip with friends', 'waterpark', 'water park', 'fun zone', 'amusement', 'kailasagiri', 'submarine museum'
    ])
    
    is_where_first = any(k in query_lower for k in [
        'where to go first', 'where should i go first', 'what to do first', 'order', 'sequence',
        'first place', 'first spot', 'start', 'begin', 'morning'
    ])
    
    is_chill = any(k in query_lower for k in [
        'chill', 'relax', 'peaceful', 'quiet', 'scenic', 'scenic cafe', 'coffee overlook', 'hangout'
    ])
    
    is_explicit_multiday_plan = bool(re.search(r'plan (an efficient )?\d+[\-– ]?day|\d+[\-– ]?day (master )?plan|\d+[\-– ]?day itinerary|cover all places', query_lower))

    # 1. Explicit Multi-Day Plan requested
    if is_explicit_multiday_plan:
        reply_parts.append(_generate_comprehensive_multiday_itinerary(dest_clean, days, travelers, budget))

    # 2. Devotional & Temple query (PRIORITIZED FOR FAMOUS SACRED SHRINES)
    elif is_devotional:
        reply_parts.append(_format_temples_for_chatbot(dest_clean, guide, matched_profile))

    # 3. Waterfalls & Adventure / Trekking:
    # When user asks about waterfalls (or clicks Adventure, Waterfalls & Treks):
    # GIVE WATERFALLS FIRST!
    elif is_waterfalls or is_trekking:
        if is_waterfalls:
            reply_parts.append(_format_waterfalls_for_chatbot(dest_clean, guide, matched_profile))
        if is_trekking:
            reply_parts.append(_format_trekking_adventure_for_chatbot(dest_clean, guide, matched_profile))

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

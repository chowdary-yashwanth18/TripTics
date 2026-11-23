# ============================================================
# utils/destination_guide.py – Master Destination Route Guide
# ============================================================
"""
Provides a comprehensive destination master guide for any travel location:
1. Complete Route Map & Geographic Sequencing
2. Categorized Visiting Spots (Temples, Hills, Waterfalls, Parks, Zoos, Malls, Fun Zones)
3. Night Stays & Lodges (Resorts, nature retreats, family stays with phones & booking)
4. Dining & Best Dishes to Try (Signature dishes, food street lanes, heritage eateries)
5. Tradition, Culture, Festivals & Rituals (Customs, dances, sacred rituals)
6. Birthday & Occasion Venues with Exact Landmark Map Directions (e.g. 'Near Inorbit Mall across Beach Road')
7. Nearby Transit ATMs (Railway, Bus Stand, Airport)
8. Enthusiastic, Entertaining & Efficient Day-by-Day Master Plan tailored to user's days
"""

import os
import urllib.parse
from utils.atm_service import get_nearby_atms
from utils.hotel_generator import generate_hotels

# ==============================================================================
# DEEP DOMAIN KNOWLEDGE REGISTRY FOR POPULAR DESTINATIONS
# ==============================================================================
DESTINATION_MASTER_REGISTRY = {
    # ── GUJARAT (Ahmedabad, Kutch, Sasan Gir, Kevadia, Vadodara, Surat) ────────
    'gujarat': {
        'title': 'Gujarat, India',
        'tagline': 'Land of Vibrant Heritage, White Deserts, Wild Lions & Grand Celebrations',
        'map_query': 'Gujarat, India',

        'tourist_spots': {
            'temples': [
                {
                    'name': 'Somnath Jyotirlinga Temple',
                    'landmark': 'Prabhas Patan, Veraval coast (overlooking Arabian Sea waves)',
                    'desc': 'The first of the twelve sacred Shiva Jyotirlingas. Majestic Chalukya-style architecture with evening sound-and-light narration.',
                    'timing': '06:00 AM – 09:30 PM (Aarti at 07:00 AM, 12:00 PM, 07:00 PM)'
                },
                {
                    'name': 'Dwarkadhish Temple (Jagat Mandir)',
                    'landmark': 'Gomti Creek confluence, Dwarka (near Dwarka Beach)',
                    'desc': '2,200-year-old 5-story sanctum dedicated to Lord Krishna with a towering 78m spire and the sacred 52-yard flag ceremony.',
                    'timing': '06:30 AM – 01:00 PM & 05:00 PM – 09:30 PM'
                },
                {
                    'name': 'Akshardham Cultural Complex',
                    'landmark': 'Sector 20, ' 'Gandhinagar Highway (opposite Secretariat Grounds)',
                    'desc': 'Stunning pink sandstone carvings, tranquil prayer halls, and the evening "Sat-Chit-Anand" water and laser fountain show.',
                    'timing': '09:30 AM – 07:30 PM (Closed Mondays)'
                },
                {
                    'name': 'Sun Temple Modhera',
                    'landmark': 'Becharaji Highway, Modhera, Mehsana district',
                    'desc': '11th-century Solanki architectural marvel designed so equinox sun rays illuminate the deity; features the 108-shrine stepped Surya Kund.',
                    'timing': '07:00 AM – 06:00 PM'
                },
                {
                    'name': 'Hutheesing Jain Temple',
                    'landmark': 'Shahibaug Road, Bardolpura, Ahmedabad (near Delhi Darwaja)',
                    'desc': '1848 white marble architectural masterpiece with 52 intricately carved devotional shrines in an open courtyard.',
                    'timing': '08:00 AM – 05:00 PM'
                }
            ],
            'hills_viewpoints': [
                {
                    'name': "Saputara Hill Station & Sunrise Point",
                    'landmark': 'Governor Hill Road, Saputara, Dang (Sahyadri mountain range)',
                    'desc': "Gujarat's premier hill station at 3,000 ft with pine valleys, cool mountain mist, ropeway cable cars, and tranquil sunset views.",
                    'highlight': 'Cable car ropeway, misty valleys, paragliding'
                },
                {
                    'name': 'Girnar Summit & Passenger Ropeway',
                    'landmark': 'Bhavnath Taleti, Junagadh (Asia’s longest ropeway)',
                    'desc': 'Ascends 2,800 ft over dramatic rocky ridges to ancient Hindu and Jain mountaintop shrines.',
                    'highlight': 'Panoramic valley views, 10-minute ropeway ride'
                },
                {
                    'name': 'Kala Dungar (Black Hill)',
                    'landmark': 'Khavda Road, Great Rann of Kutch (highest point in Kutch at 462m)',
                    'desc': 'Unbroken 360° panoramic horizon over the white salt desert and Indo-Pak border; wild jackal feeding ritual at 400-year-old temple.',
                    'highlight': 'Spectacular golden hour sunset over salt crust'
                }
            ],
            'waterfalls': [
                {
                    'name': 'Gira Waterfalls',
                    'landmark': 'Waghai-Saputara Road, Ambika River, Dang district',
                    'desc': '30-meter high thundering cascade tumbling into the Ambika River, framed by dense bamboo and teak forests.',
                    'highlight': 'Forest trails, natural spray, tea stalls'
                },
                {
                    'name': 'Zarwani Waterfalls',
                    'landmark': 'Shoolpaneshwar Wildlife Sanctuary, 28 km from Statue of Unity, Kevadia',
                    'desc': 'Lush deep-forest waterfall with natural freshwater plunge pools and eco-campsite.',
                    'highlight': 'Stream walking, bird watching, nature trek'
                },
                {
                    'name': 'Hathni Mata Waterfall',
                    'landmark': 'Pojar, Jambughoda Wildlife Sanctuary, Panchmahal district',
                    'desc': '100-meter drop scenic waterfall nestled in green cliffs with an ancient rock cave shrine.',
                    'highlight': 'Monsoon green valley, rocky streams'
                }
            ],
            'parks_botanical': [
                {
                    'name': 'Sabarmati Riverfront Flower Park',
                    'landmark': 'Between Ellis Bridge & Sardar Bridge, Riverfront West, Ahmedabad',
                    'desc': 'Sprawling landscaped floral exhibition park along the breeze-filled Sabarmati River with seasonal blooms, manicured lawns, and benches.',
                    'highlight': 'Evening river strolls, floral photography'
                },
                {
                    'name': 'Waghai Botanical Garden & Bio-Diversity Center',
                    'landmark': 'Waghai, Dang (en route to Saputara)',
                    'desc': '24-hectare state botanical sanctuary preserving 1,400+ native plants, bamboo arboretum, cacti greenhouse, and medicinal herb garden.',
                    'highlight': 'Educational tree trail, wooden gazebos'
                },
                {
                    'name': 'Indroda Dinosaur and Fossil Park',
                    'landmark': 'Sabarmati Riverbank, Sector 7, Gandhinagar',
                    'desc': "Known as 'India's Jurassic Park', housing fossilized dinosaur eggs, life-size dinosaur models, wilderness botanical garden, and zoo.",
                    'highlight': 'Fossil museum, botanical wilderness walk'
                }
            ],
            'zoo_wildlife': [
                {
                    'name': 'Sasan Gir National Park (Asiatic Lion Safari)',
                    'landmark': 'Hiran Riverbank, Sasan Gir, Junagadh District',
                    'desc': 'The world’s only natural sanctuary for the Asiatic Lion. 06:00 AM and 03:00 PM open-top Gypsy safaris spot lions, leopards, and chital.',
                    'highlight': 'Wild Asiatic Lion tracking, marsh crocodiles'
                },
                {
                    'name': 'Wild Ass Sanctuary (Little Rann of Kutch)',
                    'landmark': 'Bajana / Dhrangadhra entry points, Little Rann of Kutch',
                    'desc': '4,953 sq km saline mudflat desert protecting the rare endangered Indian Wild Ass (Khur), desert foxes, and flamingos.',
                    'highlight': 'Desert 4x4 safaris, salt pan communities'
                },
                {
                    'name': 'Kamla Nehru Zoological Garden',
                    'landmark': 'Kankaria Lakefront South Gate, Maninagar, Ahmedabad',
                    'desc': '117-acre historic zoo sheltering rare albino birds, Bengal tigers, Asiatic leopards, and an expansive nocturnal house.',
                    'highlight': 'Lakeside zoo path, butterfly park'
                }
            ],
            'shopping_malls': [
                {
                    'name': 'Ahmedabad One Mall (Alpha One)',
                    'landmark': 'Vastrapur Lake Road, Vastrapur, Ahmedabad',
                    'desc': 'Premier 1.2 million sq ft shopping mall featuring 200+ international & domestic brands, Cinepolis IMAX, and multi-cuisine food court.',
                    'highlight': 'Luxury retail, dining, family gaming'
                },
                {
                    'name': 'Palladium Ahmedabad',
                    'landmark': 'Thaltej, SG Highway, Ahmedabad (near Sarkhej-Gandhinagar Crossing)',
                    'desc': 'Gujarat’s ultra-luxury lifestyle destination housing premium fashion brands, gourmet fine dining, and rooftop bars.',
                    'highlight': 'High-end designer shopping, aesthetic cafes'
                },
                {
                    'name': 'Law Garden Night Handicraft Market',
                    'landmark': 'Netaji Road, Ellisbridge, Ahmedabad (opposite Law Garden Park)',
                    'desc': 'Famous open-air evening bazaar packed with traditional mirror-work Chaniya Cholis, Bandhani dupattas, Mojris, and antique Kutchi jewelry.',
                    'highlight': 'Bargain ethnic fashion, street food'
                },
                {
                    'name': 'Dhalgarwad Traditional Textile Market',
                    'landmark': 'Old City, Khadia, Ahmedabad (near Teen Darwaja)',
                    'desc': 'Centuries-old textile bazaar for authentic Patola silk sarees, block-printed cotton dress materials, and wedding trousseau.',
                    'highlight': 'Wholesale authentic Gujarati fabrics'
                }
            ],
            'fun_zones_waterparks': [
                {
                    'name': 'Shankus Water Park & Resort',
                    'landmark': 'Ahmedabad-Mehsana Highway, Amipura, Mehsana',
                    'desc': 'Sprawling water resort featuring colossal tsunami wave pools, spiral thrill slides, toddler splash zones, and lazy rivers.',
                    'highlight': 'High-speed speed slides, rain dance floor'
                },
                {
                    'name': 'Gujarat Science City',
                    'landmark': 'Science City Road, Sola, Ahmedabad (off SG Highway)',
                    'desc': 'World-class interactive entertainment hub with India’s largest Aquatic Gallery shark tunnel, Robotic Gallery, and IMAX 3D Theatre.',
                    'highlight': 'Dancing humanoid robots, deep-sea walk'
                },
                {
                    'name': 'Kankaria Lakefront Adventure World',
                    'landmark': 'Kankaria Lake Circular Promenade, Maninagar, Ahmedabad',
                    'desc': 'Entertainment hub with the Atal Express toy train, tethered hot air balloon (Ahmedabad Eye), speedboats, and Segway rides.',
                    'highlight': 'Lakeside rides, musical fountain show'
                }
            ]
        },

        'dining_cuisine': {
            'must_try_dishes': [
                {
                    'name': 'Authentic Gujarati Thali',
                    'type': 'Vegetarian',
                    'desc': 'A royal spread featuring sweet & tangy Gujarati Kadhai Dal, Undhiyu, Sev Tameta, fresh Phulkas, Rotla with jaggery and white butter, accompanied by Shrikhand, Basundi, and Chaas.',
                    'best_at': 'Agashiye Heritage Rooftop (House of MG, Lal Darwaja) & Gordhan Thal (SG Highway)'
                },
                {
                    'name': 'Khamand Dhokla & Khandvi',
                    'type': 'Vegetarian',
                    'desc': 'Steamed spongy gram flour cakes tempered with mustard seeds and green chilies, served with melt-in-mouth spiced gram rolls topped with grated coconut.',
                    'best_at': 'Das Khaman (Nehrunagar Circle) & Lijjat Khaman (Kankaria)'
                },
                {
                    'name': 'Surati Undhiyu & Puri',
                    'type': 'Vegetarian',
                    'desc': 'Slow-cooked winter stew of seasonal beans, purple yam (kand), baby brinjals, and fenugreek dumplings (methi muthia) cooked in earthen pots.',
                    'best_at': 'Sasumaa Gujarati Thali (Ring Road, Surat) & Chandravilas (Gandhi Road)'
                },
                {
                    'name': 'Fafda, Jalebi & Papaya Sambharo',
                    'type': 'Vegetarian Snack',
                    'desc': 'Crisp chickpea flour crackers paired with warm, saffron-soaked spiral jalebis and raw papaya mustard relish. The ultimate Gujarati morning breakfast!',
                    'best_at': 'Oshwal (Ashram Road) & Chandravilas (Old City, Ahmedabad)'
                },
                {
                    'name': 'Kathiyawadi Sev Dungri & Bajra No Rotlo',
                    'type': 'Vegetarian',
                    'desc': 'Fiery spiced curry made with spring onions and crisp gram sev, eaten with thick pearl-millet flatbread charred on clay tawa with garlic chutney.',
                    'best_at': 'Gopi Dining Hall (Pritamnagar) & Kathiyawadi Village (SG Highway)'
                }
            ],
            'famous_food_streets': [
                {
                    'name': 'Manek Chowk Night Food Street',
                    'landmark': 'Old City, Khadia, Ahmedabad (transforms from jewelry market to open-air foodie paradise at 09:00 PM)',
                    'specialties': 'Gwalior Dosa, Chocolate Cheese Sandwiches, Ashrafi Kulfi, Jalebi-Fafda, Pav Bhaji'
                },
                {
                    'name': 'Urban Chowk & Sindhu Bhavan Food Street',
                    'landmark': 'Sindhu Bhavan Marg, Bodakdev, Ahmedabad',
                    'specialties': 'Trendy food truck street with artisan pizzas, gourmet boba teas, Mexican tacos, and live acoustic music.'
                }
            ]
        },

        'culture_traditions': {
            'summary': 'Gujarat boasts a vibrant 5,000-year maritime and cultural lineage spanning the Indus Valley Civilization (Lothal/Dholavira) to Solanki dynasties and Gandhian non-violence. Famous for its warmth, entrepreneurial spirit, vegetarian culinary excellence, and vibrant craft heritage.',
            'festivals_rituals': [
                {
                    'name': 'Navratri Garba Mahotsav (September – October)',
                    'importance': "The world's longest 9-night dance festival. Millions dress in colorful mirror-work Chaniya Cholis and Kediyus, performing synchronized Garba and Dandiya Raas in massive open grounds under dazzling lights.",
                    'rituals': 'Maa Amba Aarti at midnight, fasting, and rhythmic clapping dance till dawn.'
                },
                {
                    'name': 'Rann Utsav (November – February)',
                    'importance': 'Cultural desert carnival held on the endless white salt desert of Dhordo, Kutch. Showcases Kutchi embroidery, camel safaris, stargazing, and folk music.',
                    'rituals': 'Full moon desert gatherings, Sufi folk concerts, and bonfire jam sessions.'
                },
                {
                    'name': 'International Kite Festival / Uttarayan (January 14)',
                    'importance': 'Skies across Ahmedabad, Surat, and Vadodara turn into a riot of colors as millions fly kites from rooftops with traditional shouts of "Kai Po Che!".',
                    'rituals': 'Feasting on fresh Undhiyu, Chikki, and flying illuminated night lanterns (Tukkals).'
                }
            ],
            'art_crafts': 'Patan Patola double-ikat silk weaving, Bandhani tie-dye, Rogan fabric painting (Nirona, Kutch), and brass bell craftsmanship.'
        },

        'celebrations_venues': [
            {
                'name': 'Whistling Meadows Resort & Club',
                'map_landmark': 'Sanand-Bopal Road, 500m past Gala Gymkhana across the Sardar Patel Ring Road, Ahmedabad',
                'vibe': 'Expansive private lawns & poolside resort cabanas for grand birthday bashes and group anniversaries.',
                'features': 'Private party lawn, poolside deck, personal DJ sound system, bonfire setups, and customized catering.',
                'phone': '+91 79 2970 8888'
            },
            {
                'name': 'Makeba The Lounge Cafe & Rooftop',
                'map_landmark': '8th Floor, 315 Complex, SG Highway, directly opposite Grand Bhagwati, Bodakdev, Ahmedabad',
                'vibe': 'Chic high-energy open-air rooftop with panoramic city skyline lights and celebratory party cabanas.',
                'features': 'VIP celebration cabana, celebratory LED mood lighting, gourmet mocktail bar, and DJ acoustic nights.',
                'phone': '+91 99742 03315'
            },
            {
                'name': 'Rann Utsav Luxury Tent City',
                'map_landmark': 'Dhordo Village, 85 km North of Bhuj across the White Desert Gate, Great Rann of Kutch',
                'vibe': 'World-famous desert glamping under clear starlit skies with live folk music and private campfire circles.',
                'features': 'Private campfire circle, live Kutchi folk dancers, midnight cake cutting on the white salt crust, stargazing.',
                'phone': '+91 79 4004 8888'
            },
            {
                'name': 'The Fern Gir Forest Resort / Woods at Sasan',
                'map_landmark': 'Hiran Riverbank, Sasan-Talala Road, 2 km from Sinh Sadan Safari Gate, Sasan Gir',
                'vibe': 'Luxury riverfront wilderness resort nestled amidst dense teak forests with open-air celebration decks.',
                'features': 'Riverside party lawns, live campfire barbecue, forest lantern dining, and acoustic jamming.',
                'phone': '+91 2877 285 999'
            },
            {
                'name': 'Madhavan Beach Resort & Mandvi Shacks',
                'map_landmark': 'Windmill Beach Road, 3 km from historic Vijay Vilas Palace, Mandvi Coast, Kutch',
                'vibe': 'Private beachfront lawns overlooking Arabian Sea waves for birthday parties with beach bonfires.',
                'features': 'Beach bonfire pit, live coastal seafood/veg barbecue, fairy-lit cabanas, and ocean breeze.',
                'phone': '+91 98252 61288'
            }
        ]
    },

    # ── ARAKU VALLEY & VISAKHAPATNAM (Andhra Pradesh) ────────────────────────
    'araku': {
        'title': 'Araku Valley & Visakhapatnam, Andhra Pradesh',
        'tagline': 'Misty Mountain Gorges, Ancient Caves, Coffee Plantations & Bay of Bengal Shores',
        'map_query': 'Araku Valley, Andhra Pradesh',

        'tourist_spots': {
            'temples': [
                {
                    'name': 'Sri Varaha Lakshmi Narasimha Temple (Simhachalam)',
                    'landmark': 'Simhachalam Hilltop, 16 km from Vizag Railway Station (en route to Araku)',
                    'desc': '11th-century hill shrine where the deity remains covered in sacred sandalwood paste year-round, revealed only on Chandanotsavam.',
                    'timing': '07:00 AM – 04:00 PM & 06:00 PM – 09:00 PM'
                },
                {
                    'name': 'Matsyagundam Shiva Temple',
                    'landmark': 'Near Paderu, 45 km from Araku town (Machkund River)',
                    'desc': 'Sacred freshwater pool teeming with revered giant Mahseer fish that pilgrims feed by hand; protected by ancient tribal customs.',
                    'timing': '06:00 AM – 06:00 PM'
                },
                {
                    'name': 'Subterranean Shiva Lingam (Borra Caves)',
                    'landmark': 'Inside million-year-old Borra Caves, Ananthagiri Hills',
                    'desc': 'Naturally formed stalagmite Shiva Lingam nestled 80m deep inside limestone caverns with perennial natural mineral water drops.',
                    'timing': '09:00 AM – 05:00 PM'
                }
            ],
            'hills_viewpoints': [
                {
                    'name': 'Galikonda View Point',
                    'landmark': 'Visakhapatnam-Araku Highway, 15 km before Araku town',
                    'desc': 'Highest point in Visakhapatnam district at 3,800 ft offering 360° views over misty railway viaducts and cloud-carpeted valleys.',
                    'highlight': 'Uninterrupted sunrise/sunset views, roadside ginger tea'
                },
                {
                    'name': 'Lambasingi (Kashmir of Andhra Pradesh)',
                    'landmark': 'Chintapalli Mandal, 85 km from Araku',
                    'desc': 'High-altitude village famous for sub-zero winter temperatures, morning fog, pine groves, and seasonal yellow flower fields.',
                    'highlight': 'Susan garden flower fields, morning frost'
                },
                {
                    'name': 'Kailasagiri Hilltop Park',
                    'landmark': 'Perched atop 360 ft sea-facing cliff, Beach Road, Visakhapatnam',
                    'desc': 'Spectacular hill park accessed via cable ropeway, offering sweeping views of the Bay of Bengal coastline curve.',
                    'highlight': 'Ropeway ride, giant Shiva-Parvati statue, toy train'
                }
            ],
            'waterfalls': [
                {
                    'name': 'Katiki Waterfalls',
                    'landmark': '7 km from Borra Caves via 4x4 Jeep trail and Gosthani Riverbed',
                    'desc': 'A magnificent 50-ft natural cascade fed by perennial mountain streams; requires an adventurous 4x4 stream-crossing ride and short trek.',
                    'highlight': 'Natural plunge pool, roasted bamboo chicken stalls'
                },
                {
                    'name': 'Chaparai Water Cascades (Dumbriguda)',
                    'landmark': '15 km from Araku town towards Paderu',
                    'desc': 'Flat sloping smooth river rocks with cool crystal-clear water flowing gently; shaded by thick forest trees.',
                    'highlight': 'Rock water wading, forest picnic spots'
                },
                {
                    'name': 'Kothapalli Waterfalls',
                    'landmark': 'Near Gangaraju Madugula, 40 km from Paderu',
                    'desc': 'Picturesque multi-tiered cascading waterfalls surrounded by lush greenery, ideal for relaxing foot soaks.',
                    'highlight': 'Gentle cascades, scenic bamboo bridges'
                }
            ],
            'parks_botanical': [
                {
                    'name': 'Padmapuram Botanical Gardens',
                    'landmark': 'Padmapuram Junction, 2 km from Araku Bus Station',
                    'desc': 'Historic 1942 WWII nursery housing rare regional plants, hanging wooden treehouses, rose gardens, and a mini toy train.',
                    'highlight': 'Treehouse stays, garden toy train ride'
                },
                {
                    'name': 'Ananthagiri Arabica Coffee & Pepper Plantations',
                    'landmark': 'Ananthagiri Hills, along the Ghat Road',
                    'desc': 'Miles of shaded silver-oak forests draped with fragrant organic Arabica coffee shrubs and black pepper vines.',
                    'highlight': 'Coffee berry picking tours, cool mountain breezes'
                }
            ],
            'zoo_wildlife': [
                {
                    'name': 'Indira Gandhi Zoological Park',
                    'landmark': 'Kambalakonda Forest Reserve, National Highway 16, Visakhapatnam',
                    'desc': '625-acre natural forest zoological sanctuary housing tigers, white leopards, Asiatic lions, deer, and exotic aviary.',
                    'highlight': 'Safari battery cars, coastal wetland bird sanctuary'
                },
                {
                    'name': 'Tyda Jungle Bells Eco-Reserve',
                    'landmark': 'Tyda Eco-Forest, 35 km before Araku Valley',
                    'desc': 'Deciduous nature reserve maintained by AP Forest Department; home to barking deer, giant flying squirrels, and 100+ bird species.',
                    'highlight': 'Birdwatching trails, jungle wooden log cabins'
                }
            ],
            'shopping_malls': [
                {
                    'name': 'CMR Central & Inorbit Mall Commercial Belt',
                    'landmark': 'Maddilapalem & Gajuwaka Junction, Visakhapatnam',
                    'desc': 'Multi-level premier shopping destination featuring multiplex screens, major apparel brands, and international dining.',
                    'highlight': 'Shopping, cinema, kids entertainment zone'
                },
                {
                    'name': 'Araku Tribal Handicrafts & Spices Emporium',
                    'landmark': 'Main Road, Adjacent to Tribal Museum, Araku Valley',
                    'desc': 'Government-backed tribal outlet selling 100% authentic Araku Valley Arabica Coffee, pure forest wild honey, spices, and terracotta craft.',
                    'highlight': 'Fresh coffee powder, bamboo crafts, organic honey'
                }
            ],
            'fun_zones_waterparks': [
                {
                    'name': 'Rushikonda Beach Water Sports Zone',
                    'landmark': 'Rushikonda Beach, Marine Drive, Visakhapatnam',
                    'desc': 'Premier water adventure hub with jet-skiing, speedboats, banana rides, sea kayaking, and surfing instructors.',
                    'highlight': 'Jet ski rides, coastal ocean views'
                },
                {
                    'name': 'INS Kursura Submarine & TU-142 Aircraft Museum',
                    'landmark': 'RK Beach Road Promenade (opposite Victory at Sea Memorial), Visakhapatnam',
                    'desc': 'Real decommissioned Soviet-built submarine and maritime reconnaissance aircraft converted into walkthrough museums on the beach.',
                    'highlight': 'Walk inside real torpedo rooms and cockpits'
                }
            ]
        },

        'dining_cuisine': {
            'must_try_dishes': [
                {
                    'name': 'Araku Bamboo Chicken (Bongu Kodi)',
                    'type': 'Non-Vegetarian',
                    'desc': 'Tender chicken marinated in wild local ginger, garlic, green chilies, and forest spices, stuffed inside raw green bamboo stalks and charcoal-roasted with zero oil.',
                    'best_at': 'Local stalls near Chaparai Cascades & Borra Caves entrance'
                },
                {
                    'name': 'Bongu Biryani (Bamboo Steamed Biryani)',
                    'type': 'Non-Vegetarian',
                    'desc': 'Fragrant basmati rice and marinated meat steam-cooked inside bamboo over glowing wood embers, absorbing smoky herbal flavors.',
                    'best_at': 'Bamboo Chicken Point (Chaparai Road, Araku)'
                },
                {
                    'name': 'Madugula Halwa',
                    'type': 'Sweet Delicacy',
                    'desc': 'Legendary 130-year-old traditional sweet made from crushed wheat milk, pure cow ghee, and toasted cashews that melts on your tongue.',
                    'best_at': 'Dangeti Murthy Halwa (Madugula town en route)'
                },
                {
                    'name': 'Araku Valley Arabica Organic Coffee',
                    'type': 'Beverage',
                    'desc': 'Locally harvested high-altitude shade-grown Arabica coffee with rich aromatic notes of chocolate and caramel.',
                    'best_at': 'Araku Coffee Museum Cafe & Barista kiosks'
                }
            ],
            'famous_food_streets': [
                {
                    'name': 'RK Beach & YMCA Street Food Promenade',
                    'landmark': 'Beach Road, from Novotel to Submarine Museum, Visakhapatnam',
                    'specialties': 'Muri Mixture (Puffed rice beach chaat), piping hot Mirchi Bajji, grilled sweet corn, and tender coconuts.'
                }
            ]
        },

        'culture_traditions': {
            'summary': 'Araku Valley is home to 19 indigenous tribal communities including the Valmiki, Bagata, and Khond. The valley preserves ancient animist forest traditions, sustainable organic agro-practices, and vibrant musical festivities.',
            'festivals_rituals': [
                {
                    'name': 'Dhimsa Tribal Dance & Itika Pongal (March – April)',
                    'importance': 'Traditional folk dance where tribal men and women in colorful sarees form an interlinked chain dancing to the beats of Mori and Tudumu drums.',
                    'rituals': 'Sacred village forest deity worship and ceremonial Dhimsa community dances.'
                },
                {
                    'name': 'Visakha Utsav (December)',
                    'importance': 'Grand coastal festival organized along RK Beach celebrating Andhra culture, folk arts, music concerts, and flower shows.',
                    'rituals': 'Beach carnivals, traditional Kuchipudi dances, and artisanal craft exhibitions.'
                }
            ],
            'art_crafts': 'Terracotta tribal figurines, wooden combs, bamboo masks, and naturally hand-carved coffee wood artifacts.'
        },

        'celebrations_venues': [
            {
                'name': 'Novotel Visakhapatnam Varun Beach',
                'map_landmark': 'Beach Road, directly opposite RK Beach Submarine Museum Promenade, Visakhapatnam',
                'vibe': 'Ultra-luxury sea-facing rooftop lounge & grand celebration banquet hall for glamorous birthdays and anniversaries.',
                'features': 'Vue rooftop lounge, panoramic ocean sunset view, infinity poolside cabanas, and customized cake service.',
                'phone': '+91 891 304 5678'
            },
            {
                'name': 'The Park Visakhapatnam (Aqua & Vista Lawns)',
                'map_landmark': 'Beach Road, Pandurangapuram, 1 km south of Waltair Uplands, Visakhapatnam',
                'vibe': 'Chic private oceanfront lawns and poolside dining decks surrounded by tropical coconut groves.',
                'features': 'Private ocean lawn, DJ setup, open-air seafood barbecue, and candlelit cabanas.',
                'phone': '+91 891 304 5555'
            },
            {
                'name': 'Haritha Hill Resort & Mayuri Lawns',
                'map_landmark': 'Hilltop Road, 1 km from Araku Main Bus Station overlooking the valley, Araku',
                'vibe': 'Sprawling green valley lawns and private cottages for enthusiastic group birthday celebrations.',
                'features': 'Private celebration lawn, outdoor night campfire circle, live barbecue grill, and acoustic jamming.',
                'phone': '+91 8936 249 961'
            },
            {
                'name': 'Tyda Jungle Bells Campfire Deck',
                'map_landmark': 'Tyda Eco Forest, along the Ghat Road 35 km before Araku, Tyda',
                'vibe': 'Wilderness forest cabins with personal campfire pits for an adventurous squad night party.',
                'features': 'Bonfire circle, forest barbecue, starry sky acoustic jamming, and wooden cottage stay.',
                'phone': '+91 8936 249 970'
            }
        ]
    },

    # ── VISAKHAPATNAM (VIZAG, Andhra Pradesh) ─────────────────────────────────
    'visakhapatnam': {
        'title': 'Visakhapatnam (City of Destiny & Coastline), Andhra Pradesh',
        'tagline': 'Sun-Kissed Golden Beaches, Naval Heritage, Sacred Hilltop Shrines & Spectacular Cascades',
        'map_query': 'Visakhapatnam, Andhra Pradesh',

        'tourist_spots': {
            'temples': [
                {
                    'name': 'Sri Varaha Lakshmi Narasimha Temple (Simhachalam)',
                    'landmark': 'Simhachalam Hilltop, 16 km from Vizag Central Railway Station',
                    'desc': 'Revered 11th-century hill shrine where the deity remains enveloped in sacred sandalwood paste year-round, revealed only on Chandanotsavam.',
                    'timing': '07:00 AM – 04:00 PM & 06:00 PM – 09:00 PM',
                    'highlight': 'Famous Simhachalam Laddu prasadam, Appanna Swamy Chandanotsavam Nijaroopam'
                },
                {
                    'name': 'Sri Veera Venkata Satyanarayana Swamy Temple (Annavaram)',
                    'landmark': 'Ratnagiri Hilltop, Annavaram (~110 km from Vizag on NH-16 / direct train & express bus route)',
                    'desc': 'World-famous sacred hill shrine dedicated to Lord Satyanarayana Swamy. Millions of devotees visit to perform the sacred Satyanarayana Vratham for family prosperity and new beginnings.',
                    'timing': '06:00 AM – 12:30 PM & 01:00 PM – 09:00 PM (Continuous Vratham rituals 06:00 AM – 06:00 PM)',
                    'highlight': 'World-renowned authentic Annavaram Wheat Rava (Godhumai) Prasadam and divine Satyanarayana Vrathams'
                },
                {
                    'name': 'Sri Kanaka Mahalakshmi Temple',
                    'landmark': 'Burujupeta, Old Post Office area, Old Vizag City',
                    'desc': 'Ancient wish-fulfilling presiding goddess of Visakhapatnam; unique open-air sanctum without roof or doors, accessible 24/7.',
                    'timing': 'Open 24 Hours (Special Panchamrutha Abhishekam on Thursdays)'
                },
                {
                    'name': 'Sri Sampath Vinayagar Temple',
                    'landmark': 'Asilmetta Junction, near RTC Complex, Visakhapatnam',
                    'desc': 'Hugely popular Ganesha shrine where locals and travelers break coconuts for auspicious journeys and obstacle removal.',
                    'timing': '06:00 AM – 11:30 AM & 05:30 PM – 09:00 PM'
                },
                {
                    'name': 'Ross Hill Multifaith Mount',
                    'landmark': 'Port Area, overlooking Vizag Port Entrance & Harbor',
                    'desc': 'Unique tri-hill harmony site with Ross Hill Catholic Church on one crest, Dargah of Ishaq Madina on the second, and Sri Venkateswara Swamy Temple on the third.',
                    'timing': '06:00 AM – 06:30 PM'
                },
                {
                    'name': 'Bojjannakonda & Lingalakonda Buddhist Heritage Sites',
                    'landmark': 'Sankaram village, near Anakapalle (~35 km from Vizag center)',
                    'desc': '4th to 9th-century monolithic rock-cut Buddhist stupas, meditative caves, and rock-carved Buddha reliefs perched on twin hills.',
                    'timing': '09:00 AM – 05:00 PM'
                }
            ],
            'hills_viewpoints': [
                {
                    'name': 'Kailasagiri Hilltop Park & Ropeway',
                    'landmark': 'Perched atop 360 ft sea-facing cliff, Beach Road, Visakhapatnam',
                    'desc': 'Iconic hilltop landscaped park accessed via passenger ropeway with sweeping panoramic views of the Bay of Bengal coastline curve.',
                    'highlight': 'Cable ropeway ride, 40-ft Shiva-Parvathi statue, Titanic viewpoint deck, circular toy train'
                },
                {
                    'name': 'Dolphin\'s Nose Cliff & Lighthouse',
                    'landmark': 'Gangavaram port approach, 10 km south of Vizag city center',
                    'desc': 'Dramatic 358-meter rocky promontory projecting into the sea resembling a dolphin\'s snout, featuring a powerful coastal lighthouse.',
                    'highlight': 'Breathtaking 360-degree ocean views, historic harbor entrance overlook'
                },
                {
                    'name': 'Thotlakonda & Bavikonda Coastal Hill Plateaus',
                    'landmark': 'Bheemili Beach Road (Marine Drive), 15 km north of Vizag',
                    'desc': 'Ancient 2,000-year-old Hinayana Buddhist monastic complexes situated on elevated sea-facing green hill plateaus.',
                    'highlight': 'Unbroken ocean panoramas, ancient stone stupas, ocean breeze'
                },
                {
                    'name': 'Yarada Beach & Coastal Ghat Viewpoint',
                    'landmark': 'Behind Dolphin\'s Nose Hill, 15 km from Vizag center',
                    'desc': 'Secluded golden sandy cove flanked by banana plantations and steep verdant hills on three sides.',
                    'highlight': 'Scenic coastal hill descent, tranquil turquoise water'
                }
            ],
            'waterfalls': [
                {
                    'name': 'Devarapalli Waterfalls (Bahuda River Cascades)',
                    'landmark': 'Near Devarapalli village, ~55 km from Vizag center via Anandapuram / Sambhuvanipalem',
                    'desc': 'Splendid natural cascading waterfall where the Bahuda River tumbles over layered rock formations into crystal-clear freshwater pools.',
                    'highlight': 'Freshwater rock pool bathing, peaceful green valley picnic, scenic rural drive'
                },
                {
                    'name': 'Lothugedda / Lothapalli Waterfalls',
                    'landmark': 'Near Chintapalli / Lothugedda forest range, ~90 km from Visakhapatnam',
                    'desc': 'A hidden gem waterfall cascading down rocky boulder canyons into deep natural freshwater plunge pools nestled in lush Eastern Ghats forest.',
                    'highlight': 'Pristine untouched wilderness, natural swimming pools, boulder hopping'
                },
                {
                    'name': 'Katiki Waterfalls',
                    'landmark': 'Near Borra Caves, ~95 km from Vizag (accessed via 4x4 Jeep trail from Borra)',
                    'desc': 'Spectacular 50-ft natural cascade fed by the Gosthani River; features an adventurous stream-crossing Jeep ride and short nature hike.',
                    'highlight': 'Natural mountain plunge pool, roasted bamboo chicken, lush jungle setting'
                },
                {
                    'name': 'Chaparai Water Cascades (Dumbriguda)',
                    'landmark': '15 km past Araku town towards Paderu (~115 km from Vizag)',
                    'desc': 'Broad flat sloping smooth river rocks where crystal-clear cool waters glide gently amidst a dense canopy of pine and teak trees.',
                    'highlight': 'Gentle rock water sliding, forest shade wading, hot bamboo chicken stalls'
                },
                {
                    'name': 'Kothapalli Waterfalls',
                    'landmark': 'Near G.Madugula / Paderu, ~110 km from Visakhapatnam',
                    'desc': 'Picturesque multi-tier cascading waterfall framed by lush green agricultural hills and tribal villages.',
                    'highlight': 'Tiered water cascades, tranquil photography, cool mountain spray'
                },
                {
                    'name': 'Thatipudi Reservoir & Spillway Cascades',
                    'landmark': 'Near Gantyada / S.Kota foothills, ~65 km from Vizag',
                    'desc': 'Lush reservoir surrounded by Eastern Ghats mountains with picturesque spillway cascades and boating facilities.',
                    'highlight': 'Spillway water streams, serene lake boat rides, hillside greenery'
                }
            ],
            'parks_botanical': [
                {
                    'name': 'Kondakarla Ava Freshwater Lake & Bird Sanctuary',
                    'landmark': 'Near Atchutapuram, ~48 km south of Vizag center',
                    'desc': 'Vast freshwater wetland lake blooming with pink lotus flowers and water lilies; country catamaran raft rides among migratory birds.',
                    'highlight': 'Traditional palm-log catamaran boat rides, lotus flower photography, migratory pelicans & herons'
                },
                {
                    'name': 'Mudasarlova Reservoir & Valley Park',
                    'landmark': 'Mudasarlova valley, 10 km from Vizag center near Arilova',
                    'desc': 'Centuries-old reservoir nestled in a quiet valley flanked by green hills, lush mango orchards, palm groves, and perennial streams.',
                    'highlight': 'Orchard walks, tranquil nature picnics, vintage golf course nearby'
                },
                {
                    'name': 'VMRDA City Central Park',
                    'landmark': 'Opposite Old Central Jail, Dwaraka Nagar / RTC Complex, Visakhapatnam',
                    'desc': 'Sprawling 22-acre urban botanical garden featuring a musical dancing water fountain, bonsai garden, circular jogging track, and floral beds.',
                    'highlight': 'Musical fountain show at 07:00 PM, bonsai collection'
                },
                {
                    'name': 'Tenneti Beach Park & Sea View Amphitheatre',
                    'landmark': 'Beach Road, Jodugullapalem (below Kailasagiri Hill)',
                    'desc': 'Coastal cliffside landscaped park with direct staircase access to the shore and sweeping views of the historic shipwreck.',
                    'highlight': 'Sunset ocean vistas, landscaped cliff gardens'
                }
            ],
            'zoo_wildlife': [
                {
                    'name': 'Indira Gandhi Zoological Park',
                    'landmark': 'Yendada, along Marine Drive (Beach Road), Visakhapatnam',
                    'desc': '625-acre natural forest zoo nestled between Kambalakonda forest and the sea; houses white tigers, Asiatic lions, leopards, primates, and migratory birds in spacious open-moated habitats.',
                    'highlight': 'Toy train safari, battery-operated buggy tour, butterfly park'
                },
                {
                    'name': 'Kambalakonda Wildlife Sanctuary',
                    'landmark': 'National Highway 16, opposite IGNP Zoo, Visakhapatnam',
                    'desc': '71 sq km dry evergreen forest sanctuary home to Indian leopards, barking deer, pangolins, and rare flora.',
                    'highlight': 'Nature hiking trails, canopy suspension bridge, night camping'
                }
            ],
            'shopping_malls': [
                {
                    'name': 'CMR Central Mall',
                    'landmark': 'Maddilapalem Junction, National Highway 16, Visakhapatnam',
                    'desc': 'Premier 5-story shopping mall with lifestyle departmental stores, INOX multiplex cinemas, multi-cuisine food court, and gaming zone.',
                    'highlight': 'National & international fashion, bowling alley, kids play zone'
                },
                {
                    'name': 'Lepakshi Andhra Handicrafts Emporium',
                    'landmark': 'Near Jagadamba Junction, Main Road, Visakhapatnam',
                    'desc': 'Official State handicrafts emporium showcasing authentic Kondapalli softwood toys, Kalamkari hand-printed textiles, bronze statues, and sandalwood artifacts.',
                    'highlight': 'Authentic GI-tagged souvenirs, handloom silk sarees, brass lamps'
                },
                {
                    'name': 'Kurupam Market & Jagadamba Bazaars',
                    'landmark': 'Old Post Office Road to Jagadamba Junction, Visakhapatnam',
                    'desc': 'Centuries-old bustling traditional bazaar lane famous for pure gold jewelry, authentic Uppada silk sarees, and local brassware.',
                    'highlight': 'Traditional wedding jewelry, Uppada Jamdani handloom silk'
                }
            ],
            'fun_zones_waterparks': [
                {
                    'name': 'INS Kursura Submarine Museum',
                    'landmark': 'RK Beach Road Promenade (opposite Victory at Sea Memorial), Visakhapatnam',
                    'desc': 'Asia\'s first submarine museum; a real decommissioned Russian-built Soviet naval submarine preserved directly on the beach sand.',
                    'highlight': 'Walk inside actual torpedo rooms, sonar station, and sailor bunk rooms'
                },
                {
                    'name': 'TU-142 Aircraft Museum & Flight Simulator',
                    'landmark': 'Directly across Beach Road from INS Kursura Submarine, Visakhapatnam',
                    'desc': 'Real Indian Navy long-range anti-submarine maritime patrol bomber aircraft converted into an interactive museum with flight simulators.',
                    'highlight': 'VR cockpit flight simulator, survival equipment exhibits'
                },
                {
                    'name': 'Rushikonda Beach Water Adventure Sports',
                    'landmark': 'Rushikonda Beach, Marine Drive, Visakhapatnam',
                    'desc': 'Premier coastal water sports center offering jet-skiing, banana boat rides, sea kayaking, scuba diving, and surfing lessons.',
                    'highlight': 'Jet-ski rides, scuba diving, certified surfing school'
                },
                {
                    'name': 'Matsyadarshini Marine Aquarium',
                    'landmark': 'Beach Road Promenade, near Pandurangapuram, Visakhapatnam',
                    'desc': 'Coastal aquarium featuring exotic marine specimens including clownfish, electric rays, lionfish, freshwater piranhas, and sea turtles.',
                    'highlight': 'Kids marine education, colorful reef aquariums'
                }
            ]
        },

        'dining_cuisine': {
            'must_try_dishes': [
                {
                    'name': 'Madugula Halwa',
                    'type': 'Sweet Delicacy',
                    'desc': 'Celebrated 130-year-old traditional sweet prepared from sprouted wheat milk, pure ghee, and cashews with an unforgettable melt-in-mouth texture.',
                    'best_at': 'Dangeti Murthy Original Halwa (Madugula / Vizag retail counters)'
                },
                {
                    'name': 'Andhra Royyala Iguru (Spicy Prawn Fry)',
                    'type': 'Non-Vegetarian Seafood',
                    'desc': 'Fresh Bay of Bengal prawns tossed in caramelized shallots, green chilies, curry leaves, and freshly ground coastal garam masala.',
                    'best_at': 'Sea Inn (Raju Gari Dhaba, Rushikonda Marine Drive)'
                },
                {
                    'name': 'Chepala Pulusu (Nellore-Style Tangy Fish Curry)',
                    'type': 'Non-Vegetarian Seafood',
                    'desc': 'Fresh catch of fish simmered in a fiery, tangy tamarind and raw mango gravy with fenugreek and mustard seeds.',
                    'best_at': 'Venkatadri Vantillu & Coastal Dhaba (Siripuram)'
                },
                {
                    'name': 'Vizag Bamboo Chicken (Bongu Kodi)',
                    'type': 'Non-Vegetarian Tribal Specialty',
                    'desc': 'Country chicken marinated with native forest spices, packed inside fresh green bamboo stalks and charcoal-roasted with zero oil.',
                    'best_at': 'Bamboo Chicken Point (Rushikonda & Simhachalam approach)'
                },
                {
                    'name': 'Traditional Andhra Banana Leaf Thali',
                    'type': 'Vegetarian Meals',
                    'desc': 'Steaming hot Sona Masoori rice served with hot ghee, Gunpowder (Kandi Podi), Gongura pachadi, Drumstick Sambar, and Payasam.',
                    'best_at': 'Subbayya Gari Hotel (Dwaraka Nagar)'
                }
            ],
            'famous_food_streets': [
                {
                    'name': 'RK Beach Road Promenade Food Stalls',
                    'landmark': 'From Novotel to Kali Temple stretch, Beach Road',
                    'specialties': 'Muri Mixture (Vizag beach puffed rice chaat), piping hot Mirchi Bajji, grilled buttery sweet corn, and tender coconut water.'
                },
                {
                    'name': 'Siripuram & VIP Road Night Food Street',
                    'landmark': 'Siripuram Junction, near Dutt Island, Visakhapatnam',
                    'specialties': 'Shawarma, South Indian dosas with spicy tomato chutney, seafood fried rice, and artisanal filter coffee.'
                }
            ]
        },

        'culture_traditions': {
            'summary': 'Visakhapatnam embodies a seamless confluence of ancient Kalinga Buddhist legacy, majestic 11th-century Simhachalam temple heritage, and a vibrant coastal maritime community.',
            'festivals_rituals': [
                {
                    'name': 'Visakha Utsav (December – January)',
                    'importance': 'Premier cultural carnival held along RK Beach showcasing Andhra folk traditions, classical music concerts, craft bazaars, and beach sports.',
                    'rituals': 'Beach road carnival processions, classical Kuchipudi recitals, and floral exhibits.'
                },
                {
                    'name': 'Chandanotsavam at Simhachalam (April – May)',
                    'importance': 'The sacred annual festival where the thick sandalwood paste coating is removed, allowing devotees the rare "Nijaroopa Darshanam" of Lord Narasimha for just 12 hours.',
                    'rituals': 'Nijaroopa sacred darshan and fresh sandalwood paste application.'
                },
                {
                    'name': 'Giri Pradakshina (Guru Purnima)',
                    'importance': 'Massive spiritual 32-km holy barefoot circumambulation around the sacred Simhachalam hill by hundreds of thousands of pilgrims.',
                    'rituals': 'Barefoot walking around Simhachalam hill with devotional chants.'
                }
            ],
            'art_crafts': 'Kondapalli wooden lacquer toys, Etikoppaka wooden lacquerware from nearby Yellamanchili, and authentic Uppada Jamdani handloom silk sarees.'
        },

        'celebrations_venues': [
            {
                'name': 'Novotel Visakhapatnam Varun Beach (Vue Lounge & Lawns)',
                'map_landmark': 'Beach Road, directly opposite RK Beach Submarine Museum Promenade, Visakhapatnam',
                'vibe': 'Ultra-luxury sea-facing rooftop terrace lounge & infinity poolside cabanas for glamorous birthdays and anniversaries.',
                'features': 'Vue rooftop lounge, 180-degree ocean sunset view, customized birthday decor, gourmet seafood platters, and sound system.',
                'phone': '+91 891 304 5678'
            },
            {
                'name': 'The Park Visakhapatnam (Aqua & Vista Oceanfront Lawns)',
                'map_landmark': 'Beach Road, Pandurangapuram, 1 km south of Waltair Uplands, Visakhapatnam',
                'vibe': 'Chic private oceanfront lawns and poolside dining decks surrounded by tropical palm groves.',
                'features': 'Private lawn right on the beach, DJ setup, open-air seafood barbecue, candlelit beach tables, and cake cutting service.',
                'phone': '+91 891 304 5555'
            },
            {
                'name': 'Sai Priya Beach Resort (Rushikonda Palm Lawns)',
                'map_landmark': 'Rushikonda Beach Road, Marine Drive, Visakhapatnam',
                'vibe': 'Expansive green beachfront lawns and seaside banquet cabanas for high-energy group celebrations and family parties.',
                'features': 'Private celebration lawns, campfire and bonfire pit, beach sound setup, and live barbecue grill.',
                'phone': '+91 891 279 0333'
            },
            {
                'name': 'Ironhill Brewery & Rooftop Sky Lounge',
                'map_landmark': 'Siripuram Junction, VIP Road, Visakhapatnam',
                'vibe': 'High-energy craft brewery and open-air rooftop with city skyline views, craft brews, and DJ music for squad parties.',
                'features': 'Private party deck, craft beverage platters, customized birthday lighting, and lively music.',
                'phone': '+91 891 668 8999'
            }
        ]
    },

    # ── TIRUPATI & TIRUMALA (Andhra Pradesh) ───────────────────────────────────
    'tirupati': {
        'destination': 'Tirupati',
        'title': 'Tirupati & Tirumala, Andhra Pradesh',
        'tagline': 'Spiritual Capital of Andhra Pradesh — Abode of Lord Venkateswara, Seshachalam Biosphere & Magnificent Waterfalls',
        'overview': 'Tirupati, nestled at the foot of the ancient Seshachalam Hills, is one of the world\'s most sacred pilgrimage destinations. Famous for the hilltop shrine of Lord Sri Venkateswara at Tirumala, it also features breathtaking natural waterfalls like Talakona (highest in AP), sacred rock-cut cave temples, and Asia\'s largest zoological park.',
        
        'route_map': {
            'overview_route': 'Alipiri / Foothills Gateway ➔ Kapila Theertham & Waterfall ➔ Seshachalam Ghat Road / Srivari Mettu Trek ➔ Tirumala Seven Hills Sanctum ➔ Silathoranam & Chakra Theertham ➔ Talakona Waterfall Biosphere Trek ➔ Tiruchanur Padmavathi Ammavari Temple',
            'suggested_sequence': [
                'Day 1: Foothill Darshan at Kapila Theertham, climb or drive up Tirumala Ghat road, sacred Sri Venkateswara Swamy Darshan & Laddu Prasadam.',
                'Day 2: Morning visit to Silathoranam & Papavinasanam, descent to Tirupati, Sri Govindaraja Swamy Temple, and Tiruchanur Padmavathi Ammavari Temple.',
                'Day 3: Full-day scenic nature excursion to Talakona Waterfalls (270 ft cascade) with canopy ropewalk and jungle trail inside S.V. National Park.',
                'Day 4: Kailasakona Waterfalls or Sri Kalahasteeswara Temple (Srikalahasti Vayu Lingam) and Sri Venkateswara Zoological Park safari.'
            ]
        },

        'tourist_spots': {
            'temples': [
                {
                    'name': 'Sri Venkateswara Swamy Temple (Tirumala)',
                    'landmark': 'Tirumala Seven Hills (~22 km from Tirupati foothills via scenic ghat road)',
                    'desc': 'World-famous 10th-century Dravidian shrine dedicated to Lord Balaji; the richest and most visited spiritual sanctuary in the world.',
                    'timing': '03:00 AM – 11:30 PM (Continuous Darshan slots)',
                    'highlight': 'World-famous Tirupati Laddu, Suprabhata Seva, and sacred head-tonsuring (Kalyanakatta)'
                },
                {
                    'name': 'Sri Padmavathi Ammavari Temple',
                    'landmark': 'Tiruchanur (~5 km from Tirupati Railway Station)',
                    'desc': 'Sacred temple of the presiding goddess Padmavathi (consort of Lord Venkateswara); tradition dictates visiting here to complete the Tirumala pilgrimage.',
                    'timing': '06:30 AM – 11:30 AM & 04:00 PM – 08:30 PM',
                    'highlight': 'Padma Sarovaram holy tank and Kumkumarchana ritual'
                },
                {
                    'name': 'Sri Govindaraja Swamy Temple',
                    'landmark': 'Central Tirupati, near Railway Station concourse',
                    'desc': 'Ancient 12th-century temple housing Lord Vishnu in colossal reclining posture, consecrated by Saint Ramanujacharya.',
                    'timing': '05:00 AM – 12:30 PM & 04:30 PM – 09:00 PM',
                    'highlight': 'Towering seven-tiered gopuram and peaceful morning aarti'
                },
                {
                    'name': 'Sri Kapileswara Swamy Temple',
                    'landmark': 'Northern foothills of Tirumala Hills, Alipiri bypass',
                    'desc': 'The only dedicated Shiva temple in Tirupati, located beside a sacred natural mountain waterfall pool.',
                    'timing': '06:00 AM – 12:00 PM & 04:30 PM – 08:30 PM',
                    'highlight': 'Kapila Theertham waterfall plunge pool and ancient rock inscriptions'
                },
                {
                    'name': 'Sri Kalahasteeswara Temple (Srikalahasti)',
                    'landmark': 'Srikalahasti (~36 km from Tirupati on Swarnamukhi River)',
                    'desc': 'Celebrated Pancha Bhoota Sthalam (representing the Vayu/Wind element) and premier Rahu-Ketu Sarpa Dosha Nivarana temple in India.',
                    'timing': '06:00 AM – 09:00 PM',
                    'highlight': 'Unflickering ghee lamp in the sanctum demonstrating the divine wind element'
                }
            ],

            'waterfalls': [
                {
                    'name': 'Talakona Waterfalls (Highest in Andhra Pradesh)',
                    'landmark': 'Nerabailu village, Sri Venkateswara National Park (~45 km from Tirupati via Bakarapeta)',
                    'desc': 'Magnificent 270-ft natural cascade plunging through dense evergreen forests. The crystal-clear waters pass through rare medicinal herbs into deep natural swimming pools.',
                    'highlight': '240-meter canopy ropewalk suspended 35 ft high, herbal rock pools, and biodiversity trek'
                },
                {
                    'name': 'Kapila Theertham Waterfalls',
                    'landmark': 'Alipiri bypass road, foothills of Tirumala, Tirupati',
                    'desc': 'Perennial mountain waterfall cascading down steep granite cliffs of Seshachalam range into the sacred temple pushkarini.',
                    'highlight': 'Sacred ablution point for pilgrims and spectacular cascading flow during post-monsoon'
                },
                {
                    'name': 'Kailasakona Waterfalls',
                    'landmark': 'Near Narayanavanam (~40 km from Tirupati via Puttur highway)',
                    'desc': 'Perennial 40-foot natural waterfall pouring crystal-clear mineral waters into a safe rock pond with adjacent ancient Shiva shrine.',
                    'highlight': 'Safe family swimming, scenic hill drive, and green picnic lawns'
                },
                {
                    'name': 'Ubbalamadugu Falls (Tada Falls / Siddulaiah Kona)',
                    'landmark': 'Varadaiahpalem border (~75 km from Tirupati)',
                    'desc': 'Multi-tiered mountain stream cascades cutting through deep rock gorges with crystal-clear plunge pools and a 7 km boulder trek.',
                    'highlight': 'Adventure boulder-hopping, forest trekking, and secluded swimming lagoons'
                },
                {
                    'name': 'Chakra Theertham & Papavinasanam Waterfalls',
                    'landmark': 'Tirumala forest ridge, ~5 km north of Tirumala temple',
                    'desc': 'Sacred mountain waterfalls and stream cascades nestled inside dense pine and teak woods.',
                    'highlight': 'Spiritual holy dip and peaceful forest breezes'
                }
            ],

            'hills_viewpoints': [
                {
                    'name': 'Silathoranam (Natural Stone Rock Arch)',
                    'landmark': '1 km north of Tirumala temple, Tirumala Hills',
                    'desc': 'Rare geological natural rock arch formation dating back 1.5 billion years, one of only three such arches in the world.',
                    'highlight': 'Unique prehistoric geological marvel surrounded by landscaped rock gardens'
                },
                {
                    'name': 'Srivari Mettu & Alipiri Footstep Pilgrimage Treks',
                    'landmark': 'Alipiri & Srinivasa Mangapuram footpaths, Tirupati',
                    'desc': 'Ancient stone-stepped pilgrimage paths (3,550 steps) climbed barefoot by millions of devotees amidst forest canopies.',
                    'highlight': 'Continuous drinking water, free luggage transport to Tirumala, and panoramic valley viewpoints'
                },
                {
                    'name': 'Japali Hanuman Theertham',
                    'landmark': 'Dense forest trail, 4 km from Tirumala',
                    'desc': 'Sacred forest temple and natural spring where Lord Hanuman is believed to have meditated.',
                    'highlight': 'Serene jungle walking trail under ancient banyan and teak canopies'
                }
            ],

            'parks_botanical': [
                {
                    'name': 'Sri Venkateswara Zoological Park',
                    'landmark': 'SV Zoo Road, Tirupati (~10 km from center)',
                    'desc': 'Asia’s largest zoological park spreading across 5,500 acres of natural forest reserve, featuring open-moated enclosures and lion safaris.',
                    'highlight': 'Battery buggy safari, white tigers, leopards, and Asiatic lions'
                },
                {
                    'name': 'Kalyani Dam & Forest Reservoir',
                    'landmark': 'Rangampeta forest area (~18 km from Tirupati)',
                    'desc': 'Picturesque freshwater dam nestled in deep mountain valleys providing water to Tirupati; surrounded by verdant forests.',
                    'highlight': 'Scenic nature viewpoints, peaceful sunset breezes, and birdwatching'
                }
            ],

            'shopping_malls': [
                {
                    'name': 'Tirupati Urban Haat & Craft Bazaars',
                    'landmark': 'Karakambadi Road, Tirupati',
                    'desc': 'Artisan emporium showcasing traditional Andhra brass artifacts, red sanders wood carvings, and Kalamkari handlooms.',
                    'highlight': 'Authentic Tirupati Tanjore gold-foil paintings and bronze idols'
                },
                {
                    'name': 'Kalanikethan & South India Shopping Mall',
                    'landmark': 'TK Street / Gandhi Road, Tirupati',
                    'desc': 'Premier multi-floor shopping hub for authentic Kanchipuram and Dharmavaram pure silk sarees and festive wear.',
                    'highlight': 'Handloom silk collection and traditional jewelry'
                }
            ],

            'fun_zones_waterparks': [
                {
                    'name': 'Regional Science Centre & Planetarium',
                    'landmark': 'Alipiri foothills road, Tirupati',
                    'desc': 'Interactive science museum featuring outdoor science park, 3D science theater, and state-of-the-art planetarium.',
                    'highlight': 'Stargazing telescope sessions and interactive physics exhibits'
                }
            ]
        },

        'dining_cuisine': {
            'must_try_dishes': [
                {
                    'name': 'Tirupati Laddu Prasadam',
                    'type': 'Sacred Sweet Specialty',
                    'desc': 'The GI-tagged divine sweet prepared using premium besan, pure cow ghee, cashew nuts, cardamom, raisins, and sugar candy (Kalkandu).',
                    'best_at': 'TTD Laddu Counters, Tirumala Sanctum'
                },
                {
                    'name': 'Authentic Rayalaseema & Andhra Banana Leaf Thali',
                    'type': 'Pure Vegetarian Meals',
                    'desc': 'Steaming hot Sona Masoori rice served with hot ghee, Kandi Podi (gunpowder), Gongura chutney, Gutti Vankaya curry, and Payasam.',
                    'best_at': 'Bhimas Deluxe (Railway Station Road) & Madhuram Veg'
                },
                {
                    'name': 'Tirumala Free Nitya Annadanam',
                    'type': 'Sacred Devotional Feast',
                    'desc': 'Massive state-of-the-art dining complex serving thousands of pilgrims steaming hot sambar rice, sweet pongal, and buttermilk with supreme devotion.',
                    'best_at': 'Matrusri Tarigonda Vengamamba Complex, Tirumala'
                }
            ],
            'famous_food_streets': [
                {
                    'name': 'Bhavani Nagar & Gandhi Road Food Lane',
                    'landmark': 'Central Tirupati, near RTC Complex',
                    'desc': 'Vibrant evening street famous for steaming Ghee Idlis, spicy Guntur Dosas, and hot filter coffee.'
                }
            ]
        },

        'culture_traditions': {
            'summary': 'Tirupati represents the living spiritual soul of Dravidian devotional tradition, steeped in ancient Vaishnavite traditions, daily temple rituals, and the sacred Seshachalam forest ecosystem.',
            'festivals_rituals': [
                {
                    'name': 'Srivari Salakatla Brahmotsavam (September – October)',
                    'importance': 'Grand 9-day annual celestial festival where Lord Malayappa Swamy is taken out in majestic processions on various Vahanams (Garuda Vahanam, Rathotsavam).',
                    'rituals': 'Garuda Seva, Golden Chariot procession, and Chakrasnanam bath.'
                },
                {
                    'name': 'Vaikunta Ekadasi (December – January)',
                    'importance': 'The auspicious day when the sacred northern door (Vaikunta Dwaram) is opened for devotees to attain spiritual liberation.',
                    'rituals': 'Passing through Vaikunta Dwaram with special morning darshan.'
                }
            ],
            'art_crafts': 'Red sanders wood carvings, brass temple lamps, and Tanjore gold foil art.'
        },

        'celebrations_venues': [
            {
                'name': 'Fortune Select Grand Ridge (Rooftop & Lawns)',
                'map_landmark': 'Shilparamam, Tiruchanur Road, Tirupati',
                'vibe': 'Upscale rooftop lounge and landscaped party lawns with panoramic views of the Tirumala Hills.',
                'features': 'Customized birthday setups, private terrace catering, and gourmet buffet spreads.',
                'phone': '+91 877 222 1155'
            },
            {
                'name': 'Marasa Sarovar Premiere (Water Lotus Lawns)',
                'map_landmark': 'Upadhyaya Nagar, Karakambadi Road, Tirupati',
                'vibe': 'Unique Navarasa-themed luxury resort featuring lotus waterbodies, banquet lawns, and poolside decks.',
                'features': 'Open-air celebration lawns, gourmet multi-cuisine feasts, and sound system setup.',
                'phone': '+91 877 666 0000'
            },
            {
                'name': 'Taj Tirupati (Grand Ballrooms & Garden Terrace)',
                'map_landmark': 'Tirupati-Renigunta Road, near Ramanuja Circle, Tirupati',
                'vibe': 'Ultra-luxury 5-star hospitality, grand chandeliers, and private celebration lawns.',
                'features': 'Dedicated event managers, bespoke cake cutting, and live chef stations.',
                'phone': '+91 877 660 7000'
            }
        ]
    },

    # ── GOA (Beaches, Cascades, Temples & Heritage) ───────────────────────────
    'goa': {
        'destination': 'Goa',
        'title': 'Goa — Tropical Cascades, Sacred Temples & Coastal Heritage',
        'map_query': 'Panaji, Goa, India',
        'summary': 'India\'s premier coastal paradise blending Portuguese baroque churches, ancient inland Kadamba temples, lush Western Ghat waterfalls, spice estates, and world-renowned golden beaches.',

        'route_sequence': [
            'Dudhsagar Waterfalls & Mollem National Park',
            'Historic Old Goa Churches & Ancient Ponda Temples',
            'Sahakari Spice Farm & Plantations',
            'Panaji Latin Quarter (Fontainhas) & Mandovi Cruise',
            'Vagator & Anjuna Sunset Clifftops'
        ],

        'tourist_spots': {
            'waterfalls': [
                {
                    'name': 'Dudhsagar Waterfalls (Sea of Milk)',
                    'landmark': 'Bhagwan Mahavir Wildlife Sanctuary, Mollem (accessed via Kulem / Collem safari jeep or trek)',
                    'desc': 'Majestic 310-meter four-tiered cascade tumbling through the verdant Western Ghats beneath the historic railway arch bridge.',
                    'highlight': 'Natural freshwater plunge pool swim and scenic 4x4 jungle jeep safari'
                },
                {
                    'name': 'Harvalem / Arvalem Waterfalls',
                    'landmark': 'Near Sanquelim & Arvalem rock-cut caves, North Goa (~32 km from Panaji)',
                    'desc': 'Picturesque 50-meter cascade cascading into a broad emerald plunge pool surrounded by dense fruit orchards and ancient rock caves.',
                    'highlight': 'Historic 6th-century rock-cut Pandava Buddhist caves and Rudreshwar temple'
                },
                {
                    'name': 'Tambdi Surla Waterfalls',
                    'landmark': 'Deep Mollem National Park jungle trail, starting from Tambdi Surla Mahadev Temple',
                    'desc': 'Secluded forest waterfall reached by a scenic 90-minute rainforest trek across mountain streams in the Western Ghats.',
                    'highlight': 'Pristine rainforest trail and 12th-century Kadamba black basalt temple'
                },
                {
                    'name': 'Netravali / Savari Waterfalls',
                    'landmark': 'Netravali Wildlife Sanctuary, South Goa',
                    'desc': 'Hidden double-cascade waterfall deep inside dense evergreen canopy with natural rock jacuzzis.',
                    'highlight': 'Bubbly lake phenomenon and tranquil nature solitude'
                }
            ],

            'temples': [
                {
                    'name': 'Shri Mangueshi Temple (Manguesh Devasthan)',
                    'landmark': 'Mangeshi village, Priol, Ponda (~21 km from Panaji)',
                    'desc': 'Celebrated 400-year-old Shiva temple featuring ornate Konkani-Goan architecture, a seven-story Deepastambha (lamp tower), and sacred temple tank.',
                    'timing': '06:00 AM – 10:00 PM',
                    'highlight': 'Spectacular evening lamp tower illumination and Maha Shivaratri celebrations'
                },
                {
                    'name': 'Shri Shanta Durga Temple (Kavlem)',
                    'landmark': 'Foothills of Kavalem village, Ponda (~28 km from Panaji)',
                    'desc': 'Revered peaceful Goddess temple dedicated to the deity who mediated the celestial war between Vishnu and Shiva; showcases pyramidal shikharas and Roman arched stained-glass windows.',
                    'timing': '06:00 AM – 09:30 PM',
                    'highlight': 'Golden palanquin procession (Palkhi) and tranquil hillside courtyard'
                },
                {
                    'name': 'Tambdi Surla Mahadev Temple (Kadamba Temple)',
                    'landmark': 'Mollem National Park forest base, North Goa',
                    'desc': 'The oldest surviving temple in Goa (12th century), masterfully carved from weather-resistant black basalt stone featuring intricate Kadamba-Yadava carvings.',
                    'timing': '07:00 AM – 06:00 PM',
                    'highlight': 'Ancient rock craftsmanship nestled amidst dense virgin rainforest'
                },
                {
                    'name': 'Shri Mahalaxmi Temple (Bandora)',
                    'landmark': 'Bandivade / Bandora, Ponda',
                    'desc': 'Sacred ancestral temple of Goddess Mahalaxmi wearing a linga on her crown; holds historical wooden galleries depicting Bhagavad Gita scenes.',
                    'timing': '06:30 AM – 08:30 PM',
                    'highlight': 'Navaratri festival rathotsavam'
                }
            ],

            'hills_viewpoints': [
                {
                    'name': 'Fort Aguada & Lighthouse Clifftop',
                    'landmark': 'Sinquerim Beach headland, Candolim, North Goa',
                    'desc': '17th-century Portuguese coastal fort offering 360-degree vistas over the Arabian Sea and Mandovi River confluence.',
                    'highlight': 'Four-story historic lighthouse and panoramic ocean sunset'
                },
                {
                    'name': 'Chapora Fort Clifftop (Dil Chahta Hai Point)',
                    'landmark': 'Vagator headland, overlooking Chapora River estuary',
                    'desc': 'Red laterite cliff ramparts overlooking golden Vagator shoreline and crashing surf.',
                    'highlight': 'Spectacular sunset silhouettes and sea-breeze panorama'
                },
                {
                    'name': 'Cabo de Rama Fort Sea Cliffs',
                    'landmark': 'Canacona, South Goa (~30 km from Margao)',
                    'desc': 'Wild secluded cliff promontory with dramatic vertical drop into turquoise coastal waters.',
                    'highlight': 'Unspoiled sea views and tranquil white chapel ruins'
                }
            ],

            'parks_botanical': [
                {
                    'name': 'Sahakari Spice Farm & Plantations',
                    'landmark': 'Curti, Ponda (~2 km from Ponda town)',
                    'desc': '130-acre lush organic spice plantation cultivating vanilla, cardamom, cinnamon, peri-peri peppers, and betel nut palms.',
                    'highlight': 'Guided spice botanical walk, elephant bathing, and authentic buffet lunch'
                },
                {
                    'name': 'Salim Ali Bird Sanctuary (Chorão Island)',
                    'landmark': 'Mandovi River estuary, accessed via Ribandar ferry',
                    'desc': 'Pristine mangrove swamp forest sanctuary hosting migratory waterbirds, kingfishers, and mudskippers.',
                    'highlight': 'Early morning quiet boat safari through winding mangrove canals'
                }
            ],

            'zoo_wildlife': [
                {
                    'name': 'Bhagwan Mahavir Wildlife Sanctuary & Mollem National Park',
                    'landmark': 'Eastern border along Western Ghats, Mollem',
                    'desc': 'Goa\'s largest wildlife reserve spanning 240 sq km; home to leopards, barking deer, giant flying squirrels, and King Cobras.',
                    'highlight': 'Dudhsagar waterfall jeep safaris and canopy birdwatching'
                },
                {
                    'name': 'Bondla Wildlife Sanctuary & Zoo',
                    'landmark': 'Ponda Taluka foothills, North Goa',
                    'desc': 'Family-friendly sanctuary with mini zoo, deer safari park, botanical rose garden, and rehabilitation center.',
                    'highlight': 'Safe animal viewing and quiet botanical walk'
                }
            ],

            'shopping_malls': [
                {
                    'name': 'Mall De Goa (Porvorim)',
                    'landmark': 'NH-66 Highway, Porvorim, North Goa',
                    'desc': 'Premier modern multi-level shopping destination featuring international fashion brands, INOX cinema, and multi-cuisine food court.',
                    'highlight': 'Air-conditioned leisure and branded shopping'
                },
                {
                    'name': 'Anjuna Flea Market & Arpora Saturday Night Market',
                    'landmark': 'Anjuna Beachfront & Arpora Hillside, North Goa',
                    'desc': 'World-famous open-air bohemian markets brimming with handmade silver jewelry, spices, leather crafts, live acoustic bands, and global street food.',
                    'highlight': 'Vibrant bohemian night shopping and live music'
                }
            ],

            'fun_zones_waterparks': [
                {
                    'name': 'Splashdown Waterpark (Anjuna)',
                    'landmark': 'Calangute-Anjuna Main Road, North Goa',
                    'desc': 'High-energy family water park featuring 5 pools, tornado flumes, spiral aqua slides, and dancing rain decks.',
                    'highlight': 'Adrenaline water slides and family wave pool'
                },
                {
                    'name': 'Grand Island Scuba Diving & Snorkeling Expeditions',
                    'landmark': 'Departs from Sinquerim / Vasco jetties',
                    'desc': 'Open-sea underwater adventure featuring shallow coral reef diving, tropical fish sightings, and dolphin spotting cruises.',
                    'highlight': 'PADI certified instructors and underwater photography'
                }
            ]
        },

        'dining_cuisine': {
            'must_try_dishes': [
                {
                    'name': 'Authentic Goan Fish Curry Thali',
                    'type': 'Coastal Seafood Delight',
                    'desc': 'Fresh Kingfish (Surmai) or Pomfret curry prepared with freshly grated coconut, Kashmiri chilies, and tangy Kokum (Amsol), served with rice and fried prawns.',
                    'best_at': 'Ritz Classic (Panaji 18th June Road) & Anand Seafood (Anjuna)'
                },
                {
                    'name': 'Chicken / Vegetable Xacuti & Poi Bread',
                    'type': 'Heritage Indo-Portuguese Specialty',
                    'desc': 'Rich, complex gravy made with roasted whole spices, poppy seeds, and desiccated coconut, paired with hot traditional Goan wood-fired Poi bread.',
                    'best_at': 'Viva Panjim (Fontainhas Heritage Quarter)'
                },
                {
                    'name': 'Traditional Goan Bebinca',
                    'type': 'Multi-Layered Coconut Pudding',
                    'desc': 'The "Queen of Goan desserts" — 7 to 16 baked layers of rich coconut milk, egg yolk, flour, pure ghee, and grated nutmeg.',
                    'best_at': 'Confeitaria 31 de Janeiro (Fontainhas)'
                }
            ],
            'famous_food_streets': [
                {
                    'name': 'Fontainhas & 18th June Road Food Walk',
                    'landmark': 'Panaji Latin Quarter & City Center',
                    'desc': 'Charming cobblestone lanes lined with Portuguese heritage bakeries, craft cafes, and seafood bistros.'
                }
            ]
        },

        'culture_traditions': {
            'summary': 'Goa embodies a vibrant synthesis of four centuries of Portuguese influence and indigenous Konkani Hindu heritage, expressed through melodious Konkani Mandos, festive Carnival processions, Shigmo folk dances, and relaxed \'Susegad\' living.',
            'festivals_rituals': [
                {
                    'name': 'Goa Carnival (February)',
                    'importance': 'Colossal 4-day pre-Lent cultural fiesta led by King Momo featuring extravagant street floats, brass bands, masked dancers, and colorful street parades in Panaji and Margao.',
                    'rituals': 'Float parade processions, Red and Black gala dance, and street music.'
                },
                {
                    'name': 'Shigmo Spring Festival (March)',
                    'importance': 'Traditional Goan Hindu spring celebration honoring warrior heroes and the harvest with colossal mythological tableau processions and traditional Ghode Modni folk dances.',
                    'rituals': 'Fugdi dances, temple rath processions, and vibrant color smearing.'
                }
            ],
            'art_crafts': 'Terracotta pottery, Azulejos hand-painted ceramic tiles, brass samai lamps, and coconut shell crafts.'
        },

        'celebrations_venues': [
            {
                'name': 'W Goa Rockpool (Vagator Hilltop)',
                'map_landmark': 'Vagator Beach headland, below Chapora Fort, North Goa',
                'vibe': 'Ultra-stylish cliffside poolside lounge carved into the red laterite rocks with uninterrupted ocean sunset views.',
                'features': 'Sunset cocktails, private DJ booths, customized celebration cakes, and coastal grill banquet.',
                'phone': '+91 832 671 8888'
            },
            {
                'name': 'Thalassa Greek Taverna & Sunset Deck',
                'map_landmark': 'Vaddy, Siolim (~15 mins from Morjim / Vagator), North Goa',
                'vibe': 'Iconic open-air Mediterranean taverna perched over the backwaters with white cabanas and fire dancer shows.',
                'features': 'Sunset cake cutting, live Greek sirtaki dance, and gourmet Mediterranean platters.',
                'phone': '+91 98500 33537'
            },
            {
                'name': 'Purple Martini at Sunset Point (Anjuna Clifftop)',
                'map_landmark': 'St. Michael\'s Vaddo, Anjuna Clifftop, North Goa',
                'vibe': 'Santorini-themed clifftop lounge with direct crashing wave views, saxophone artists, and twilight celebrations.',
                'features': 'Reserved ocean-view private tables, candlelit setup, and anniversary/birthday decor.',
                'phone': '+91 98719 00995'
            }
        ]
    },

    # ── SRIKAKULAM (Arasavilli, Srikurmam, Mukhalingam, Kalingapatnam) ────────
    'srikakulam': {
        'destination': 'Srikakulam',
        'title': 'Srikakulam — Sacred Sun Temple, Rare Kurma Kshetra & Scenic Coastline',
        'map_query': 'Srikakulam, Andhra Pradesh, India',
        'summary': 'Historic temple district of northern Andhra Pradesh, world-famous for the ancient Arasavalli Sun Temple, the world\'s only Sri Kurmam tortoise avatar temple, and quiet Bay of Bengal beaches.',

        'route_sequence': [
            'Sri Suryanarayana Swamy Temple (Arasavalli)',
            'Sri Kurmanatha Swamy Temple (Srikurmam)',
            'Kalingapatnam Beach & Lighthouse',
            'Salihundam Buddhist Heritage Hill',
            'Sri Mukhalingeswara Swamy Temple (Mukhalingam)'
        ],

        'tourist_spots': {
            'temples': [
                {
                    'name': 'Sri Suryanarayana Swamy Temple (Arasavalli Sun Temple)',
                    'landmark': 'Arasavalli, ~3 km from Srikakulam town center',
                    'desc': 'Ancient 7th-century Sun God temple built by Kalinga King Devendra Varma. It is the premier living Sun temple in India where morning sunlight illuminates the feet of the Lord twice a year.',
                    'timing': '06:00 AM – 12:30 PM & 03:30 PM – 08:00 PM',
                    'highlight': 'Early morning Aditya Hrudayam prayers & special Sunday darshan'
                },
                {
                    'name': 'Sri Kurmanatha Swamy Temple (Srikurmam)',
                    'landmark': 'Srikurmam village, ~14 km from Srikakulam town',
                    'desc': 'The only temple in the entire world dedicated to Lord Vishnu in His Kurma (Tortoise) Avatar. Features a sacred tortoise sanctuary lake (Swetha Pushkarini) and two Dhwajasthambhams.',
                    'timing': '06:00 AM – 12:30 PM & 03:00 PM – 08:00 PM',
                    'highlight': 'Rare Kurma Avatar darshan and feeding sacred tortoises'
                },
                {
                    'name': 'Sri Mukhalingeswara Swamy Temple (Mukhalingam)',
                    'landmark': 'Jalumuru, on the banks of Vamsadhara River (~45 km from Srikakulam)',
                    'desc': 'Exquisite 8th-century temple complex built by Eastern Ganga kings featuring beautiful stone carvings and an ancient Shiva Lingam.',
                    'timing': '06:00 AM – 07:30 PM',
                    'highlight': 'Historic stone architecture and peaceful riverside ambiance'
                },
                {
                    'name': 'Sri Endala Mallikarjuna Swamy Temple (Ravivalasa)',
                    'landmark': 'Ravivalasa, Tekkali mandal (~40 km from Srikakulam)',
                    'desc': 'Unique ancient Shiva temple without a roof, worshiped directly under the open sky (Endala).',
                    'timing': '06:30 AM – 06:30 PM',
                    'highlight': 'Open-sky sanctum and special Maha Shivaratri celebrations'
                }
            ],

            'hills_viewpoints': [
                {
                    'name': 'Kalingapatnam Beach & British Lighthouse',
                    'landmark': 'Kalingapatnam coastal village (~28 km from Srikakulam)',
                    'desc': 'Scenic, peaceful beach at the confluence of Vamsadhara River and Bay of Bengal, featuring a historic British-era lighthouse.',
                    'highlight': 'Panoramic sea view from lighthouse top and relaxing breeze'
                },
                {
                    'name': 'Salihundam Buddhist Heritage Hillock',
                    'landmark': 'Salihundam, ~18 km from Srikakulam (on Vamsadhara riverbank)',
                    'desc': 'Ancient 2nd-century BC Buddhist archaeological site with rock stupas, chaityas, and meditation caves on a breezy hillock.',
                    'highlight': 'Sweeping views over Vamsadhara river and ancient stone stupas'
                },
                {
                    'name': 'Baruva Beach & Estuary',
                    'landmark': 'Baruva, Sompeta (~85 km from Srikakulam on coastal road)',
                    'desc': 'Tranquil golden beach lined with lush green coconut groves and old harbor ruins.',
                    'highlight': 'Quiet seaside strolls and photography'
                }
            ],

            'waterfalls': [
                {
                    'name': 'Telineelapuram Migratory Bird Sanctuary',
                    'landmark': 'Near Tekkali, ~60 km from Srikakulam',
                    'desc': 'Lush wetland sanctuary hosting thousands of migratory painted storks and spot-billed pelicans traveling all the way from Siberia.',
                    'highlight': 'Birdwatching towers and quiet nature photography'
                }
            ],

            'parks_botanical': [
                {
                    'name': 'Vamsadhara Riverfront Park',
                    'landmark': 'Near Old River Bridge, Srikakulam',
                    'desc': 'Peaceful riverbank promenade and green garden for evening walks and sunset views.',
                    'highlight': 'Gentle evening river breeze'
                }
            ],

            'shopping_malls': [
                {
                    'name': 'Srikakulam Main Bazaar & Gandhi Road',
                    'landmark': 'Central Market Area, Srikakulam',
                    'desc': 'Traditional local bazaar famous for genuine Srikakulam Bellam Jalebi, Pootharekulu sweets, and handloom cotton sarees.',
                    'highlight': 'Local sweets and authentic handloom fabrics'
                }
            ],

            'fun_zones_waterparks': [
                {
                    'name': 'Kalingapatnam Beach Water Activities',
                    'landmark': 'Kalingapatnam Beach',
                    'desc': 'Beach horse rides, ATV rides along the sand, and speed boating near the river mouth.',
                    'highlight': 'Fun family beach sports'
                }
            ]
        },

        'dining_cuisine': {
            'must_try_dishes': [
                {
                    'name': 'Srikakulam Hot Bellam Jalebi',
                    'type': 'Signature Regional Sweet',
                    'desc': 'Crispy, juicy sweet prepared with pure organic sugarcane jaggery (bellam) instead of refined sugar, served piping hot.',
                    'best_at': 'Traditional Sweet Stalls, Old Bus Stand Road'
                },
                {
                    'name': 'Arasavalli Sun Temple Godhuma Halwa Prasadam',
                    'type': 'Sacred Devotional Prasadam',
                    'desc': 'Divine wheat halwa cooked in pure ghee and cardamom, famous among pilgrims.',
                    'best_at': 'Official Temple Prasadam Counter, Arasavalli'
                },
                {
                    'name': 'Traditional Andhra Banana Leaf Thali',
                    'type': 'Pure Veg Meal',
                    'desc': 'Hot steamed rice served with freshly made Gongura pickle, Kandi Podi with pure ghee, Gutti Vankaya curry, and Srikakulam Majjiga Pulusu.',
                    'best_at': 'Hotel Grand Vamsadhara & Sri Suryanarayana Meals'
                }
            ],
            'famous_food_streets': [
                {
                    'name': 'Old Bus Stand Road & Rythu Bazaar Lane',
                    'landmark': 'Central Srikakulam',
                    'desc': 'Famous for evening hot tiffins, crispy Karam Podi Dosas, and hot filter coffee.'
                }
            ]
        },

        'culture_traditions': {
            'summary': 'Srikakulam is steeped in ancient Kalinga heritage, known for living sun worship traditions, brass handicrafts, and classical Kuchipudi and folk dance cultures.',
            'festivals_rituals': [
                {
                    'name': 'Ratha Saptami (Surya Jayanti in February)',
                    'importance': 'The biggest annual festival at Arasavalli Sun Temple celebrating the birth of the Sun God. Over 200,000 pilgrims take holy baths in the temple tank.',
                    'rituals': 'Surya Namaskaram, Kalyanotsavam, and Maha Ksheerabhishekam with milk.'
                },
                {
                    'name': 'Maha Shivaratri at Mukhalingam & Ravivalasa',
                    'importance': 'All-night devotional vigilance, sacred dip in Vamsadhara River, and special Rudrabhishekam.',
                    'rituals': 'Continuous chanting and night darshan.'
                }
            ],
            'art_crafts': 'Ponduru fine Khadi handspun cotton, brass temple bells, and terracotta pottery.'
        },

        'celebrations_venues': [
            {
                'name': 'Hotel Grand Vamsadhara Banquet & Terrace',
                'map_landmark': 'Main Road, near RTC Bus Complex, Srikakulam',
                'vibe': 'Top-rated hotel in Srikakulam with spacious air-conditioned banquet halls and rooftop terrace for birthdays and family gatherings.',
                'features': 'Full catering service, event audio system, and customized party cakes.',
                'phone': '+91 8942 225 555'
            },
            {
                'name': 'Sunrise Riverside Resort & Lawns',
                'map_landmark': 'Kalingapatnam Road, near Vamsadhara Bridge, Srikakulam',
                'vibe': 'Open-air green lawns beside the river, perfect for outdoor birthday celebrations, photography, and evening family dinner.',
                'features': 'Lawn seating, buffet dinner setup, and music system.',
                'phone': '+91 8942 278 999'
            }
        ]
    }
}


def get_destination_master_guide(destination, state='', days=3):
    """
    Returns the comprehensive, all-inclusive destination master guide:
    - Route map & visual sequence
    - All categorized tourist spots (Temples, Hills, Waterfalls, Parks, Zoos, Malls, Fun Zones)
    - Night stays & lodges (phones, booking links, no prices)
    - Dining & best dishes to try
    - Culture, festivals & rituals
    - Occasion / Birthday venues with exact landmark map addresses
    - Nearby Transit ATMs
    - Tailored enthusiastic day-by-day itinerary for user's 'days'
    """
    dest_clean = (destination or 'Gujarat').strip()
    dest_lower = dest_clean.lower()
    state_lower = (state or '').strip().lower()

    # Find curated match with aliases
    matched = None
    if any(alias in dest_lower for alias in ['vizag', 'visakhapatnam', 'vishakapatnam', 'vishakhapatnam', 'visakha']):
        matched = DESTINATION_MASTER_REGISTRY.get('visakhapatnam')
    elif any(alias in dest_lower for alias in ['araku', 'borra']):
        matched = DESTINATION_MASTER_REGISTRY.get('araku')
    elif any(alias in dest_lower for alias in ['tirupati', 'tirumala', 'tirupathi', 'renigunta', 'srikalahasti', 'chandragiri']):
        matched = DESTINATION_MASTER_REGISTRY.get('tirupati')
    elif any(alias in dest_lower for alias in ['goa', 'panaji', 'madgaon', 'vasco', 'calangute', 'baga', 'anjuna', 'candolim', 'siolim', 'vagator']):
        matched = DESTINATION_MASTER_REGISTRY.get('goa')
    elif any(alias in dest_lower for alias in ['srikakulam', 'arasavilli', 'arasavalli', 'srikurmam', 'kurmam', 'mukhalingam']):
        matched = DESTINATION_MASTER_REGISTRY.get('srikakulam')
    elif any(alias in dest_lower for alias in ['gujarat', 'ahmedabad', 'kutch', 'sasan gir', 'dwarka', 'somnath']):
        matched = DESTINATION_MASTER_REGISTRY.get('gujarat')

    if not matched:
        for k in DESTINATION_MASTER_REGISTRY.keys():
            if k in dest_lower or (state_lower and k in state_lower):
                matched = DESTINATION_MASTER_REGISTRY[k]
                break

    dest_title = dest_clean.title()
    days_count = max(1, min(days, 7))

    # Fetch verified hotels
    stays = generate_hotels(f"{dest_title}, {state}") or []

    # Fetch verified transit ATMs
    atms = get_nearby_atms(dest_clean, state)

    if matched:
        guide = dict(matched)
        guide['destination'] = dest_title
        guide['days'] = days_count
        guide['stays'] = stays[:6]
        guide['atms'] = atms
        guide['map_embed_url'] = f"https://maps.google.com/maps?q={urllib.parse.quote_plus(guide.get('map_query', dest_title))}&t=&z=11&ie=UTF8&iwloc=&output=embed"
        guide['enthusiastic_itinerary'] = _build_enthusiastic_plan(dest_title, guide['tourist_spots'], days_count)
        return guide

    # ── Universal Dynamic Master Guide for Any Other Destination ─────────────
    from utils.universal_generator import generate_universal_destination
    univ = generate_universal_destination(dest_title) or {}
    
    # Extract attractions from CSV
    csv_attrs = []
    try:
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'destinations.csv')
        if os.path.exists(csv_path):
            import pandas as pd
            df = pd.read_csv(csv_path)
            m = df[df['Destination'].str.lower() == dest_clean.lower()]
            if m.empty:
                m = df[df['State'].str.lower() == dest_clean.lower()]
            if not m.empty and pd.notna(m.iloc[0]['Attractions']):
                csv_attrs = [a.strip() for a in str(m.iloc[0]['Attractions']).split(',') if a.strip()]
    except Exception:
        pass

    # Categorize real CSV attractions into specific categories
    temple_attrs = []
    falls_attrs = []
    hills_attrs = []
    zoo_attrs = []
    botanical_attrs = []
    general_attrs = []

    for attr in csv_attrs:
        a_low = attr.lower()
        if any(w in a_low for w in ['temple', 'swamy', 'shrine', 'mandir', 'kovil', 'devasthanam', 'arasavilli', 'arasavalli', 'srikurmam', 'kurmam', 'mukhalingam', 'jyotirlinga', 'dargah', 'church', 'cathedral', 'stupa', 'monastery', 'peeth', 'veerabhadra']):
            temple_attrs.append(attr)
        elif any(w in a_low for w in ['fall', 'falls', 'waterfall', 'waterfalls', 'cascade']):
            falls_attrs.append(attr)
        elif any(w in a_low for w in ['hill', 'peak', 'viewpoint', 'point', 'ridge', 'canyon', 'valley', 'cave', 'caves', 'fort', 'overlook']):
            hills_attrs.append(attr)
        elif any(w in a_low for w in ['wildlife', 'sanctuary', 'zoo', 'safari', 'national park', 'deer', 'bird']):
            zoo_attrs.append(attr)
        elif any(w in a_low for w in ['lake', 'beach', 'river', 'dam', 'reservoir', 'park', 'garden', 'botanical', 'island', 'ghat', 'farm']):
            botanical_attrs.append(attr)
        else:
            general_attrs.append(attr)

    dynamic_temples = []
    for t in temple_attrs:
        dynamic_temples.append({
            'name': t,
            'landmark': f'{t}, {dest_title}',
            'desc': f'Famous sacred shrine in {dest_title} visited by pilgrims.',
            'timing': '06:00 AM – 12:30 PM & 04:00 PM – 08:30 PM'
        })
    if not dynamic_temples:
        cand = general_attrs.pop(0) if general_attrs else f'{dest_title} Historical Temple'
        dynamic_temples.append({
            'name': cand,
            'landmark': f'Temple Road, {dest_title}',
            'desc': f'Historic temple and spiritual landmark in {dest_title}.',
            'timing': '06:00 AM – 08:30 PM'
        })

    dynamic_falls = []
    for f in falls_attrs:
        dynamic_falls.append({
            'name': f,
            'landmark': f'{f}, near {dest_title}',
            'desc': f'Natural waterfall cascading through scenic surroundings near {dest_title}.',
            'highlight': 'Natural freshwater splash, scenic photos'
        })
    if not dynamic_falls:
        dynamic_falls.append({
            'name': f'{dest_title} Nature Cascades',
            'landmark': f'Forest Valley, near {dest_title}',
            'desc': 'Scenic mountain stream waterfall with rocky bathing pools and shaded forest banks.',
            'highlight': 'Freshwater splash, nature walk'
        })

    dynamic_hills = []
    for h in hills_attrs:
        dynamic_hills.append({
            'name': h,
            'landmark': f'{h}, {dest_title}',
            'desc': f'Scenic viewpoint and natural attraction in {dest_title}.',
            'highlight': 'Panoramic views, cool breeze'
        })
    if not dynamic_hills:
        cand = general_attrs.pop(0) if general_attrs else f'{dest_title} Sunset Point'
        dynamic_hills.append({
            'name': cand,
            'landmark': f'Hilltop Overlook, {dest_title}',
            'desc': 'High vantage point offering wide views over the area and sunset.',
            'highlight': 'Sunset views, evening breeze'
        })

    dynamic_botanical = []
    for b in botanical_attrs:
        dynamic_botanical.append({
            'name': b,
            'landmark': f'{b}, {dest_title}',
            'desc': f'Popular scenic nature and waterfront attraction in {dest_title}.',
            'highlight': 'Green trees, relaxing walk'
        })
    if not dynamic_botanical:
        cand = general_attrs.pop(0) if general_attrs else f'{dest_title} Central Garden'
        dynamic_botanical.append({
            'name': cand,
            'landmark': f'Park Avenue, {dest_title}',
            'desc': 'Pleasant green park with shady trees and walking paths.',
            'highlight': 'Quiet walks, relaxing benches'
        })

    dynamic_zoo = []
    for z in zoo_attrs:
        dynamic_zoo.append({
            'name': z,
            'landmark': f'{z}, {dest_title}',
            'desc': f'Wildlife habitat and nature reserve in {dest_title}.',
            'highlight': 'Animal watching, birdwatching'
        })
    if not dynamic_zoo:
        dynamic_zoo.append({
            'name': f'{dest_title} Nature & Wildlife Park',
            'landmark': f'Forest Reserve Road, {dest_title}',
            'desc': 'Sprawling wildlife reserve preserving regional deer, birds, and nature.',
            'highlight': 'Safari cart, birdwatching'
        })

    dynamic_spots = {
        'temples': dynamic_temples,
        'hills_viewpoints': dynamic_hills,
        'waterfalls': dynamic_falls,
        'parks_botanical': dynamic_botanical,
        'zoo_wildlife': dynamic_zoo,
        'shopping_malls': [
            {'name': f'{dest_title} Main Market Mall', 'landmark': f'Station Road, {dest_title}', 'desc': 'Modern retail center with shopping stores, food stalls, and entertainment.', 'highlight': 'Shopping, food court'},
            {'name': f'{dest_title} Traditional Bazaar', 'landmark': f'Old Market Road, {dest_title}', 'desc': 'Vibrant local market for traditional clothes, handicrafts, and souvenirs.', 'highlight': 'Local handicrafts, clothes'}
        ],
        'fun_zones_waterparks': [
            {'name': f'{dest_title} Water & Amusement Park', 'landmark': f'Bypass Road, {dest_title}', 'desc': 'Popular family waterpark with wave pool, slides, and fun rides.', 'highlight': 'Wave pool, water slides'}
        ]
    }

    h1_name = stays[0]['name'] if stays else f'{dest_title} Grand Palace Hotel'
    h1_addr = stays[0]['address'] if stays else f'Main Boulevard, {dest_title}'
    h1_phone = stays[0].get('phone', '+91 98480 12345') if stays else '+91 98480 12345'

    h2_name = stays[1]['name'] if len(stays) > 1 else f'{dest_title} Valley Resort'
    h2_addr = stays[1]['address'] if len(stays) > 1 else f'Hilltop Avenue, {dest_title}'
    h2_phone = stays[1].get('phone', '+91 88640 55555') if len(stays) > 1 else '+91 88640 55555'

    dynamic_celebrations = [
        {
            'name': f'{h1_name} Celebration Lawns & Cabanas',
            'map_landmark': f'{h1_addr} (Near Central Commercial Hub across Main Avenue)',
            'vibe': 'Expansive private banquet lawns and poolside dining decks for memorable birthdays and family occasions.',
            'features': 'Private party lawn, personal DJ audio system, customized cake service, and banquet catering.',
            'phone': h1_phone
        },
        {
            'name': f'Skyline Rooftop Lounge at {h2_name}',
            'map_landmark': f'{h2_addr} (Perched atop 6th floor with panoramic city views)',
            'vibe': 'Open-air high-rise terrace with ambient celebratory LED lighting and group party platters.',
            'features': 'VIP celebration cabana, celebratory mood lighting, mocktails, and live acoustic sound.',
            'phone': h2_phone
        }
    ]

    dynamic_dining = {
        'must_try_dishes': [
            {'name': f'Traditional {dest_title} Special Thali', 'type': 'Vegetarian', 'desc': 'Wholesome meal with traditional curries, warm flatbreads, dal, seasonal vegetables, and sweets.', 'best_at': f'Local restaurants near {h1_addr}'},
            {'name': f'{dest_title} Street Food & Hot Snacks', 'type': 'Snack', 'desc': 'Freshly prepared savoury street snacks, sweets, and hot tea.', 'best_at': f'Main Bazaar Food Street, {dest_title}'}
        ],
        'famous_food_streets': [
            {'name': f'{dest_title} Main Food Street', 'landmark': 'Main Market Road (Evening 06:00 PM – 10:30 PM)', 'specialties': 'Local street delicacies, sweets, fresh juices, and hot snacks.'}
        ]
    }

    dynamic_culture = {
        'summary': f'{dest_title} features a rich regional culture rooted in centuries of indigenous craftsmanship, seasonal agricultural festivals, and traditional folklore.',
        'festivals_rituals': [
            {'name': f'Annual {dest_title} Cultural & Temple Festival', 'importance': 'Vibrant community gathering with illuminated temple chariot processions, traditional music, and food fairs.', 'rituals': 'Morning temple rituals, evening cultural dances.'}
        ],
        'art_crafts': 'Handwoven regional textiles, brassware, and traditional wooden carvings.'
    }

    return {
        'destination': dest_title,
        'title': f'{dest_title}, {state if state else "India"}',
        'tagline': f'Discover the Heritage, Natural Splendor & Culinary Flavors of {dest_title}',
        'days': days_count,
        'map_query': f'{dest_title}, {state}',
        'map_embed_url': f"https://maps.google.com/maps?q={urllib.parse.quote_plus(f'{dest_title}, {state}')}&t=&z=11&ie=UTF8&iwloc=&output=embed",
        'tourist_spots': dynamic_spots,
        'dining_cuisine': dynamic_dining,
        'culture_traditions': dynamic_culture,
        'celebrations_venues': dynamic_celebrations,
        'stays': stays[:6],
        'atms': atms,
        'enthusiastic_itinerary': _build_enthusiastic_plan(dest_title, dynamic_spots, days_count)
    }


def _build_enthusiastic_plan(dest_title, spots, days_count):
    """Generates an easy-to-follow, simple everyday English day-by-day itinerary."""
    temples = spots.get('temples', [])
    hills = spots.get('hills_viewpoints', [])
    falls = spots.get('waterfalls', [])
    parks = spots.get('parks_botanical', [])
    zoos = spots.get('zoo_wildlife', [])
    malls = spots.get('shopping_malls', [])
    funs = spots.get('fun_zones_waterparks', [])

    plan = []
    for d in range(1, days_count + 1):
        day_info = {'day_number': d, 'slots': []}
        if d == 1:
            day_info['theme'] = 'Top Sights, City Views & Sunset'
            if temples:
                day_info['slots'].append({'time': '08:30 AM – 11:00 AM', 'title': f"Visit {temples[0]['name']}", 'desc': f"Start early in the morning! Located at {temples[0]['landmark']}. Avoid long lines and pray peacefully.", 'icon': '🛕'})
            day_info['slots'].append({'time': '12:00 PM – 02:00 PM', 'title': 'Tasty Local Lunch & Rest', 'desc': 'Enjoy tasty local food at a good nearby restaurant and rest during the afternoon heat.', 'icon': '🍽️'})
            if parks:
                day_info['slots'].append({'time': '03:00 PM – 04:30 PM', 'title': f"Relax at {parks[0]['name']}", 'desc': f"Pleasant walk among green trees and flowers at {parks[0]['landmark']}.", 'icon': '🌺'})
            if hills:
                day_info['slots'].append({'time': '05:00 PM – 07:30 PM', 'title': f"Sunset View at {hills[0]['name']}", 'desc': f"Head to {hills[0]['landmark']} for cool evening breezes and sunset views.", 'icon': '🌅'})
            day_info['slots'].append({'time': '08:00 PM onwards', 'title': 'Dinner & Relax', 'desc': 'Have a relaxed dinner at a good nearby restaurant.', 'icon': '🌙'})

        elif d == 2:
            day_info['theme'] = 'Waterfalls, Nature & Hill Station'
            if falls:
                day_info['slots'].append({'time': '08:30 AM – 12:30 PM', 'title': f"Visit Waterfalls at {falls[0]['name']}", 'desc': f"Located at {falls[0]['landmark']}. Dip your feet in the cool water and enjoy the morning freshness.", 'icon': '🌊'})
            day_info['slots'].append({'time': '01:00 PM – 02:30 PM', 'title': 'Lunch & Short Nature Walk', 'desc': 'Enjoy lunch and an easy walk under the green trees.', 'icon': '🍗'})
            if len(hills) > 1:
                day_info['slots'].append({'time': '03:30 PM – 06:00 PM', 'title': f"Hill Viewpoint at {hills[1]['name']}", 'desc': f"Located at {hills[1]['landmark']}. Enjoy hot tea or coffee while looking out at the hills.", 'icon': '☕'})
            day_info['slots'].append({'time': '07:00 PM – 10:00 PM', 'title': 'Campfire & Dinner', 'desc': 'Campfire, music, and a tasty dinner with family or friends.', 'icon': '🔥'})

        elif d == 3:
            day_info['theme'] = 'Zoo, Animals, Green Farms & Heritage'
            if zoos:
                day_info['slots'].append({'time': '06:30 AM – 10:30 AM', 'title': f"Zoo & Wildlife at {zoos[0]['name']}", 'desc': f"Located at {zoos[0]['landmark']}. Visit early in the morning when animals and birds are active and easy to spot.", 'icon': '🦁'})
            day_info['slots'].append({'time': '11:30 AM – 02:30 PM', 'title': 'Countryside Walk & Green Farms', 'desc': 'Take a calm walk through green farm fields and village sights.', 'icon': '🌾'})
            if len(temples) > 1:
                day_info['slots'].append({'time': '03:30 PM – 05:30 PM', 'title': f"Visit {temples[1]['name']}", 'desc': f"Located at {temples[1]['landmark']}.", 'icon': '🏛️'})
            day_info['slots'].append({'time': '06:30 PM onwards', 'title': 'Local Evening Street Food & Snacks', 'desc': 'Check out local food stalls for hot snacks and sweets.', 'icon': '🍢'})

        elif d == 4:
            day_info['theme'] = 'Waterpark, Shopping & Fun Zones'
            if funs:
                day_info['slots'].append({'time': '10:00 AM – 03:30 PM', 'title': f"Waterpark & Fun Rides at {funs[0]['name']}", 'desc': f"Located at {funs[0]['landmark']}. Have fun on the water slides, wave pool, and rides.", 'icon': '🎢'})
            if malls:
                day_info['slots'].append({'time': '04:30 PM – 07:30 PM', 'title': f"Shopping & Entertainment at {malls[0]['name']}", 'desc': f"Located at {malls[0]['landmark']}. Shopping stores, food court, and gaming zones.", 'icon': '🛍️'})
            day_info['slots'].append({'time': '08:00 PM onwards', 'title': 'Group Dinner & Celebration', 'desc': 'Enjoy a special dinner together. Great time for cake cutting if celebrating.', 'icon': '🎉'})

        elif d == 5:
            day_info['theme'] = 'Boating, Shopping for Gifts & Final Sunset'
            day_info['slots'].append({'time': '09:00 AM – 11:30 AM', 'title': 'Boating or Lake Walk', 'desc': 'Relax near the water with boating and quiet views.', 'icon': '🚣'})
            if len(malls) > 1:
                day_info['slots'].append({'time': '01:00 PM – 04:00 PM', 'title': f"Shopping for Local Clothes & Sweets at {malls[1]['name']}", 'desc': f"Located at {malls[1]['landmark']}. Buy local famous clothes, traditional items, and gifts to take home.", 'icon': '🧵'})
            day_info['slots'].append({'time': '05:00 PM – 07:30 PM', 'title': 'Farewell Sunset & Group Photos', 'desc': 'Take group photos, enjoy the sunset, and complete your trip happily.', 'icon': '🌅'})
        else:
            day_info['theme'] = f'Day {d} Relaxed Exploration'
            day_info['slots'].append({'time': '10:00 AM – 05:00 PM', 'title': 'Relaxed Day & Local Cafes', 'desc': 'Visit quiet gardens, try local snacks, and enjoy an easy pace.', 'icon': '🌿'})

        plan.append(day_info)
    return plan

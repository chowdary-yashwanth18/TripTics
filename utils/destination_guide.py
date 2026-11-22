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
        guide['stays'] = stays[:5]
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

    a1 = csv_attrs[0] if len(csv_attrs) > 0 else f"{dest_title} Heritage Monument"
    a2 = csv_attrs[1] if len(csv_attrs) > 1 else f"{dest_title} Scenic Viewpoint"
    a3 = csv_attrs[2] if len(csv_attrs) > 2 else f"{dest_title} Central Lakefront"

    dynamic_spots = {
        'temples': [
            {'name': f'Sri {dest_title} Historical Temple', 'landmark': f'Old Town Heritage Lane, near Clock Tower, {dest_title}', 'desc': 'Revered regional shrine with ornate stone carvings and morning spiritual aarti.', 'timing': '06:00 AM – 08:30 PM'},
            {'name': f'{dest_title} Hilltop Shrine', 'landmark': f'Ridge Road Overlook, {dest_title}', 'desc': 'Peaceful panoramic vantage point and sacred spiritual retreat.', 'timing': '06:30 AM – 07:00 PM'}
        ],
        'hills_viewpoints': [
            {'name': f'{dest_title} Sunset Ridge Point', 'landmark': f'Valley View Drive, 4 km from Central Station, {dest_title}', 'desc': 'Highest accessible elevation offering 360-degree vistas over the city and surrounding hills.', 'highlight': 'Golden hour sunset, evening breeze'},
            {'name': a2, 'landmark': f'Scenic Bypass, {dest_title}', 'desc': 'Scenic natural overlook and photography pavilion.', 'highlight': 'Panoramic photos'}
        ],
        'waterfalls': [
            {'name': f'{dest_title} Valley Cascades', 'landmark': f'Forest Reserve Road, 12 km from city center, {dest_title}', 'desc': 'Natural mountain stream waterfall with rocky bathing pools and shaded forest banks.', 'highlight': 'Natural freshwater splash, forest trek'}
        ],
        'parks_botanical': [
            {'name': f'{dest_title} Central Botanical Gardens', 'landmark': f'Civil Lines Road, adjacent to Museum, {dest_title}', 'desc': 'Historic landscaped park with century-old trees, seasonal floral exhibitions, and walking trails.', 'highlight': 'Rose nursery, quiet benches'},
            {'name': a3, 'landmark': f'Promenade Boulevard, {dest_title}', 'desc': 'Scenic waterfront walking track with paddle-boating and green gardens.', 'highlight': 'Evening lake strolls'}
        ],
        'zoo_wildlife': [
            {'name': f'{dest_title} Zoological & Nature Park', 'landmark': f'Forest Sanctuary Highway, {dest_title}', 'desc': 'Sprawling wildlife reserve preserving regional deer, leopards, aviary, and botanical species.', 'highlight': 'Battery safari cart, birdwatching'}
        ],
        'shopping_malls': [
            {'name': f'{dest_title} City Center Mall', 'landmark': f'Main Commercial Avenue, near Metro/Bus Hub, {dest_title}', 'desc': 'Multi-level modern retail hub with department stores, multiplex cinema, and food court.', 'highlight': 'Brand shopping, entertainment'},
            {'name': f'Old Bazaar & Handicraft Street', 'landmark': f'Heritage Market Chowk, {dest_title}', 'desc': 'Vibrant traditional street bazaar for authentic local textiles, handloom sarees, and souvenir keepsakes.', 'highlight': 'Authentic handicrafts, bargain shopping'}
        ],
        'fun_zones_waterparks': [
            {'name': f'{dest_title} Splash Water Park & Fun World', 'landmark': f'Highway Junction, 8 km from town, {dest_title}', 'desc': 'Popular family amusement park with wave pool, spiral water flumes, and adventure rides.', 'highlight': 'Wave pool, thrill slides'}
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
            {'name': f'Traditional {dest_title} Special Thali', 'type': 'Vegetarian', 'desc': 'Wholesome regional platter featuring traditional curries, fresh flatbreads, dal, seasonal vegetable preparations, and authentic dessert.', 'best_at': f'Heritage Dining Hall near {h1_addr}'},
            {'name': f'{dest_title} Street Chaat & Crispy Snacks', 'type': 'Snack', 'desc': 'Freshly prepared savoury roadside street bites seasoned with roasted cumin and tangy tamarind.', 'best_at': 'Main Clock Tower Food Chowk'}
        ],
        'famous_food_streets': [
            {'name': f'{dest_title} Heritage Food Street', 'landmark': 'Old Bazaar Street (Evening 06:00 PM – 11:00 PM)', 'specialties': 'Local street delicacies, sweets, fresh fruit juices, and midnight savouries.'}
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
        'stays': stays[:5],
        'atms': atms,
        'enthusiastic_itinerary': _build_enthusiastic_plan(dest_title, dynamic_spots, days_count)
    }


def _build_enthusiastic_plan(dest_title, spots, days_count):
    """Generates an energetic, enthusiastic day-by-day itinerary maximizing fun and minimizing transit."""
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
            day_info['theme'] = 'Spiritual Heritage, Grand City Vistas & Sunset Chill'
            if temples:
                day_info['slots'].append({'time': '08:30 AM – 11:00 AM', 'title': f"Sacred Darshan at {temples[0]['name']}", 'desc': f"Start your holiday early! Located at {temples[0]['landmark']}. Beat midday queues and experience morning aarti peace.", 'icon': '🛕'})
            day_info['slots'].append({'time': '12:00 PM – 02:00 PM', 'title': 'Authentic Local Feast & Cultural Stroll', 'desc': 'Savor signature regional cuisine at an authentic heritage eatery during peak heat.', 'icon': '🍽️'})
            if parks:
                day_info['slots'].append({'time': '03:00 PM – 04:30 PM', 'title': f"Botanical Stroll at {parks[0]['name']}", 'desc': f"Shaded peaceful walk at {parks[0]['landmark']}.", 'icon': '🌺'})
            if hills:
                day_info['slots'].append({'time': '05:00 PM – 07:30 PM', 'title': f"Golden Hour Sunset at {hills[0]['name']}", 'desc': f"Head up to {hills[0]['landmark']} for cool breezes and breathtaking panoramic views.", 'icon': '🌅'})
            day_info['slots'].append({'time': '08:00 PM onwards', 'title': 'Celebratory Group Dinner & Leisure Stroll', 'desc': 'Relax at a rooftop lounge or open-air garden restaurant with live music.', 'icon': '🌙'})

        elif d == 2:
            day_info['theme'] = 'Cascading Waterfalls, Nature Trails & Mountain Breezes'
            if falls:
                day_info['slots'].append({'time': '08:30 AM – 12:30 PM', 'title': f"Gushing Cascades at {falls[0]['name']}", 'desc': f"Located at {falls[0]['landmark']}. Dip your feet in natural rock streams and enjoy morning freshness.", 'icon': '🌊'})
            day_info['slots'].append({'time': '01:00 PM – 02:30 PM', 'title': 'Shaded Forest Picnic & Bamboo Delicacies', 'desc': 'Authentic outdoor rustic lunch with fresh regional delicacies.', 'icon': '🍗'})
            if len(hills) > 1:
                day_info['slots'].append({'time': '03:30 PM – 06:00 PM', 'title': f"Mountain Ridge Exploration at {hills[1]['name']}", 'desc': f"Located at {hills[1]['landmark']}. Savor hot local tea looking over cloud-filled valleys.", 'icon': '☕'})
            day_info['slots'].append({'time': '07:00 PM – 10:00 PM', 'title': 'Campfire Circle & Barbecue Night', 'desc': 'Private resort lawn campfire with starry night acoustic music.', 'icon': '🔥'})

        elif d == 3:
            day_info['theme'] = 'Wildlife Safari, Animal Encounters & Rolling Countryside'
            if zoos:
                day_info['slots'].append({'time': '06:30 AM – 10:30 AM', 'title': f"Wildlife Tracking Safari at {zoos[0]['name']}", 'desc': f"Located at {zoos[0]['landmark']}. Early morning slot when wildlife is actively roaming.", 'icon': '🦁'})
            day_info['slots'].append({'time': '11:30 AM – 02:30 PM', 'title': 'Rolling Countryside Farms & Agro-Tour', 'desc': 'Drive through agricultural crop fields, organic fruit orchards, and pastoral hamlets.', 'icon': '🌾'})
            if len(temples) > 1:
                day_info['slots'].append({'time': '03:30 PM – 05:30 PM', 'title': f"Ancient Architectural Wonder at {temples[1]['name']}", 'desc': f"Located at {temples[1]['landmark']}.", 'icon': '🏛️'})
            day_info['slots'].append({'time': '06:30 PM onwards', 'title': 'Night Bazaar & Street Food Trail', 'desc': 'Explore bustling evening bazaars for hot savouries and regional sweets.', 'icon': '🍢'})

        elif d == 4:
            day_info['theme'] = 'Thrilling Waterparks, Shopping Malls & High-Energy Fun'
            if funs:
                day_info['slots'].append({'time': '10:00 AM – 03:30 PM', 'title': f"Water Splash Adventure at {funs[0]['name']}", 'desc': f"Located at {funs[0]['landmark']}. High-speed water flumes, wave pools, and rain dance.", 'icon': '🎢'})
            if malls:
                day_info['slots'].append({'time': '04:30 PM – 07:30 PM', 'title': f"Retail Therapy & Entertainment at {malls[0]['name']}", 'desc': f"Located at {malls[0]['landmark']}. International brands, IMAX cinema, and gaming zones.", 'icon': '🛍️'})
            day_info['slots'].append({'time': '08:00 PM onwards', 'title': 'Rooftop Party Deck Celebration', 'desc': 'Celebrate with your group at a top-floor party cabana with city lights.', 'icon': '🎉'})

        elif d == 5:
            day_info['theme'] = 'Hidden Natural Gems, Handloom Shopping & Farewell Golden Hour'
            day_info['slots'].append({'time': '09:00 AM – 11:30 AM', 'title': 'Peaceful Hidden Lakefront or River Crossing', 'desc': 'Escape the crowds for quiet row-boating and birdwatching.', 'icon': '🚣'})
            if len(malls) > 1:
                day_info['slots'].append({'time': '01:00 PM – 04:00 PM', 'title': f"Traditional Artisan Handicraft Shopping at {malls[1]['name']}", 'desc': f"Located at {malls[1]['landmark']}. Authentic handwoven textiles, spices, and keepsakes.", 'icon': '🧵'})
            day_info['slots'].append({'time': '05:00 PM – 07:30 PM', 'title': 'Farewell Panoramic Sunset Overlook', 'desc': 'Watch the golden sun dip below the horizon with group memories and photos.', 'icon': '🌅'})
        else:
            day_info['theme'] = f'Day {d} Off-Beat Exploration'
            day_info['slots'].append({'time': '10:00 AM – 05:00 PM', 'title': 'Slow-Paced Countryside & Cafe Hopping', 'desc': 'Relax in quiet hill gardens, local art galleries, and quaint artisan cafes.', 'icon': '🌿'})

        plan.append(day_info)
    return plan

# 🌍 TripTics – Budget-Friendly Trip Planner using Data Analytics

> **B.Tech Data Analytics Essentials – Semester Project**
> Developer: Chowdary Yashwanth · [chowdaryyashwanth18@gmail.com](mailto:chowdaryyashwanth18@gmail.com)
> GitHub: [github.com/chowdary-yashwanth18/TripTics](https://github.com/chowdary-yashwanth18/TripTics)

---

## 📌 Project Overview

**TripTics** is a data-driven web application that helps budget-conscious travelers plan trips across India. A user enters their total budget, number of days, number of travelers, and trip preferences — the system then recommends the top 3 matching destinations with a full cost breakdown and analytics dashboard.

The project demonstrates how data analytics concepts (filtering, scoring, aggregation, and visualization) can be applied to a real-world problem that students and young travelers face every day.

---

## 🚨 Problem Statement

Planning a budget trip in India is difficult. Travelers often:

- Don't know which destinations are affordable for their group size
- Can't easily estimate hotel + food + transport costs per trip
- Have no data-backed way to compare destinations by budget level or trip type

**TripTics** solves this by combining a curated travel cost dataset, a rule-based recommendation engine, and an interactive analytics dashboard into a single Flask web app.

---

## 📊 Why This Fits Data Analytics Essentials

| Analytics Concept | How TripTics Uses It |
|---|---|
| Data Collection | 125-row CSV dataset with real-world cost estimates |
| Data Cleaning | Pandas type coercion, normalization, null handling in `data_loader.py` |
| Descriptive Analytics | KPI cards: cheapest daily cost, avg hotel rate, best trip type |
| Exploratory Analysis | 7 interactive Plotly charts on the analytics dashboard |
| Rule-based Scoring | 100-point scoring model in `recommender.py` |
| Aggregation | `groupby` for type-wise and state-wise cost comparisons |
| Data Storytelling | Key Insights section derived automatically from dataset |

---

## ✨ Key Features

- 🎯 **Smart Recommendation Engine** – Scores destinations using 4 factors: trip type match, budget fit comfort, days relevance, and budget level preference
- 💰 **Accurate Cost Calculation** – Formula: `Travel + (Hotel × days) + (Food × travelers × days) + (Local Transport × days)`
- 📊 **Analytics Dashboard** – 7 interactive Plotly charts with KPI cards and auto-generated insights
- 🔍 **No-match Handling** – When budget is too low, shows nearest alternatives and actionable suggestions
- 🏷️ **Crowd Level & Family Tags** – Optional metadata on each recommendation card
- 📱 **Responsive Design** – Works on desktop, tablet, and mobile

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.x, Flask |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly (interactive), Plotly Express |
| Frontend | HTML5, Bootstrap 5, Vanilla CSS |
| Data Source | CSV file (125 Indian destinations) |
| Font | Google Fonts – Outfit |

---

## 📁 Folder Structure

```
TripTics/
│
├── app.py                  ← Flask app entry point (routes + request handling)
├── requirements.txt        ← Python dependencies
├── generate_data.py        ← Script used to generate destinations.csv
├── smoke_test.py           ← Quick backend test script
│
├── data/
│   └── destinations.csv    ← Main dataset (125 Indian travel destinations)
│
├── utils/
│   ├── data_loader.py      ← CSV loading + data type normalization
│   ├── recommender.py      ← Cost calculator + scoring engine
│   └── analytics.py        ← Plotly chart generation + KPI/insights functions
│
├── templates/
│   ├── base.html           ← Shared navbar + layout
│   ├── index.html          ← Home / landing page
│   ├── planner.html        ← Trip planner form
│   ├── results.html        ← Recommendation results page
│   └── dashboard.html      ← Analytics dashboard
│
└── static/
    └── css/
        └── style.css       ← Custom CSS (glassmorphism + dashboard styles)
```

---

## 🗂️ Dataset Description

**File:** `data/destinations.csv`
**Rows:** 125 Indian travel destinations

| Column | Type | Description |
|---|---|---|
| `Destination` | String | Name of the place |
| `State` | String | Indian state |
| `Type` | String | Beach / Hill / Nature / Temple / City |
| `Avg_Travel_Cost` | Integer | One-way travel cost estimate (₹) |
| `Avg_Hotel_Per_Day` | Integer | Avg hotel/night cost (₹) |
| `Avg_Food_Per_Day_Per_Person` | Integer | Avg food cost per person per day (₹) |
| `Avg_Local_Travel_Per_Day` | Integer | Local transport cost per day (₹) |
| `Best_Season` | String | Winter / Summer / Monsoon / All |
| `Budget_Level` | String | Low / Medium / High |
| `Recommended_Days` | Integer | Suggested trip duration |
| `Crowd_Level` | String | Low / Medium / High |
| `Family_Friendly` | String | Yes / No |

**Coverage:** Andhra Pradesh, Telangana, Tamil Nadu, Karnataka, Kerala, Goa, Maharashtra

---

## 🧠 Recommendation Logic Overview

### Step 1 – Cost Calculation
```
Total = Travel + (Hotel × days) + (Food × travelers × days) + (Local × days)
```

### Step 2 – 100-Point Scoring
| Factor | Max Points | Logic |
|---|---|---|
| Trip type match | 30 | 30 if exact match, 20 if "Any" selected |
| Budget fit comfort | 25 | 25 if uses 75–100% of budget, less for under-usage |
| Days relevance | 25 | Compares user days vs `Recommended_Days` column |
| Budget level match | 20 | 20 for exact match, 8 for adjacent level |

### Step 3 – Ranking
- Destinations within budget → sorted by **Score DESC**
- If no match → top 3 over-budget alternatives + actionable suggestions

---

## 📈 Dashboard / Analytics Overview

| Chart | Purpose |
|---|---|
| Top 10 Cheapest Destinations | Horizontal bar – daily running cost comparison |
| Destinations by Trip Type | Donut – dataset category distribution |
| Hotel vs Food Cost by Type | Grouped bar – side-by-side cost comparison |
| Avg Full Trip Cost by Budget Level | Bar – Low vs Medium vs High full trip cost |
| Top States by Destination Count | Horizontal bar – geographic coverage |
| Avg Recommended Duration by Type | Bar – days by trip category |
| Budget Level Mix | Donut – Low/Medium/High dataset split |

**KPI Cards (auto-calculated from dataset):**
- Total Destinations
- Cheapest Daily Cost
- Avg Hotel/Night
- Most Affordable Trip Type

---

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/chowdary-yashwanth18/TripTics.git
cd TripTics
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Flask App
```bash
python app.py
```

### 4. Open in Browser
```
http://127.0.0.1:5000
```

> **Note:** Python 3.8+ recommended. No database setup required.

---

## 🧪 Example User Inputs & Outputs

| Input | Value |
|---|---|
| Total Budget | ₹15,000 |
| Number of Days | 3 |
| Number of Travelers | 2 |
| Trip Type | Beach |
| Budget Style | Low |

**Example Output:**
1. 🏖️ **Suryalanka, Andhra Pradesh** – Score: 93/100 – Total: ₹8,053
2. 🏖️ **Tarkarli, Maharashtra** – Score: 88/100 – Total: ₹11,985
3. 🏖️ **Gokarna, Karnataka** – Score: 88/100 – Total: ₹14,269

---

## 📸 Screenshots

> *(Take screenshots after running the app and place them in a `screenshots/` folder)*

| Page | Preview |
|---|---|
| Home Page | `screenshots/home.png` |
| Planner Form | `screenshots/planner.png` |
| Results Page | `screenshots/results.png` |
| Analytics Dashboard | `screenshots/dashboard.png` |

---

## ⚠️ Limitations

- Travel cost data is estimated — not fetched from live APIs
- Prices are static (no inflation adjustment or seasonal pricing)
- No user authentication or saved trip history
- Recommendation engine is rule-based, not ML-based
- Dataset covers only 7 Indian states (extendable)
- Does not consider flight/train booking or real-time availability

---

## 🔭 Future Scope

- Integrate live transport cost APIs (IRCTC, MakeMyTrip)
- Add a user account system to save and compare trip plans
- Introduce ML-based recommendation using collaborative filtering
- Expand dataset to cover all 28 Indian states
- Add PDF trip report export feature
- Add travel time estimation from starting city

---

## 📄 License

This project is submitted as an academic semester project.
Feel free to fork and build upon it with attribution.

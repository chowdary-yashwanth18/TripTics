import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go


# ─────────────────────────────────────────────────────────────────────────────
# KPI METRICS
# ─────────────────────────────────────────────────────────────────────────────

def get_kpi_metrics(df):
    """
    Calculates the 4 headline KPI cards shown at the top of the dashboard.
    All values come directly from the dataset — easy to explain in viva.

    Returns a dict with:
        total_destinations  – total rows in dataset
        cheapest_daily      – minimum Base_Cost_Per_Day across all rows
        avg_hotel           – mean hotel cost per night across all destinations
        best_type           – destination type with the lowest avg daily cost
    """
    df = df.copy()

    # Daily running cost (excludes one-time travel cost for fair comparison)
    df['Base_Cost_Per_Day'] = (
        df['Avg_Hotel_Per_Day'] +
        df['Avg_Food_Per_Day_Per_Person'] +
        df['Avg_Local_Travel_Per_Day']
    )

    best_type_row = (
        df.groupby('Type')['Base_Cost_Per_Day']
        .mean()
        .idxmin()
    )

    return {
        'total_destinations': len(df),
        'cheapest_daily':     f"{int(df['Base_Cost_Per_Day'].min()):,}",
        'avg_hotel':          f"{int(df['Avg_Hotel_Per_Day'].mean()):,}",
        'best_type':          best_type_row,
    }


# ─────────────────────────────────────────────────────────────────────────────
# KEY INSIGHTS (bottom section)
# ─────────────────────────────────────────────────────────────────────────────

def get_key_insights(df):
    """
    Derives 5 plain-English data insights from the dataset.
    Each insight is a dict: { icon, title, text }
    """
    df = df.copy()
    df['Base_Cost_Per_Day'] = (
        df['Avg_Hotel_Per_Day'] +
        df['Avg_Food_Per_Day_Per_Person'] +
        df['Avg_Local_Travel_Per_Day']
    )

    # 1. Most expensive type for hotels
    priciest_hotel_type = df.groupby('Type')['Avg_Hotel_Per_Day'].mean().idxmax()
    priciest_hotel_val  = int(df.groupby('Type')['Avg_Hotel_Per_Day'].mean().max())

    # 2. Cheapest overall type
    cheapest_type     = df.groupby('Type')['Base_Cost_Per_Day'].mean().idxmin()
    cheapest_type_val = int(df.groupby('Type')['Base_Cost_Per_Day'].mean().min())

    # 3. Temple budget tendency
    temple_pct_low = 0
    temple_df = df[df['Type'] == 'Temple']
    if len(temple_df) > 0:
        temple_pct_low = int(
            (temple_df['Budget_Level'] == 'Low').sum() / len(temple_df) * 100
        )

    # 4. Most represented state
    top_state     = df['State'].value_counts().idxmax()
    top_state_cnt = int(df['State'].value_counts().max())

    # 5. Avg recommended trip duration by cheapest type
    avg_days_cheapest = round(
        df[df['Type'] == cheapest_type]['Recommended_Days'].mean(), 1
    )

    return [
        {
            'icon': '🏨',
            'title': f'{priciest_hotel_type} trips have the highest hotel cost',
            'text':  f'On average, {priciest_hotel_type.lower()} destinations cost '
                     f'₹{priciest_hotel_val:,}/night for accommodation – the most of any category.'
        },
        {
            'icon': '💸',
            'title': f'{cheapest_type} is the most budget-friendly trip type',
            'text':  f'The average daily running cost for {cheapest_type.lower()} trips is '
                     f'₹{cheapest_type_val:,}/day – making them ideal for tight budgets.'
        },
        {
            'icon': '🛕',
            'title': f'{temple_pct_low}% of Temple destinations are Low-budget',
            'text':  'Temple and pilgrimage towns tend to be among the most affordable options, '
                     'with low hotel and food costs driven by large pilgrim economies.'
        },
        {
            'icon': '📍',
            'title': f'{top_state} has the most listed destinations ({top_state_cnt})',
            'text':  f'With {top_state_cnt} destinations in our dataset, {top_state} offers '
                     'the widest range of trip options – from beaches to temples to hill stations.'
        },
        {
            'icon': '📅',
            'title': f'Ideal trip length for {cheapest_type} trips: {avg_days_cheapest} days',
            'text':  f'Data suggests that {avg_days_cheapest}-day {cheapest_type.lower()} trips '
                     'offer the best value — long enough to explore but short enough to stay on budget.'
        },
    ]


# ─────────────────────────────────────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────────────────────────────────────

def generate_analytics_charts(df):
    """
    Generates 7 Plotly charts for the redesigned dashboard.
    Works on a copy of df to prevent mutating the shared DataFrame.

    Returns a dict of HTML div strings keyed by chart name.
    """
    charts = {}
    if df.empty:
        return charts

    df = df.copy()
    template = 'plotly_white'

    # Ensure numerics
    for col in ['Avg_Hotel_Per_Day', 'Avg_Food_Per_Day_Per_Person',
                'Avg_Local_Travel_Per_Day', 'Avg_Travel_Cost', 'Recommended_Days']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    df['Base_Cost_Per_Day'] = (
        df['Avg_Hotel_Per_Day'] +
        df['Avg_Food_Per_Day_Per_Person'] +
        df['Avg_Local_Travel_Per_Day']
    )

    COLORS = px.colors.qualitative.Vivid

    # ── Chart 1: Top 10 cheapest destinations (horizontal bar) ───────────────
    cheapest = df.sort_values('Base_Cost_Per_Day').head(10).sort_values(
        'Base_Cost_Per_Day', ascending=True
    )
    fig1 = px.bar(
        cheapest, y='Destination', x='Base_Cost_Per_Day', orientation='h',
        title='Top 10 Cheapest Destinations by Daily Cost',
        labels={'Base_Cost_Per_Day': 'Daily Cost (₹)', 'Destination': ''},
        color='Base_Cost_Per_Day',
        color_continuous_scale='Blues',
        template=template,
        text='Base_Cost_Per_Day'
    )
    fig1.update_traces(texttemplate='₹%{text:,}', textposition='outside')
    fig1.update_layout(
        margin=dict(l=10, r=30, t=50, b=10),
        coloraxis_showscale=False,
        height=380
    )
    charts['cheapest_destinations'] = pio.to_html(
        fig1, full_html=False, include_plotlyjs='cdn'
    )

    # ── Chart 2: Destination count by type (donut) ───────────────────────────
    type_counts = df['Type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Count']
    fig2 = px.pie(
        type_counts, values='Count', names='Type',
        title='Destinations by Trip Type',
        hole=0.45,
        color_discrete_sequence=COLORS,
        template=template
    )
    fig2.update_traces(textinfo='label+percent', pull=[0.03]*len(type_counts))
    fig2.update_layout(showlegend=True, height=380, margin=dict(t=60, b=20))
    charts['type_distribution'] = pio.to_html(
        fig2, full_html=False, include_plotlyjs=False
    )

    # ── Chart 3: Avg hotel vs food cost by type (grouped bar) ────────────────
    grouped = df.groupby('Type').agg(
        Hotel=('Avg_Hotel_Per_Day', 'mean'),
        Food=('Avg_Food_Per_Day_Per_Person', 'mean')
    ).reset_index()
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        name='Hotel/Night (₹)', x=grouped['Type'], y=grouped['Hotel'].round(),
        marker_color='#4F46E5'
    ))
    fig3.add_trace(go.Bar(
        name='Food/Person/Day (₹)', x=grouped['Type'], y=grouped['Food'].round(),
        marker_color='#06B6D4'
    ))
    fig3.update_layout(
        title='Hotel vs Food Cost by Destination Type',
        barmode='group',
        template=template,
        height=380,
        margin=dict(t=60, b=20),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    charts['hotel_vs_food'] = pio.to_html(
        fig3, full_html=False, include_plotlyjs=False
    )

    # ── Chart 4: Average trip cost by Budget_Level ───────────────────────────
    df['Full_Trip_Cost'] = (
        df['Avg_Travel_Cost'] +
        df['Avg_Hotel_Per_Day'] * df['Recommended_Days'] +
        df['Avg_Food_Per_Day_Per_Person'] * 2 * df['Recommended_Days'] +
        df['Avg_Local_Travel_Per_Day'] * df['Recommended_Days']
    )
    cost_by_level = df.groupby('Budget_Level')['Full_Trip_Cost'].mean().reset_index()
    cost_by_level.columns = ['Budget Level', 'Avg Full Trip Cost']
    # Sort meaningfully
    level_order = ['Low', 'Medium', 'High']
    cost_by_level['Budget Level'] = pd.Categorical(
        cost_by_level['Budget Level'], categories=level_order, ordered=True
    )
    cost_by_level = cost_by_level.sort_values('Budget Level')

    fig4 = px.bar(
        cost_by_level, x='Budget Level', y='Avg Full Trip Cost',
        title='Average Full Trip Cost by Budget Level',
        color='Budget Level',
        color_discrete_map={'Low': '#22c55e', 'Medium': '#f59e0b', 'High': '#ef4444'},
        template=template,
        text='Avg Full Trip Cost',
        labels={'Avg Full Trip Cost': 'Avg Cost (₹)'}
    )
    fig4.update_traces(
        texttemplate='₹%{text:,.0f}', textposition='outside'
    )
    fig4.update_layout(
        showlegend=False, height=380,
        margin=dict(t=60, b=20)
    )
    charts['cost_by_budget_level'] = pio.to_html(
        fig4, full_html=False, include_plotlyjs=False
    )

    # ── Chart 5: State-wise destination count (horizontal bar, top 10) ───────
    state_counts = df['State'].value_counts().head(10).reset_index()
    state_counts.columns = ['State', 'Count']
    fig5 = px.bar(
        state_counts, y='State', x='Count', orientation='h',
        title='Top States by Number of Destinations',
        color='Count',
        color_continuous_scale='Purples',
        template=template,
        labels={'Count': 'No. of Destinations', 'State': ''},
        text='Count'
    )
    fig5.update_traces(textposition='outside')
    fig5.update_layout(
        coloraxis_showscale=False, height=380,
        margin=dict(l=10, r=30, t=60, b=10)
    )
    charts['state_distribution'] = pio.to_html(
        fig5, full_html=False, include_plotlyjs=False
    )

    # ── Chart 6: Avg recommended trip duration by type ───────────────────────
    avg_days = df.groupby('Type')['Recommended_Days'].mean().reset_index()
    avg_days.columns = ['Type', 'Avg Days']
    avg_days['Avg Days'] = avg_days['Avg Days'].round(1)
    fig6 = px.bar(
        avg_days, x='Type', y='Avg Days',
        title='Average Recommended Trip Duration by Type',
        color='Type',
        color_discrete_sequence=COLORS,
        template=template,
        labels={'Avg Days': 'Days'},
        text='Avg Days'
    )
    fig6.update_traces(textposition='outside')
    fig6.update_layout(
        showlegend=False, height=380,
        margin=dict(t=60, b=20)
    )
    charts['avg_trip_duration'] = pio.to_html(
        fig6, full_html=False, include_plotlyjs=False
    )

    # ── Chart 7: Budget level distribution (donut) ───────────────────────────
    level_counts = df['Budget_Level'].value_counts().reset_index()
    level_counts.columns = ['Level', 'Count']
    fig7 = px.pie(
        level_counts, values='Count', names='Level',
        title='Budget Level Mix in Dataset',
        hole=0.5,
        color='Level',
        color_discrete_map={'Low': '#22c55e', 'Medium': '#f59e0b', 'High': '#ef4444'},
        template=template
    )
    fig7.update_traces(textinfo='label+percent', pull=[0.03]*len(level_counts))
    fig7.update_layout(height=380, margin=dict(t=60, b=20))
    charts['budget_distribution'] = pio.to_html(
        fig7, full_html=False, include_plotlyjs=False
    )

    return charts

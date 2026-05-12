import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

# Load custom page icon image
# Place your icon image (e.g. icon.png) in the same folder as app.py
try:
    page_icon = Image.open("icon.png")
except FileNotFoundError:
    page_icon = "🕯️"  # fallback if image is missing

st.set_page_config(
    page_title="Samsara — A Story of BaBa",
    page_icon=page_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Lora', serif !important;
}

.main { background-color: #FAF7F2; }
[data-testid="stSidebar"] { background-color: #F2EDE4; }

.story-quote {
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 1.15rem;
    color: #5C4A32;
    border-left: 3px solid #C4956A;
    padding: 1rem 1.5rem;
    margin: 1.5rem 0;
    background: #FDF5EC;
    border-radius: 0 8px 8px 0;
    line-height: 1.8;
}

.metric-card {
    background: #FFFFFF;
    border: 1px solid #E8DDD0;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}

.metric-label {
    font-size: 0.78rem;
    color: #8C7560;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 4px;
}

.metric-value {
    font-family: 'Lora', serif;
    font-size: 2rem;
    font-weight: 600;
    color: #3D2B1F;
}

.section-header {
    font-family: 'Lora', serif;
    font-size: 1.4rem;
    color: #3D2B1F;
    border-bottom: 1.5px solid #E8DDD0;
    padding-bottom: 0.5rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

.insight-box {
    background: #FDF5EC;
    border: 1px solid #E8DDD0;
    border-left: 4px solid #C4956A;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.2rem;
    margin: 0.75rem 0;
    font-size: 0.92rem;
    color: #4A3728;
    line-height: 1.7;
}

.ethics-block {
    background: #F5F0E8;
    border: 1px solid #DDD4C5;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin: 0.75rem 0;
}

.ethics-title {
    font-weight: 500;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #8C7560;
    margin-bottom: 0.4rem;
}

.badge {
    display: inline-block;
    background: #EDE0D0;
    color: #5C4A32;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.78rem;
    font-weight: 500;
    margin: 2px;
}

.stButton > button {
    background: #3D2B1F;
    color: white;
    border: none;
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    padding: 0.4rem 1.2rem;
}

.stButton > button:hover {
    background: #C4956A;
    color: white;
}

footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("baba_memories_dataset.csv")
    def get_era(stage):
        if 'Early Childhood' in stage or stage == 'Childhood':
            return 'Childhood'
        elif 'High School' in stage:
            return 'High School'
        elif 'University' in stage and 'Parami' not in stage and 'Post' not in stage:
            return 'University (Mandalay)'
        elif 'Post' in stage or 'Political' in stage:
            return 'Crisis & Loss'
        else:
            return 'Parami / Chiang Mai'
    df['era'] = df['life_stage'].apply(get_era)
    df['relationship_closeness_score'] = pd.to_numeric(df['relationship_closeness_score'], errors='coerce')
    return df

df = load_data()

COLORS = {
    'primary':   '#3D2B1F',
    'accent':    '#C4956A',
    'warm':      '#E8A87C',
    'soft':      '#F2DEC8',
    'teal':      '#5B9E8F',
    'coral':     '#D4715A',
    'muted':     '#8C7560',
    'bg':        '#FAF7F2',
}

ERA_ORDER = ['Childhood', 'High School', 'University (Mandalay)', 'Crisis & Loss', 'Parami / Chiang Mai']
ERA_COLORS = {
    'Childhood':             '#5B9E8F',
    'High School':           '#C4956A',
    'University (Mandalay)': '#7F77DD',
    'Crisis & Loss':         '#D4715A',
    'Parami / Chiang Mai':   '#888780',
}

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem;'>
        <div style='font-size: 2rem;'>🕯️</div>
        <div style='font-family: Lora, serif; font-size: 1.1rem; color: #3D2B1F; font-weight: 600;'>Samsara</div>
        <div style='font-size: 0.78rem; color: #8C7560; margin-top: 2px;'>A story of BaBa & me</div>
    </div>
    <hr style='border-color: #E8DDD0; margin: 0.75rem 0;'>
    """, unsafe_allow_html=True)

    st.markdown("**Navigate**")
    page = st.radio(
        "",
        ["📖 Story Overview", "📊 Data Visualizations", "🔍 Key Insights", "🎯 Decision-Making", "⚖️ Ethics & Responsibility"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color: #E8DDD0; margin: 0.75rem 0;'>", unsafe_allow_html=True)
    st.markdown("**Filters**")
    era_options = ERA_ORDER
    selected_eras = st.multiselect("Life era", era_options, default=era_options)
    year_range = st.slider("Year range", int(df.year.min()), int(df.year.max()), (1998, 2025))

    filtered_df = df[
        (df['era'].isin(selected_eras)) &
        (df['year'] >= year_range[0]) &
        (df['year'] <= year_range[1])
    ]

    st.markdown("<hr style='border-color: #E8DDD0; margin: 0.75rem 0;'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:0.78rem; color:#8C7560;'>Showing <b>{len(filtered_df)}</b> of <b>{len(df)}</b> records</div>", unsafe_allow_html=True)


# ─── PAGE 1: STORY OVERVIEW ──────────────────────────────────────────────────
if page == "📖 Story Overview":
    st.markdown("<h1 style='font-family:Lora,serif; color:#3D2B1F; font-size:2.4rem; margin-bottom:0;'>Samsara</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8C7560; font-size:1rem; margin-top:4px;'>A data story about the man I will never forget — my BaBa</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class='story-quote'>
        "No matter how early I woke up in the morning, BaBa was always awake before me.
        He had already boiled water and was waiting for me, preparing my favorite breakfast —
        Mont T, along with plain tea or sometimes coffee."
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <p style='color:#4A3728; line-height:1.9; font-size:0.97rem;'>
        BaBa — the husband of my grandmother's sister — lived just across the yard from my childhood home
        in Myanmar. He was not my grandfather by blood, but he was the one who held me when my father's
        discipline was too harsh. He was the one who applied medicine to my wounds, shared stories at
        night, and gave me his own clothing when I had none.
        </p>
        <p style='color:#4A3728; line-height:1.9; font-size:0.97rem;'>
        As I moved away — to high school in Monywa, then university in Mandalay — my visits grew rarer.
        Life pulled me forward. In November 2020, during my fourth university year, BaBa suffered a
        sudden stroke. He passed away at 72. I had planned to bring him a good bottle of liquor after
        my midterms. I never got the chance.
        </p>
        <p style='color:#4A3728; line-height:1.9; font-size:0.97rem;'>
        This project transforms those memories into data — not to make loss feel mechanical,
        but to find the patterns that grief alone cannot see clearly.
        </p>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-header' style='font-size:1rem; margin-top:0;'>Journey at a glance</div>", unsafe_allow_html=True)
        timeline = [
            ("1998", "Born in Myanmar hometown"),
            ("2003", "Started primary school"),
            ("2013", "Moved to Monywa for high school"),
            ("2015", "Passed matriculation exam"),
            ("2016", "Started university, Mandalay"),
            ("2020", "BaBa passed away — November"),
            ("2021", "Left university; joined CDM"),
            ("2023", "Enrolled at Parami University"),
            ("2024", "Relocated to Chiang Mai"),
            ("2025", "Continuing studies in Thailand"),
        ]
        for yr, evt in timeline:
            dot_color = "#D4715A" if yr == "2020" else "#C4956A"
            st.markdown(f"""
            <div style='display:flex; align-items:flex-start; gap:10px; margin-bottom:8px;'>
                <div style='min-width:36px; font-size:0.72rem; font-weight:500; color:#8C7560; padding-top:2px;'>{yr}</div>
                <div style='width:8px; height:8px; border-radius:50%; background:{dot_color}; margin-top:4px; flex-shrink:0;'></div>
                <div style='font-size:0.82rem; color:#4A3728; line-height:1.5;'>{evt}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Why this story matters</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    cards = [
        ("27 years", "of data spanning birth to present"),
        ("50 → 0", "visits/year — the drift made visible"),
        ("Samsara", "impermanence as the core theme"),
    ]
    for col, (val, desc) in zip([c1, c2, c3], cards):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{val}</div>
                <div class='metric-label'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# ─── PAGE 2: DATA VISUALIZATIONS ─────────────────────────────────────────────
elif page == "📊 Data Visualizations":
    st.markdown("<h2 class='section-header' style='margin-top:0;'>Data visualizations</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#8C7560; font-size:0.9rem;'>Filtered to {len(filtered_df)} records · {year_range[0]}–{year_range[1]}</p>", unsafe_allow_html=True)

    # Chart 1: Dual axis — visits + emotion over time
    st.markdown("<div class='section-header'>Visit frequency & emotional impact over time</div>", unsafe_allow_html=True)

    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(go.Scatter(
        x=filtered_df['year'], y=filtered_df['visit_frequency_to_baba_per_year'],
        name="Visits / year", fill='tozeroy',
        fillcolor='rgba(91,158,143,0.15)', line=dict(color='#5B9E8F', width=2.5),
        mode='lines+markers', marker=dict(size=5)
    ), secondary_y=False)
    fig1.add_trace(go.Scatter(
        x=filtered_df['year'], y=filtered_df['emotional_impact_score'],
        name="Emotional impact", line=dict(color='#D4715A', width=2.5, dash='dot'),
        mode='lines+markers',
        marker=dict(
            size=[12 if y == 2020 else 5 for y in filtered_df['year']],
            color=['#D4715A' if y == 2020 else '#D4715A' for y in filtered_df['year']],
            symbol=['star' if y == 2020 else 'circle' for y in filtered_df['year']]
        )
    ), secondary_y=True)

    if 2020 in filtered_df['year'].values:
        fig1.add_vline(x=2020, line_dash="dash", line_color="#D4715A", line_width=1, opacity=0.5)
        fig1.add_annotation(x=2020, y=10, text="BaBa passed away", showarrow=True,
                            arrowhead=2, arrowcolor="#D4715A", font=dict(color="#D4715A", size=11),
                            ax=40, ay=-30, secondary_y=True)

    fig1.update_layout(
        plot_bgcolor='#FAF7F2', paper_bgcolor='#FAF7F2',
        font=dict(family='DM Sans', color='#3D2B1F'),
        legend=dict(orientation='h', y=1.08, x=0),
        margin=dict(t=40, b=30, l=10, r=10), height=360,
        hovermode='x unified'
    )
    fig1.update_yaxes(title_text="Visits per year", secondary_y=False, gridcolor='#E8DDD0')
    fig1.update_yaxes(title_text="Emotional impact (1–10)", secondary_y=True, range=[0, 12], gridcolor='#E8DDD0')
    fig1.update_xaxes(gridcolor='#E8DDD0')
    st.plotly_chart(fig1, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        # Chart 2: Avg emotional impact by era
        st.markdown("<div class='section-header'>Avg. emotional impact by era</div>", unsafe_allow_html=True)
        era_data = filtered_df.groupby('era')['emotional_impact_score'].mean().reset_index()
        era_data.columns = ['era', 'avg_impact']
        era_data = era_data[era_data['era'].isin(ERA_ORDER)]
        era_data['era'] = pd.Categorical(era_data['era'], categories=ERA_ORDER, ordered=True)
        era_data = era_data.sort_values('era')
        era_data['color'] = era_data['era'].map(ERA_COLORS)

        fig2 = go.Figure(go.Bar(
            x=era_data['avg_impact'].round(2),
            y=era_data['era'],
            orientation='h',
            marker_color=era_data['color'],
            text=era_data['avg_impact'].round(2),
            textposition='outside',
            textfont=dict(size=11)
        ))
        fig2.update_layout(
            plot_bgcolor='#FAF7F2', paper_bgcolor='#FAF7F2',
            font=dict(family='DM Sans', color='#3D2B1F'),
            xaxis=dict(range=[0, 11], gridcolor='#E8DDD0', title='Score'),
            yaxis=dict(gridcolor='#E8DDD0'),
            margin=dict(t=20, b=20, l=10, r=40),
            height=300, showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        # Chart 3: Memory category donut
        st.markdown("<div class='section-header'>Memory category distribution</div>", unsafe_allow_html=True)
        cat_counts = filtered_df['memory_category'].value_counts().reset_index()
        cat_counts.columns = ['category', 'count']
        top5 = cat_counts.head(5)
        other_count = cat_counts.iloc[5:]['count'].sum()
        if other_count > 0:
            top5 = pd.concat([top5, pd.DataFrame([{'category': 'Other', 'count': other_count}])], ignore_index=True)

        fig3 = go.Figure(go.Pie(
            labels=top5['category'],
            values=top5['count'],
            hole=0.55,
            marker_colors=['#5B9E8F','#C4956A','#7F77DD','#D4715A','#D4537E','#B4B2A9'],
            textfont=dict(size=11)
        ))
        fig3.update_layout(
            plot_bgcolor='#FAF7F2', paper_bgcolor='#FAF7F2',
            font=dict(family='DM Sans', color='#3D2B1F'),
            margin=dict(t=20, b=20),
            height=300,
            legend=dict(font=dict(size=10), orientation='v', x=1.0)
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Chart 4: Scatter — closeness vs visits
    st.markdown("<div class='section-header'>Relationship closeness vs. visit frequency</div>", unsafe_allow_html=True)
    scatter_df = filtered_df.dropna(subset=['relationship_closeness_score'])
    fig4 = px.scatter(
        scatter_df,
        x='visit_frequency_to_baba_per_year',
        y='relationship_closeness_score',
        color='era',
        size='emotional_impact_score',
        hover_data=['year', 'memory_description', 'emotional_impact_score'],
        color_discrete_map=ERA_COLORS,
        labels={
            'visit_frequency_to_baba_per_year': 'Visits per year',
            'relationship_closeness_score': 'Closeness score (1–10)',
            'era': 'Life era'
        },
        size_max=20
    )
    fig4.update_layout(
        plot_bgcolor='#FAF7F2', paper_bgcolor='#FAF7F2',
        font=dict(family='DM Sans', color='#3D2B1F'),
        margin=dict(t=20, b=30, l=10, r=10),
        height=360,
        legend=dict(orientation='h', y=1.05, x=0)
    )
    fig4.update_xaxes(gridcolor='#E8DDD0')
    fig4.update_yaxes(gridcolor='#E8DDD0', range=[0, 12])
    if 2020 in scatter_df['year'].values:
        row_2020 = scatter_df[scatter_df['year'] == 2020].iloc[0]
        fig4.add_annotation(
            x=row_2020['visit_frequency_to_baba_per_year'],
            y=row_2020['relationship_closeness_score'],
            text="2020 — BaBa passed",
            showarrow=True, arrowhead=2,
            arrowcolor="#D4715A", font=dict(color="#D4715A", size=11),
            ax=60, ay=-30
        )
    st.plotly_chart(fig4, use_container_width=True)


# ─── PAGE 3: KEY INSIGHTS ────────────────────────────────────────────────────
elif page == "🔍 Key Insights":
    st.markdown("<h2 class='section-header' style='margin-top:0;'>Key insights</h2>", unsafe_allow_html=True)

    insights = [
        ("The drift was gradual, then absolute",
         "Visit frequency dropped from ~50/year in childhood to 10 during high school, then 4–5 during university, and finally 0 after BaBa's passing. "
         "No single year felt like abandonment — but the accumulated distance was total."),
        ("Emotional impact and physical presence are not the same thing",
         "The correlation between visits and emotional impact is 0.54 — moderate, not perfect. "
         "The year BaBa died (2020), visits were at their second lowest (2), yet emotional impact reached its maximum (10/10). "
         "Significance is not measured in frequency."),
        ("Comfort & Care was the dominant memory theme",
         "4 out of 28 records are classified as 'Comfort & Care' — the highest single category. "
         "BaBa's role was fundamentally that of a safe refuge: someone who healed wounds, made breakfast, and never turned me away."),
        ("Childhood held the richest emotional density",
         "Average emotional impact during childhood (1998–2012) was 7.47/10 — the highest of any era. "
         "High school followed closely at 7.33. The university years averaged 6.60, declining steadily as distance grew."),
        ("Crisis & Loss era was the emotional nadir",
         "The 2021–2022 period — BaBa's death combined with Myanmar's military coup and leaving university — "
         "produced the lowest average emotional impact at 4.5/10. Grief compounded by political trauma."),
        ("The regret of 2019 is data-legible",
         "One year before BaBa's passing, visit frequency was 4/year and the emotional impact score was 6/10. "
         "There was a planned gift (a good liquor bottle) that was never delivered. "
         "The data marks this year with the tag 'Regret' — the only year labeled that way."),
    ]

    for i, (title, body) in enumerate(insights):
        st.markdown(f"""
        <div class='insight-box'>
            <div style='font-weight:500; color:#3D2B1F; margin-bottom:4px;'>{i+1}. {title}</div>
            <div style='color:#5C4A32;'>{body}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Best & worst moments</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Highest impact moments (score ≥ 9)**")
        best = df[df['emotional_impact_score'] >= 9][['year','memory_category','emotional_impact_score','memory_description']].sort_values('year')
        for _, row in best.iterrows():
            st.markdown(f"""
            <div style='background:#EAF3DE; border-radius:8px; padding:0.6rem 0.9rem; margin:4px 0; font-size:0.85rem;'>
                <b style='color:#3D2B1F;'>{int(row.year)}</b>
                <span class='badge'>{row.memory_category}</span>
                <span style='color:#27500A; font-weight:500;'> {row.emotional_impact_score}/10</span>
                <div style='color:#5C4A32; margin-top:2px; font-size:0.8rem;'>{row.memory_description}</div>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        st.markdown("**Lowest impact moments (score ≤ 5)**")
        worst = df[df['emotional_impact_score'] <= 5][['year','memory_category','emotional_impact_score','memory_description']].sort_values('year')
        for _, row in worst.iterrows():
            st.markdown(f"""
            <div style='background:#FCEBEB; border-radius:8px; padding:0.6rem 0.9rem; margin:4px 0; font-size:0.85rem;'>
                <b style='color:#3D2B1F;'>{int(row.year)}</b>
                <span class='badge'>{row.memory_category}</span>
                <span style='color:#A32D2D; font-weight:500;'> {row.emotional_impact_score}/10</span>
                <div style='color:#5C4A32; margin-top:2px; font-size:0.8rem;'>{row.memory_description}</div>
            </div>
            """, unsafe_allow_html=True)


# ─── PAGE 4: DECISION-MAKING ─────────────────────────────────────────────────
elif page == "🎯 Decision-Making":
    st.markdown("<h2 class='section-header' style='margin-top:0;'>Decision-making</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='story-quote'>
        "Based on my data, what should I do differently in the future?"
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='color:#4A3728; font-size:0.97rem; line-height:1.9;'>
    The data presents a clear behavioral pattern: as physical distance grew, visit frequency
    collapsed — from 50 visits/year in childhood, to 5 during early university, to 2 in BaBa's
    final year. Yet emotional impact peaked exactly at that last year. This is the central paradox
    the data reveals: <b>we understand the value of someone most clearly when we can no longer reach them.</b>
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Three data-supported decisions</div>", unsafe_allow_html=True)

    decisions = [
        ("Prioritize presence before loss makes it impossible",
         "Visit frequency dropped 96% from childhood to BaBa's final year (50 → 2 visits). "
         "The data shows that I had 4–5 opportunities per year during university but did not always use them for visits home. "
         "Decision: in the future, treat visits to aging loved ones as non-negotiable calendar commitments — not optional additions.",
         "#5B9E8F"),
        ("Deliver gestures before they become regrets",
         "2019 is the only year labeled 'Regret' in the dataset. The planned gift (a bottle of good liquor) was never delivered. "
         "The emotional impact score for that year was 6/10 — lower than any childhood year. "
         "Decision: act on intentions immediately. Deferred kindness has an expiry date.",
         "#C4956A"),
        ("Measure closeness by quality, not quantity",
         "The scatter data shows a 0.54 correlation between visits and emotional impact — meaningful, but far from absolute. "
         "The 2020 data point (2 visits, closeness 10, impact 10) shows that depth of connection outlasts frequency. "
         "Decision: when visits are impossible (due to distance, conflict, or circumstance), invest in the quality of each contact — calls, letters, presence of mind.",
         "#7F77DD"),
    ]

    for title, body, color in decisions:
        st.markdown(f"""
        <div style='background:#FFFFFF; border:1px solid #E8DDD0; border-left: 4px solid {color};
                    border-radius: 0 10px 10px 0; padding: 1.1rem 1.3rem; margin: 0.75rem 0;'>
            <div style='font-family: Lora, serif; font-weight:600; color:#3D2B1F; margin-bottom:6px;'>{title}</div>
            <div style='color:#5C4A32; font-size:0.9rem; line-height:1.75;'>{body}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Limitations of these decisions</div>", unsafe_allow_html=True)
    limits = [
        "The dataset covers only one relationship. These findings may not generalize to all bonds.",
        "Visit frequency was estimated from memory — actual numbers may differ slightly.",
        "External factors (university schedule, coup, pandemic, finances) constrained visits in ways the data alone cannot fully capture.",
        "Emotional impact scores are subjective and retrospective — scored in 2025 looking back, not in real-time.",
    ]
    for lim in limits:
        st.markdown(f"<div style='color:#8C7560; font-size:0.88rem; padding: 4px 0 4px 12px; border-left: 2px solid #E8DDD0;'>⚠ {lim}</div>", unsafe_allow_html=True)


# ─── PAGE 5: ETHICS ──────────────────────────────────────────────────────────
elif page == "⚖️ Ethics & Responsibility":
    st.markdown("<h2 class='section-header' style='margin-top:0;'>Ethics & responsibility</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='ethics-block'>
            <div class='ethics-title'>🔒 Privacy statement</div>
            <p style='color:#4A3728; font-size:0.9rem; line-height:1.75; margin:0;'>
            This dataset contains no real full names. BaBa is a relational term, not an identifier.
            Grandma Cho is referred to by a common name only. No addresses, ID numbers, medical records,
            or third-party personal data are included. All emotional scores are self-generated by the author.
            The dataset reflects only the author's own memories and perceptions.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='ethics-block'>
            <div class='ethics-title'>⚠️ Bias & limitations</div>
            <ul style='color:#4A3728; font-size:0.9rem; line-height:1.9; margin:0; padding-left: 1.2rem;'>
                <li><b>Memory bias:</b> All data is reconstructed from personal recollection. Early years (1998–2005) especially may be idealized.</li>
                <li><b>Small dataset:</b> 28 rows representing 27 years. Statistical conclusions should be held lightly.</li>
                <li><b>Subjective scoring:</b> Emotional impact and closeness scores were assigned by the author — they are inherently personal, not objective.</li>
                <li><b>Retrospective framing:</b> Knowing BaBa passed in 2020 may have inflated or colored scores for years before.</li>
                <li><b>Missing data:</b> Relationship closeness scores are absent for post-2020 rows (BaBa was no longer present).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='ethics-block'>
            <div class='ethics-title'>📊 Visualization justification</div>
            <ul style='color:#4A3728; font-size:0.9rem; line-height:1.9; margin:0; padding-left: 1.2rem;'>
                <li><b>Dual-axis line chart:</b> Chosen to show two variables (visits + emotion) across time simultaneously. Risk: dual axes can mislead scale perception — both axes are clearly labeled.</li>
                <li><b>Horizontal bar chart:</b> Used for era comparisons because category names are long and benefit from horizontal space.</li>
                <li><b>Donut chart:</b> Shows memory category proportion at a glance. Risk: small slices are hard to compare — "Other" bucket reduces clutter.</li>
                <li><b>Bubble scatter plot:</b> Visits vs. closeness with bubble size = emotional impact. Reveals the paradox of 2020 directly. Risk: overlapping points — hover tooltips provide detail.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='ethics-block'>
            <div class='ethics-title'>🎯 Responsible decision statement</div>
            <p style='color:#4A3728; font-size:0.9rem; line-height:1.75; margin:0;'>
            The decisions on this dashboard are personal behavioral reflections — not prescriptions for others.
            No claim is made that these patterns are universal. The author acknowledges that geopolitical events
            (Myanmar coup, displacement) severely limited choices in ways data cannot fully represent.
            This project does not monetize or expose any third party's personal data.
            The dataset exists solely as a reflective academic exercise.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Buddha's teaching — the project's guiding frame</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='story-quote'>
    "Nothing is forever. Everything will eventually come to an end. The root of suffering is attachment.
    Therefore, each of you should make a dedicated effort by holding your awareness in your mind
    to break free from the cycle of Samsara."
    </div>
    <p style='color:#8C7560; font-size:0.85rem; margin-top: -0.5rem;'>
    This project does not claim to resolve grief or offer spiritual prescriptions.
    It uses the concept of Samsara as a reflective lens — a way of understanding why the cycle of
    attachment and loss is universal, and what data can and cannot tell us about it.
    </p>
    """, unsafe_allow_html=True)

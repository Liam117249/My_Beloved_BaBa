import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

# Load page icon
try:
    _icon = Image.open("icon.png")
except FileNotFoundError:
    _icon = "🕯️"

st.set_page_config(
    page_title="Samsara — A Story of BaBa",
    page_icon=_icon,
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
    try:
        sidebar_img = Image.open("icon.png")
        st.image(sidebar_img, use_container_width=True)
    except FileNotFoundError:
        st.markdown("<div style='text-align:center; font-size:2rem;'>🕯️</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; padding: 0.2rem 0 0.5rem;'>
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
        He had already boiled water and was waiting for me, preparing my favorite breakfast,
        Mont T, along with plain tea or sometimes coffee."
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <p style='color:#4A3728; line-height:1.9; font-size:0.97rem;'>
        BaBa was the husband of my grandmother's sister. He lived just across the yard from my home in Myanmar.
        He was not my grandfather by blood. But he was the one who held me when things were hard at home.
        He put medicine on my wounds, told me stories at night, and gave me his own clothes when I had none.
        </p>
        <p style='color:#4A3728; line-height:1.9; font-size:0.97rem;'>
        When I moved away for high school and then university, I visited him less and less.
        Life moved fast and I kept going forward. In November 2020, during my fourth year at university,
        BaBa had a sudden stroke and passed away at age 72.
        I had planned to bring him a good bottle of liquor after my midterms. I never got the chance.
        </p>
        <p style='color:#4A3728; line-height:1.9; font-size:0.97rem;'>
        This project turns those memories into data. Not to make loss feel cold,
        but to see the patterns that grief alone cannot show clearly.
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

    # Chart 1: Dual axis — visits + emotion over time (unchanged)
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
        # Chart 2: Avg emotional impact by era (unchanged)
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
        # Chart 3: Memory Timeline — Gantt-style by category.
        # Each memory record is a colored block placed at its year on the x-axis,
        # stacked by memory category on the y-axis.
        # Rare categories stand out visually. The full 27-year story reads left to right.
        st.markdown("<div class='section-header'>Memory timeline by category</div>", unsafe_allow_html=True)

        gantt_df = filtered_df.copy()

        # Assign a unique color per memory category
        all_cats = gantt_df['memory_category'].unique().tolist()
        cat_palette = [
            '#5B9E8F','#C4956A','#7F77DD','#D4715A','#D4537E',
            '#6BA8C4','#A8B86B','#B47CC4','#888780','#C4A46B'
        ]
        cat_color_map = {cat: cat_palette[i % len(cat_palette)] for i, cat in enumerate(sorted(all_cats))}

        # Each block spans half a year for visual clarity
        fig3 = go.Figure()
        for _, row in gantt_df.iterrows():
            fig3.add_trace(go.Bar(
                x=[0.7],
                y=[row['memory_category']],
                base=[row['year'] - 0.35],
                orientation='h',
                marker=dict(
                    color=cat_color_map[row['memory_category']],
                    opacity=0.4 + 0.06 * row['emotional_impact_score'],
                    line=dict(color='white', width=1)
                ),
                hovertemplate=(
                    f"<b>{int(row['year'])}</b><br>"
                    f"Category: {row['memory_category']}<br>"
                    f"Impact: {row['emotional_impact_score']}/10<br>"
                    f"{row['memory_description']}<extra></extra>"
                ),
                showlegend=False
            ))

        # 2020 marker line
        if 2020 in gantt_df['year'].values:
            fig3.add_vline(
                x=2020, line_dash="dash",
                line_color="#D4715A", line_width=1.5, opacity=0.7
            )
            fig3.add_annotation(
                x=2020, y=len(all_cats) - 0.3,
                text="2020", showarrow=False,
                font=dict(color="#D4715A", size=10),
                xanchor='center'
            )

        fig3.update_layout(
            plot_bgcolor='#FAF7F2', paper_bgcolor='#FAF7F2',
            font=dict(family='DM Sans', color='#3D2B1F'),
            barmode='overlay',
            xaxis=dict(
                title='Year',
                gridcolor='#E8DDD0',
                range=[gantt_df['year'].min() - 0.5, gantt_df['year'].max() + 0.5],
                dtick=4
            ),
            yaxis=dict(gridcolor='#E8DDD0', title=''),
            margin=dict(t=20, b=30, l=10, r=10),
            height=300,
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Chart 4: Memory category ranked bar with color = avg emotional impact.
    # Sorted by count. Color scale shows which categories carried the most weight emotionally.
    st.markdown("<div class='section-header'>What kinds of memories stand out most</div>", unsafe_allow_html=True)
    cat_df = filtered_df.groupby('memory_category').agg(
        count=('memory_category', 'count'),
        avg_impact=('emotional_impact_score', 'mean')
    ).reset_index().sort_values('count', ascending=True)

    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=cat_df['count'],
        y=cat_df['memory_category'],
        orientation='h',
        marker=dict(
            color=cat_df['avg_impact'],
            colorscale=[[0, '#F2DEC8'], [0.5, '#C4956A'], [1, '#3D2B1F']],
            colorbar=dict(title='Avg impact', thickness=12, len=0.6),
            showscale=True
        ),
        text=cat_df['count'],
        textposition='outside',
        textfont=dict(size=11),
        hovertemplate='<b>%{y}</b><br>Memories: %{x}<br>Avg impact: %{marker.color:.1f}/10<extra></extra>'
    ))
    fig4.update_layout(
        plot_bgcolor='#FAF7F2', paper_bgcolor='#FAF7F2',
        font=dict(family='DM Sans', color='#3D2B1F'),
        xaxis=dict(title='Number of memories', gridcolor='#E8DDD0'),
        yaxis=dict(gridcolor='#E8DDD0'),
        margin=dict(t=20, b=30, l=10, r=80),
        height=380,
        showlegend=False
    )
    st.plotly_chart(fig4, use_container_width=True)


# ─── PAGE 3: KEY INSIGHTS ────────────────────────────────────────────────────
elif page == "🔍 Key Insights":
    st.markdown("<h2 class='section-header' style='margin-top:0;'>Key insights</h2>", unsafe_allow_html=True)

    insights = [
        ("Visits dropped slowly, then stopped",
         "I visited BaBa about 50 times a year in childhood. That fell to 10 in high school, then 4 to 5 in university, then 0 after he passed. "
         "No single year felt like a goodbye. But over time the distance became total."),
        ("Being there more did not always mean feeling more",
         "Visits and emotional impact have a 0.54 correlation. That is moderate, not strong. "
         "In 2020, the year BaBa died, I only visited twice. Yet that year scored 10 out of 10 on emotional impact. "
         "Presence alone does not explain how much a moment matters."),
        ("Comfort and care was the most common memory type",
         "4 out of 28 records fall under Comfort and Care. That is the highest single category. "
         "BaBa was the person I went to when things went wrong. He made breakfast, treated my wounds, and never turned me away."),
        ("Childhood had the highest emotional scores",
         "The average emotional impact in childhood was 7.47 out of 10. High school was 7.33. University dropped to 6.60. "
         "The further away I moved, the lower the scores became."),
        ("The Crisis and Loss years were the hardest",
         "From 2021 to 2022, the average emotional impact was 4.5 out of 10. That is the lowest of any era. "
         "BaBa had just passed. Myanmar was in political crisis. I had left university. Everything happened at once."),
        ("2019 is the only year tagged as Regret",
         "That year I visited 4 times and the emotional score was 6 out of 10. "
         "I had planned to bring BaBa a bottle of good liquor. I never did. "
         "It is the only year in the data with that tag."),
    ]

    for i, (title, body) in enumerate(insights):
        st.markdown(f"""
        <div class='insight-box'>
            <div style='font-weight:500; color:#3D2B1F; margin-bottom:4px;'>{i+1}. {title}</div>
            <div style='color:#5C4A32;'>{body}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Best and worst moments</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Highest impact moments (score 9 or above)**")
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
        st.markdown("**Lowest impact moments (score 5 or below)**")
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
    The data shows one clear pattern. As I moved further away, I visited BaBa less.
    Visits went from 50 a year in childhood, down to 5 in early university, and just 2 in his final year.
    But emotional impact was highest in that last year. The data shows that
    <b>we often understand how much someone matters only after we can no longer reach them.</b>
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Three decisions based on the data</div>", unsafe_allow_html=True)

    decisions = [
        ("Visit before it is too late",
         "Visits dropped 96 percent from childhood to BaBa's last year, from 50 down to 2. "
         "During university I had 4 to 5 chances a year to go home but often did not use them. "
         "Going forward, I will treat visits to aging loved ones as fixed plans, not optional ones.",
         "#5B9E8F"),
        ("Do not delay kind gestures",
         "2019 is the only year in the dataset tagged as Regret. I planned to bring BaBa a gift but never did. "
         "The emotional score that year was 6 out of 10, lower than any year in childhood. "
         "If I plan to do something kind, I will do it now.",
         "#C4956A"),
        ("Quality matters more than quantity",
         "The correlation between visits and emotional impact is 0.54. It matters, but it is not everything. "
         "In 2020 I only visited twice, yet the closeness and impact scores were both 10 out of 10. "
         "When visits are not possible, I will focus on making each call or message count.",
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

    st.markdown("<div class='section-header'>Limits of these decisions</div>", unsafe_allow_html=True)
    limits = [
        "This dataset covers only one relationship. The findings may not apply to others.",
        "Visit counts were estimated from memory. The exact numbers may be slightly off.",
        "Outside events like the military coup, the pandemic, and financial limits affected how often I could visit. The data does not fully capture that.",
        "All emotional scores were assigned in 2025, looking back. They reflect how I feel now, not how I felt at the time.",
    ]
    for lim in limits:
        st.markdown(f"<div style='color:#8C7560; font-size:0.88rem; padding: 4px 0 4px 12px; border-left: 2px solid #E8DDD0;'>⚠ {lim}</div>", unsafe_allow_html=True)


# ─── PAGE 5: ETHICS ──────────────────────────────────────────────────────────
elif page == "⚖️ Ethics & Responsibility":
    st.markdown("<h2 class='section-header' style='margin-top:0;'>Ethics and responsibility</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='ethics-block'>
            <div class='ethics-title'>🔒 Privacy</div>
            <p style='color:#4A3728; font-size:0.9rem; line-height:1.75; margin:0;'>
            No real full names are used in this dataset. BaBa is a family term, not an identifier.
            Grandma Cho is referred to by a common name only. No addresses, ID numbers, or private records are included.
            All scores were created by me and reflect only my own memories.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='ethics-block'>
            <div class='ethics-title'>⚠️ Bias and limits</div>
            <ul style='color:#4A3728; font-size:0.9rem; line-height:1.9; margin:0; padding-left: 1.2rem;'>
                <li><b>Memory bias.</b> All data comes from personal memory. Early years may be idealized.</li>
                <li><b>Small dataset.</b> 28 rows covering 27 years. Numbers should not be treated as hard facts.</li>
                <li><b>Subjective scores.</b> Emotional impact and closeness were scored by me. They are personal, not objective.</li>
                <li><b>Looking back.</b> Knowing BaBa passed in 2020 may have affected how I scored earlier years.</li>
                <li><b>Missing data.</b> Closeness scores are blank for years after 2020 because BaBa was no longer here.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='ethics-block'>
            <div class='ethics-title'>📊 Why I chose each chart</div>
            <ul style='color:#4A3728; font-size:0.9rem; line-height:1.9; margin:0; padding-left: 1.2rem;'>
                <li><b>Dual-axis line chart.</b> Shows visits and emotion together over time. Both axes are labeled clearly to avoid confusion.</li>
                <li><b>Horizontal bar chart.</b> Compares average emotional impact across eras. The horizontal layout fits the long era names.</li>
                <li><b>Memory timeline (Gantt-style).</b> Places every memory as a colored block at its year, grouped by category. The full 27-year story reads left to right. Block opacity reflects emotional impact — darker means heavier.</li>
                <li><b>Ranked bar with color scale.</b> Shows which memory types appear most often and how emotionally heavy each type was on average.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='ethics-block'>
            <div class='ethics-title'>🎯 Responsible use</div>
            <p style='color:#4A3728; font-size:0.9rem; line-height:1.75; margin:0;'>
            The decisions on this dashboard are personal reflections. They are not advice for others.
            I do not claim these patterns apply to everyone. Outside events like the Myanmar coup and displacement
            limited my choices in ways the data cannot fully show.
            No one else's private data is used or shared here. This project is an academic exercise only.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>The guiding idea behind this project</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='story-quote'>
    "Nothing is forever. Everything will eventually come to an end. The root of suffering is attachment.
    Therefore, each of you should make a dedicated effort by holding your awareness in your mind
    to break free from the cycle of Samsara."
    </div>
    <p style='color:#8C7560; font-size:0.85rem; margin-top: -0.5rem;'>
    This project does not offer spiritual answers or claim to resolve grief.
    Samsara is used here as a lens to understand why attachment and loss repeat across every life,
    and what data can and cannot tell us about that.
    </p>
    """, unsafe_allow_html=True)

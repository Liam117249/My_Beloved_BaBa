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
        # Chart 2: Scatter — Visit Frequency vs. Relationship Closeness, colored by era.
        # Makes the counterintuitive argument that presence ≠ closeness.
        # 2020: 2 visits, closeness 10 — the outlier that tells the whole story.
        st.markdown("<div class='section-header'>Does visiting more mean feeling closer?</div>", unsafe_allow_html=True)

        scatter_df = filtered_df.dropna(subset=['relationship_closeness_score']).copy()
        scatter_df['era'] = pd.Categorical(scatter_df['era'], categories=ERA_ORDER, ordered=True)

        fig2 = go.Figure()
        for era in ERA_ORDER:
            era_pts = scatter_df[scatter_df['era'] == era]
            if era_pts.empty:
                continue
            is_2020 = era_pts['year'] == 2020
            fig2.add_trace(go.Scatter(
                x=era_pts['visit_frequency_to_baba_per_year'],
                y=era_pts['relationship_closeness_score'],
                mode='markers',
                name=era,
                marker=dict(
                    color=ERA_COLORS[era],
                    size=[18 if y == 2020 else 10 for y in era_pts['year']],
                    symbol=['star' if y == 2020 else 'circle' for y in era_pts['year']],
                    line=dict(color='white', width=1),
                    opacity=0.88,
                ),
                customdata=era_pts[['year', 'memory_category', 'memory_description']].values,
                hovertemplate=(
                    '<b>%{customdata[0]}</b><br>'
                    'Visits: %{x}/yr<br>'
                    'Closeness: %{y}/10<br>'
                    '%{customdata[1]}<br>'
                    '<i style="color:#8C7560">%{customdata[2]}</i>'
                    '<extra></extra>'
                ),
            ))

        # Annotation for 2020 outlier
        row_2020 = scatter_df[scatter_df['year'] == 2020]
        if not row_2020.empty:
            fig2.add_annotation(
                x=row_2020['visit_frequency_to_baba_per_year'].values[0],
                y=row_2020['relationship_closeness_score'].values[0],
                text="2020 — 2 visits,<br>closeness 10",
                showarrow=True, arrowhead=2,
                arrowcolor='#D4715A',
                font=dict(color='#D4715A', size=10),
                ax=55, ay=-38,
                bgcolor='#FDF5EC', bordercolor='#D4715A', borderwidth=1,
                borderpad=4,
            )

        fig2.update_layout(
            plot_bgcolor='#FAF7F2', paper_bgcolor='#FAF7F2',
            font=dict(family='DM Sans', color='#3D2B1F'),
            xaxis=dict(title='Visits per year', gridcolor='#E8DDD0', zeroline=False),
            yaxis=dict(title='Relationship closeness (1–10)', gridcolor='#E8DDD0', range=[4, 11]),
            legend=dict(title='Era', font=dict(size=10), bgcolor='rgba(0,0,0,0)'),
            margin=dict(t=20, b=30, l=10, r=10),
            height=340,
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(
            "<p style='font-size:0.8rem; color:#8C7560; margin-top:-8px;'>"
            "⭐ star = 2020 (BaBa's final year). Closeness scores unavailable after 2020."
            "</p>", unsafe_allow_html=True
        )

    with col_b:
        # Chart 3: Stacked 100% bar — Memory category composition per life era.
        # Shows how the KIND of relationship changed across life stages, not just the quantity.
        # Childhood: rich mix of care, stories, daily life. Later eras: only separation, reunion, grief.
        st.markdown("<div class='section-header'>How the relationship changed in kind</div>", unsafe_allow_html=True)

        CAT_PALETTE = {
            'Bond Formation':  '#5B9E8F',
            'Daily Life':      '#6BA8C4',
            'Comfort & Care':  '#C4956A',
            'Entertainment':   '#A8B86B',
            'Storytelling':    '#7F77DD',
            'Food & Sharing':  '#D4A056',
            'Clothing & Gift': '#B47CC4',
            'Concern':         '#D4537E',
            'Separation':      '#888780',
            'Reunion':         '#5B8FA8',
            'Milestone':       '#8FAF5B',
            'Regret':          '#C47070',
            'Loss':            '#D4715A',
            'Political Crisis':'#9E5B5B',
            'Grief and Reflection': '#A08080',
            'New Beginning':   '#5B9E8F',
            'Displacement':    '#8C7560',
            'Continuity':      '#7AA88C',
        }

        comp_df = filtered_df.copy()
        comp_df['era'] = pd.Categorical(comp_df['era'], categories=ERA_ORDER, ordered=True)
        comp_df = comp_df[comp_df['era'].isin(selected_eras)]

        # Count memories per era × category, then normalise to 100%
        pivot = comp_df.groupby(['era', 'memory_category']).size().unstack(fill_value=0)
        pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100
        pivot_pct = pivot_pct.reindex([e for e in ERA_ORDER if e in pivot_pct.index])

        fig3 = go.Figure()
        for cat in pivot_pct.columns:
            color = CAT_PALETTE.get(cat, '#CCCCCC')
            vals = pivot_pct[cat]
            raw_counts = pivot.reindex(pivot_pct.index)[cat]
            fig3.add_trace(go.Bar(
                name=cat,
                x=pivot_pct.index.tolist(),
                y=vals,
                marker_color=color,
                customdata=raw_counts.values,
                hovertemplate=(
                    '<b>%{x}</b><br>'
                    f'{cat}<br>'
                    'Share: %{y:.1f}%<br>'
                    'Count: %{customdata}<extra></extra>'
                ),
                text=[f"{v:.0f}%" if v >= 7 else "" for v in vals],
                textposition='inside',
                textfont=dict(size=9, color='white'),
            ))

        fig3.update_layout(
            barmode='stack',
            plot_bgcolor='#FAF7F2', paper_bgcolor='#FAF7F2',
            font=dict(family='DM Sans', color='#3D2B1F'),
            xaxis=dict(title='Life era', gridcolor='#E8DDD0', tickangle=-15),
            yaxis=dict(title='% of memories', gridcolor='#E8DDD0', range=[0, 101]),
            legend=dict(
                orientation='v', x=1.01, y=1,
                font=dict(size=9), bgcolor='rgba(0,0,0,0)',
                title=dict(text='Category', font=dict(size=10)),
            ),
            margin=dict(t=20, b=50, l=10, r=170),
            height=340,
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown(
            "<p style='font-size:0.8rem; color:#8C7560; margin-top:-8px;'>"
            "Each bar = 100% of memories in that era. Shows how the texture of the relationship narrowed over time."
            "</p>", unsafe_allow_html=True
        )

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
        ("Visits peaked at age 10, then kept falling",
         "Visits grew as I got older and could walk next door on my own — reaching 50 at age 10. "
         "After I left for high school, they dropped to 8–10. University brought it to 4–5. "
         "In 2020, BaBa's last year, I visited just 2 times."),
        ("More visits meant more closeness — but not always",
         "Years with more visits were generally closer years. But 2020 breaks that rule: "
         "only 2 visits, yet a closeness score of 10 — the highest in the whole dataset. "
         "Being there helped, but it was not the only thing that mattered."),
        ("The relationship lost its richness before it lost its frequency",
         "In childhood, memories cover 7 types — meals, stories, comfort, gifts, and more. "
         "By university, it was mostly just Separation and Reunion. "
         "I was not only visiting less — we had less and less to share."),
        ("Comfort & Care stands out most in the data",
         "It is the most common memory type, with 4 records. Three of those score 9/10. "
         "BaBa was the person I went to when I was hurt or in trouble. "
         "No other memory type shows up that often or that strongly."),
        ("Emotional scores dropped slowly as I moved further away",
         "Childhood averaged 7.5/10. High school 7.3. University 6.6. Post-2020 dropped to 4.5. "
         "The decline was steady — except for 2020 itself, which scored 10. "
         "Distance reduced the quality of the relationship, but not all at once."),
        ("There is only one Regret in 27 years — and it sits right before he died",
         "In 2019 I planned to bring BaBa a bottle of liquor after my exams. I never did. "
         "That is the only Regret record in the entire dataset. "
         "His health that year looked fine. There was no warning."),
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
    Visits peaked at 50 when I was 10, then dropped every year after I left home.
    By 2020, I was down to 2 visits. That same year scored the highest closeness in the dataset — 10 out of 10.
    The data shows that <b>I still felt close to BaBa even when I rarely visited. But I ran out of time.</b>
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Three things I will do differently</div>", unsafe_allow_html=True)

    decisions = [
        ("Visit the people I love — and put it in the calendar",
         "Visits dropped 96% from age 10 to BaBa's last year. During university, I averaged 4 visits a year. "
         "I kept telling myself I would go soon. The data shows I never went more than I planned to. "
         "From now on, I will set fixed dates to visit people I care about — not leave it open.",
         "#5B9E8F"),
        ("Do the kind thing now, not later",
         "2019 is the only Regret in 27 years of data. I had a simple plan — bring BaBa a bottle of liquor after exams. I did not do it. "
         "His health looked fine that year. There was no sign anything was wrong. "
         "I learned that there is no safe 'later'. If I want to do something kind, I should do it now.",
         "#C4956A"),
        ("Keep the relationship varied, not just frequent",
         "By university, almost all my memories with BaBa were only Separation and Reunion — nothing else. "
         "The relationship had become thin, not just less frequent. "
         "When I cannot visit, I will still try to share something real — a story, a question, a memory. "
         "That is what kept us close even in 2020.",
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

    st.markdown("<div class='section-header'>Limitations</div>", unsafe_allow_html=True)
    limits = [
        "This is one relationship, 28 data points. The patterns here may not apply to other people or other relationships.",
        "Visit counts for early childhood are estimates from memory. They are not exact.",
        "Emotional and closeness scores were assigned in 2025, looking back. Knowing BaBa passed away likely affected how I scored earlier years.",
        "Some years I could not visit more even if I wanted to — due to the coup, displacement, and money. The data does not show those barriers.",
    ]
    for lim in limits:
        st.markdown(f"<div style='color:#8C7560; font-size:0.88rem; padding: 5px 0 5px 12px; margin: 3px 0; border-left: 2px solid #E8DDD0;'>⚠ {lim}</div>", unsafe_allow_html=True)


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
                <li><b>Dual-axis line chart.</b> Shows visits and emotional impact together over time. Both axes are clearly labeled to avoid misreading the two scales as equivalent.</li>
                <li><b>Scatter plot — visits vs. closeness.</b> Each dot is one year. Placing visit frequency on the x-axis and relationship closeness on the y-axis tests a direct hypothesis: does visiting more produce a closer bond? The 2020 outlier (2 visits, closeness 10) makes the counterargument visually without needing words. Era color makes temporal clustering readable without cluttering the axes.</li>
                <li><b>Stacked 100% bar — memory composition by era.</b> Normalising to 100% removes the distortion of unequal record counts per era and focuses the eye on proportion, not volume. It shows how the texture of the relationship narrowed over time — from a rich mix of care, storytelling, and daily life down to only separation, reunion, and grief. The risk of misreading is that equal bar heights imply equal importance; the caption addresses this.</li>
                <li><b>Ranked bar with color scale.</b> Shows which memory categories appear most often and how emotionally weighted each type was on average. Sorting by count reveals frequency; the color gradient adds a second variable without a second axis.</li>
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

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# ---------------------------------------------------------
# PAGE SETUP & STYLING
# ---------------------------------------------------------
try:
    _icon = Image.open("icon (1).jpg")
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
}

.section-header {
    font-family: 'Lora', serif;
    color: #4A3728;
    font-size: 1.5rem;
    margin-top: 2rem;
    border-bottom: 1px solid #C4956A;
    padding-bottom: 0.5rem;
}

.ethics-block {
    background-color: #E8DCCB;
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
}
.ethics-title {
    font-weight: 600;
    color: #4A3728;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("baba_memories_dataset.csv")
    return df

df = load_data()

# ---------------------------------------------------------
# SIDEBAR & INTERACTIVITY
# ---------------------------------------------------------
st.sidebar.title("Journey Timeline")
st.sidebar.markdown("Filter the memories by life stage to explore the data interactively.")

life_stages = df['life_stage'].unique()
selected_stages = st.sidebar.multiselect(
    "Select Life Stages:",
    options=life_stages,
    default=life_stages
)

# Apply filter
filtered_df = df[df['life_stage'].isin(selected_stages)].copy()

# ---------------------------------------------------------
# MAIN HEADER
# ---------------------------------------------------------
st.title("Samsara — A Story of BaBa")
st.markdown("""
<div class='story-quote'>
"When my father's punishment became too severe, I had a secret hiding place to seek refuge... my BaBa's house."
</div>
""", unsafe_allow_html=True)
st.write("This dashboard explores the enduring impact of a beloved great-uncle, mapping the warmth of early childhood memories against the profound grief of loss and the harsh realities of displacement.")

# ---------------------------------------------------------
# VISUALIZATIONS
# ---------------------------------------------------------
st.markdown("<div class='section-header'>1. The Architecture of Care (Visit Frequency)</div>", unsafe_allow_html=True)
fig1 = px.area(
    filtered_df, 
    x="year", 
    y="visit_frequency_to_baba_per_year",
    title="Annual Visit Frequency to BaBa's House",
    labels={"year": "Year", "visit_frequency_to_baba_per_year": "Visits Per Year"},
    color_discrete_sequence=["#C4956A"]
)
fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig1, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='section-header'>2. Geography & Closeness</div>", unsafe_allow_html=True)
    fig2 = px.scatter(
        filtered_df,
        x="age",
        y="relationship_closeness_score",
        color="location",
        size="emotional_impact_score",
        title="Closeness over Life Stages & Locations",
        labels={"age": "My Age", "relationship_closeness_score": "Closeness Score (1-10)"},
        color_discrete_sequence=px.colors.qualitative.Earth
    )
    fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.markdown("<div class='section-header'>3. Types of Memories</div>", unsafe_allow_html=True)
    fig_pie = px.pie(
        filtered_df, 
        names='memory_category', 
        title='Distribution of Memory Categories',
        color_discrete_sequence=px.colors.qualitative.Antique
    )
    fig_pie.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_pie, use_container_width=True)

# --- NEW DIVERGING BAR CHART ---
st.markdown("<div class='section-header'>4. The Arc of Samsara (Emotional Impact)</div>", unsafe_allow_html=True)
st.write("This chart maps emotional impact relative to the lifetime average. Bars extending to the right indicate years of deep warmth and connection. Bars extending to the left reflect periods dominated by grief, loss, and displacement.")

# Calculate average emotional impact from the FULL dataset to maintain a stable baseline
avg_impact = df['emotional_impact_score'].mean()

# Calculate variance for the filtered dataset
filtered_df['impact_variance'] = filtered_df['emotional_impact_score'] - avg_impact

# Color mapping: Warmth (Right/Positive) vs Grief (Left/Negative)
filtered_df['bar_color'] = filtered_df['impact_variance'].apply(lambda x: '#C4956A' if x >= 0 else '#4A3728')

# Sort by year so the narrative flows chronologically top-to-bottom
df_sorted = filtered_df.sort_values('year', ascending=False)

fig3 = go.Figure()
fig3.add_trace(go.Bar(
    x=df_sorted['impact_variance'],
    y=df_sorted['year'].astype(str), # Treat years as categories for the y-axis
    orientation='h',
    marker_color=df_sorted['bar_color'],
    text=df_sorted['major_life_event'], # Show life event on hover
    hovertemplate="<b>Year: %{y}</b><br>Life Event: %{text}<br>Variance from Avg: %{x:.2f}<extra></extra>"
))

fig3.update_layout(
    title="Emotional Impact Relative to Lifetime Average",
    xaxis_title="← Grief & Loss (Below Avg) | Warmth & Connection (Above Avg) →",
    yaxis_title="Year",
    yaxis=dict(autorange="reversed"), # Ensures chronological order from top down
    plot_bgcolor="rgba(0,0,0,0)", 
    paper_bgcolor="rgba(0,0,0,0)",
    shapes=[dict(
        type='line',
        yref='paper', y0=0, y1=1,
        xref='x', x0=0, x1=0,
        line=dict(color='gray', width=2, dash='dash')
    )]
)
st.plotly_chart(fig3, use_container_width=True)


# ---------------------------------------------------------
# DECISION MAKING & INSIGHTS
# ---------------------------------------------------------
st.markdown("<div class='section-header'>🔍 Key Insights & Decision-Making</div>", unsafe_allow_html=True)
st.markdown("""
* **The Gravity of Absence:** The diverging bar chart reveals a sharp pivot in 2020. The transition from intense connection (positive variance) to intense grief and displacement (negative variance) visually confirms that BaBa was the anchor of my early life.
* **Based on my data, what should I do differently in the future?** My data shows that my highest emotional connection and comfort occurred during the simple, consistent routines shared with BaBa (like morning tea and storytelling). Moving forward, especially while living displaced in a new country, I need to intentionally build small, consistent daily rituals of comfort for myself, rather than waiting for large milestones to find stability.
""")

# ---------------------------------------------------------
# ETHICS & RESPONSIBILITY (MANDATORY SECTION)
# ---------------------------------------------------------
st.markdown("<div class='section-header'>⚖️ Ethics & Responsibility</div>", unsafe_allow_html=True)

with st.container():
    st.markdown("""
    <div class='ethics-block'>
        <div class='ethics-title'>🔒 Privacy Statement</div>
        <ul style='color:#4A3728; font-size:0.9rem; line-height:1.6;'>
            <li>This dataset uses my own lived experiences. No third-party sensitive data is exposed.</li>
            <li>Specific addresses of my village and family members' private details have been excluded or anonymized.</li>
        </ul>
        
        <div class='ethics-title' style='margin-top: 1rem;'>⚠️ Bias & Limitation Disclosure</div>
        <ul style='color:#4A3728; font-size:0.9rem; line-height:1.6;'>
            <li><b>Memory Bias:</b> The emotional scores from 1998-2005 are reconstructions based on fond nostalgia, not real-time tracking.</li>
            <li><b>Subjective Scoring:</b> The "Closeness Score" is highly subjective and heavily influenced by my current feelings of grief.</li>
            <li><b>Omitted Variables:</b> The data cannot fully capture the complexity of the Myanmar political crisis, which heavily influenced the trajectory of the later years.</li>
        </ul>

        <div class='ethics-title' style='margin-top: 1rem;'>📊 Visualization Justification</div>
        <ul style='color:#4A3728; font-size:0.9rem; line-height:1.6;'>
            <li><b>Area Chart:</b> Used to show the "volume" of time spent with BaBa over the years, making the drop to zero visually striking.</li>
            <li><b>Diverging Bar Chart:</b> Chosen specifically to show emotional polarity. By setting the lifetime average as the center line, it clearly visualizes the shift from the warmth of childhood presence to the cold reality of his passing and subsequent displacement.</li>
        </ul>
        
        <div class='ethics-title' style='margin-top: 1rem;'>🎯 Responsible use</div>
        <p style='color:#4A3728; font-size:0.9rem; line-height:1.6; margin:0;'>
        The decisions on this dashboard are personal reflections. They are not advice for others. I do not claim these patterns apply to everyone. Outside events like the Myanmar coup and displacement limited my choices in ways the data cannot fully show. No one else's private data is used or shared here. This project is an academic exercise only.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# CLOSING THOUGHT
# ---------------------------------------------------------
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

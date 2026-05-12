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

# Custom CSS styling
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

.ethics-block {
    background-color: #EFEBE1;
    border: 1px solid #D9CDB8;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 2rem 0;
}

.ethics-title {
    font-family: 'Lora', serif;
    font-size: 1.2rem;
    font-weight: 600;
    color: #4A3728;
    margin-bottom: 0.5rem;
}

.section-header {
    font-family: 'Lora', serif;
    font-size: 1.5rem;
    color: #4A3728;
    border-bottom: 1px solid #D9CDB8;
    padding-bottom: 0.5rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------
@st.cache_data
def load_data():
    # Load dataset
    df = pd.read_csv("baba_memories_dataset.csv")
    return df

df = load_data()

# ---------------------------------------------------------
# SIDEBAR FILTERS (Interactive Requirement)
# ---------------------------------------------------------
st.sidebar.title("🕯️ Samsara")
st.sidebar.markdown("Filter the memories and data below.")

# Filter by Life Stage
stages = ["All"] + list(df['life_stage'].unique())
selected_stage = st.sidebar.selectbox("Select Life Stage", stages)

# Filter by Year Range
min_year, max_year = int(df['year'].min()), int(df['year'].max())
selected_years = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

# Apply Filters
filtered_df = df.copy()
if selected_stage != "All":
    filtered_df = filtered_df[filtered_df['life_stage'] == selected_stage]
filtered_df = filtered_df[(filtered_df['year'] >= selected_years[0]) & (filtered_df['year'] <= selected_years[1])]

# ---------------------------------------------------------
# MAIN LAYOUT & HEADER
# ---------------------------------------------------------
st.title("Samsara — A Story of BaBa")

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

st.markdown("<div class='section-header'>Data Visualizations</div>", unsafe_allow_html=True)

# Create 2x2 grid layout for charts
col1, col2 = st.columns(2)

# CHART 1: Relationship Closeness Over Time
with col1:
    fig1 = px.line(
        filtered_df, 
        x="year", 
        y="relationship_closeness_score", 
        markers=True,
        title="1. The Cycle of Attachment (Closeness over Time)",
        color_discrete_sequence=["#C4956A"],
        hover_data=['memory_description', 'life_stage']
    )
    fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig1, use_container_width=True)

# CHART 2: Visit Frequency vs. Emotional Impact
with col2:
    fig2 = px.scatter(
        filtered_df, 
        x="visit_frequency_to_baba_per_year", 
        y="emotional_impact_score",
        size="relationship_closeness_score",
        color="life_stage",
        title="2. Presence vs. Emotional Resonance",
        hover_data=['year', 'memory_description']
    )
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)


# ---------------------------------------------------------
# CHART 3: DIVERGING BAR - EMOTIONAL IMPACT RELATIVE TO AVERAGE
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

# Calculate the overall average emotional impact score
overall_avg_impact = df['emotional_impact_score'].mean()

# Calculate the difference from the average for the diverging bar
diverging_df = filtered_df.copy()
diverging_df['impact_centered'] = diverging_df['emotional_impact_score'] - overall_avg_impact

# Determine colors: Warmth (Right/Positive) vs Grief (Left/Negative)
diverging_df['Color'] = diverging_df['impact_centered'].apply(lambda x: '#C4956A' if x >= 0 else '#5C4A32')
diverging_df['Direction'] = diverging_df['impact_centered'].apply(lambda x: 'Above Avg (Warmth)' if x >= 0 else 'Below Avg (Grief)')

fig3 = px.bar(
    diverging_df,
    x='impact_centered',
    y='year',
    orientation='h',
    title="3. The Shape of Samsara: Emotional Impact Relative to Lifetime Average",
    color='Direction',
    color_discrete_map={'Above Avg (Warmth)': '#C4956A', 'Below Avg (Grief)': '#5C4A32'},
    hover_data={'year': True, 'emotional_impact_score': True, 'impact_centered': False, 'memory_description': True},
    labels={'impact_centered': f'Variance from Average ({overall_avg_impact:.1f})', 'year': 'Year'}
)

# Add a vertical line for the average (0 point on the centered axis)
fig3.add_vline(x=0, line_width=2, line_dash="dash", line_color="#8C7560")
fig3.update_layout(
    barmode='relative',
    paper_bgcolor="rgba(0,0,0,0)", 
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(autorange="reversed") # Latest years at the bottom or top depending on preference
)

st.plotly_chart(fig3, use_container_width=True)


# CHART 4: Memory Categories Distribution
col3, col4 = st.columns([1, 1])
with col3:
    fig4 = px.pie(
        filtered_df, 
        names="memory_category", 
        title="4. Fragments of Memory (Categories)",
        color_discrete_sequence=px.colors.qualitative.Earth
    )
    fig4.update_traces(textposition='inside', textinfo='percent+label')
    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

with col4:
    st.markdown("### 🔍 Key Insights")
    st.markdown("""
    * **The Shape of Grief:** The Diverging Bar chart reveals exactly when the emotional tone shifted. Years on the right reflect periods of deep attachment and comfort at BaBa's house, while years leaning left visually represent the profound absence felt after 2020.
    * **Impermanence in Data:** The sharp drop in physical visits (due to moving, then the Myanmar military coup) highlights how rapidly life circumstances change, reinforcing BaBa's lessons on Samsara.
    * **Resilience:** Even in later years characterized by physical displacement and grief, the emotional impact score remains significant, showing that memory sustains connection even when physical presence ends.
    """)

# ---------------------------------------------------------
# DECISION MAKING & ETHICS (MANDATORY RUBRIC REQUIREMENTS)
# ---------------------------------------------------------
st.markdown("<div class='section-header'>Future Decisions & Ethics</div>", unsafe_allow_html=True)

st.markdown("""
<div class='ethics-block'>
    <div class='ethics-title'>⚖️ Privacy & Limitations</div>
    <ul>
        <li><strong>Privacy Statement:</strong> This dataset focuses entirely on my personal experiences. Names of specific extended family members outside the core narrative have been anonymized or generalized.</li>
        <li><strong>Memory Bias:</strong> Emotional impact scores are entirely subjective. They represent how I feel <i>now</i> about memories from my childhood, not necessarily how I felt in that exact moment.</li>
        <li><strong>Small Dataset:</strong> This is a lifetime mapped into a few dozen rows. The data simplifies complex, multi-layered human experiences into single scores.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='ethics-block'>
    <div class='ethics-title'>🎯 Responsible use & Decision Making</div>
    <p style='color:#4A3728; font-size:0.9rem; line-height:1.75; margin:0;'>
    <strong>Based on this data, what will I do differently?</strong><br>
    The visual drop in "presence" leading up to BaBa's passing serves as a stark reminder of impermanence. In the future, I aim to consciously invest time into my remaining loved ones and document conversations while they are still here, recognizing that the "warmth" (right-side bars) comes primarily from daily, simple routines rather than grand events.<br><br>
    <strong>Responsibility:</strong> The decisions on this dashboard are personal reflections. They are not advice for others.
    I do not claim these patterns apply to everyone. Outside events like the Myanmar coup and displacement
    limited my choices in ways the data cannot fully show. No one else's private data is used or shared here. This project is an academic exercise only.
    </p>
</div>
""", unsafe_allow_html=True)

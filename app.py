from theme import apply_theme, render_sidebar
from auth import init_auth, login_form, require_login
import streamlit as st

COMPANY_NAME = "Pizzeria Insights"

apply_theme()
init_auth()

if not require_login():
    login_form(COMPANY_NAME)
    st.stop()

render_sidebar(COMPANY_NAME)

# 🎨 Extra CSS for Home Page
st.markdown("""
<style>
.hero-box {
    background: linear-gradient(135deg, #065f46, #10b981);
    padding: 2rem;
    border-radius: 22px;
    color: white;
    margin-bottom: 1.5rem;
    text-align: center;
}

.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
}

.hero-subtitle {
    font-size: 1.1rem;
    opacity: 0.95;
}

.section-title {
    font-size: 1.4rem;
    font-weight: bold;
    margin-top: 1rem;
}

.card {
    background: white;
    padding: 1.4rem;
    border-radius: 20px;
    border: 1px solid #e5e7eb;
    transition: 0.3s;
    text-align: center;
    min-height: 200px;
}

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.card-title {
    font-size: 1.2rem;
    font-weight: 700;
}

.card-text {
    color: #4b5563;
    font-size: 0.95rem;
    margin: 0.7rem 0;
    line-height: 1.6;
}

.metric-box {
    background: #ecfdf5;
    border-radius: 15px;
    padding: 1rem;
    text-align: center;
    border: 1px solid #d1fae5;
}

.metric-number {
    font-size: 1.5rem;
    font-weight: bold;
    color: #065f46;
}

.metric-label {
    font-size: 0.9rem;
    color: #047857;
}
</style>
""", unsafe_allow_html=True)

# 🍕 Hero Section
st.markdown("""
<div class="hero-box">
    <div class="hero-title">🍕 Pizzeria Insights</div>
    <div class="hero-subtitle">
        A powerful platform for analyzing customer experience using CSAT, CES, NPS, and advanced analytics tools.
    </div>
</div>
""", unsafe_allow_html=True)

# Section Title
st.markdown('<div class="section-title">Available Tools</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")
col3, col4 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">📈 CSAT</div>
        <div class="card-text">
            Measure customer satisfaction on a scale from 1 to 5 and calculate the overall satisfaction percentage.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_csat.py", label="Open CSAT", icon="📈")

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">⚙️ CES</div>
        <div class="card-text">
            Analyze customer effort on a scale from 1 to 7 and evaluate ease of service experience.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_ces.py", label="Open CES", icon="⚙️")

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-title">⭐ NPS</div>
        <div class="card-text">
            Calculate Net Promoter Score on a scale from 1 to 10 and classify customers into promoters, passives, and detractors.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_nps.py", label="Open NPS", icon="⭐")

with col4:
    st.markdown("""
    <div class="card">
        <div class="card-title">📊 Analysis Tool</div>
        <div class="card-text">
            Perform advanced column analysis and generate insights with visual charts and exportable results.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/4_analysis.py", label="Open Analysis", icon="📊")

st.markdown("<br>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-number">4</div>
        <div class="metric-label">Tools</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-number">Excel</div>
        <div class="metric-label">File Support</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-number">PPTX</div>
        <div class="metric-label">Export</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-number">Live</div>
        <div class="metric-label">Real-Time</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<br>
<center style="color: gray;">
Use the sidebar or the buttons above to navigate between tools.
</center>
""", unsafe_allow_html=True)
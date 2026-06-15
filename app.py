from auth import init_auth, login_form, require_login
from theme import apply_theme, render_sidebar
import streamlit as st

COMPANY_NAME = "Pizzeria Insights"

apply_theme()
init_auth()

if not require_login():
    login_form(COMPANY_NAME)
    st.stop()

render_sidebar(COMPANY_NAME)


def tool_card(title, description, page, icon):
    st.markdown(f"""
    <div class="tool-card">
        <div class="tool-title">{icon} {title}</div>
        <div class="tool-text">{description}</div>
    </div>
    """, unsafe_allow_html=True)

    st.page_link(page, label=f"Open {title}", icon=icon)


def metric_box(number, label):
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number">{number}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div class="hero-box">
    <div class="hero-title">🍕 Pizzeria Insights</div>
    <div class="hero-subtitle">
        A powerful platform for analyzing customer experience using CSAT, CES, NPS, compliance, and advanced analytics tools.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Available Tools</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")
col3, col4 = st.columns(2, gap="large")
col5, col6 = st.columns(2, gap="large")

with col1:
    tool_card(
        "CSAT",
        "Measure customer satisfaction on a scale from 1 to 5 and calculate the overall satisfaction percentage.",
        "pages/1_csat.py",
        "📈"
    )

with col2:
    tool_card(
        "CES",
        "Analyze customer effort on a scale from 1 to 7 and evaluate ease of service experience.",
        "pages/2_ces.py",
        "⚙️"
    )

with col3:
    tool_card(
        "NPS",
        "Calculate Net Promoter Score on a scale from 1 to 10 and classify customers into promoters, passives, and detractors.",
        "pages/3_nps.py",
        "⭐"
    )

with col4:
    tool_card(
        "Analysis Tool",
        "Perform advanced column analysis and generate insights with visual charts and exportable results.",
        "pages/4_analysis.py",
        "📊"
    )

with col5:
    tool_card(
        "Report Automation",
        "Generate weekly PowerPoint reports automatically using a fixed template and uploaded Excel data.<br><br>Institute of Public Administration.",
        "pages/5_report_automation.py",
        "📄"
    )

with col6:
    tool_card(
        "Compliance",
        "Analyze compliance using values 1 (Compliant), 0 (Partially Compliant), and -1 (Not Compliant), with automatic calculation and export.",
        "pages/6_compliance.py",
        "✅"
    )

st.markdown("<br>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

with m1:
    metric_box("6", "Tools")

with m2:
    metric_box("Excel", "File Support")

with m3:
    metric_box("PPTX", "Export")

with m4:
    metric_box("Live", "Real-Time")

st.markdown("""
<br>
<center style="color: gray;">
Use the sidebar or the buttons above to navigate between tools.
</center>
""", unsafe_allow_html=True)
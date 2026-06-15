import streamlit as st

def apply_theme():
    st.set_page_config(
        page_title="Pizzeria Insights",
        page_icon="🍕",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
    <style>
    .stApp {
        background-color: #fffaf0;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #7f1d1d, #15803d);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

   section[data-testid="stSidebar"] .stButton button {
    background-color: #b91c1c !important;
    color: white !important;
    border: 1px solid #ef4444 !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background-color: #991b1b !important;
    color: white !important;
    border-color: #fecaca !important;

    }

    [data-testid="stSidebarNav"] {
        display: none;
    }

    .hero-box {
        background: linear-gradient(135deg, #b91c1c, #15803d);
        padding: 2rem;
        border-radius: 24px;
        color: white;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 12px 30px rgba(0,0,0,0.12);
    }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.95;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 800;
        margin-top: 1rem;
        margin-bottom: 0.7rem;
        color: #1f2937;
    }

    .tool-card {
        background: white;
        padding: 1.4rem;
        border-radius: 20px;
        border: 1px solid #fed7aa;
        min-height: 200px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        transition: 0.3s;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .tool-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 10px 25px rgba(185, 28, 28, 0.12);
    }

    .tool-title {
        font-size: 1.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        color: #7f1d1d;
    }

    .tool-text {
        color: #4b5563;
        font-size: 0.96rem;
        line-height: 1.7;
        margin-bottom: 1rem;
    }

    .metric-box {
        background: #fef3c7;
        border: 1px solid #fde68a;
        border-radius: 18px;
        padding: 1rem;
        text-align: center;
    }

    .metric-number {
        font-size: 1.5rem;
        font-weight: 800;
        color: #92400e;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #78350f;
    }

    .login-box {
        max-width: 420px;
        margin: 3rem auto;
        background: white;
        padding: 2rem;
        border-radius: 24px;
        border: 1px solid #fed7aa;
        box-shadow: 0 12px 30px rgba(0,0,0,0.08);
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar(company_name="Pizzeria Insights"):
    with st.sidebar:
        st.markdown(f"## 🍕 {company_name}")
        st.caption("Customer Experience Platform")
        st.markdown("---")

        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("pages/1_csat.py", label="CSAT", icon="📈")
        st.page_link("pages/2_ces.py", label="CES", icon="⚙️")
        st.page_link("pages/3_nps.py", label="NPS", icon="⭐")
        st.page_link("pages/4_analysis.py", label="Analysis", icon="📊")
        st.page_link("pages/5_report_automation.py", label="Report Automation", icon="📄")
        st.page_link("pages/6_compliance.py", label="Compliance", icon="✅")

        st.markdown("---")

        if st.session_state.get("logged_in"):
            st.write(f"Signed in as: **{st.session_state.get('username')}**")

            if st.button("Logout", use_container_width=True):
                st.session_state["logged_in"] = False
                st.session_state["username"] = ""
                st.rerun()
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
        background-color: #f8fafc;
    }

    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #064e3b, #10b981);
    }

    /* Make sidebar text white */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Hide Streamlit default pages navigation */
    [data-testid="stSidebarNav"] {
        display: none;
    }

    .hero-box {
        background: linear-gradient(135deg, #065f46, #10b981);
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

    .tool-card {
        background: white;
        padding: 1.4rem;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        min-height: 200px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
    }

    .tool-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #111827;
    }

    .tool-text {
        color: #4b5563;
        font-size: 0.96rem;
        line-height: 1.7;
        margin-bottom: 1rem;
    }

    .metric-box {
        background: #ecfdf5;
        border: 1px solid #d1fae5;
        border-radius: 18px;
        padding: 1rem;
        text-align: center;
    }

    .metric-number {
        font-size: 1.5rem;
        font-weight: 800;
        color: #065f46;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #047857;
    }

    .login-box {
        max-width: 420px;
        margin: 3rem auto;
        background: white;
        padding: 2rem;
        border-radius: 24px;
        border: 1px solid #e5e7eb;
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

        st.markdown("---")

        if st.session_state.get("logged_in"):
            st.write(f"Signed in as: **{st.session_state.get('username')}**")

            if st.button("Logout", use_container_width=True):
                st.session_state["logged_in"] = False
                st.session_state["username"] = ""
                st.rerun()
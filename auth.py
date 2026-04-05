import streamlit as st

USERS = {
    "admin": "1234",
    "ahmed": "1234"
}

def init_auth():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = ""

def login_form(company_name="Pizzeria Insights"):
    st.markdown("""
    <div class="hero-box">
        <div class="hero-title">🍕 Pizzeria Insights</div>
        <div class="hero-subtitle">
            Sign in to access the analytics dashboard.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("### Welcome Back")
    st.write("Please enter your username and password.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if username in USERS and USERS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid username or password")

    st.markdown("</div>", unsafe_allow_html=True)

def require_login():
    return st.session_state.get("logged_in", False)
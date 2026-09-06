import streamlit as st

# ⚠️ set_page_config hamesha FIRST Streamlit command hona chahiye
st.set_page_config(page_title="HMF book", page_icon="🟢", layout="centered")

# ---- Navigation state (page switch ke liye) ----
if "page" not in st.session_state:
    st.session_state.page = "splash"


# ============================================================
#                  PAGE 1: SPLASH SCREEN
# ============================================================
if st.session_state.page == "splash":

    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #00B074 0%, #056839 100%) !important;
        }
        /* Streamlit header, menu, footer hide */
        header[data-testid="stHeader"], #MainMenu, footer {
            visibility: hidden;
        }
        .main-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 70vh;
            text-align: center;
        }
        .logo-text {
            font-size: 90px;
            font-weight: 900;
            margin: 0;
            letter-spacing: 4px;
            color: white;
            text-shadow: 0 4px 12px rgba(0,0,0,0.25);
        }
        .subtitle-text {
            font-size: 24px;
            font-weight: 600;
            color: rgba(255,255,255,0.9);
            margin: 5px 0 0 0;
            letter-spacing: 2px;
        }
        div[data-testid="stButton"] > button,
        div.stButton > button {
            background-color: white !important;
            color: #00B074 !important;
            font-size: 18px !important;
            font-weight: bold !important;
            padding: 12px 45px !important;
            border-radius: 30px !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.25) !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stButton"] > button:hover,
        div.stButton > button:hover {
            transform: scale(1.05) !important;
            background-color: #f0fff5 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # ✅ FIX 1: Pura HTML ab EK hi markdown call mein
    # (pehle div/h1/p alag calls mein the is liye CSS apply nahi hoti thi)
    st.markdown("""
        <div class="main-container">
            <h1 class="logo-text">HMF</h1>
            <p class="subtitle-text">HMF book</p>
        </div>
    """, unsafe_allow_html=True)

    # Center-aligned Get Started button
    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        if st.button("Get Started", use_container_width=True):
            # ✅ FIX 2: Ab asli page switch hota hai
            st.session_state.page = "signup"
            st.rerun()


# ============================================================
#                  PAGE 2: SIGNUP SCREEN
# ============================================================
elif st.session_state.page == "signup":

    st.markdown("""
        <style>
        .stApp {
            background: #F6FCF8 !important;
        }
        header[data-testid="stHeader"], #MainMenu, footer {
            visibility: hidden;
        }
        .hmf-badge {
            background: linear-gradient(135deg, #00B074, #056839);
            display: inline-block;
            padding: 22px 55px;
            border-radius: 24px;
            box-shadow: 0 6px 18px rgba(0,176,116,0.35);
        }
        .hmf-badge h1 {
            color: white;
            font-size: 40px;
            font-weight: 900;
            letter-spacing: 3px;
            margin: 0;
        }
        .create-title {
            color: #222;
            font-size: 26px;
            font-weight: 700;
            margin-top: 28px;
            margin-bottom: 5px;
        }
        .create-sub {
            color: #888;
            font-size: 14px;
            margin-top: 0;
        }
        .or-continue {
            text-align: center;
            color: #999;
            font-size: 14px;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        div[data-testid="stButton"] > button,
        div.stButton > button {
            background: #00B074 !important;
            color: white !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 12px !important;
        }
        div[data-testid="stTextInput"] input {
            border-radius: 12px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # HMF header + Create Account (ek hi call mein)
    st.markdown("""
        <div style="text-align:center; margin-top:20px;">
            <div class="hmf-badge"><h1>HMF</h1></div>
            <h2 class="create-title">Create Account</h2>
            <p class="create-sub">Sign up to continue to HMF book</p>
        </div>
    """, unsafe_allow_html=True)

    # Input fields — Password mein eye icon built-in hai
    username = st.text_input("Username", placeholder="Enter your username")
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # Sign Up button (validation ke saath)
    if st.button("Sign Up", use_container_width=True):
        if username and email and password:
            st.success("Account created successfully! 🎉")
        else:
            st.error("Please fill in all fields!")

    # Or continue with
    st.markdown('<p class="or-continue">Or continue with</p>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.button("Google", use_container_width=True)
    with c2:
        st.button("Snapchat", use_container_width=True)
    with c3:
        st.button("Facebook", use_container_width=True)

    # Bottom: Login link + Back button
    st.markdown("<hr style='margin-top:35px; margin-bottom:15px;'>", unsafe_allow_html=True)
    bcol1, bcol2 = st.columns([1.5, 1])
    with bcol1:
        st.markdown(
            "<p style='color:#555; font-size:15px; margin:0; padding-top:8px;'>"
            "Already have an account? <b style='color:#00B074;'>Login</b></p>",
            unsafe_allow_html=True,
        )
    with bcol2:
        if st.button("⬅ Back"):
            st.session_state.page = "splash"
            st.rerun()

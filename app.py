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
import streamlit as st

# Page Configuration
st.set_page_config(page_title="HMF book", page_icon="🟢", layout="centered")

# Custom CSS for Instagram-Style Green Interface
st.markdown("""
    <style>
    /* Main Background Layout */
    .stApp {
        background-color: #f0f2f5 !important;
        color: #1f2937 !important;
    }
    
    /* Global App Container to mimic a Mobile Device Frame */
    .mobile-frame {
        max-width: 450px;
        margin: 0 auto;
        background-color: #ffffff;
        min-height: 100vh;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.1);
        display: flex;
        flex-direction: column;
    }

    /* 1. Instagram-Style Header Top Bar */
    .insta-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 20px;
        background-color: #ffffff;
        border-b: 1px solid #e5e7eb;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .brand-logo {
        font-size: 28px;
        font-weight: 900;
        color: #00B074;
        font-style: italic;
        letter-spacing: -1px;
    }
    .header-icons {
        display: flex;
        gap: 20px;
        font-size: 22px;
        color: #374151;
    }

    /* 2. Stories Row with Green Gradient Rings */
    .stories-container {
        display: flex;
        gap: 15px;
        padding: 12px 15px;
        background-color: #ffffff;
        border-bottom: 1px solid #f3f4f6;
        overflow-x: auto;
    }
    .story-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        min-width: 65px;
    }
    .story-ring {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        padding: 2.5px;
        background: linear-gradient(135deg, #00B074 0%, #056839 100%);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .story-img {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background-color: #e5e7eb;
        border: 2px solid white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #4b5563;
        font-size: 18px;
    }
    .story-name {
        font-size: 11px;
        color: #4b5563;
        margin-top: 4px;
        max-width: 65px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    /* 3. Feed Post Card Styling */
    .post-card {
        background-color: #ffffff;
        margin-bottom: 12px;
        border-bottom: 1px solid #e5e7eb;
    }
    .post-header {
        display: flex;
        align-items: center;
        padding: 12px 15px;
    }
    .post-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background-color: #00B074;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 10px;
    }
    .post-username {
        font-size: 14px;
        font-weight: 700;
        color: #1f2937;
    }
    .post-image-placeholder {
        width: 100%;
        height: 350px;
        background-color: #f3f4f6;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        color: #9ca3af;
        border-y: 1px solid #f3f4f6;
    }
    .post-actions {
        display: flex;
        justify-content: space-between;
        padding: 12px 15px;
        font-size: 22px;
        color: #374151;
    }
    .action-left {
        display: flex;
        gap: 18px;
    }
    .post-details {
        padding: 0px 15px 15px 15px;
    }
    .likes-count {
        font-size: 14px;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 4px;
    }
    .post-caption {
        font-size: 14px;
        color: #374151;
    }
    .post-caption b {
        color: #1f2937;
        margin-right: 5px;
    }

    /* 4. Fixed Bottom Navigation Bar */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #ffffff;
        border-top: 1px solid #e5e7eb;
        display: flex;
        justify-content: space-around;
        padding: 12px 0px;
        font-size: 24px;
        color: #4b5563;
        z-index: 1000;
        max-width: 450px;
        margin: 0 auto;
    }
    .nav-item-active {
        color: #00B074 !important;
    }
    </style>
""", unsafe_allowed_html=True)

# Main Application Frame Renderer
st.markdown('<div class="mobile-frame">', unsafe_allowed_html=True)

# --- 1. INSTAGRAM TOP HEADER ---
st.markdown("""
    <div class="insta-header">
        <div class="brand-logo">HMF book</div>
        <div class="header-icons">
            <span>➕</span>
            <span>❤️</span>
            <span>💬</span>
        </div>
    </div>
""", unsafe_allowed_html=True)

# --- 2. INSTAGRAM STORIES ROW ---
st.markdown("""
    <div class="stories-container">
        <div class="story-card">
            <div class="story-ring"><div class="story-img" style="background-color: #056839; color: white;">+</div></div>
            <div class="story-name">Your Story</div>
        </div>
        <div class="story-card">
            <div class="story-ring"><div class="story-img">HJ</div></div>
            <div class="story-name">hoor_jannat</div>
        </div>
        <div class="story-card">
            <div class="story-ring"><div class="story-img">FM</div></div>
            <div class="story-name">farrukh_m</div>
        </div>
        <div class="story-card">
            <div class="story-ring"><div class="story-img">AK</div></div>
            <div class="story-name">ali_khan</div>
        </div>
    </div>
""", unsafe_allowed_html=True)

# --- 3. DYNAMIC POST FEED CONTENT ---
# Post 1
st.markdown("""
    <div class="post-card">
        <div class="post-header">
            <div class="post-avatar">HJ</div>
            <div class="post-username">hoor_jannat</div>
        </div>
        <div class="post-image-placeholder" style="background: linear-gradient(45deg, #e6f7f0, #b3e6cc); color: #056839; font-weight: bold;">
            🖼️ HMF Post Layout Setup
        </div>
        <div class="post-actions">
            <div class="action-left">
                <span>❤️</span>
                <span>💬</span>
                <span>🚀</span>
            </div>
            <div><span>🔖</span></div>
        </div>
        <div class="post-details">
            <div class="likes-count">143 likes</div>
            <div class="post-caption"><b>hoor_jannat</b> New layout system for our green minimalist app environment! Testing responsive framework.</div>
        </div>
    </div>
""", unsafe_allowed_html=True)

# Post 2
st.markdown("""
    <div class="post-card">
        <div class="post-header">
            <div class="post-avatar">FM</div>
            <div class="post-username">farrukh_m</div>
        </div>
        <div class="post-image-placeholder" style="background: linear-gradient(45deg, #f0fdf4, #ccfbf1); color: #047857; font-weight: bold;">
            🎮 Ludo Game Mode Preview Coming Soon
        </div>
        <div class="post-actions">
            <div class="action-left">
                <span>❤️</span>
                <span>💬</span>
                <span>🚀</span>
            </div>
            <div><span>🔖</span></div>
        </div>
        <div class="post-details">
            <div class="likes-count">52 likes</div>
            <div class="post-caption"><b>farrukh_m</b> Multi-device configuration setup done. Next step is real-time ludo match implementation.</div>
        </div>
    </div>
""", unsafe_allowed_html=True)

# Extra spacer to ensure content isn't cut off by the fixed bottom navigation bar
st.markdown("<br><br><br>", unsafe_allowed_html=True)

# --- 4. FIXED BOTTOM NAVIGATION BAR ---
st.markdown("""
    <div class="bottom-nav">
        <span class="nav-item-active">🏠</span>
        <span>🔍</span>
        <span>➕</span>
        <span>🎮</span>
        <span>👤</span>
    </div>
""", unsafe_allowed_html=True)

st.markdown('</div>', unsafe_allowed_html=True)

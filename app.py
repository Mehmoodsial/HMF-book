import streamlit as st
import json, os
from datetime import datetime

st.set_page_config(
    page_title="HMF Book",
    page_icon="📖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- Session State (KeyError fix) ----------
defaults = {"logged_in": False, "username": "", "name": ""}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# ---------- Current page (query params se) ----------
def get_page():
    try:
        return st.query_params.get("page", "home")
    except AttributeError:  # purana Streamlit
        return st.experimental_get_query_params().get("page", ["home"])[0]

page = get_page()

# ================= INSTAGRAM-STYLE BOTTOM NAVBAR =================
def bottom_navbar(current):
    def cls(p):
        return "nav-link active" if p == current else "nav-link"

    st.markdown(f"""
    <style>
        /* Streamlit ka default toolbar chhupao */
        #MainMenu, header[data-testid="stHeader"], footer {{
            visibility: hidden;
        }}
        /* Content ko upar khiskao taake navbar ke neeche na chhupe */
        .block-container {{
            padding-bottom: 100px !important;
            max-width: 600px;
        }}
        /* Fixed Bottom Navbar — Instagram jaisa */
        .ig-nav {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 60px;
            background: #ffffff;
            border-top: 1px solid #dbdbdb;
            display: flex;
            justify-content: space-around;
            align-items: center;
            z-index: 9999;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.06);
        }}
        .ig-nav a {{
            text-decoration: none;
            font-size: 22px;
            color: #262626;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1px;
            transition: transform 0.15s ease;
        }}
        .ig-nav a:hover {{ transform: scale(1.2); }}
        .ig-nav a.active {{ color: #ff3040; }}
        .ig-nav a .lbl {{
            font-size: 9px;
            font-family: -apple-system, sans-serif;
        }}
    </style>

    <nav class="ig-nav">
        <a href="?page=home" class="{cls('home')}">
            🏠<span class="lbl">Home</span>
        </a>
        <a href="?page=search" class="{cls('search')}">
            🔍<span class="lbl">Search</span>
        </a>
        <a href="?page=add" class="{cls('add')}">
            ➕<span class="lbl">Add</span>
        </a>
        <a href="?page=favorites" class="{cls('favorites')}">
            ❤️<span class="lbl">Likes</span>
        </a>
        <a href="?page=profile" class="{cls('profile')}">
            👤<span class="lbl">Profile</span>
        </a>
    </nav>
    """, unsafe_allow_html=True)

# ---------- Login Page ----------
def login_page():
    st.title("📖 HMF Book")
    st.caption("Apne doston se connect karo")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            users = load_users()
            user = users.get(username)
            if user and user.get("password") == password:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["name"] = user.get("name", username)
                st.rerun()
            else:
                st.error("❌ Galat username ya password!")

    with tab2:
        name = st.text_input("Apna naam")
        new_user = st.text_input("Username chuno")
        new_pass = st.text_input("Password chuno", type="password")
        if st.button("Account banao", use_container_width=True):
            users = load_users()
            if new_user in users:
                st.warning("Ye username pehle se le liya gaya hai!")
            elif new_user and new_pass:
                users[new_user] = {
                    "name": name or new_user,
                    "password": new_pass,
                    "created": str(datetime.now()),
                }
                save_users(users)
                st.success("✅ Account ban gaya! Ab Login karo.")
            else:
                st.warning("Username aur password dono zaroori hain!")

# ---------- Pages ----------
def page_home():
    name = st.session_state.get("name", "")
    st.markdown(f"### 👋 Welcome, {name}!")

    # Your Story section (pehle jaisa)
    st.markdown("**✨ Your Story**")
    cols = st.columns([3, 1])
    with cols[0]:
        story = st.text_input("Add to Story...", label_visibility="collapsed")
    with cols[1]:
        if st.button("Post", use_container_width=True):
            if story.strip():
                st.success("Story post ho gayi! 🎉")
            else:
                st.warning("Story khali hai!")

    st.divider()
    st.markdown("**📰 Feed**")
    st.info("Yahan feed aayegi — posts, stories, etc.")

def page_search():
    st.markdown("### 🔍 Search")
    q = st.text_input("Dhundo...", placeholder="Users ya posts")
    if q:
        users = load_users()
        found = [u for u in users if q.lower() in u.lower()]
        if found:
            for u in found:
                st.write(f"👤 **{users[u].get('name', u)}** (@{u})")
        else:
            st.warning("Kuch nahi mila!")

def page_add():
    st.markdown("### ➕ Add Story / Post")
    txt = st.text_area("Kya share karna hai?", height=120)
    if st.button("Post karo", use_container_width=True):
        if txt.strip():
            st.success("Post ho gaya! 🎉")
        else:
            st.warning("Khali post nahi ho sakta!")

def page_favorites():
    st.markdown("### ❤️ Favorites")
    st.info("Yahan aapki pasandeeda cheezein aayengi.")

def page_profile():
    username = st.session_state.get("username", "")
    name = st.session_state.get("name", "")
    st.markdown("### 👤 Profile")
    st.write(f"**Naam:** {name}")
    st.write(f"**Username:** @{username}")

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.session_state["name"] = ""
        try:
            st.query_params.clear()
        except AttributeError:
            pass
        st.rerun()

# ---------- Router ----------
if not st.session_state.get("logged_in"):
    login_page()          # Login pehle
else:
    bottom_navbar(page)   # Instagram-style navbar neeche
    if page == "search":
        page_search()
    elif page == "add":
        page_add()
    elif page == "favorites":
        page_favorites()
    elif page == "profile":
        page_profile()
    else:
        page_home()
    

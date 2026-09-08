import streamlit as st
import json, os
from datetime import datetime

st.set_page_config(page_title="HMF Book", page_icon="📖", layout="wide")

# ---------- Session State (KeyError ka asli fix yahi hai) ----------
defaults = {"logged_in": False, "username": "", "name": ""}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

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
            # .get() use kiya — isliye KeyError kabhi nahi aayega
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

# ---------- Main App (login ke baad) ----------
def main_app():
    # Safe access
    name = st.session_state.get("name", "")
    username = st.session_state.get("username", "")

    st.title(f"📖 HMF Book")
    st.write(f"Welcome, **{name}** 👋")

    tabs = st.tabs(["🏠 Home", "👥 Following", "⭐ Favorites"])
    with tabs[0]:
        st.subheader("Your Story")
        story = st.text_area("Add to Story...", height=100)
        if st.button("Post Story"):
            if story.strip():
                st.success("Story post ho gayi! 🎉")
            else:
                st.warning("Story khali hai!")

    if st.sidebar.button("🚪 Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()

# ---------- Router (yehi "pehle jaisa" flow banata hai) ----------
if not st.session_state.get("logged_in"):
    login_page()      # Login page PEHLE dikhega
else:
    main_app()        # Login ke baad app

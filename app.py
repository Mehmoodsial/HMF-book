import os
import json
import html
from urllib.parse import quote

import streamlit as st

# ================== PAGE SETUP ==================
st.set_page_config(
    page_title="HMF Book",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ================== SAFE HELPERS ==================
def get_param(key, default=""):
    try:
        value = st.query_params.get(key, default)
        if isinstance(value, list):
            value = value[0] if value else default
        return value or default
    except Exception:
        try:
            params = st.experimental_get_query_params()
            value = params.get(key, [default])
            return value[0] if value else default
        except Exception:
            return default


def set_param(key, value):
    try:
        st.query_params[key] = value
    except Exception:
        try:
            st.experimental_set_query_params(**{key: value})
        except Exception:
            pass


def do_rerun():
    try:
        st.rerun()
    except Exception:
        try:
            st.experimental_rerun()
        except Exception:
            pass


# ================== CHAT STORAGE ==================
CHAT_FILE = "chats.json"


def load_chats():
    if os.path.exists(CHAT_FILE):
        try:
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
        except Exception:
            pass
    return []


def save_chats(chats):
    try:
        with open(CHAT_FILE, "w", encoding="utf-8") as f:
            json.dump(chats, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


page = get_param("page", "home")
user_name = get_param("name", "")


# ================== AUTO REFRESH (har 5 second) ==================
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=5000, key="chat_autorefresh")
except Exception:
    pass


# ================== CSS ==================
st.markdown(
    """
    <style>
        .stApp { padding-bottom: 90px; }

        /* Main content ko mobile jaisa patla rakhta hai */
        .block-container {
            max-width: 500px;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .chat-box {
            background: #f1f1f1;
            border-radius: 14px;
            padding: 10px 14px;
            margin-bottom: 10px;
        }
        .chat-name { font-size: 12px; color: #888888; }
        .chat-text { font-size: 15px; color: #262626; word-wrap: break-word; }

        /* ===== BOTTOM MENU BAR (app ke andar, mobile width mein) ===== */
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 500px;
            height: 60px;
            background: #ffffff;
            display: flex;
            flex-direction: row;
            justify-content: space-around;
            align-items: center;
            border-top: 1px solid #dbdbdb;
            border-radius: 0;
            box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.05);
            z-index: 999999;
        }
        .bottom-nav a {
            text-decoration: none;
            font-size: 24px;
            padding: 6px 12px;
            border-radius: 10px;
        }
        .bottom-nav a.active { background: #e7f3ff; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ================== BOTTOM MENU BAR ==================
def bottom_nav(current):
    icons = [
        ("home", "🏠"),
        ("videos", "🎬"),
        ("add", "➕"),
        ("chats", "💬"),
        ("profile", "👤"),
        ("settings", "⚙️"),
    ]
    suffix = ""
    if user_name:
        suffix = "&name=" + quote(user_name)
    links = ""
    for key, icon in icons:
        active_class = "active" if key == current else ""
        links += f'<a class="{active_class}" href="?page={key}{suffix}">{icon}</a>'
    st.markdown(f'<div class="bottom-nav">{links}</div>', unsafe_allow_html=True)


# ================== PAGES ==================
if page == "home":
    st.markdown("<h1 style='text-align:center;'>💬 HMF Book</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Neeche menu se page chunein.</p>", unsafe_allow_html=True)

elif page == "videos":
    st.title("🎬 Videos")
    st.info("Videos page — yahan aapka videos content aayega.")

elif page == "add":
    st.title("➕ Add")
    st.info("Add page — yahan aapka add content aayega.")

elif page == "chats":
    st.title("💬 Messages")

    if user_name == "":
        new_name = st.text_input("Aapka naam likhein")
        if st.button("Start Chat"):
            if new_name.strip():
                set_param("name", new_name.strip())
                do_rerun()
    else:
        st.success("Aap: " + user_name)
        chats = load_chats()

        for c in chats:
            c_name = html.escape(str(c.get("name", "")))
            c_msg = html.escape(str(c.get("message", "")))
            st.markdown(
                '<div class="chat-box">'
                '<div class="chat-name">👤 ' + c_name + '</div>'
                '<div class="chat-text">' + c_msg + '</div>'
                '</div>',
                unsafe_allow_html=True,
            )

        with st.form("message_form", clear_on_submit=True):
            msg = st.text_input("Message", placeholder="Type a message...", label_visibility="collapsed")
            send = st.form_submit_button("Send")

        if send and msg.strip():
            chats.append({"name": user_name, "message": msg.strip()})
            save_chats(chats)
            do_rerun()

        st.caption("🔄 Chats auto-refresh every few seconds.")

elif page == "profile":
    st.title("👤 Profile")
    if user_name:
        st.success("Logged in as: " + user_name)
    else:
        st.info("Pehle Chats page par apna naam dein.")

else:
    st.title("⚙️ Settings")
    st.info("Settings page — yahan aapki settings aayengi.")


# ================== MENU BAR HAMESHA NEECHE ==================
bottom_nav(page)

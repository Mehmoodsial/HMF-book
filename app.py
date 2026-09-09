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

# ================== CHAT STORAGE ==================
CHAT_FILE = "chats.json"


def load_chats():
    if os.path.exists(CHAT_FILE):
        try:
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_chats(chats):
    try:
        with open(CHAT_FILE, "w", encoding="utf-8") as f:
            json.dump(chats, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ================== CURRENT PAGE / NAME (menu se aata hai) ==================
try:
    page = st.query_params.get("page", "home") or "home"
    user_name = st.query_params.get("name", "") or ""
except Exception:
    page = "home"
    user_name = ""


# ================== AUTO REFRESH (har 5 second) ==================
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=5000, key="auto_refresh")
except Exception:
    pass


# ================== CSS ==================
st.markdown(
    """
    <style>
        .stApp { padding-bottom: 90px; }
        header[data-testid="stHeader"] { display: none; }

        .chat-box {
            background: #f1f1f1;
            border-radius: 14px;
            padding: 10px 14px;
            margin-bottom: 10px;
        }
        .chat-name { font-size: 12px; color: #888888; }
        .chat-text { font-size: 15px; color: #262626; word-wrap: break-word; }

        /* ===== BOTTOM MENU BAR (Instagram Style) ===== */
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 60px;
            background: #ffffff;
            display: flex;
            justify-content: space-around;
            align-items: center;
            border-top: 1px solid #dbdbdb;
            z-index: 999999;
        }
        .bottom-nav a {
            text-decoration: none;
            font-size: 25px;
            padding: 6px 14px;
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
    suffix = f"&name={quote(user_name)}" if user_name else ""
    links = ""
    for key, icon in icons:
        active = "active" if key == current else ""
        links += f'<a class="{active}" href="?page={key}{suffix}">{icon}</a>'
    st.markdown(
        f'<div class="bottom-nav">{links}</div>',
        unsafe_allow_html=True,
    )


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
        if st.button("Start Chat", type="primary", use_container_width=True):
            if new_name.strip():
                st.query_params["name"] = new_name.strip()
                st.rerun()
    else:
        chats = load_chats()

        for c in chats:
            st.markdown(
                f"""
                <div class="chat-box">
                    <div class="chat-name">👤 {html.escape(str(c.get("name", "")))}</div>
                    <div class="chat-text">{html.escape(str(c.get("message", "")))}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with st.form("message_form", clear_on_submit=True):
            msg = st.text_input(
                "Message",
                placeholder="Type a message...",
                label_visibility="collapsed",
            )
            send = st.form_submit_button("Send", type="primary", use_container_width=True)

        if send and msg.strip():
            chats.append({"name": user_name, "message": msg.strip()})
            save_chats(chats)
            st.rerun()

        st.caption("🔄 Chats auto-refresh every few seconds.")

elif page == "profile":
    st.title("👤 Profile")
    if user_name:
        st.success(f"Logged in as: {user_name}")
    else:
        st.info("Pehle Chats page par apna naam dein.")

else:  # settings
    st.title("⚙️ Settings")
    st.info("Settings page — yahan aapki settings aayengi.")


# ================== MENU BAR HAMESHA NEECHE ==================
bottom_nav(page)

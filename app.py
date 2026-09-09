import streamlit as st
import streamlit.components.v1 as components
import random
import json
import os
import time
import uuid
from html import escape as esc

st.set_page_config(
    page_title="HMF book",
    page_icon="🟢",
    layout="centered",
)

try:
    from streamlit_autorefresh import st_autorefresh
    HAS_REFRESH = True
except Exception:
    HAS_REFRESH = False


# ---------- SAFE HELPERS ----------
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


def safe_toast(msg):
    if hasattr(st, "toast"):
        st.toast(msg)
    else:
        st.info(msg)


# ---------- SHARED DATABASE (multi-user) ----------
DB_FILE = "hmf_db.json"
UPLOAD_DIR = "uploads"


def load_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
    except Exception:
        db = {}
    if "users" not in db:
        db["users"] = {}
    if "messages" not in db:
        db["messages"] = []
    if "posts" not in db:
        db["posts"] = []
    return db


def save_db(db):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=1)
        return True
    except Exception:
        return False


DB = load_db()

SEED_USERS = [
    ("demo", "demo@hmfbook.com", "1234", "Demo User"),
    ("hoor_jannat", "hoor@hmfbook.com", "1234", "Hoor Jannat"),
    ("farrukh_m", "farrukh@hmfbook.com", "1234", "Farrukh M"),
    ("zara_x", "zara@hmfbook.com", "1234", "Zara X"),
]

changed = False
for uname, mail, pw, name in SEED_USERS:
    if uname not in DB["users"]:
        DB["users"][uname] = {
            "email": mail,
            "password": pw,
            "display_name": name,
            "bio": "Living life one post at a time.",
            "coins": 550,
            "followers": 1240,
            "following": 356,
            "blocked": [],
        }
        changed = True

if not DB["posts"]:
    DB["posts"] = [
        {
            "id": "s1",
            "user": "hoor_jannat",
            "type": "youtube",
            "ref": "aqz-KE-bpKQ",
            "cap": "Big Buck Bunny - my favorite animation!",
            "likes": {},
            "comments": [],
        },
        {
            "id": "s2",
            "user": "farrukh_m",
            "type": "text",
            "grad": "linear-gradient(45deg,#d1fae5,#a7f3d0)",
            "txt": "🎲 Ludo Night Tournament",
            "cap": "Tonight 8 PM - winner takes all coins!",
            "likes": {},
            "comments": [],
        },
        {
            "id": "s3",
            "user": "zara_x",
            "type": "youtube",
            "ref": "eRsGyueVLvQ",
            "cap": "Sintel - a beautiful short film!",
            "likes": {},
            "comments": [],
        },
        {
            "id": "s4",
            "user": "demo",
            "type": "text",
            "grad": "linear-gradient(45deg,#ecfdf5,#6ee7b7)",
            "txt": "🌿 Green Vibes Only",
            "cap": "Loving this new HMF book app!",
            "likes": {},
            "comments": [],
        },
    ]
    changed = True

REEL_URLS = [
    ("https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
     "Fun times!"),
    ("https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
     "Fire content!"),
    ("https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
     "Bunny life"),
    ("https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
     "Dream big"),
]

seed_members = ["demo", "hoor_jannat", "farrukh_m", "zara_x"]
for i, (url, cap) in enumerate(REEL_URLS):
    rid = "reel_seed" + str(i)
    exists = False
    for p in DB["posts"]:
        if p.get("id") == rid:
            exists = True
            break
    if not exists:
        DB["posts"].append({
            "id": rid,
            "user": seed_members[i % len(seed_members)],
            "type": "reel",
            "ref": url,
            "cap": cap,
            "likes": {},
            "comments": [],
        })
        changed = True

if changed:
    save_db(DB)


# ---------- SESSION STATE ----------
SS = st.session_state

defaults = {
    "page": "splash",
    "logged_in": False,
    "username": "",
    "email": "",
    "auth_mode": "login",
    "current_tab": "Home",
    "settings_page": "menu",
    "privacy_step": 0,
    "blocked": [],
    "clear_cmt": "",
    "clear_msg": "",
    "block_msg": "",
    "report_msg": "",
    "help_msg": "",
    "withdraw_msg": "",
    "social_msg": "",
    "data_msg": "",
    "pin_msg": "",
    "app_lock": False,
    "app_pin": "",
    "pin_unlocked": True,
    "pin_attempts": 0,
    "pin_lock_until": 0,
    "auto_logout": 0,
    "last_active": 0,
    "dark_mode": False,
    "language": "English",
    "region": "Worldwide",
    "feed_sort": "Most Recent",
    "show_stories": True,
    "comment_filter": True,
    "private_account": False,
    "activity_status": True,
    "searchable": True,
    "hide_last_seen": False,
    "profile_lock": False,
    "friend_requests": "Everyone",
    "messages_privacy": "Friends",
    "story_privacy": "Friends",
    "tagging_privacy": "Friends",
    "ad_personalization": False,
    "strong_password": False,
    "two_factor": False,
    "two_fa_code": "",
    "login_alerts": True,
    "post_visibility": "Friends",
    "reports": [],
    "security_log": [],
    "login_history": [],
    "tx_history": [],
    "room_code": "",
    "joined": False,
    "dice": 0,
    "notif": {
        "likes": True,
        "comments": True,
        "follows": True,
        "messages": True,
    },
}

for k, v in defaults.items():
    if k not in SS:
        SS[k] = v


# ---------- SECURITY HELPERS ----------
BAD_WORDS = ["stupid", "idiot", "hate", "dumb", "ugly"]


def comment_is_clean(text):
    low = text.lower()
    for w in BAD_WORDS:
        if w in low:
            return False
    return True


def password_strength(pw):
    score = 0
    if len(pw) >= 8:
        score = score + 25
    if any(c.isdigit() for c in pw):
        score = score + 25
    if any(c.isupper() for c in pw) and any(c.islower() for c in pw):
        score = score + 25
    symbols = "!@#$%^&*()-_=+[]{};:,.<>?/"
    if any(c in symbols for c in pw):
        score = score + 25
    return score


def add_security_event(text):
    entry = {"event": text, "time": "Just now"}
    SS.security_log.insert(0, entry)
    if len(SS.security_log) > 20:
        SS.security_log = SS.security_log[:20]


def security_score():
    score = 0
    tips = []
    if SS.two_factor:
        score = score + 20
    else:
        tips.append("Enable Two-Factor Authentication (+20)")
    if SS.login_alerts:
        score = score + 15
    else:
        tips.append("Enable Login Alerts (+15)")
    if SS.app_lock:
        score = score + 20
    else:
        tips.append("Set up App Lock PIN (+20)")
    if SS.strong_password:
        score = score + 20
    else:
        tips.append("Use a stronger password (+20)")
    if SS.auto_logout > 0:
        score = score + 10
    else:
        tips.append("Enable Auto Logout (+10)")
    if SS.private_account:
        score = score + 10
    else:
        tips.append("Make your account private (+10)")
    if SS.comment_filter:
        score = score + 5
    else:
        tips.append("Turn on Comment Filter (+5)")
    return score, tips


def settings_back(key):
    if st.button("← Back to Settings", key=key):
        SS.settings_page = "menu"
        SS.privacy_step = 0
        safe_rerun()


# ---------- CSS ----------
def build_main_css(dark):
    if dark:
        APPBG = "#0f1110"
        CARDBG = "#1b1e1b"
        BORDERC = "#2a2e2a"
        TXT1 = "#eef1ee"
        TXT2 = "#9aa69a"
        LOGOC = "#00e08a"
    else:
        APPBG = "#f0f2f5"
        CARDBG = "#ffffff"
        BORDERC = "#e5e7eb"
        TXT1 = "#1f2937"
        TXT2 = "#4b5563"
        LOGOC = "#00B074"

    css = f"""
    <style>
    .stApp {{ background-color:{APPBG} !important; }}
    header[data-testid="stHeader"], #MainMenu, footer {{
        visibility:hidden !important; }}
    [data-testid="stToolbar"] {{ visibility:hidden !important; }}
    [data-testid="stStatusWidget"] {{ visibility:hidden !important; }}

    .block-container, [data-testid="block-container"] {{
        max-width:460px; margin:0 auto; background:{CARDBG};
        padding-top:0 !important; padding-bottom:30px !important;
        min-height:100vh; box-shadow:0 0 25px rgba(0,0,0,.12);
    }}

    .insta-header {{
        position:sticky; top:0; z-index:100; display:flex;
        justify-content:space-between; align-items:center;
        padding:14px 18px; background:{CARDBG};
        border-bottom:1px solid {BORDERC};
    }}
    .brand-logo {{
        font-size:28px; font-weight:900; color:{LOGOC};
        letter-spacing:-1px;
    }}
    .nico {{ font-size:20px; }}

    .stories-container {{
        display:flex; gap:15px; padding:12px 15px;
        background:{CARDBG}; border-bottom:1px solid {BORDERC};
        overflow-x:auto;
    }}
    .story-card {{
        display:flex; flex-direction:column; align-items:center;
        text-align:center; min-width:65px;
    }}
    .story-ring {{
        width:60px; height:60px; border-radius:50%; padding:2.5px;
        background:linear-gradient(135deg,#00B074 0%,#056839 100%);
        display:flex; align-items:center; justify-content:center;
    }}
    .story-img {{
        width:100%; height:100%; border-radius:50%;
        background:{CARDBG}; border:2px solid {CARDBG};
        display:flex; align-items:center; justify-content:center;
        font-weight:bold; color:{TXT2}; font-size:14px;
    }}
    .story-name {{
        font-size:11px; color:{TXT2}; margin-top:4px; max-width:65px;
        overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
    }}

    .post-card {{
        background:{CARDBG}; margin-bottom:12px;
        border-bottom:1px solid {BORDERC};
    }}
    .post-header {{
        display:flex; align-items:center; padding:12px 15px;
    }}
    .post-avatar {{
        width:36px; height:36px; border-radius:50%;
        background:#00B074; color:#fff;
        display:flex; align-items:center; justify-content:center;
        font-weight:bold; margin-right:10px; font-size:13px;
    }}
    .post-username {{
        font-size:14px; font-weight:700; color:{TXT1};
    }}
    .post-image-placeholder {{
        width:100%; height:300px; background:#f3f4f6;
        display:flex; align-items:center; justify-content:center;
        font-size:16px;
    }}
    .likes-txt {{
        padding:8px 15px 2px; font-weight:600; font-size:13px;
        color:{TXT1}; margin:0;
    }}
    .post-details {{
        padding:0 15px 10px 15px; font-size:14px;
        color:{TXT1}; margin:0;
    }}

    .panel-header {{
        padding:18px; font-size:22px; font-weight:bold;
        color:{LOGOC}; border-bottom:1px solid {BORDERC};
        text-align:center;
    }}

    .set-label {{
        font-weight:700; color:{TXT1}; margin:14px 0 4px;
    }}
    .sec-label {{
        font-size:12px; font-weight:800; letter-spacing:1px;
        color:{TXT2}; margin:18px 6px 8px;
    }}
    .privacy-card {{
        display:flex; gap:14px; align-items:center;
        background:rgba(0,176,116,0.10);
        border:1px solid #00B074; border-radius:14px;
        padding:14px 16px; margin:10px 0 4px;
    }}
    .privacy-card b {{ color:{TXT1}; font-size:15px; }}
    .privacy-card p {{ margin:2px 0 0; font-size:12px; color:{TXT2}; }}
    .member-chip {{
        display:inline-block; background:{CARDBG};
        border:1px solid {BORDERC}; border-radius:20px;
        padding:4px 12px; margin:3px; font-size:12px;
        color:{TXT2};
    }}
    .session-row {{
        display:flex; align-items:center; gap:12px;
        padding:10px 4px; border-bottom:1px solid {BORDERC};
        font-size:13px; color:{TXT1};
    }}
    .lock-screen {{
        display:flex; flex-direction:column; align-items:center;
        justify-content:center; height:60vh; text-align:center;
    }}

    .chat-me {{
        background:#00B074; color:#fff; padding:8px 14px;
        border-radius:16px 16px 4px 16px; max-width:72%;
        margin:4px 0 4px auto; font-size:14px;
        display:block; width:fit-content;
    }}
    .chat-them {{
        background:{BORDERC}; color:{TXT1}; padding:8px 14px;
        border-radius:16px 16px 16px 4px; max-width:72%;
        margin:4px auto 4px 0; font-size:14px;
        display:block; width:fit-content;
    }}
    .chat-time {{
        font-size:10px; color:{TXT2};
        display:block; text-align:right;
    }}

    div[data-testid="stButton"] > button, div.stButton > button {{
        background:#00B074 !important; color:#fff !important;
        font-weight:600 !important; border:none !important;
        border-radius:12px !important;
    }}
    div[data-testid="stButton"] > button:hover,
    div.stButton > button:hover {{
        background:#056839 !important; color:#fff !important;
    }}
    </style>
    """

    if dark:
        css += """
        <style>
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea {{
            background:#242824 !important;
            color:#fff !important;
            border-color:#3a3f3a !important;
        }}
        [data-testid="stCheckbox"] label p,
        [data-testid="stRadio"] label p {{
            color:#e5e9e5 !important;
        }}
        [data-baseweb="select"] > div {{
            background:#242824 !important;
            color:#fff !important;
        }}
        hr {{ border-color:#2a2e2a !important; }}
        </style>
        """

    return css


# ================= 1) SPLASH =================
if SS.page == "splash":

    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #00B074 0%, #056839 100%) !important;
        }
        header[data-testid="stHeader"], #MainMenu, footer {
            visibility:hidden !important;
        }
        [data-testid="stToolbar"] { visibility:hidden !important; }
        [data-testid="stStatusWidget"] { visibility:hidden !important; }
        .mid {
            display:flex; flex-direction:column; align-items:center;
            justify-content:center; height:70vh; text-align:center;
        }
        .logo {
            font-size:90px; font-weight:900; color:#fff;
            letter-spacing:4px;
            text-shadow:0 4px 14px rgba(0,0,0,.25); margin:0;
        }
        .sub {
            font-size:24px; color:rgba(255,255,255,.92);
            margin:5px 0 0; letter-spacing:2px;
        }
        div[data-testid="stButton"] > button, div.stButton > button {
            background:#fff !important; color:#00B074 !important;
            font-size:18px !important; font-weight:bold !important;
            padding:12px 45px !important;
            border-radius:30px !important; border:none !important;
            box-shadow:0 4px 15px rgba(0,0,0,.25) !important;
        }
        </style>
        <div class="mid">
            <h1 class="logo">HMF</h1>
            <p class="sub">HMF book</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        if st.button("Get Started", use_container_width=True):
            SS.page = "auth"
            safe_rerun()


# ================= 2) LOGIN / SIGNUP =================
elif SS.page == "auth":

    is_signup = SS.auth_mode == "signup"

    if is_signup:
        title = "Create Account"
        subtitle = "Sign up to continue to HMF book"
        btn_label = "Sign Up"
        switch_txt = "Already have an account? Login"
    else:
        title = "Welcome Back"
        subtitle = "Login to continue to HMF book"
        btn_label = "Login"
        switch_txt = "New here? Create an account"

    st.markdown(
        """
        <style>
        .stApp { background:#F3FAF6 !important; }
        header[data-testid="stHeader"], #MainMenu, footer {
            visibility:hidden !important;
        }
        [data-testid="stToolbar"] { visibility:hidden !important; }
        [data-testid="stStatusWidget"] { visibility:hidden !important; }
        .badge {
            background:linear-gradient(135deg,#00B074,#056839);
            display:inline-block; padding:18px 52px;
            border-radius:22px;
            box-shadow:0 6px 18px rgba(0,176,116,.35);
        }
        .badge h1 {
            color:#fff; font-size:36px; font-weight:900;
            letter-spacing:3px; margin:0;
        }
        .title {
            text-align:center; font-size:24px; font-weight:700;
            color:#222; margin:26px 0 4px;
        }
        .sub2 {
            text-align:center; color:#889; font-size:14px;
            margin:0 0 22px;
        }
        div[data-testid="stButton"] > button, div.stButton > button {
            background:#00B074 !important; color:#fff !important;
            font-weight:600 !important; border:none !important;
            border-radius:12px !important;
        }
        .or {
            text-align:center; color:#99a; font-size:13px;
            margin:20px 0 8px;
        }
        </style>
        <div style="text-align:center; margin-top:14px;">
            <div class="badge"><h1>HMF</h1></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    head = f"<h2 class='title'>{title}</h2><p class='sub2'>{subtitle}</p>"
    st.markdown(head, unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter username")

    if is_signup:
        email = st.text_input("Email", placeholder="Enter email")
    else:
        email = SS.email

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password",
    )

    if is_signup and password:
        sc = password_strength(password)
        st.progress(sc)
        if sc >= 75:
            st.caption("Strong password - excellent!")
            SS.strong_password = True
        elif sc >= 50:
            st.caption("Medium password - add symbols and capitals")
            SS.strong_password = False
        else:
            st.caption("Weak password - use 8+ chars, numbers and symbols")
            SS.strong_password = False

    if st.button(btn_label, use_container_width=True):

        u = username.strip().lower()
        db = load_db()

        if not u or not password:
            st.error("Please enter both username and password!")

        elif is_signup:
            if u in db["users"]:
                st.error("This username is already taken!")
            else:
                db["users"][u] = {
                    "email": email,
                    "password": password,
                    "display_name": u.title(),
                    "bio": "New to HMF book!",
                    "coins": 100,
                    "followers": 0,
                    "following": 0,
                    "blocked": [],
                }
                save_db(db)
                SS.logged_in = True
                SS.username = u
                SS.email = email
                SS.blocked = []
                SS.page = "app"
                SS.pin_unlocked = not SS.app_lock
                SS.last_active = time.time()
                add_security_event("Account created and login")
                safe_rerun()

        else:
            if u in db["users"] and db["users"][u]["password"] == password:
                SS.logged_in = True
                SS.username = u
                SS.email = db["users"][u].get("email", "")
                SS.blocked = db["users"][u].get("blocked", [])
                SS.page = "app"
                SS.pin_unlocked = not SS.app_lock
                SS.last_active = time.time()
                add_security_event("Login successful")
                safe_rerun()
            else:
                st.error("Invalid username or password!")

    if st.button(switch_txt):
        if is_signup:
            SS.auth_mode = "login"
        else:
            SS.auth_mode = "signup"
        safe_rerun()

    st.markdown(
        "<p class='or'>Demo accounts: demo / 1234, "
        "hoor_jannat / 1234, farrukh_m / 1234</p>",
        unsafe_allow_html=True,
    )

    g, s, f = st.columns(3)
    if g.button("Google", use_container_width=True):
        SS.social_msg = "Google sign-in will be available soon."
        safe_rerun()
    if s.button("Snapchat", use_container_width=True):
        SS.social_msg = "Snapchat login will be available soon."
        safe_rerun()
    if f.button("Facebook", use_container_width=True):
        SS.social_msg = "Facebook login will be available soon."
        safe_rerun()
    if SS.social_msg:
        st.info(SS.social_msg)


# ================= 3) PIN LOCK =================
elif SS.page == "app" and SS.logged_in and SS.app_lock and not SS.pin_unlocked:

    st.markdown(build_main_css(SS.dark_mode), unsafe_allow_html=True)

    lock_html = """
    <div class="lock-screen">
        <div style="font-size:60px;">🔐</div>
        <h2>App Locked</h2>
        <p style="color:#6b7280;">Enter your PIN to unlock HMF book</p>
    </div>
    """
    st.markdown(lock_html, unsafe_allow_html=True)

    now = time.time()

    if SS.pin_lock_until > now:
        remaining = int(SS.pin_lock_until - now) + 1
        st.error(
            "Too many wrong attempts! Locked for " +
            str(remaining) + " seconds."
        )
    else:
        pin_in = st.text_input(
            "Enter 4-digit PIN",
            type="password",
            key="pin_in",
        )
        if st.button("🔓 Unlock", use_container_width=True):
            if pin_in == SS.app_pin:
                SS.pin_unlocked = True
                SS.pin_attempts = 0
                SS.pin_msg = ""
                add_security_event("App unlocked with PIN")
                safe_rerun()
            else:
                SS.pin_attempts = SS.pin_attempts + 1
                left = 3 - SS.pin_attempts
                if left <= 0:
                    SS.pin_lock_until = time.time() + 30
                    SS.pin_attempts = 0
                    add_security_event("3 wrong PIN attempts")
                else:
                    SS.pin_msg = (
                        "Wrong PIN! " + str(left) +
                        " attempt(s) remaining."
                    )
                safe_rerun()

        if SS.pin_msg:
            st.error(SS.pin_msg)
            SS.pin_msg = ""

        if st.button("🚪 Logout instead", key="pin_logout"):
            SS.logged_in = False
            SS.page = "auth"
            SS.pin_attempts = 0
            safe_rerun()


# ================= 4) MAIN APP =================
elif SS.page == "app" and SS.logged_in:

    st.markdown(build_main_css(SS.dark_mode), unsafe_allow_html=True)

    DB = load_db()

    now = time.time()
    if SS.auto_logout > 0 and SS.last_active > 0:
        if now - SS.last_active > SS.auto_logout * 60:
            SS.logged_in = False
            SS.page = "auth"
            SS.pin_unlocked = not SS.app_lock
            SS.last_active = 0
            safe_rerun()
    SS.last_active = now

    # ---------- TOP BAR ----------
    st.markdown(
        """
        <div class="insta-header">
            <div class="brand-logo">HMF book</div>
            <div class="nico">❤️ &nbsp; ✉️ &nbsp; 🔔</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    q1, q2, q3, q4, q5 = st.columns([0.6, 0.6, 0.6, 0.6, 1.6])

    if q1.button("⚙️", key="top_set", use_container_width=True,
                 help="Open Settings"):
        SS.current_tab = "Settings"
        SS.settings_page = "menu"
        safe_rerun()

    if q2.button("🔔", key="top_bell", use_container_width=True):
        safe_toast("You have new notifications!")

    if q3.button("✉️", key="top_mail", use_container_width=True,
                 help="Messages"):
        SS.current_tab = "Messages"
        safe_rerun()

    if q4.button("🌙", key="top_dark", use_container_width=True,
                 help="Toggle Dark Mode"):
        SS.dark_mode = not SS.dark_mode
        safe_rerun()

    if SS.current_tab == "Messages":
        q5.markdown(
            "<b style='color:#00B074;'>✉️ Live Messages</b>",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

    # ================= TAB: HOME =================
    if SS.current_tab == "Home":

        h1c, h2c = st.columns(2)
        if h1c.button("🎮 Play Ludo", key="home_ludo",
                      use_container_width=True):
            SS.current_tab = "Ludo"
            safe_rerun()
        if h2c.button("🎬 Watch Reels", key="home_reels",
                      use_container_width=True):
            SS.current_tab = "Reels"
            safe_rerun()

        if SS.show_stories:
            stories_html = """
            <div class="stories-container">
                <div class="story-card">
                    <div class="story-ring" style="background:#6b7280;">
                        <div class="story-img"
                             style="background-color:#056839;color:#fff;">+
                        </div>
                    </div>
                    <div class="story-name">Your Story</div>
                </div>
                <div class="story-card">
                    <div class="story-ring">
                        <div class="story-img">HJ</div>
                    </div>
                    <div class="story-name">hoor_jannat</div>
                </div>
                <div class="story-card">
                    <div class="story-ring">
                        <div class="story-img">FM</div>
                    </div>
                    <div class="story-name">farrukh_m</div>
                </div>
                <div class="story-card">
                    <div class="story-ring">
                        <div class="story-img">ZX</div>
                    </div>
                    <div class="story-name">zara_x</div>
                </div>
                <div class="story-card">
                    <div class="story-ring">
                        <div class="story-img">D</div>
                    </div>
                    <div class="story-name">demo</div>
                </div>
            </div>
            """
            st.markdown(stories_html, unsafe_allow_html=True)

        if SS.block_msg:
            st.success(SS.block_msg)
            SS.block_msg = ""

        visible_posts = []
        for p in DB["posts"]:
            if p.get("type") == "reel":
                continue
            if p["user"] in SS.blocked:
                continue
            visible_posts.append(p)

        if SS.feed_sort == "Top Posts":
            visible_posts = sorted(
                visible_posts,
                key=lambda x: len(x.get("likes", {})),
                reverse=True,
            )

        if not visible_posts:
            st.info("Your feed is empty. Upload the first post!")

        if SS.clear_cmt:
            SS[SS.clear_cmt] = ""
            SS.clear_cmt = ""

        for p in visible_posts:

            ptype = p.get("type", "text")

            if ptype == "text":
                post_html = f"""
                <div class="post-card">
                    <div class="post-header">
                        <div class="post-avatar">
                            {p['user'][:2].upper()}
                        </div>
                        <div class="post-username">{p['user']}</div>
                    </div>
                    <div class="post-image-placeholder"
                         style="background:{p.get('grad', '#f3f4f6')};
                                color:#056839; font-weight:bold;">
                        {p.get('txt', '')}
                    </div>
                </div>
                """
                st.markdown(post_html, unsafe_allow_html=True)

            else:
                head_html = f"""
                <div class="post-card">
                    <div class="post-header">
                        <div class="post-avatar">
                            {p['user'][:2].upper()}
                        </div>
                        <div class="post-username">{p['user']}</div>
                    </div>
                </div>
                """
                st.markdown(head_html, unsafe_allow_html=True)

                if ptype == "youtube":
                    yt = (
                        '<iframe width="100%" height="230" '
                        'src="https://www.youtube.com/embed/'
                        + p["ref"] + '" title="HMF video" '
                        'frameborder="0" allow="accelerometer; '
                        'autoplay; clipboard-write; encrypted-media; '
                        'gyroscope; picture-in-picture" '
                        'allowfullscreen></iframe>'
                    )
                    components.html(yt, height=245)

                elif ptype == "image":
                    if os.path.exists(p["ref"]):
                        st.image(p["ref"], use_container_width=True)

                elif ptype == "video":
                    st.video(p["ref"])

            liked = SS.username in p.get("likes", {})

            a1, a2, a3, a4 = st.columns(4)

            like_icon = "❤️" if liked else "🤍"
            if a1.button(
                like_icon,
                key="lk_" + p["id"],
                use_container_width=True,
            ):
                db = load_db()
                for post in db["posts"]:
                    if post["id"] == p["id"]:
                        lk = post.setdefault("likes", {})
                        if SS.username in lk:
                            del lk[SS.username]
                        else:
                            lk[SS.username] = True
                        break
                save_db(db)
                safe_rerun()

            if a2.button("💬", key="cm_" + p["id"],
                         use_container_width=True):
                st.info("Type your comment in the box below.")

            if a3.button("✈️", key="sh_" + p["id"],
                         use_container_width=True):
                st.info("Post link copied!")

            if a4.button("🚫", key="bl_" + p["id"],
                         use_container_width=True):
                db = load_db()
                u = db["users"].get(SS.username, {})
                bl = u.setdefault("blocked", [])
                if p["user"] not in bl:
                    bl.append(p["user"])
                save_db(db)
                SS.blocked = list(bl)
                SS.block_msg = (
                    "@" + p["user"] + " has been blocked."
                )
                safe_rerun()

            n = len(p.get("likes", {}))

            likes_html = (
                "<p class='likes-txt'>" + str(n) + " likes</p>"
                "<p class='post-details'><b>" + p["user"] +
                "</b> " + esc(p.get("cap", "")) + "</p>"
            )
            st.markdown(likes_html, unsafe_allow_html=True)

            cmt = st.text_input(
                "comment",
                key="cmt_" + p["id"],
                placeholder="Add a comment...",
                label_visibility="collapsed",
            )

            if st.button("Post Comment", key="pc_" + p["id"]):
                if cmt.strip():
                    if SS.comment_filter and not comment_is_clean(cmt):
                        st.warning("Comment blocked by security filter!")
                    else:
                        db = load_db()
                        for post in db["posts"]:
                            if post["id"] == p["id"]:
                                post.setdefault("comments", []).append(
                                    {"user": SS.username, "text": cmt}
                                )
                                break
                        save_db(db)
                        SS.clear_cmt = "cmt_" + p["id"]
                        safe_rerun()
                else:
                    st.warning("Comment cannot be empty!")

            for c in p.get("comments", []):
                cmt_html = (
                    "<p class='post-details' style='color:#6b7280;'>"
                    "<b>" + esc(c["user"]) + "</b> " +
                    esc(c["text"]) + "</p>"
                )
                st.markdown(cmt_html, unsafe_allow_html=True)

    # ================= TAB: REELS =================
    elif SS.current_tab == "Reels":

        st.markdown(
            '<div class="panel-header">🎬 Reels</div>',
            unsafe_allow_html=True,
        )

        reels = []
        for p in DB["posts"]:
            if p.get("type") in ("reel", "video"):
                if p["user"] in SS.blocked:
                    continue
                reels.append(p)

        reels = list(reversed(reels))

        if not reels:
            st.info("No reels yet. Upload a video from Create tab!")

        for r in reels:

            head_html = f"""
            <div class="post-card">
                <div class="post-header">
                    <div class="post-avatar">
                        {r['user'][:2].upper()}
                    </div>
                    <div class="post-username">{r['user']}</div>
                </div>
            </div>
            """
            st.markdown(head_html, unsafe_allow_html=True)

            st.video(r["ref"])

            liked = SS.username in r.get("likes", {})

            ra1, ra2 = st.columns(2)

            if ra1.button(
                "❤️" if liked else "🤍",
                key="rl_" + r["id"],
                use_container_width=True,
            ):
                db = load_db()
                for post in db["posts"]:
                    if post["id"] == r["id"]:
                        lk = post.setdefault("likes", {})
                        if SS.username in lk:
                            del lk[SS.username]
                        else:
                            lk[SS.username] = True
                        break
                save_db(db)
                safe_rerun()

            if ra2.button("✈️ Share", key="rsh_" + r["id"],
                          use_container_width=True):
                st.info("Reel link copied!")

            n = len(r.get("likes", {}))
            cap_html = (
                "<p class='likes-txt'>" + str(n) + " likes</p>"
                "<p class='post-details'><b>" + r["user"] +
                "</b> " + esc(r.get("cap", "")) + "</p>"
            )
            st.markdown(cap_html, unsafe_allow_html=True)

    # ================= TAB: CREATE (UPLOAD) =================
    elif SS.current_tab == "Create":

        st.markdown(
            '<div class="panel-header">➕ Create Post</div>',
            unsafe_allow_html=True,
        )

        kind = st.radio(
            "What do you want to post?",
            ["Photo", "Video"],
            horizontal=True,
            key="create_kind",
        )

        if kind == "Photo":
            f = st.file_uploader(
                "Choose a photo",
                type=["png", "jpg", "jpeg", "webp"],
                key="up_photo",
            )
        else:
            f = st.file_uploader(
                "Choose a video (will also appear in Reels)",
                type=["mp4", "mov", "webm"],
                key="up_video",
            )

        cap = st.text_input(
            "Caption",
            key="up_cap",
            placeholder="Write a caption...",
        )

        if st.button("🚀 Publish Post", key="up_publish",
                     use_container_width=True):
            if f is None:
                st.warning("Please choose a file first!")
            else:
                try:
                    os.makedirs(UPLOAD_DIR, exist_ok=True)
                    ext = f.name.split(".")[-1].lower()
                    if ext not in (
                        "png", "jpg", "jpeg", "webp",
                        "mp4", "mov", "webm",
                    ):
                        ext = "bin"
                    fname = uuid.uuid4().hex + "." + ext
                    path = os.path.join(UPLOAD_DIR, fname)
                    with open(path, "wb") as out:
                        out.write(f.getbuffer())

                    db = load_db()
                    ptype = "image" if kind == "Photo" else "video"
                    db["posts"].insert(0, {
                        "id": uuid.uuid4().hex[:8],
                        "user": SS.username,
                        "type": ptype,
                        "ref": path,
                        "cap": cap,
                        "likes": {},
                        "comments": [],
                    })
                    save_db(db)
                    st.success("Posted successfully!")
                    SS.current_tab = "Home"
                    safe_rerun()
                except Exception as e:
                    st.error("Upload failed: " + str(e))

        st.caption(
            "Note: On free Streamlit Cloud, uploaded files may reset "
            "when the app restarts."
        )

    # ================= TAB: MESSAGES =================
    elif SS.current_tab == "Messages":

        if HAS_REFRESH:
            st_autorefresh(interval=4000, key="msg_ref")

        st.markdown(
            '<div class="panel-header">✉️ Messages</div>',
            unsafe_allow_html=True,
        )

        db = load_db()

        others = []
        for u in db["users"]:
            if u != SS.username and u not in SS.blocked:
                others.append(u)

        if not others:
            st.info("No other members to chat with yet.")
        else:

            partner = st.selectbox(
                "Chat with:",
                others,
                key="chat_sel",
            )

            me = SS.username

            convo = []
            for m in db["messages"]:
                cond1 = m["from"] == me and m["to"] == partner
                cond2 = m["from"] == partner and m["to"] == me
                if cond1 or cond2:
                    convo.append(m)

            convo.sort(key=lambda x: x["time"])

            if SS.clear_msg:
                SS[SS.clear_msg] = ""
                SS.clear_msg = ""

            chat_html = ""
            for m in convo:
                tstr = time.strftime("%H:%M", time.localtime(m["time"]))
                if m["from"] == me:
                    chat_html += (
                        "<span class='chat-me'>" + esc(m["text"]) +
                        "<span class='chat-time'>" + tstr +
                        "</span></span>"
                    )
                else:
                    chat_html += (
                        "<span class='chat-them'>" + esc(m["text"]) +
                        "<span class='chat-time'>" + tstr +
                        "</span></span>"
                    )

            if chat_html:
                st.markdown(chat_html, unsafe_allow_html=True)
            else:
                st.caption("No messages yet - say hello!")

            txt = st.text_input(
                "Message",
                key="msg_input",
                placeholder="Type a message...",
            )

            if st.button("➡️ Send", key="msg_send",
                         use_container_width=True):
                if txt.strip():
                    db = load_db()
                    db["messages"].append({
                        "from": me,
                        "to": partner,
                        "text": txt.strip(),
                        "time": time.time(),
                    })
                    save_db(db)
                    SS.clear_msg = "msg_input"
                    safe_rerun()
                else:
                    st.warning("Message cannot be empty!")

            st.caption("🔄 Chats auto-refresh every few seconds.")

    # ================= TAB: LUDO =================
    elif SS.current_tab == "Ludo":

        st.markdown(
            '<div class="panel-header">🎲 HMF Ludo Club</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="post-image-placeholder" '
            'style="height:200px; font-size:34px;">🎲 LUDO</div>',
            unsafe_allow_html=True,
        )

        if st.button("🏆 Create Private Room Code",
                     use_container_width=True):
            letters = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
            SS.room_code = "".join(random.choices(letters, k=6))
            safe_rerun()

        if SS.room_code:
            st.success(
                "Room Code: **" + SS.room_code +
                "** - share this with your friends!"
            )

        if st.button("🎲 Roll Dice", use_container_width=True):
            SS.dice = random.randint(1, 6)
            if SS.dice == 6:
                db = load_db()
                u = db["users"].get(SS.username)
                if u is not None:
                    u["coins"] = u.get("coins", 0) + 5
                    save_db(db)
                SS.tx_history.insert(0, {
                    "type": "Ludo Dice Bonus",
                    "amount": "+5 coins",
                    "time": "Just now",
                })
            safe_rerun()

        if SS.dice:
            extra = ""
            if SS.dice == 6:
                extra = " - Six! +5 coins earned"
            dice_txt = (
                "<h3 style='text-align:center; color:#00B074;'>"
                "🎯 You rolled " + str(SS.dice) + extra + "</h3>"
            )
            st.markdown(dice_txt, unsafe_allow_html=True)

        if st.button("🏠 Back to Home", key="ludo_back",
                     use_container_width=True):
            SS.current_tab = "Home"
            safe_rerun()

    # ================= TAB: PROFILE =================
    elif SS.current_tab == "Profile":

        st.markdown(
            '<div class="panel-header">👤 Profile</div>',
            unsafe_allow_html=True,
        )

        db = load_db()
        me_db = db["users"].get(SS.username, {})
        dname = me_db.get("display_name", SS.username)
        mybio = me_db.get("bio", "")
        mycoins = me_db.get("coins", 0)
        myfollowers = me_db.get("followers", 0)

        my_posts = []
        for p in db["posts"]:
            if p["user"] == SS.username:
                my_posts.append(p)

        initial = SS.username[:1].upper()

        profile_html = f"""
        <div style="text-align:center; margin:10px 0;">
            <div style="width:86px;height:86px;border-radius:50%;
                 background:linear-gradient(135deg,#00B074,#056839);
                 color:#fff;font-size:34px;font-weight:800;
                 display:flex;align-items:center;
                 justify-content:center;margin:0 auto;">
                 {initial}
            </div>
            <h3 style="margin:10px 0 2px;">{esc(dname)}</h3>
            <p style="color:#6b7280; font-size:13px; margin:0;">
                {esc(mybio)}</p>
            <p style="color:#6b7280; font-size:12px; margin:8px 0 0;">
                {len(my_posts)} Posts • {myfollowers} Followers
            </p>
        </div>
        """
        st.markdown(profile_html, unsafe_allow_html=True)

        st.success("💰 Wallet Balance: **" + str(mycoins) + " Coins**")

        if st.button("💳 Request Withdrawal", key="prof_wd",
                     use_container_width=True):
            db = load_db()
            u = db["users"].get(SS.username)
            if u is not None and u.get("coins", 0) >= 100:
                u["coins"] = u["coins"] - 100
                save_db(db)
                SS.tx_history.insert(0, {
                    "type": "Withdrawal Payout",
                    "amount": "-100 coins",
                    "time": "Just now",
                })
                SS.withdraw_msg = (
                    "Withdrawal request submitted! "
                    "Processing in 3-5 business days."
                )
            else:
                SS.withdraw_msg = (
                    "Minimum 100 coins required for withdrawal!"
                )
            safe_rerun()

        if SS.withdraw_msg:
            st.info(SS.withdraw_msg)
            SS.withdraw_msg = ""

        pr1, pr2 = st.columns(2)
        if pr1.button("⚙️ Open Settings", use_container_width=True):
            SS.current_tab = "Settings"
            SS.settings_page = "menu"
            safe_rerun()
        if pr2.button("🚪 Logout", use_container_width=True):
            SS.logged_in = False
            SS.page = "auth"
            SS.current_tab = "Home"
            safe_rerun()

    # ================= TAB: SETTINGS =================
    elif SS.current_tab == "Settings":

        if SS.settings_page == "menu":

            st.markdown(
                '<div class="panel-header">⚙️ Settings & Privacy</div>',
                unsafe_allow_html=True,
            )
            st.caption("@" + SS.username + " - HMF book")

            if st.button("🔐 Security Center   ›", key="m_security",
                         use_container_width=True):
                SS.settings_page = "security"
                safe_rerun()
            if st.button("📋 Personal Info   ›", key="m_personal",
                         use_container_width=True):
                SS.settings_page = "personal"
                safe_rerun()
            if st.button("💰 Payments & Wallet   ›", key="m_payments",
                         use_container_width=True):
                SS.settings_page = "payments"
                safe_rerun()
            if st.button("📰 News Feed   ›", key="m_feed",
                         use_container_width=True):
                SS.settings_page = "feed"
                safe_rerun()
            if st.button("🔔 Notifications   ›", key="m_notif",
                         use_container_width=True):
                SS.settings_page = "notifications"
                safe_rerun()
            if st.button("🌐 Language & Region   ›", key="m_lang",
                         use_container_width=True):
                SS.settings_page = "language"
                safe_rerun()
            if st.button("🛡️ Privacy Checkup   ›", key="m_privacy",
                         use_container_width=True):
                SS.settings_page = "privacy"
                safe_rerun()
            if st.button("👥 Privacy Settings   ›", key="m_friends",
                         use_container_width=True):
                SS.settings_page = "friends"
                safe_rerun()
            if st.button("🚫 Blocked Members   ›", key="m_blocked",
                         use_container_width=True):
                SS.settings_page = "blocked"
                safe_rerun()
            if st.button("⚠️ Report a Member   ›", key="m_reports",
                         use_container_width=True):
                SS.settings_page = "reports"
                safe_rerun()
            if st.button("❓ Help Center   ›", key="m_help",
                         use_container_width=True):
                SS.settings_page = "help"
                safe_rerun()
            if st.button("ℹ️ About   ›", key="m_about",
                         use_container_width=True):
                SS.settings_page = "about"
                safe_rerun()

            st.markdown(
                "<div style='height:12px;'></div>",
                unsafe_allow_html=True,
            )
            if st.button("🚪 Logout", key="m_logout",
                         use_container_width=True):
                SS.logged_in = False
                SS.page = "auth"
                SS.current_tab = "Home"
                safe_rerun()

        elif SS.settings_page == "security":

            settings_back("bk_security")
            st.markdown(
                '<div class="panel-header">🔐 Security Center</div>',
                unsafe_allow_html=True,
            )

            score, tips = security_score()
            st.progress(score / 100.0)
            if score >= 80:
                st.success("Security Score: " + str(score) + "/100 - Excellent!")
            elif score >= 50:
                st.warning("Security Score: " + str(score) + "/100 - Good.")
            else:
                st.error("Security Score: " + str(score) + "/100 - Weak!")

            if tips:
                st.markdown("💡 **Improve your security:**")
                for t in tips:
                    st.markdown("• " + t)

            st.markdown(
                "<p class='set-label'>🔢 App Lock (PIN)</p>",
                unsafe_allow_html=True,
            )
            if not SS.app_lock:
                pin_set = st.text_input(
                    "Choose a 4-digit PIN",
                    type="password",
                    key="pin_set",
                    max_chars=4,
                )
                if st.button("🔒 Enable App Lock", key="pin_enable",
                             use_container_width=True):
                    if len(pin_set) == 4 and pin_set.isdigit():
                        SS.app_pin = pin_set
                        SS.app_lock = True
                        add_security_event("App Lock enabled")
                        st.success("App Lock enabled!")
                    else:
                        st.warning("PIN must be exactly 4 digits!")
            else:
                st.success("App Lock is ON")
                lc1, lc2 = st.columns(2)
                if lc1.button("🔒 Lock Now", key="lock_now",
                              use_container_width=True):
                    SS.pin_unlocked = False
                    SS.pin_attempts = 0
                    safe_rerun()
                if lc2.button("❌ Disable", key="pin_disable",
                              use_container_width=True):
                    SS.app_lock = False
                    SS.app_pin = ""
                    SS.pin_unlocked = True
                    safe_rerun()

            st.markdown(
                "<p class='set-label'>🔑 Two-Factor Auth</p>",
                unsafe_allow_html=True,
            )
            tf = st.checkbox("Enable 2FA", value=SS.two_factor,
                             key="tf_chk2")
            if tf != SS.two_factor:
                SS.two_factor = tf
                if tf:
                    SS.two_fa_code = str(random.randint(100000, 999999))
                    st.success("2FA enabled! Backup code: " +
                               SS.two_fa_code)
                safe_rerun()

            SS.login_alerts = st.checkbox(
                "📩 Login Alerts",
                value=SS.login_alerts,
                key="la_chk2",
            )

            st.markdown(
                "<p class='set-label'>⏱️ Auto Logout</p>",
                unsafe_allow_html=True,
            )
            timeout_opts = [0, 5, 10, 30]
            timeout_labels = ["Off", "5 minutes", "10 minutes",
                              "30 minutes"]
            cur = 0
            if SS.auto_logout in timeout_opts:
                cur = timeout_opts.index(SS.auto_logout)
            sel = st.selectbox("Log out after:", timeout_labels,
                               index=cur, key="timeout_sel")
            SS.auto_logout = timeout_opts[timeout_labels.index(sel)]

            st.markdown(
                "<p class='set-label'>⚠️ Security Log</p>",
                unsafe_allow_html=True,
            )
            if SS.security_log:
                for ev in SS.security_log:
                    st.markdown("• " + ev["event"])
            else:
                st.caption("No security events yet.")

        elif SS.settings_page == "personal":

            settings_back("bk_personal")
            st.markdown(
                '<div class="panel-header">📋 Personal Info</div>',
                unsafe_allow_html=True,
            )

            db = load_db()
            me_db = db["users"].get(SS.username, {})

            st.text_input("Username", value=SS.username,
                          disabled=True, key="pi_user")
            st.text_input("Email",
                          value=me_db.get("email", ""),
                          key="pi_email")
            dn = st.text_input("Display Name",
                               value=me_db.get("display_name", ""),
                               key="st_dn")
            bio = st.text_input("Bio",
                                value=me_db.get("bio", ""),
                                key="st_bio")

            if st.button("💾 Save Changes", key="st_save",
                         use_container_width=True):
                db = load_db()
                u = db["users"].get(SS.username)
                if u is not None:
                    u["display_name"] = dn
                    u["bio"] = bio
                    u["email"] = me_db.get("email", "")
                    save_db(db)
                st.success("Profile saved successfully!")

        elif SS.settings_page == "payments":

            settings_back("bk_payments")
            st.markdown(
                '<div class="panel-header">💰 Payments & Wallet</div>',
                unsafe_allow_html=True,
            )

            db = load_db()
            me_db = db["users"].get(SS.username, {})
            st.success("Balance: **" + str(me_db.get("coins", 0)) +
                       " Coins**")

            if st.button("💳 Request Payout", key="pay_wd",
                         use_container_width=True):
                db = load_db()
                u = db["users"].get(SS.username)
                if u is not None and u.get("coins", 0) >= 100:
                    u["coins"] = u["coins"] - 100
                    save_db(db)
                    SS.tx_history.insert(0, {
                        "type": "Withdrawal Payout",
                        "amount": "-100 coins",
                        "time": "Just now",
                    })
                    SS.withdraw_msg = "Payout request submitted!"
                else:
                    SS.withdraw_msg = "Minimum 100 coins required!"
                safe_rerun()

            if SS.withdraw_msg:
                st.info(SS.withdraw_msg)
                SS.withdraw_msg = ""

            st.markdown("📜 **Transaction History**")
            if SS.tx_history:
                for t in SS.tx_history:
                    st.markdown("• " + t["type"] + " (" + t["amount"] + ")")
            else:
                st.caption("No transactions yet.")

        elif SS.settings_page == "feed":

            settings_back("bk_feed")
            st.markdown(
                '<div class="panel-header">📰 News Feed</div>',
                unsafe_allow_html=True,
            )
            SS.feed_sort = st.radio(
                "Sort feed by:",
                ["Most Recent", "Top Posts"],
                index=0 if SS.feed_sort == "Most Recent" else 1,
                key="feed_sort_radio",
            )
            SS.show_stories = st.checkbox(
                "Show Stories row",
                value=SS.show_stories,
                key="stories_chk",
            )
            SS.comment_filter = st.checkbox(
                "🛡️ Comment Filter",
                value=SS.comment_filter,
                key="cfilter_chk",
            )

        elif SS.settings_page == "notifications":

            settings_back("bk_notif")
            st.markdown(
                '<div class="panel-header">🔔 Notifications</div>',
                unsafe_allow_html=True,
            )
            SS.notif["likes"] = st.checkbox("❤️ Likes",
                                            value=SS.notif["likes"],
                                            key="ntf_l")
            SS.notif["comments"] = st.checkbox("💬 Comments",
                                               value=SS.notif["comments"],
                                               key="ntf_c")
            SS.notif["follows"] = st.checkbox("👥 New Followers",
                                              value=SS.notif["follows"],
                                              key="ntf_f")
            SS.notif["messages"] = st.checkbox("✉️ Messages",
                                               value=SS.notif["messages"],
                                               key="ntf_m")

        elif SS.settings_page == "language":

            settings_back("bk_lang")
            st.markdown(
                '<div class="panel-header">🌐 Language & Region</div>',
                unsafe_allow_html=True,
            )
            lang = st.radio("App Language:", ["English", "Urdu"],
                            index=0 if SS.language == "English" else 1,
                            key="lang_radio")
            SS.language = lang
            regions = ["Worldwide", "Pakistan", "United Arab Emirates",
                       "United Kingdom", "United States", "Saudi Arabia"]
            if SS.region in regions:
                r_index = regions.index(SS.region)
            else:
                r_index = 0
            SS.region = st.selectbox("Region:", regions,
                                     index=r_index, key="region_sel")

        elif SS.settings_page == "privacy":

            settings_back("bk_privacy")
            st.markdown(
                '<div class="panel-header">🛡️ Privacy Checkup</div>',
                unsafe_allow_html=True,
            )
            st.progress(min(SS.privacy_step / 4, 1.0))

            if SS.privacy_step == 0:
                st.markdown("Review your key privacy settings.")
                if st.button("🚀 Get Started", key="pc_start",
                             use_container_width=True):
                    SS.privacy_step = 1
                    safe_rerun()
            elif SS.privacy_step == 1:
                options = ["Public", "Friends", "Only Me"]
                SS.post_visibility = st.radio(
                    "Who can see your posts:",
                    options,
                    index=options.index(SS.post_visibility),
                    key="vis_radio",
                )
                if st.button("Next →", key="pc_next1",
                             use_container_width=True):
                    SS.privacy_step = 2
                    safe_rerun()
            elif SS.privacy_step == 2:
                if SS.blocked:
                    for u in SS.blocked:
                        st.markdown("🚫 **@" + u + "**")
                else:
                    st.caption("No one is blocked. Great job!")
                if st.button("Next →", key="pc_next2",
                             use_container_width=True):
                    SS.privacy_step = 3
                    safe_rerun()
            elif SS.privacy_step == 3:
                SS.searchable = st.checkbox("Allow profile search",
                                            value=SS.searchable,
                                            key="search_chk")
                SS.hide_last_seen = st.checkbox("Hide last seen",
                                                value=SS.hide_last_seen,
                                                key="hide_seen_chk")
                if st.button("Finish ✓", key="pc_finish",
                             use_container_width=True):
                    SS.privacy_step = 4
                    safe_rerun()
            else:
                st.success("Privacy Checkup complete!")
                if st.button("Done", key="pc_done",
                             use_container_width=True):
                    SS.settings_page = "menu"
                    SS.privacy_step = 0
                    safe_rerun()

        elif SS.settings_page == "friends":

            settings_back("bk_friends")
            st.markdown(
                '<div class="panel-header">👥 Privacy Settings</div>',
                unsafe_allow_html=True,
            )
            SS.private_account = st.checkbox(
                "🔒 Private Account",
                value=SS.private_account,
                key="priv_chk2",
            )
            SS.profile_lock = st.checkbox(
                "🔒 Profile Lock",
                value=SS.profile_lock,
                key="plock_chk",
            )
            SS.activity_status = st.checkbox(
                "🟢 Show online status",
                value=SS.activity_status,
                key="act_chk3",
            )
            fr_opts = ["Everyone", "Friends of friends", "No one"]
            if SS.friend_requests in fr_opts:
                fi = fr_opts.index(SS.friend_requests)
            else:
                fi = 0
            SS.friend_requests = st.radio(
                "Who can send friend requests:",
                fr_opts,
                index=fi,
                key="fr_radio",
            )

        elif SS.settings_page == "blocked":

            settings_back("bk_blocked")
            st.markdown(
                '<div class="panel-header">🚫 Blocked Members</div>',
                unsafe_allow_html=True,
            )

            if SS.block_msg:
                st.success(SS.block_msg)
                SS.block_msg = ""

            db = load_db()
            chips = ""
            for m in db["users"]:
                if m != SS.username:
                    chips += "<span class='member-chip'>👤 @" + m + "</span>"
            st.markdown(chips, unsafe_allow_html=True)

            block_input = st.text_input(
                "Username to block",
                key="block_input",
                placeholder="e.g. farrukh_m",
            )

            if st.button("🚫 Block This Member", key="block_btn",
                         use_container_width=True):
                u = block_input.strip().lower()
                if not u:
                    st.warning("Please enter an ID first!")
                elif u == SS.username:
                    st.warning("You cannot block yourself!")
                elif u in SS.blocked:
                    st.warning("Already blocked!")
                else:
                    db = load_db()
                    rec = db["users"].get(SS.username)
                    if rec is not None:
                        rec.setdefault("blocked", []).append(u)
                        save_db(db)
                    SS.blocked.append(u)
                    SS.block_msg = "@" + u + " has been blocked."
                    safe_rerun()

            if SS.blocked:
                for i, u in enumerate(SS.blocked):
                    bc1, bc2 = st.columns([0.65, 0.35])
                    bc1.markdown("**🚫 @" + u + "**")
                    if bc2.button("✅ Unblock", key="ub_" + str(i),
                                  use_container_width=True):
                        db = load_db()
                        rec = db["users"].get(SS.username)
                        if rec is not None and u in rec.get("blocked", []):
                            rec["blocked"].remove(u)
                            save_db(db)
                        SS.blocked.remove(u)
                        SS.block_msg = "@" + u + " unblocked."
                        safe_rerun()
            else:
                st.caption("No members blocked yet.")

        elif SS.settings_page == "reports":

            settings_back("bk_reports")
            st.markdown(
                '<div class="panel-header">⚠️ Report a Member</div>',
                unsafe_allow_html=True,
            )
            if SS.report_msg:
                st.success(SS.report_msg)
                SS.report_msg = ""

            rep_id = st.text_input("Member ID", key="rep_id",
                                   placeholder="e.g. bilal_plays")
            reasons = [
                "Harassment / Bullying",
                "Abusive Language",
                "Spam or Fake Posts",
                "Fake Account",
                "Scam / Fraud",
                "Other",
            ]
            reason = st.selectbox("Reason", reasons, key="rep_reason")
            rep_detail = st.text_area("Details (optional)",
                                      key="rep_detail", height=80)

            if st.button("🚩 Submit Report", key="rep_btn",
                         use_container_width=True):
                r = rep_id.strip().lower()
                if r:
                    SS.reports.append({
                        "user": r,
                        "reason": reason,
                        "detail": rep_detail,
                    })
                    SS.report_msg = "Report submitted - reviewed in 24h."
                    safe_rerun()
                else:
                    st.warning("Please enter a member ID!")

        elif SS.settings_page == "help":

            settings_back("bk_help")
            st.markdown(
                '<div class="panel-header">❓ Help Center</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                "• **Earn coins** - play Ludo and roll a six\n"
                "• **Messages** - open Messages tab and chat live\n"
                "• **Upload posts** - Create tab, photo or video\n"
                "• **Someone bothering you?** - Settings, Blocked Members"
            )

            bug = st.text_area("Describe your issue:",
                               key="bug_txt", height=80)
            if st.button("✉️ Send to Support", key="sup_btn",
                         use_container_width=True):
                if bug.strip():
                    SS.help_msg = "Message sent to support team!"
                else:
                    SS.help_msg = "Please describe your issue first."
                safe_rerun()
            if SS.help_msg:
                st.info(SS.help_msg)
                SS.help_msg = ""

        elif SS.settings_page == "about":

            settings_back("bk_about")
            st.markdown(
                '<div class="panel-header">ℹ️ About</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                "**HMF book** v3.0.0\n\n"
                "Social feed • Reels • Live Messages • "
                "Uploads • Games • Coins\n\n"
                "© 2025 HMF - All rights reserved."
            )

    # ---------- BOTTOM NAV ----------
    st.markdown(
        "<hr style='border:none; border-top:1px solid #e5e7eb; "
        "margin:25px 0 10px;'>",
        unsafe_allow_html=True,
    )

    n1, n2, n3, n4, n5, n6 = st.columns(6)

    if n1.button("🏠", key="nav_home", use_container_width=True):
        SS.current_tab = "Home"
        safe_rerun()
    if n2.button("🎬", key="nav_reels", use_container_width=True):
        SS.current_tab = "Reels"
        safe_rerun()
    if n3.button("➕", key="nav_create", use_container_width=True):
        SS.current_tab = "Create"
        safe_rerun()
    if n4.button("✉️", key="nav_msg", use_container_width=True):
        SS.current_tab = "Messages"
        safe_rerun()
    if n5.button("👤", key="nav_profile", use_container_width=True):
        SS.current_tab = "Profile"
        safe_rerun()
    if n6.button("⚙️", key="nav_settings", use_container_width=True):
        SS.current_tab = "Settings"
        SS.settings_page = "menu"
        safe_rerun()


# ---------- SAFETY ----------
else:
    SS.page = "splash"
    safe_rerun()
    

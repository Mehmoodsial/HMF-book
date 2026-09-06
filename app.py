import streamlit as st
import streamlit.components.v1 as components
import random
import json
import os
import time
import uuid
import base64
from html import escape as esc

st.set_page_config(page_title="HMF book", page_icon="🟢",
                   layout="centered")

try:
    from streamlit_autorefresh import st_autorefresh
    HAS_REFRESH = True
except Exception:
    HAS_REFRESH = False

try:
    from streamlit_js_eval import js_eval
    HAS_JS = True
except Exception:
    HAS_JS = False

CHANNEL_NAME = "Color Pop Cartoons"
CHANNEL_HANDLE = "@ColorPopCartoons83"
CHANNEL_URL = "https://www.youtube.com/" + CHANNEL_HANDLE
CHANNEL_ID = ""
UPLOADS_PL = ""
if CHANNEL_ID.startswith("UC") and len(CHANNEL_ID) > 5:
    UPLOADS_PL = "UU" + CHANNEL_ID[2:]


def parse_youtube_id(url):
    url = url.strip()
    if not url:
        return None
    if len(url) == 11 and "/" not in url:
        return url
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0].split("/")[0] or None
    if "v=" in url:
        return url.split("v=")[1].split("&")[0] or None
    if "/shorts/" in url:
        return url.split("/shorts/")[1].split("?")[0].split("/")[0] or None
    if "/embed/" in url:
        return url.split("/embed/")[1].split("?")[0].split("/")[0] or None
    return None


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


# ---------- DATABASE ----------
DB_FILE = "hmf_db.json"
UPLOAD_DIR = "uploads"


def load_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
    except Exception:
        db = {}
    for key in ("users", "messages", "posts", "groups",
                "notifications", "reports"):
        if key not in db:
            db[key] = []
    if "follows" not in db:
        db["follows"] = {}
    return db


def save_db(db):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=1)
        return True
    except Exception:
        return False


def add_notification(to_user, text):
    if not to_user:
        return
    db = load_db()
    db["notifications"].insert(0, {
        "to": to_user, "text": text,
        "time": time.time(), "read": False})
    db["notifications"] = db["notifications"][:200]
    save_db(db)


def unread_count(user):
    db = load_db()
    n = 0
    for x in db["notifications"]:
        if x.get("to") == user and not x.get("read"):
            n = n + 1
    return n


def save_upload(file_obj):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = file_obj.name.split(".")[-1].lower()
    if ext not in ("png", "jpg", "jpeg", "webp", "mp4", "mov", "webm"):
        ext = "bin"
    fname = uuid.uuid4().hex + "." + ext
    path = os.path.join(UPLOAD_DIR, fname)
    with open(path, "wb") as out:
        out.write(file_obj.getbuffer())
    return path


def avatar_html(username, avatar_path=None, size=36):
    if avatar_path and os.path.exists(avatar_path):
        try:
            data = base64.b64encode(open(avatar_path, "rb").read())
            b64 = data.decode()
            return ("<img src='data:image/*;base64," + b64 + "' "
                    "style='width:" + str(size) + "px;height:" +
                    str(size) + "px;border-radius:50%;"
                    "object-fit:cover;margin-right:10px;'>")
        except Exception:
            pass
    ini = username[:2].upper()
    return ("<div style='width:" + str(size) + "px;height:" +
            str(size) + "px;border-radius:50%;background:"
            "linear-gradient(135deg,#00B074,#056839);color:#fff;"
            "display:flex;align-items:center;justify-content:center;"
            "font-weight:bold;margin-right:10px;font-size:" +
            str(int(size * 0.38)) + "px;'>" + ini + "</div>")


# ---------- JS HELPERS (screenshot + base url) ----------
def shot_install():
    if not HAS_JS:
        return
    code = ("(()=>{const w=window.parent;if(!w.hmfListenSet){"
            "w.hmfListenSet=1;"
            "w.addEventListener('keyup',function(e){"
            "if(e.key==='PrintScreen'){w.hmfShotPending='print';}});"
            "w.addEventListener('copy',function(){"
            "w.hmfShotPending='copy';});}"
            "return 1;})()")
    try:
        js_eval(code, key="shot_listen")
    except Exception:
        pass


def shot_check():
    if not HAS_JS:
        return None
    code = ("(()=>{const w=window.parent;const v=w.hmfShotPending;"
            "w.hmfShotPending=null;return v;})()")
    try:
        return js_eval(code)
    except Exception:
        return None


def get_base_url():
    if not HAS_JS:
        return None
    try:
        return js_eval(
            "window.parent.location.origin + "
            "window.parent.location.pathname",
            key="base_url",
        )
    except Exception:
        return None


def clear_profile_param():
    try:
        qp = dict(st.query_params)
        if "profile" in qp:
            st.query_params.pop("profile")
    except Exception:
        try:
            st.experimental_set_query_params()
        except Exception:
            pass


# ---------- SEED ----------
DB = load_db()

SEED_USERS = [
    ("demo", "demo@hmfbook.com", "1234", "Demo User", 550, 1240),
    ("hoor_jannat", "hoor@hmfbook.com", "1234", "Hoor Jannat", 550, 1240),
    ("farrukh_m", "farrukh@hmfbook.com", "1234", "Farrukh M", 550, 800),
    ("zara_x", "zara@hmfbook.com", "1234", "Zara X", 550, 900),
    ("admin", "admin@hmfbook.com", "admin123", "HMF Admin", 0, 0),
]

changed = False
for uname, mail, pw, name, coins, foll in SEED_USERS:
    if uname not in DB["users"]:
        DB["users"][uname] = {
            "email": mail, "password": pw, "display_name": name,
            "bio": "Living life one post at a time.",
            "coins": coins, "followers": foll, "following": 120,
            "blocked": [], "avatar": None,
        }
        changed = True

if not DB["posts"]:
    DB["posts"] = [
        {"id": "s1", "user": "hoor_jannat", "type": "youtube",
         "ref": "aqz-KE-bpKQ", "cap": "Big Buck Bunny!",
         "likes": {}, "comments": [], "avatar": None},
        {"id": "s2", "user": "farrukh_m", "type": "text",
         "grad": "linear-gradient(45deg,#d1fae5,#a7f3d0)",
         "txt": "🎲 Ludo Night Tournament",
         "cap": "Tonight 8 PM - winner takes all coins!",
         "likes": {}, "comments": [], "avatar": None},
        {"id": "s4", "user": "demo", "type": "text",
         "grad": "linear-gradient(45deg,#ecfdf5,#6ee7b7)",
         "txt": "🌿 Green Vibes Only",
         "cap": "Loving this new HMF book app!",
         "likes": {}, "comments": [], "avatar": None},
    ]
    changed = True

REELS = [
    ("https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4", "Fun times!"),
    ("https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4", "Fire content!"),
]
for i, (url, cap) in enumerate(REELS):
    rid = "reel_seed" + str(i)
    if not any(p.get("id") == rid for p in DB["posts"]):
        DB["posts"].append({
            "id": rid, "user": ["demo", "hoor_jannat"][i % 2],
            "type": "reel", "ref": url, "cap": cap,
            "likes": {}, "comments": [], "avatar": None})
        changed = True

if changed:
    save_db(DB)


# ---------- SESSION STATE ----------
SS = st.session_state

defaults = {
    "page": "splash", "logged_in": False, "username": "", "email": "",
    "auth_mode": "login", "current_tab": "Home", "settings_page": "menu",
    "privacy_step": 0, "blocked": [], "clear_cmt": "", "clear_msg": "",
    "block_msg": "", "report_msg": "", "help_msg": "", "withdraw_msg": "",
    "social_msg": "", "pin_msg": "", "yt_msg": "", "view_user": None,
    "chat_partner": None, "chat_mode": "Direct", "last_shot_time": 0,
    "app_lock": False, "app_pin": "", "pin_unlocked": True,
    "pin_attempts": 0, "pin_lock_until": 0, "auto_logout": 0,
    "last_active": 0, "dark_mode": False, "language": "English",
    "region": "Worldwide", "feed_sort": "Most Recent",
    "show_stories": True, "comment_filter": True,
    "private_account": False, "activity_status": True,
    "searchable": True, "hide_last_seen": False, "profile_lock": False,
    "friend_requests": "Everyone", "strong_password": False,
    "two_factor": False, "two_fa_code": "", "login_alerts": True,
    "post_visibility": "Friends", "security_log": [], "tx_history": [],
    "room_code": "", "dice": 0,
    "notif": {"likes": True, "comments": True, "follows": True,
              "messages": True},
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
        score += 25
    if any(c.isdigit() for c in pw):
        score += 25
    if any(c.isupper() for c in pw) and any(c.islower() for c in pw):
        score += 25
    symbols = "!@#$%^&*()-_=+[]{};:,.<>?/"
    if any(c in symbols for c in pw):
        score += 25
    return score


def add_security_event(text):
    SS.security_log.insert(0, {"event": text, "time": "Just now"})
    SS.security_log = SS.security_log[:20]


def security_score():
    score = 0
    tips = []
    checks = [
        ("two_factor", 20, "Enable Two-Factor Authentication (+20)"),
        ("login_alerts", 15, "Enable Login Alerts (+15)"),
        ("app_lock", 20, "Set up App Lock PIN (+20)"),
        ("strong_password", 20, "Use a stronger password (+20)"),
    ]
    for key, pts, tip in checks:
        if SS[key]:
            score += pts
        else:
            tips.append(tip)
    if SS["auto_logout"] > 0:
        score += 10
    else:
        tips.append("Enable Auto Logout (+10)")
    if SS["private_account"]:
        score += 10
    else:
        tips.append("Make your account private (+10)")
    if SS["comment_filter"]:
        score += 5
    else:
        tips.append("Turn on Comment Filter (+5)")
    return score, tips


def settings_back(key):
    if st.button("← Back to Settings", key=key):
        SS.settings_page = "menu"
        SS.privacy_step = 0
        safe_rerun()


# ---------- QUERY PARAM (profile link) ----------
PROFILE_VIEW = None
try:
    qp = dict(st.query_params)
    PROFILE_VIEW = qp.get("profile")
except Exception:
    try:
        qp2 = st.experimental_get_query_params() or {}
        val = qp2.get("profile", [None])
        PROFILE_VIEW = val[0] if val else None
    except Exception:
        pass


# ---------- CSS ----------
def build_main_css(dark):
    if dark:
        T = {"APPBG": "#0f1110", "CARDBG": "#1b1e1b", "BORDERC": "#2a2e2a",
             "TXT1": "#eef1ee", "TXT2": "#9aa69a", "LOGOC": "#00e08a"}
    else:
        T = {"APPBG": "#f0f2f5", "CARDBG": "#ffffff", "BORDERC": "#e5e7eb",
             "TXT1": "#1f2937", "TXT2": "#4b5563", "LOGOC": "#00B074"}

    css = """
    <style>
    .stApp { background-color:APPBG !important; }
    header[data-testid="stHeader"], #MainMenu, footer
        { visibility:hidden !important; }
    [data-testid="stToolbar"] { visibility:hidden !important; }
    [data-testid="stStatusWidget"] { visibility:hidden !important; }
    .block-container, [data-testid="block-container"] {
        max-width:460px; margin:0 auto; background:CARDBG;
        padding-top:0 !important; padding-bottom:30px !important;
        min-height:100vh; box-shadow:0 0 25px rgba(0,0,0,.12); }
    .insta-header { position:sticky; top:0; z-index:100; display:flex;
        justify-content:space-between; align-items:center;
        padding:14px 18px; background:CARDBG;
        border-bottom:1px solid BORDERC; }
    .brand-logo { font-size:28px; font-weight:900; color:LOGOC;
        letter-spacing:-1px; }
    .nico { font-size:20px; }
    .stories-container { display:flex; gap:15px; padding:12px 15px;
        background:CARDBG; border-bottom:1px solid BORDERC;
        overflow-x:auto; }
    .story-card { display:flex; flex-direction:column;
        align-items:center; text-align:center; min-width:65px; }
    .story-ring { width:60px; height:60px; border-radius:50%;
        padding:2.5px; background:linear-gradient(135deg,
        #00B074 0%,#056839 100%); display:flex;
        align-items:center; justify-content:center; }
    .story-img { width:100%; height:100%; border-radius:50%;
        background:CARDBG; border:2px solid CARDBG; display:flex;
        align-items:center; justify-content:center; font-weight:bold;
        color:TXT2; font-size:14px; }
    .story-name { font-size:11px; color:TXT2; margin-top:4px;
        max-width:65px; overflow:hidden; text-overflow:ellipsis;
        white-space:nowrap; }
    .post-card { background:CARDBG; margin-bottom:12px;
        border-bottom:1px solid BORDERC; }
    .post-header { display:flex; align-items:center; padding:12px 15px; }
    .post-username { font-size:14px; font-weight:700; color:TXT1; }
    .post-image-placeholder { width:100%; height:300px;
        background:#f3f4f6; display:flex; align-items:center;
        justify-content:center; font-size:16px; }
    .likes-txt { padding:8px 15px 2px; font-weight:600; font-size:13px;
        color:TXT1; margin:0; }
    .post-details { padding:0 15px 10px 15px; font-size:14px;
        color:TXT1; margin:0; }
    .panel-header { padding:18px; font-size:22px; font-weight:bold;
        color:LOGOC; border-bottom:1px solid BORDERC;
        text-align:center; }
    .set-label { font-weight:700; color:TXT1; margin:14px 0 4px; }
    .channel-banner { background:linear-gradient(135deg,#00B074,#056839);
        border-radius:16px; padding:20px; text-align:center;
        margin:12px 0; }
    .channel-banner h2 { color:#fff; margin:0 0 4px; font-size:22px; }
    .channel-banner p { color:rgba(255,255,255,.9); margin:0;
        font-size:13px; }
    .chat-me { background:#00B074; color:#fff; padding:8px 14px;
        border-radius:16px 16px 4px 16px; max-width:72%;
        margin:4px 0 4px auto; font-size:14px; display:block;
        width:fit-content; }
    .chat-them { background:BORDERC; color:TXT1; padding:8px 14px;
        border-radius:16px 16px 16px 4px; max-width:72%;
        margin:4px auto 4px 0; font-size:14px; display:block;
        width:fit-content; }
    .chat-time { font-size:10px; color:TXT2; display:block;
        text-align:right; }
    .lock-screen { display:flex; flex-direction:column;
        align-items:center; justify-content:center; height:60vh;
        text-align:center; }
    .member-chip { display:inline-block; background:CARDBG;
        border:1px solid BORDERC; border-radius:20px; padding:4px 12px;
        margin:3px; font-size:12px; color:TXT2; }
    .notif-row { padding:10px 6px; border-bottom:1px solid BORDERC;
        font-size:14px; color:TXT1; }
    .badge-dot { background:#e53e3e; color:#fff; border-radius:50%;
        padding:2px 8px; font-size:11px; font-weight:bold;
        margin-left:6px; }
    div[data-testid="stButton"] > button, div.stButton > button {
        background:#00B074 !important; color:#fff !important;
        font-weight:600 !important; border:none !important;
        border-radius:12px !important; }
    div[data-testid="stButton"] > button:hover,
    div.stButton > button:hover { background:#056839 !important;
        color:#fff !important; }
    </style>
    """
    for k, v in T.items():
        css = css.replace(k, v)

    if dark:
        css += """
        <style>
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea {
            background:#242824 !important; color:#fff !important;
            border-color:#3a3f3a !important; }
        [data-testid="stCheckbox"] label p,
        [data-testid="stRadio"] label p { color:#e5e9e5 !important; }
        hr { border-color:#2a2e2a !important; }
        </style>
        """
    return css


# ================= 1) SPLASH / PUBLIC PROFILE LINK =================
if SS.page == "splash":

    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #00B074 0%, #056839 100%) !important; }
    header[data-testid="stHeader"], #MainMenu, footer { visibility:hidden !important; }
    [data-testid="stToolbar"] { visibility:hidden !important; }
    [data-testid="stStatusWidget"] { visibility:hidden !important; }
    .mid { display:flex; flex-direction:column; align-items:center; justify-content:center; height:60vh; text-align:center; }
    .logo { font-size:90px; font-weight:900; color:#fff; letter-spacing:4px; text-shadow:0 4px 14px rgba(0,0,0,.25); margin:0; }
    .sub { font-size:24px; color:rgba(255,255,255,.92); margin:5px 0 0; letter-spacing:2px; }
    div[data-testid="stButton"] > button, div.stButton > button { background:#fff !important; color:#00B074 !important; font-size:18px !important; font-weight:bold !important; padding:12px 45px !important; border-radius:30px !important; border:none !important; box-shadow:0 4px 15px rgba(0,0,0,.25) !important; }
    </style>
    """, unsafe_allow_html=True)

    db = load_db()

    if PROFILE_VIEW and PROFILE_VIEW in db["users"]:
        u = db["users"][PROFILE_VIEW]
        my_posts = [p for p in db["posts"] if p["user"] == PROFILE_VIEW]
        st.markdown(build_main_css(False), unsafe_allow_html=True)
        st.markdown('<div class="panel-header">👤 HMF Profile</div>',
                    unsafe_allow_html=True)
        st.markdown("<div style='text-align:center; margin:10px 0;'>" +
                    avatar_html(PROFILE_VIEW, u.get("avatar"), 86) +
                    "</div>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;'>" +
                    esc(u.get("display_name", PROFILE_VIEW)) +
                    "</h3><p style='text-align:center;color:#6b7280;"
                    "font-size:13px;'>" + esc(u.get("bio", "")) +
                    "</p><p style='text-align:center;color:#00B074;"
                    "font-size:12px;'>" + str(len(my_posts)) +
                    " Posts • " + str(u.get("followers", 0)) +
                    " Followers</p>", unsafe_allow_html=True)
        if st.button("Open HMF book App", use_container_width=True):
            clear_profile_param()
            if SS.logged_in:
                SS.view_user = PROFILE_VIEW
                SS.page = "app"
            else:
                SS.page = "auth"
            safe_rerun()
    else:
        st.markdown(
            "<div class='mid'><h1 class='logo'>HMF</h1>"
            "<p class='sub'>HMF book</p></div>",
            unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1.3, 1])
        with c2:
            if st.button("Get Started", use_container_width=True):
                SS.page = "auth"
                safe_rerun()


# ================= 2) LOGIN / SIGNUP =================
elif SS.page == "auth":

    is_signup = SS.auth_mode == "signup"
    if is_signup:
        title, subtitle = "Create Account", "Sign up to continue"
        btn_label = "Sign Up"
        switch_txt = "Already have an account? Login"
    else:
        title, subtitle = "Welcome Back", "Login to continue"
        btn_label = "Login"
        switch_txt = "New here? Create an account"

    st.markdown("""
    <style>
    .stApp { background:#F3FAF6 !important; }
    header[data-testid="stHeader"], #MainMenu, footer { visibility:hidden !important; }
    [data-testid="stToolbar"] { visibility:hidden !important; }
    [data-testid="stStatusWidget"] { visibility:hidden !important; }
    .badge { background:linear-gradient(135deg,#00B074,#056839); display:inline-block; padding:18px 52px; border-radius:22px; box-shadow:0 6px 18px rgba(0,176,116,.35); }
    .badge h1 { color:#fff; font-size:36px; font-weight:900; letter-spacing:3px; margin:0; }
    .title { text-align:center; font-size:24px; font-weight:700; color:#222; margin:26px 0 4px; }
    .sub2 { text-align:center; color:#889; font-size:14px; margin:0 0 22px; }
    div[data-testid="stButton"] > button, div.stButton > button { background:#00B074 !important; color:#fff !important; font-weight:600 !important; border:none !important; border-radius:12px !important; }
    </style>
    <div style="text-align:center; margin-top:14px;"><div class="badge"><h1>HMF</h1></div></div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 class='title'>" + title + "</h2>"
                "<p class='sub2'>" + subtitle + "</p>",
                unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter username")
    if is_signup:
        email = st.text_input("Email", placeholder="Enter email")
    else:
        email = SS.email
    password = st.text_input("Password", type="password",
                             placeholder="Enter password")

    if is_signup and password:
        sc = password_strength(password)
        st.progress(sc)
        if sc >= 75:
            st.caption("Strong password - excellent!")
            SS.strong_password = True
        else:
            st.caption("Weak password - use 8+ chars, numbers, symbols")
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
                    "email": email, "password": password,
                    "display_name": u.title(), "bio": "New to HMF book!",
                    "coins": 100, "followers": 0, "following": 0,
                    "blocked": [], "avatar": None}
                save_db(db)
                SS.logged_in = True
                SS.username = u
                SS.email = email
                SS.blocked = []
                SS.page = "app"
                SS.last_active = time.time()
                add_security_event("Account created")
                safe_rerun()
        else:
            if (u in db["users"] and
                    db["users"][u]["password"] == password):
                SS.logged_in = True
                SS.username = u
                SS.email = db["users"][u].get("email", "")
                SS.blocked = db["users"][u].get("blocked", [])
                SS.page = "app"
                SS.last_active = time.time()
                add_security_event("Login successful")
                safe_rerun()
            else:
                st.error("Invalid username or password!")

    if st.button(switch_txt):
        SS.auth_mode = "login" if is_signup else "signup"
        safe_rerun()

    st.markdown("<p style='text-align:center; color:#99a; font-size:13px;'>"
                "Demo: demo / 1234 • Admin: admin / admin123</p>",
                unsafe_allow_html=True)

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
elif (SS.page == "app" and SS.logged_in and SS.app_lock
      and not SS.pin_unlocked):

    st.markdown(build_main_css(SS.dark_mode), unsafe_allow_html=True)
    st.markdown("""
    <div class="lock-screen">
        <div style="font-size:60px;">🔐</div>
        <h2>App Locked</h2>
        <p style="color:#6b7280;">Enter your PIN to unlock</p>
    </div>
    """, unsafe_allow_html=True)

    now = time.time()
    if SS.pin_lock_until > now:
        rem = int(SS.pin_lock_until - now) + 1
        st.error("Locked for " + str(rem) + " seconds.")
    else:
        pin_in = st.text_input("Enter 4-digit PIN", type="password",
                               key="pin_in")
        if st.button("🔓 Unlock", use_container_width=True):
            if pin_in == SS.app_pin:
                SS.pin_unlocked = True
                SS.pin_attempts = 0
                safe_rerun()
            else:
                SS.pin_attempts += 1
                left = 3 - SS.pin_attempts
                if left <= 0:
                    SS.pin_lock_until = time.time() + 30
                    SS.pin_attempts = 0
                else:
                    SS.pin_msg = "Wrong PIN! " + str(left) + " left."
                safe_rerun()
        if SS.pin_msg:
            st.error(SS.pin_msg)
            SS.pin_msg = ""


# ================= 4) MAIN APP =================
elif SS.page == "app" and SS.logged_in:

    st.markdown(build_main_css(SS.dark_mode), unsafe_allow_html=True)
    DB = load_db()

    # profile link redirect
    if PROFILE_VIEW and PROFILE_VIEW in DB["users"]:
        SS.view_user = PROFILE_VIEW
        clear_profile_param()

    # auto logout
    now = time.time()
    if SS.auto_logout > 0 and SS.last_active > 0:
        if now - SS.last_active > SS.auto_logout * 60:
            SS.logged_in = False
            SS.page = "auth"
            SS.last_active = 0
            safe_rerun()
    SS.last_active = now

    unread = unread_count(SS.username)

    # ---------- TOP BAR ----------
    st.markdown("""
    <div class="insta-header">
        <div class="brand-logo">HMF book</div>
        <div class="nico">❤️ &nbsp; ✉️ &nbsp; 🔔</div>
    </div>
    """, unsafe_allow_html=True)

    q1, q2, q3, q4, q5 = st.columns([0.7, 0.9, 0.6, 0.6, 1.4])
    if q1.button("⚙️", key="top_set", use_container_width=True):
        SS.current_tab = "Settings"
        SS.settings_page = "menu"
        safe_rerun()
    bell_label = "🔔"
    if unread > 0:
        bell_label = "🔔 " + str(unread)
    if q2.button(bell_label, key="top_bell", use_container_width=True):
        SS.current_tab = "Notifications"
        safe_rerun()
    if q3.button("✉️", key="top_mail", use_container_width=True):
        SS.current_tab = "Messages"
        safe_rerun()
    if q4.button("🌙", key="top_dark", use_container_width=True):
        SS.dark_mode = not SS.dark_mode
        safe_rerun()
    q5.markdown("<b style='color:#00B074;'>@" + SS.username + "</b>",
                unsafe_allow_html=True)

    # ============ VIEW OTHER USER PROFILE ============
    if SS.view_user and SS.view_user != SS.username:

        db = load_db()
        vu = SS.view_user
        if vu not in db["users"]:
            st.warning("User not found.")
            SS.view_user = None
            safe_rerun()
        else:
            u = db["users"][vu]
            my_posts = [p for p in db["posts"] if p["user"] == vu]

            st.markdown('<div class="panel-header">👤 Profile</div>',
                        unsafe_allow_html=True)
            st.markdown("<div style='text-align:center;margin:10px 0;'>"
                        + avatar_html(vu, u.get("avatar"), 86) +
                        "</div>", unsafe_allow_html=True)
            st.markdown(
                "<h3 style='text-align:center;'>" +
                esc(u.get("display_name", vu)) +
                "</h3><p style='text-align:center;color:#6b7280;"
                "font-size:13px;'>" + esc(u.get("bio", "")) +
                "</p><p style='text-align:center;color:#00B074;"
                "font-size:12px;'>" + str(len(my_posts)) +
                " Posts • " + str(u.get("followers", 0)) +
                " Followers</p>", unsafe_allow_html=True)
            st.caption("👁️ View only - nobody can open your account "
                       "without your password.")

            # profile link
            base = get_base_url()
            if base:
                link = base + "?profile=" + vu
                st.caption("🔗 Share this profile link:")
                st.code(link)

            follows = db["follows"].get(SS.username, [])
            is_following = vu in follows

            v1, v2 = st.columns(2)
            if v1.button("❤️ Following" if is_following else "➕ Follow",
                         key="vw_follow", use_container_width=True):
                db = load_db()
                fl = db["follows"].setdefault(SS.username, [])
                if vu in fl:
                    fl.remove(vu)
                    db["users"][vu]["followers"] = max(
                        0, db["users"][vu].get("followers", 0) - 1)
                else:
                    fl.append(vu)
                    db["users"][vu]["followers"] = (
                        db["users"][vu].get("followers", 0) + 1)
                    add_notification(vu, "👥 @" + SS.username +
                                     " started following you!")
                save_db(db)
                safe_rerun()
            if v2.button("✉️ Message", key="vw_msg",
                         use_container_width=True):
                SS.chat_partner = vu
                SS.chat_mode = "Direct"
                SS.current_tab = "Messages"
                SS.view_user = None
                safe_rerun()

            v3, v4 = st.columns(2)
            if v3.button("🚫 Block", key="vw_block",
                         use_container_width=True):
                db = load_db()
                rec = db["users"].get(SS.username)
                if rec is not None and vu not in rec.get("blocked", []):
                    rec["blocked"].append(vu)
                    save_db(db)
                    SS.blocked = list(rec["blocked"])
                SS.view_user = None
                st.success("@" + vu + " blocked.")
                safe_rerun()
            if v4.button("🚩 Report", key="vw_report",
                         use_container_width=True):
                db = load_db()
                db["reports"].append({
                    "from": SS.username, "user": vu,
                    "reason": "From profile view", "time": time.time()})
                save_db(db)
                add_notification("admin", "🚩 New report against @" + vu +
                                 " by @" + SS.username)
                st.success("Report sent to admin!")

            st.markdown("**Posts:**")
            for p in my_posts[:6]:
                if p.get("type") == "text":
                    st.markdown("<div class='post-image-placeholder' "
                                "style='background:" +
                                p.get("grad", "#f3f4f6") +
                                ";color:#056839;font-weight:bold;"
                                "height:120px;'>" + p.get("txt", "") +
                                "</div>", unsafe_allow_html=True)
                elif p.get("type") == "youtube":
                    yt = ('<iframe width="100%" height="180" '
                          'src="https://www.youtube.com/embed/' +
                          p["ref"] + '" frameborder="0" allowfullscreen>'
                          '</iframe>')
                    components.html(yt, height=190)

            if st.button("← Back", key="vw_back",
                         use_container_width=True):
                SS.view_user = None
                safe_rerun()

    else:
        if SS.view_user == SS.username:
            SS.view_user = None
            SS.current_tab = "Profile"

        # ================= TAB: HOME =================
        if SS.current_tab == "Home":

            h1c, h2c, h3c = st.columns(3)
            if h1c.button("📺 Channel", key="home_channel",
                          use_container_width=True):
                SS.current_tab = "Channel"
                safe_rerun()
            if h2c.button("🎬 Reels", key="home_reels",
                          use_container_width=True):
                SS.current_tab = "Reels"
                safe_rerun()
            if h3c.button("🎲 Ludo", key="home_ludo",
                          use_container_width=True):
                SS.current_tab = "Ludo"
                safe_rerun()

            if SS.show_stories:
                st.markdown("""
                <div class="stories-container">
                    <div class="story-card"><div class="story-ring" style="background:#6b7280;"><div class="story-img">+</div></div><div class="story-name">Your Story</div></div>
                    <div class="story-card"><div class="story-ring"><div class="story-img">HJ</div></div><div class="story-name">hoor_jannat</div></div>
                    <div class="story-card"><div class="story-ring"><div class="story-img">FM</div></div><div class="story-name">farrukh_m</div></div>
                    <div class="story-card"><div class="story-ring"><div class="story-img">D</div></div><div class="story-name">demo</div></div>
                </div>
                """, unsafe_allow_html=True)

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
                    reverse=True)

            if not visible_posts:
                st.info("Feed is empty. Create the first post!")

            if SS.clear_cmt:
                SS[SS.clear_cmt] = ""
                SS.clear_cmt = ""

            for p in visible_posts:

                ptype = p.get("type", "text")
                st.markdown("<div class='post-card'>"
                            "<div class='post-header'>" +
                            avatar_html(p["user"], p.get("avatar"), 36) +
                            "<div class='post-username'>" + p["user"] +
                            "</div></div></div>", unsafe_allow_html=True)

                if ptype == "text":
                    st.markdown("<div class='post-image-placeholder' "
                                "style='background:" +
                                p.get("grad", "#f3f4f6") +
                                ";color:#056839;font-weight:bold;'>" +
                                p.get("txt", "") + "</div>",
                                unsafe_allow_html=True)
                elif ptype == "youtube":
                    yt = ('<iframe width="100%" height="230" '
                          'src="https://www.youtube.com/embed/' + p["ref"] +
                          '" frameborder="0" allow="autoplay; '
                          'encrypted-media; picture-in-picture" '
                          'allowfullscreen></iframe>')
                    components.html(yt, height=245)
                elif ptype == "image":
                    if os.path.exists(p["ref"]):
                        st.image(p["ref"], use_container_width=True)
                elif ptype == "video":
                    st.video(p["ref"])

                liked = SS.username in p.get("likes", {})
                vu_col, a1, a2, a3, a4 = st.columns(
                    [1.6, 0.55, 0.55, 0.55, 0.55])

                if vu_col.button("👤 " + p["user"], key="vu_" + p["id"],
                                 use_container_width=True):
                    SS.view_user = p["user"]
                    safe_rerun()

                if a1.button("❤️" if liked else "🤍",
                             key="lk_" + p["id"],
                             use_container_width=True):
                    db = load_db()
                    for post in db["posts"]:
                        if post["id"] == p["id"]:
                            lk = post.setdefault("likes", {})
                            if SS.username in lk:
                                del lk[SS.username]
                            else:
                                lk[SS.username] = True
                                if post["user"] != SS.username:
                                    add_notification(
                                        post["user"], "❤️ @" +
                                        SS.username + " liked your post!")
                            break
                    save_db(db)
                    safe_rerun()

                if a2.button("💬", key="cm_" + p["id"],
                             use_container_width=True):
                    st.info("Type your comment below.")
                if a3.button("✈️", key="sh_" + p["id"],
                             use_container_width=True):
                    st.info("Post link copied!")
                if a4.button("🚫", key="bl_" + p["id"],
                             use_container_width=True):
                    db = load_db()
                    rec = db["users"].get(SS.username, {})
                    bl = rec.setdefault("blocked", [])
                    if p["user"] not in bl:
                        bl.append(p["user"])
                        save_db(db)
                        SS.blocked = list(bl)
                        SS.block_msg = "@" + p["user"] + " blocked."
                    safe_rerun()

                n = len(p.get("likes", {}))
                st.markdown("<p class='likes-txt'>" + str(n) +
                            " likes</p><p class='post-details'><b>" +
                            p["user"] + "</b> " +
                            esc(p.get("cap", "")) + "</p>",
                            unsafe_allow_html=True)

                cmt = st.text_input("comment", key="cmt_" + p["id"],
                                    placeholder="Add a comment...",
                                    label_visibility="collapsed")
                if st.button("Post Comment", key="pc_" + p["id"]):
                    if cmt.strip():
                        if SS.comment_filter and not comment_is_clean(cmt):
                            st.warning("Blocked by security filter!")
                        else:
                            db = load_db()
                            for post in db["posts"]:
                                if post["id"] == p["id"]:
                                    post.setdefault("comments", []).append(
                                        {"user": SS.username, "text": cmt})
                                    if post["user"] != SS.username:
                                        add_notification(
                                            post["user"], "💬 @" +
                                            SS.username +
                                            " commented: " + cmt[:30])
                                    break
                            save_db(db)
                            SS.clear_cmt = "cmt_" + p["id"]
                            safe_rerun()
                    else:
                        st.warning("Comment cannot be empty!")

                for c in p.get("comments", []):
                    st.markdown("<p class='post-details' "
                                "style='color:#6b7280;'><b>" +
                                esc(c["user"]) + "</b> " +
                                esc(c["text"]) + "</p>",
                                unsafe_allow_html=True)

        # ================= TAB: CHANNEL =================
        elif SS.current_tab == "Channel":

            st.markdown("<div class='channel-banner'><h2>📺 " +
                        CHANNEL_NAME + "</h2><p>" + CHANNEL_HANDLE +
                        " • Videos inside HMF book</p></div>",
                        unsafe_allow_html=True)

            if UPLOADS_PL:
                pl = ('<iframe width="100%" height="230" src='
                      '"https://www.youtube.com/embed/videoseries?list=' +
                      UPLOADS_PL + '" frameborder="0" allowfullscreen>'
                      '</iframe>')
                components.html(pl, height=245)
            else:
                st.info("💡 Channel ID paste karne se poori playlist "
                        "chalti hai (code ke upar CHANNEL_ID).")

            st.markdown("[🔗 Open channel on YouTube](" + CHANNEL_URL + ")")

            if SS.yt_msg:
                st.success(SS.yt_msg)
                SS.yt_msg = ""

            yt_link = st.text_input("Paste YouTube video link",
                                    key="ch_link")
            if st.button("➕ Add Video", key="ch_add",
                         use_container_width=True):
                vid = parse_youtube_id(yt_link)
                if vid:
                    db = load_db()
                    my_av = db["users"].get(SS.username, {}).get("avatar")
                    db["posts"].insert(0, {
                        "id": uuid.uuid4().hex[:8], "user": SS.username,
                        "type": "youtube", "ref": vid,
                        "cap": "From " + CHANNEL_NAME,
                        "likes": {}, "comments": [],
                        "avatar": my_av, "channel": True})
                    save_db(db)
                    SS.yt_msg = "Video added!"
                    safe_rerun()
                else:
                    st.error("Invalid YouTube link!")

            st.markdown("**📺 Added videos:**")
            ch_posts = [p for p in DB["posts"] if p.get("channel")]
            if not ch_posts:
                st.caption("No videos added yet.")
            for p in reversed(ch_posts):
                yt = ('<iframe width="100%" height="200" src='
                      '"https://www.youtube.com/embed/' + p["ref"] +
                      '" frameborder="0" allowfullscreen></iframe>')
                components.html(yt, height=210)

        # ================= TAB: REELS =================
        elif SS.current_tab == "Reels":

            st.markdown('<div class="panel-header">🎬 Reels</div>',
                        unsafe_allow_html=True)
            reels = [p for p in DB["posts"]
                     if p.get("type") in ("reel", "video")
                     and p["user"] not in SS.blocked]

            if not reels:
                st.info("No reels yet. Upload a video!")
            for r in reversed(reels):
                st.markdown("<div class='post-card'>"
                            "<div class='post-header'>" +
                            avatar_html(r["user"], r.get("avatar"), 36) +
                            "<div class='post-username'>" + r["user"] +
                            "</div></div></div>", unsafe_allow_html=True)
                st.video(r["ref"])
                liked = SS.username in r.get("likes", {})
                ra1, ra2 = st.columns(2)
                if ra1.button("❤️" if liked else "🤍",
                              key="rl_" + r["id"],
                              use_container_width=True):
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

        # ================= TAB: CREATE =================
        elif SS.current_tab == "Create":

            st.markdown('<div class="panel-header">➕ Create Post</div>',
                        unsafe_allow_html=True)

            kind = st.radio("What do you want to post?",
                            ["Photo", "Video", "Camera", "YouTube Link"],
                            horizontal=True, key="create_kind")

            f = None
            cam = None
            yt_link = ""

            if kind == "Photo":
                f = st.file_uploader("Choose a photo",
                                     type=["png", "jpg", "jpeg", "webp"],
                                     key="up_photo")
            elif kind == "Video":
                f = st.file_uploader("Choose a video (also in Reels)",
                                     type=["mp4", "mov", "webm"],
                                     key="up_video")
            elif kind == "Camera":
                cam = st.camera_input("📸 Take a photo", key="up_cam")
            else:
                yt_link = st.text_input("Paste YouTube link",
                                        key="up_yt")

            cap = st.text_input("Caption", key="up_cap",
                                placeholder="Write a caption...")

            if st.button("🚀 Publish", key="up_publish",
                         use_container_width=True):

                db = load_db()
                my_av = db["users"].get(SS.username, {}).get("avatar")

                if kind == "YouTube Link":
                    vid = parse_youtube_id(yt_link)
                    if not vid:
                        st.error("Invalid YouTube link!")
                    else:
                        db["posts"].insert(0, {
                            "id": uuid.uuid4().hex[:8],
                            "user": SS.username, "type": "youtube",
                            "ref": vid, "cap": cap or "YouTube video",
                            "likes": {}, "comments": [],
                            "avatar": my_av})
                        save_db(db)
                        st.success("Posted!")
                        SS.current_tab = "Home"
                        safe_rerun()
                else:
                    src = f if f is not None else cam
                    if src is None:
                        st.warning("Please choose/take a photo first!")
                    else:
                        try:
                            path = save_upload(src)
                            ptype = "video" if kind == "Video" else "image"
                            db["posts"].insert(0, {
                                "id": uuid.uuid4().hex[:8],
                                "user": SS.username, "type": ptype,
                                "ref": path, "cap": cap,
                                "likes": {}, "comments": [],
                                "avatar": my_av})
                            save_db(db)
                            st.success("Posted!")
                            SS.current_tab = "Home"
                            safe_rerun()
                        except Exception as e:
                            st.error("Upload failed: " + str(e))

            st.caption("Note: free Cloud par app restart hone par "
                       "uploads reset ho sakte hain.")

        # ================= TAB: MESSAGES =================
        elif SS.current_tab == "Messages":

            if HAS_REFRESH:
                st_autorefresh(interval=4000, key="msg_ref")

            shot_install()

            st.markdown('<div class="panel-header">✉️ Messages</div>',
                        unsafe_allow_html=True)

            m1, m2 = st.columns(2)
            if m1.button("👤 Direct", key="mode_direct",
                         use_container_width=True):
                SS.chat_mode = "Direct"
                safe_rerun()
            if m2.button("👥 Groups", key="mode_group",
                         use_container_width=True):
                SS.chat_mode = "Group"
                safe_rerun()

            if SS.chat_mode == "Direct":

                db = load_db()
                others = [u for u in db["users"]
                          if u != SS.username and u not in SS.blocked]

                if not others:
                    st.info("No members to chat with.")
                else:
                    if SS.chat_partner and SS.chat_partner in others:
                        default_idx = others.index(SS.chat_partner)
                    else:
                        default_idx = 0
                    partner = st.selectbox("Chat with:", others,
                                           index=default_idx,
                                           key="chat_sel")
                    SS.chat_partner = partner

                    convo = []
                    for m in db["messages"]:
                        if ((m["from"] == SS.username and
                             m["to"] == partner) or
                            (m["from"] == partner and
                             m["to"] == SS.username)):
                            convo.append(m)
                    convo.sort(key=lambda x: x["time"])

                    # screenshot detection
                    pending = shot_check()
                    if pending:
                        if time.time() - SS.last_shot_time > 5:
                            SS.last_shot_time = time.time()
                            add_notification(
                                partner, "📸 @" + SS.username +
                                " took a screenshot of your chat!")
                            safe_toast("📸 Screenshot detected - "
                                       "partner notified!")
                            safe_rerun()

                    if SS.clear_msg:
                        SS[SS.clear_msg] = ""
                        SS.clear_msg = ""

                    chat_html = ""
                    for m in convo:
                        tstr = time.strftime(
                            "%H:%M", time.localtime(m["time"]))
                        if m["from"] == SS.username:
                            chat_html += ("<span class='chat-me'>" +
                                          esc(m["text"]) +
                                          "<span class='chat-time'>" +
                                          tstr + "</span></span>")
                        else:
                            chat_html += ("<span class='chat-them'>" +
                                          esc(m["text"]) +
                                          "<span class='chat-time'>" +
                                          tstr + "</span></span>")
                    if chat_html:
                        st.markdown(chat_html, unsafe_allow_html=True)
                    else:
                        st.caption("No messages yet - say hello!")

                    txt = st.text_input("Message", key="msg_input",
                                        placeholder="Type a message...")
                    if st.button("➡️ Send", key="msg_send",
                                 use_container_width=True):
                        if txt.strip():
                            db = load_db()
                            db["messages"].append({
                                "from": SS.username, "to": partner,
                                "text": txt.strip(),
                                "time": time.time()})
                            save_db(db)
                            add_notification(
                                partner, "✉️ @" + SS.username +
                                " sent you a message")
                            SS.clear_msg = "msg_input"
                            safe_rerun()
                        else:
                            st.warning("Message cannot be empty!")

                    st.caption("🛡️ Screenshot & copy detect hota hai - "
                               "partner ko notification jata hai.")

            else:
                # ---------- GROUPS ----------
                db = load_db()

                with st.expander("➕ Create Group"):
                    gname = st.text_input("Group name", key="g_name")
                    others = [u for u in db["users"]
                              if u != SS.username]
                    members = st.multiselect("Add members", others,
                                             key="g_members")
                    if st.button("Create Group", key="g_create",
                                 use_container_width=True):
                        if gname.strip() and members:
                            db = load_db()
                            gid = uuid.uuid4().hex[:8]
                            db["groups"].append({
                                "id": gid, "name": gname.strip(),
                                "members": [SS.username] + members,
                                "messages": []})
                            save_db(db)
                            for m in members:
                                add_notification(
                                    m, "👥 @" + SS.username +
                                    " added you to group '" +
                                    gname.strip() + "'")
                            st.success("Group created!")
                            safe_rerun()
                        else:
                            st.warning("Name aur members select karein!")

                my_groups = [g for g in db["groups"]
                             if SS.username in g["members"]]
                if not my_groups:
                    st.info("No groups yet. Create one above!")
                else:
                    names = [g["name"] for g in my_groups]
                    gsel = st.selectbox("Your groups:", names,
                                        key="g_sel")
                    group = my_groups[names.index(gsel)]

                    st.caption("Members: " +
                               ", ".join("@" + m for m in
                                         group["members"]))

                    msgs = sorted(group["messages"],
                                  key=lambda x: x["time"])

                    pending = shot_check()
                    if pending:
                        if time.time() - SS.last_shot_time > 5:
                            SS.last_shot_time = time.time()
                            for m in group["members"]:
                                if m != SS.username:
                                    add_notification(
                                        m, "📸 @" + SS.username +
                                        " took a screenshot of group '" +
                                        group["name"] + "'!")
                            safe_toast("📸 Screenshot detected!")
                            safe_rerun()

                    if SS.clear_msg:
                        SS[SS.clear_msg] = ""
                        SS.clear_msg = ""

                    chat_html = ""
                    for m in msgs:
                        tstr = time.strftime(
                            "%H:%M", time.localtime(m["time"]))
                        who = "<b>@" + esc(m["from"]) + "</b> "
                        if m["from"] == SS.username:
                            chat_html += ("<span class='chat-me'>" + who +
                                          esc(m["text"]) +
                                          "<span class='chat-time'>" +
                                          tstr + "</span></span>")
                        else:
                            chat_html += ("<span class='chat-them'>" +
                                          who + esc(m["text"]) +
                                          "<span class='chat-time'>" +
                                          tstr + "</span></span>")
                    if chat_html:
                        st.markdown(chat_html, unsafe_allow_html=True)
                    else:
                        st.caption("No group messages yet!")

                    txt = st.text_input("Group message", key="gmsg_input",
                                        placeholder="Type a message...")
                    if st.button("➡️ Send", key="g_send",
                                 use_container_width=True):
                        if txt.strip():
                            db = load_db()
                            for g in db["groups"]:
                                if g["id"] == group["id"]:
                                    g["messages"].append({
                                        "from": SS.username,
                                        "text": txt.strip(),
                                        "time": time.time()})
                                    break
                            save_db(db)
                            for m in group["members"]:
                                if m != SS.username:
                                    add_notification(
                                        m, "👥 @" + SS.username +
                                        " in '" + group["name"] +
                                        "': " + txt.strip()[:25])
                            SS.clear_msg = "gmsg_input"
                            safe_rerun()
                        else:
                            st.warning("Message cannot be empty!")

        # ================= TAB: NOTIFICATIONS =================
        elif SS.current_tab == "Notifications":

            st.markdown('<div class="panel-header">🔔 Notifications</div>',
                        unsafe_allow_html=True)

            db = load_db()
            my_notifs = [n for n in db["notifications"]
                         if n.get("to") == SS.username][:40]

            if st.button("✅ Mark all as read", key="ntf_read",
                         use_container_width=True):
                db = load_db()
                for n in db["notifications"]:
                    if n.get("to") == SS.username:
                        n["read"] = True
                save_db(db)
                safe_rerun()

            if not my_notifs:
                st.info("No notifications yet!")
            for i, n in enumerate(my_notifs):
                tstr = time.strftime("%d %b %H:%M",
                                     time.localtime(n["time"]))
                dot = "" if n.get("read") else "<span class='badge-dot'>NEW</span>"
                st.markdown("<div class='notif-row'>" + n["text"] + dot +
                            "<br><span style='font-size:11px;"
                            "color:#9ca3af;'>" + tstr + "</span></div>",
                            unsafe_allow_html=True)

        # ================= TAB: LUDO =================
        elif SS.current_tab == "Ludo":

            st.markdown('<div class="panel-header">🎲 HMF Ludo Club</div>',
                        unsafe_allow_html=True)
            st.markdown("<div class='post-image-placeholder' "
                        "style='height:180px;font-size:34px;'>🎲 LUDO"
                        "</div>", unsafe_allow_html=True)

            if st.button("🏆 Create Room Code", use_container_width=True):
                letters = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
                SS.room_code = "".join(random.choices(letters, k=6))
                safe_rerun()
            if SS.room_code:
                st.success("Room Code: **" + SS.room_code + "**")

            if st.button("🎲 Roll Dice", use_container_width=True):
                SS.dice = random.randint(1, 6)
                if SS.dice == 6:
                    db = load_db()
                    u = db["users"].get(SS.username)
                    if u is not None:
                        u["coins"] = u.get("coins", 0) + 5
                        save_db(db)
                    SS.tx_history.insert(0, {
                        "type": "Ludo Bonus", "amount": "+5 coins",
                        "time": "Just now"})
                safe_rerun()

            if SS.dice:
                extra = " - Six! +5 coins" if SS.dice == 6 else ""
                st.markdown("<h3 style='text-align:center;color:#00B074;'>"
                            "🎯 You rolled " + str(SS.dice) + extra +
                            "</h3>", unsafe_allow_html=True)

        # ================= TAB: PROFILE =================
        elif SS.current_tab == "Profile":

            st.markdown('<div class="panel-header">👤 Profile</div>',
                        unsafe_allow_html=True)

            db = load_db()
            me_db = db["users"].get(SS.username, {})
            my_posts = [p for p in db["posts"] if p["user"] == SS.username]

            st.markdown("<div style='text-align:center;margin:10px 0;'>" +
                        avatar_html(SS.username, me_db.get("avatar"), 86) +
                        "</div>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:center;'>" +
                        esc(me_db.get("display_name", SS.username)) +
                        "</h3><p style='text-align:center;color:#6b7280;"
                        "font-size:13px;'>" +
                        esc(me_db.get("bio", "")) +
                        "</p><p style='text-align:center;color:#00B074;"
                        "font-size:12px;'>" + str(len(my_posts)) +
                        " Posts • " + str(me_db.get("followers", 0)) +
                        " Followers</p>", unsafe_allow_html=True)

            # profile link share
            base = get_base_url()
            if base:
                link = base + "?profile=" + SS.username
                st.caption("🔗 Your shareable profile link:")
                st.code(link)

            # profile pic change
            with st.expander("🖼️ Change Profile Picture"):
                pic = st.file_uploader("Upload picture",
                                       type=["png", "jpg", "jpeg",
                                             "webp"], key="avatar_up")
                campic = st.camera_input("Or take with camera",
                                         key="avatar_cam")
                if st.button("💾 Update Profile Pic", key="avatar_save",
                             use_container_width=True):
                    src = pic if pic is not None else campic
                    if src is None:
                        st.warning("Pehle photo choose karein!")
                    else:
                        try:
                            path = save_upload(src)
                            db = load_db()
                            db["users"][SS.username]["avatar"] = path
                            save_db(db)
                            st.success("Profile pic updated! Purani posts "
                                       "mein purani pic rahegi (Facebook "
                                       "style).")
                            safe_rerun()
                        except Exception as e:
                            st.error("Failed: " + str(e))

            st.success("💰 Balance: **" + str(me_db.get("coins", 0)) +
                       " Coins**")

            if st.button("💳 Request Withdrawal", key="prof_wd",
                         use_container_width=True):
                db = load_db()
                u = db["users"].get(SS.username)
                if u is not None and u.get("coins", 0) >= 100:
                    u["coins"] -= 100
                    save_db(db)
                    SS.tx_history.insert(0, {
                        "type": "Withdrawal", "amount": "-100 coins",
                        "time": "Just now"})
                    SS.withdraw_msg = "Payout submitted!"
                else:
                    SS.withdraw_msg = "Minimum 100 coins required!"
                safe_rerun()
            if SS.withdraw_msg:
                st.info(SS.withdraw_msg)
                SS.withdraw_msg = ""

            pr1, pr2 = st.columns(2)
            if pr1.button("⚙️ Settings", use_container_width=True):
                SS.current_tab = "Settings"
                SS.settings_page = "menu"
                safe_rerun()
            if pr2.button("🚪 Logout", use_container_width=True):
                SS.logged_in = False
                SS.page = "auth"
                safe_rerun()

        # ================= TAB: SETTINGS =================
        elif SS.current_tab == "Settings":

            if SS.settings_page == "menu":

                st.markdown('<div class="panel-header">⚙️ Settings</div>',
                            unsafe_allow_html=True)
                st.caption("@" + SS.username)

                if SS.username == "admin":
                    if st.button("🛡️ Admin Panel   ›", key="m_admin",
                                 use_container_width=True):
                        SS.settings_page = "admin"
                        safe_rerun()

                items = [
                    ("🔐 Security Center", "security"),
                    ("📋 Personal Info", "personal"),
                    ("💰 Payments", "payments"),
                    ("📰 News Feed", "feed"),
                    ("🔔 Notifications", "notifications"),
                    ("🌐 Language & Region", "language"),
                    ("🛡️ Privacy Checkup", "privacy"),
                    ("🚫 Blocked Members", "blocked"),
                    ("⚠️ Report a Member", "reports"),
                    ("❓ Help Center", "help"),
                    ("ℹ️ About", "about"),
                ]
                for label, page in items:
                    if st.button(label + "   ›", key="m_" + page,
                                 use_container_width=True):
                        SS.settings_page = page
                        safe_rerun()

                if st.button("🚪 Logout", key="m_logout",
                             use_container_width=True):
                    SS.logged_in = False
                    SS.page = "auth"
                    safe_rerun()

            elif SS.settings_page == "admin":

                settings_back("bk_admin")
                st.markdown('<div class="panel-header">🛡️ Admin Panel'
                            '</div>', unsafe_allow_html=True)

                db = load_db()
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Users", len(db["users"]))
                c2.metric("Posts", len(db["posts"]))
                c3.metric("Messages", len(db["messages"]))
                c4.metric("Groups", len(db["groups"]))

                st.markdown("### 🚩 Reports")
                if not db["reports"]:
                    st.caption("No reports yet.")
                for i, r in enumerate(db["reports"]):
                    st.markdown("• 🚩 **@" + r["user"] + "** by @" +
                                r["from"] + " - " + r["reason"])

                st.markdown("### 👥 Users (ban)")
                for u in db["users"]:
                    if u == "admin":
                        continue
                    b1, b2 = st.columns([0.6, 0.4])
                    b1.markdown("👤 **@" + u + "**")
                    if b2.button("Ban", key="ban_" + u,
                                 use_container_width=True):
                        db = load_db()
                        db["users"].pop(u, None)
                        db["posts"] = [p for p in db["posts"]
                                       if p["user"] != u]
                        db["messages"] = [m for m in db["messages"]
                                          if u not in (m["from"],
                                                       m["to"])]
                        save_db(db)
                        st.success("@" + u + " banned!")
                        safe_rerun()

            elif SS.settings_page == "security":
                settings_back("bk_security")
                st.markdown('<div class="panel-header">🔐 Security Center'
                            '</div>', unsafe_allow_html=True)
                score, tips = security_score()
                st.progress(score / 100.0)
                st.write("Score: **" + str(score) + "/100**")
                for t in tips:
                    st.markdown("• " + t)

                st.markdown("<p class='set-label'>🔢 App Lock</p>",
                            unsafe_allow_html=True)
                if not SS.app_lock:
                    pin_set = st.text_input("4-digit PIN", type="password",
                                            key="pin_set", max_chars=4)
                    if st.button("🔒 Enable", key="pin_enable",
                                 use_container_width=True):
                        if len(pin_set) == 4 and pin_set.isdigit():
                            SS.app_pin = pin_set
                            SS.app_lock = True
                            st.success("App Lock enabled!")
                        else:
                            st.warning("PIN must be 4 digits!")
                else:
                    st.success("App Lock is ON")
                    lc1, lc2 = st.columns(2)
                    if lc1.button("🔒 Lock Now", key="lock_now",
                                  use_container_width=True):
                        SS.pin_unlocked = False
                        safe_rerun()
                    if lc2.button("❌ Disable", key="pin_disable",
                                  use_container_width=True):
                        SS.app_lock = False
                        SS.pin_unlocked = True
                        safe_rerun()

            elif SS.settings_page == "personal":
                settings_back("bk_personal")
                st.markdown('<div class="panel-header">📋 Personal Info'
                            '</div>', unsafe_allow_html=True)
                db = load_db()
                me_db = db["users"].get(SS.username, {})
                st.text_input("Username", value=SS.username,
                              disabled=True, key="pi_user")
                dn = st.text_input("Display Name",
                                   value=me_db.get("display_name", ""),
                                   key="st_dn")
                bio = st.text_input("Bio", value=me_db.get("bio", ""),
                                    key="st_bio")
                if st.button("💾 Save", key="st_save",
                             use_container_width=True):
                    db = load_db()
                    u = db["users"].get(SS.username)
                    if u is not None:
                        u["display_name"] = dn
                        u["bio"] = bio
                        save_db(db)
                    st.success("Saved!")

            elif SS.settings_page == "payments":
                settings_back("bk_payments")
                st.markdown('<div class="panel-header">💰 Payments'
                            '</div>', unsafe_allow_html=True)
                db = load_db()
                me_db = db["users"].get(SS.username, {})
                st.success("Balance: **" + str(me_db.get("coins", 0)) +
                           " Coins**")
                if st.button("💳 Request Payout", key="pay_wd",
                             use_container_width=True):
                    db = load_db()
                    u = db["users"].get(SS.username)
                    if u is not None and u.get("coins", 0) >= 100:
                        u["coins"] -= 100
                        save_db(db)
                        SS.tx_history.insert(0, {
                            "type": "Withdrawal", "amount": "-100",
                            "time": "Now"})
                        SS.withdraw_msg = "Payout submitted!"
                    else:
                        SS.withdraw_msg = "Min 100 coins needed!"
                    safe_rerun()
                if SS.withdraw_msg:
                    st.info(SS.withdraw_msg)
                    SS.withdraw_msg = ""
                for t in SS.tx_history:
                    st.markdown("• " + t["type"] + " (" + t["amount"] + ")")

            elif SS.settings_page == "feed":
                settings_back("bk_feed")
                SS.feed_sort = st.radio(
                    "Sort by:", ["Most Recent", "Top Posts"],
                    key="feed_sort_radio")
                SS.show_stories = st.checkbox("Show Stories",
                                              value=SS.show_stories,
                                              key="stories_chk")
                SS.comment_filter = st.checkbox(
                    "🛡️ Comment Filter",
                    value=SS.comment_filter, key="cfilter_chk")

            elif SS.settings_page == "notifications":
                settings_back("bk_notif")
                SS.notif["likes"] = st.checkbox("❤️ Likes",
                                                value=SS.notif["likes"],
                                                key="ntf_l")
                SS.notif["comments"] = st.checkbox(
                    "💬 Comments", value=SS.notif["comments"],
                    key="ntf_c")
                SS.notif["follows"] = st.checkbox(
                    "👥 Followers", value=SS.notif["follows"],
                    key="ntf_f")
                SS.notif["messages"] = st.checkbox(
                    "✉️ Messages", value=SS.notif["messages"],
                    key="ntf_m")

            elif SS.settings_page == "language":
                settings_back("bk_lang")
                lang = st.radio("Language:", ["English", "Urdu"],
                                key="lang_radio")
                SS.language = lang

            elif SS.settings_page == "privacy":
                settings_back("bk_privacy")
                st.progress(min(SS.privacy_step / 4, 1.0))
                if SS.privacy_step == 0:
                    if st.button("🚀 Start Checkup", key="pc_start",
                                 use_container_width=True):
                        SS.privacy_step = 1
                        safe_rerun()
                elif SS.privacy_step == 1:
                    SS.post_visibility = st.radio(
                        "Post visibility:", ["Public", "Friends",
                                             "Only Me"], key="vis_radio")
                    if st.button("Next →", key="pc_next1",
                                 use_container_width=True):
                        SS.privacy_step = 2
                        safe_rerun()
                elif SS.privacy_step == 2:
                    SS.private_account = st.checkbox(
                        "Private Account", value=SS.private_account,
                        key="priv_chk")
                    if st.button("Next →", key="pc_next2",
                                 use_container_width=True):
                        SS.privacy_step = 3
                        safe_rerun()
                elif SS.privacy_step == 3:
                    SS.searchable = st.checkbox("Searchable",
                                                value=SS.searchable,
                                                key="srch_chk")
                    if st.button("Finish ✓", key="pc_fin",
                                 use_container_width=True):
                        SS.privacy_step = 4
                        safe_rerun()
                else:
                    st.success("Checkup complete!")
                    if st.button("Done", key="pc_done",
                                 use_container_width=True):
                        SS.settings_page = "menu"
                        SS.privacy_step = 0
                        safe_rerun()

            elif SS.settings_page == "blocked":
                settings_back("bk_blocked")
                st.markdown('<div class="panel-header">🚫 Blocked'
                            '</div>', unsafe_allow_html=True)
                if SS.block_msg:
                    st.success(SS.block_msg)
                    SS.block_msg = ""
                db = load_db()
                chips = ""
                for m in db["users"]:
                    if m != SS.username:
                        chips += ("<span class='member-chip'>@" + m +
                                  "</span>")
                st.markdown(chips, unsafe_allow_html=True)
                block_input = st.text_input("Username", key="block_input")
                if st.button("🚫 Block", key="block_btn",
                             use_container_width=True):
                    u = block_input.strip().lower()
                    if not u:
                        st.warning("Enter an ID first!")
                    elif u == SS.username:
                        st.warning("Cannot block yourself!")
                    elif u in SS.blocked:
                        st.warning("Already blocked!")
                    else:
                        db = load_db()
                        rec = db["users"].get(SS.username)
                        if rec is not None:
                            rec.setdefault("blocked", []).append(u)
                            save_db(db)
                        SS.blocked.append(u)
                        SS.block_msg = "@" + u + " blocked."
                        safe_rerun()
                for i, u in enumerate(SS.blocked):
                    bc1, bc2 = st.columns([0.6, 0.4])
                    bc1.markdown("**🚫 @" + u + "**")
                    if bc2.button("Unblock", key="ub_" + str(i),
                                  use_container_width=True):
                        db = load_db()
                        rec = db["users"].get(SS.username)
                        if rec is not None and u in rec.get("blocked", []):
                            rec["blocked"].remove(u)
                            save_db(db)
                        SS.blocked.remove(u)
                        safe_rerun()

            elif SS.settings_page == "reports":
                settings_back("bk_reports")
                st.markdown('<div class="panel-header">⚠️ Report</div>',
                            unsafe_allow_html=True)
                if SS.report_msg:
                    st.success(SS.report_msg)
                    SS.report_msg = ""
                rep_id = st.text_input("Member ID", key="rep_id")
                reasons = ["Harassment", "Abusive Language", "Spam",
                           "Fake Account", "Scam", "Other"]
                reason = st.selectbox("Reason", reasons, key="rep_reason")
                if st.button("🚩 Submit Report", key="rep_btn",
                             use_container_width=True):
                    r = rep_id.strip().lower()
                    if r:
                        db = load_db()
                        db["reports"].append({
                            "from": SS.username, "user": r,
                            "reason": reason, "time": time.time()})
                        save_db(db)
                        add_notification(
                            "admin", "🚩 New report against @" + r +
                            " by @" + SS.username)
                        SS.report_msg = ("Report submitted! Admin ko "
                                         "notification chali gayi.")
                        safe_rerun()
                    else:
                        st.warning("Enter a member ID!")

                db = load_db()
                my_reps = [r for r in db["reports"]
                           if r["from"] == SS.username]
                for r in my_reps:
                    st.markdown("• 🚩 @" + r["user"] + " - " + r["reason"])

            elif SS.settings_page == "help":
                settings_back("bk_help")
                st.markdown(
                    "• **Profile link** - Profile tab se link copy karein\n"
                    "• **Groups** - Messages → Groups\n"
                    "• **Admin** - admin/admin123 se login karein\n"
                    "• **Reports** - Settings → Report")

            elif SS.settings_page == "about":
                settings_back("bk_about")
                st.markdown("**HMF book** v4.0.0\n\n"
                            "Profile Links • Groups • Notifications • "
                            "Screenshot Alerts • Camera • Admin Panel\n\n"
                            "© 2025 HMF")

    # ---------- BOTTOM NAV ----------
    st.markdown("<hr style='border:none;border-top:1px solid #e5e7eb;"
                "margin:25px 0 10px;'>", unsafe_allow_html=True)

    nb1, nb2, nb3, nb4, nb5, nb6, nb7, nb8 = st.columns(8)
    nav = [("🏠", "Home"), ("📺", "Channel"), ("🎬", "Reels"),
           ("➕", "Create"), ("✉️", "Messages"), ("🔔", "Notifications"),
           ("👤", "Profile"), ("⚙️", "Settings")]
    for i, (icon, tab) in enumerate(nav):
        col = [nb1, nb2, nb3, nb4, nb5, nb6, nb7, nb8][i]
        if col.button(icon, key="nav_" + tab, use_container_width=True):
            SS.current_tab = tab
            if tab == "Settings":
                SS.settings_page = "menu"
            safe_rerun()


# ---------- SAFETY ----------
else:
    SS.page = "splash"
    safe_rerun()
    

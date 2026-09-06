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

# ============ OWNER CONFIG ============
# Pehla NAYA signup automatically owner ban jata hai.
# Ya yahan apna username likh dein:
FORCE_OWNER = ""

CHANNEL_NAME = "Color Pop Cartoons"
CHANNEL_HANDLE = "@ColorPopCartoons83"
CHANNEL_URL = "https://www.youtube.com/" + CHANNEL_HANDLE


def get_owner(db):
    if FORCE_OWNER:
        return FORCE_OWNER
    return db.get("owner", "")


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
                "notifications", "reports", "banned"):
        if key not in db:
            db[key] = []
    if "follows" not in db:
        db["follows"] = {}
    if "owner" not in db:
        db["owner"] = ""
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
            n += 1
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
            b64 = base64.b64encode(
                open(avatar_path, "rb").read()).decode()
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


# ---------- JS HELPERS ----------
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
            key="base_url")
    except Exception:
        return None


def clear_profile_param():
    try:
        qp = dict(st.query_params)
        if "profile" in qp:
            st.query_params.pop("profile")
    except Exception:
        pass


# ---------- SEED ----------
DB = load_db()

SEED_USERS = [
    ("demo", "demo@hmfbook.com", "1234", "Demo User"),
    ("hoor_jannat", "hoor@hmfbook.com", "1234", "Hoor Jannat"),
    ("farrukh_m", "farrukh@hmfbook.com", "1234", "Farrukh M"),
    ("zara_x", "zara@hmfbook.com", "1234", "Zara X"),
]

changed = False
owner_now = get_owner(DB)
for uname, mail, pw, name in SEED_USERS:
    if uname in DB["banned"]:
        continue
    if uname not in DB["users"]:
        DB["users"][uname] = {
            "email": mail, "password": pw, "display_name": name,
            "bio": "Living life one post at a time.",
            "coins": 550, "followers": 1240, "following": 120,
            "blocked": [], "avatar": None}
        changed = True

if not DB["posts"]:
    DB["posts"] = [
        {"id": "s1", "user": "hoor_jannat", "type": "youtube",
         "ref": "aqz-KE-bpKQ", "cap": "Big Buck Bunny!",
         "likes": {}, "comments": [], "avatar": None},
        {"id": "s2", "user": "farrukh_m", "type": "text",
         "grad": "linear-gradient(45deg,#d1fae5,#a7f3d0)",
         "txt": "🎲 Ludo Night Tournament",
         "cap": "Tonight 8 PM - winner takes all!",
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
    "private_account": False, "strong_password": False,
    "two_factor": False, "login_alerts": True, "searchable": True,
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
    if SS.two_factor:
        score += 20
    else:
        tips.append("Enable 2FA (+20)")
    if SS.login_alerts:
        score += 15
    else:
        tips.append("Enable Login Alerts (+15)")
    if SS.app_lock:
        score += 20
    else:
        tips.append("Set up App Lock PIN (+20)")
    if SS.strong_password:
        score += 20
    else:
        tips.append("Use a stronger password (+20)")
    if SS.auto_logout > 0:
        score += 10
    else:
        tips.append("Enable Auto Logout (+10)")
    if SS.private_account:
        score += 10
    else:
        tips.append("Make account private (+10)")
    if SS.comment_filter:
        score += 5
    else:
        tips.append("Turn on Comment Filter (+5)")
    return score, tips


def settings_back(key):
    if st.button("← Back to Settings", key=key):
        SS.settings_page = "menu"
        SS.privacy_step = 0
        safe_rerun()


PROFILE_VIEW = None
try:
    qp = dict(st.query_params)
    PROFILE_VIEW = qp.get("profile")
except Exception:
    PROFILE_VIEW = None


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
    header[data-testid="stHeader"], #MainMenu, footer { visibility:hidden !important; }
    [data-testid="stToolbar"] { visibility:hidden !important; }
    [data-testid="stStatusWidget"] { visibility:hidden !important; }
    .block-container, [data-testid="block-container"] { max-width:460px; margin:0 auto; background:CARDBG; padding-top:0 !important; padding-bottom:30px !important; min-height:100vh; box-shadow:0 0 25px rgba(0,0,0,.12); }
    .insta-header { position:sticky; top:0; z-index:100; display:flex; justify-content:space-between; align-items:center; padding:14px 18px; background:CARDBG; border-bottom:1px solid BORDERC; }
    .brand-logo { font-size:28px; font-weight:900; color:LOGOC; letter-spacing:-1px; }
    .stories-container { display:flex; gap:15px; padding:12px 15px; background:CARDBG; border-bottom:1px solid BORDERC; overflow-x:auto; }
    .story-card { display:flex; flex-direction:column; align-items:center; text-align:center; min-width:65px; }
    .story-ring { width:60px; height:60px; border-radius:50%; padding:2.5px; background:linear-gradient(135deg,#00B074 0%,#056839 100%); display:flex; align-items:center; justify-content:center; }
    .story-img { width:100%; height:100%; border-radius:50%; background:CARDBG; border:2px solid CARDBG; display:flex; align-items:center; justify-content:center; font-weight:bold; color:TXT2; font-size:14px; }
    .story-name { font-size:11px; color:TXT2; margin-top:4px; max-width:65px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
    .post-card { background:CARDBG; margin-bottom:12px; border-bottom:1px solid BORDERC; }
    .post-header { display:flex; align-items:center; padding:12px 15px; }
    .post-username { font-size:14px; font-weight:700; color:TXT1; }
    .post-image-placeholder { width:100%; height:300px; background:#f3f4f6; display:flex; align-items:center; justify-content:center; font-size:16px; }
    .likes-txt { padding:8px 15px 2px; font-weight:600; font-size:13px; color:TXT1; margin:0; }
    .post-details { padding:0 15px 10px 15px; font-size:14px; color:TXT1; margin:0; }
    .panel-header { padding:18px; font-size:22px; font-weight:bold; color:LOGOC; border-bottom:1px solid BORDERC; text-align:center; }
    .set-label { font-weight:700; color:TXT1; margin:14px 0 4px; }
    .channel-banner { background:linear-gradient(135deg,#00B074,#056839); border-radius:16px; padding:20px; text-align:center; margin:12px 0; }
    .channel-banner h2 { color:#fff; margin:0 0 4px; font-size:22px; }
    .channel-banner p { color:rgba(255,255,255,.9); margin:0; font-size:13px; }
    .chat-me { background:#00B074; color:#fff; padding:8px 14px; border-radius:16px 16px 4px 16px; max-width:72%; margin:4px 0 4px auto; font-size:14px; display:block; width:fit-content; }
    .chat-them { background:BORDERC; color:TXT1; padding:8px 14px; border-radius:16px 16px 16px 4px; max-width:72%; margin:4px auto 4px 0; font-size:14px; display:block; width:fit-content; }
    .chat-time { font-size:10px; color:TXT2; display:block; text-align:right; }
    .lock-screen { display:flex; flex-direction:column; align-items:center; justify-content:center; height:60vh; text-align:center; }
    .member-chip { display:inline-block; background:CARDBG; border:1px solid BORDERC; border-radius:20px; padding:4px 12px; margin:3px; font-size:12px; color:TXT2; }
    .notif-row { padding:10px 6px; border-bottom:1px solid BORDERC; font-size:14px; color:TXT1; }
    .badge-dot { background:#e53e3e; color:#fff; border-radius:50%; padding:2px 8px; font-size:11px; font-weight:bold; margin-left:6px; }
    .search-row { display:flex; align-items:center; padding:10px 4px; border-bottom:1px solid BORDERC; }
    .owner-badge { background:linear-gradient(135deg,#f59e0b,#d97706); color:#fff; padding:3px 10px; border-radius:12px; font-size:11px; font-weight:bold; }
    .ban-tag { background:#e53e3e; color:#fff; padding:3px 10px; border-radius:12px; font-size:11px; font-weight:bold; }
    div[data-testid="stButton"] > button, div.stButton > button { background:#00B074 !important; color:#fff !important; font-weight:600 !important; border:none !important; border-radius:12px !important; }
    div[data-testid="stButton"] > button:hover, div.stButton > button:hover { background:#056839 !important; color:#fff !important; }
    </style>
    """
    for k, v in T.items():
        css = css.replace(k, v)
    if dark:
        css += """
        <style>
        [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea { background:#242824 !important; color:#fff !important; border-color:#3a3f3a !important; }
        [data-testid="stCheckbox"] label p, [data-testid="stRadio"] label p { color:#e5e9e5 !important; }
        hr { border-color:#2a2e2a !important; }
        </style>
        """
    return css


# ================= 1) SPLASH =================
if SS.page == "splash":

    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #00B074 0%, #056839 100%) !important; }
    header[data-testid="stHeader"], #MainMenu, footer { visibility:hidden !important; }
    [data-testid="stToolbar"] { visibility:hidden !important; }
    .mid { display:flex; flex-direction:column; align-items:center; justify-content:center; height:60vh; text-align:center; }
    .logo { font-size:90px; font-weight:900; color:#fff; letter-spacing:4px; text-shadow:0 4px 14px rgba(0,0,0,.25); margin:0; }
    .sub { font-size:24px; color:rgba(255,255,255,.92); margin:5px 0 0; }
    div[data-testid="stButton"] > button { background:#fff !important; color:#00B074 !important; font-size:18px !important; font-weight:bold !important; padding:12px 45px !important; border-radius:30px !important; border:none !important; box-shadow:0 4px 15px rgba(0,0,0,.25) !important; }
    </style>
    """, unsafe_allow_html=True)

    db = load_db()

    if PROFILE_VIEW and PROFILE_VIEW in db["users"]:
        u = db["users"][PROFILE_VIEW]
        my_posts = [p for p in db["posts"] if p["user"] == PROFILE_VIEW]
        st.markdown(build_main_css(False), unsafe_allow_html=True)
        st.markdown('<div class="panel-header">👤 HMF Profile</div>',
                    unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;margin:10px 0;'>" +
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
            SS.page = "app" if SS.logged_in else "auth"
            safe_rerun()
    else:
        st.markdown("<div class='mid'><h1 class='logo'>HMF</h1>"
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
        title = "Create Account"
        btn_label = "Sign Up"
        switch_txt = "Already have an account? Login"
    else:
        title = "Welcome Back"
        btn_label = "Login"
        switch_txt = "New here? Create an account"

    st.markdown("""
    <style>
    .stApp { background:#F3FAF6 !important; }
    header[data-testid="stHeader"], #MainMenu, footer { visibility:hidden !important; }
    [data-testid="stToolbar"] { visibility:hidden !important; }
    .badge { background:linear-gradient(135deg,#00B074,#056839); display:inline-block; padding:18px 52px; border-radius:22px; box-shadow:0 6px 18px rgba(0,176,116,.35); }
    .badge h1 { color:#fff; font-size:36px; font-weight:900; letter-spacing:3px; margin:0; }
    .title { text-align:center; font-size:24px; font-weight:700; color:#222; margin:26px 0 4px; }
    div[data-testid="stButton"] > button { background:#00B074 !important; color:#fff !important; font-weight:600 !important; border:none !important; border-radius:12px !important; }
    </style>
    <div style="text-align:center; margin-top:14px;"><div class="badge"><h1>HMF</h1></div></div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 class='title'>" + title + "</h2>",
                unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter username")
    if is_signup:
        email = st.text_input("Email", placeholder="Enter email")
    password = st.text_input("Password", type="password",
                             placeholder="Enter password")

    if st.button(btn_label, use_container_width=True):
        u = username.strip().lower()
        db = load_db()

        if not u or not password:
            st.error("Please enter both username and password!")
        elif u in db["banned"]:
            st.error("🚫 This account has been PERMANENTLY BANNED "
                     "by the owner! You cannot login.")
        elif is_signup:
            if u in db["users"]:
                st.error("This username is already taken!")
            else:
                became_owner = False
                if not get_owner(db) and not db.get("owner"):
                    db["owner"] = u
                    became_owner = True
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
                if became_owner:
                    st.balloons()
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
                safe_rerun()
            else:
                st.error("Invalid username or password!")

    if st.button(switch_txt):
        SS.auth_mode = "login" if is_signup else "signup"
        safe_rerun()

    st.markdown("<p style='text-align:center;color:#99a;font-size:13px;'>"
                "Demo: demo / 1234 • Pehla naya signup = Owner 👑</p>",
                unsafe_allow_html=True)


# ================= 3) PIN LOCK =================
elif (SS.page == "app" and SS.logged_in and SS.app_lock
      and not SS.pin_unlocked):

    st.markdown(build_main_css(SS.dark_mode), unsafe_allow_html=True)
    st.markdown("""
    <div class="lock-screen">
        <div style="font-size:60px;">🔐</div>
        <h2>App Locked</h2>
    </div

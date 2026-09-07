import streamlit as st
import streamlit.components.v1 as components
import random
import json
import os
import io
import time
import uuid
import base64
import hashlib
from html import escape as esc
from urllib.parse import quote_plus
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

st.set_page_config(page_title="HMF Book", page_icon="🟢",
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

FORCE_OWNER = ""
SALT = "hmf_book_secret_2025"
APP_INFO = {
    "name": "HMF Book", "founded": "February 4, 2026",
    "founders": "Mehmood Sial, Hoor-e-Jannat, Farwa",
    "parent": "HMF Group",
    "hq": "Bahawalpur / Okara, Pakistan",
    "type": "Social networking + earning platform",
}
CHANNEL_NAME = "Color Pop Cartoons"
CHANNEL_HANDLE = "@ColorPopCartoons83"
CHANNEL_URL = "https://www.youtube.com/" + CHANNEL_HANDLE
DB_FILE = "hmf_db.json"
UPLOAD_DIR = "uploads"
FILTER_NAMES = ["None", "Beauty", "Sepia", "Vintage", "Cool",
                "Grayscale", "Bright", "Cartoon"]
GRADS = ["linear-gradient(45deg,#d1fae5,#a7f3d0)",
         "linear-gradient(45deg,#ecfdf5,#6ee7b7)",
         "linear-gradient(45deg,#e6f7f0,#b3e6cc)"]
VALID_TABS = ["Home", "Search", "Friends", "Groups", "Pages",
              "Events", "Marketplace", "Channel", "Reels",
              "Create", "Messages", "Notifications", "Ludo",
              "Profile", "Settings", "Ads"]


def hash_pw(pw):
    return hashlib.sha256((SALT + pw).encode()).hexdigest()


def pw_ok(stored, pw):
    return stored == hash_pw(pw) or stored == pw


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


def parse_youtube_id(url):
    url = (url or "").strip()
    if not url:
        return None
    if len(url) == 11 and "/" not in url:
        return url
    for tag in ("youtu.be/", "v=", "/shorts/", "/embed/"):
        if tag in url:
            p = url.split(tag)[1]
            p = p.split("?")[0].split("&")[0].split("/")[0]
            if p:
                return p
    return None


def load_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
    except Exception:
        db = {}
    for key in ("users", "messages", "posts", "groups",
                "notifications", "reports", "banned",
                "friend_requests", "pages", "events",
                "listings", "ads"):
        if key not in db:
            db[key] = []
    for key in ("follows", "friends", "seen"):
        if key not in db:
            db[key] = {}
    if "owner" not in db:
        db["owner"] = ""
    return db


def save_db(db):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=1)
    except Exception:
        pass


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


def unseen_count(me, partner):
    db = load_db()
    last = db.get("seen", {}).get(me, {}).get(partner, 0)
    return sum(1 for m in db["messages"]
               if m["from"] == partner and m["to"] == me
               and m.get("time", 0) > last)


def mark_seen(me, partner):
    db = load_db()
    db.setdefault("seen", {}).setdefault(me, {})[partner] = \
        time.time()
    save_db(db)


def toggle_reaction(is_group, group_id, msg_id, user):
    db = load_db()
    if is_group:
        for g in db["groups"]:
            if g["id"] == group_id:
                for m in g["messages"]:
                    if m.get("id") == msg_id:
                        rr = m.setdefault("reactions", [])
                        if user in rr:
                            rr.remove(user)
                        else:
                            rr.append(user)
                        break
                break
    else:
        for m in db["messages"]:
            if m.get("id") == msg_id:
                rr = m.setdefault("reactions", [])
                if user in rr:
                    rr.remove(user)
                else:
                    rr.append(user)
                break
    save_db(db)


def send_chat_message(is_group, group_id, to_user, text,
                      photo=None):
    me = st.session_state.username
    db = load_db()
    msg = {"id": uuid.uuid4().hex[:8], "from": me,
           "text": text, "time": time.time(),
           "reactions": []}
    if photo:
        msg["photo"] = photo
    if is_group:
        for g in db["groups"]:
            if g["id"] == group_id:
                g["messages"].append(msg)
                break
        save_db(db)
    else:
        msg["to"] = to_user
        db["messages"].append(msg)
        save_db(db)
        add_notification(to_user, "✉️ @" + me +
                         " sent you a message")


def send_friend_request(a, b):
    db = load_db()
    for r in db["friend_requests"]:
        if r["from"] == a and r["to"] == b:
            return
    db["friend_requests"].append(
        {"from": a, "to": b, "time": time.time()})
    save_db(db)
    add_notification(b, "👋 @" + a +
                     " sent you a friend request!")


def accept_friend(a, b):
    db = load_db()
    db["friend_requests"] = [
        r for r in db["friend_requests"]
        if not (r["from"] == b and r["to"] == a)]
    fa = db["friends"].setdefault(a, [])
    fb = db["friends"].setdefault(b, [])
    if b not in fa:
        fa.append(b)
    if a not in fb:
        fb.append(a)
    save_db(db)
    add_notification(b, "✅ @" + a +
                     " accepted your friend request!")


def reject_friend(a, b):
    db = load_db()
    db["friend_requests"] = [
        r for r in db["friend_requests"]
        if not (r["from"] == b and r["to"] == a)]
    save_db(db)


def remove_friend(a, b):
    db = load_db()
    fa = db["friends"].get(a, [])
    fb = db["friends"].get(b, [])
    if b in fa:
        fa.remove(b)
    if a in fb:
        fb.remove(a)
    save_db(db)


def save_upload(file_obj):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = file_obj.name.split(".")[-1].lower()
    if ext not in ("png", "jpg", "jpeg", "webp",
                   "mp4", "mov", "webm"):
        ext = "bin"
    fname = uuid.uuid4().hex + "." + ext
    path = os.path.join(UPLOAD_DIR, fname)
    with open(path, "wb") as out:
        out.write(file_obj.getbuffer())
    return path


def save_pil(pil_img):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    fname = uuid.uuid4().hex + ".png"
    path = os.path.join(UPLOAD_DIR, fname)
    pil_img.save(path, "PNG")
    return path


def avatar_html(username, avatar_path=None, size=36,
                border=False):
    bstyle = "border:4px solid #fff;" if border else ""
    if avatar_path and os.path.exists(avatar_path):
        try:
            b64 = base64.b64encode(
                open(avatar_path, "rb").read()).decode()
            return ("<img src='data:image/png;base64," + b64 +
                    "' style='width:" + str(size) +
                    "px;height:" + str(size) +
                    "px;border-radius:50%;object-fit:cover;"
                    "margin-right:10px;" + bstyle + "'>")
        except Exception:
            pass
    ini = esc(str(username)[:2].upper())
    return ("<div style='width:" + str(size) +
            "px;height:" + str(size) +
            "px;border-radius:50%;background:"
            "linear-gradient(135deg,#00B074,#056839);"
            "color:#fff;display:flex;align-items:center;"
            "justify-content:center;font-weight:bold;"
            "margin-right:10px;" + bstyle + "font-size:" +
            str(int(size * 0.38)) + "px;'>" + ini + "</div>")


def apply_filter(pil_img, name):
    try:
        img = pil_img.convert("RGB")
        if name == "Beauty":
            b = img.filter(ImageFilter.GaussianBlur(3))
            out = Image.blend(img, b, 0.5)
            out = ImageEnhance.Brightness(out).enhance(1.1)
            out = ImageEnhance.Color(out).enhance(1.15)
        elif name == "Sepia":
            out = ImageOps.colorize(img.convert("L"),
                                    "#704214", "#ffe8c0")
        elif name == "Vintage":
            out = ImageOps.colorize(img.convert("L"),
                                    "#3a2a1a", "#e8d8b0")
        elif name == "Cool":
            out = ImageOps.colorize(img.convert("L"),
                                    "#20304a", "#c8e0ff")
        elif name == "Grayscale":
            out = img.convert("L").convert("RGB")
        elif name == "Bright":
            out = ImageEnhance.Brightness(img).enhance(1.4)
        elif name == "Cartoon":
            small = img.resize((max(1, img.width // 6),
                                max(1, img.height // 6)))
            small = small.filter(ImageFilter.MedianFilter(7))
            out = small.resize((img.width, img.height))
            out = ImageOps.posterize(out, 5)
            out = ImageEnhance.Color(out).enhance(1.3)
        else:
            out = img
        return out
    except Exception:
        return pil_img


def is_local_file(ref):
    ref = str(ref or "")
    if ref.startswith("http"):
        return False
    return os.path.exists(ref)


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


def rsvp_status(event, user):
    for r in event.get("rsvps", []):
        if r["user"] == user:
            return r["status"]
    return ""


def set_rsvp(event_id, user, status):
    db = load_db()
    for e in db["events"]:
        if e["id"] == event_id:
            e.setdefault("rsvps", [])
            e["rsvps"] = [r for r in e["rsvps"]
                          if r["user"] != user]
            if status:
                e["rsvps"].append({"user": user,
                                   "status": status})
            break
    save_db(db)


# ---------- SEED ----------
DB = load_db()
SEED_USERS = [
    ("demo", "demo@hmfbook.com", "1234", "Demo User",
     "21 Dec 1996", "Male"),
    ("hoor_jannat", "hoor@hmfbook.com", "1234",
     "Hoor Jannat", "14 Mar 2000", "Female"),
    ("farrukh_m", "farrukh@hmfbook.com", "1234",
     "Farrukh M", "5 Jan 1995", "Male"),
    ("zara_x", "zara@hmfbook.com", "1234",
     "Zara X", "9 Sep 1999", "Female"),
]
changed = False
for uname, mail, pw, name, bday, gen in SEED_USERS:
    if uname in DB["banned"]:
        continue
    if uname not in DB["users"]:
        DB["users"][uname] = {
            "email": mail, "password": hash_pw(pw),
            "display_name": name,
            "bio": "Living life one post at a time.",
            "birthday": bday, "gender": gen,
            "coins": 550, "followers": 1240,
            "blocked": [], "avatar": None,
            "fails": 0, "lock_until": 0}
        changed = True

if not DB["posts"]:
    DB["posts"] = [
        {"id": "s1", "user": "hoor_jannat",
         "type": "youtube", "ref": "aqz-KE-bpKQ",
         "cap": "Big Buck Bunny!", "likes": {},
         "comments": [], "avatar": None},
        {"id": "s2", "user": "farrukh_m", "type": "text",
         "grad": GRADS[0], "txt": "🎲 Ludo Night",
         "cap": "Tonight 8 PM - winner takes all!",
         "likes": {}, "comments": [], "avatar": None},
        {"id": "s3", "user": "demo", "type": "text",
         "grad": GRADS[1], "txt": "🌿 Green Vibes",
         "cap": "Loving HMF Book!", "likes": {},
         "comments": [], "avatar": None},
    ]
    changed = True

if not DB["pages"]:
    DB["pages"].append({
        "id": "pg1", "name": "HMF Official",
        "category": "Brand",
        "owner": "demo", "description":
        "The official HMF Book page!",
        "followers": ["hoor_jannat"], "createdAt":
        time.time()})
    changed = True

if not DB["events"]:
    DB["events"].append({
        "id": "ev1", "title": "HMF Meetup Bahawalpur",
        "description": "Sab users milte hain!",
        "host": "demo", "location": "Bahawalpur",
        "date": "2026-03-15", "time": "6:00 PM",
        "rsvps": []})
    changed = True

if not DB["listings"]:
    DB["listings"].append({
        "id": "ls1", "seller": "farrukh_m",
        "title": "Gaming Mouse", "description":
        "Almost new, RGB lights", "price": 1500,
        "category": "Electronics", "image": None,
        "location": "Okara", "status": "available"})
    changed = True

if changed:
    save_db(DB)


# ---------- SESSION STATE ----------
SS = st.session_state
defaults = {
    "page": "splash", "logged_in": False, "username": "",
    "email": "", "auth_mode": "login", "current_tab": "Home",
    "settings_page": "menu", "privacy_step": 0,
    "blocked": [], "clear_cmt": "", "clear_msg": "",
    "block_msg": "", "report_msg": "", "withdraw_msg": "",
    "yt_msg": "", "view_user": None,
    "open_group": "", "open_page": "", "open_event": "",
    "open_listing": "", "prof_tab": "All",
    "msg_view": "list", "msg_target": "",
    "msg_target_type": "direct", "last_shot_time": 0,
    "app_lock": False, "app_pin": "", "pin_unlocked": True,
    "pin_attempts": 0, "pin_lock_until": 0,
    "finger_lock": False, "finger_unlocked": True,
    "auto_logout": 0, "last_active": 0, "dark_mode": False,
    "feed_sort": "Most Recent", "show_stories": True,
    "comment_filter": True, "private_account": False,
    "strong_password": False, "two_factor": False,
    "login_alerts": True, "security_log": [],
    "room_code": "", "dice": 0,
    "notif": {"likes": True, "comments": True,
              "follows": True, "messages": True},
}
for k, v in defaults.items():
    if k not in SS:
        SS[k] = v

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
    if any(c.isupper() for c in pw) and \
            any(c.islower() for c in pw):
        score += 25
    symbols = "!@#$%^&*()-_=+[]{};:,.<>?/"
    if any(c in symbols for c in pw):
        score += 25
    return score


def security_score():
    score = 0
    tips = []
    checks = [(SS.two_factor, 20, "Enable 2FA (+20)"),
              (SS.login_alerts, 15, "Login Alerts (+15)"),
              (SS.app_lock or SS.finger_lock, 20,
               "App Lock/Fingerprint (+20)"),
              (SS.strong_password, 20,
               "Stronger password (+20)"),
              (SS.auto_logout > 0, 10, "Auto Logout (+10)"),
              (SS.private_account, 10,
               "Private account (+10)"),
              (SS.comment_filter, 5, "Comment Filter (+5)")]
    for ok, pts, tip in checks:
        if ok:
            score += pts
        else:
            tips.append(tip)
    return score, tips


def settings_back(key):
    if st.button("← Back to Settings", key=key):
        SS.settings_page = "menu"
        safe_rerun()


try:
    qp = dict(st.query_params)
except Exception:
    qp = {}

tab_q = qp.get("tab")
dark_q = qp.get("dark")

if SS.logged_in:
    if tab_q in VALID_TABS:
        SS.current_tab = tab_q
        if tab_q == "Settings":
            SS.settings_page = "menu"
        if tab_q == "Messages":
            SS.msg_view = "list"
    if dark_q in ("0", "1"):
        SS.dark_mode = dark_q == "1"

if tab_q in VALID_TABS or dark_q in ("0", "1"):
    try:
        st.query_params.clear()
    except Exception:
        pass


# ---------- CSS ----------
def build_main_css(dark):
    if dark:
        T = {"APPBG": "#0f1110", "CARDBG": "#1b1e1b",
             "BORDERC": "#2a2e2a", "TXT1": "#eef1ee",
             "TXT2": "#9aa69a", "LOGOC": "#00e08a"}
    else:
        T = {"APPBG": "#f0f2f5", "CARDBG": "#ffffff",
             "BORDERC": "#e5e7eb", "TXT1": "#1f2937",
             "TXT2": "#4b5563", "LOGOC": "#00B074"}

    css = """
    <style>
    .stApp { background-color:APPBG !important; }
    header[data-testid="stHeader"], #MainMenu, footer
        { visibility:hidden !important; }
    [data-testid="stToolbar"], [data-testid=
        "stStatusWidget"], [data-testid="stDecoration"]
        { display:none !important; }
    .block-container, [data-testid="block-container"] {
        max-width:430px; margin:0 auto;
        background:CARDBG; padding-top:0 !important;
        padding-left:10px !important;
        padding-right:10px !important;
        padding-bottom:95px !important;
        min-height:100vh;
        box-shadow:0 0 35px rgba(0,0,0,.18); }
    .ig-topbar { position:sticky; top:0; z-index:995;
        display:flex; justify-content:space-between;
        align-items:center; padding:12px 14px;
        background:CARDBG;
        border-bottom:1px solid BORDERC;
        margin:0 -10px; }
    .ig-logo { font-size:26px; font-weight:700;
        font-family:'Segoe Script','Brush Script MT',
        cursive; color:TXT1; }
    .ig-icons a { font-size:21px; text-decoration:none;
        margin-left:14px; position:relative; }
    .nav-dot { position:absolute; top:-6px;
        right:-10px; background:#e53e3e; color:#fff;
        border-radius:10px; font-size:10px;
        font-weight:700; padding:1px 5px; }
    .stories-container { display:flex; gap:14px;
        padding:12px 4px;
        border-bottom:1px solid BORDERC;
        overflow-x:auto; }
    .story-card { display:flex; flex-direction:column;
        align-items:center; min-width:64px; }
    .story-ring { width:58px; height:58px;
        border-radius:50%; padding:2.5px;
        background:linear-gradient(135deg,#00B074,
        #056839); display:flex;
        align-items:center; justify-content:center; }
    .story-ring.gray { background:#dbdbdb; }
    .story-img { width:100%; height:100%;
        border-radius:50%; background:CARDBG;
        border:2px solid CARDBG; display:flex;
        align-items:center; justify-content:center;
        font-weight:bold; color:TXT2; font-size:14px; }
    .story-name { font-size:11px; color:TXT2;
        margin-top:4px; }
    .quick-row { display:flex; gap:8px; padding:10px 0 4px;
        flex-wrap:wrap; }
    .quick-pill { text-align:center; padding:6px 10px;
        border:1px solid BORDERC; border-radius:20px;
        font-size:12px; text-decoration:none;
        color:TXT1; font-weight:600; }
    .post-card { background:CARDBG;
        border-bottom:1px solid BORDERC;
        margin-bottom:10px; }
    .post-header { display:flex; align-items:center;
        padding:10px 4px; }
    .post-username { font-size:14px; font-weight:700;
        color:TXT1; }
    .post-ph { width:100%; height:300px;
        background:#f3f4f6; display:flex;
        align-items:center; justify-content:center;
        font-size:16px; }
    .likes-txt { padding:6px 2px 0; font-weight:600;
        font-size:13px; color:TXT1; margin:0; }
    .post-details { padding:0 2px 8px; font-size:14px;
        color:TXT1; margin:0; }
    .panel-header { padding:16px 4px; font-size:20px;
        font-weight:bold; color:LOGOC;
        border-bottom:1px solid BORDERC;
        text-align:center; }
    .set-label { font-weight:700; color:TXT1;
        margin:12px 0 4px; }
    .channel-banner {
        background:linear-gradient(135deg,#00B074,
        #056839); border-radius:16px; padding:18px;
        text-align:center; margin:10px 0; }
    .channel-banner h2 { color:#fff; margin:0 0 4px;
        font-size:20px; }
    .channel-banner p { color:rgba(255,255,255,.9);
        margin:0; font-size:12px; }
    .notif-row { padding:10px 4px;
        border-bottom:1px solid BORDERC;
        font-size:14px; color:TXT1; }
    .badge-dot { background:#e53e3e; color:#fff;
        border-radius:50%; padding:2px 8px;
        font-size:11px; font-weight:bold;
        margin-left:6px; }
    .owner-badge {
        background:linear-gradient(135deg,#f59e0b,
        #d97706); color:#fff; padding:2px 10px;
        border-radius:12px; font-size:11px;
        font-weight:bold; }
    .ban-tag { background:#e53e3e; color:#fff;
        padding:2px 10px; border-radius:12px;
        font-size:11px; font-weight:bold; }
    .chat-item { display:flex; align-items:center;
        padding:11px 4px;
        border-bottom:1px solid BORDERC; }
    .av-wrap { position:relative; margin-right:6px; }
    .online-dot { position:absolute; bottom:2px;
        right:2px; width:12px; height:12px;
        border-radius:50%; background:#31a24c;
        border:2px solid CARDBG; }
    .chat-info { flex:1; min-width:0; }
    .chat-name { font-weight:700; font-size:14px;
        color:TXT1; }
    .chat-preview { font-size:12.5px; color:TXT2;
        overflow:hidden; text-overflow:ellipsis;
        white-space:nowrap; margin-top:2px; }
    .chat-time { font-size:11px; color:TXT2; }
    .unread-badge { background:#00B074; color:#fff;
        border-radius:50%; min-width:20px; height:20px;
        display:inline-flex; align-items:center;
        justify-content:center; font-size:11px;
        font-weight:700; padding:0 6px; }
    .bubble-me { background:#00B074; color:#fff;
        padding:8px 13px;
        border-radius:18px 18px 4px 18px;
        max-width:78%; margin:3px 0 3px auto;
        font-size:14px; display:block;
        width:fit-content; }
    .bubble-them { background:BORDERC; color:TXT1;
        padding:8px 13px;
        border-radius:18px 18px 18px 4px;
        max-width:78%; margin:3px auto 3px 0;
        font-size:14px; display:block;
        width:fit-content; }
    .bubble-time { font-size:10px; opacity:.75;
        display:block; text-align:right; }
    .fr-row { display:flex; align-items:center;
        padding:10px 4px;
        border-bottom:1px solid BORDERC; }
    .search-row { display:flex; align-items:center;
        padding:10px 4px;
        border-bottom:1px solid BORDERC; }
    .lock-screen { display:flex; flex-direction:column;
        align-items:center; justify-content:center;
        height:60vh; text-align:center; }
    .finger-icon { font-size:70px; margin-bottom:10px; }
    .fb-cover { height:120px; border-radius:0 0 14px 14px;
        background:linear-gradient(135deg,#00B074,
        #056839); margin:0 -10px; }
    .fb-av-wrap { text-align:center; margin:-50px 0 0; }
    .fb-name { text-align:center; font-size:22px;
        font-weight:800; color:TXT1; margin:8px 0 2px; }
    .fb-sub { text-align:center; font-size:13px;
        color:TXT2; margin:0 0 12px; }
    .pd-row { display:flex; align-items:center;
        gap:10px; padding:9px 4px; font-size:14px;
        color:TXT1; }
    .composer { display:flex; align-items:center;
        gap:10px; border:1px solid BORDERC;
        border-radius:20px; padding:10px 14px;
        font-size:14px; color:TXT2; margin:8px 0; }
    .g-links { display:flex; flex-direction:column;
        gap:8px; margin:8px 0; }
    .g-link { display:block; padding:10px 14px;
        border:1px solid BORDERC; border-radius:12px;
        text-decoration:none; font-size:14px;
        font-weight:600; color:LOGOC; }
    /* FB-style cards */
    .grp-card { border:1px solid BORDERC;
        border-radius:12px; padding:12px;
        margin-bottom:10px; }
    .grp-cover { height:70px; border-radius:8px;
        background:linear-gradient(135deg,#00B074,
        #056839); margin-bottom:8px; }
    .grp-name { font-weight:800; font-size:15px;
        color:TXT1; }
    .grp-sub { font-size:12px; color:TXT2; }
    .ev-date { background:#00B074; color:#fff;
        border-radius:8px; padding:6px 10px;
        text-align:center; min-width:54px;
        font-weight:700; font-size:12px; }
    .ad-card { border:2px solid #f59e0b;
        border-radius:12px; padding:12px;
        margin:10px 0;
        background:rgba(245,158,11,.06); }
    .ad-tag { background:#f59e0b; color:#fff;
        padding:2px 8px; border-radius:8px;
        font-size:10px; font-weight:700; }
    .mk-grid { display:grid;
        grid-template-columns:repeat(2,1fr);
        gap:10px; }
    .mk-card { border:1px solid BORDERC;
        border-radius:12px; overflow:hidden;
        text-align:center; padding:10px; }
    .mk-price { color:#00B074; font-weight:800;
        font-size:16px; }
    .ig-nav { position:fixed; bottom:0; left:50%;
        transform:translateX(-50%); width:100%;
        max-width:430px; background:CARDBG;
        border-top:1px solid BORDERC;
        display:flex; justify-content:space-around;
        align-items:center; padding:10px 0 14px;
        z-index:998; }
    .ig-nav a { font-size:22px; text-decoration:none;
        filter:grayscale(1) opacity(.45);
        position:relative; line-height:1; }
    .ig-nav a.on { filter:none; transform:scale(1.12); }
    div[data-testid="stButton"] > button,
    div.stButton > button { background:#00B074
        !important; color:#fff !important;
        font-weight:600 !important; border:none
        !important; border-radius:12px !important; }
    div[data-testid="stButton"] > button:hover {
        background:#056839 !important;
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
            background:#242824 !important;
            color:#fff !important;
            border-color:#3a3f3a !important; }
        [data-testid="stCheckbox"] label p,
        [data-testid="stRadio"] label p {
            color:#e5e9e5 !important; }
        </style>
        """
    return css


SPLASH_CSS = """
<style>
.stApp { background: linear-gradient(135deg,#00B074 0%,
    #056839 100%) !important; }
header[data-testid="stHeader"], #MainMenu, footer {
    visibility:hidden !important; }
[data-testid="stToolbar"], [data-testid=
    "stDecoration"] { display:none !important; }
.mid { display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    height:60vh; text-align:center; }
.logo { font-size:90px; font-weight:900; color:#fff;
    letter-spacing:4px;
    text-shadow:0 4px 14px rgba(0,0,0,.25); margin:0; }
.sub { font-size:24px; color:rgba(255,255,255,.92);
    margin:5px 0 0; }
div[data-testid="stButton"] > button {
    background:#fff !important; color:#00B074
    !important; font-size:18px !important;
    font-weight:bold !important;
    padding:12px 45px !important;
    border-radius:30px !important; border:none
    !important;
    box-shadow:0 4px 15px rgba(0,0,0,.25) !important; }
</style>
"""

AUTH_CSS = """
<style>
.stApp { background:#F3FAF6 !important; }
header[data-testid="stHeader"], #MainMenu, footer {
    visibility:hidden !important; }
[data-testid="stToolbar"], [data-testid=
    "stDecoration"] { display:none !important; }
.badge { background:linear-gradient(135deg,#00B074,
    #056839); display:inline-block; padding:18px 52px;
    border-radius:22px;
    box-shadow:0 6px 18px rgba(0,176,116,.35); }
.badge h1 { color:#fff; font-size:36px; font-weight:900;
    letter-spacing:3px; margin:0; }
.title { text-align:center; font-size:24px;
    font-weight:700; color:#222; margin:26px 0 4px; }
div[data-testid="stButton"] > button {
    background:#00B074 !important; color:#fff
    !important; font-weight:600 !important;
    border:none !important;
    border-radius:12px !important; }
</style>
"""


# ================= 1) SPLASH =================
if SS.page == "splash":
    st.markdown(SPLASH_CSS, unsafe_allow_html=True)
    st.markdown("<div class='mid'><h1 class='logo'>HMF"
                "</h1><p class='sub'>HMF Book</p></div>",
                unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        if st.button("Get Started",
                     use_container_width=True):
            SS.page = "auth"
            safe_rerun()


# ================= 2) LOGIN =================
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

    st.markdown(AUTH_CSS, unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;'
                'margin-top:14px;"><div class="badge">'
                '<h1>HMF</h1></div></div>',
                unsafe_allow_html=True)
    st.markdown("<h2 class='title'>" + title + "</h2>",
                unsafe_allow_html=True)

    username = st.text_input("Username",
                             placeholder="Enter username")
    if is_signup:
        email = st.text_input("Email",
                              placeholder="Enter email")
    password = st.text_input("Password", type="password",
                             placeholder="Enter password")

    if is_signup and password:
        sc = password_strength(password)
        st.progress(sc)
        if sc >= 75:
            SS.strong_password = True
            st.caption("Strong password!")
        else:
            SS.strong_password = False
            st.caption("Weak - use 8+ chars")

    if st.button(btn_label, use_container_width=True):
        u = username.strip().lower()
        db = load_db()
        if not u or not password:
            st.error("Please enter username and password!")
        elif u in db["banned"]:
            st.error("🚫 PERMANENTLY BANNED by owner!")
        elif is_signup:
            if u in db["users"]:
                st.error("Username taken!")
            else:
                became_owner = False
                if FORCE_OWNER:
                    db["owner"] = FORCE_OWNER
                elif not db.get("owner"):
                    db["owner"] = u
                    became_owner = True
                db["users"][u] = {
                    "email": email,
                    "password": hash_pw(password),
                    "display_name": u.title(),
                    "bio": "New to HMF Book!",
                    "birthday": "Not set",
                    "gender": "Not set",
                    "coins": 100, "followers": 0,
                    "blocked": [], "avatar": None,
                    "fails": 0, "lock_until": 0}
                save_db(db)
                SS.logged_in = True
                SS.username = u
                SS.page = "app"
                SS.last_active = time.time()
                if became_owner:
                    st.balloons()
                safe_rerun()
        else:
            rec = db["users"].get(u)
            if rec and rec.get("lock_until", 0) > \
                    time.time():
                st.error("🔒 Locked! Wait " +
                         str(int(rec["lock_until"] -
                                 time.time()) + 1) + "s.")
            elif rec and pw_ok(rec.get("password", ""),
                               password):
                rec["fails"] = 0
                rec["lock_until"] = 0
                save_db(db)
                SS.logged_in = True
                SS.username = u
                SS.blocked = rec.get("blocked", [])
                SS.page = "app"
                SS.pin_unlocked = True
                SS.finger_unlocked = True
                SS.last_active = time.time()
                safe_rerun()
            elif rec:
                rec["fails"] = rec.get("fails", 0) + 1
                if rec["fails"] >= 5:
                    rec["lock_until"] = time.time() + 60
                    rec["fails"] = 0
                    st.error("🔒 5 wrong! Locked 60s.")
                else:
                    st.error("Invalid! " +
                             str(5 - rec["fails"]) +
                             " left.")
                save_db(db)
            else:
                st.error("Invalid username or password!")

    if st.button(switch_txt):
        SS.auth_mode = "login" if is_signup else "signup"
        safe_rerun()
    st.markdown("<p style='text-align:center;color:#99a;"
                "font-size:13px;'>Demo: demo / 1234 • "
                "First signup = Owner 👑</p>",
                unsafe_allow_html=True)


# ================= 3) MAIN =================
elif SS.page == "app" and SS.logged_in:

    st.markdown(build_main_css(SS.dark_mode),
                unsafe_allow_html=True)
    DB = load_db()
    owner = FORCE_OWNER or DB.get("owner", "")
    is_owner = (SS.username == owner)

    now = time.time()
    if SS.auto_logout > 0 and SS.last_active > 0:
        if now - SS.last_active > SS.auto_logout * 60:
            SS.logged_in = False
            SS.page = "auth"
            safe_rerun()
    SS.last_active = now

    unread = unread_count(SS.username)
    banned_list = DB.get("banned", [])

    # ---- TOPBAR ----
    if SS.dark_mode:
        dhref, dicon = "?dark=0", "☀️"
    else:
        dhref, dicon = "?dark=1", "🌙"
    nb = ""
    if unread > 0:
        nb = "<span class='nav-dot'>" + str(unread) + \
             "</span>"
    st.markdown(("<div class='ig-topbar'>"
                 "<div class='ig-logo'>HMF Book</div>"
                 "<div class='ig-icons'>"
                 "<a href='?tab=Messages'>✉️</a>"
                 "<a href='?tab=Notifications'>🔔" + nb +
                 "</a><a href='" + dhref + "'>" + dicon +
                 "</a><a href='?tab=Settings'>⚙️</a>"
                 "</div></div>"), unsafe_allow_html=True)

    # ---- VIEW USER ----
    if SS.view_user and SS.view_user != SS.username:
        vu = SS.view_user
        if vu not in DB["users"]:
            SS.view_user = None
            safe_rerun()
        else:
            u = DB["users"][vu]
            mp = [p for p in DB["posts"]
                  if p["user"] == vu]
            tf = DB["friends"].get(vu, [])
            st.markdown("<div class='fb-cover'></div>",
                        unsafe_allow_html=True)
            st.markdown("<div class='fb-av-wrap'>" +
                        avatar_html(vu, u.get("avatar"),
                                    100, border=True) +
                        "</div>", unsafe_allow_html=True)
            st.markdown("<div class='fb-name'>" +
                        esc(u.get("display_name", vu)) +
                        "</div><div class='fb-sub'>" +
                        str(len(tf)) + " friends · " +
                        str(len(mp)) + " posts</div>",
                        unsafe_allow_html=True)
            if is_owner:
                if vu in banned_list:
                    if st.button("✅ Unban (Owner)",
                                 key="vw_unban",
                                 use_container_width=True):
                        db = load_db()
                        db["banned"].remove(vu)
                        save_db(db)
                        safe_rerun()
                else:
                    if st.button("🔨 BAN (Owner)",
                                 key="vw_ban",
                                 use_container_width=True):
                        db = load_db()
                        db["banned"].append(vu)
                        save_db(db)
                        safe_rerun()
            af = vu in DB["friends"].get(SS.username, [])
            sent = any(r["from"] == SS.username and
                       r["to"] == vu
                       for r in DB["friend_requests"])
            v1, v2, v3 = st.columns(3)
            if v1.button("✅ Friends" if af else
                         "Sent" if sent else "➕ Add",
                         key="vw_fr",
                         use_container_width=True):
                if not af and not sent:
                    send_friend_request(SS.username, vu)
                    safe_rerun()
            if v2.button("✉️ Message", key="vw_msg",
                         use_container_width=True):
                SS.msg_view = "chat"
                SS.msg_target = vu
                SS.msg_target_type = "direct"
                SS.current_tab = "Messages"
                SS.view_user = None
                safe_rerun()
            if v3.button("🚩 Report", key="vw_rep",
                         use_container_width=True):
                db = load_db()
                db["reports"].append({
                    "from": SS.username, "user": vu,
                    "reason": "profile", "time": now})
                save_db(db)
                st.success("Report sent to owner!")
            for p in mp[:5]:
                if p.get("type") == "text":
                    st.markdown("<div class='post-ph' "
                                "style='background:" +
                                p.get("grad", "#f0f0f0") +
                                ";height:100px;'>" +
                                esc(p.get("txt", "")) +
                                "</div>",
                                unsafe_allow_html=True)
                elif p.get("type") == "youtube":
                    components.html(
                        '<iframe width="100%" height="170"'
                        ' src="https://www.youtube.com/'
                        'embed/' + p["ref"] + '" frameborder'
                        '="0" allowfullscreen></iframe>',
                        height=180)
            if st.button("← Back", key="vw_back",
                         use_container_width=True):
                SS.view_user = None
                safe_rerun()

    else:
        if SS.view_user == SS.username:
            SS.view_user = None
            SS.current_tab = "Profile"

        # ================= HOME =================
        if SS.current_tab == "Home":

            st.markdown("""
            <div class="stories-container">
                <div class="story-card"><div class="story-ring gray"><div class="story-img">+</div></div><div class="story-name">Your Story</div></div>
                <div class="story-card"><div class="story-ring"><div class="story-img">HJ</div></div><div class="story-name">hoor_jannat</div></div>
                <div class="story-card"><div class="story-ring"><div class="story-img">FM</div></div><div class="story-name">farrukh_m</div></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(("<div class='quick-row'>"
                         "<a href='?tab=Groups' class="
                         "'quick-pill'>👥 Groups</a>"
                         "<a href='?tab=Pages' class="
                         "'quick-pill'>📄 Pages</a>"
                         "<a href='?tab=Events' class="
                         "'quick-pill'>📅 Events</a>"
                         "<a href='?tab=Marketplace' class="
                         "'quick-pill'>🛒 Market</a>"
                         "<a href='?tab=Ludo' class="
                         "'quick-pill'>🎲 Games</a>"
                         "<a href='?tab=Channel' class="
                         "'quick-pill'>📺 Channel</a>"
                         "</div>"), unsafe_allow_html=True)

            visible = [p for p in DB["posts"]
                       if p.get("type") != "reel"
                       and p["user"] not in SS.blocked
                       and p["user"] not in banned_list]
            if SS.feed_sort == "Top Posts":
                visible = sorted(
                    visible,
                    key=lambda x: len(x.get("likes", {})),
                    reverse=True)

            # APPROVED ADS mixed in feed
            ads = [a for a in DB["ads"]
                   if a.get("status") == "active"]

            if SS.clear_cmt:
                SS[SS.clear_cmt] = ""
                SS.clear_cmt = ""

            for idx, p in enumerate(visible):

                st.markdown(("<div class='post-card'>"
                             "<div class='post-header'>" +
                             avatar_html(p["user"],
                                         p.get("avatar"),
                                         36) +
                             "<div class='post-username'>" +
                             esc(p["user"]) +
                             "</div></div></div>"),
                            unsafe_allow_html=True)

                pt = p.get("type", "text")
                if pt == "text":
                    st.markdown("<div class='post-ph' "
                                "style='background:" +
                                p.get("grad", "#f0f0f0") +
                                ";color:#056839;"
                                "font-weight:bold;'>" +
                                esc(p.get("txt", "")) +
                                "</div>",
                                unsafe_allow_html=True)
                elif pt == "youtube":
                    components.html(
                        '<iframe width="100%" height="230"'
                        ' src="https://www.youtube.com/'
                        'embed/' + p["ref"] + '" frameborder'
                        '="0" allowfullscreen></iframe>',
                        height=240)
                elif pt == "image" and \
                        is_local_file(p["ref"]):
                    st.image(p["ref"],
                             use_container_width=True)
                elif pt == "video":
                    st.video(p["ref"])

                liked = SS.username in p.get("likes", {})
                c1, c2, c3, c4 = st.columns(4)
                ic = "❤️" if liked else "🤍"
                if c1.button(ic, key="lk_" + p["id"],
                             use_container_width=True):
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
                if c2.button("💬", key="cm_" + p["id"],
                             use_container_width=True):
                    st.info("Comment box below.")
                if c3.button("👤", key="vu_" + p["id"],
                             use_container_width=True):
                    SS.view_user = p["user"]
                    safe_rerun()
                if c4.button("🚫", key="bl_" + p["id"],
                             use_container_width=True):
                    db = load_db()
                    rec = db["users"].get(SS.username, {})
                    bl = rec.setdefault("blocked", [])
                    if p["user"] not in bl:
                        bl.append(p["user"])
                        save_db(db)
                        SS.blocked = list(bl)
                    safe_rerun()

                n = len(p.get("likes", {}))
                st.markdown("<p class='likes-txt'>" +
                            str(n) + " likes</p><p class=" +
                            "'post-details'><b>" +
                            esc(p["user"]) + "</b> " +
                            esc(p.get("cap", "")) + "</p>",
                            unsafe_allow_html=True)

                cm = st.text_input("comment",
                                   key="cmt_" + p["id"],
                                   placeholder=
                                   "Add a comment...",
                                   label_visibility=
                                   "collapsed")
                if st.button("Post Comment",
                             key="pc_" + p["id"]):
                    if cm.strip():
                        db = load_db()
                        for post in db["posts"]:
                            if post["id"] == p["id"]:
                                post.setdefault(
                                    "comments",
                                    []).append({
                                    "user": SS.username,
                                    "text": cm})
                                break
                        save_db(db)
                        SS.clear_cmt = "cmt_" + p["id"]
                        safe_rerun()

                for c in p.get("comments", []):
                    st.markdown("<p class='post-details' "
                                "style='color:#6b7280;'>"
                                "<b>" + esc(c["user"]) +
                                "</b> " + esc(c["text"]) +
                                "</p>",
                                unsafe_allow_html=True)

                # inject an ad after every 3 posts
                if ads and (idx + 1) % 3 == 0:
                    ad = ads[(idx // 3) % len(ads)]
                    ad_html = ("<div class='ad-card'>"
                               "<span class='ad-tag'>📢 "
                               "SPONSORED</span><br>"
                               "<b style='font-size:15px;'>" +
                               esc(ad["title"]) + "</b><br>"
                               "<span style='font-size:13px;"
                               "color:#6b7280;'>" +
                               esc(ad.get("text", "")) +
                               "</span><br>"
                               "<a href='" +
                               esc(ad.get("link", "#")) +
                               "' target='_blank' style="
                               "'color:#00B074;font-weight:"
                               "700;font-size:13px;'>🔗 " +
                               "Learn More</a></div>")
                    st.markdown(ad_html,
                                unsafe_allow_html=True)

        # ================= GROUPS (FB) =================
        elif SS.current_tab == "Groups":

            if SS.open_group:
                db = load_db()
                grp = None
                for g in db["groups"]:
                    if g["id"] == SS.open_group:
                        grp = g
                        break
                if grp is None:
                    SS.open_group = ""
                    safe_rerun()
                else:
                    if st.button("← Back to Groups",
                                 key="g_back"):
                        SS.open_group = ""
                        safe_rerun()

                    st.markdown("<div class='grp-card'>"
                                "<div class='grp-cover'>"
                                "</div><div class="
                                "'grp-name'>👥 " +
                                esc(grp["name"]) +
                                "</div><div class="
                                "'grp-sub'>" +
                                str(len(grp["members"])) +
                                " members · " +
                                grp["privacy"] +
                                "</div></div>",
                                unsafe_allow_html=True)

                    # join/leave
                    is_member = SS.username in \
                        grp["members"]
                    is_admin = grp["createdBy"] == \
                        SS.username
                    if grp["privacy"] == "public":
                        lbl = "✅ Leave" if is_member \
                            else "➕ Join Group"
                        if st.button(lbl, key="g_join",
                                     use_container_width
                                     =True):
                            db = load_db()
                            for g in db["groups"]:
                                if g["id"] == grp["id"]:
                                    if is_member:
                                        g["members"].remove(
                                            SS.username)
                                    else:
                                        g["members"].append(
                                            SS.username)
                                    break
                            save_db(db)
                            safe_rerun()
                    else:
                        if not is_member:
                            pending = SS.username in \
                                grp.get("requests", [])
                            if st.button(
                                    "Request Sent" if
                                    pending else
                                    "➕ Request to Join",
                                    key="g_req",
                                    use_container_width
                                    =True):
                                if not pending:
                                    db = load_db()
                                    for g in db["groups"]:
                                        if g["id"] == \
                                                grp["id"]:
                                            g.setdefault(
                                                "requests",
                                                []).append(
                                                SS.username)
                                            break
                                    save_db(db)
                                    safe_rerun()
                        else:
                            st.success("You are a member!")

                    # admin: approve requests
                    if is_admin and grp.get("requests"):
                        st.markdown("**Pending Requests:**")
                        for req in grp["requests"]:
                            rc1, rc2 = st.columns(2)
                            rc1.markdown("👤 @" + esc(req))
                            if rc2.button("✅ Approve",
                                          key="gapp_" + req,
                                          use_container_width
                                          =True):
                                db = load_db()
                                for g in db["groups"]:
                                    if g["id"] == grp["id"]:
                                        g["requests"]\
                                            .remove(req)
                                        g["members"]\
                                            .append(req)
                                        break
                                save_db(db)
                                add_notification(
                                    req, "✅ Aapko group '" +
                                    grp["name"] +
                                    "' mein add kiya!")
                                safe_rerun()

                    # group feed (posts with groupId)
                    gposts = [p for p in db["posts"]
                              if p.get("groupId") ==
                              grp["id"]]
                    if is_member:
                        gtxt = st.text_input(
                            "Post to group...",
                            key="gpost_txt")
                        if st.button("🚀 Post to Group",
                                     key="gpost_btn",
                                     use_container_width
                                     =True):
                            if gtxt.strip():
                                db = load_db()
                                db["posts"].insert(0, {
                                    "id": uuid.uuid4()
                                    .hex[:8],
                                    "user": SS.username,
                                    "type": "text",
                                    "grad": random.choice(
                                        GRADS),
                                    "txt": esc(gtxt)[:40],
                                    "cap": gtxt.strip(),
                                    "groupId": grp["id"],
                                    "likes": {},
                                    "comments": []})
                                save_db(db)
                                for mm in grp["members"]:
                                    if mm != SS.username:
                                        add_notification(
                                            mm, "👥 '" +
                                            grp["name"] +
                                            "' new post by @" +
                                            SS.username)
                                safe_rerun()

                    if not gposts:
                        st.caption("No posts yet.")
                    for p in gposts:
                        st.markdown(("<div class="
                                     "'grp-card'><b>@" +
                                     esc(p["user"]) +
                                     "</b><br>" +
                                     esc(p.get("cap", "")) +
                                     "<br><span style="
                                     "'font-size:12px;"
                                     "color:#9ca3af;'>" +
                                     str(len(p.get(
                                         "likes", {}))) +
                                     " likes</span>"
                                     "</div>"),
                                    unsafe_allow_html=True)

            else:
                st.markdown('<div class="panel-header">👥 '
                            'Groups</div>',
                            unsafe_allow_html=True)

                with st.expander("➕ Create Group"):
                    gname = st.text_input("Group name",
                                          key="ng_name")
                    gdesc = st.text_input(
                        "Description", key="ng_desc")
                    gpriv = st.selectbox("Privacy",
                                         ["public",
                                          "private"],
                                         key="ng_priv")
                    if st.button("Create Group",
                                 key="ng_btn",
                                 use_container_width=True):
                        if gname.strip():
                            db = load_db()
                            db["groups"].append({
                                "id": uuid.uuid4()
                                .hex[:8],
                                "name": gname.strip(),
                                "description": gdesc,
                                "privacy": gpriv,
                                "createdBy":
                                SS.username,
                                "members":
                                [SS.username],
                                "requests": []})
                            save_db(db)
                            st.success("Group created!")
                            safe_rerun()
                        else:
                            st.warning("Naam likhein!")

                st.markdown("**Discover Groups:**")
                if not DB["groups"]:
                    st.caption("No groups yet.")
                for g in DB["groups"]:
                    if g["privacy"] == "private" and \
                            SS.username not in \
                            g["members"]:
                        mem = "🔒 Private"
                    else:
                        mem = str(len(g["members"])) + \
                              " members"
                    st.markdown("<div class='grp-card'>"
                                "<div class='grp-cover'>"
                                "</div><div class="
                                "'grp-name'>" +
                                esc(g["name"]) +
                                "</div><div class="
                                "'grp-sub'>" + mem +
                                "</div></div>",
                                unsafe_allow_html=True)
                    if g["privacy"] == "public" or \
                            SS.username in g["members"]:
                        if st.button("Open",
                                     key="gop_" + g["id"],
                                     use_container_width
                                     =True):
                            SS.open_group = g["id"]
                            safe_rerun()

        # ================= PAGES (FB) =================
        elif SS.current_tab == "Pages":

            if SS.open_page:
                db = load_db()
                pg = None
                for p in db["pages"]:
                    if p["id"] == SS.open_page:
                        pg = p
                        break
                if pg is None:
                    SS.open_page = ""
                    safe_rerun()
                else:
                    if st.button("← Back to Pages",
                                 key="p_back"):
                        SS.open_page = ""
                        safe_rerun()

                    st.markdown("<div class='fb-cover'>"
                                "</div>",
                                unsafe_allow_html=True)
                    st.markdown("<div class='fb-name'>📄 "
                                + esc(pg["name"]) +
                                "</div><div class="
                                "'fb-sub'>" +
                                esc(pg.get("category",
                                           "")) + " · " +
                                str(len(pg.get(
                                    "followers", []))) +
                                " followers</div>",
                                unsafe_allow_html=True)
                    st.caption(pg.get("description", ""))

                    is_own = pg["owner"] == SS.username
                    is_fol = SS.username in \
                        pg.get("followers", [])

                    if is_own:
                        st.success("👤 You manage this page")
                        ptxt = st.text_input(
                            "Post as " + pg["name"],
                            key="ppost_txt")
                        if st.button("🚀 Post as Page",
                                     key="ppost_btn",
                                     use_container_width
                                     =True):
                            if ptxt.strip():
                                db = load_db()
                                db["posts"].insert(0, {
                                    "id": uuid.uuid4()
                                    .hex[:8],
                                    "user": pg["name"],
                                    "type": "text",
                                    "grad": random
                                    .choice(GRADS),
                                    "txt": esc(ptxt)[:40],
                                    "cap": ptxt.strip(),
                                    "pageId": pg["id"],
                                    "page": True,
                                    "likes": {},
                                    "comments": []})
                                save_db(db)
                                for f in pg.get(
                                        "followers", []):
                                    add_notification(
                                        f, "📄 '" +
                                        pg["name"] +
                                        "' posted!")
                                safe_rerun()
                    else:
                        lbl = "❤️ Following" if is_fol \
                            else "➕ Follow Page"
                        if st.button(lbl, key="p_fol",
                                     use_container_width
                                     =True):
                            db = load_db()
                            for p in db["pages"]:
                                if p["id"] == pg["id"]:
                                    fl = p.setdefault(
                                        "followers", [])
                                    if is_fol:
                                        fl.remove(
                                            SS.username)
                                    else:
                                        fl.append(
                                            SS.username)
                                    break
                            save_db(db)
                            safe_rerun()

                    pposts = [p for p in db["posts"]
                              if p.get("pageId") == pg["id"]]
                    if not pposts:
                        st.caption("No posts yet.")
                    for p in pposts:
                        st.markdown("<div class='grp-card'>"
                                    "<b>📄 " +
                                    esc(p["user"]) +
                                    "</b><br>" +
                                    esc(p.get("cap", "")) +
                                    "</div>",
                                    unsafe_allow_html=True)
            else:
                st.markdown('<div class="panel-header">📄 '
                            'Pages</div>',
                            unsafe_allow_html=True)

                with st.expander("➕ Create Page"):
                    pname = st.text_input("Page name",
                                          key="np_name")
                    pcat = st.text_input(
                        "Category (Brand, Shop...)",
                        key="np_cat")
                    pdesc = st.text_input(
                        "Description", key="np_desc")
                    if st.button("Create Page", key="np_btn",
                                 use_container_width=True):
                        if pname.strip():
                            db = load_db()
                            db["pages"].append({
                                "id": uuid.uuid4()
                                .hex[:8],
                                "name": pname.strip(),
                                "category": pcat,
                                "owner": SS.username,
                                "description": pdesc,
                                "followers": []})
                            save_db(db)
                            st.success("Page created!")
                            safe_rerun()
                        else:
                            st.warning("Naam likhein!")

                st.markdown("**Discover Pages:**")
                for pg in DB["pages"]:
                    st.markdown("<div class='grp-card'>"
                                "<div class='grp-name'>📄 "
                                + esc(pg["name"]) +
                                "</div><div class="
                                "'grp-sub'>" +
                                esc(pg.get("category", "")) +
                                " · " +
                                str(len(pg.get("followers",
                                               []))) +
                                " followers</div></div>",
                                unsafe_allow_html=True)
                    if st.button("Open", key="pop_" + pg["id"],
                                 use_container_width=True):
                        SS.open_page = pg["id"]
                        safe_rerun()

        # ================= EVENTS (FB) =================
        elif SS.current_tab == "Events":

            if SS.open_event:
                db = load_db()
                ev = None
                for e in db["events"]:
                    if e["id"] == SS.open_event:
                        ev = e
                        break
                if ev is None:
                    SS.open_event = ""
                    safe_rerun()
                else:
                    if st.button("← Back to Events",
                                 key="e_back"):
                        SS.open_event = ""
                        safe_rerun()

                    st.markdown("<div class='grp-card'>"
                                "<div class='grp-cover'>"
                                "</div><div class="
                                "'grp-name'>📅 " +
                                esc(ev["title"]) +
                                "</div><div class="
                                "'grp-sub'>📍 " +
                                esc(ev.get("location",
                                           "")) + " · " +
                                esc(ev.get("date", "")) +
                                " " +
                                esc(ev.get("time", "")) +
                                "</div></div>",
                                unsafe_allow_html=True)
                    st.caption(ev.get("description", ""))
                    st.caption("Host: @" + ev["host"])

                    going = sum(1 for r in ev.get("rsvps", [])
                                if r["status"] == "going")
                    inter = sum(1 for r in
                                ev.get("rsvps", [])
                                if r["status"] ==
                                "interested")
                    st.markdown("✅ **" + str(going) +
                                " going** · 🌟 " +
                                str(inter) + " interested")

                    e1, e2, e3 = st.columns(3)
                    cur = rsvp_status(ev, SS.username)
                    if e1.button("✅ Going" if cur ==
                                 "going" else "Going",
                                 key="ev_go",
                                 use_container_width=True):
                        set_rsvp(ev["id"], SS.username,
                                 "going")
                        safe_rerun()
                    if e2.button("🌟 Interested" if cur ==
                                 "interested" else
                                 "Interested",
                                 key="ev_in",
                                 use_container_width=True):
                        set_rsvp(ev["id"], SS.username,
                                 "interested")
                        safe_rerun()
                    if e3.button("❌ Not Going" if cur ==
                                 "not_going" else
                                 "Not Going",
                                 key="ev_no",
                                 use_container_width=True):
                        set_rsvp(ev["id"], SS.username,
                                 "not_going")
                        safe_rerun()
            else:
                st.markdown('<div class="panel-header">📅 '
                            'Events</div>',
                            unsafe_allow_html=True)

                with st.expander("➕ Create Event"):
                    etitle = st.text_input("Title",
                                           key="ne_title")
                    edesc = st.text_area(
                        "Description", key="ne_desc",
                        height=60)
                    eloc = st.text_input("Location",
                                         key="ne_loc")
                    edate = st.date_input("Date",
                                          key="ne_date")
                    etime = st.text_input("Time (6:00 PM)",
                                          key="ne_time")
                    if st.button("Create Event",
                                 key="ne_btn",
                                 use_container_width=True):
                        if etitle.strip():
                            db = load_db()
                            db["events"].append({
                                "id": uuid.uuid4()
                                .hex[:8],
                                "title": etitle.strip(),
                                "description": edesc,
                                "host": SS.username,
                                "location": eloc,
                                "date": str(edate),
                                "time": etime,
                                "rsvps": []})
                            save_db(db)
                            st.success("Event created!")
                            safe_rerun()
                        else:
                            st.warning("Title likhein!")

                st.markdown("**Upcoming Events:**")
                if not DB["events"]:
                    st.caption("No events yet.")
                for ev in DB["events"]:
                    st.markdown("<div class='grp-card'>"
                                "<div style='display:flex;"
                                "gap:10px;align-items:"
                                "center;'><div class="
                                "'ev-date'>📅<br>" +
                                esc(ev.get("date", "")[:5]) +
                                "</div><div><div class="
                                "'grp-name'>" +
                                esc(ev["title"]) +
                                "</div><div class="
                                "'grp-sub'>📍 " +
                                esc(ev.get("location",
                                           "")) +
                                "</div></div></div>"
                                "</div>",
                                unsafe_allow_html=True)
                    if st.button("Open",
                                 key="eop_" + ev["id"],
                                 use_container_width=True):
                        SS.open_event = ev["id"]
                        safe_rerun()

        # ================= MARKETPLACE =================
        elif SS.current_tab == "Marketplace":

            if SS.open_listing:
                db = load_db()
                ls = None
                for l in db["listings"]:
                    if l["id"] == SS.open_listing:
                        ls = l
                        break
                if ls is None:
                    SS.open_listing = ""
                    safe_rerun()
                else:
                    if st.button("← Back to Marketplace",
                                 key="m_back"):
                        SS.open_listing = ""
                        safe_rerun()

                    st.markdown('<div class="panel-header">'
                                '🛒 ' +
                                esc(ls["title"]) +
                                '</div>',
                                unsafe_allow_html=True)
                    if ls.get("image") and \
                            is_local_file(ls["image"]):
                        st.image(ls["image"],
                                 use_container_width=True)
                    st.markdown("<p class='mk-price' style="
                                "'font-size:24px;'>PKR " +
                                str(ls["price"]) +
                                "</p>", unsafe_allow_html=True)
                    st.write("**Category:** " +
                             esc(ls.get("category", "")))
                    st.write("**Location:** " +
                             esc(ls.get("location", "")))
                    st.write(ls.get("description", ""))

                    if ls["status"] == "sold":
                        st.error("❌ SOLD")
                    else:
                        st.success("✅ Available")

                    if ls["seller"] != SS.username:
                        if st.button("✉️ Message Seller",
                                     key="ms_btn",
                                     use_container_width
                                     =True):
                            SS.msg_view = "chat"
                            SS.msg_target = ls["seller"]
                            SS.msg_target_type = "direct"
                            SS.current_tab = "Messages"
                            send_chat_message(
                                False, "", ls["seller"],
                                "🛒 Hi! Interested in '" +
                                ls["title"] + "'")
                            SS.open_listing = ""
                            safe_rerun()
                    else:
                        if ls["status"] != "sold":
                            if st.button("✅ Mark as Sold",
                                         key="ms_sold",
                                         use_container_width
                                         =True):
                                db = load_db()
                                for l in db["listings"]:
                                    if l["id"] == ls["id"]:
                                        l["status"] = "sold"
                                        break
                                save_db(db)
                                safe_rerun()
            else:
                st.markdown('<div class="panel-header">🛒 '
                            'Marketplace</div>',
                            unsafe_allow_html=True)

                with st.expander("➕ Sell Something"):
                    sl_title = st.text_input("Title",
                                             key="sl_title")
                    sl_desc = st.text_area(
                        "Description", key="sl_desc",
                        height=60)
                    sl_price = st.number_input(
                        "Price (PKR)", min_value=0,
                        key="sl_price")
                    sl_cat = st.selectbox(
                        "Category",
                        ["Electronics", "Clothes",
                         "Furniture", "Mobiles",
                         "Vehicles", "Other"],
                        key="sl_cat")
                    sl_loc = st.text_input("Location",
                                           key="sl_loc")
                    sl_img = st.file_uploader(
                        "Photo", type=["png", "jpg",
                                       "jpeg", "webp"],
                        key="sl_img")
                    if st.button("🚀 Publish Listing",
                                 key="sl_btn",
                                 use_container_width=True):
                        if sl_title.strip():
                            img_path = None
                            if sl_img is not None:
                                img_path = save_upload(
                                    sl_img)
                            db = load_db()
                            db["listings"].insert(0, {
                                "id": uuid.uuid4()
                                .hex[:8],
                                "seller": SS.username,
                                "title": sl_title.strip(),
                                "description": sl_desc,
                                "price": int(sl_price),
                                "category": sl_cat,
                                "image": img_path,
                                "location": sl_loc,
                                "status": "available"})
                            save_db(db)
                            st.success("Listed for sale!")
                            safe_rerun()
                        else:
                            st.warning("Title likhein!")

                mfilter = st.text_input(
                    "🔍 Search listings...",
                    key="mk_search")
                cat_filter = st.selectbox(
                    "Category", ["All", "Electronics",
                                 "Clothes", "Furniture",
                                 "Mobiles", "Vehicles",
                                 "Other"],
                    key="mk_cat")

                items = [l for l in DB["listings"]
                         if (cat_filter == "All" or
                             l.get("category") ==
                             cat_filter) and
                         (not mfilter or mfilter.lower()
                          in l["title"].lower())]

                if not items:
                    st.caption("No listings found.")
                st.markdown("<div class='mk-grid'>",
                            unsafe_allow_html=True)
                st.markdown("</div>",
                            unsafe_allow_html=True)
                for l in items:
                    st.markdown(("<div class='mk-card'>"
                                 "<b>" +
                                 esc(l["title"]) +
                                 "</b><br><span class="
                                 "'mk-price'>PKR " +
                                 str(l["price"]) +
                                 "</span><br><span style="
                                 "'font-size:11px;color:"
                                 "#9ca3af;'>" +
                                 esc(l.get("category",
                                           "")) + " · @" +
                                 esc(l["seller"]) +
                                 "</span><br>" +
                                 ("✅" if l["status"] ==
                                  "available" else
                                  "❌ SOLD") +
                                 "</div>"),
                                unsafe_allow_html=True)
                    if st.button("View",
                                 key="lop_" + l["id"],
                                 use_container_width=True):
                        SS.open_listing = l["id"]
                        safe_rerun()

        # ================= ADS MANAGER =================
        elif SS.current_tab == "Ads":

            st.markdown('<div class="panel-header">📢 Ads '
                        'Manager</div>',
                        unsafe_allow_html=True)

            with st.expander("➕ Create Ad"):
                ad_title = st.text_input("Ad title",
                                         key="ad_title")
                ad_text = st.text_area("Ad text",
                                       key="ad_text",
                                       height=60)
                ad_link = st.text_input(
                    "Link URL (https://...)",
                    key="ad_link")
                ad_budget = st.number_input(
                    "Budget (coins)", min_value=10,
                    value=50, key="ad_budget")
                ad_img = st.file_uploader(
                    "Ad image", type=["png", "jpg",
                                      "jpeg", "webp"],
                    key="ad_img")
                if st.button("🚀 Submit Ad",
                             key="ad_btn",
                             use_container_width=True):
                    if ad_title.strip():
                        db = load_db()
                        u = db["users"].get(SS.username)
                        cost = int(ad_budget)
                        if u is not None and \
                                u.get("coins", 0) >= cost:
                            u["coins"] -= cost
                            img_path = None
                            if ad_img is not None:
                                img_path = save_upload(
                                    ad_img)
                            db["ads"].append({
                                "id": uuid.uuid4()
                                .hex[:8],
                                "advertiser":
                                SS.username,
                                "title":
                                ad_title.strip(),
                                "text": ad_text,
                                "link": ad_link,
                                "budget": cost,
                                "image": img_path,
                                "status": "pending",
                                "impressions": 0})
                            save_db(db)
                            if owner:
                                add_notification(
                                    owner, "📢 New ad "
                                    "pending approval "
                                    "by @" +
                                    SS.username)
                            st.success("Ad submitted! "
                                       "Owner approval "
                                       "ke baad feed "
                                       "mein dikhegi. " +
                                       str(cost) +
                                       " coins kat "
                                       "gaye.")
                            safe_rerun()
                        else:
                            st.warning("Insufficient "
                                       "coins!")
                    else:
                        st.warning("Title likhein!")

            st.markdown("**Your Ads:**")
            my_ads = [a for a in DB["ads"]
                      if a["advertiser"] == SS.username]
            if not my_ads:
                st.caption("No ads yet.")
            for a in my_ads:
                if a["status"] == "active":
                    tag = "🟢 ACTIVE"
                elif a["status"] == "pending":
                    tag = "🟡 PENDING"
                elif a["status"] == "rejected":
                    tag = "🔴 REJECTED"
                else:
                    tag = "⚫ ENDED"
                st.markdown("<div class='ad-card'>"
                            "<span class='ad-tag'>" + tag +
                            "</span><br><b>" +
                            esc(a["title"]) + "</b><br>"
                            "<span style='font-size:12px;"
                            "color:#6b7280;'>Budget: " +
                            str(a["budget"]) +
                            " coins</span></div>",
                            unsafe_allow_html=True)

            if is_owner:
                st.markdown("---")
                st.markdown("### 🛡️ Owner: Approve Ads")
                pending = [a for a in DB["ads"]
                           if a["status"] == "pending"]
                if not pending:
                    st.caption("No pending ads.")
                for i, a in enumerate(pending):
                    ac1, ac2, ac3 = st.columns(
                        [0.5, 0.25, 0.25])
                    ac1.markdown("📢 **" +
                                 esc(a["title"]) +
                                 "** by @" +
                                 a["advertiser"])
                    if ac2.button("✅ Approve",
                                  key="adapp_" + str(i),
                                  use_container_width=True):
                        db = load_db()
                        for ad in db["ads"]:
                            if ad["id"] == a["id"]:
                                ad["status"] = "active"
                                break
                        save_db(db)
                        add_notification(
                            a["advertiser"],
                            "📢 Aapki ad approve ho "
                            "gayi!")
                        safe_rerun()
                    if ac3.button("❌ Reject",
                                  key="adrej_" + str(i),
                                  use_container_width=True):
                        db = load_db()
                        for ad in db["ads"]:
                            if ad["id"] == a["id"]:
                                ad["status"] = "rejected"
                                u = db["users"].get(
                                    ad["advertiser"])
                                if u is not None:
                                    u["coins"] += \
                                        ad["budget"]
                                break
                        save_db(db)
                        add_notification(
                            a["advertiser"],
                            "🔴 Ad rejected - coins "
                            "wapas.")
                        safe_rerun()

        # ================= SEARCH =================
        elif SS.current_tab == "Search":

            st.markdown('<div class="panel-header">🔍 '
                        'Search</div>',
                        unsafe_allow_html=True)

            mode = st.radio("Search in:",
                            ["👤 Users", "🖼️ Photos",
                             "🎬 Videos", "🌐 Google"],
                            horizontal=True,
                            key="search_mode")
            query = st.text_input(
                "Search...", key="search_input",
                placeholder="Type anything...")

            if query.strip():
                q = query.strip().lower()
                if mode == "👤 Users":
                    res = [(un, ud) for un, ud in
                           DB["users"].items()
                           if q in un.lower()]
                    if not res:
                        st.info("❌ No users!")
                    for un, ud in res:
                        st.markdown("<div class="
                                    "'search-row'>" +
                                    avatar_html(
                                        un,
                                        ud.get("avatar"),
                                        44) +
                                    "<div><b>@" + un +
                                    "</b></div></div>",
                                    unsafe_allow_html=True)
                        if st.button("View",
                                     key="sr_" + un,
                                     use_container_width
                                     =True):
                            SS.view_user = un
                            safe_rerun()
                elif mode in ("🖼️ Photos", "🎬 Videos"):
                    types = ("image",) if mode == \
                        "🖼️ Photos" else \
                        ("youtube", "video", "reel")
                    found = [p for p in DB["posts"]
                             if p.get("type") in types and
                             q in (p.get("cap", "") or
                                   "").lower()]
                    if not found:
                        st.info("App mein nahi mila - "
                                "Google se dekhein:")
                        gq = quote_plus(query.strip())
                        st.markdown(
                            "<div class='g-links'>"
                            "<a class='g-link' href="
                            "'https://www.google.com/"
                            "search?tbm=isch&q=" + gq +
                            "'>🖼️ Google Images</a>"
                            "<a class='g-link' href="
                            "'https://www.youtube.com/"
                            "results?search_query=" + gq +
                            "'>🎬 YouTube</a></div>",
                            unsafe_allow_html=True)
                    for p in found:
                        st.caption("@" + p["user"] + " - " +
                                   p.get("cap", ""))
                        if p.get("type") == "image" and \
                                is_local_file(p["ref"]):
                            st.image(p["ref"],
                                     use_container_width
                                     =True)
                        elif p.get("type") == "youtube":
                            components.html(
                                '<iframe width="100%" '
                                'height="190" src='
                                '"https://www.youtube.'
                                'com/embed/' + p["ref"] +
                                '" frameborder="0" '
                                'allowfullscreen>'
                                '</iframe>', height=200)
                else:
                    gq = quote_plus(query.strip())
                    st.markdown("<div class='g-links'>"
                                "<a class='g-link' href="
                                "'https://www.google.com/"
                                "search?tbm=isch&q=" + gq +
                                "'>🖼️ Google Images</a>"
                                "<a class='g-link' href="
                                "'https://www.youtube.com/"
                                "results?search_query=" +
                                gq + "'>🎬 YouTube</a>"
                                "<a class='g-link' href="
                                "'https://www.google.com/"
                                "search?q=" + gq +
                                "'>🔍 Google</a></div>",
                                unsafe_allow_html=True)
            else:
                st.caption("👆 Kuch bhi search karein!")

        # ================= FRIENDS =================
        elif SS.current_tab == "Friends":

            st.markdown('<div class="panel-header">👥 '
                        'Friends</div>',
                        unsafe_allow_html=True)
            db = load_db()
            in_fr = [r for r in db["friend_requests"]
                     if r["to"] == SS.username]
            friends = db["friends"].get(SS.username, [])

            st.markdown("### 📨 Requests (" +
                        str(len(in_fr)) + ")")
            for i, r in enumerate(in_fr):
                f = r["from"]
                st.markdown("<div class='fr-row'>" +
                            avatar_html(f, None, 40) +
                            "<div><b>@" + esc(f) +
                            "</b></div></div>",
                            unsafe_allow_html=True)
                f1, f2, f3 = st.columns(3)
                if f2.button("✅", key="fa_" + str(i),
                             use_container_width=True):
                    accept_friend(SS.username, f)
                    safe_rerun()
                if f3.button("❌", key="frj_" + str(i),
                             use_container_width=True):
                    reject_friend(SS.username, f)
                    safe_rerun()
                if f1.button("👤", key="fv_" + str(i),
                             use_container_width=True):
                    SS.view_user = f
                    safe_rerun()

            st.markdown("### 🧑‍🤝‍🧑 Friends (" +
                        str(len(friends)) + ")")
            for f in friends:
                st.markdown("<div class='fr-row'>" +
                            avatar_html(f, None, 40) +
                            "<div><b>@" + esc(f) +
                            "</b></div></div>",
                            unsafe_allow_html=True)
                f1, f2, f3 = st.columns(3)
                if f1.button("👤", key="flv_" + f,
                             use_container_width=True):
                    SS.view_user = f
                    safe_rerun()
                if f2.button("✉️", key="flm_" + f,
                             use_container_width=True):
                    SS.msg_view = "chat"
                    SS.msg_target = f
                    SS.msg_target_type = "direct"
                    SS.current_tab = "Messages"
                    safe_rerun()
                if f3.button("📞", key="flc_" + f,
                             use_container_width=True):
                    safe_toast("Call sent (demo)!")
            if not friends:
                st.caption("No friends yet.")

            st.markdown("### 🌟 People You May Know")
            sugg = [un for un in db["users"]
                    if un != SS.username
                    and un not in friends
                    and un not in SS.blocked
                    and un not in banned_list
                    and not any(r["from"] == SS.username
                                and r["to"] == un
                                for r in db[
                                    "friend_requests"])]
            for un in sugg:
                st.markdown("<div class='fr-row'>" +
                            avatar_html(un, None, 40) +
                            "<div><b>@" + esc(un) +
                            "</b></div></div>",
                            unsafe_allow_html=True)
                s1, s2 = st.columns(2)
                if s1.button("➕ Add", key="sg_" + un,
                             use_container_width=True):
                    send_friend_request(SS.username, un)
                    safe_rerun()
                if s2.button("👤", key="sgv_" + un,
                             use_container_width=True):
                    SS.view_user = un
                    safe_rerun()
            if not sugg:
                st.caption("No suggestions.")

        # ================= CHANNEL =================
        elif SS.current_tab == "Channel":

            st.markdown("<div class='channel-banner'>"
                        "<h2>📺 " + CHANNEL_NAME +
                        "</h2><p>" + CHANNEL_HANDLE +
                        "</p></div>",
                        unsafe_allow_html=True)
            st.markdown("[🔗 Open on YouTube](" +
                        CHANNEL_URL + ")")
            with st.expander("➕ Add Video"):
                yl = st.text_input(
                    "Paste YouTube link", key="ch_link")
                if st.button("Add", key="ch_add",
                             use_container_width=True):
                    vid = parse_youtube_id(yl)
                    if vid:
                        db = load_db()
                        db["posts"].insert(0, {
                            "id": uuid.uuid4().hex[:8],
                            "user": SS.username,
                            "type": "youtube", "ref": vid,
                            "cap": "From " + CHANNEL_NAME,
                            "likes": {}, "comments": [],
                            "channel": True})
                        save_db(db)
                        safe_rerun()
            for p in [x for x in DB["posts"]
                      if x.get("channel")]:
                components.html(
                    '<iframe width="100%" height="190" '
                    'src="https://www.youtube.com/embed/'
                    + p["ref"] + '" frameborder="0" '
                    'allowfullscreen></iframe>',
                    height=200)

        # ================= REELS =================
        elif SS.current_tab == "Reels":
            st.markdown('<div class="panel-header">🎬 '
                        'Reels</div>',
                        unsafe_allow_html=True)
            reels = [p for p in DB["posts"]
                     if p.get("type") in ("reel", "video")]
            if not reels:
                st.info("No reels yet!")
            for r in reversed(reels):
                st.caption("@" + r["user"])
                st.video(r["ref"])

        # ================= CREATE =================
        elif SS.current_tab == "Create":
            st.markdown('<div class="panel-header">➕ '
                        'Create</div>',
                        unsafe_allow_html=True)
            kind = st.radio("Type:",
                            ["Photo", "Video",
                             "Camera 🎨",
                             "YouTube Link"],
                            horizontal=True,
                            key="create_kind")
            cap = st.text_input("Caption", key="up_cap")

            if kind == "Camera 🎨":
                filt = st.selectbox("Filter:", FILTER_NAMES,
                                    key="cam_filter")
                cam = st.camera_input("📸 Photo",
                                      key="up_cam")
                fi = None
                if cam is not None:
                    try:
                        pil = Image.open(cam)
                        fi = apply_filter(pil, filt)
                        buf = io.BytesIO()
                        fi.save(buf, format="PNG")
                        st.image(buf.getvalue())
                    except Exception:
                        pass
                if st.button("🚀 Publish", key="up2",
                             use_container_width=True):
                    if fi is None:
                        st.warning("Photo lein!")
                    else:
                        db = load_db()
                        db["posts"].insert(0, {
                            "id": uuid.uuid4().hex[:8],
                            "user": SS.username,
                            "type": "image",
                            "ref": save_pil(fi),
                            "cap": cap + " [" + filt + "]",
                            "likes": {}, "comments": []})
                        save_db(db)
                        SS.current_tab = "Home"
                        safe_rerun()
            elif kind == "YouTube Link":
                yl = st.text_input("Link", key="up_yt")
                if st.button("🚀 Publish", key="up1",
                             use_container_width=True):
                    vid = parse_youtube_id(yl)
                    if not vid:
                        st.error("Invalid link!")
                    else:
                        db = load_db()
                        db["posts"].insert(0, {
                            "id": uuid.uuid4().hex[:8],
                            "user": SS.username,
                            "type": "youtube",
                            "ref": vid,
                            "cap": cap or "Video",
                            "likes": {}, "comments": []})
                        save_db(db)
                        SS.current_tab = "Home"
                        safe_rerun()
            else:
                if kind == "Photo":
                    f = st.file_uploader(
                        "Photo", type=["png", "jpg",
                                      "jpeg", "webp"],
                        key="up_photo")
                else:
                    f = st.file_uploader(
                        "Video", type=["mp4", "mov",
                                      "webm"],
                        key="up_video")
                if st.button("🚀 Publish", key="up3",
                             use_container_width=True):
                    if f is None:
                        st.warning("File choose karein!")
                    else:
                        db = load_db()
                        db["posts"].insert(0, {
                            "id": uuid.uuid4().hex[:8],
                            "user": SS.username,
                            "type": "video" if kind ==
                            "Video" else "image",
                            "ref": save_upload(f),
                            "cap": cap, "likes": {},
                            "comments": []})
                        save_db(db)
                        SS.current_tab = "Home"
                        safe_rerun()

        # ================= MESSAGES =================
        elif SS.current_tab == "Messages":

            if HAS_REFRESH:
                st_autorefresh(interval=4000,
                               key="msg_ref")
            db = load_db()

            if SS.msg_view == "chat":
                tgt = SS.msg_target
                is_group = (SS.msg_target_type == "group")
                valid = tgt in db["users"]
                grp = None
                if is_group:
                    for g in db["groups"]:
                        if g["id"] == tgt:
                            grp = g
                            valid = True
                            break
                    else:
                        valid = False
                if not valid:
                    SS.msg_view = "list"
                    safe_rerun()
                else:
                    hb, ha, hi = st.columns(
                        [0.12, 0.15, 0.73])
                    if hb.button("←", key="ch_back"):
                        SS.msg_view = "list"
                        safe_rerun()
                    if is_group:
                        ha.markdown(avatar_html(
                            grp["name"], None, 40),
                            unsafe_allow_html=True)
                        hi.markdown("<b>" +
                                    esc(grp["name"]) +
                                    "</b>",
                                    unsafe_allow_html=True)
                        msgs = grp["messages"]
                    else:
                        u = db["users"][tgt]
                        mark_seen(SS.username, tgt)
                        ha.markdown(avatar_html(
                            tgt, u.get("avatar"), 40),
                            unsafe_allow_html=True)
                        hi.markdown("<b>" +
                                    esc(u.get(
                                        "display_name",
                                        tgt)) +
                                    "</b><br><span style="
                                    "'font-size:11px;"
                                    "color:#31a24c;'>"
                                    "● Active</span>",
                                    unsafe_allow_html=True)
                        msgs = [m for m in db["messages"]
                                if (m["from"] ==
                                    SS.username and
                                    m["to"] == tgt) or
                                (m["from"] == tgt and
                                 m["to"] == SS.username)]

                    if SS.clear_msg:
                        SS[SS.clear_msg] = ""
                        SS.clear_msg = ""

                    for m in sorted(msgs,
                                    key=lambda x:
                                    x["time"]):
                        mine = (m["from"] == SS.username)
                        tstr = time.strftime(
                            "%I:%M %p",
                            time.localtime(m["time"])
                        ).lower()
                        if m.get("photo") and \
                                is_local_file(
                                    m["photo"]):
                            st.image(m["photo"], width=200)
                        cls = "bubble-me" if mine \
                            else "bubble-them"
                        snd = ""
                        if is_group and not mine:
                            snd = "<b>@" + esc(m["from"]) \
                                  + "</b><br>"
                        st.markdown("<span class='" + cls +
                                    "'>" + snd +
                                    esc(m.get("text", "")) +
                                    "<span class="
                                    "'bubble-time'>" +
                                    tstr + "</span></span>",
                                    unsafe_allow_html=True)
                        r = m.get("reactions", [])
                        mk = m.get("id",
                                   str(m["time"]))
                        btn = "👍 " + str(len(r)) if r \
                            else "👍"
                        if st.button(btn, key="rx_" + mk):
                            toggle_reaction(is_group, tgt,
                                            m.get("id"),
                                            SS.username)
                            safe_rerun()

                    with st.expander("📷 Send Photo"):
                        ph = st.file_uploader(
                            "Photo", type=["png", "jpg",
                                           "jpeg"],
                            key="chat_photo")
                        if st.button("Send",
                                     key="chat_sp",
                                     use_container_width
                                     =True):
                            if ph is None:
                                st.warning("Choose!")
                            else:
                                path = save_upload(ph)
                                send_chat_message(
                                    is_group, tgt, tgt,
                                    "📷 Photo",
                                    photo=path)
                                safe_rerun()

                    txt = st.text_input("Message...",
                                        key="chat_txt")
                    if st.button("➡️ Send",
                                 key="chat_send",
                                 use_container_width=True):
                        if txt.strip():
                            send_chat_message(
                                is_group, tgt, tgt,
                                txt.strip())
                            SS.clear_msg = "chat_txt"
                            safe_rerun()
            else:
                st.markdown('<div class="panel-header">✉️ '
                            'Chats</div>',
                            unsafe_allow_html=True)
                partners = set()
                for m in db["messages"]:
                    if m["from"] == SS.username:
                        partners.add(m["to"])
                    elif m["to"] == SS.username:
                        partners.add(m["from"])
                for f in db.get("friends", {}).get(
                        SS.username, []):
                    partners.add(f)
                convos = []
                for p in partners:
                    if p == SS.username or p in SS.blocked:
                        continue
                    cn = [m for m in db["messages"]
                          if (m["from"] == SS.username and
                              m["to"] == p) or
                          (m["from"] == p and
                           m["to"] == SS.username)]
                    last = cn[-1] if cn else None
                    convos.append({"u": p, "last": last,
                                   "un": unseen_count(
                                       SS.username, p)})
                convos.sort(key=lambda c: c["last"]["time"]
                            if c["last"] else 0,
                            reverse=True)
                if not convos:
                    st.info("No chats yet!")
                for c in convos:
                    u = db["users"].get(c["u"], {})
                    if c["last"]:
                        if c["last"]["from"] == SS.username:
                            pre = "You: "
                        else:
                            pre = ""
                        pv = pre + esc(c["last"].get(
                            "text", ""))[:30]
                        tm = time.strftime(
                            "%I:%M %p",
                            time.localtime(
                                c["last"]["time"])).lower()
                    else:
                        pv = "Say hello 👋"
                        tm = ""
                    bd = ""
                    if c["un"] > 0:
                        bd = ("<span class="
                              "'unread-badge'>" +
                              str(c["un"]) + "</span>")
                    st.markdown("<div class='chat-item'>"
                                "<div class='av-wrap'>" +
                                avatar_html(c["u"],
                                            u.get("avatar"),
                                            46) +
                                "</div><div class="
                                "'chat-info'><div class="
                                "'chat-name'>" +
                                esc(u.get("display_name",
                                          c["u"])) +
                                "</div><div class="
                                "'chat-preview'>" + pv +
                                "</div></div><div style="
                                "'text-align:right;'>"
                                "<div class='chat-time'>" +
                                tm + "</div>" + bd +
                                "</div></div>",
                                unsafe_allow_html=True)
                    if st.button("💬", key="op_" + c["u"],
                                 use_container_width=True):
                        SS.msg_view = "chat"
                        SS.msg_target = c["u"]
                        SS.msg_target_type = "direct"
                        safe_rerun()

                with st.expander("➕ New Chat"):
                    others = [x for x in db["users"]
                              if x != SS.username]
                    pick = st.selectbox(
                        "Chat with:", others,
                        key="nc_sel")
                    if st.button("Start",
                                 key="nc_btn",
                                 use_container_width=True):
                        SS.msg_view = "chat"
                        SS.msg_target = pick
                        SS.msg_target_type = "direct"
                        safe_rerun()

        # ================= NOTIFICATIONS =================
        elif SS.current_tab == "Notifications":
            st.markdown('<div class="panel-header">🔔 '
                        'Notifications</div>',
                        unsafe_allow_html=True)
            db = load_db()
            mn = [n for n in db["notifications"]
                  if n.get("to") == SS.username][:40]
            if st.button("✅ Mark all read", key="ntf_r",
                         use_container_width=True):
                db = load_db()
                for n in db["notifications"]:
                    if n.get("to") == SS.username:
                        n["read"] = True
                save_db(db)
                safe_rerun()
            if not mn:
                st.info("No notifications!")
            for n in mn:
                tstr = time.strftime(
                    "%d %b %H:%M",
                    time.localtime(n["time"]))
                st.markdown("<div class='notif-row'>" +
                            n["text"] +
                            "<br><span style='font-size:"
                            "11px;color:#9ca3af;'>" + tstr +
                            "</span></div>",
                            unsafe_allow_html=True)

        # ================= LUDO =================
        elif SS.current_tab == "Ludo":
            st.markdown('<div class="panel-header">🎲 '
                        'Ludo</div>',
                        unsafe_allow_html=True)
            if st.button("🎲 Roll Dice",
                         use_container_width=True):
                SS.dice = random.randint(1, 6)
                if SS.dice == 6:
                    db = load_db()
                    u = db["users"].get(SS.username)
                    if u is not None:
                        u["coins"] = u.get("coins", 0) + 5
                        save_db(db)
                safe_rerun()
            if SS.dice:
                st.markdown("<h3 style='text-align:center;"
                            "color:#00B074;'>🎯 " +
                            str(SS.dice) + "</h3>",
                            unsafe_allow_html=True)

        # ================= PROFILE =================
        elif SS.current_tab == "Profile":
            me = DB["users"].get(SS.username, {})
            mp = [p for p in DB["posts"]
                  if p["user"] == SS.username]
            fr = DB["friends"].get(SS.username, [])
            st.markdown("<div class='fb-cover'></div>",
                        unsafe_allow_html=True)
            st.markdown("<div class='fb-av-wrap'>" +
                        avatar_html(SS.username,
                                    me.get("avatar"), 100,
                                    border=True) +
                        "</div>", unsafe_allow_html=True)
            st.markdown("<div class='fb-name'>" +
                        esc(me.get("display_name",
                                   SS.username)) +
                        "</div><div class='fb-sub'>" +
                        str(len(fr)) + " friends · " +
                        str(len(mp)) + " posts</div>",
                        unsafe_allow_html=True)
            if is_owner:
                st.markdown("<p style='text-align:center;'>"
                            "<span class='owner-badge'>👑 "
                            "OWNER</span></p>",
                            unsafe_allow_html=True)
            b1, b2, b3 = st.columns(3)
            if b1.button("➕ Story", key="fb_st",
                         use_container_width=True):
                SS.current_tab = "Create"
                safe_rerun()
            if b2.button("✏️ Edit", key="fb_ed",
                         use_container_width=True):
                SS.current_tab = "Settings"
                SS.settings_page = "personal"
                safe_rerun()
            if b3.button("📢 My Ads", key="fb_ads",
                         use_container_width=True):
                SS.current_tab = "Ads"
                safe_rerun()

            st.markdown("**Personal Details**")
            st.markdown("<div class='pd-row'>🎂 <b>" +
                        esc(me.get("birthday",
                                   "Not set")) +
                        "</b></div>", unsafe_allow_html=True)
            st.markdown("<div class='pd-row'>👤 <b>" +
                        esc(me.get("gender",
                                   "Not set")) +
                        "</b></div>", unsafe_allow_html=True)
            st.markdown("<div class='pd-row'>💰 <b>" +
                        str(me.get("coins", 0)) +
                        " coins</b></div>",
                        unsafe_allow_html=True)

            st.markdown("**Posts**")
            st.markdown("<div class='composer'>" +
                        avatar_html(SS.username,
                                    me.get("avatar"), 36) +
                        "What's on your mind?</div>",
                        unsafe_allow_html=True)
            pt = st.text_input("Write...",
                               key="fb_comp")
            if st.button("🚀 Post", key="fb_post",
                         use_container_width=True):
                if pt.strip():
                    db = load_db()
                    db["posts"].insert(0, {
                        "id": uuid.uuid4().hex[:8],
                        "user": SS.username, "type": "text",
                        "grad": random.choice(GRADS),
                        "txt": esc(pt)[:40], "cap": pt,
                        "likes": {}, "comments": []})
                    save_db(db)
                    st.success("Posted!")
                    SS.clear_cmt = "fb_comp"
                    safe_rerun()
            for p in mp[:6]:
                if p.get("type") == "text":
                    st.markdown("<div class='post-ph' "
                                "style='background:" +
                                p.get("grad", "#f0f0f0") +
                                ";height:100px;'>" +
                                esc(p.get("txt", "")) +
                                "</div>",
                                unsafe_allow_html=True)
                elif p.get("type") == "image" and \
                        is_local_file(p["ref"]):
                    st.image(p["ref"],
                             use_container_width=True)

        # ================= SETTINGS =================
        elif SS.current_tab == "Settings":

            if SS.settings_page == "menu":
                st.markdown('<div class="panel-header">⚙️ '
                            'Settings</div>',
                            unsafe_allow_html=True)
                st.caption("@" + SS.username)
                if is_owner:
                    if st.button("🛡️ OWNER PANEL ›",
                                 key="m_admin",
                                 use_container_width=True):
                        SS.settings_page = "admin"
                        safe_rerun()
                items = [
                    ("📋 Personal Info", "personal"),
                    ("🔐 Security", "security"),
                    ("💰 Payments", "payments"),
                    ("📰 News Feed", "feed"),
                    ("🚫 Blocked", "blocked"),
                    ("⚠️ Report", "reports"),
                    ("ℹ️ About", "about"),
                ]
                for label, page in items:
                    if st.button(label + " ›",
                                 key="m_" + page,
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
                st.markdown('<div class="panel-header">🛡️ '
                            'Owner Panel</div>',
                            unsafe_allow_html=True)
                db = load_db()
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Users", len(db["users"]))
                c2.metric("Posts", len(db["posts"]))
                c3.metric("Groups",
                          len(db["groups"]))
                c4.metric("Reports", len(db["reports"]))
                st.markdown("### 🚩 Reports")
                for i, r in enumerate(
                        reversed(db["reports"][:10])):
                    ru = r.get("user", "")
                    rc1, rc2 = st.columns([0.6, 0.4])
                    rc1.markdown("🚩 **@" + esc(ru) +
                                 "** by @" +
                                 esc(r.get("from", "")))
                    if ru in db["banned"]:
                        if rc2.button("Unban",
                                      key="rp_unb_" +
                                      str(i),
                                      use_container_width
                                      =True):
                            db = load_db()
                            db["banned"].remove(ru)
                            save_db(db)
                            safe_rerun()
                    else:
                        if rc2.button("BAN",
                                      key="rp_ban_" +
                                      str(i),
                                      use_container_width
                                      =True):
                            db = load_db()
                            db["banned"].append(ru)
                            save_db(db)
                            safe_rerun()
                st.markdown("### 🔨 Ban by ID")
                bi = st.text_input("Username",
                                   key="ob_in")
                if st.button("🔨 Ban", key="ob_btn",
                             use_container_width=True):
                    db = load_db()
                    u = bi.strip().lower()
                    if u and u != SS.username and \
                            u in db["users"]:
                        db["banned"].append(u)
                        save_db(db)
                        safe_rerun()
                st.markdown("### 📢 Ads (approve yahan "
                            "se bhi — Ads tab)")
                pending = [a for a in db["ads"]
                           if a["status"] == "pending"]
                st.write("Pending ads: " +
                         str(len(pending)))

            elif SS.settings_page == "personal":
                settings_back("bk_p")
                me = DB["users"].get(SS.username, {})
                dn = st.text_input(
                    "Display Name",
                    value=me.get("display_name", ""),
                    key="st_dn")
                bio = st.text_input(
                    "Bio", value=me.get("bio", ""),
                    key="st_bio")
                bday = st.text_input(
                    "Birthday",
                    value=me.get("birthday", ""),
                    key="st_bd")
                gen = st.selectbox(
                    "Gender", ["Male", "Female",
                               "Other"], key="st_g")
                if st.button("💾 Save", key="st_s",
                             use_container_width=True):
                    db = load_db()
                    u = db["users"].get(SS.username)
                    if u is not None:
                        u["display_name"] = dn
                        u["bio"] = bio
                        u["birthday"] = bday
                        u["gender"] = gen
                        save_db(db)
                    st.success("Saved!")

            elif SS.settings_page == "security":
                settings_back("bk_s")
                score, tips = security_score()
                st.progress(score / 100.0)
                st.write("Score: **" + str(score) + "/100**")
                for t in tips:
                    st.markdown("• " + t)
                SS.pin_state = st.checkbox(
                    "App Lock (session)", key="al")
                SS.finger_lock = st.checkbox(
                    "Fingerprint Lock (session)",
                    key="fl")
                SS.login_alerts = st.checkbox(
                    "Login Alerts", key="la")
                SS.auto_logout = st.selectbox(
                    "Auto logout:", [0, 5, 10, 30],
                    key="to")

            elif SS.settings_page == "payments":
                settings_back("bk_pay")
                me = DB["users"].get(SS.username, {})
                st.success("Balance: **" +
                           str(me.get("coins", 0)) +
                           " Coins**")
                if st.button("💳 Payout", key="pw",
                             use_container_width=True):
                    db = load_db()
                    u = db["users"].get(SS.username)
                    if u is not None and \
                            u.get("coins", 0) >= 100:
                        u["coins"] -= 100
                        save_db(db)
                        st.success("Payout submitted!")
                    else:
                        st.warning("Min 100 coins!")

            elif SS.settings_page == "feed":
                settings_back("bk_f")
                SS.feed_sort = st.radio(
                    "Sort:", ["Most Recent", "Top Posts"],
                    key="fs")
                SS.show_stories = st.checkbox(
                    "Show Stories", key="ss")
                SS.comment_filter = st.checkbox(
                    "Comment Filter", key="cf")

            elif SS.settings_page == "blocked":
                settings_back("bk_b")
                bi = st.text_input("Username to block",
                                   key="bi2")
                if st.button("🚫 Block", key="bb2",
                             use_container_width=True):
                    u = bi.strip().lower()
                    if u and u != SS.username:
                        db = load_db()
                        rec = db["users"].get(
                            SS.username)
                        if rec is not None:
                            rec.setdefault(
                                "blocked", []).append(u)
                            save_db(db)
                            SS.blocked.append(u)
                        safe_rerun()
                for i, u in enumerate(SS.blocked):
                    bc1, bc2 = st.columns([0.6, 0.4])
                    bc1.markdown("**🚫 @" + u + "**")
                    if bc2.button("Unblock",
                                  key="ub2_" + str(i),
                                  use_container_width=True):
                        db = load_db()
                        rec = db["users"].get(
                            SS.username)
                        if rec is not None and u in \
                                rec.get("blocked", []):
                            rec["blocked"].remove(u)
                            save_db(db)
                        SS.blocked.remove(u)
                        safe_rerun()

            elif SS.settings_page == "reports":
                settings_back("bk_r")
                ri = st.text_input("Member ID",
                                   key="ri")
                rs = st.selectbox(
                    "Reason", ["Harassment", "Abusive",
                               "Spam", "Scam", "Other"],
                    key="rs")
                if st.button("🚩 Submit", key="rb",
                             use_container_width=True):
                    if ri.strip().lower():
                        db = load_db()
                        db["reports"].append({
                            "from": SS.username,
                            "user": ri.strip().lower(),
                            "reason": rs,
                            "time": time.time()})
                        save_db(db)
                        if owner:
                            add_notification(
                                owner, "🚩 Report: @" +
                                ri.strip().lower() +
                                " by @" + SS.username)
                        st.success("Report sent!")

            elif SS.settings_page == "about":
                settings_back("bk_a")
                st.markdown("<div class='channel-banner'>"
                            "<h2>ℹ️ " + APP_INFO["name"] +
                            "</h2><p>" + APP_INFO["type"] +
                            "</p></div>",
                            unsafe_allow_html=True)
                st.markdown(
                    "**🏢 Parent Company:** " +
                    APP_INFO["parent"] + "\n\n" +
                    "**👑 Founders:** " +
                    APP_INFO["founders"] + "\n\n" +
                    "**📍 Headquarters:** " +
                    APP_INFO["hq"] + "\n\n" +
                    "**📅 Founded:** " +
                    APP_INFO["founded"] + "\n\n" +
                    "---\n\n" +
                    "**Features:**\n"
                    "• News Feed, Stories, Reels\n"
                    "• 👥 Groups & 📄 Pages\n"
                    "• 📅 Events with RSVP\n"
                    "• 🛒 Marketplace\n"
                    "• 📢 Ads Manager\n"
                    "• ✉️ Messenger (chats, groups, "
                    "photos, reactions)\n"
                    "• 🎲 Games + Coins Wallet\n\n"
                    "© 2026 " + APP_INFO["parent"] +
                    " - All rights reserved.")

        # ---- BOTTOM NAV ----
        nav_items = [
            ("Home", "🏠"), ("Search", "🔍"),
            ("Groups", "👥"), ("Marketplace", "🛒"),
            ("Create", "➕"), ("Messages", "✉️"),
            ("Profile", "👤"),
        ]
        nav_html = "<div class='ig-nav'>"
        for t, ic in nav_items:
            cls = " on" if SS.current_tab == t else ""
            nav_html += ("<a href='?tab=" + t +
                         "' class='" + cls + "'>" + ic +
                         "</a>")
        nav_html += "</div>"
        st.markdown(nav_html, unsafe_allow_html=True)


# ---------- SAFETY ----------
else:
    SS.page = "splash"
    safe_rerun()

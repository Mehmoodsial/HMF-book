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
                 "<a href

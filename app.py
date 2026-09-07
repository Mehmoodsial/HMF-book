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
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

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

FORCE_OWNER = ""
SALT = "hmf_book_secret_2025"
CHANNEL_NAME = "Color Pop Cartoons"
CHANNEL_HANDLE = "@ColorPopCartoons83"
CHANNEL_URL = "https://www.youtube.com/" + CHANNEL_HANDLE
DB_FILE = "hmf_db.json"
CALL_FILE = "calls.json"
UPLOAD_DIR = "uploads"
FILTER_NAMES = ["None", "Beauty", "Sepia", "Vintage", "Cool",
                "Grayscale", "Bright", "Cartoon"]
VALID_TABS = ["Home", "Search", "Friends", "Channel",
              "Reels", "Create", "Messages", "Notifications",
              "Ludo", "Profile", "Settings"]


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
            part = url.split(tag)[1]
            part = part.split("?")[0].split("&")[0].split("/")[0]
            if part:
                return part
    return None


def load_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
    except Exception:
        db = {}
    for key in ("users", "messages", "posts", "groups",
                "notifications", "reports", "banned",
                "friend_requests"):
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
    n = 0
    for m in db["messages"]:
        if m["from"] == partner and m["to"] == me \
                and m.get("time", 0) > last:
            n += 1
    return n


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
        db2 = load_db()
        for g in db2["groups"]:
            if g["id"] == group_id:
                for mm in g["members"]:
                    if mm != me:
                        add_notification(
                            mm, "👥 '" + g["name"] + "': @" +
                            me + " " + text[:25])
                break
    else:
        msg["to"] = to_user
        db["messages"].append(msg)
        save_db(db)
        add_notification(to_user, "✉️ @" + me +
                         " sent you a message")


def hmf_ai_reply(q):
    q = (q or "").lower()
    if not q:
        return "Kuch likhein - main madad karta hoon!"
    if "hi" in q or "hello" in q or "salam" in q:
        return "Hello! Main HMF AI hoon. Kaise madad karun?"
    if "coin" in q:
        return "Coins: Ludo khelen (6 par +5) aur games jeeten!"
    if "friend" in q:
        return "Friends tab mein requests bhejein!"
    if "call" in q:
        return "Voice calls chat/profile se - 📞 button!"
    if "security" in q or "hack" in q:
        return "Security Center mein score check karein!"
    return ("Main seekh raha hoon - Friends, Chats, Calls "
            "aur Coins mein madad kar sakta hoon.")


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


def load_calls():
    try:
        with open(CALL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"active": {}, "history": []}


def save_calls(c):
    try:
        with open(CALL_FILE, "w", encoding="utf-8") as f:
            json.dump(c, f)
    except Exception:
        pass


def start_call(a, b):
    calls = load_calls()
    cid = uuid.uuid4().hex[:8]
    calls["active"][cid] = {
        "id": cid, "from": a, "to": b,
        "start": time.time(), "status": "ringing"}
    save_calls(calls)
    return cid


def answer_call(call_id, accept=True):
    calls = load_calls()
    if call_id not in calls["active"]:
        return
    if accept:
        calls["active"][call_id]["status"] = "active"
        calls["active"][call_id]["answered"] = time.time()
    else:
        calls["active"][call_id]["status"] = "ended"
    save_calls(calls)
    if not accept:
        end_call(call_id)


def end_call(call_id):
    calls = load_calls()
    if call_id in calls["active"]:
        c = calls["active"].pop(call_id)
        c["end"] = time.time()
        calls["history"].append(c)
        save_calls(calls)


def get_incoming_call(user):
    calls = load_calls()
    for cid, c in calls["active"].items():
        if c.get("to") == user and c.get("status") == "ringing":
            return c
    return None


def get_active_call_for(user):
    calls = load_calls()
    for cid, c in calls["active"].items():
        if (c.get("from") == user or
                c.get("to") == user) and \
                c.get("status") == "active":
            return c
    return None


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


def avatar_html(username, avatar_path=None, size=36):
    if avatar_path and os.path.exists(avatar_path):
        try:
            b64 = base64.b64encode(
                open(avatar_path, "rb").read()).decode()
            return ("<img src='data:image/png;base64," + b64 +
                    "' style='width:" + str(size) +
                    "px;height:" + str(size) +
                    "px;border-radius:50%;object-fit:cover;"
                    "margin-right:10px;'>")
        except Exception:
            pass
    ini = esc(str(username)[:2].upper())
    return ("<div style='width:" + str(size) +
            "px;height:" + str(size) +
            "px;border-radius:50%;background:"
            "linear-gradient(135deg,#00B074,#056839);"
            "color:#fff;display:flex;align-items:center;"
            "justify-content:center;font-weight:bold;"
            "margin-right:10px;font-size:" +
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


def shot_install():
    if not HAS_JS:
        return
    code = ("(()=>{const w=window.parent;"
            "if(!w.hmfListenSet){w.hmfListenSet=1;"
            "w.addEventListener('keyup',function(e){"
            "if(e.key==='PrintScreen'){"
            "w.hmfShotPending='print';}});"
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
    code = ("(()=>{const w=window.parent;"
            "const v=w.hmfShotPending;"
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


# ---------- SEED ----------
DB = load_db()
SEED_USERS = [
    ("demo", "demo@hmfbook.com", "1234", "Demo User"),
    ("hoor_jannat", "hoor@hmfbook.com", "1234",
     "Hoor Jannat"),
    ("farrukh_m", "farrukh@hmfbook.com", "1234",
     "Farrukh M"),
    ("zara_x", "zara@hmfbook.com", "1234", "Zara X"),
]
changed = False
for uname, mail, pw, name in SEED_USERS:
    if uname in DB["banned"]:
        continue
    if uname not in DB["users"]:
        DB["users"][uname] = {
            "email": mail, "password": hash_pw(pw),
            "display_name": name,
            "bio": "Living life one post at a time.",
            "coins": 550, "followers": 1240,
            "following": 120, "blocked": [],
            "avatar": None, "fails": 0, "lock_until": 0}
        changed = True

if not DB["posts"]:
    DB["posts"] = [
        {"id": "s1", "user": "hoor_jannat",
         "type": "youtube", "ref": "aqz-KE-bpKQ",
         "cap": "Big Buck Bunny!", "likes": {},
         "comments": [], "avatar": None},
        {"id": "s2", "user": "farrukh_m", "type": "text",
         "grad": "linear-gradient(45deg,#d1fae5,#a7f3d0)",
         "txt": "🎲 Ludo Night Tournament",
         "cap": "Tonight 8 PM - winner takes all!",
         "likes": {}, "comments": [], "avatar": None},
        {"id": "s3", "user": "demo", "type": "text",
         "grad": "linear-gradient(45deg,#ecfdf5,#6ee7b7)",
         "txt": "🌿 Green Vibes Only",
         "cap": "Loving this new HMF book app!",
         "likes": {}, "comments": [], "avatar": None},
    ]
    changed = True

REELS = [
    ("https://commondatastorage.googleapis.com/"
     "gtv-videos-bucket/sample/ForBiggerFun.mp4",
     "Fun times!"),
    ("https://commondatastorage.googleapis.com/"
     "gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
     "Fire content!"),
]
for i, (url, cap) in enumerate(REELS):
    rid = "reel_seed" + str(i)
    if not any(p.get("id") == rid for p in DB["posts"]):
        DB["posts"].append({
            "id": rid,
            "user": ["demo", "hoor_jannat"][i % 2],
            "type": "reel", "ref": url, "cap": cap,
            "likes": {}, "comments": [], "avatar": None})
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
    "block_msg": "", "report_msg": "", "help_msg": "",
    "withdraw_msg": "", "yt_msg": "", "view_user": None,
    "msg_view": "list", "msg_target": "",
    "msg_target_type": "direct", "last_shot_time": 0,
    "app_lock": False, "app_pin": "", "pin_unlocked": True,
    "pin_attempts": 0, "pin_lock_until": 0, "pin_msg": "",
    "finger_lock": False, "finger_unlocked": True,
    "auto_logout": 0, "last_active": 0, "dark_mode": False,
    "language": "English", "feed_sort": "Most Recent",
    "show_stories": True, "comment_filter": True,
    "private_account": False, "strong_password": False,
    "two_factor": False, "login_alerts": True,
    "security_log": [], "tx_history": [],
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


def add_security_event(text):
    SS.security_log.insert(0, {"event": text,
                               "time": "Just now"})
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
    if SS.app_lock or SS.finger_lock:
        score += 20
    else:
        tips.append("App Lock or Fingerprint (+20)")
    if SS.strong_password:
        score += 20
    else:
        tips.append("Stronger password (+20)")
    if SS.auto_logout > 0:
        score += 10
    else:
        tips.append("Auto Logout (+10)")
    if SS.private_account:
        score += 10
    else:
        tips.append("Private account (+10)")
    if SS.comment_filter:
        score += 5
    else:
        tips.append("Comment Filter (+5)")
    return score, tips


def settings_back(key):
    if st.button("← Back to Settings", key=key):
        SS.settings_page = "menu"
        SS.privacy_step = 0
        safe_rerun()


# ---------- URL PARAMS (?tab= / ?dark= / ?profile=) ----
try:
    qp = dict(st.query_params)
except Exception:
    qp = {}

tab_q = qp.get("tab")
dark_q = qp.get("dark")
PROFILE_VIEW = qp.get("profile")

if SS.logged_in:
    if tab_q in VALID_TABS:
        SS.current_tab = tab_q
        if tab_q == "Settings":
            SS.settings_page = "menu"
        if tab_q == "Messages":
            SS.msg_view = "list"
    if dark_q in ("0", "1"):
        SS.dark_mode = dark_q == "1"

if tab_q in VALID_TABS or dark_q in ("0", "1") \
        or PROFILE_VIEW:
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
    [data-testid="stToolbar"] { visibility:hidden
        !important; }
    [data-testid="stStatusWidget"] { visibility:hidden
        !important; }
    [data-testid="stDecoration"] { display:none
        !important; }

    /* ===== PHONE FRAME (Instagram jaisa) ===== */
    .block-container, [data-testid="block-container"] {
        max-width:430px; margin:0 auto;
        background:CARDBG;
        padding-top:0 !important;
        padding-left:10px !important;
        padding-right:10px !important;
        padding-bottom:95px !important;
        min-height:100vh;
        box-shadow:0 0 35px rgba(0,0,0,.18); }

    /* ===== INSTAGRAM TOPBAR ===== */
    .ig-topbar { position:sticky; top:0; z-index:995;
        display:flex; justify-content:space-between;
        align-items:center; padding:12px 14px;
        background:CARDBG;
        border-bottom:1px solid BORDERC;
        margin:0 -10px; }
    .ig-logo { font-size:26px; font-weight:700;
        font-family:'Segoe Script','Brush Script MT',
        cursive; color:TXT1; letter-spacing:.5px; }
    .ig-icons a { font-size:21px; text-decoration:none;
        margin-left:16px; position:relative;
        display:inline-block; }
    .nav-dot { position:absolute; top:-6px;
        right:-10px; background:#e53e3e; color:#fff;
        border-radius:10px; font-size:10px;
        font-weight:700; padding:1px 5px;
        font-family:sans-serif; }

    /* ===== STORIES ===== */
    .stories-container { display:flex; gap:14px;
        padding:12px 4px;
        border-bottom:1px solid BORDERC;
        overflow-x:auto; }
    .story-card { display:flex; flex-direction:column;
        align-items:center; text-align:center;
        min-width:64px; }
    .story-ring { width:58px; height:58px;
        border-radius:50%; padding:2.5px;
        background:linear-gradient(135deg,#00B074,
        #056839); display:flex; align-items:center;
        justify-content:center; }
    .story-ring.gray { background:#dbdbdb; }
    .story-img { width:100%; height:100%;
        border-radius:50%; background:CARDBG;
        border:2px solid CARDBG; display:flex;
        align-items:center; justify-content:center;
        font-weight:bold; color:TXT2; font-size:14px; }
    .story-name { font-size:11px; color:TXT2;
        margin-top:4px; }

    /* ===== QUICK PILLS ===== */
    .quick-row { display:flex; gap:10px;
        padding:10px 0 4px; }
    .quick-pill { flex:1; text-align:center;
        padding:7px 10px; border:1px solid BORDERC;
        border-radius:20px; font-size:13px;
        text-decoration:none; color:TXT1;
        font-weight:600; }

    /* ===== POSTS ===== */
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

    /* ===== CHATS ===== */
    .chat-item { display:flex; align-items:center;
        padding:11px 4px;
        border-bottom:1px solid BORDERC; }
    .av-wrap { position:relative; margin-right:6px;
        flex-shrink:0; }
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
        font-weight:700; padding:0 6px; margin-top:4px; }
    .chat-header { display:flex; align-items:center;
        gap:8px; padding:10px 4px;
        border-bottom:1px solid BORDERC;
        margin-bottom:6px; }
    .enc-note { text-align:center; font-size:11px;
        color:TXT2; background:rgba(0,176,116,.07);
        border-radius:10px; padding:6px 10px;
        margin:6px 0; }
    .friend-note { text-align:center; font-size:12px;
        color:#00B074; margin:8px 0; font-weight:600; }
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
        display:block; text-align:right;
        margin-top:2px; }

    .call-window { background:CARDBG;
        border:1px solid BORDERC; border-radius:14px;
        padding:12px; margin:8px 0; }
    .call-row { display:flex; align-items:center;
        gap:12px; padding:6px 0; }

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

    /* ===== FIXED BOTTOM NAV (Instagram style) ===== */
    .ig-nav { position:fixed; bottom:0; left:50%;
        transform:translateX(-50%); width:100%;
        max-width:430px; background:CARDBG;
        border-top:1px solid BORDERC;
        display:flex; justify-content:space-around;
        align-items:center; padding:10px 0 14px;
        z-index:998; margin:0; }
    .ig-nav a { font-size:23px; text-decoration:none;
        filter:grayscale(1) opacity(.45);
        position:relative; line-height:1; }
    .ig-nav a.on { filter:none;
        transform:scale(1.12); }

    div[data-testid="stButton"] > button,
    div.stButton > button { background:#00B074
        !important; color:#fff !important;
        font-weight:600 !important; border:none
        !important; border-radius:12px !important; }
    div[data-testid="stButton"] > button:hover,
    div.stButton > button:hover {
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
        hr { border-color:#2a2e2a !important; }
        </style>
        """
    return css


SPLASH_CSS = """
<style>
.stApp { background: linear-gradient(135deg,#00B074 0%,
    #056839 100%) !important; }
header[data-testid="stHeader"], #MainMenu, footer {
    visibility:hidden !important; }
[data-testid="stToolbar"] { visibility:hidden !important; }
[data-testid="stDecoration"] { display:none !important; }
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
[data-testid="stToolbar"] { visibility:hidden !important; }
[data-testid="stDecoration"] { display:none !important; }
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
    db = load_db()

    if PROFILE_VIEW and PROFILE_VIEW in db["users"]:
        u = db["users"][PROFILE_VIEW]
        st.markdown(build_main_css(False),
                    unsafe_allow_html=True)
        st.markdown('<div class="panel-header">👤 HMF '
                    'Profile</div>', unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;"
                    "margin:10px 0;'>" +
                    avatar_html(PROFILE_VIEW,
                                u.get("avatar"), 86) +
                    "</div>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;'>" +
                    esc(u.get("display_name",
                              PROFILE_VIEW)) + "</h3>",
                    unsafe_allow_html=True)
        if st.button("Open HMF book App",
                     use_container_width=True):
            SS.page = "app" if SS.logged_in else "auth"
            safe_rerun()
    else:
        st.markdown("<div class='mid'><h1 class='logo'>HMF"
                    "</h1><p class='sub'>HMF book</p></div>",
                    unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1.3, 1])
        with c2:
            if st.button("Get Started",
                         use_container_width=True):
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
            st.caption("Strong password!")
            SS.strong_password = True
        else:
            st.caption("Weak - use 8+ chars, numbers, "
                       "symbols")
            SS.strong_password = False

    if st.button(btn_label, use_container_width=True):
        u = username.strip().lower()
        db = load_db()

        if not u or not password:
            st.error("Please enter both username and "
                     "password!")
        elif u in db["banned"]:
            st.error("🚫 This account is PERMANENTLY "
                     "BANNED by the owner!")
        elif is_signup:
            if u in db["users"]:
                st.error("Username already taken!")
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
                    "bio": "New to HMF book!",
                    "coins": 100, "followers": 0,
                    "following": 0, "blocked": [],
                    "avatar": None, "fails": 0,
                    "lock_until": 0}
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
            rec = db["users"].get(u)
            if rec and rec.get("lock_until", 0) > \
                    time.time():
                wait = int(rec["lock_until"] -
                           time.time()) + 1
                st.error("🔒 Locked! Try in " + str(wait) +
                         " seconds.")
            elif rec and pw_ok(rec.get("password", ""),
                               password):
                if rec.get("password") == password:
                    rec["password"] = hash_pw(password)
                rec["fails"] = 0
                rec["lock_until"] = 0
                save_db(db)
                SS.logged_in = True
                SS.username = u
                SS.email = rec.get("email", "")
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
                    st.error("🔒 5 wrong attempts! Locked "
                             "60 seconds.")
                else:
                    left = 5 - rec["fails"]
                    st.error("Invalid password! " +
                             str(left) + " left.")
                save_db(db)
            else:
                st.error("Invalid username or password!")

    if st.button(switch_txt):
        SS.auth_mode = "login" if is_signup else "signup"
        safe_rerun()

    st.markdown("<p style='text-align:center;color:#99a;"
                "font-size:13px;'>Demo: demo / 1234 • "
                "First new signup = Owner 👑</p>",
                unsafe_allow_html=True)


# ================= 3) LOCKS + MAIN =================
elif SS.page == "app" and SS.logged_in:
    need_pin = SS.app_lock and not SS.pin_unlocked
    need_finger = SS.finger_lock and not SS.finger_unlocked

    if need_finger or need_pin:

        st.markdown(build_main_css(SS.dark_mode),
                    unsafe_allow_html=True)

        if need_finger:
            st.markdown("""
            <div class="lock-screen">
                <div class="finger-icon">👆</div>
                <h2>Fingerprint Lock</h2>
            </div>
            """, unsafe_allow_html=True)
            if st.button("👆 Scan Fingerprint",
                         use_container_width=True,
                         key="finger_scan"):
                time.sleep(1.2)
                SS.finger_unlocked = True
                safe_rerun()
            if st.button("🚪 Logout instead",
                         key="finger_out",
                         use_container_width=True):
                SS.logged_in = False
                SS.page = "auth"
                safe_rerun()

        else:
            st.markdown("""
            <div class="lock-screen">
                <div class="finger-icon">🔐</div>
                <h2>App Locked</h2>
            </div>
            """, unsafe_allow_html=True)
            now = time.time()
            if SS.pin_lock_until > now:
                st.error("Locked for " +
                         str(int(SS.pin_lock_until - now) +
                              1) + " seconds.")
            else:
                pin_in = st.text_input("4-digit PIN",
                                       type="password",
                                       key="pin_in")
                if st.button("🔓 Unlock",
                             use_container_width=True):
                    if pin_in == SS.app_pin:
                        SS.pin_unlocked = True
                        SS.pin_attempts = 0
                        safe_rerun()
                    else:
                        SS.pin_attempts += 1
                        if SS.pin_attempts >= 3:
                            SS.pin_lock_until = \
                                time.time() + 30
                            SS.pin_attempts = 0
                        safe_rerun()

    else:
        # ============ MAIN APP ============
        st.markdown(build_main_css(SS.dark_mode),
                    unsafe_allow_html=True)
        DB = load_db()
        owner = FORCE_OWNER or DB.get("owner", "")
        is_owner = (SS.username == owner)

        if PROFILE_VIEW and PROFILE_VIEW in DB["users"]:
            SS.view_user = PROFILE_VIEW

        now = time.time()
        if SS.auto_logout > 0 and SS.last_active > 0:
            if now - SS.last_active > SS.auto_logout * 60:
                SS.logged_in = False
                SS.page = "auth"
                safe_rerun()
        SS.last_active = now

        unread = unread_count(SS.username)
        banned_list = DB.get("banned", [])

        # ---------- CALLS ----------
        incoming = get_incoming_call(SS.username)
        active_call = get_active_call_for(SS.username)

        if incoming:
            st.markdown("""
            <div class="call-window" style=
                 "border:2px solid #00B074;">
                <div class="call-row">
                    <div style="font-size:26px;">📞</div>
                    <div><b>Incoming Call from @""" +
                esc(incoming["from"]) + """</b><br>
                    <span style="font-size:12px;
                    color:#6b7280;">Ringing...</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            ic1, ic2 = st.columns(2)
            if ic1.button("✅ Accept", key="call_accept",
                          use_container_width=True):
                answer_call(incoming["id"], True)
                add_notification(incoming["from"],
                                 "📞 @" + SS.username +
                                 " accepted your call!")
                safe_rerun()
            if ic2.button("❌ Reject", key="call_reject",
                          use_container_width=True):
                answer_call(incoming["id"], False)
                safe_rerun()

        if active_call:
            st.markdown("""
            <div class="call-window" style=
                 "border:2px solid #00B074;">
                <div class="call-row">
                    <div style="font-size:26px;">🎙️</div>
                    <div><b>Call Active</b><br>
                    <span style="font-size:12px;
                    color:#6b7280;">Connected</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            ac1, ac2, ac3 = st.columns(3)
            if ac1.button("🎤 Mute", key="call_mute",
                          use_container_width=True):
                safe_toast("Muted (demo)")
            if ac2.button("🔊 Speaker",
                          key="call_speaker",
                          use_container_width=True):
                safe_toast("Speaker on (demo)")
            if ac3.button("📴 End", key="call_end",
                          use_container_width=True):
                other = active_call["to"]
                if other == SS.username:
                    other = active_call["from"]
                add_notification(other, "📴 @" +
                                 SS.username +
                                 " ended the call")
                end_call(active_call["id"])
                safe_rerun()

        # ---------- INSTAGRAM TOPBAR ----------
        if SS.dark_mode:
            dark_href = "?dark=0"
            dark_icon = "☀️"
        else:
            dark_href = "?dark=1"
            dark_icon = "🌙"

        n_badge = ""
        if unread > 0:
            n_badge = ("<span class='nav-dot'>" +
                       str(unread) + "</span>")

        topbar = ("<div class='ig-topbar'>"
                  "<div class='ig-logo'>HMF book</div>"
                  "<div class='ig-icons'>"
                  "<a href='?tab=Messages'>✉️</a>"
                  "<a href='?tab=Notifications'>🔔" +
                  n_badge + "</a>"
                  "<a href='" + dark_href + "'>" +
                  dark_icon + "</a>"
                  "<a href='?tab=Settings'>⚙️</a>"
                  "</div></div>")
        st.markdown(topbar, unsafe_allow_html=True)

        # ============ VIEW USER ============
        if SS.view_user and SS.view_user != SS.username:

            vu = SS.view_user
            if vu not in DB["users"]:
                SS.view_user = None
                safe_rerun()
            else:
                u = DB["users"][vu]
                my_posts = [p for p in DB["posts"]
                            if p["user"] == vu]

                st.markdown('<div class="panel-header">👤 '
                            'Profile</div>',
                            unsafe_allow_html=True)
                st.markdown(
                    "<div style='text-align:center;"
                    "margin:10px 0;'>" +
                    avatar_html(vu, u.get("avatar"), 86) +
                    "</div>", unsafe_allow_html=True)
                st.markdown(
                    "<h3 style='text-align:center;'>" +
                    esc(u.get("display_name", vu)) +
                    "</h3><p style='text-align:center;"
                    "color:#6b7280;font-size:13px;'>" +
                    esc(u.get("bio", "")) +
                    "</p><p style='text-align:center;"
                    "color:#00B074;font-size:12px;'>" +
                    str(len(my_posts)) + " Posts • " +
                    str(u.get("followers", 0)) +
                    " Followers</p>",
                    unsafe_allow_html=True)

                if is_owner:
                    if vu in banned_list:
                        if st.button("✅ Unban (Owner)",
                                     key="vw_unban",
                                     use_container_width
                                     =True):
                            db = load_db()
                            if vu in db["banned"]:
                                db["banned"].remove(vu)
                                save_db(db)
                                safe_rerun()
                    else:
                        if st.button(
                                "🔨 BAN (Owner)",
                                key="vw_ban",
                                use_container_width=True):
                            db = load_db()
                            db["banned"].append(vu)
                            save_db(db)
                            add_notification(
                                vu, "🚫 Owner ne aapko "
                                "ban kar diya!")
                            safe_rerun()

                already_friend = vu in DB["friends"].get(
                    SS.username, [])
                already_sent = any(
                    r["from"] == SS.username and
                    r["to"] == vu
                    for r in DB["friend_requests"])

                v1, v2, v3 = st.columns(3)
                if v1.button(
                        "✅ Friends" if already_friend
                        else "Sent" if already_sent
                        else "➕ Add Friend",
                        key="vw_friend",
                        use_container_width=True):
                    if not already_friend and \
                            not already_sent:
                        send_friend_request(
                            SS.username, vu)
                        safe_rerun()
                if v2.button("✉️ Message", key="vw_msg",
                             use_container_width=True):
                    SS.msg_view = "chat"
                    SS.msg_target = vu
                    SS.msg_target_type = "direct"
                    SS.current_tab = "Messages"
                    SS.view_user = None
                    safe_rerun()
                if v3.button("📞 Call", key="vw_call",
                             use_container_width=True):
                    start_call(SS.username, vu)
                    add_notification(
                        vu, "📞 @" + SS.username +
                        " is calling you!")
                    safe_rerun()

                v4, v5 = st.columns(2)
                if v4.button("🚫 Block", key="vw_block",
                             use_container_width=True):
                    db = load_db()
                    rec = db["users"].get(SS.username)
                    if rec is not None:
                        rec.setdefault(
                            "blocked", []).append(vu)
                        save_db(db)
                        SS.blocked = list(
                            rec["blocked"])
                    SS.view_user = None
                    safe_rerun()
                if v5.button("🚩 Report",
                             key="vw_report",
                             use_container_width=True):
                    db = load_db()
                    db["reports"].append({
                        "from": SS.username, "user": vu,
                        "reason": "From profile",
                        "time": time.time()})
                    save_db(db)
                    if owner:
                        add_notification(
                            owner, "🚩 Report: @" + vu +
                            " (by @" + SS.username + ")")
                    st.success("Report owner ko gayi!")

                for p in my_posts[:6]:
                    if p.get("type") == "text":
                        st.markdown(
                            "<div class='post-ph' "
                            "style='background:" +
                            p.get("grad", "#f3f4f6") +
                            ";height:110px;color:#056839;"
                            "font-weight:bold;'>" +
                            p.get("txt", "") + "</div>",
                            unsafe_allow_html=True)
                    elif p.get("type") == "youtube":
                        yt = ('<iframe width="100%" '
                              'height="170" src='
                              '"https://www.youtube.com/'
                              'embed/' + p["ref"] +
                              '" frameborder="0" '
                              'allowfullscreen></iframe>')
                        components.html(yt, height=180)

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
                    <div class="story-card"><div class="story-ring"><div class="story-img">D</div></div><div class="story-name">demo</div></div>
                </div>
                """, unsafe_allow_html=True)

                quick = ("<div class='quick-row'>"
                         "<a href='?tab=Ludo' class="
                         "'quick-pill'>🎲 Games</a>"
                         "<a href='?tab=Channel' class="
                         "'quick-pill'>📺 Channel</a>"
                         "<a href='?tab=Friends' class="
                         "'quick-pill'>👥 Friends</a>"
                         "</div>")
                st.markdown(quick, unsafe_allow_html=True)

                if SS.block_msg:
                    st.success(SS.block_msg)
                    SS.block_msg = ""

                visible = []
                for p in DB["posts"]:
                    if p.get("type") == "reel":
                        continue
                    if p["user"] in SS.blocked:
                        continue
                    if p["user"] in banned_list:
                        continue
                    visible.append(p)

                if SS.feed_sort == "Top Posts":
                    visible = sorted(
                        visible,
                        key=lambda x: len(x.get("likes",
                                                {})),
                        reverse=True)

                if SS.clear_cmt:
                    SS[SS.clear_cmt] = ""
                    SS.clear_cmt = ""

                for p in visible:

                    st.markdown(
                        "<div class='post-card'><div "
                        "class='post-header'>" +
                        avatar_html(p["user"],
                                    p.get("avatar"), 36) +
                        "<div class='post-username'>" +
                        p["user"] + "</div></div></div>",
                        unsafe_allow_html=True)

                    ptype = p.get("type", "text")
                    if ptype == "text":
                        st.markdown(
                            "<div class='post-ph' "
                            "style='background:" +
                            p.get("grad", "#f3f4f6") +
                            ";color:#056839;"
                            "font-weight:bold;'>" +
                            p.get("txt", "") + "</div>",
                            unsafe_allow_html=True)
                    elif ptype == "youtube":
                        yt = ('<iframe width="100%" '
                              'height="230" src='
                              '"https://www.youtube.com/'
                              'embed/' + p["ref"] +
                              '" frameborder="0" '
                              'allowfullscreen></iframe>')
                        components.html(yt, height=240)
                    elif ptype == "image":
                        if is_local_file(p["ref"]):
                            st.image(p["ref"],
                                     use_container_width
                                     =True)
                            with open(p["ref"],
                                      "rb") as fh:
                                st.download_button(
                                    "⬇️ Download",
                                    fh.read(),
                                    os.path.basename(
                                        p["ref"]),
                                    mime="image/png",
                                    key="dlb_" + p["id"])
                    elif ptype == "video":
                        st.video(p["ref"])
                        if is_local_file(p["ref"]):
                            with open(p["ref"],
                                      "rb") as fh:
                                st.download_button(
                                    "⬇️ Download",
                                    fh.read(),
                                    os.path.basename(
                                        p["ref"]),
                                    mime="video/mp4",
                                    key="dlb_" + p["id"])

                    liked = SS.username in p.get("likes", {})
                    vu_c, a1, a2, a3 = st.columns(
                        [1.8, 0.6, 0.6, 0.6])

                    if vu_c.button("👤 " + p["user"],
                                   key="vu_" + p["id"],
                                   use_container_width
                                   =True):
                        SS.view_user = p["user"]
                        safe_rerun()

                    ic = "❤️" if liked else "🤍"
                    if a1.button(ic, key="lk_" + p["id"],
                                 use_container_width=True):
                        db = load_db()
                        for post in db["posts"]:
                            if post["id"] == p["id"]:
                                lk = post.setdefault(
                                    "likes", {})
                                if SS.username in lk:
                                    del lk[SS.username]
                                else:
                                    lk[SS.username] = True
                                    if post["user"] != \
                                            SS.username:
                                        add_notification(
                                            post["user"],
                                            "❤️ @" +
                                            SS.username +
                                            " liked your "
                                            "post!")
                                break
                        save_db(db)
                        safe_rerun()
                    if a2.button("💬", key="cm_" + p["id"],
                                 use_container_width=True):
                        st.info("Comment box neeche hai.")
                    if a3.button("🚫", key="bl_" + p["id"],
                                 use_container_width=True):
                        db = load_db()
                        rec = db["users"].get(
                            SS.username, {})
                        bl = rec.setdefault("blocked", [])
                        if p["user"] not in bl:
                            bl.append(p["user"])
                            save_db(db)
                            SS.blocked = list(bl)
                            SS.block_msg = "@" + \
                                p["user"] + " blocked."
                        safe_rerun()

                    n = len(p.get("likes", {}))
                    st.markdown(
                        "<p class='likes-txt'>" + str(n) +
                        " likes</p><p class="
                        "'post-details'><b>" + p["user"] +
                        "</b> " + esc(p.get("cap", "")) +
                        "</p>", unsafe_allow_html=True)

                    cmt = st.text_input(
                        "comment", key="cmt_" + p["id"],
                        placeholder="Add a comment...",
                        label_visibility="collapsed")
                    if st.button("Post Comment",
                                 key="pc_" + p["id"]):
                        if cmt.strip():
                            if SS.comment_filter and \
                                    not comment_is_clean(
                                        cmt):
                                st.warning(
                                    "Blocked by filter!")
                            else:
                                db = load_db()
                                for post in db["posts"]:
                                    if post["id"] == \
                                            p["id"]:
                                        post.setdefault(
                                            "comments",
                                            []).append({
                                            "user":
                                            SS.username,
                                            "text": cmt})
                                        if post["user"] != \
                                                SS.username:
                                            add_notification(
                                                post["user"],
                                                "💬 @" +
                                                SS.username +
                                                ": " +
                                                cmt[:30])
                                        break
                                save_db(db)
                                SS.clear_cmt = "cmt_" + \
                                    p["id"]
                                safe_rerun()

                    for c in p.get("comments", []):
                        st.markdown(
                            "<p class='post-details' "
                            "style='color:#6b7280;'><b>" +
                            esc(c["user"]) + "</b> " +
                            esc(c["text"]) + "</p>",
                            unsafe_allow_html=True)

            # ================= FRIENDS =================
            elif SS.current_tab == "Friends":

                st.markdown('<div class="panel-header">👥 '
                            'Friends</div>',
                            unsafe_allow_html=True)

                db = load_db()
                incoming_fr = [r for r in
                               db["friend_requests"]
                               if r["to"] == SS.username]
                friends = db["friends"].get(
                    SS.username, [])

                st.markdown("### 📨 Requests (" +
                            str(len(incoming_fr)) + ")")
                if not incoming_fr:
                    st.caption("No new requests.")
                for i, r in enumerate(incoming_fr):
                    f = r["from"]
                    fu = db["users"].get(f, {})
                    st.markdown(
                        "<div class='fr-row'>" +
                        avatar_html(f, fu.get("avatar"),
                                    44) +
                        "<div><b>@" + esc(f) + "</b></div>"
                        "</div>", unsafe_allow_html=True)
                    fr1, fr2, fr3 = st.columns(3)
                    if fr2.button("✅ Accept",
                                  key="fr_acc_" + str(i),
                                  use_container_width=True):
                        accept_friend(SS.username, f)
                        safe_rerun()
                    if fr3.button("❌ Reject",
                                  key="fr_rej_" + str(i),
                                  use_container_width=True):
                        reject_friend(SS.username, f)
                        safe_rerun()
                    if fr1.button("👤",
                                  key="fr_view_" + str(i),
                                  use_container_width=True):
                        SS.view_user = f
                        safe_rerun()

                st.markdown("### 🧑‍🤝‍🧑 Your Friends (" +
                            str(len(friends)) + ")")
                if not friends:
                    st.caption("No friends yet!")
                for i, f in enumerate(friends):
                    fu = db["users"].get(f, {})
                    st.markdown(
                        "<div class='fr-row'>" +
                        avatar_html(f, fu.get("avatar"),
                                    44) +
                        "<div><b>@" + esc(f) + "</b></div>"
                        "</div>", unsafe_allow_html=True)
                    f1, f2, f3 = st.columns(3)
                    if f1.button("👤",
                                 key="fl_v_" + str(i),
                                 use_container_width=True):
                        SS.view_user = f
                        safe_rerun()
                    if f2.button("✉️",
                                 key="fl_m_" + str(i),
                                 use_container_width=True):
                        SS.msg_view = "chat"
                        SS.msg_target = f
                        SS.msg_target_type = "direct"
                        SS.current_tab = "Messages"
                        safe_rerun()
                    if f3.button("📞",
                                 key="fl_c_" + str(i),
                                 use_container_width=True):
                        start_call(SS.username, f)
                        safe_rerun()

                st.markdown("### 🌟 People You May Know")
                suggestions = []
                for un in db["users"]:
                    if un == SS.username or un in friends:
                        continue
                    if un in SS.blocked or un in banned_list:
                        continue
                    sent = any(
                        r["from"] == SS.username and
                        r["to"] == un
                        for r in db["friend_requests"])
                    if not sent:
                        suggestions.append(un)

                if not suggestions:
                    st.caption("No new people right now.")
                for un in suggestions:
                    su = db["users"].get(un, {})
                    st.markdown(
                        "<div class='fr-row'>" +
                        avatar_html(un, su.get("avatar"),
                                    44) +
                        "<div><b>@" + esc(un) + "</b></div>"
                        "</div>", unsafe_allow_html=True)
                    s1, s2 = st.columns(2)
                    if s1.button("➕ Add",
                                 key="sg_add_" + un,
                                 use_container_width=True):
                        send_friend_request(
                            SS.username, un)
                        safe_rerun()
                    if s2.button("👤",
                                 key="sg_v_" + un,
                                 use_container_width=True):
                        SS.view_user = un
                        safe_rerun()

            # ================= SEARCH =================
            elif SS.current_tab == "Search":

                st.markdown('<div class="panel-header">🔍 '
                            'Search</div>',
                            unsafe_allow_html=True)

                query = st.text_input(
                    "Search by username / ID",
                    key="search_input",
                    placeholder="🔍 Search users...")

                if query.strip():
                    q = query.strip().lower()
                    results = [(un, ud) for un, ud in
                               DB["users"].items()
                               if q in un.lower()
                               and un not in SS.blocked]

                    if not results:
                        st.info("❌ No users found!")
                    else:
                        for un, ud in results:
                            badge = ""
                            if un == owner:
                                badge = (" <span class="
                                         "'owner-badge'>👑"
                                         "</span>")
                            if un in banned_list:
                                badge += (" <span class="
                                          "'ban-tag'>🚫"
                                          "</span>")
                            st.markdown(
                                "<div class="
                                "'search-row'>" +
                                avatar_html(un,
                                            ud.get("avatar"),
                                            44) +
                                "<div><b>@" + un +
                                "</b>" + badge +
                                "</div></div>",
                                unsafe_allow_html=True)
                            s1, s2 = st.columns(2)
                            if s1.button("👤 View",
                                         key="sr_v_" + un,
                                         use_container_width
                                         =True):
                                SS.view_user = un
                                safe_rerun()
                            if s2.button("💬 Chat",
                                         key="sr_m_" + un,
                                         use_container_width
                                         =True):
                                SS.msg_view = "chat"
                                SS.msg_target = un
                                SS.msg_target_type = \
                                    "direct"
                                SS.current_tab = \
                                    "Messages"
                                safe_rerun()
                else:
                    st.caption("👆 Type any username!")

            # ================= CHANNEL =================
            elif SS.current_tab == "Channel":

                st.markdown(
                    "<div class='channel-banner'><h2>📺 " +
                    CHANNEL_NAME + "</h2><p>" +
                    CHANNEL_HANDLE + "</p></div>",
                    unsafe_allow_html=True)
                st.markdown("[🔗 Open on YouTube](" +
                            CHANNEL_URL + ")")

                if SS.yt_msg:
                    st.success(SS.yt_msg)
                    SS.yt_msg = ""

                with st.expander("➕ Add Video"):
                    yt_link = st.text_input(
                        "Paste YouTube video link",
                        key="ch_link")
                    if st.button("➕ Add",
                                 key="ch_add",
                                 use_container_width=True):
                        vid = parse_youtube_id(yt_link)
                        if vid:
                            db = load_db()
                            my_av = db["users"].get(
                                SS.username,
                                {}).get("avatar")
                            db["posts"].insert(0, {
                                "id":
                                uuid.uuid4().hex[:8],
                                "user": SS.username,
                                "type": "youtube",
                                "ref": vid,
                                "cap": "From " +
                                       CHANNEL_NAME,
                                "likes": {},
                                "comments": [],
                                "avatar": my_av,
                                "channel": True})
                            save_db(db)
                            SS.yt_msg = "Video added!"
                            safe_rerun()
                        else:
                            st.error("Invalid link!")

                ch_posts = [p for p in DB["posts"]
                            if p.get("channel")]
                if not ch_posts:
                    st.caption("No videos yet.")
                for p in reversed(ch_posts):
                    yt = ('<iframe width="100%" '
                          'height="190" src='
                          '"https://www.youtube.com/'
                          'embed/' + p["ref"] +
                          '" frameborder="0" '
                          'allowfullscreen></iframe>')
                    components.html(yt, height=200)

            # ================= REELS =================
            elif SS.current_tab == "Reels":

                st.markdown('<div class="panel-header">🎬 '
                            'Reels</div>',
                            unsafe_allow_html=True)
                reels = [p for p in DB["posts"]
                         if p.get("type") in ("reel",
                                              "video")
                         and p["user"] not in SS.blocked
                         and p["user"] not in banned_list]
                if not reels:
                    st.info("No reels yet!")
                for r in reversed(reels):
                    st.markdown(
                        "<div class='post-card'><div "
                        "class='post-header'>" +
                        avatar_html(r["user"],
                                    r.get("avatar"), 36) +
                        "<div class='post-username'>" +
                        r["user"] + "</div></div></div>",
                        unsafe_allow_html=True)
                    st.video(r["ref"])
                    if is_local_file(r["ref"]):
                        with open(r["ref"], "rb") as fh:
                            st.download_button(
                                "⬇️ Download",
                                fh.read(),
                                os.path.basename(
                                    r["ref"]),
                                mime="video/mp4",
                                key="dlr_" + r["id"])
                    liked = SS.username in r.get("likes",
                                                 {})
                    ra1, ra2 = st.columns(2)
                    ic = "❤️" if liked else "🤍"
                    if ra1.button(ic, key="rl_" + r["id"],
                                  use_container_width=True):
                        db = load_db()
                        for post in db["posts"]:
                            if post["id"] == r["id"]:
                                lk = post.setdefault(
                                    "likes", {})
                                if SS.username in lk:
                                    del lk[SS.username]
                                else:
                                    lk[SS.username] = True
                                break
                        save_db(db)
                        safe_rerun()
                    if ra2.button("✈️", key="rsh_" + r["id"],
                                  use_container_width=True):
                        st.info("Copied!")

            # ================= CREATE =================
            elif SS.current_tab == "Create":

                st.markdown('<div class="panel-header">➕ '
                            'Create</div>',
                            unsafe_allow_html=True)

                kind = st.radio("Post type:",
                                ["Photo", "Video",
                                 "Camera 🎨",
                                 "YouTube Link"],
                                horizontal=True,
                                key="create_kind")

                cap = st.text_input("Caption",
                                    key="up_cap")

                if kind == "YouTube Link":
                    yt_link = st.text_input(
                        "YouTube link", key="up_yt")
                    if st.button("🚀 Publish",
                                 key="up_publish",
                                 use_container_width=True):
                        vid = parse_youtube_id(yt_link)
                        if not vid:
                            st.error("Invalid link!")
                        else:
                            db = load_db()
                            my_av = db["users"].get(
                                SS.username,
                                {}).get("avatar")
                            db["posts"].insert(0, {
                                "id":
                                uuid.uuid4().hex[:8],
                                "user": SS.username,
                                "type": "youtube",
                                "ref": vid,
                                "cap": cap or "Video",
                                "likes": {},
                                "comments": [],
                                "avatar": my_av})
                            save_db(db)
                            SS.current_tab = "Home"
                            safe_rerun()

                elif kind == "Camera 🎨":

                    st.markdown(
                        "<p class='set-label'>🎨 Filter"
                        "</p>", unsafe_allow_html=True)
                    filt = st.selectbox("Filter:",
                                        FILTER_NAMES,
                                        key="cam_filter")
                    cam = st.camera_input(
                        "📸 Take photo", key="up_cam")

                    filtered_img = None
                    if cam is not None:
                        try:
                            pil = Image.open(cam)
                            filtered_img = apply_filter(
                                pil, filt)
                            buf = io.BytesIO()
                            filtered_img.save(
                                buf, format="PNG")
                            st.image(
                                buf.getvalue(),
                                caption="Filter: " +
                                filt)
                        except Exception as e:
                            st.error("Filter error: " +
                                     str(e))

                    if st.button("🚀 Publish",
                                 key="up_publish2",
                                 use_container_width=True):
                        if filtered_img is None:
                            st.warning(
                                "Pehle photo lein!")
                        else:
                            path = save_pil(
                                filtered_img)
                            db = load_db()
                            my_av = db["users"].get(
                                SS.username,
                                {}).get("avatar")
                            db["posts"].insert(0, {
                                "id":
                                uuid.uuid4().hex[:8],
                                "user": SS.username,
                                "type": "image",
                                "ref": path,
                                "cap": cap + " [" +
                                       filt + "]",
                                "likes": {},
                                "comments": [],
                                "avatar": my_av})
                            save_db(db)
                            SS.current_tab = "Home"
                            safe_rerun()

                else:
                    if kind == "Photo":
                        f = st.file_uploader(
                            "Choose photo",
                            type=["png", "jpg", "jpeg",
                                  "webp"],
                            key="up_photo")
                    else:
                        f = st.file_uploader(
                            "Choose video",
                            type=["mp4", "mov", "webm"],
                            key="up_video")

                    if st.button("🚀 Publish",
                                 key="up_publish3",
                                 use_container_width=True):
                        if f is None:
                            st.warning(
                                "File choose karein!")
                        else:
                            path = save_upload(f)
                            db = load_db()
                            my_av = db["users"].get(
                                SS.username,
                                {}).get("avatar")
                            ptype = "video" \
                                if kind == "Video" \
                                else "image"
                            db["posts"].insert(0, {
                                "id":
                                uuid.uuid4().hex[:8],
                                "user": SS.username,
                                "type": ptype,
                                "ref": path,
                                "cap": cap,
                                "likes": {},
                                "comments": [],
                                "avatar": my_av})
                            save_db(db)
                            SS.current_tab = "Home"
                            safe_rerun()

            # ================= MESSAGES =================
            elif SS.current_tab == "Messages":

                if HAS_REFRESH:
                    st_autorefresh(interval=4000,
                                   key="msg_ref")

                db = load_db()
                shot_install()

                if SS.msg_view == "chat":

                    tgt = SS.msg_target
                    is_group = (SS.msg_target_type ==
                                "group")

                    valid = True
                    group = None
                    if is_group:
                        for g in db["groups"]:
                            if g["id"] == tgt:
                                group = g
                                break
                        if group is None:
                            valid = False
                    else:
                        if tgt not in db["users"] or \
                                tgt in SS.blocked:
                            valid = False

                    if not valid:
                        SS.msg_view = "list"
                        safe_rerun()
                    else:

                        hb, ha, hi, hc = st.columns(
                            [0.1, 0.14, 0.5, 0.26])
                        if hb.button("←", key="ch_back"):
                            SS.msg_view = "list"
                            safe_rerun()

                        if is_group:
                            ha.markdown(
                                avatar_html(
                                    group["name"], None,
                                    40),
                                unsafe_allow_html=True)
                            hi.markdown(
                                "<b>" +
                                esc(group["name"]) +
                                "</b><br><span style="
                                "'font-size:11px;color:"
                                "#9ca3af;'>" +
                                str(len(group["members"]))
                                + " members</span>",
                                unsafe_allow_html=True)
                            msgs = sorted(
                                group["messages"],
                                key=lambda x: x["time"])
                        else:
                            u = db["users"][tgt]
                            mark_seen(SS.username, tgt)
                            ha.markdown(
                                avatar_html(
                                    tgt, u.get("avatar"),
                                    40),
                                unsafe_allow_html=True)
                            hi.markdown(
                                "<b>" +
                                esc(u.get("display_name",
                                          tgt)) +
                                "</b><br><span style="
                                "'font-size:11px;color:"
                                "#31a24c;'>● Active now"
                                "</span>",
                                unsafe_allow_html=True)
                            if hc.button("📞 Call",
                                         key="ch_call",
                                         use_container_width
                                         =True):
                                start_call(SS.username,
                                           tgt)
                                add_notification(
                                    tgt, "📞 @" +
                                    SS.username +
                                    " is calling you!")
                                safe_rerun()
                            convo = []
                            for m in db["messages"]:
                                if (m["from"] ==
                                        SS.username and
                                        m["to"] == tgt) \
                                        or \
                                        (m["from"] == tgt
                                         and m["to"] ==
                                         SS.username):
                                    convo.append(m)
                            msgs = sorted(
                                convo,
                                key=lambda x: x["time"])

                        st.markdown(
                            "<div class='enc-note'>🔒 "
                            "End-to-end encrypted (demo)"
                            "</div>",
                            unsafe_allow_html=True)

                        if not is_group:
                            if tgt in db.get(
                                    "friends", {}).get(
                                        SS.username, []):
                                st.markdown(
                                    "<div class="
                                    "'friend-note'>🤝 You "
                                    "and @" + esc(tgt) +
                                    " are now friends"
                                    "</div>",
                                    unsafe_allow_html=True)

                        pending = shot_check()
                        if pending and \
                                time.time() - \
                                SS.last_shot_time > 5:
                            SS.last_shot_time = \
                                time.time()
                            if is_group:
                                for mm in group[
                                        "members"]:
                                    if mm != \
                                            SS.username:
                                        add_notification(
                                            mm, "📸 @" +
                                            SS.username +
                                            " screenshot!")
                            else:
                                add_notification(
                                    tgt, "📸 @" +
                                    SS.username +
                                    " took a screenshot!")
                            safe_toast(
                                "📸 Screenshot detected!")
                            safe_rerun()

                        if SS.clear_msg:
                            SS[SS.clear_msg] = ""
                            SS.clear_msg = ""

                        if not msgs:
                            st.caption(
                                "No messages yet - say "
                                "hello! 👋")

                        for m in msgs:
                            mine = (m["from"] ==
                                    SS.username)
                            tstr = time.strftime(
                                "%I:%M %p",
                                time.localtime(
                                    m["time"])).lower()

                            if m.get("photo") and \
                                    is_local_file(
                                        m["photo"]):
                                st.image(m["photo"],
                                         width=200)

                            if mine:
                                cls = "bubble-me"
                            else:
                                cls = "bubble-them"
                            sender = ""
                            if is_group and not mine:
                                sender = ("<b>@" +
                                          esc(m["from"]) +
                                          "</b><br>")

                            st.markdown(
                                "<span class='" + cls +
                                "'>" + sender +
                                esc(m.get("text", "")) +
                                "<span class="
                                "'bubble-time'>" + tstr +
                                "</span></span>",
                                unsafe_allow_html=True)

                            r = m.get("reactions", [])
                            mkey = m.get(
                                "id", str(m["time"]))
                            if r:
                                btn = ("👍 " +
                                       str(len(r)))
                            else:
                                btn = "👍"
                            if st.button(
                                    btn,
                                    key="rx_" + mkey,
                                    use_container_width
                                    =False):
                                toggle_reaction(
                                    is_group, tgt,
                                    m.get("id"),
                                    SS.username)
                                safe_rerun()

                        with st.expander("📷 Send Photo"):
                            photo = st.file_uploader(
                                "Choose photo",
                                type=["png", "jpg",
                                      "jpeg", "webp"],
                                key="chat_photo")
                            if st.button(
                                    "📷 Send",
                                    key="chat_sendphoto",
                                    use_container_width
                                    =True):
                                if photo is None:
                                    st.warning(
                                        "Photo choose "
                                        "karein!")
                                else:
                                    path = save_upload(
                                        photo)
                                    send_chat_message(
                                        is_group, tgt,
                                        "📷 Photo",
                                        photo=path)
                                    safe_rerun()

                        if hasattr(st, "audio_input"):
                            audio = st.audio_input(
                                "🎙️ Record voice",
                                key="chat_voice")
                            if audio is not None:
                                st.audio(audio)
                                if st.button(
                                        "➡️ Send Voice",
                                        key="chat_sendvc",
                                        use_container_width
                                        =True):
                                    send_chat_message(
                                        is_group, tgt,
                                        "🎤 Voice "
                                        "message")
                                    st.success(
                                        "Voice sent!")
                                    safe_rerun()

                        txt = st.text_input(
                            "Message...", key="chat_txt")
                        if st.button("➡️ Send",
                                     key="chat_send",
                                     use_container_width
                                     =True):
                            if txt.strip():
                                send_chat_message(
                                    is_group, tgt,
                                    txt.strip())
                                SS.clear_msg = "chat_txt"
                                safe_rerun()

                else:

                    partners_all = set()
                    for m in db["messages"]:
                        if m["from"] == SS.username:
                            partners_all.add(m["to"])
                        elif m["to"] == SS.username:
                            partners_all.add(m["from"])

                    total_unread = 0
                    for p in partners_all:
                        if p != SS.username:
                            total_unread += unseen_count(
                                SS.username, p)

                    if total_unread > 0:
                        head = ("✉️ Chats <span class="
                                "'unread-badge'>" +
                                str(total_unread) +
                                "</span>")
                    else:
                        head = "✉️ Chats"
                    st.markdown(
                        '<div class="panel-header">' +
                        head + '</div>',
                        unsafe_allow_html=True)

                    search_q = st.text_input(
                        "🔍 Search chats",
                        key="msg_search")

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
                        if p == SS.username or \
                                p in SS.blocked or \
                                p in banned_list:
                            continue
                        if search_q and \
                                search_q.lower() \
                                not in p.lower():
                            continue
                        convo = []
                        for m in db["messages"]:
                            if (m["from"] ==
                                    SS.username and
                                    m["to"] == p) or \
                                    (m["from"] == p and
                                     m["to"] ==
                                     SS.username):
                                convo.append(m)
                        if convo:
                            last = convo[-1]
                        else:
                            last = None
                        un = unseen_count(SS.username, p)
                        convos.append({
                            "t": "direct", "u": p,
                            "last": last, "unread": un})

                    for g in db["groups"]:
                        if SS.username not in \
                                g["members"]:
                            continue
                        if search_q and \
                                search_q.lower() \
                                not in g["name"].lower():
                            continue
                        if g["messages"]:
                            last = g["messages"][-1]
                        else:
                            last = None
                        convos.append({
                            "t": "group", "g": g,
                            "last": last})

                    convos.sort(
                        key=lambda c: (
                            c["last"]["time"]
                            if c["last"] else 0),
                        reverse=True)

                    if not convos:
                        st.info("No chats yet!")

                    for c in convos:
                        if c["t"] == "direct":
                            p = c["u"]
                            u_data = db["users"].get(
                                p, {})
                            is_friend = p in \
                                db.get("friends",
                                       {}).get(
                                           SS.username,
                                           [])
                            if is_friend:
                                dot = ("<div class="
                                       "'online-dot'>"
                                       "</div>")
                            else:
                                dot = ""
                            name = esc(
                                u_data.get(
                                    "display_name", p))
                            if c["last"]:
                                if c["last"]["from"] == \
                                        SS.username:
                                    pre = "You: "
                                else:
                                    pre = ""
                                preview = pre + esc(
                                    c["last"].get(
                                        "text",
                                        ""))[:35]
                            else:
                                preview = "Say hello 👋"
                            av = avatar_html(
                                p,
                                u_data.get("avatar"),
                                46)
                            key_id = p
                        else:
                            g = c["g"]
                            dot = ""
                            name = "👥 " + esc(g["name"])
                            if c["last"]:
                                preview = ("@" +
                                           esc(c["last"]
                                               ["from"]) +
                                           ": " +
                                           esc(c["last"]
                                               .get("text",
                                                    ""))[:28])
                            else:
                                preview = "Group chat"
                            av = avatar_html(
                                g["name"], None, 46)
                            key_id = g["id"]

                        if c["last"]:
                            tm = time.strftime(
                                "%I:%M %p",
                                time.localtime(
                                    c["last"]["time"])
                            ).lower()
                        else:
                            tm = ""

                        badge = ""
                        if c.get("unread", 0) > 0:
                            badge = ("<span class="
                                     "'unread-badge'>"
                                     + str(
                                         c["unread"]) +
                                     "</span>")

                        row = ("<div class='chat-item'>"
                               "<div class='av-wrap'>"
                               + av + dot +
                               "</div><div class="
                               "'chat-info'><div class="
                               "'chat-name'>" + name +
                               "</div><div class="
                               "'chat-preview'>"
                               + preview +
                               "</div></div><div "
                               "style='text-align:"
                               "right;'><div class="
                               "'chat-time'>" + tm +
                               "</div>" + badge +
                               "</div></div>")

                        r1, r2 = st.columns(
                            [0.86, 0.14])
                        r1.markdown(
                            row, unsafe_allow_html=True)
                        if r2.button(
                                "💬",
                                key="op_" + key_id,
                                use_container_width
                                =True):
                            SS.msg_view = "chat"
                            SS.msg_target = key_id
                            if c["t"] == "direct":
                                SS.msg_target_type = \
                                    "direct"
                            else:
                                SS.msg_target_type = \
                                    "group"
                            safe_rerun()

                    with st.expander("➕ New Chat / Group"):
                        others = [x for x in db["users"]
                                  if x != SS.username
                                  and x not in
                                  SS.blocked
                                  and x not in
                                  banned_list]
                        if others:
                            pick = st.selectbox(
                                "Chat with:", others,
                                key="new_chat_sel")
                            if st.button(
                                    "💬 Start Chat",
                                    key="new_chat_btn",
                                    use_container_width
                                    =True):
                                SS.msg_view = "chat"
                                SS.msg_target = pick
                                SS.msg_target_type = \
                                    "direct"
                                safe_rerun()

                        gname = st.text_input(
                            "Group name",
                            key="g_name")
                        members = st.multiselect(
                            "Members", others,
                            key="g_members")
                        if st.button("Create Group",
                                     key="g_create",
                                     use_container_width
                                     =True):
                            if gname.strip() and members:
                                db = load_db()
                                db["groups"].append({
                                    "id": uuid.uuid4()
                                    .hex[:8],
                                    "name":
                                    gname.strip(),
                                    "members":
                                    [SS.username] +
                                    members,
                                    "messages": []})
                                save_db(db)
                                for m in members:
                                    add_notification(
                                        m, "👥 @" +
                                        SS.username +
                                        " added you "
                                        "to '" +
                                        gname + "'")
                                safe_rerun()
                            else:
                                st.warning("Naam aur "
                                           "members "
                                           "chunein!")

                    with st.expander("✨ Ask HMF AI"):
                        ai_q = st.text_input(
                            "Ask anything...",
                            key="ai_q")
                        if st.button("Ask", key="ai_btn"):
                            st.info(
                                hmf_ai_reply(ai_q))

            # ================= NOTIFICATIONS ============
            elif SS.current_tab == "Notifications":

                st.markdown('<div class="panel-header">🔔 '
                            'Notifications</div>',
                            unsafe_allow_html=True)

                db = load_db()
                my_notifs = [
                    n for n in db["notifications"]
                    if n.get("to") == SS.username][:40]

                if st.button("✅ Mark all read",
                             key="ntf_read",
                             use_container_width=True):
                    db = load_db()
                    for n in db["notifications"]:
                        if n.get("to") == SS.username:
                            n["read"] = True
                    save_db(db)
                    safe_rerun()

                if not my_notifs:
                    st.info("No notifications!")
                for n in my_notifs:
                    tstr = time.strftime(
                        "%d %b %H:%M",
                        time.localtime(n["time"]))
                    if n.get("read"):
                        dot = ""
                    else:
                        dot = ("<span class="
                               "'badge-dot'>NEW"
                               "</span>")
                    st.markdown(
                        "<div class='notif-row'>" +
                        n["text"] + dot +
                        "<br><span style="
                        "'font-size:11px;color:"
                        "#9ca3af;'>" + tstr +
                        "</span></div>",
                        unsafe_allow_html=True)

            # ================= LUDO =================
            elif SS.current_tab == "Ludo":

                st.markdown('<div class="panel-header">🎲 '
                            'Ludo</div>',
                            unsafe_allow_html=True)
                st.markdown(
                    "<div class='post-ph' style="
                    "'height:170px;font-size:34px;'>"
                    "🎲 LUDO</div>",
                    unsafe_allow_html=True)

                if st.button("🏆 Create Room Code",
                             use_container_width=True):
                    letters = ("ABCDEFGHJKLMNPQRSTUVWXYZ"
                               "23456789")
                    SS.room_code = "".join(
                        random.choices(letters, k=6))
                    safe_rerun()
                if SS.room_code:
                    st.success("Room Code: **" +
                               SS.room_code + "**")

                if st.button("🎲 Roll Dice",
                             use_container_width=True):
                    SS.dice = random.randint(1, 6)
                    if SS.dice == 6:
                        db = load_db()
                        u = db["users"].get(SS.username)
                        if u is not None:
                            u["coins"] = \
                                u.get("coins", 0) + 5
                            save_db(db)
                    safe_rerun()
                if SS.dice:
                    st.markdown(
                        "<h3 style='text-align:center;"
                        "color:#00B074;'>🎯 You rolled " +
                        str(SS.dice) + "</h3>",
                        unsafe_allow_html=True)

            # ================= PROFILE =================
            elif SS.current_tab == "Profile":

                st.markdown('<div class="panel-header">👤 '
                            'Profile</div>',
                            unsafe_allow_html=True)

                me_db = DB["users"].get(SS.username, {})
                my_posts = [p for p in DB["posts"]
                            if p["user"] == SS.username]
                my_friends = DB["friends"].get(
                    SS.username, [])

                st.markdown(
                    "<div style='text-align:center;"
                    "margin:10px 0;'>" +
                    avatar_html(SS.username,
                                me_db.get("avatar"), 86) +
                    "</div>", unsafe_allow_html=True)
                st.markdown(
                    "<h3 style='text-align:center;'>" +
                    esc(me_db.get("display_name",
                                  SS.username)) +
                    "</h3><p style='text-align:center;"
                    "color:#6b7280;font-size:13px;'>" +
                    esc(me_db.get("bio", "")) +
                    "</p><p style='text-align:center;"
                    "color:#00B074;font-size:12px;'>" +
                    str(len(my_posts)) + " Posts • " +
                    str(len(my_friends)) + " Friends</p>",
                    unsafe_allow_html=True)

                if is_owner:
                    st.markdown(
                        "<p style='text-align:center;'>"
                        "<span class='owner-badge'>👑 YOU "
                        "ARE THE OWNER</span></p>",
                        unsafe_allow_html=True)

                base = get_base_url()
                if base:
                    st.caption("🔗 Your profile link:")
                    st.code(base + "?profile=" +
                            SS.username)

                with st.expander("🖼️ Change Profile "
                                 "Picture"):
                    filt = st.selectbox(
                        "Filter:", FILTER_NAMES,
                        key="avatar_filter")
                    pic = st.file_uploader(
                        "Upload", type=["png", "jpg",
                                        "jpeg", "webp"],
                        key="avatar_up")
                    campic = st.camera_input(
                        "Or camera", key="avatar_cam")
                    if st.button("💾 Update Pic",
                                 key="avatar_save",
                                 use_container_width=True):
                        src = pic if pic is not None \
                            else campic
                        if src is None:
                            st.warning(
                                "Photo choose karein!")
                        else:
                            try:
                                pil = Image.open(src)
                                pil = apply_filter(
                                    pil, filt)
                                path = save_pil(pil)
                                db = load_db()
                                db["users"][
                                    SS.username][
                                    "avatar"] = path
                                save_db(db)
                                st.success("Updated!")
                                safe_rerun()
                            except Exception as e:
                                st.error("Failed: " +
                                         str(e))

                st.success("💰 Balance: **" +
                           str(me_db.get("coins", 0)) +
                           " Coins**")

                if st.button("💳 Withdrawal",
                             key="prof_wd",
                             use_container_width=True):
                    db = load_db()
                    u = db["users"].get(SS.username)
                    if u is not None and \
                            u.get("coins", 0) >= 100:
                        u["coins"] -= 100
                        save_db(db)
                        SS.withdraw_msg = \
                            "Payout submitted!"
                    else:
                        SS.withdraw_msg = \
                            "Min 100 coins!"
                    safe_rerun()
                if SS.withdraw_msg:
                    st.info(SS.withdraw_msg)
                    SS.withdraw_msg = ""

            # ================= SETTINGS =================
            elif SS.current_tab == "Settings":

                if SS.settings_page == "menu":

                    st.markdown(
                        '<div class="panel-header">⚙️ '
                        'Settings</div>',
                        unsafe_allow_html=True)
                    st.caption("@" + SS.username)

                    if is_owner:
                        if st.button(
                                "🛡️ OWNER PANEL ›",
                                key="m_admin",
                                use_container_width=True):
                            SS.settings_page = "admin"
                            safe_rerun()

                    items = [
                        ("🔐 Security Center", "security"),
                        ("📋 Personal Info", "personal"),
                        ("💰 Payments", "payments"),
                        ("📰 News Feed", "feed"),
                        ("🔔 Notifications",
                         "notifications"),
                        ("🌐 Language", "language"),
                        ("🛡️ Privacy Checkup", "privacy"),
                        ("🚫 Blocked Members", "blocked"),
                        ("⚠️ Report a Member", "reports"),
                        ("❓ Help Center", "help"),
                        ("ℹ️ About", "about"),
                    ]
                    for label, page in items:
                        if st.button(label + " ›",
                                     key="m_" + page,
                                     use_container_width
                                     =True):
                            SS.settings_page = page
                            safe_rerun()

                    if st.button("🚪 Logout",
                                 key="m_logout",
                                 use_container_width=True):
                        SS.logged_in = False
                        SS.page = "auth"
                        safe_rerun()

                elif SS.settings_page == "admin":
                    settings_back("bk_admin")
                    st.markdown(
                        '<div class="panel-header">🛡️ '
                        'Owner Panel</div>',
                        unsafe_allow_html=True)
                    if not is_owner:
                        st.error("Sirf owner!")
                    else:
                        db = load_db()
                        banned = db.get("banned", [])
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Users",
                                  len(db["users"]))
                        c2.metric("Posts",
                                  len(db["posts"]))
                        c3.metric("Reports",
                                  len(db["reports"]))
                        c4.metric("Banned", len(banned))

                        st.markdown("### 🚩 Reports")
                        if not db["reports"]:
                            st.caption("No reports.")
                        for i, r in enumerate(
                                reversed(db["reports"])):
                            ru = r.get("user", "")
                            rc1, rc2 = st.columns(
                                [0.65, 0.35])
                            rc1.markdown(
                                "🚩 **@" + esc(ru) +
                                "**<br><span style="
                                "'font-size:11px;color:"
                                "#9ca3af;'>By @" +
                                esc(r.get("from", "")) +
                                "</span>",
                                unsafe_allow_html=True)
                            if ru in banned:
                                if rc2.button(
                                        "✅ Unban",
                                        key="rp_unb_" +
                                        str(i),
                                        use_container_width
                                        =True):
                                    db = load_db()
                                    db["banned"].remove(
                                        ru)
                                    save_db(db)
                                    safe_rerun()
                            else:
                                if rc2.button(
                                        "🔨 BAN",
                                        key="rp_ban_" +
                                        str(i),
                                        use_container_width
                                        =True):
                                    db = load_db()
                                    db["banned"].append(
                                        ru)
                                    save_db(db)
                                    add_notification(
                                        ru, "🚫 Banned!")
                                    safe_rerun()

                        st.markdown("### 🔨 Ban by "
                                    "Username")
                        ban_input = st.text_input(
                            "Username",
                            key="owner_ban_in")
                        b1, b2 = st.columns(2)
                        if b1.button("🔨 Ban",
                                     key="owner_ban_btn",
                                     use_container_width
                                     =True):
                            u = ban_input.strip().lower()
                            db = load_db()
                            if not u or u == \
                                    SS.username:
                                st.warning("Invalid!")
                            elif u in db["users"]:
                                if u not in \
                                        db["banned"]:
                                    db["banned"].append(
                                        u)
                                    save_db(db)
                                    st.success(
                                        "Banned!")
                                    safe_rerun()
                            else:
                                st.warning(
                                    "User not found!")
                        if b2.button("✅ Unban",
                                     key="owner_unban_btn",
                                     use_container_width
                                     =True):
                            u = ban_input.strip().lower()
                            db = load_db()
                            if u in db["banned"]:
                                db["banned"].remove(u)
                                save_db(db)
                                st.success("Unbanned!")
                                safe_rerun()

                elif SS.settings_page == "security":
                    settings_back("bk_security")
                    score, tips = security_score()
                    st.progress(score / 100.0)
                    st.write("Score: **" + str(score) +
                             "/100**")
                    for t in tips:
                        st.markdown("• " + t)

                    fl_new = st.checkbox(
                        "👆 Fingerprint Lock",
                        value=SS.finger_lock,
                        key="finger_chk")
                    if fl_new != SS.finger_lock:
                        SS.finger_lock = fl_new
                        SS.finger_unlocked = not fl_new
                        safe_rerun()

                    if not SS.app_lock:
                        pin_set = st.text_input(
                            "4-digit PIN",
                            type="password",
                            key="pin_set", max_chars=4)
                        if st.button("🔒 Enable App Lock",
                                     key="pin_enable",
                                     use_container_width
                                     =True):
                            if len(pin_set) == 4 and \
                                    pin_set.isdigit():
                                SS.app_pin = pin_set
                                SS.app_lock = True
                                st.success("Enabled!")
                            else:
                                st.warning(
                                    "4 digits chahiye!")
                    else:
                        st.success("App Lock ON")
                        lc1, lc2 = st.columns(2)
                        if lc1.button("🔒 Lock Now",
                                      key="lock_now",
                                      use_container_width
                                      =True):
                            SS.pin_unlocked = False
                            safe_rerun()
                        if lc2.button("❌ Disable",
                                      key="pin_disable",
                                      use_container_width
                                      =True):
                            SS.app_lock = False
                            SS.pin_unlocked = True
                            safe_rerun()

                    SS.login_alerts = st.checkbox(
                        "📩 Login Alerts",
                        value=SS.login_alerts,
                        key="la_chk")
                    timeout_opts = [0, 5, 10, 30]
                    timeout_labels = ["Off", "5 min",
                                      "10 min",
                                      "30 min"]
                    if SS.auto_logout in timeout_opts:
                        cur = timeout_opts.index(
                            SS.auto_logout)
                    else:
                        cur = 0
                    sel = st.selectbox(
                        "Auto logout:",
                        timeout_labels, index=cur,
                        key="timeout_sel")
                    SS.auto_logout = timeout_opts[
                        timeout_labels.index(sel)]

                elif SS.settings_page == "personal":
                    settings_back("bk_personal")
                    me_db = DB["users"].get(
                        SS.username, {})
                    st.text_input("Username",
                                  value=SS.username,
                                  disabled=True,
                                  key="pi_user")
                    dn = st.text_input(
                        "Display Name",
                        value=me_db.get("display_name",
                                        ""),
                        key="st_dn")
                    bio = st.text_input(
                        "Bio",
                        value=me_db.get("bio", ""),
                        key="st_bio")
                    if st.button("💾 Save",
                                 key="st_save",
                                 use_container_width=True):
                        db = load_db()
                        u = db["users"].get(
                            SS.username)
                        if u is not None:
                            u["display_name"] = dn
                            u["bio"] = bio
                            save_db(db)
                        st.success("Saved!")

                elif SS.settings_page == "payments":
                    settings_back("bk_payments")
                    me_db = DB["users"].get(
                        SS.username, {})
                    st.success("Balance: **" +
                               str(me_db.get("coins",
                                             0)) +
                               " Coins**")
                    if st.button("💳 Payout",
                                 key="pay_wd",
                                 use_container_width=True):
                        db = load_db()
                        u = db["users"].get(
                            SS.username)
                        if u is not None and \
                                u.get("coins", 0) >= 100:
                            u["coins"] -= 100
                            save_db(db)
                            SS.withdraw_msg = \
                                "Payout submitted!"
                        else:
                            SS.withdraw_msg = \
                                "Min 100 coins!"
                        safe_rerun()
                    if SS.withdraw_msg:
                        st.info(SS.withdraw_msg)
                        SS.withdraw_msg = ""

                elif SS.settings_page == "feed":
                    settings_back("bk_feed")
                    SS.feed_sort = st.radio(
                        "Sort by:",
                        ["Most Recent", "Top Posts"],
                        key="feed_sort_radio")
                    SS.show_stories = st.checkbox(
                        "Show Stories",
                        value=SS.show_stories,
                        key="stories_chk")
                    SS.comment_filter = st.checkbox(
                        "🛡️ Comment Filter",
                        value=SS.comment_filter,
                        key="cfilter_chk")

                elif SS.settings_page == "notifications":
                    settings_back("bk_notif")
                    SS.notif["likes"] = st.checkbox(
                        "❤️ Likes",
                        value=SS.notif["likes"],
                        key="ntf_l")
                    SS.notif["comments"] = st.checkbox(
                        "💬 Comments",
                        value=SS.notif["comments"],
                        key="ntf_c")
                    SS.notif["follows"] = st.checkbox(
                        "👥 Followers",
                        value=SS.notif["follows"],
                        key="ntf_f")
                    SS.notif["messages"] = st.checkbox(
                        "✉️ Messages",
                        value=SS.notif["messages"],
                        key="ntf_m")

                elif SS.settings_page == "language":
                    settings_back("bk_lang")
                    SS.language = st.radio(
                        "Language:",
                        ["English", "Urdu"],
                        key="lang_radio")

                elif SS.settings_page == "privacy":
                    settings_back("bk_privacy")
                    st.progress(
                        min(SS.privacy_step / 4, 1.0))
                    if SS.privacy_step == 0:
                        if st.button("🚀 Start",
                                     key="pc_start",
                                     use_container_width
                                     =True):
                            SS.privacy_step = 1
                            safe_rerun()
                    elif SS.privacy_step == 1:
                        SS.private_account = \
                            st.checkbox(
                                "Private Account",
                                value=SS.
                                private_account,
                                key="priv_chk")
                        if st.button("Next →",
                                     key="pc_next1",
                                     use_container_width
                                     =True):
                            SS.privacy_step = 2
                            safe_rerun()
                    elif SS.privacy_step == 2:
                        st.write("Blocked: " +
                                 str(len(
                                     SS.blocked)))
                        if st.button("Next →",
                                     key="pc_next2",
                                     use_container_width
                                     =True):
                            SS.privacy_step = 3
                            safe_rerun()
                    else:
                        st.success("Complete!")
                        if st.button("Done",
                                     key="pc_done",
                                     use_container_width
                                     =True):
                            SS.settings_page = "menu"
                            SS.privacy_step = 0
                            safe_rerun()

                elif SS.settings_page == "blocked":
                    settings_back("bk_blocked")
                    block_input = st.text_input(
                        "Username", key="block_input")
                    if st.button("🚫 Block",
                                 key="block_btn",
                                 use_container_width=True):
                        u = block_input.strip().lower()
                        if not u or u == SS.username:
                            st.warning("Invalid!")
                        elif u in SS.blocked:
                            st.warning(
                                "Already blocked!")
                        else:
                            db = load_db()
                            rec = db["users"].get(
                                SS.username)
                            if rec is not None:
                                rec.setdefault(
                                    "blocked",
                                    []).append(u)
                                save_db(db)
                            SS.blocked.append(u)
                            safe_rerun()
                    for i, u in enumerate(SS.blocked):
                        bc1, bc2 = st.columns(
                            [0.6, 0.4])
                        bc1.markdown(
                            "**🚫 @" + u + "**")
                        if bc2.button(
                                "Unblock",
                                key="ub_" + str(i),
                                use_container_width
                                =True):
                            db = load_db()
                            rec = db["users"].get(
                                SS.username)
                            if rec is not None and \
                                    u in rec.get(
                                        "blocked",
                                        []):
                                rec["blocked"]\
                                    .remove(u)
                                save_db(db)
                            SS.blocked.remove(u)
                            safe_rerun()

                elif SS.settings_page == "reports":
                    settings_back("bk_reports")
                    if SS.report_msg:
                        st.success(SS.report_msg)
                        SS.report_msg = ""
                    rep_id = st.text_input(
                        "Member ID", key="rep_id")
                    reasons = ["Harassment", "Abusive",
                               "Spam", "Fake Account",
                               "Scam", "Other"]
                    reason = st.selectbox(
                        "Reason", reasons,
                        key="rep_reason")
                    if st.button("🚩 Submit",
                                 key="rep_btn",
                                 use_container_width=True):
                        r = rep_id.strip().lower()
                        if r:
                            db = load_db()
                            db["reports"].append({
                                "from": SS.username,
                                "user": r,
                                "reason": reason,
                                "time": time.time()})
                            save_db(db)
                            if owner:
                                add_notification(
                                    owner,
                                    "🚩 Report: @" + r +
                                    " (by @" +
                                    SS.username + ")")
                            SS.report_msg = \
                                "Report owner ko gayi!"
                            safe_rerun()
                        else:
                            st.warning("Enter ID!")

                elif SS.settings_page == "help":
                    settings_back("bk_help")
                    st.markdown(
                        "• **Nav** - neeche taskbar "
                        "icons\n"
                        "• **Theme** - topbar ☀️/🌙\n"
                        "• **Chats** - Messenger style "
                        "+ reactions 👍\n"
                        "• **Owner** - first new signup 👑")

                elif SS.settings_page == "about":
                    settings_back("bk_about")
                    st.markdown(
                        "**HMF book** v10.0.0\n\n"
                        "Instagram-style UI • Fixed "
                        "Taskbar • Messenger Chats\n\n"
                        "© 2025 HMF - All rights "
                        "reserved.")

        # ---------- FIXED BOTTOM NAV ----------
        nav_items = [
            ("Home", "🏠"), ("Search", "🔍"),
            ("Friends", "👥"), ("Reels", "🎬"),
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

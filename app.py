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

SALT = "hmf_book_secret_2025"
DB_FILE = "hmf_db.json"
UPLOAD_DIR = "uploads"
FILTER_NAMES = ["None", "Beauty", "Sepia", "Vintage",
                "Cool", "Grayscale", "Bright", "Cartoon"]
GRADS = ["linear-gradient(45deg,#d1fae5,#a7f3d0)",
         "linear-gradient(45deg,#ecfdf5,#6ee7b7)",
         "linear-gradient(45deg,#e6f7f0,#b3e6cc)"]
VALID_TABS = ["Home", "Search", "Friends", "Groups",
              "Pages", "Events", "Marketplace", "Ads",
              "Channel", "Reels", "Create", "Messages",
              "Notifications", "Ludo", "Profile",
              "Settings"]
BAD_WORDS = ["stupid", "idiot", "hate", "dumb", "ugly"]
CHANNEL_URL = "https://www.youtube.com/@ColorPopCartoons83"
APP_INFO = {"name": "HMF Book",
            "founded": "February 4, 2026",
            "founders": "Mehmood Sial, Hoor-e-Jannat, Farwa",
            "parent": "HMF Group",
            "hq": "Bahawalpur / Okara, Pakistan"}


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


def parse_yt(url):
    url = (url or "").strip()
    if len(url) == 11 and "/" not in url:
        return url
    for t in ("youtu.be/", "v=", "/shorts/", "/embed/"):
        if t in url:
            p = url.split(t)[1]
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
    for k in ("users", "messages", "posts", "groups",
              "notifications", "reports", "banned",
              "friend_requests", "pages", "events",
              "listings", "ads"):
        if k not in db:
            db[k] = []
    for k in ("friends", "seen"):
        if k not in db:
            db[k] = {}
    if "owner" not in db:
        db["owner"] = ""
    return db


def save_db(db):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=1)
    except Exception:
        pass


def get_u(name):
    return load_db()["users"].get(name, {})


def set_pref(name, key, val):
    db = load_db()
    u = db["users"].get(name)
    if u is not None:
        u[key] = val
        save_db(db)


def add_notification(to_user, text, kind="messages"):
    if not to_user:
        return
    db = load_db()
    u = db["users"].get(to_user)
    if u is not None:
        prefs = u.get("notif", {"likes": True,
                                "comments": True,
                                "follows": True,
                                "messages": True})
        if kind in prefs and not prefs.get(kind, True):
            return
    db["notifications"].insert(0, {
        "to": to_user, "text": text,
        "time": time.time(), "read": False})
    db["notifications"] = db["notifications"][:200]
    save_db(db)


def unread_count(user):
    db = load_db()
    return sum(1 for x in db["notifications"]
               if x.get("to") == user and not x.get("read"))


def unseen_count(me, partner):
    db = load_db()
    last = db.get("seen", {}).get(me, {}).get(partner, 0)
    return sum(1 for m in db["messages"]
               if m["from"] == partner and m["to"] == me
               and m.get("time", 0) > last)


def mark_seen(me, partner):
    db = load_db()
    db.setdefault("seen", {}).setdefault(
        me, {})[partner] = time.time()
    save_db(db)


def text_clean(text):
    low = text.lower()
    for w in BAD_WORDS:
        if w in low:
            return False
    return True


def send_msg(is_group, gid, to_user, text, photo=None):
    me = st.session_state.username
    db = load_db()
    m = {"id": uuid.uuid4().hex[:8], "from": me,
         "text": text, "time": time.time(),
         "reactions": []}
    if photo:
        m["photo"] = photo
    if is_group:
        for g in db["groups"]:
            if g["id"] == gid:
                g["messages"].append(m)
                break
        save_db(db)
        db2 = load_db()
        for g in db2["groups"]:
            if g["id"] == gid:
                for mm in g["members"]:
                    if mm != me:
                        add_notification(
                            mm, "👥 '" + g["name"] +
                            "': @" + me + " " + text[:25])
                break
    else:
        m["to"] = to_user
        db["messages"].append(m)
        save_db(db)
        add_notification(to_user, "✉️ @" + me +
                         " sent you a message")


def toggle_rx(is_group, gid, mid, user):
    db = load_db()
    if is_group:
        for g in db["groups"]:
            if g["id"] == gid:
                for m in g["messages"]:
                    if m.get("id") == mid:
                        rr = m.setdefault("reactions", [])
                        if user in rr:
                            rr.remove(user)
                        else:
                            rr.append(user)
                        break
                break
    else:
        for m in db["messages"]:
            if m.get("id") == mid:
                rr = m.setdefault("reactions", [])
                if user in rr:
                    rr.remove(user)
                else:
                    rr.append(user)
                break
    save_db(db)


def start_call(a, b):
    try:
        with open("calls.json", "r") as f:
            c = json.load(f)
    except Exception:
        c = {"active": {}, "history": []}
    cid = uuid.uuid4().hex[:8]
    c["active"][cid] = {"id": cid, "from": a, "to": b,
                        "status": "ringing",
                        "start": time.time()}
    try:
        with open("calls.json", "w") as f:
            json.dump(c, f)
    except Exception:
        pass


def answer_call(cid, accept):
    try:
        with open("calls.json", "r") as f:
            c = json.load(f)
    except Exception:
        return
    if cid in c["active"]:
        if accept:
            c["active"][cid]["status"] = "active"
        else:
            c["active"][cid]["status"] = "ended"
        try:
            with open("calls.json", "w") as f:
                json.dump(c, f)
        except Exception:
            pass


def end_call(cid):
    try:
        with open("calls.json", "r") as f:
            c = json.load(f)
    except Exception:
        return
    if cid in c["active"]:
        c["active"].pop(cid)
        try:
            with open("calls.json", "w") as f:
                json.dump(c, f)
        except Exception:
            pass


def incoming_call(user):
    try:
        with open("calls.json", "r") as f:
            c = json.load(f)
        for cid, call in c["active"].items():
            if call.get("to") == user and \
                    call.get("status") == "ringing":
                return call
    except Exception:
        pass
    return None


def save_upload(fobj):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = fobj.name.split(".")[-1].lower()
    if ext not in ("png", "jpg", "jpeg", "webp",
                   "mp4", "mov", "webm"):
        ext = "bin"
    p = os.path.join(UPLOAD_DIR,
                     uuid.uuid4().hex + "." + ext)
    with open(p, "wb") as o:
        o.write(fobj.getbuffer())
    return p


def save_pil(img):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    p = os.path.join(UPLOAD_DIR,
                     uuid.uuid4().hex + ".png")
    img.save(p, "PNG")
    return p


def av_html(name, path=None, size=36, border=False):
    bs = "border:4px solid #fff;" if border else ""
    if path and os.path.exists(path):
        try:
            b64 = base64.b64encode(
                open(path, "rb").read()).decode()
            return ("<img src='data:image/png;base64," + b64 +
                    "' style='width:" + str(size) +
                    "px;height:" + str(size) +
                    "px;border-radius:50%;object-fit:"
                    "cover;margin-right:8px;" + bs + "'>")
        except Exception:
            pass
    ini = esc(str(name)[:2].upper())
    return ("<div style='width:" + str(size) +
            "px;height:" + str(size) +
            "px;border-radius:50%;background:linear-"
            "gradient(135deg,#00B074,#056839);color:#fff;"
            "display:flex;align-items:center;justify-"
            "content:center;font-weight:bold;margin-"
            "right:8px;" + bs + "font-size:" +
            str(int(size * 0.38)) + "px;'>" + ini + "</div>")


def apply_filter(img, name):
    try:
        im = img.convert("RGB")
        if name == "Beauty":
            b = im.filter(ImageFilter.GaussianBlur(3))
            o = Image.blend(im, b, 0.5)
            o = ImageEnhance.Brightness(o).enhance(1.1)
            o = ImageEnhance.Color(o).enhance(1.15)
        elif name == "Sepia":
            o = ImageOps.colorize(im.convert("L"),
                                  "#704214", "#ffe8c0")
        elif name == "Vintage":
            o = ImageOps.colorize(im.convert("L"),
                                  "#3a2a1a", "#e8d8b0")
        elif name == "Cool":
            o = ImageOps.colorize(im.convert("L"),
                                  "#20304a", "#c8e0ff")
        elif name == "Grayscale":
            o = im.convert("L").convert("RGB")
        elif name == "Bright":
            o = ImageEnhance.Brightness(im).enhance(1.4)
        elif name == "Cartoon":
            s = im.resize((max(1, im.width // 6),
                           max(1, im.height // 6)))
            s = s.filter(ImageFilter.MedianFilter(7))
            o = s.resize((im.width, im.height))
            o = ImageOps.posterize(o, 5)
            o = ImageEnhance.Color(o).enhance(1.3)
        else:
            o = im
        return o
    except Exception:
        return img


def is_local(ref):
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


# ---------- SEED ----------
DB = load_db()
SEED = [("demo", "demo@hmfbook.com", "1234",
         "Demo User", "21 Dec 1996", "Male"),
        ("hoor_jannat", "hoor@hmfbook.com", "1234",
         "Hoor Jannat", "14 Mar 2000", "Female"),
        ("farrukh_m", "farrukh@hmfbook.com", "1234",
         "Farrukh M", "5 Jan 1995", "Male"),
        ("zara_x", "zara@hmfbook.com", "1234",
         "Zara X", "9 Sep 1999", "Female")]
ch = False
for un, ml, pw, nm, bd, gn in SEED:
    if un in DB["banned"]:
        continue
    if un not in DB["users"]:
        DB["users"][un] = {
            "email": ml, "password": hash_pw(pw),
            "display_name": nm, "bio": "Hi!",
            "birthday": bd, "gender": gn,
            "coins": 550, "followers": 200,
            "blocked": [], "avatar": None,
            "fails": 0, "lock_until": 0,
            "app_lock": False, "app_pin": "",
            "finger_lock": False, "two_fa": False,
            "login_alerts": True, "auto_logout": 0,
            "comment_filter": True, "feed_sort":
            "Most Recent", "show_stories": True,
            "notif": {"likes": True, "comments": True,
                      "follows": True, "messages": True}}
        ch = True
if not DB["posts"]:
    DB["posts"] = [
        {"id": "s1", "user": "hoor_jannat", "type":
         "youtube", "ref": "aqz-KE-bpKQ", "cap":
         "Big Buck Bunny!", "likes": {},
         "comments": []},
        {"id": "s2", "user": "farrukh_m", "type":
         "text", "grad": GRADS[0], "txt":
         "Ludo Night", "cap": "Tonight 8 PM!",
         "likes": {}, "comments": []}]
    ch = True
if not DB["pages"]:
    DB["pages"].append({"id": "pg1", "name":
                        "HMF Official", "category": "Brand",
                        "owner": "demo", "description":
                        "Official page!", "followers": []})
    ch = True
if not DB["events"]:
    DB["events"].append({"id": "ev1", "title":
                         "HMF Meetup", "description": "Milte hain!",
                         "host": "demo", "location": "Bahawalpur",
                         "date": "2026-03-15", "time": "6 PM",
                         "rsvps": []})
    ch = True
if not DB["listings"]:
    DB["listings"].append({"id": "ls1", "seller":
                           "farrukh_m", "title": "Gaming Mouse",
                           "description": "RGB, almost new",
                           "price": 1500, "category": "Electronics",
                           "image": None, "location": "Okara",
                           "status": "available"})
    ch = True
if ch:
    save_db(DB)


# ---------- SESSION ----------
SS = st.session_state
for k, v in {
        "page": "splash", "logged_in": False,
        "username": "", "email": "", "auth_mode":
        "login", "current_tab": "Home",
        "settings_page": "menu", "blocked": [],
        "clear_cmt": "", "clear_msg": "",
        "block_msg": "", "report_msg": "",
        "withdraw_msg": "", "yt_msg": "",
        "view_user": None, "open_group": "",
        "open_page": "", "open_event": "",
        "open_listing": "", "pin_unlocked": True,
        "finger_unlocked": True, "pin_attempts": 0,
        "pin_lock_until": 0, "pin_msg": "",
        "msg_view": "list", "msg_target": "",
        "msg_target_type": "direct",
        "last_shot_time": 0, "twofa_code": "",
        "last_active": 0, "dark_mode": False,
        "dice": 0, "room_code": ""}.items():
    if k not in SS:
        SS[k] = v

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
def css_main(dark):
    if dark:
        T = {"BG": "#0f1110", "CARD": "#1b1e1b",
             "BR": "#2a2e2a", "T1": "#eef1ee",
             "T2": "#9aa69a", "LG": "#00e08a"}
    else:
        T = {"BG": "#f0f2f5", "CARD": "#ffffff",
             "BR": "#e5e7eb", "T1": "#1f2937",
             "T2": "#4b5563", "LG": "#00B074"}
    c = """
    <style>
    .stApp{background-color:BG !important}
    header[data-testid="stHeader"],#MainMenu,footer,
    [data-testid="stToolbar"],[data-testid="stStatusWidget"],
    [data-testid="stDecoration"]{display:none !important}
    .block-container,[data-testid="block-container"]{
    max-width:430px;margin:0 auto;background:CARD;
    padding:0 10px 95px !important;min-height:100vh;
    box-shadow:0 0 35px rgba(0,0,0,.18)}
    .topbar{position:sticky;top:0;z-index:995;display:flex;
    justify-content:space-between;align-items:center;
    padding:12px 14px;background:CARD;border-bottom:
    1px solid BR;margin:0 -10px}
    .logo{font-size:25px;font-weight:700;font-family:
    'Segoe Script','Brush Script MT',cursive;color:T1}
    .ticons a{font-size:20px;text-decoration:none;
    margin-left:13px;position:relative}
    .ndot{position:absolute;top:-6px;right:-10px;
    background:#e53e3e;color:#fff;border-radius:10px;
    font-size:10px;font-weight:700;padding:1px 5px}
    .stories{display:flex;gap:14px;padding:12px 4px;
    border-bottom:1px solid BR;overflow-x:auto}
    .sc{display:flex;flex-direction:column;align-items:
    center;min-width:62px}
    .ring{width:56px;height:56px;border-radius:50%;
    padding:2.5px;background:linear-gradient(135deg,
    #00B074,#056839);display:flex;align-items:center;
    justify-content:center}
    .ringg{background:#dbdbdb}
    .rim{width:100%;height:100%;border-radius:50%;
    background:CARD;border:2px solid CARD;display:flex;
    align-items:center;justify-content:center;font-weight:
    bold;color:T2;font-size:13px}
    .snm{font-size:11px;color:T2;margin-top:4px}
    .qr{display:flex;gap:8px;padding:10px 0 4px;
    flex-wrap:wrap}
    .qp{text-align:center;padding:6px 10px;border:1px
    solid BR;border-radius:20px;font-size:12px;
    text-decoration:none;color:T1;font-weight:600}
    .pc{background:CARD;border-bottom:1px solid BR;
    margin-bottom:10px}
    .ph2{display:flex;align-items:center;padding:10px 4px}
    .pun{font-size:14px;font-weight:700;color:T1}
    .pph{width:100%;height:280px;background:#f3f4f6;
    display:flex;align-items:center;justify-content:
    center;font-size:15px}
    .lk{padding:6px 2px 0;font-weight:600;font-size:13px;
    color:T1;margin:0}
    .pd{padding:0 2px 8px;font-size:14px;color:T1;margin:0}
    .phdr{padding:16px 4px;font-size:20px;font-weight:
    bold;color:LG;border-bottom:1px solid BR;
    text-align:center}
    .sl{font-weight:700;color:T1;margin:12px 0 4px}
    .nr{padding:10px 4px;border-bottom:1px solid BR;
    font-size:14px;color:T1}
    .bdot{background:#e53e3e;color:#fff;border-radius:50%;
    padding:2px 8px;font-size:11px;font-weight:700;
    margin-left:6px}
    .ob{background:linear-gradient(135deg,#f59e0b,
    #d97706);color:#fff;padding:2px 10px;border-radius:
    12px;font-size:11px;font-weight:bold}
    .ci{display:flex;align-items:center;padding:11px 4px;
    border-bottom:1px solid BR}
    .aw{position:relative;margin-right:6px}
    .odot{position:absolute;bottom:2px;right:2px;width:
    12px;height:12px;border-radius:50%;background:
    #31a24c;border:2px solid CARD}
    .cinf{flex:1;min-width:0}
    .cnm{font-weight:700;font-size:14px;color:T1}
    .cpv{font-size:12.5px;color:T2;overflow:hidden;
    text-overflow:ellipsis;white-space:nowrap;margin-top:2px}
    .ctm{font-size:11px;color:T2}
    .ub{background:#00B074;color:#fff;border-radius:50%;
    min-width:20px;height:20px;display:inline-flex;
    align-items:center;justify-content:center;font-size:
    11px;font-weight:700;padding:0 6px;margin-top:4px}
    .bme{background:#00B074;color:#fff;padding:8px 13px;
    border-radius:18px 18px 4px 18px;max-width:78%;
    margin:3px 0 3px auto;font-size:14px;display:block;
    width:fit-content}
    .bth{background:BR;color:T1;padding:8px 13px;
    border-radius:18px 18px 18px 4px;max-width:78%;
    margin:3px auto 3px 0;font-size:14px;display:block;
    width:fit-content}
    .btm{font-size:10px;opacity:.75;display:block;
    text-align:right;margin-top:2px}
    .enc{text-align:center;font-size:11px;color:T2;
    background:rgba(0,176,116,.07);border-radius:10px;
    padding:6px 10px;margin:6px 0}
    .fr{display:flex;align-items:center;padding:10px 4px;
    border-bottom:1px solid BR}
    .sr{display:flex;align-items:center;padding:10px 4px;
    border-bottom:1px solid BR}
    .lkscr{display:flex;flex-direction:column;align-items:
    center;justify-content:center;height:55vh;text-align:
    center}
    .fbi{font-size:70px;margin-bottom:10px}
    .fbc{height:115px;border-radius:0 0 14px 14px;
    background:linear-gradient(135deg,#00B074,#056839);
    margin:0 -10px}
    .fbn{font-size:22px}
    .fbs{font-size:13px;color:T2}
    .gc{border:1px solid BR;border-radius:12px;padding:
    12px;margin-bottom:10px}
    .gcv{height:65px;border-radius:8px;background:
    linear-gradient(135deg,#00B074,#056839);
    margin-bottom:8px}
    .gnm{font-weight:800;font-size:15px;color:T1}
    .gsb{font-size:12px;color:T2}
    .adc{border:2px solid #f59e0b;border-radius:12px;
    padding:12px;margin:10px 0;background:rgba(245,
    158,11,.06)}
    .adt{background:#f59e0b;color:#fff;padding:2px 8px;
    border-radius:8px;font-size:10px;font-weight:700}
    .nav{position:fixed;bottom:0;left:50%;transform:
    translateX(-50%);width:100%;max-width:430px;
    background:CARD;border-top:1px solid BR;display:
    flex;justify-content:space-around;align-items:
    center;padding:10px 0 14px;z-index:998}
    .nav a{font-size:22px;text-decoration:none;filter:
    grayscale(1) opacity(.45);position:relative;
    line-height:1}
    .nav a.on{filter:none;transform:scale(1.12)}
    .call{background:CARD;border:2px solid #00B074;
    border-radius:14px;padding:12px;margin:8px 0;
    display:flex;align-items:center;gap:12px}
    div[data-testid="stButton"]>button,
    div.stButton>button{background:#00B074 !important;
    color:#fff !important;font-weight:600 !important;
    border:none !important;border-radius:12px !important}
    div[data-testid="stButton"]>button:hover{
    background:#056839 !important;color:#fff !important}
    </style>
    """
    for k, v in T.items():
        c = c.replace(k, v)
    if dark:
        c += """
        <style>
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea{
        background:#242824 !important;color:#fff
        !important;border-color:#3a3f3a !important}
        [data-testid="stCheckbox"] label p,
        [data-testid="stRadio"] label p{color:#e5e9e5
        !important}
        </style>
        """
    return c


# ================= SPLASH =================
if SS.page == "splash":
    st.markdown("""
    <style>
    .stApp{background:linear-gradient(135deg,#00B074,
    #056839) !important}
    header[data-testid="stHeader"],#MainMenu,footer,
    [data-testid="stToolbar"],[data-testid=
    "stDecoration"]{display:none !important}
    .mid{display:flex;flex-direction:column;align-items:
    center;justify-content:center;height:60vh;
    text-align:center}
    .lgo{font-size:90px;font-weight:900;color:#fff;
    letter-spacing:4px;margin:0}
    .sub{font-size:24px;color:rgba(255,255,255,.92)}
    div[data-testid="stButton"]>button{background:#fff
    !important;color:#00B074 !important;font-size:18px
    !important;font-weight:bold !important;padding:12px
    45px !important;border-radius:30px !important;border:
    none !important}
    </style>
    <div class="mid"><h1 class="lgo">HMF</h1>
    <p class="sub">HMF Book</p></div>
    """, unsafe_allow_html=True)
    if st.button("Get Started", use_container_width=True):
        SS.page = "auth"
        safe_rerun()


# ================= AUTH =================
elif SS.page == "auth":

    sup = SS.auth_mode == "signup"
    title = "Create Account" if sup else "Welcome Back"
    btn = "Sign Up" if sup else "Login"

    st.markdown(css_main(False), unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;"
                "margin-top:14px;'><div style="
                "'background:linear-gradient(135deg,"
                "#00B074,#056839);display:inline-block;"
                "padding:16px 48px;border-radius:22px;'>"
                "<h1 style='color:#fff;font-size:34px;"
                "margin:0;font-weight:900;letter-spacing:"
                "3px;'>HMF</h1></div></div>",
                unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>" +
                title + "</h2>", unsafe_allow_html=True)

    un = st.text_input("Username", placeholder="username")
    if sup:
        em = st.text_input("Email", placeholder="email")
    pw = st.text_input("Password", type="password")

    if st.button(btn, use_container_width=True):
        u = un.strip().lower()
        db = load_db()
        if not u or not pw:
            st.error("Dono fields bharin!")
        elif u in db["banned"]:
            st.error("🚫 PERMANENTLY BANNED!")
        elif sup:
            if u in db["users"]:
                st.error("Username taken!")
            else:
                made_owner = not db.get("owner")
                if made_owner:
                    db["owner"] = u
                db["users"][u] = {
                    "email": em, "password": hash_pw(pw),
                    "display_name": u.title(), "bio": "Hi!",
                    "birthday": "Not set", "gender": "Not set",
                    "coins": 100, "followers": 0, "blocked": [],
                    "avatar": None, "fails": 0,
                    "lock_until": 0, "app_lock": False,
                    "app_pin": "", "finger_lock": False,
                    "two_fa": False, "login_alerts": True,
                    "auto_logout": 0, "comment_filter": True,
                    "feed_sort": "Most Recent",
                    "show_stories": True,
                    "notif": {"likes": True, "comments": True,
                              "follows": True,
                              "messages": True}}
                save_db(db)
                SS.logged_in = True
                SS.username = u
                SS.page = "app"
                SS.pin_unlocked = True
                SS.finger_unlocked = True
                SS.last_active = time.time()
                add_notification(u, "👋 Welcome to HMF Book!")
                if made_owner:
                    st.balloons()
                safe_rerun()
        else:
            rec = db["users"].get(u)
            if rec and rec.get("lock_until", 0) > time.time():
                st.error("🔒 Locked! Wait " + str(int(
                    rec["lock_until"] - time.time()) + 1) +
                    "s")
            elif rec and pw_ok(rec.get("password", ""), pw):
                rec["fails"] = 0
                rec["lock_until"] = 0
                save_db(db)
                SS.logged_in = True
                SS.username = u
                SS.blocked = rec.get("blocked", [])
                SS.last_active = time.time()
                # 2FA check
                if rec.get("two_fa"):
                    SS.twofa_code = str(random.randint(
                        100000, 999999))
                    SS.page = "twofa"
                else:
                    SS.page = "app"
                    SS.pin_unlocked = not rec.get(
                        "app_lock", False)
                    SS.finger_unlocked = not rec.get(
                        "finger_lock", False)
                    if rec.get("login_alerts"):
                        add_notification(u, "📩 New login "
                                         "detected")
                safe_rerun()
            elif rec:
                rec["fails"] = rec.get("fails", 0) + 1
                if rec["fails"] >= 5:
                    rec["lock_until"] = time.time() + 60
                    rec["fails"] = 0
                    st.error("🔒 5 wrong! Locked 60s.")
                else:
                    st.error("Wrong! " + str(5 - rec["fails"])
                             + " left.")
                save_db(db)
            else:
                st.error("Invalid username or password!")

    if st.button("Switch to " +
                 ("Login" if sup else "Sign Up")):
        SS.auth_mode = "login" if sup else "signup"
        safe_rerun()
    st.caption("Demo: demo/1234 • First signup = Owner 👑")


# ================= 2FA =================
elif SS.page == "twofa" and SS.logged_in:
    st.markdown(css_main(False), unsafe_allow_html=True)
    st.markdown("<div class='lkscr'><div class='fbi'>🔑"
                "</div><h2>Two-Factor Verification</h2>"
                "<p style='color:#6b7280;'>6-digit code "
                "enter karein</p></div>",
                unsafe_allow_html=True)
    st.info("Demo code: **" + SS.twofa_code + "**")
    code_in = st.text_input("Enter code", max_chars=6)
    if st.button("✅ Verify", use_container_width=True):
        if code_in == SS.twofa_code:
            rec = get_u(SS.username)
            SS.page = "app"
            SS.pin_unlocked = not rec.get("app_lock", False)
            SS.finger_unlocked = not rec.get(
                "finger_lock", False)
            if rec.get("login_alerts"):
                add_notification(SS.username,
                                 "📩 New login detected")
            safe_rerun()
        else:
            st.error("Wrong code!")
    if st.button("🚪 Logout", use_container_width=True):
        SS.logged_in = False
        SS.page = "auth"
        safe_rerun()


# ================= MAIN =================
elif SS.page == "app" and SS.logged_in:

    db = load_db()
    me = db["users"].get(SS.username, {})
    owner = db.get("owner", "")
    is_owner = SS.username == owner

    need_pin = me.get("app_lock") and not SS.pin_unlocked
    need_f = me.get("finger_lock") and not SS.finger_unlocked

    # ---- LOCK SCREENS (asli mein kaam karte hain!) ----
    if need_f or need_pin:

        st.markdown(css_main(SS.dark_mode),
                    unsafe_allow_html=True)

        if need_f:
            st.markdown("<div class='lkscr'><div class="
                        "'fbi'>👆</div><h2>Fingerprint "
                        "Lock</h2><p style='color:"
                        "#6b7280;'>Tap to scan</p></div>",
                        unsafe_allow_html=True)
            if st.button("👆 Scan Fingerprint",
                         use_container_width=True):
                time.sleep(1.2)
                SS.finger_unlocked = True
                add_notification(SS.username,
                                 "👆 Unlocked with fingerprint")
                safe_rerun()
            if st.button("🚪 Logout",
                         use_container_width=True):
                SS.logged_in = False
                SS.page = "auth"
                safe_rerun()
        else:
            st.markdown("<div class='lkscr'><div class="
                        "'fbi'>🔐</div><h2>App Locked"
                        "</h2><p style='color:#6b7280;'>"
                        "4-digit PIN</p></div>",
                        unsafe_allow_html=True)
            if SS.pin_lock_until > time.time():
                st.error("Locked " + str(int(
                    SS.pin_lock_until - time.time()) + 1)
                    + "s")
            else:
                pin_in = st.text_input("PIN",
                                       type="password",
                                       max_chars=4)
                if st.button("🔓 Unlock",
                             use_container_width=True):
                    if pin_in == me.get("app_pin"):
                        SS.pin_unlocked = True
                        SS.pin_attempts = 0
                        safe_rerun()
                    else:
                        SS.pin_attempts += 1
                        if SS.pin_attempts >= 3:
                            SS.pin_lock_until = \
                                time.time() + 30
                            SS.pin_attempts = 0
                        st.error("Wrong PIN!")

    else:
        st.markdown(css_main(SS.dark_mode),
                    unsafe_allow_html=True)
        DB = load_db()

        now = time.time()
        al = me.get("auto_logout", 0)
        if al > 0 and SS.last_active > 0 and \
                now - SS.last_active > al * 60:
            SS.logged_in = False
            SS.page = "auth"
            safe_rerun()
        SS.last_active = now

        unread = unread_count(SS.username)
        banned = DB.get("banned", [])

        # ---- INCOMING CALL ----
        inc = incoming_call(SS.username)
        if inc:
            st.markdown("<div class='call'><div style="
                        "'font-size:24px;'>📞</div><div>"
                        "<b>Incoming: @" + esc(inc["from"]) +
                        "</b></div></div>",
                        unsafe_allow_html=True)
            i1, i2 = st.columns(2)
            if i1.button("✅ Accept", key="ca"):
                answer_call(inc["id"], True)
                add_notification(inc["from"], "📞 " +
                                 SS.username + " accepted!")
                safe_rerun()
            if i2.button("❌ Reject", key="cr"):
                answer_call(inc["id"], False)
                safe_rerun()

        # ---- TOPBAR ----
        if SS.dark_mode:
            dh, di = "?dark=0", "☀️"
        else:
            dh, di = "?dark=1", "🌙"
        nb = ""
        if unread > 0:
            nb = "<span class='ndot'>" + str(unread) + \
                 "</span>"
        st.markdown("<div class='topbar'><div class="
                    "'logo'>HMF Book</div><div class="
                    "'ticons'><a href='?tab=Messages'>✉️</a>"
                    "<a href='?tab=Notifications'>🔔" + nb +
                    "</a><a href='" + dh + "'>" + di +
                    "</a><a href='?tab=Settings'>⚙️</a></div>"
                    "</div>", unsafe_allow_html=True)

        # ---- VIEW USER ----
        if SS.view_user and SS.view_user != SS.username:
            vu = SS.view_user
            if vu not in DB["users"]:
                SS.view_user = None
                safe_rerun()
            ud = DB["users"][vu]
            mp = [p for p in DB["posts"]
                  if p["user"] == vu]
            tf = DB["friends"].get(vu, [])
            st.markdown("<div class='fbc'></div>",
                        unsafe_allow_html=True)
            st.markdown("<div style='text-align:center;"
                        "margin-top:-50px;'>" +
                        av_html(vu, ud.get("avatar"), 100,
                                border=True) + "</div>",
                        unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:center;"
                        "margin:8px 0 2px;'>" +
                        esc(ud.get("display_name", vu)) +
                        "</h3><p style='text-align:center;"
                        "color:#6b7280;font-size:13px;'>" +
                        str(len(tf)) + " friends · " +
                        str(len(mp)) + " posts</p>",
                        unsafe_allow_html=True)
            af = vu in DB["friends"].get(SS.username, [])
            v1, v2, v3 = st.columns(3)
            if v1.button("✅ Friend" if af else "➕ Add",
                         key="vfa"):
                if not af:
                    db = load_db()
                    db["friend_requests"].append(
                        {"from": SS.username, "to": vu,
                         "time": now})
                    save_db(db)
                    add_notification(vu, "👋 @" +
                                     SS.username +
                                     " sent request!", "follows")
                    safe_rerun()
            if v2.button("✉️ Msg", key="vfm"):
                SS.msg_view = "chat"
                SS.msg_target = vu
                SS.msg_target_type = "direct"
                SS.current_tab = "Messages"
                SS.view_user = None
                safe_rerun()
            if v3.button("📞 Call", key="vfc"):
                start_call(SS.username, vu)
                add_notification(vu, "📞 @" + SS.username +
                                 " is calling!")
                safe_rerun()
            if st.button("← Back", key="vb"):
                SS.view_user = None
                safe_rerun()

        else:
            if SS.view_user == SS.username:
                SS.view_user = None
                SS.current_tab = "Profile"

            # ============ HOME ============
            if SS.current_tab == "Home":

                if me.get("show_stories", True):
                    st.markdown("""
                    <div class="stories">
                    <div class="sc"><div class="ring ringg"><div class="rim">+</div></div><div class="snm">Your Story</div></div>
                    <div class="sc"><div class="ring"><div class="rim">HJ</div></div><div class="snm">hoor_jannat</div></div>
                    <div class="sc"><div class="ring"><div class="rim">FM</div></div><div class="snm">farrukh_m</div></div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(("<div class='qr'>"
                             "<a href='?tab=Groups' class="
                             "'qp'>👥 Groups</a>"
                             "<a href='?tab=Pages' class="
                             "'qp'>📄 Pages</a>"
                             "<a href='?tab=Events' class="
                             "'qp'>📅 Events</a>"
                             "<a href='?tab=Marketplace' class="
                             "'qp'>🛒 Market</a>"
                             "<a href='?tab=Ads' class="
                             "'qp'>📢 Ads</a>"
                             "<a href='?tab=Ludo' class="
                             "'qp'>🎲 Ludo</a></div>"),
                            unsafe_allow_html=True)

                vis = [p for p in DB["posts"]
                       if p.get("type") != "reel"
                       and p["user"] not in SS.blocked
                       and p["user"] not in banned]
                if me.get("feed_sort") == "Top Posts":
                    vis = sorted(vis, key=lambda x: len(
                        x.get("likes", {})), reverse=True)

                ads = [a for a in DB["ads"]
                       if a.get("status") == "active"]

                if SS.clear_cmt:
                    SS[SS.clear_cmt] = ""
                    SS.clear_cmt = ""

                for idx, p in enumerate(vis):

                    st.markdown("<div class='pc'><div class="
                                "'ph2'>" + av_html(
                                    p["user"],
                                    p.get("avatar"), 36) +
                                "<div class='pun'>" +
                                esc(p["user"]) + "</div>"
                                "</div></div>",
                                unsafe_allow_html=True)
                    pt = p.get("type", "text")
                    if pt == "text":
                        st.markdown("<div class='pph' style="
                                    "'background:" +
                                    p.get("grad", "#f0f0f0") +
                                    ";color:#056839;font-"
                                    "weight:bold;'>" +
                                    esc(p.get("txt", "")) +
                                    "</div>",
                                    unsafe_allow_html=True)
                    elif pt == "youtube":
                        components.html(
                            '<iframe width="100%" height="225" '
                            'src="https://www.youtube.com/embed/'
                            + p["ref"] + '" frameborder="0" '
                            'allowfullscreen></iframe>',
                            height=235)
                    elif pt == "image" and is_local(p["ref"]):
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
                                            " liked!",
                                            "likes")
                                break
                        save_db(db)
                        safe_rerun()
                    if c2.button("💬", key="cm_" + p["id"],
                                 use_container_width=True):
                        st.info("Box neeche hai.")
                    if c3.button("👤", key="vu_" + p["id"],
                                 use_container_width=True):
                        SS.view_user = p["user"]
                        safe_rerun()
                    if c4.button("🚫", key="bl_" + p["id"],
                                 use_container_width=True):
                        db = load_db()
                        rec = db["users"].get(
                            SS.username, {})
                        bl = rec.setdefault("blocked", [])
                        if p["user"] not in bl:
                            bl.append(p["user"])
                            save_db(db)
                            SS.blocked = list(bl)
                        safe_rerun()

                    st.markdown("<p class='lk'>" + str(len(
                        p.get("likes", {}))) + " likes</p>"
                        "<p class='pd'><b>" + esc(p["user"]) +
                        "</b> " + esc(p.get("cap", "")) +
                        "</p>", unsafe_allow_html=True)

                    cm = st.text_input("comment",
                                       key="cmt_" + p["id"],
                                       placeholder=
                                       "Add a comment...",
                                       label_visibility=
                                       "collapsed")
                    if st.button("Post",
                                 key="pc_" + p["id"]):
                        if cm.strip():
                            if me.get("comment_filter",
                                      True) and \
                                    not text_clean(cm):
                                st.warning("🛡️ Blocked "
                                           "by filter!")
                            else:
                                db = load_db()
                                for post in db["posts"]:
                                    if post["id"] == \
                                            p["id"]:
                                        post.setdefault(
                                            "comments",
                                            []).append(
                                            {"user":
                                             SS.username,
                                             "text": cm})
                                        break
                                save_db(db)
                                SS.clear_cmt = "cmt_" + \
                                    p["id"]
                                safe_rerun()

                    for c in p.get("comments", []):
                        st.markdown("<p class='pd' style="
                                    "'color:#6b7280;'><b>" +
                                    esc(c["user"]) +
                                    "</b> " + esc(c["text"]) +
                                    "</p>",
                                    unsafe_allow_html=True)

                    if ads and (idx + 1) % 3 == 0:
                        ad = ads[(idx // 3) % len(ads)]
                        st.markdown("<div class='adc'><span "
                                    "class='adt'>📢 SPONSORED"
                                    "</span><br><b>" +
                                    esc(ad["title"]) +
                                    "</b><br><span style="
                                    "'font-size:13px;color:"
                                    "#6b7280;'>" +
                                    esc(ad.get("text", "")) +
                                    "</span><br><a href='" +
                                    esc(ad.get("link", "#")) +
                                    "' target='_blank' style="
                                    "'color:#00B074;'>🔗 "
                                    "Learn More</a></div>",
                                    unsafe_allow_html=True)

            # ============ GROUPS ============
            elif SS.current_tab == "Groups":

                if SS.open_group:
                    grp = next((g for g in DB["groups"]
                                if g["id"] ==
                                SS.open_group), None)
                    if grp is None:
                        SS.open_group = ""
                        safe_rerun()
                    else:
                        if st.button("← Back",
                                     key="gb"):
                            SS.open_group = ""
                            safe_rerun()
                        st.markdown("<div class='gc'><div "
                                    "class='gcv'></div><div "
                                    "class='gnm'>👥 " +
                                    esc(grp["name"]) +
                                    "</div><div class='gsb'>" +
                                    str(len(grp["members"])) +
                                    " members · " +
                                    grp["privacy"] +
                                    "</div></div>",
                                    unsafe_allow_html=True)
                        ism = SS.username in grp["members"]
                        if grp["privacy"] == "public":
                            lbl = "✅ Leave" if ism \
                                else "➕ Join"
                            if st.button(lbl, key="gj",
                                         use_container_width
                                         =True):
                                db = load_db()
                                for g in db["groups"]:
                                    if g["id"] == \
                                            grp["id"]:
                                        if ism:
                                            g["members"]\
                                                .remove(
                                                    SS.username)
                                        else:
                                            g["members"]\
                                                .append(
                                                    SS.username)
                                        break
                                save_db(db)
                                safe_rerun()
                        else:
                            if not ism:
                                if st.button("➕ Request",
                                             key="gr",
                                             use_container_width
                                             =True):
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
                                st.success("Member ho aap!")

                        if grp.get("requests"):
                            st.markdown("**Requests:**")
                            for rq in grp["requests"]:
                                rc1, rc2 = st.columns(2)
                                rc1.markdown("@" + esc(rq))
                                if rc2.button("✅",
                                              key="ga_" + rq):
                                    db = load_db()
                                    for g in db["groups"]:
                                        if g["id"] == \
                                                grp["id"]:
                                            g["requests"]\
                                                .remove(rq)
                                            g["members"]\
                                                .append(rq)
                                            break
                                    save_db(db)
                                    safe_rerun()

                        if ism:
                            gt = st.text_input("Post...",
                                               key="gpt")
                            if st.button("🚀 Post",
                                         key="gpb",
                                         use_container_width
                                         =True):
                                if gt.strip():
                                    db = load_db()
                                    db["posts"].insert(0, {
                                        "id": uuid.uuid4()
                                        .hex[:8],
                                        "user": SS.username,
                                        "type": "text",
                                        "grad": random.choice(
                                            GRADS),
                                        "txt": esc(gt)[:40],
                                        "cap": gt.strip(),
                                        "groupId":
                                        grp["id"],
                                        "likes": {},
                                        "comments": []})
                                    save_db(db)
                                    safe_rerun()
                        gp = [p for p in DB["posts"]
                              if p.get("groupId") ==
                              grp["id"]]
                        for p in gp:
                            st.markdown("<div class='gc'><b>@"
                                        + esc(p["user"]) +
                                        "</b><br>" +
                                        esc(p.get("cap", "")) +
                                        "</div>",
                                        unsafe_allow_html=True)
                else:
                    st.markdown("<div class='phdr'>👥 "
                                "Groups</div>",
                                unsafe_allow_html=True)
                    with st.expander("➕ Create Group"):
                        gn = st.text_input("Name", key="ngn")
                        gp_ = st.selectbox("Privacy",
                                           ["public",
                                            "private"],
                                           key="ngp")
                        if st.button("Create", key="ngb",
                                     use_container_width
                                     =True):
                            if gn.strip():
                                db = load_db()
                                db["groups"].append({
                                    "id": uuid.uuid4()
                                    .hex[:8],
                                    "name": gn.strip(),
                                    "privacy": gp_,
                                    "createdBy":
                                    SS.username,
                                    "members":
                                    [SS.username],
                                    "requests": [],
                                    "messages": []})
                                save_db(db)
                                safe_rerun()
                    for g in DB["groups"]:
                        st.markdown("<div class='gc'><div "
                                    "class='gcv'></div><div "
                                    "class='gnm'>" +
                                    esc(g["name"]) +
                                    "</div><div class='gsb'>"
                                    + str(len(g["members"])) +
                                    " members · " +
                                    g["privacy"] +
                                    "</div></div>",
                                    unsafe_allow_html=True)
                        if st.button("Open",
                                     key="go_" + g["id"],
                                     use_container_width
                                     =True):
                            SS.open_group = g["id"]
                            safe_rerun()

            # ============ PAGES ============
            elif SS.current_tab == "Pages":
                if SS.open_page:
                    pg = next((p for p in DB["pages"]
                                if p["id"] ==
                                SS.open_page), None)
                    if pg is None:
                        SS.open_page = ""
                        safe_rerun()
                    else:
                        if st.button("← Back", key="pb"):
                            SS.open_page = ""
                            safe_rerun()
                        st.markdown("<div class='fbc'></div>",
                                    unsafe_allow_html=True)
                        st.markdown("<h3 style='text-align:"
                                    "center;margin-top:-"
                                    "30px;'>📄 " +
                                    esc(pg["name"]) +
                                    "</h3><p style='text-"
                                    "align:center;color:"
                                    "#6b7280;font-size:"
                                    "13px;'>" +
                                    esc(pg.get("category",
                                               "")) + " · " +
                                    str(len(pg.get(
                                        "followers", []))) +
                                    " followers</p>",
                                    unsafe_allow_html=True)
                        own = pg["owner"] == SS.username
                        fol = SS.username in pg.get(
                            "followers", [])
                        if own:
                            pt2 = st.text_input(
                                "Post as page", key="ppt")
                            if st.button("🚀 Post as Page",
                                         key="ppb",
                                         use_container_width
                                         =True):
                                if pt2.strip():
                                    db = load_db()
                                    db["posts"].insert(0, {
                                        "id": uuid.uuid4()
                                        .hex[:8],
                                        "user": pg["name"],
                                        "type": "text",
                                        "grad": random.choice(
                                            GRADS),
                                        "txt": esc(pt2)[:40],
                                        "cap": pt2.strip(),
                                        "pageId":
                                        pg["id"],
                                        "likes": {},
                                        "comments": []})
                                    save_db(db)
                                    safe_rerun()
                        else:
                            lbl = "❤️ Following" if fol \
                                else "➕ Follow"
                            if st.button(lbl, key="pf",
                                         use_container_width
                                         =True):
                                db = load_db()
                                for p in db["pages"]:
                                    if p["id"] == pg["id"]:
                                        fl = p.setdefault(
                                            "followers", [])
                                        if fol:
                                            fl.remove(
                                                SS.username)
                                        else:
                                            fl.append(
                                                SS.username)
                                        break
                                save_db(db)
                                safe_rerun()
                        pp = [p for p in DB["posts"]
                              if p.get("pageId") == pg["id"]]
                        for p in pp:
                            st.markdown("<div class='gc'><b>📄"
                                        + esc(p["user"]) +
                                        "</b><br>" +
                                        esc(p.get("cap", "")) +
                                        "</div>",
                                        unsafe_allow_html=True)
                else:
                    st.markdown("<div class='phdr'>📄 "
                                "Pages</div>",
                                unsafe_allow_html=True)
                    with st.expander("➕ Create Page"):
                        pn = st.text_input("Name", key="npn")
                        pc_ = st.text_input("Category",
                                            key="npc")
                        if st.button("Create", key="npb",
                                     use_container_width
                                     =True):
                            if pn.strip():
                                db = load_db()
                                db["pages"].append({
                                    "id": uuid.uuid4()
                                    .hex[:8],
                                    "name": pn.strip(),
                                    "category": pc_,
                                    "owner": SS.username,
                                    "followers": []})
                                save_db(db)
                                safe_rerun()
                    for pg in DB["pages"]:
                        st.markdown("<div class='gc'><div "
                                    "class='gnm'>📄 " +
                                    esc(pg["name"]) +
                                    "</div><div class='gsb'>"
                                    + esc(pg.get("category",
                                                 "")) +
                                    "</div></div>",
                                    unsafe_allow_html=True)
                        if st.button("Open",
                                     key="po_" + pg["id"],
                                     use_container_width
                                     =True):
                            SS.open_page = pg["id"]
                            safe_rerun()

            # ============ EVENTS ============
            elif SS.current_tab == "Events":
                if SS.open_event:
                    ev = next((e for e in DB["events"]
                                if e["id"] ==
                                SS.open_event), None)
                    if ev is None:
                        SS.open_event = ""
                        safe_rerun()
                    else:
                        if st.button("← Back", key="eb"):
                            SS.open_event = ""
                            safe_rerun()
                        st.markdown("<div class='gc'><div "
                                    "class='gcv'></div><div "
                                    "class='gnm'>📅 " +
                                    esc(ev["title"]) +
                                    "</div><div class='gsb'>📍 "
                                    + esc(ev.get("location",
                                                 "")) + " · "
                                    + esc(ev.get("date", "")) +
                                    " " + esc(ev.get("time",
                                                     "")) +
                                    "</div></div>",
                                    unsafe_allow_html=True)
                        st.caption(ev.get("description", ""))
                        going = sum(1 for r in ev.get(
                            "rsvps", []) if r["status"] ==
                            "going")
                        st.markdown("✅ **" + str(going) +
                                    " going**")
                        e1, e2, e3 = st.columns(3)
                        if e1.button("✅ Going", key="eg"):
                            db = load_db()
                            for e in db["events"]:
                                if e["id"] == ev["id"]:
                                    e["rsvps"] = [
                                        r for r in e.get(
                                            "rsvps", [])
                                        if r["user"] !=
                                        SS.username]
                                    e["rsvps"].append(
                                        {"user": SS.username,
                                         "status": "going"})
                            save_db(db)
                            safe_rerun()
                        if e2.button("🌟 Maybe", key="ei"):
                            db = load_db()
                            for e in db["events"]:
                                if e["id"] == ev["id"]:
                                    e["rsvps"] = [
                                        r for r in e.get(
                                            "rsvps", [])
                                        if r["user"] !=
                                        SS.username]
                                    e["rsvps"].append(
                                        {"user": SS.username,
                                         "status":
                                         "interested"})
                            save_db(db)
                            safe_rerun()
                        if e3.button("❌ No", key="en"):
                            db = load_db()
                            for e in db["events"]:
                                if e["id"] == ev["id"]:
                                    e["rsvps"] = [
                                        r for r in e.get(
                                            "rsvps", [])
                                        if r["user"] !=
                                        SS.username]
                            save_db(db)
                            safe_rerun()
                else:
                    st.markdown("<div class='phdr'>📅 "
                                "Events</div>",
                                unsafe_allow_html=True)
                    with st.expander("➕ Create Event"):
                        et = st.text_input("Title", key="net")
                        el = st.text_input("Location",
                                           key="nel")
                        ed = st.text_input("Date (15 Mar "
                                           "2026)", key="ned")
                        if st.button("Create", key="neb",
                                     use_container_width
                                     =True):
                            if et.strip():
                                db = load_db()
                                db["events"].append({
                                    "id": uuid.uuid4()
                                    .hex[:8],
                                    "title": et.strip(),
                                    "host": SS.username,
                                    "location": el,
                                    "date": ed,
                                    "rsvps": []})
                                save_db(db)
                                safe_rerun()
                    for ev in DB["events"]:
                        st.markdown("<div class='gc'><div "
                                    "class='gnm'>📅 " +
                                    esc(ev["title"]) +
                                    "</div><div class='gsb'>📍 "
                                    + esc(ev.get("location",
                                                 "")) +
                                    "</div></div>",
                                    unsafe_allow_html=True)
                        if st.button("Open",
                                     key="eo_" + ev["id"],
                                     use_container_width
                                     =True):
                            SS.open_event = ev["id"]
                            safe_rerun()

            # ============ MARKETPLACE ============
            elif SS.current_tab == "Marketplace":
                if SS.open_listing:
                    ls = next((l for l in DB["listings"]
                                if l["id"] ==
                                SS.open_listing), None)
                    if ls is None:
                        SS.open_listing = ""
                        safe_rerun()
                    else:
                        if st.button("← Back", key="mb"):
                            SS.open_listing = ""
                            safe_rerun()
                        st.markdown("<div class='phdr'>🛒 " +
                                    esc(ls["title"]) +
                                    "</div>",
                                    unsafe_allow_html=True)
                        if ls.get("image") and \
                                is_local(ls["image"]):
                            st.image(ls["image"],
                                     use_container_width
                                     =True)
                        st.markdown("<h2 style='color:"
                                    "#00B074;'>PKR " +
                                    str(ls["price"]) +
                                    "</h2>",
                                    unsafe_allow_html=True)
                        st.write(ls.get("description", ""))
                        st.caption("📍 " + ls.get("location",
                                                  "") +
                                   " · @" + ls["seller"])
                        if ls["status"] == "sold":
                            st.error("❌ SOLD")
                        elif ls["seller"] == SS.username:
                            if st.button("✅ Mark Sold",
                                         key="msold",
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
                            if st.button("✉️ Message Seller",
                                         key="msgsl",
                                         use_container_width
                                         =True):
                                send_msg(False, "",
                                         ls["seller"],
                                         "🛒 Interested in '"
                                         + ls["title"] +
                                         "'")
                                SS.msg_view = "chat"
                                SS.msg_target = ls["seller"]
                                SS.msg_target_type = \
                                    "direct"
                                SS.current_tab = "Messages"
                                SS.open_listing = ""
                                safe_rerun()
                else:
                    st.markdown("<div class='phdr'>🛒 "
                                "Marketplace</div>",
                                unsafe_allow_html=True)
                    with st.expander("➕ Sell"):
                        st_ = st.text_input("Title",
                                            key="slt")
                        sd = st.text_area("Desc",
                                          key="sld",
                                          height=60)
                        sp = st.number_input("PKR",
                                             min_value=0,
                                             key="slp")
                        sc = st.selectbox("Cat",
                                          ["Electronics",
                                           "Clothes",
                                           "Other"],
                                          key="slc")
                        si = st.file_uploader("Photo",
                                              type=["png",
                                                    "jpg",
                                                    "jpeg"],
                                              key="sli")
                        if st.button("🚀 List", key="slb",
                                     use_container_width
                                     =True):
                            if st_.strip():
                                img = None
                                if si is not None:
                                    img = save_upload(si)
                                db = load_db()
                                db["listings"].insert(0, {
                                    "id": uuid.uuid4()
                                    .hex[:8],
                                    "seller": SS.username,
                                    "title": st_.strip(),
                                    "description": sd,
                                    "price": int(sp),
                                    "category": sc,
                                    "image": img,
                                    "location": "PK",
                                    "status":
                                    "available"})
                                save_db(db)
                                safe_rerun()
                    for l in DB["listings"]:
                        stst = "✅" if l["status"] == \
                            "available" else "❌ SOLD"
                        st.markdown("<div class='gc'><div "
                                    "class='gnm'>" +
                                    esc(l["title"]) +
                                    "</div><div class='gsb'>"
                                    "PKR " + str(l["price"]) +
                                    " · " + stst + " · @" +
                                    esc(l["seller"]) +
                                    "</div></div>",
                                    unsafe_allow_html=True)
                        if st.button("View",
                                     key="lo_" + l["id"],
                                     use_container_width
                                     =True):
                            SS.open_listing = l["id"]
                            safe_rerun()

            # ============ ADS ============
            elif SS.current_tab == "Ads":
                st.markdown("<div class='phdr'>📢 Ads "
                            "Manager</div>",
                            unsafe_allow_html=True)
                with st.expander("➕ Create Ad"):
                    at = st.text_input("Title", key="adt")
                    ax = st.text_area("Text", key="adx",
                                      height=60)
                    al2 = st.text_input("Link", key="adl")
                    ab = st.number_input("Budget coins",
                                         min_value=10,
                                         value=50,
                                         key="adb")
                    if st.button("🚀 Submit", key="adb2",
                                 use_container_width=True):
                        if at.strip():
                            db = load_db()
                            u = db["users"].get(SS.username)
                            cost = int(ab)
                            if u is not None and \
                                    u.get("coins", 0) >= \
                                    cost:
                                u["coins"] -= cost
                                db["ads"].append({
                                    "id": uuid.uuid4()
                                    .hex[:8],
                                    "advertiser":
                                    SS.username,
                                    "title": at.strip(),
                                    "text": ax,
                                    "link": al2,
                                    "budget": cost,
                                    "status": "pending"})
                                save_db(db)
                                if owner:
                                    add_notification(
                                        owner, "📢 Ad "
                                        "pending by @" +
                                        SS.username)
                                st.success("Submitted! "
                                           "Owner approve "
                                           "karega.")
                                safe_rerun()
                            else:
                                st.warning("Coins kam hain!")
                        else:
                            st.warning("Title likhein!")
                my_ads = [a for a in DB["ads"]
                          if a["advertiser"] ==
                          SS.username]
                for a in my_ads:
                    st.markdown("<div class='adc'><span "
                                "class='adt'>" +
                                a["status"].upper() +
                                "</span><br><b>" +
                                esc(a["title"]) + "</b></div>",
                                unsafe_allow_html=True)
                if is_owner:
                    st.markdown("### 🛡️ Approve")
                    pend = [a for a in DB["ads"]
                            if a["status"] == "pending"]
                    for i, a in enumerate(pend):
                        a1, a2 = st.columns(2)
                        a1.markdown("📢 **" + esc(a["title"])
                                    + "**")
                        if a2.button("✅", key="adp_" +
                                     str(i)):
                            db = load_db()
                            for ad in db["ads"]:
                                if ad["id"] == a["id"]:
                                    ad["status"] = "active"
                                    break
                            save_db(db)
                            safe_rerun()

            # ============ SEARCH ============
            elif SS.current_tab == "Search":
                st.markdown("<div class='phdr'>🔍 "
                            "Search</div>",
                            unsafe_allow_html=True)
                q = st.text_input("Search...",
                                  key="sq")
                if q.strip():
                    res = [u for u in DB["users"]
                           if q.lower() in u.lower()]
                    if res:
                        for un in res:
                            st.markdown("<div class='sr'>" +
                                        av_html(un, DB[
                                            "users"][un].get(
                                                "avatar"),
                                            40) +
                                        "<div><b>@" + un +
                                        "</b></div></div>",
                                        unsafe_allow_html
                                        =True)
                            if st.button("View",
                                         key="sv_" + un,
                                         use_container_width
                                         =True):
                                SS.view_user = un
                                safe_rerun()
                    else:
                        st.info("Users nahi mile - Google:")
                        from urllib.parse import quote_plus
                        gq = quote_plus(q.strip())
                        st.markdown("[🖼️ Google Images]"
                                    "(https://www.google.com"
                                    "/search?tbm=isch&q=" +
                                    gq + ") · [🎬 YouTube]"
                                    "(https://www.youtube.com"
                                    "/results?search_query="
                                    + gq + ")")

            # ============ FRIENDS ============
            elif SS.current_tab == "Friends":
                st.markdown("<div class='phdr'>👥 "
                            "Friends</div>",
                            unsafe_allow_html=True)
                inr = [r for r in DB["friend_requests"]
                       if r["to"] == SS.username]
                frs = DB["friends"].get(SS.username, [])
                st.markdown("### 📨 Requests (" +
                            str(len(inr)) + ")")
                for i, r in enumerate(inr):
                    st.markdown("<div class='fr'>" +
                                av_html(r["from"], None,
                                        40) +
                                "<div><b>@" + r["from"] +
                                "</b></div></div>",
                                unsafe_allow_html=True)
                    f1, f2 = st.columns(2)
                    if f1.button("✅", key="fa_" + str(i),
                                 use_container_width=True):
                        db = load_db()
                        db["friend_requests"] = [
                            x for x in db[
                                "friend_requests"]
                            if not (x["from"] == r["from"]
                                    and x["to"] ==
                                    SS.username)]
                        fa = db["friends"].setdefault(
                            SS.username, [])
                        fb = db["friends"].setdefault(
                            r["from"], [])
                        if r["from"] not in fa:
                            fa.append(r["from"])
                        if SS.username not in fb:
                            fb.append(SS.username)
                        save_db(db)
                        add_notification(r["from"],
                                         "✅ Accepted!",
                                         "follows")
                        safe_rerun()
                    if f2.button("❌", key="fr_" + str(i),
                                 use_container_width=True):
                        db = load_db()
                        db["friend_requests"] = [
                            x for x in db[
                                "friend_requests"]
                            if not (x["from"] == r["from"]
                                    and x["to"] ==
                                    SS.username)]
                        save_db(db)
                        safe_rerun()
                st.markdown("### Friends (" + str(len(frs))
                            + ")")
                for f in frs:
                    st.markdown("<div class='fr'>" +
                                av_html(f, None, 40) +
                                "<div><b>@" + f +
                                "</b></div></div>",
                                unsafe_allow_html=True)
                    b1, b2, b3 = st.columns(3)
                    if b1.button("👤", key="fv_" + f):
                        SS.view_user = f
                        safe_rerun()
                    if b2.button("✉️", key="fm_" + f):
                        SS.msg_view = "chat"
                        SS.msg_target = f
                        SS.msg_target_type = "direct"
                        SS.current_tab = "Messages"
                        safe_rerun()
                    if b3.button("📞", key="fc_" + f):
                        start_call(SS.username, f)
                        add_notification(f, "📞 Call!")
                        safe_rerun()
                st.markdown("### 🌟 Suggestions")
                sugg = [u for u in DB["users"]
                        if u != SS.username
                        and u not in frs
                        and u not in SS.blocked
                        and not any(x["from"] ==
                                    SS.username and
                                    x["to"] == u
                                    for x in DB[
                                        "friend_requests"])]
                for s in sugg:
                    st.markdown("<div class='fr'>" +
                                av_html(s, None, 40) +
                                "<div><b>@" + s +
                                "</b></div></div>",
                                unsafe_allow_html=True)
                    if st.button("➕", key="sg_" + s,
                                 use_container_width=True):
                        db = load_db()
                        db["friend_requests"].append(
                            {"from": SS.username, "to": s,
                             "time": now})
                        save_db(db)
                        add_notification(s, "👋 Request!",
                                         "follows")
                        safe_rerun()

            # ============ CHANNEL ============
            elif SS.current_tab == "Channel":
                st.markdown("<div class='phdr'>📺 "
                            "Channel</div>",
                            unsafe_allow_html=True)
                st.markdown("[🔗 Color Pop Cartoons on "
                            "YouTube](" + CHANNEL_URL + ")")
                with st.expander("➕ Add Video"):
                    yl = st.text_input("Link", key="cl")
                    if st.button("Add", key="cb",
                                 use_container_width=True):
                        vid = parse_yt(yl)
                        if vid:
                            db = load_db()
                            db["posts"].insert(0, {
                                "id": uuid.uuid4().hex[:8],
                                "user": SS.username,
                                "type": "youtube",
                                "ref": vid,
                                "cap": "Channel",
                                "likes": {},
                                "comments": [],
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

            # ============ REELS ============
            elif SS.current_tab == "Reels":
                st.markdown("<div class='phdr'>🎬 "
                            "Reels</div>",
                            unsafe_allow_html=True)
                rl = [p for p in DB["posts"]
                      if p.get("type") in ("reel", "video")]
                for r in reversed(rl):
                    st.caption("@" + r["user"])
                    st.video(r["ref"])

            # ============ CREATE ============
            elif SS.current_tab == "Create":
                st.markdown("<div class='phdr'>➕ "
                            "Create</div>",
                            unsafe_allow_html=True)
                kind = st.radio("Type:",
                                ["Photo", "Video",
                                 "Camera 🎨",
                                 "YouTube"],
                                horizontal=True,
                                key="ck")
                cap = st.text_input("Caption", key="uc")
                if kind == "Camera 🎨":
                    fl = st.selectbox("Filter:",
                                      FILTER_NAMES,
                                      key="cf")
                    cam = st.camera_input("📸", key="ucam")
                    fi = None
                    if cam is not None:
                        try:
                            pil = Image.open(cam)
                            fi = apply_filter(pil, fl)
                            buf = io.BytesIO()
                            fi.save(buf, format="PNG")
                            st.image(buf.getvalue())
                        except Exception:
                            pass
                    if st.button("🚀", key="up2",
                                 use_container_width=True):
                        if fi is None:
                            st.warning("Photo lein!")
                        else:
                            db = load_db()
                            db["posts"].insert(0, {
                                "id": uuid.uuid4()
                                .hex[:8],
                                "user": SS.username,
                                "type": "image",
                                "ref": save_pil(fi),
                                "cap": cap, "likes": {},
                                "comments": []})
                            save_db(db)
                            SS.current_tab = "Home"
                            safe_rerun()
                elif kind == "YouTube":
                    yl = st.text_input("Link", key="uy")
                    if st.button("🚀", key="up1",
                                 use_container_width=True):
                        vid = parse_yt(yl)
                        if vid:
                            db = load_db()
                            db["posts"].insert(0, {
                                "id": uuid.uuid4()
                                .hex[:8],
                                "user": SS.username,
                                "type": "youtube",
                                "ref": vid,
                                "cap": cap, "likes": {},
                                "comments": []})
                            save_db(db)
                            SS.current_tab = "Home"
                            safe_rerun()
                        else:
                            st.error("Invalid link!")
                else:
                    if kind == "Photo":
                        f = st.file_uploader(
                            "Photo", type=["png", "jpg",
                                          "jpeg"],
                            key="up")
                    else:
                        f = st.file_uploader(
                            "Video", type=["mp4", "mov"],
                            key="uv")
                    if st.button("🚀", key="up3",
                                 use_container_width=True):
                        if f is None:
                            st.warning("File!")
                        else:
                            db = load_db()
                            db["posts"].insert(0, {
                                "id": uuid.uuid4()
                                .hex[:8],
                                "user": SS.username,
                                "type": "video" if kind ==
                                "Video" else "image",
                                "ref": save_upload(f),
                                "cap": cap, "likes": {},
                                "comments": []})
                            save_db(db)
                            SS.current_tab = "Home"
                            safe_rerun()

            # ============ MESSAGES (sab ON!) ============
            elif SS.current_tab == "Messages":

                if HAS_REFRESH:
                    st_autorefresh(interval=4000,
                                   key="mr")
                db = load_db()
                shot_install()

                if SS.msg_view == "chat":
                    tgt = SS.msg_target
                    isg = (SS.msg_target_type == "group")
                    grp = None
                    if isg:
                        grp = next((g for g in db["groups"]
                                    if g["id"] == tgt),
                                   None)
                        if grp is None:
                            SS.msg_view = "list"
                            safe_rerun()
                    elif tgt not in db["users"]:
                        SS.msg_view = "list"
                        safe_rerun()

                    hb, ha, hi, hc = st.columns(
                        [0.1, 0.14, 0.5, 0.26])
                    if hb.button("←", key="cbk"):
                        SS.msg_view = "list"
                        safe_rerun()
                    if isg:
                        ha.markdown(av_html(
                            grp["name"], None, 40),
                            unsafe_allow_html=True)
                        hi.markdown("<b>" + esc(
                            grp["name"]) + "</b><br>"
                            "<span style='font-size:11px;"
                            "color:#9ca3af;'>" +
                            str(len(grp["members"])) +
                            " members</span>",
                            unsafe_allow_html=True)
                        msgs = grp.get("messages", [])
                    else:
                        ud = db["users"][tgt]
                        mark_seen(SS.username, tgt)
                        ha.markdown(av_html(
                            tgt, ud.get("avatar"), 40),
                            unsafe_allow_html=True)
                        hi.markdown("<b>" + esc(
                            ud.get("display_name", tgt)) +
                            "</b><br><span style='font-"
                            "size:11px;color:#31a24c;'>"
                            "● Active</span>",
                            unsafe_allow_html=True)
                        if hc.button("📞 Call", key="ccl"):
                            start_call(SS.username, tgt)
                            add_notification(
                                tgt, "📞 Calling!")
                            safe_rerun()
                        msgs = [m for m in db["messages"]
                                if (m["from"] ==
                                    SS.username and
                                    m["to"] == tgt) or
                                (m["from"] == tgt and
                                 m["to"] == SS.username)]

                    st.markdown("<div class='enc'>🔒 "
                                "End-to-end encrypted "
                                "(demo)</div>",
                                unsafe_allow_html=True)

                    # screenshot detection ON
                    pend = shot_check()
                    if pend and time.time() - \
                            SS.last_shot_time > 5:
                        SS.last_shot_time = time.time()
                        if isg:
                            for mm in grp["members"]:
                                if mm != SS.username:
                                    add_notification(
                                        mm, "📸 @" +
                                        SS.username +
                                        " screenshot!")
                        else:
                            add_notification(
                                tgt, "📸 @" +
                                SS.username +
                                " screenshot!")
                        safe_toast("📸 Detected!")
                        safe_rerun()

                    if SS.clear_msg:
                        SS[SS.clear_msg] = ""
                        SS.clear_msg = ""

                    for m in sorted(msgs,
                                    key=lambda x:
                                    x["time"]):
                        mine = m["from"] == SS.username
                        ts = time.strftime(
                            "%I:%M %p",
                            time.localtime(
                                m["time"])).lower()
                        if m.get("photo") and \
                                is_local(m["photo"]):
                            st.image(m["photo"], width=180)
                        cls = "bme" if mine else "bth"
                        snd = ""
                        if isg and not mine:
                            snd = "<b>@" + esc(m["from"]) + \
                                  "</b><br>"
                        st.markdown("<span class='" + cls +
                                    "'>" + snd +
                                    esc(m.get("text", "")) +
                                    "<span class='btm'>" +
                                    ts + "</span></span>",
                                    unsafe_allow_html=True)
                        r = m.get("reactions", [])
                        mk = m.get("id",
                                   str(m["time"]))
                        lb = "👍 " + str(len(r)) if r \
                            else "👍"
                        if st.button(lb, key="rx_" + mk):
                            toggle_rx(isg, tgt,
                                      m.get("id"),
                                      SS.username)
                            safe_rerun()

                    # PHOTO send ON
                    with st.expander("📷 Send Photo"):
                        ph = st.file_uploader(
                            "Photo", type=["png", "jpg",
                                           "jpeg"],
                            key="cph")
                        if st.button("📷 Send",
                                     key="csph",
                                     use_container_width
                                     =True):
                            if ph is None:
                                st.warning("Choose!")
                            else:
                                path = save_upload(ph)
                                send_msg(isg, tgt, tgt,
                                         "📷 Photo",
                                         photo=path)
                                safe_rerun()

                    # VOICE send ON
                    if hasattr(st, "audio_input"):
                        au = st.audio_input(
                            "🎙️ Record", key="cvc")
                        if au is not None:
                            st.audio(au)
                            if st.button("➡️ Send Voice",
                                         key="csvc",
                                         use_container_width
                                         =True):
                                send_msg(isg, tgt, tgt,
                                         "🎤 Voice note")
                                st.success("Sent!")
                                safe_rerun()

                    # TEXT send ON (filter ke saath)
                    tx = st.text_input("Message...",
                                       key="ctx")
                    if st.button("➡️ Send", key="csd",
                                 use_container_width=True):
                        if tx.strip():
                            if me.get("comment_filter",
                                      True) and \
                                    not text_clean(tx):
                                st.warning("🛡️ Filtered!")
                            else:
                                send_msg(isg, tgt, tgt,
                                         tx.strip())
                                SS.clear_msg = "ctx"
                                safe_rerun()

                else:
                    st.markdown("<div class='phdr'>✉️ "
                                "Chats</div>",
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
                    convs = []
                    for p in partners:
                        if p == SS.username or \
                                p in SS.blocked:
                            continue
                        cn = [m for m in db["messages"]
                              if (m["from"] ==
                                  SS.username and
                                  m["to"] == p) or
                              (m["from"] == p and
                               m["to"] == SS.username)]
                        convs.append({"u": p,
                                      "last": cn[-1]
                                      if cn else None,
                                      "un": unseen_count(
                                          SS.username,
                                          p)})
                    for g in db["groups"]:
                        if SS.username in g["members"]:
                            convs.append({"g": g,
                                          "last": g.get(
                                              "messages",
                                              [None])[-1]
                                          if g.get(
                                              "messages")
                                          else None})
                    convs.sort(key=lambda c: c["last"]
                               ["time"] if c["last"]
                               else 0, reverse=True)
                    if not convs:
                        st.info("No chats yet!")
                    for c in convs:
                        if "u" in c:
                            p = c["u"]
                            ud = db["users"].get(p, {})
                            if p in db.get("friends",
                                           {}).get(
                                               SS.username,
                                               []):
                                dot = ("<div class="
                                       "'odot'></div>")
                            else:
                                dot = ""
                            nm = esc(ud.get(
                                "display_name", p))
                            if c["last"]:
                                if c["last"]["from"] == \
                                        SS.username:
                                    pre = "You: "
                                else:
                                    pre = ""
                                pv = pre + esc(
                                    c["last"].get(
                                        "text", ""))[:30]
                                tm = time.strftime(
                                    "%I:%M %p",
                                    time.localtime(
                                        c["last"]
                                        ["time"])).lower()
                            else:
                                pv = "Say hello 👋"
                                tm = ""
                            av = av_html(
                                p, ud.get("avatar"), 46)
                            kid = p
                            bd = ""
                            if c["un"] > 0:
                                bd = ("<span class="
                                      "'ub'>" +
                                      str(c["un"]) +
                                      "</span>")
                        else:
                            g = c["g"]
                            dot = ""
                            nm = "👥 " + esc(g["name"])
                            if c["last"]:
                                pv = ("@" +
                                      esc(c["last"]
                                          ["from"]) +
                                      ": " + esc(
                                          c["last"].get(
                                              "text",
                                              ""))[:25])
                                tm = time.strftime(
                                    "%I:%M %p",
                                    time.localtime(
                                        c["last"]
                                        ["time"])).lower()
                            else:
                                pv = "Group"
                                tm = ""
                            av = av_html(g["name"], None,
                                         46)
                            kid = g["id"]
                            bd = ""
                        st.markdown("<div class='ci'>"
                                    "<div class='aw'>" +
                                    av + dot +
                                    "</div><div class="
                                    "'cinf'><div class="
                                    "'cnm'>" + nm +
                                    "</div><div class="
                                    "'cpv'>" + pv +
                                    "</div></div><div "
                                    "style='text-align:"
                                    "right;'><div class="
                                    "'ctm'>" + tm +
                                    "</div>" + bd +
                                    "</div></div>",
                                    unsafe_allow_html=True)
                        if st.button("💬", key="op_" + kid,
                                     use_container_width
                                     =True):
                            SS.msg_view = "chat"
                            SS.msg_target = kid
                            if "u" in c:
                                SS.msg_target_type = \
                                    "direct"
                            else:
                                SS.msg_target_type = \
                                    "group"
                            safe_rerun()

                    with st.expander("➕ New Chat/Group"):
                        others = [x for x in db["users"]
                                  if x != SS.username]
                        pick = st.selectbox("Chat:",
                                            others,
                                            key="ncs")
                        if st.button("Start", key="ncb",
                                     use_container_width
                                     =True):
                            SS.msg_view = "chat"
                            SS.msg_target = pick
                            SS.msg_target_type = "direct"
                            safe_rerun()
                        gn = st.text_input("Group name",
                                           key="ngn2")
                        gm = st.multiselect("Members",
                                            others,
                                            key="ngm")
                        if st.button("Create Group",
                                     key="ngb2",
                                     use_container_width
                                     =True):
                            if gn.strip() and gm:
                                db = load_db()
                                db["groups"].append({
                                    "id": uuid.uuid4()
                                    .hex[:8],
                                    "name": gn.strip(),
                                    "privacy": "public",
                                    "createdBy":
                                    SS.username,
                                    "members":
                                    [SS.username] + gm,
                                    "requests": [],
                                    "messages": []})
                                save_db(db)
                                safe_rerun()

            # ============ NOTIFICATIONS ============
            elif SS.current_tab == "Notifications":
                st.markdown("<div class='phdr'>🔔 "
                            "Notifications</div>",
                            unsafe_allow_html=True)
                db = load_db()
                mn = [n for n in db["notifications"]
                      if n.get("to") == SS.username][:40]
                if st.button("✅ Mark all read", key="mr2",
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
                    ts = time.strftime(
                        "%d %b %H:%M",
                        time.localtime(n["time"]))
                    st.markdown("<div class='nr'>" +
                                n["text"] + "<br><span "
                                "style='font-size:11px;"
                                "color:#9ca3af;'>" + ts +
                                "</span></div>",
                                unsafe_allow_html=True)

            # ============ LUDO ============
            elif SS.current_tab == "Ludo":
                st.markdown("<div class='phdr'>🎲 Ludo"
                            "</div>",
                            unsafe_allow_html=True)
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
                    st.markdown("<h3 style='text-align:"
                                "center;color:#00B074;'>🎯 "
                                + str(SS.dice) + "</h3>",
                                unsafe_allow_html=True)

            # ============ PROFILE ============
            elif SS.current_tab == "Profile":
                me = DB["users"].get(SS.username, {})
                mp = [p for p in DB["posts"]
                      if p["user"] == SS.username]
                fr = DB["friends"].get(SS.username, [])
                st.markdown("<div class='fbc'></div>",
                            unsafe_allow_html=True)
                st.markdown("<div style='text-align:center;"
                            "margin-top:-50px;'>" +
                            av_html(SS.username,
                                    me.get("avatar"), 100,
                                    border=True) + "</div>",
                            unsafe_allow_html=True)
                st.markdown("<h3 style='text-align:center;"
                            "margin:8px 0 2px;'>" +
                            esc(me.get("display_name",
                                       SS.username)) +
                            "</h3><p style='text-align:"
                            "center;color:#6b7280;font-size:"
                            "13px;'>" + str(len(fr)) +
                            " friends · " + str(len(mp)) +
                            " posts</p>",
                            unsafe_allow_html=True)
                if is_owner:
                    st.markdown("<p style='text-align:"
                                "center;'><span class="
                                "'ob'>👑 OWNER</span></p>",
                                unsafe_allow_html=True)
                b1, b2 = st.columns(2)
                if b1.button("✏️ Edit Profile", key="pe"):
                    SS.current_tab = "Settings"
                    SS.settings_page = "personal"
                    safe_rerun()
                if b2.button("💰 " + str(me.get("coins", 0))
                             + " Coins · Payout", key="pp"):
                    db = load_db()
                    u = db["users"].get(SS.username)
                    if u is not None and \
                            u.get("coins", 0) >= 100:
                        u["coins"] -= 100
                        save_db(db)
                        st.success("Payout submitted!")
                        safe_rerun()
                    else:
                        st.warning("Min 100 coins!")
                with st.expander("🖼️ Change Pic"):
                    fl = st.selectbox("Filter:",
                                      FILTER_NAMES,
                                      key="pf")
                    pi = st.file_uploader(
                        "Upload", type=["png", "jpg",
                                        "jpeg"],
                        key="pi")
                    if st.button("💾 Update", key="pu",
                                 use_container_width=True):
                        if pi is None:
                            st.warning("Choose!")
                        else:
                            pil = Image.open(pi)
                            pil = apply_filter(pil, fl)
                            set_pref(SS.username,
                                     "avatar",
                                     save_pil(pil))
                            st.success("Updated!")
                            safe_rerun()
                for p in mp[:5]:
                    if p.get("type") == "text":
                        st.markdown("<div class='pph' "
                                    "style='background:" +
                                    p.get("grad", "#f0f0f0")
                                    + ";height:90px;'>"
                                    + esc(p.get("txt", ""))
                                    + "</div>",
                                    unsafe_allow_html=True)
                    elif p.get("type") == "image" and \
                            is_local(p["ref"]):
                        st.image(p["ref"],
                                 use_container_width=True)

            # ============ SETTINGS (sab asli!) ========
            elif SS.current_tab == "Settings":

                if SS.settings_page == "menu":
                    st.markdown("<div class='phdr'>⚙️ "
                                "Settings</div>",
                                unsafe_allow_html=True)
                    st.caption("@" + SS.username)
                    if is_owner:
                        if st.button("🛡️ OWNER PANEL ›",
                                     key="mo",
                                     use_container_width
                                     =True):
                            SS.settings_page = "admin"
                            safe_rerun()
                    for label, pg in [
                            ("🔐 Security & Locks",
                             "security"),
                            ("📋 Personal Info",
                             "personal"),
                            ("📰 Feed & Messages",
                             "feed"),
                            ("🔔 Notifications",
                             "notifs"),
                            ("🚫 Blocked", "blocked"),
                            ("⚠️ Report", "reports"),
                            ("ℹ️ About", "about")]:
                        if st.button(label + " ›",
                                     key="m_" + pg,
                                     use_container_width
                                     =True):
                            SS.settings_page = pg
                            safe_rerun()
                    if st.button("🚪 Logout", key="mlo",
                                 use_container_width=True):
                        SS.logged_in = False
                        SS.page = "auth"
                        safe_rerun()

                elif SS.settings_page == "admin":
                    if st.button("← Back", key="ba"):
                        SS.settings_page = "menu"
                        safe_rerun()
                    st.markdown("<div class='phdr'>🛡️ "
                                "Owner</div>",
                                unsafe_allow_html=True)
                    db = load_db()
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Users", len(db["users"]))
                    c2.metric("Posts", len(db["posts"]))
                    c3.metric("Reports",
                              len(db["reports"]))
                    st.markdown("### 🚩 Reports → Ban")
                    for i, r in enumerate(
                            reversed(db["reports"][:10])):
                        r1, r2 = st.columns([0.6, 0.4])
                        r1.markdown("🚩 **@" +
                                    esc(r.get("user",
                                              "")) +
                                    "** by @" +
                                    esc(r.get("from",
                                              "")))
                        if r.get("user") in db["banned"]:
                            if r2.button("Unban",
                                         key="ru_" +
                                         str(i),
                                         use_container_width
                                         =True):
                                db = load_db()
                                db["banned"].remove(
                                    r["user"])
                                save_db(db)
                                safe_rerun()
                        else:
                            if r2.button("🔨 BAN",
                                         key="rb_" +
                                         str(i),
                                         use_container_width
                                         =True):
                                db = load_db()
                                db["banned"].append(
                                    r["user"])
                                save_db(db)
                                safe_rerun()

                elif SS.settings_page == "security":
                    if st.button("← Back", key="bs"):
                        SS.settings_page = "menu"
                        safe_rerun()
                    st.markdown("<div class='phdr'>🔐 "
                                "Security</div>",
                                unsafe_allow_html=True)

                    # --- APP LOCK PIN (asli!) ---
                    st.markdown("<p class='sl'>🔢 App "
                                "Lock (PIN)</p>",
                                unsafe_allow_html=True)
                    if not me.get("app_lock"):
                        npin = st.text_input(
                            "4-digit PIN chunein",
                            type="password",
                            max_chars=4, key="spn")
                        if st.button("🔒 Enable App Lock",
                                     key="sae",
                                     use_container_width
                                     =True):
                            if len(npin) == 4 and \
                                    npin.isdigit():
                                set_pref(SS.username,
                                         "app_pin", npin)
                                set_pref(SS.username,
                                         "app_lock", True)
                                st.success("Enabled! Ab "
                                           "Lock Now "
                                           "dabayein.")
                                safe_rerun()
                            else:
                                st.warning("4 digits!")
                    else:
                        st.success("✅ App Lock ON")
                        l1, l2 = st.columns(2)
                        if l1.button("🔒 Lock Now",
                                     key="sln",
                                     use_container_width
                                     =True):
                            SS.pin_unlocked = False
                            safe_rerun()
                        if l2.button("❌ Disable",
                                     key="sdn",
                                     use_container_width
                                     =True):
                            set_pref(SS.username,
                                     "app_lock", False)
                            set_pref(SS.username,
                                     "app_pin", "")
                            st.success("Disabled!")
                            safe_rerun()

                    # --- FINGERPRINT (asli!) ---
                    st.markdown("<p class='sl'>👆 "
                                "Fingerprint Lock</p>",
                                unsafe_allow_html=True)
                    cur_f = me.get("finger_lock", False)
                    nf = st.checkbox("Enable Fingerprint",
                                     value=cur_f,
                                     key="sfl")
                    if nf != cur_f:
                        set_pref(SS.username,
                                 "finger_lock", nf)
                        if nf:
                            SS.finger_unlocked = False
                            st.success("Enabled! Lock "
                                       "screen aayega.")
                        else:
                            SS.finger_unlocked = True
                        safe_rerun()

                    # --- 2FA (asli!) ---
                    st.markdown("<p class='sl'>🔑 "
                                "Two-Factor (2FA)</p>",
                                unsafe_allow_html=True)
                    cur_2 = me.get("two_fa", False)
                    n2 = st.checkbox("Login par code "
                                     "maangein",
                                     value=cur_2,
                                     key="s2f")
                    if n2 != cur_2:
                        set_pref(SS.username,
                                 "two_fa", n2)
                        if n2:
                            st.success("2FA ON! Agli "
                                       "baar login "
                                       "par code "
                                       "aayega.")
                        else:
                            st.success("2FA OFF.")
                        safe_rerun()

                    # --- LOGIN ALERTS (asli!) ---
                    cur_la = me.get("login_alerts", True)
                    nla = st.checkbox("📩 Login Alerts",
                                      value=cur_la,
                                      key="sla")
                    if nla != cur_la:
                        set_pref(SS.username,
                                 "login_alerts", nla)
                        safe_rerun()

                    # --- AUTO LOGOUT (asli!) ---
                    st.markdown("<p class='sl'>⏱️ Auto "
                                "Logout</p>",
                                unsafe_allow_html=True)
                    cur_al = me.get("auto_logout", 0)
                    nal = st.selectbox(
                        "Idle minutes:",
                        [0, 5, 10, 30],
                        index=[0, 5, 10, 30].index(cur_al)
                        if cur_al in [0, 5, 10, 30] else 0,
                        key="sal")
                    if nal != cur_al:
                        set_pref(SS.username,
                                 "auto_logout", nal)
                        if nal > 0:
                            st.success(str(nal) +
                                       " min idle par "
                                       "auto logout!")
                        safe_rerun()

                elif SS.settings_page == "personal":
                    if st.button("← Back", key="bp"):
                        SS.settings_page = "menu"
                        safe_rerun()
                    dn = st.text_input(
                        "Display Name",
                        value=me.get("display_name", ""),
                        key="pdn")
                    bio = st.text_input(
                        "Bio", value=me.get("bio", ""),
                        key="pbio")
                    bd = st.text_input(
                        "Birthday",
                        value=me.get("birthday", ""),
                        key="pbd")
                    gn = st.selectbox(
                        "Gender", ["Male", "Female",
                                   "Other"],
                        key="pgn")
                    if st.button("💾 Save", key="psv",
                                 use_container_width=True):
                        set_pref(SS.username,
                                 "display_name", dn)
                        set_pref(SS.username, "bio", bio)
                        set_pref(SS.username,
                                 "birthday", bd)
                        set_pref(SS.username, "gender", gn)
                        st.success("Saved!")

                elif SS.settings_page == "feed":
                    if st.button("← Back", key="bf"):
                        SS.settings_page = "menu"
                        safe_rerun()
                    st.markdown("<p class='sl'>📰 Feed"
                                "</p>",
                                unsafe_allow_html=True)
                    cur_fs = me.get("feed_sort",
                                    "Most Recent")
                    nfs = st.radio("Sort:",
                                   ["Most Recent",
                                    "Top Posts"],
                                   index=0 if cur_fs ==
                                   "Most Recent" else 1,
                                   key="nfs")
                    if nfs != cur_fs:
                        set_pref(SS.username,
                                 "feed_sort", nfs)
                        st.success("Feed sort saved!")
                        safe_rerun()
                    cur_ss = me.get("show_stories", True)
                    nss = st.checkbox("Show Stories",
                                      value=cur_ss,
                                      key="nss")
                    if nss != cur_ss:
                        set_pref(SS.username,
                                 "show_stories", nss)
                        safe_rerun()
                    st.markdown("<p class='sl'>🛡️ Message "
                                "& Comment Filter</p>",
                                unsafe_allow_html=True)
                    cur_cf = me.get("comment_filter", True)
                    ncf = st.checkbox(
                        "Bad words block karein",
                        value=cur_cf, key="ncf")
                    if ncf != cur_cf:
                        set_pref(SS.username,
                                 "comment_filter", ncf)
                        safe_rerun()

                elif SS.settings_page == "notifs":
                    if st.button("← Back", key="bn"):
                        SS.settings_page = "menu"
                        safe_rerun()
                    st.markdown("<div class='phdr'>🔔 "
                                "Notifications</div>",
                                unsafe_allow_html=True)
                    st.caption("Ye settings har user ki "
                               "apni hain - notifications "
                               "is ke mutabiq aate hain!")
                    prefs = me.get("notif",
                                   {"likes": True,
                                    "comments": True,
                                    "follows": True,
                                    "messages": True})
                    for kind, label in [
                            ("likes", "❤️ Likes"),
                            ("comments", "💬 Comments"),
                            ("follows", "👥 Follows"),
                            ("messages", "✉️ Messages")]:
                        cur = prefs.get(kind, True)
                        nv = st.checkbox(label,
                                         value=cur,
                                         key="ntf_" + kind)
                        if nv != cur:
                            db = load_db()
                            u = db["users"].get(
                                SS.username)
                            if u is not None:
                                u.setdefault(
                                    "notif", {})[kind] \
                                    = nv
                                save_db(db)
                            safe_rerun()

                elif SS.settings_page == "blocked":
                    if st.button("← Back", key="bb"):
                        SS.settings_page = "menu"
                        safe_rerun()
                    bi = st.text_input("Username",
                                       key="bki")
                    if st.button("🚫 Block", key="bkb",
                                 use_container_width=True):
                        u = bi.strip().lower()
                        if u and u != SS.username:
                            db = load_db()
                            rec = db["users"].get(
                                SS.username)
                            if rec is not None:
                                rec.setdefault(
                                    "blocked",
                                    []).append(u)
                                save_db(db)
                                SS.blocked = list(
                                    rec["blocked"])
                            safe_rerun()
                    for i, u in enumerate(SS.blocked):
                        b1, b2 = st.columns([0.6, 0.4])
                        b1.markdown("**🚫 @" + u + "**")
                        if b2.button("Unblock",
                                     key="ub3_" +
                                     str(i),
                                     use_container_width
                                     =True):
                            db = load_db()
                            rec = db["users"].get(
                                SS.username)
                            if rec is not None and \
                                    u in rec.get(
                                        "blocked", []):
                                rec["blocked"].remove(u)
                                save_db(db)
                            SS.blocked.remove(u)
                            safe_rerun()

                elif SS.settings_page == "reports":
                    if st.button("← Back", key="br"):
                        SS.settings_page = "menu"
                        safe_rerun()
                    ri = st.text_input("Member ID",
                                       key="rki")
                    if st.button("🚩 Report", key="rkb",
                                 use_container_width=True):
                        u = ri.strip().lower()
                        if u:
                            db = load_db()
                            db["reports"].append(
                                {"from": SS.username,
                                 "user": u,
                                 "reason": "report",
                                 "time": now})
                            save_db(db)
                            if owner:
                                add_notification(
                                    owner,
                                    "🚩 Report: @" + u)
                            st.success("Owner ko gayi!")
                        else:
                            st.warning("ID likhein!")

                elif SS.settings_page == "about":
                    if st.button("← Back", key="baf"):
                        SS.settings_page = "menu"
                        safe_rerun()
                    st.markdown("### ℹ️ " +
                                APP_INFO["name"])
                    st.markdown(
                        "**🏢 Parent:** " +
                        APP_INFO["parent"] + "\n\n" +
                        "**👑 Founders:** " +
                        APP_INFO["founders"] + "\n\n" +
                        "**📍 HQ:** " + APP_INFO["hq"] +
                        "\n\n**📅 Founded:** " +
                        APP_INFO["founded"] + "\n\n" +
                        "**Type:** " + APP_INFO["type"] +
                        "\n\n---\n**Features:** Feed • "
                        "Stories • Groups • Pages • "
                        "Events • Marketplace • Ads • "
                        "Messenger • Voice • Calls • "
                        "Games • Wallet\n\n© 2026 " +
                        APP_INFO["parent"])

        # ---- BOTTOM NAV ----
        st.markdown("<div class='nav'>" +
                    "<a href='?tab=Home' class='" +
                    ("on" if SS.current_tab == "Home"
                     else "") + "'>🏠</a>" +
                    "<a href='?tab=Search' class='" +
                    ("on" if SS.current_tab == "Search"
                     else "") + "'>🔍</a>" +
                    "<a href='?tab=Groups' class='" +
                    ("on" if SS.current_tab == "Groups"
                     else "") + "'>👥</a>" +
                    "<a href='?tab=Marketplace' class='" +
                    ("on" if SS.current_tab ==
                     "Marketplace" else "") +
                    "'>🛒</a>" +
                    "<a href='?tab=Create' class='" +
                    ("on" if SS.current_tab == "Create"
                     else "") + "'>➕</a>" +
                    "<a href='?tab=Messages' class='" +
                    ("on" if SS.current_tab == "Messages"
                     else "") + "'>✉️</a>" +
                    "<a href='?tab=Profile' class='" +
                    ("on" if SS.current_tab == "Profile"
                     else "") + "'>👤</a></div>",
                    unsafe_allow_html=True)


# ---------- SAFETY ----------
else:
    SS.page = "splash"
    safe_rerun()
  

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

SALT = "hmf_secret_2025"
DB_FILE = "hmf_db.json"
UPLOAD_DIR = "uploads"
FILTERS = ["None", "Beauty", "Sepia", "Vintage", "Cool",
           "Gray", "Bright", "Cartoon"]
GRADS = ["linear-gradient(45deg,#d1fae5,#a7f3d0)",
         "linear-gradient(45deg,#ecfdf5,#6ee7b7)",
         "linear-gradient(45deg,#e6f7f0,#b3e6cc)"]
BAD_WORDS = ["stupid", "idiot", "hate", "dumb", "ugly"]


def hash_pw(p):
    return hashlib.sha256((SALT + p).encode()).hexdigest()


def pw_ok(s, p):
    return s == hash_pw(p) or s == p


def rr():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


def toast(m):
    if hasattr(st, "toast"):
        st.toast(m)
    else:
        st.info(m)


def parse_yt(u):
    u = (u or "").strip()
    if not u:
        return None
    if len(u) == 11 and "/" not in u:
        return u
    for t in ("youtu.be/", "v=", "/shorts/", "/embed/"):
        if t in u:
            p = u.split(t)[1]
            p = p.split("?")[0]
            p = p.split("&")[0]
            p = p.split("/")[0]
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


def setp(u, k, v):
    db = load_db()
    rec = db["users"].get(u)
    if rec is not None:
        rec[k] = v
        save_db(db)


def notify(to, text):
    if not to:
        return
    db = load_db()
    db["notifications"].insert(0, {"to": to, "text": text,
                                   "time": time.time(),
                                   "read": False})
    db["notifications"] = db["notifications"][:200]
    save_db(db)


def unread(u):
    db = load_db()
    n = 0
    for x in db["notifications"]:
        if x.get("to") == u and not x.get("read"):
            n = n + 1
    return n


def unseen(me, p):
    db = load_db()
    last = db.get("seen", {}).get(me, {}).get(p, 0)
    n = 0
    for m in db["messages"]:
        if m["from"] == p and m["to"] == me:
            if m.get("time", 0) > last:
                n = n + 1
    return n


def seen(me, p):
    db = load_db()
    if me not in db["seen"]:
        db["seen"][me] = {}
    db["seen"][me][p] = time.time()
    save_db(db)


def clean(t):
    for w in BAD_WORDS:
        if w in t.lower():
            return False
    return True


def smsg(isg, gid, to, text, photo=None):
    me = st.session_state.username
    db = load_db()
    m = {"id": uuid.uuid4().hex[:8], "from": me,
         "text": text, "time": time.time(),
         "reactions": []}
    if photo:
        m["photo"] = photo
    if isg:
        for g in db["groups"]:
            if g["id"] == gid:
                g.setdefault("messages", []).append(m)
                break
        save_db(db)
    else:
        m["to"] = to
        db["messages"].append(m)
        save_db(db)
        notify(to, "@" + me + " sent you a message")


def tog_rx(isg, gid, mid, u):
    db = load_db()
    if isg:
        for g in db["groups"]:
            if g["id"] == gid:
                for m in g.get("messages", []):
                    if m.get("id") == mid:
                        rx = m.setdefault("reactions", [])
                        if u in rx:
                            rx.remove(u)
                        else:
                            rx.append(u)
                break
    else:
        for m in db["messages"]:
            if m.get("id") == mid:
                rx = m.setdefault("reactions", [])
                if u in rx:
                    rx.remove(u)
                else:
                    rx.append(u)
                break
    save_db(db)


def supload(f):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = f.name.split(".")[-1].lower()
    if ext not in ("png", "jpg", "jpeg", "mp4", "mov",
                   "webm"):
        ext = "bin"
    p = os.path.join(UPLOAD_DIR, uuid.uuid4().hex + "." + ext)
    with open(p, "wb") as o:
        o.write(f.getbuffer())
    return p


def spil(img):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    p = os.path.join(UPLOAD_DIR, uuid.uuid4().hex + ".png")
    img.save(p, "PNG")
    return p


def av(name, path=None, size=36):
    if path and os.path.exists(path):
        try:
            b = base64.b64encode(open(path, "rb").read())
            return "<img src='data:image/png;base64," + \
                b.decode() + "' style='width:" + str(size) + \
                "px;height:" + str(size) + \
                "px;border-radius:50%;object-fit:cover;'>"
        except Exception:
            pass
    return "<div style='width:" + str(size) + "px;height:" + \
        str(size) + "px;border-radius:50%;background:" + \
        "linear-gradient(135deg,#00B074,#056839);color:#fff;" + \
        "display:flex;align-items:center;justify-content:" + \
        "center;font-weight:bold;font-size:" + \
        str(int(size * 0.38)) + "px;'>" + \
        esc(str(name)[:2].upper()) + "</div>"


def filt(img, name):
    try:
        im = img.convert("RGB")
        if name == "Beauty":
            b = im.filter(ImageFilter.GaussianBlur(3))
            o = Image.blend(im, b, 0.5)
            return ImageEnhance.Brightness(o).enhance(1.1)
        if name == "Sepia":
            return ImageOps.colorize(im.convert("L"),
                                     "#704214", "#ffe8c0")
        if name == "Vintage":
            return ImageOps.colorize(im.convert("L"),
                                     "#3a2a1a", "#e8d8b0")
        if name == "Cool":
            return ImageOps.colorize(im.convert("L"),
                                     "#20304a", "#c8e0ff")
        if name == "Gray":
            return im.convert("L").convert("RGB")
        if name == "Bright":
            return ImageEnhance.Brightness(im).enhance(1.4)
        if name == "Cartoon":
            w = max(1, im.width // 6)
            h = max(1, im.height // 6)
            s = im.resize((w, h))
            s = s.filter(ImageFilter.MedianFilter(7))
            o = s.resize((im.width, im.height))
            o = ImageOps.posterize(o, 5)
            return ImageEnhance.Color(o).enhance(1.3)
        return im
    except Exception:
        return img


def isfile(r):
    r = str(r or "")
    if r.startswith("http"):
        return False
    return os.path.exists(r)


# ---------- SEED ----------
DB = load_db()
for un, pw, nm in [("demo", "1234", "Demo User"),
                   ("hoor", "1234", "Hoor Jannat"),
                   ("farrukh", "1234", "Farrukh M")]:
    if un not in DB["users"] and un not in DB["banned"]:
        DB["users"][un] = {
            "password": hash_pw(pw), "display_name": nm,
            "bio": "Hi!", "coins": 550, "blocked": [],
            "avatar": None, "fails": 0,
            "app_lock": False, "app_pin": "",
            "finger_lock": False, "auto_logout": 0,
            "comment_filter": True, "show_stories": True}
if not DB["posts"]:
    DB["posts"] = [
        {"id": "s1", "user": "hoor", "type": "youtube",
         "ref": "aqz-KE-bpKQ", "cap": "Big Buck Bunny!",
         "likes": {}, "comments": []},
        {"id": "s2", "user": "farrukh", "type": "text",
         "grad": GRADS[0], "txt": "Ludo Night",
         "cap": "Tonight 8 PM!", "likes": {},
         "comments": []}]
if not DB["listings"]:
    DB["listings"].append(
        {"id": "ls1", "seller": "farrukh",
         "title": "Gaming Mouse", "price": 1500,
         "description": "RGB", "image": None,
         "status": "available"})
save_db(DB)

SS = st.session_state
for k, v in {"page": "splash", "logged_in": False,
             "username": "", "auth_mode": "login",
             "tab": "Home", "setpage": "menu",
             "blocked": [], "clear_c": "", "clear_m": "",
             "view_user": None, "open_group": "",
             "open_page": "", "open_event": "",
             "open_list": "", "open_reel": "",
             "pin_ok": True, "fin_ok": True,
             "pin_att": 0, "pin_lock": 0,
             "msg_view": "list", "msg_target": "",
             "msg_ttype": "direct", "dark": False,
             "dice": 0, "last_active": 0}.items():
    if k not in SS:
        SS[k] = v


def go(tab):
    SS.tab = tab
    if tab == "Settings":
        SS.setpage = "menu"
    if tab == "Messages":
        SS.msg_view = "list"
    rr()


BASE_CSS = """
<style>
.stApp{background:#f0f2f5 !important}
header[data-testid=stHeader],#MainMenu,footer,
[data-testid=stToolbar],[data-testid=stStatusWidget],
[data-testid=stDecoration]{display:none !important}
.block-container{max-width:430px;margin:0 auto;
background:#fff;padding:0 10px 40px !important;
min-height:100vh;box-shadow:0 0 35px rgba(0,0,0,.18)}
.tb{position:sticky;top:0;z-index:99;display:flex;
justify-content:space-between;align-items:center;
padding:12px 14px;background:#fff;border-bottom:
1px solid #e5e7eb;margin:0 -10px}
.lg{font-size:25px;font-weight:700;font-family:
'Segoe Script','Brush Script MT',cursive;color:#1f2937}
.pc{background:#fff;border-bottom:1px solid #e5e7eb;
margin-bottom:10px}
.ph2{display:flex;align-items:center;padding:10px 4px}
.pu{font-size:14px;font-weight:700;color:#1f2937}
.pph{width:100%;height:270px;background:#f3f4f6;
display:flex;align-items:center;justify-content:center}
.lk{padding:6px 2px 0;font-weight:600;font-size:13px;
color:#1f2937;margin:0}
.pd{padding:0 2px 8px;font-size:14px;color:#1f2937;margin:0}
.ph{padding:14px 4px;font-size:20px;font-weight:bold;
color:#00B074;border-bottom:1px solid #e5e7eb;text-align:center}
.sl{font-weight:700;color:#1f2937;margin:12px 0 4px}
.nr{padding:10px 4px;border-bottom:1px solid #e5e7eb;
font-size:14px;color:#1f2937}
.ob{background:#f59e0b;color:#fff;padding:2px 10px;
border-radius:12px;font-size:11px;font-weight:bold}
.ci{display:flex;align-items:center;padding:11px 4px;
border-bottom:1px solid #e5e7eb}
.aw{margin-right:8px}
.cn{flex:1;min-width:0}
.nm{font-weight:700;font-size:14px;color:#1f2937}
.pv{font-size:12px;color:#4b5563;overflow:hidden;
text-overflow:ellipsis;white-space:nowrap;margin-top:2px}
.ub{background:#00B074;color:#fff;border-radius:50%;
min-width:20px;height:20px;display:inline-flex;
align-items:center;justify-content:center;font-size:11px;
font-weight:700;padding:0 6px}
.bm{background:#00B074;color:#fff;padding:8px 13px;
border-radius:18px 18px 4px 18px;max-width:78%;
margin:3px 0 3px auto;font-size:14px;display:block}
.bh{background:#e5e7eb;color:#1f2937;padding:8px 13px;
border-radius:18px 18px 18px 4px;max-width:78%;
margin:3px auto 3px 0;font-size:14px;display:block}
.bt{font-size:10px;opacity:.75;display:block;
text-align:right;margin-top:2px}
.fr{display:flex;align-items:center;padding:10px 4px;
border-bottom:1px solid #e5e7eb}
.gc{border:1px solid #e5e7eb;border-radius:12px;
padding:12px;margin-bottom:10px}
.gv{height:60px;border-radius:8px;background:
linear-gradient(135deg,#00B074,#056839);margin-bottom:8px}
.gn{font-weight:800;font-size:15px;color:#1f2937}
.gs{font-size:12px;color:#4b5563}
.ad{border:2px solid #f59e0b;border-radius:12px;
padding:12px;margin:10px 0;background:rgba(245,158,11,.06)}
.at{background:#f59e0b;color:#fff;padding:2px 8px;
border-radius:8px;font-size:10px;font-weight:700}
.fbc{height:110px;border-radius:0 0 14px 14px;
background:linear-gradient(135deg,#00B074,#056839);
margin:0 -10px}
div[data-testid=stButton]>button{background:#00B074
!important;color:#fff !important;font-weight:600
!important;border:none !important;border-radius:12px
!important}
</style>
"""

DARK_CSS = """
<style>
.stApp{background:#0f1110 !important}
.block-container{background:#1b1e1b !important}
.tb{background:#1b1e1b !important;border-color:#2a2e2a}
.lg,.pu,.nm,.gn,.lk,.pd,.nr,.sl{color:#eef1ee !important}
.pv,.gs,.bt{color:#9aa69a !important}
.bh{background:#2a2e2a !important;color:#eef1ee !important}
.ph{color:#00e08a !important;border-color:#2a2e2a}
.gc,.ci,.fr,.nr{border-color:#2a2e2a !important}
[data-testid=stTextInput] input,[data-testid=
stTextArea] textarea{background:#242824 !important;
color:#fff !important;border-color:#3a3f3a !important}
[data-testid=stCheckbox] label p,[data-testid=stRadio]
label p{color:#e5e9e5 !important}
</style>
"""


def show_css():
    st.markdown(BASE_CSS, unsafe_allow_html=True)
    if SS.dark:
        st.markdown(DARK_CSS, unsafe_allow_html=True)


# ================= SPLASH =================
if SS.page == "splash":
    show_css()
    st.markdown(
        "<div style='display:flex;flex-direction:column;"
        "align-items:center;justify-content:center;"
        "height:60vh;text-align:center;'>"
        "<h1 style='font-size:90px;font-weight:900;"
        "color:#1f2937;margin:0;'>HMF</h1>"
        "<p style='font-size:24px;color:#4b5563;'>"
        "HMF Book</p></div>", unsafe_allow_html=True)
    if st.button("Get Started", use_container_width=True):
        SS.page = "auth"
        rr()


# ================= AUTH =================
elif SS.page == "auth":

    sup = SS.auth_mode == "signup"
    ttl = "Create Account" if sup else "Welcome Back"
    btn = "Sign Up" if sup else "Login"

    show_css()
    st.markdown(
        "<div style='text-align:center;margin-top:14px;'>"
        "<div style='background:linear-gradient(135deg,"
        "#00B074,#056839);display:inline-block;padding:"
        "16px 48px;border-radius:22px;'>"
        "<h1 style='color:#fff;font-size:34px;margin:0;"
        "font-weight:900;letter-spacing:3px;'>HMF</h1>"
        "</div></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>" + ttl +
                "</h2>", unsafe_allow_html=True)

    un = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button(btn, use_container_width=True):
        u = un.strip().lower()
        db = load_db()
        if not u or not pw:
            st.error("Dono fields bharin!")
        elif u in db["banned"]:
            st.error("BANNED!")
        elif sup:
            if u in db["users"]:
                st.error("Taken!")
            else:
                if not db.get("owner"):
                    db["owner"] = u
                db["users"][u] = {
                    "password": hash_pw(pw),
                    "display_name": u.title(), "bio": "Hi!",
                    "coins": 100, "blocked": [],
                    "avatar": None, "fails": 0,
                    "app_lock": False, "app_pin": "",
                    "finger_lock": False,
                    "auto_logout": 0,
                    "comment_filter": True,
                    "show_stories": True}
                save_db(db)
                SS.logged_in = True
                SS.username = u
                SS.page = "app"
                rr()
        else:
            rec = db["users"].get(u)
            if rec and rec.get("lock_until", 0) > time.time():
                st.error("Locked! Wait 60s")
            elif rec and pw_ok(rec.get("password", ""), pw):
                SS.logged_in = True
                SS.username = u
                SS.blocked = rec.get("blocked", [])
                SS.page = "app"
                SS.last_active = time.time()
                rr()
            elif rec:
                rec["fails"] = rec.get("fails", 0) + 1
                if rec["fails"] >= 5:
                    rec["lock_until"] = time.time() + 60
                    rec["fails"] = 0
                save_db(db)
                st.error("Wrong!")
            else:
                st.error("Invalid!")

    if st.button("Switch to " +
                 ("Login" if sup else "Sign Up")):
        SS.auth_mode = "login" if sup else "signup"
        rr()
    st.caption("Demo: demo/1234")


# ================= MAIN =================
elif SS.page == "app" and SS.logged_in:

    show_css()
    db = load_db()
    me = db["users"].get(SS.username, {})
    is_owner = SS.username == db.get("owner", "")

    al = me.get("auto_logout", 0)
    if al > 0 and SS.last_active > 0:
        if time.time() - SS.last_active > al * 60:
            SS.logged_in = False
            SS.page = "auth"
            rr()
    SS.last_active = time.time()

    if me.get("app_lock") and not SS.pin_ok:
        st.markdown("<div style='text-align:center;"
                    "padding:25vh 0;font-size:70px;'>🔒"
                    "</div>", unsafe_allow_html=True)
        pi = st.text_input("PIN", type="password",
                           max_chars=4)
        if st.button("Unlock", use_container_width=True):
            if pi == me.get("app_pin"):
                SS.pin_ok = True
                rr()
            else:
                st.error("Wrong!")
    elif me.get("finger_lock") and not SS.fin_ok:
        st.markdown("<div style='text-align:center;"
                    "padding:25vh 0;font-size:70px;'>👆"
                    "</div>", unsafe_allow_html=True)
        if st.button("Scan", use_container_width=True):
            time.sleep(1.2)
            SS.fin_ok = True
            rr()
    else:

        # TOPBAR
        unread = unread_count(SS.username)
        st.markdown("<div class='tb'><div class='lg'>"
                    "HMF Book</div></div>",
                    unsafe_allow_html=True)
        tq = st.columns(6)
        if tq[0].button("✉️", key="tbm",
                        use_container_width=True):
            go("Messages")
        bl = "🔔"
        if unread > 0:
            bl = "🔔" + str(unread)
        if tq[1].button(bl, key="tbn",
                        use_container_width=True):
            go("Notifications")
        if tq[2].button("🌙" if not SS.dark else "☀️",
                        key="tbd", use_container_width=True):
            SS.dark = not SS.dark
            rr()
        if tq[3].button("⚙️", key="tbs",
                        use_container_width=True):
            go("Settings")
        if tq[4].button("👤", key="tbp",
                        use_container_width=True):
            go("Profile")
        if tq[5].button("🚪", key="tbo",
                        use_container_width=True):
            SS.logged_in = False
            SS.page = "auth"
            rr()

        # NAV
        nv = st.columns(8)
        for i, (t, ic) in enumerate(
                [("Home", "🏠"), ("Search", "🔍"),
                 ("Reels", "🎬"), ("Market", "🛒"),
                 ("Messages", "✉️"), ("Create", "➕"),
                 ("Friends", "👥"), ("Profile", "👤")]):
            mk = ic
            if SS.tab == t:
                mk = "🔹"
            if nv[i].button(mk, key="nv_" + t,
                            use_container_width=True):
                go(t)

        # VIEW USER
        if SS.view_user and SS.view_user != SS.username:
            vu = SS.view_user
            if vu not in db["users"]:
                SS.view_user = None
                rr()
            ud = db["users"][vu]
            st.markdown("<div class='fbc'></div>",
                        unsafe_allow_html=True)
            st.markdown("<div style='text-align:center;"
                        "margin-top:-50px;'>" +
                        av(vu, ud.get("avatar"), 90) +
                        "</div>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:center;'>"
                        + esc(ud.get("display_name", vu)) +
                        "</h3>", unsafe_allow_html=True)
            v1, v2 = st.columns(2)
            if v1.button("✉️ Message", key="vfm"):
                SS.msg_view = "chat"
                SS.msg_target = vu
                SS.msg_ttype = "direct"
                SS.view_user = None
                go("Messages")
            if v2.button("← Back", key="vbk"):
                SS.view_user = None
                rr()
        else:
            if SS.view_user == SS.username:
                SS.view_user = None
                SS.tab = "Profile"

            # ===== HOME =====
            if SS.tab == "Home":

                if me.get("show_stories", True):
                    st.markdown(
                        "<div style='display:flex;gap:14px;"
                        "padding:10px 0;border-bottom:1px "
                        "solid #e5e7eb;overflow-x:auto;'>"
                        "<div style='width:54px;height:54px;"
                        "border-radius:50%;background:#dbdbdb;"
                        "display:flex;align-items:center;"
                        "justify-content:center;font-weight:"
                        "bold;'>+</div>"
                        "<div style='width:54px;height:54px;"
                        "border-radius:50%;padding:2px;"
                        "background:linear-gradient(135deg,"
                        "#00B074,#056839);'><div style="
                        "'width:100%;height:100%;border-"
                        "radius:50%;background:#fff;display:"
                        "flex;align-items:center;justify-"
                        "content:center;font-weight:bold;"
                        "font-size:12px;'>HJ</div></div>"
                        "</div>", unsafe_allow_html=True)

                q1, q2, q3, q4 = st.columns(4)
                if q1.button("Groups", key="hq1",
                             use_container_width=True):
                    go("Groups")
                if q2.button("Pages", key="hq2",
                             use_container_width=True):
                    go("Pages")
                if q3.button("Events", key="hq3",
                             use_container_width=True):
                    go("Events")
                if q4.button("Games", key="hq4",
                             use_container_width=True):
                    go("Games")

                vis = []
                for p in db["posts"]:
                    if p.get("type") != "reel":
                        if p["user"] not in SS.blocked:
                            vis.append(p)

                ads = []
                for a in db["ads"]:
                    if a.get("status") == "active":
                        ads.append(a)

                if SS.clear_c:
                    SS[SS.clear_c] = ""
                    SS.clear_c = ""

                for idx, p in enumerate(vis):
                    st.markdown("<div class='pc'><div "
                                "class='ph2'>" +
                                av(p["user"],
                                   p.get("avatar")) +
                                "<div class='pu'>" +
                                esc(p["user"]) +
                                "</div></div></div>",
                                unsafe_allow_html=True)
                    pt = p.get("type", "text")
                    if pt == "text":
                        st.markdown(
                            "<div class='pph' style="
                            "'background:" +
                            p.get("grad", "#f0f0f0") +
                            ";color:#056839;font-weight:"
                            "bold;'>" +
                            esc(p.get("txt", "")) +
                            "</div>", unsafe_allow_html=True)
                    elif pt == "youtube":
                        components.html(
                            "<iframe width='100%' height='225'"
                            " src='https://www.youtube.com/"
                            "embed/" + p["ref"] +
                            "' frameborder='0' "
                            "allowfullscreen></iframe>",
                            height=235)
                    elif pt == "image" and isfile(p["ref"]):
                        st.image(p["ref"],
                                 use_container_width=True)
                    elif pt == "video":
                        st.video(p["ref"])

                    liked = SS.username in p.get("likes", {})
                    c1, c2, c3 = st.columns(3)
                    if liked:
                        ic = "❤️"
                    else:
                        ic = "🤍"
                    if c1.button(ic, key="lk_" + p["id"],
                                 use_container_width=True):
                        db = load_db()
                        for po in db["posts"]:
                            if po["id"] == p["id"]:
                                lk = po.setdefault("likes", {})
                                if SS.username in lk:
                                    del lk[SS.username]
                                else:
                                    lk[SS.username] = True
                                break
                        save_db(db)
                        rr()
                    if c2.button("👤", key="vu_" + p["id"],
                                 use_container_width=True):
                        SS.view_user = p["user"]
                        rr()
                    if c3.button("🚫", key="bl_" + p["id"],
                                 use_container_width=True):
                        db = load_db()
                        rec = db["users"].get(SS.username)
                        if rec is not None:
                            bl = rec.setdefault("blocked", [])
                            if p["user"] not in bl:
                                bl.append(p["user"])
                            save_db(db)
                            SS.blocked = list(bl)
                        rr()

                    nl = str(len(p.get("likes", {})))
                    st.markdown("<p class='lk'>" + nl +
                                " likes</p><p class='pd'>"
                                "<b>" + esc(p["user"]) +
                                "</b> " +
                                esc(p.get("cap", "")) +
                                "</p>", unsafe_allow_html=True)

                    cm = st.text_input("c", key="c_" + p["id"],
                                       placeholder="Comment...",
                                       label_visibility="collapsed")
                    if st.button("Post", key="p_" + p["id"]):
                        if cm.strip():
                            if not clean(cm) and \
                                    me.get("comment_filter",
                                           True):
                                st.warning("Filtered!")
                            else:
                                db = load_db()
                                for po in db["posts"]:
                                    if po["id"] == p["id"]:
                                        po.setdefault(
                                            "comments",
                                            []).append(
                                            {"user": SS.username,
                                             "text": cm})
                                        break
                                save_db(db)
                                SS.clear_c = "c_" + p["id"]
                                rr()
                    for c in p.get("comments", []):
                        st.markdown(
                            "<p class='pd' style="
                            "'color:#6b7280;'><b>" +
                            esc(c["user"]) + "</b> " +
                            esc(c["text"]) + "</p>",
                            unsafe_allow_html=True)

                    if ads and (idx + 1) % 3 == 0:
                        ad = ads[(idx // 3) % len(ads)]
                        st.markdown(
                            "<div class='ad'><span class="
                            "'at'>SPONSORED</span><br><b>" +
                            esc(ad["title"]) + "</b></div>",
                            unsafe_allow_html=True)

            # ===== REELS =====
            elif SS.tab == "Reels":
                if SS.open_reel:
                    rp = None
                    for p in db["posts"]:
                        if p["id"] == SS.open_reel:
                            rp = p
                            break
                    if rp is None:
                        SS.open_reel = ""
                        rr()
                    if st.button("← Back", key="rbk"):
                        SS.open_reel = ""
                        rr()
                    st.markdown("<div class='ph2'>" +
                                av(rp["user"],
                                   rp.get("avatar")) +
                                "<div class='pu'>@" +
                                esc(rp["user"]) +
                                "</div></div>",
                                unsafe_allow_html=True)
                    st.video(rp["ref"])
                    liked = SS.username in rp.get("likes", {})
                    if liked:
                        ic = "❤️"
                    else:
                        ic = "🤍"
                    if st.button(ic + " " + str(
                            len(rp.get("likes", {}))),
                            key="rlk"):
                        db = load_db()
                        for po in db["posts"]:
                            if po["id"] == rp["id"]:
                                lk = po.setdefault("likes", {})
                                if SS.username in lk:
                                    del lk[SS.username]
                                else:
                                    lk[SS.username] = True
                                break
                        save_db(db)
                        rr()
                else:
                    st.markdown("<div class='ph'>🎬 Reels"
                                "</div>", unsafe_allow_html=True)
                    rl = []
                    for p in db["posts"]:
                        if p.get("type") in ("reel", "video"):
                            rl.append(p)
                    for r in reversed(rl):
                        if st.button("▶ " +
                                     r.get("cap",
                                           "Reel")[:15],
                                     key="rop_" + r["id"],
                                     use_container_width=True):
                            SS.open_reel = r["id"]
                            rr()
                        st.video(r["ref"])

            # ===== SEARCH =====
            elif SS.tab == "Search":
                st.markdown("<div class='ph'>🔍 Search"
                            "</div>", unsafe_allow_html=True)
                q = st.text_input("Search...", key="sq")
                if q.strip():
                    ql = q.strip().lower()
                    for u in db["users"]:
                        if ql in u.lower():
                            st.markdown(
                                "<div class='fr'>" +
                                av(u, None, 40) +
                                "<div><b>@" + u + "</b>"
                                "</div></div>",
                                unsafe_allow_html=True)
                            if st.button("Open",
                                         key="so_" + u,
                                         use_container_width
                                         =True):
                                SS.view_user = u
                                rr()
                    for p in db["posts"]:
                        cp = p.get("cap", "") or ""
                        if ql in cp.lower():
                            if st.button("▶ " + cp[:20],
                                         key="spo_" +
                                         p["id"],
                                         use_container_width
                                         =True):
                                rr()
                    for l in db["listings"]:
                        if ql in l["title"].lower():
                            if st.button("PKR " +
                                         str(l["price"]) +
                                         " - " +
                                         l["title"][:20],
                                         key="slo_" +
                                         l["id"],
                                         use_container_width
                                         =True):
                                SS.open_list = l["id"]
                                SS.tab = "Market"
                                rr()
                else:
                    st.caption("Kuch bhi likhein...")

            # ===== FRIENDS =====
            elif SS.tab == "Friends":
                st.markdown("<div class='ph'>👥 Friends"
                            "</div>", unsafe_allow_html=True)
                inr = []
                for r in db["friend_requests"]:
                    if r["to"] == SS.username:
                        inr.append(r)
                frs = db["friends"].get(SS.username, [])
                if inr:
                    st.markdown("### 📨 Requests")
                    for i, r in enumerate(inr):
                        f = r["from"]
                        f1, f2 = st.columns(2)
                        f1.markdown("<div class='fr'>" +
                                    av(f, None, 40) +
                                    "<b>@" + f + "</b></div>",
                                    unsafe_allow_html=True)
                        if f2.button("✅",
                                     key="fa_" + str(i)):
                            db = load_db()
                            db["friend_requests"] = [
                                x for x in
                                db["friend_requests"]
                                if not (x["from"] == f
                                        and x["to"] ==
                                        SS.username)]
                            db["friends"].setdefault(
                                SS.username, []).append(f)
                            db["friends"].setdefault(
                                f, []).append(SS.username)
                            save_db(db)
                            rr()
                st.markdown("### 🌟 Suggestions")
                for u in db["users"]:
                    if u == SS.username or u in frs:
                        continue
                    s1, s2 = st.columns(2)
                    s1.markdown("<div class='fr'>" +
                                av(u, None, 40) +
                                "<b>@" + u + "</b></div>",
                                unsafe_allow_html=True)
                    if s2.button("➕", key="sg_" + u):
                        db = load_db()
                        db["friend_requests"].append(
                            {"from": SS.username, "to": u,
                             "time": time.time()})
                        save_db(db)
                        rr()

            # ===== GROUPS/PAGES/EVENTS/MARKET =====
            elif SS.tab == "Groups":
                st.markdown("<div class='ph'>👥 Groups"
                            "</div>", unsafe_allow_html=True)
                with st.expander("➕ Create"):
                    gn = st.text_input("Name", key="gn")
                    if st.button("Create", key="gcr",
                                 use_container_width=True):
                        if gn.strip():
                            db = load_db()
                            db["groups"].append(
                                {"id": uuid.uuid4().hex[:8],
                                 "name": gn.strip(),
                                 "members": [SS.username],
                                 "messages": []})
                            save_db(db)
                            rr()
                for g in db["groups"]:
                    st.markdown("<div class='gc'><div "
                                "class='gv'></div><div "
                                "class='gn'>" +
                                esc(g["name"]) +
                                "</div><div class='gs'>" +
                                str(len(g["members"])) +
                                " members</div></div>",
                                unsafe_allow_html=True)
                    if st.button("Open", key="go_" + g["id"],
                                 use_container_width=True):
                        SS.open_group = g["id"]
                        rr()

            elif SS.tab == "Pages":
                st.markdown("<div class='ph'>📄 Pages"
                            "</div>", unsafe_allow_html=True)
                with st.expander("➕ Create"):
                    pn = st.text_input("Name", key="pn")
                    if st.button("Create", key="pcr",
                                 use_container_width=True):
                        if pn.strip():
                            db = load_db()
                            db["pages"].append(
                                {"id": uuid.uuid4().hex[:8],
                                 "name": pn.strip(),
                                 "owner": SS.username,
                                 "followers": []})
                            save_db(db)
                            rr()
                for pg in db["pages"]:
                    st.markdown("<div class='gc'><div "
                                "class='gn'>📄 " +
                                esc(pg["name"]) +
                                "</div></div>",
                                unsafe_allow_html=True)
                    if st.button("Open", key="po_" + pg["id"],
                                 use_container_width=True):
                        SS.open_page = pg["id"]
                        rr()

            elif SS.tab == "Events":
                st.markdown("<div class='ph'>📅 Events"
                            "</div>", unsafe_allow_html=True)
                with st.expander("➕ Create"):
                    et = st.text_input("Title", key="et")
                    if st.button("Create", key="ecr",
                                 use_container_width=True):
                        if et.strip():
                            db = load_db()
                            db["events"].append(
                                {"id": uuid.uuid4().hex[:8],
                                 "title": et.strip(),
                                 "host": SS.username,
                                 "location": "",
                                 "rsvps": []})
                            save_db(db)
                            rr()
                for ev in db["events"]:
                    st.markdown("<div class='gc'><div "
                                "class='gn'>📅 " +
                                esc(ev["title"]) +
                                "</div></div>",
                                unsafe_allow_html=True)

            elif SS.tab == "Market":
                if SS.open_list:
                    ls = None
                    for x in db["listings"]:
                        if x["id"] == SS.open_list:
                            ls = x
                            break
                    if ls is None:
                        SS.open_list = ""
                        rr()
                    if st.button("← Back", key="mbk"):
                        SS.open_list = ""
                        rr()
                    st.markdown("<div class='ph'>🛒 " +
                                esc(ls["title"]) +
                                "</div>", unsafe_allow_html=True)
                    st.markdown("<h2 style='color:#00B074;"
                                "'>PKR " + str(ls["price"]) +
                                "</h2>", unsafe_allow_html=True)
                    if ls["seller"] != SS.username:
                        if st.button("✉️ Message Seller",
                                     key="msl",
                                     use_container_width=True):
                            smsg(False, "",
                                 ls["seller"],
                                 "Interested: " +
                                 ls["title"])
                            SS.msg_view = "chat"
                            SS.msg_target = ls["seller"]
                            SS.msg_ttype = "direct"
                            SS.open_list = ""
                            go("Messages")
                else:
                    st.markdown("<div class='ph'>🛒 Market"
                                "</div>", unsafe_allow_html=True)
                    with st.expander("➕ Sell"):
                        st_ = st.text_input("Title", key="st")
                        sp = st.number_input("PKR",
                                             min_value=0,
                                             key="sp")
                        if st.button("List", key="slb",
                                     use_container_width=True):
                            if st_.strip():
                                db = load_db()
                                db["listings"].insert(0, {
                                    "id": uuid.uuid4()
                                    .hex[:8],
                                    "seller": SS.username,
                                    "title": st_.strip(),
                                    "price": int(sp),
                                    "image": None,
                                    "status": "available"})
                                save_db(db)
                                rr()
                    for l in db["listings"]:
                        st.markdown("<div class='gc'><div "
                                    "class='gn'>" +
                                    esc(l["title"]) +
                                    "</div><div class="
                                    "'gs'>PKR " +
                                    str(l["price"]) +
                                    " · @" +
                                    esc(l["seller"]) +
                                    "</div></div>",
                                    unsafe_allow_html=True)
                        if st.button("Open",
                                     key="lo_" + l["id"],
                                     use_container_width=True):
                            SS.open_list = l["id"]
                            rr()

            # ===== CREATE =====
            elif SS.tab == "Create":
                st.markdown("<div class='ph'>➕ Create"
                            "</div>", unsafe_allow_html=True)
                kind = st.radio("Type:",
                                ["Photo", "Video",
                                 "Camera 🎨", "YouTube"],
                                horizontal=True, key="ck")
                cap = st.text_input("Caption", key="uc")
                if kind == "Camera 🎨":
                    fl = st.selectbox("Filter:", FILTERS,
                                      key="cf")
                    cam = st.camera_input("📸", key="cam")
                    fi = None
                    if cam is not None:
                        try:
                            pil = Image.open(cam)
                            fi = filt(pil, fl)
                            buf = io.BytesIO()
                            fi.save(buf, format="PNG")
                            st.image(buf.getvalue())
                        except Exception:
                            pass
                    if st.button("Post", key="up2",
                                 use_container_width=True):
                        if fi is None:
                            st.warning("Photo!")
                        else:
                            db = load_db()
                            db["posts"].insert(0, {
                                "id": uuid.uuid4().hex[:8],
                                "user": SS.username,
                                "type": "image",
                                "ref": spil(fi),
                                "cap": cap, "likes": {},
                                "comments": []})
                            save_db(db)
                            go("Home")
                elif kind == "YouTube":
                    yl = st.text_input("Link", key="uy")
                    if st.button("Post", key="up1",
                                 use_container_width=True):
                        vid = parse_yt(yl)
                        if vid:
                            db = load_db()
                            db["posts"].insert(0, {
                                "id": uuid.uuid4().hex[:8],
                                "user": SS.username,
                                "type": "youtube",
                                "ref": vid, "cap": cap,
                                "likes": {}, "comments": []})
                            save_db(db)
                            go("Home")
                        else:
                            st.error("Invalid!")
                else:
                    if kind == "Photo":
                        f = st.file_uploader(
                            "Photo", type=["png", "jpg",
                                           "jpeg"],
                            key="uf")
                    else:
                        f = st.file_uploader(
                            "Video", type=["mp4", "mov"],
                            key="uv")
                    if st.button("Post", key="up3",
                                 use_container_width=True):
                        if f is None:
                            st.warning("File!")
                        else:
                            db = load_db()
                            if kind == "Video":
                                pt = "video"
                            else:
                                pt = "image"
                            db["posts"].insert(0, {
                                "id": uuid.uuid4().hex[:8],
                                "user": SS.username,
                                "type": pt,
                                "ref": supload(f),
                                "cap": cap, "likes": {},
                                "comments": []})
                            save_db(db)
                            go("Home")

            # ===== MESSAGES =====
            elif SS.tab == "Messages":

                if HAS_REFRESH:
                    st_autorefresh(interval=4000, key="mr")
                db = load_db()

                if SS.msg_view == "chat":
                    tgt = SS.msg_target
                    isg = (SS.msg_ttype == "group")
                    grp = None
                    if isg:
                        for g in db["groups"]:
                            if g["id"] == tgt:
                                grp = g
                                break
                        if grp is None:
                            SS.msg_view = "list"
                            rr()
                    elif tgt not in db["users"]:
                        SS.msg_view = "list"
                        rr()

                    if st.button("← Back", key="cbk"):
                        SS.msg_view = "list"
                        rr()

                    if isg and grp is not None:
                        st.markdown("<h3>👥 " +
                                    esc(grp["name"]) +
                                    "</h3>",
                                    unsafe_allow_html=True)
                        msgs = grp.get("messages", [])
                    elif tgt in db["users"]:
                        ud = db["users"][tgt]
                        seen(SS.username, tgt)
                        st.markdown(
                            "<div class='ph2'>" +
                            av(tgt, ud.get("avatar")) +
                            "<div class='pu'>@" +
                            esc(ud.get("display_name",
                                      tgt)) +
                            "</div></div>",
                            unsafe_allow_html=True)
                        msgs = []
                        for m in db["messages"]:
                            if (m["from"] == SS.username
                                    and m["to"] == tgt):
                                msgs.append(m)
                            elif (m["from"] == tgt
                                  and m["to"] ==
                                  SS.username):
                                msgs.append(m)

                    if SS.clear_m:
                        SS[SS.clear_m] = ""
                        SS.clear_m = ""

                    for m in sorted(msgs,
                                    key=lambda x: x["time"]):
                        mine = m["from"] == SS.username
                        ts = time.strftime(
                            "%I:%M %p",
                            time.localtime(m["time"])).lower()
                        if m.get("photo") and \
                                isfile(m["photo"]):
                            st.image(m["photo"], width=180)
                        if mine:
                            cls = "bm"
                        else:
                            cls = "bh"
                        st.markdown(
                            "<span class='" + cls + "'>" +
                            esc(m.get("text", "")) +
                            "<span class='bt'>" + ts +
                            "</span></span>",
                            unsafe_allow_html=True)
                        r = m.get("reactions", [])
                        mk = m.get("id", str(m["time"]))
                        if r:
                            lb = "👍 " + str(len(r))
                        else:
                            lb = "👍"
                        if st.button(lb, key="rx_" + mk):
                            tog_rx(isg, tgt, m.get("id"),
                                   SS.username)
                            rr()

                    with st.expander("📷 Photo"):
                        ph = st.file_uploader(
                            "Photo", type=["png", "jpg"],
                            key="cph")
                        if st.button("Send", key="csp",
                                     use_container_width=True):
                            if ph is not None:
                                smsg(isg, tgt, tgt, "📷 Photo",
                                     photo=supload(ph))
                            rr()

                    tx = st.text_input("Message...", key="ctx")
                    if st.button("Send", key="csd",
                                 use_container_width=True):
                        if tx.strip():
                            smsg(isg, tgt, tgt, tx.strip())
                            SS.clear_m = "ctx"
                            rr()

                else:
                    st.markdown("<div class='ph'>✉️ Chats"
                                "</div>", unsafe_allow_html=True)
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
                        if p != SS.username and \
                                p not in SS.blocked:
                            cn = []
                            for m in db["messages"]:
                                if (m["from"] == SS.username
                                        and m["to"] == p):
                                    cn.append(m)
                                elif (m["from"] == p
                                      and m["to"] ==
                                      SS.username):
                                    cn.append(m)
                            last = None
                            if cn:
                                last = cn[-1]
                            convs.append({"u": p, "last": last,
                                          "un": unseen(
                                              SS.username, p)})
                    for g in db["groups"]:
                        if SS.username in g["members"]:
                            gms = g.get("messages", [])
                            last = None
                            if gms:
                                last = gms[-1]
                            convs.append({"g": g, "last": last})
                    convs.sort(key=lambda c: (
                        c["last"]["time"] if c["last"]
                        else 0), reverse=True)
                    if not convs:
                        st.info("No chats!")
                    for c in convs:
                        isg2 = "g" in c
                        if not isg2:
                            p = c["u"]
                            ud = db["users"].get(p, {})
                            nm = esc(ud.get("display_name", p))
                            avh = av(p, ud.get("avatar"), 46)
                            kid = p
                            pv = "Say hello 👋"
                            if c["last"]:
                                if c["last"]["from"] == \
                                        SS.username:
                                    pre = "You: "
                                else:
                                    pre = ""
                                pv = pre + esc(
                                    c["last"].get("text",
                                                  ""))[:28]
                            bd = ""
                            if c["un"] > 0:
                                bd = "<span class='ub'>" + \
                                     str(c["un"]) + "</span>"
                        else:
                            g = c["g"]
                            nm = "👥 " + esc(g["name"])
                            avh = av(g["name"], None, 46)
                            kid = g["id"]
                            pv = "Group"
                            bd = ""
                        st.markdown(
                            "<div class='ci'><div class="
                            "'aw'>" + avh + "</div><div "
                            "class='cn'><div class='nm'>" +
                            nm + "</div><div class='pv'>" +
                            pv + "</div></div>" + bd +
                            "</div>", unsafe_allow_html=True)
                        if st.button("💬", key="op_" + kid,
                                     use_container_width=True):
                            SS.msg_view = "chat"
                            SS.msg_target = kid
                            if isg2:
                                SS.msg_ttype = "group"
                            else:
                                SS.msg_ttype = "direct"
                            rr()

                    with st.expander("➕ New"):
                        others = []
                        for x in db["users"]:
                            if x != SS.username:
                                others.append(x)
                        pick = st.selectbox("Chat:", others,
                                            key="ncs")
                        if st.button("Start", key="ncb",
                                     use_container_width=True):
                            SS.msg_view = "chat"
                            SS.msg_target = pick
                            SS.msg_ttype = "direct"
                            rr()
                        gn = st.text_input("Group name",
                                           key="gn2")
                        gm = st.multiselect("Members", others,
                                            key="gm2")
                        if st.button("Create Group", key="gcb",
                                     use_container_width=True):
                            if gn.strip() and gm:
                                db = load_db()
                                db["groups"].append({
                                    "id": uuid.uuid4()
                                    .hex[:8],
                                    "name": gn.strip(),
                                    "members":
                                    [SS.username] + gm,
                                    "messages": []})
                                save_db(db)
                                rr()

            # ===== NOTIFICATIONS =====
            elif SS.tab == "Notifications":
                st.markdown("<div class='ph'>🔔 Notifications"
                            "</div>", unsafe_allow_html=True)
                db = load_db()
                mn = []
                for n in db["notifications"]:
                    if n.get("to") == SS.username:
                        mn.append(n)
                mn = mn[:40]
                if st.button("Mark read", key="mkr",
                             use_container_width=True):
                    db = load_db()
                    for n in db["notifications"]:
                        if n.get("to") == SS.username:
                            n["read"] = True
                    save_db(db)
                    rr()
                if not mn:
                    st.info("Empty!")
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

            # ===== GAMES =====
            elif SS.tab == "Games":
                st.markdown("<div class='ph'>🎲 Games"
                            "</div>", unsafe_allow_html=True)
                if st.button("🎲 Roll Dice",
                             use_container_width=True):
                    SS.dice = random.randint(1, 6)
                    if SS.dice == 6:
                        db = load_db()
                        u = db["users"].get(SS.username)
                        if u is not None:
                            u["coins"] = u.get("coins", 0) + 5
                            save_db(db)
                    rr()
                if SS.dice:
                    st.markdown(
                        "<h2 style='text-align:center;"
                        "color:#00B074;'>🎯 " +
                        str(SS.dice) + "</h2>",
                        unsafe_allow_html=True)

            # ===== PROFILE =====
            elif SS.tab == "Profile":
                me = db["users"].get(SS.username, {})
                mp = []
                for p in db["posts"]:
                    if p["user"] == SS.username:
                        mp.append(p)
                fr = db["friends"].get(SS.username, [])
                st.markdown("<div class='fbc'></div>",
                            unsafe_allow_html=True)
                st.markdown("<div style='text-align:center;"
                            "margin-top:-50px;'>" +
                            av(SS.username, me.get("avatar"),
                               90) + "</div>",
                            unsafe_allow_html=True)
                st.markdown(
                    "<h3 style='text-align:center;'>"
                    + esc(me.get("display_name",
                                 SS.username)) +
                    "</h3><p style='text-align:center;"
                    "color:#4b5563;font-size:13px;'>"
                    + str(len(fr)) + " friends · " +
                    str(len(mp)) + " posts · 💰" +
                    str(me.get("coins", 0)) + "</p>",
                    unsafe_allow_html=True)
                if is_owner:
                    st.markdown("<p style='text-align:"
                                "center;'><span class="
                                "'ob'>👑 OWNER</span></p>",
                                unsafe_allow_html=True)
                with st.expander("🖼️ Change Pic"):
                    fl = st.selectbox("Filter:", FILTERS,
                                      key="pf")
                    pi = st.file_uploader(
                        "Upload", type=["png", "jpg"],
                        key="pi")
                    if st.button("Update", key="pu",
                                 use_container_width=True):
                        if pi is not None:
                            pil = Image.open(pi)
                            setp(SS.username, "avatar",
                                 spil(filt(pil, fl)))
                            st.success("Updated!")
                            rr()
                if st.button("💰 Payout (100 coins)",
                             key="pp",
                             use_container_width=True):
                    db = load_db()
                    u = db["users"].get(SS.username)
                    if u is not None and \
                            u.get("coins", 0) >= 100:
                        u["coins"] -= 100
                        save_db(db)
                        st.success("Payout!")
                        rr()
                    else:
                        st.warning("Min 100!")

            # ===== SETTINGS =====
            elif SS.tab == "Settings":

                if SS.setpage == "menu":
                    st.markdown("<div class='ph'>⚙️ Settings"
                                "</div>", unsafe_allow_html=True)
                    for label, pg in [
                            ("🔐 Security", "security"),
                            ("📋 Personal", "personal"),
                            ("📰 Feed", "feed"),
                            ("🚫 Blocked", "blocked"),
                            ("ℹ️ About", "about")]:
                        if st.button(label + " ›",
                                     key="m_" + pg,
                                     use_container_width=True):
                            SS.setpage = pg
                            rr()
                    if is_owner:
                        if st.button("🛡️ OWNER ›",
                                     key="mown",
                                     use_container_width=True):
                            SS.setpage = "admin"
                            rr()
                    if st.button("🚪 Logout", key="mlo",
                                 use_container_width=True):
                        SS.logged_in = False
                        SS.page = "auth"
                        rr()

                elif SS.setpage == "security":
                    if st.button("← Back", key="bs"):
                        SS.setpage = "menu"
                        rr()
                    if not me.get("app_lock"):
                        npin = st.text_input(
                            "4-digit PIN", type="password",
                            max_chars=4, key="spn")
                        if st.button("Enable Lock",
                                     key="sae",
                                     use_container_width=True):
                            if len(npin) == 4 and \
                                    npin.isdigit():
                                setp(SS.username,
                                     "app_pin", npin)
                                setp(SS.username,
                                     "app_lock", True)
                                st.success("ON!")
                                rr()
                            else:
                                st.warning("4 digits!")
                    else:
                        st.success("Lock ON")
                        l1, l2 = st.columns(2)
                        if l1.button("Lock Now", key="sln",
                                     use_container_width=True):
                            SS.pin_ok = False
                            rr()
                        if l2.button("Disable", key="sdn",
                                     use_container_width=True):
                            setp(SS.username, "app_lock",
                                 False)
                            setp(SS.username, "app_pin", "")
                            rr()
                    cf = st.checkbox(
                        "Fingerprint",
                        value=me.get("finger_lock", False),
                        key="sfl")
                    if cf != me.get("finger_lock", False):
                        setp(SS.username, "finger_lock", cf)
                        if cf:
                            SS.fin_ok = False
                        else:
                            SS.fin_ok = True
                        rr()
                    cur = me.get("auto_logout", 0)
                    opts = [0, 5, 10, 30]
                    if cur in opts:
                        ci = opts.index(cur)
                    else:
                        ci = 0
                    nal = st.selectbox("Auto logout min:",
                                       opts, index=ci,
                                       key="sal")
                    if nal != cur:
                        setp(SS.username, "auto_logout", nal)
                        rr()

                elif SS.setpage == "personal":
                    if st.button("← Back", key="bp"):
                        SS.setpage = "menu"
                        rr()
                    dn = st.text_input(
                        "Name",
                        value=me.get("display_name", ""),
                        key="pdn")
                    bio = st.text_input(
                        "Bio", value=me.get("bio", ""),
                        key="pbio")
                    if st.button("Save", key="psv",
                                 use_container_width=True):
                        setp(SS.username, "display_name", dn)
                        setp(SS.username, "bio", bio)
                        st.success("Saved!")

                elif SS.setpage == "feed":
                    if st.button("← Back", key="bf"):
                        SS.setpage = "menu"
                        rr()
                    cs = st.checkbox(
                        "Show Stories",
                        value=me.get("show_stories", True),
                        key="nss")
                    if cs != me.get("show_stories", True):
                        setp(SS.username, "show_stories", cs)
                        rr()
                    cc = st.checkbox(
                        "Word Filter",
                        value=me.get("comment_filter", True),
                        key="ncf")
                    if cc != me.get("comment_filter", True):
                        setp(SS.username, "comment_filter", cc)
                        rr()

                elif SS.setpage == "blocked":
                    if st.button("← Back", key="bbl"):
                        SS.setpage = "menu"
                        rr()
                    bi = st.text_input("Username", key="bki")
                    if st.button("Block", key="bkb",
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
                                SS.blocked = list(
                                    rec["blocked"])
                            rr()
                    for i, u in enumerate(SS.blocked):
                        b1, b2 = st.columns([0.6, 0.4])
                        b1.markdown("🚫 @" + u)
                        if b2.button("Unblock",
                                     key="ubk_" + str(i),
                                     use_container_width=True):
                            SS.blocked.remove(u)
                            db = load_db()
                            rec = db["users"].get(
                                SS.username)
                            if rec is not None:
                                rec["blocked"] = SS.blocked
                                save_db(db)
                            rr()

                elif SS.setpage == "about":
                    if st.button("← Back", key="baf"):
                        SS.setpage = "menu"
                        rr()
                    st.markdown("### ℹ️ HMF Book")
                    st.markdown(
                        "**🏢 Parent:** HMF Group\n\n"
                        "**👑 Founders:** Mehmood Sial, "
                        "Hoor-e-Jannat, Farwa\n\n"
                        "**📍 HQ:** Bahawalpur / Okara\n\n"
                        "© 2026 HMF Group")

                elif SS.setpage == "admin":
                    if st.button("← Back", key="bad"):
                        SS.setpage = "menu"
                        rr()
                    st.markdown("<div class='ph'>🛡️ Owner"
                                "</div>", unsafe_allow_html=True)
                    db = load_db()
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Users", len(db["users"]))
                    c2.metric("Posts", len(db["posts"]))
                    c3.metric("Reports", len(db["reports"]))
                    for i, r in enumerate(
                            reversed(db["reports"][:10])):
                        r1, r2 = st.columns([0.6, 0.4])
                        r1.markdown("🚩 @" +
                                    esc(r.get("user", "")))
                        ru = r.get("user", "")
                        if ru in db["banned"]:
                            if r2.button("Unban",
                                         key="ru_" + str(i),
                                         use_container_width
                                         =True):
                                db = load_db()
                                db["banned"].remove(ru)
                                save_db(db)
                                rr()
                        else:
                            if r2.button("BAN",
                                         key="rbn_" + str(i),
                                         use_container_width
                                         =True):
                                db = load_db()
                                db["banned"].append(ru)
                                save_db(db)
                                rr()


# ---------- SAFETY ----------
else:
    SS.page = "splash"
    rr()

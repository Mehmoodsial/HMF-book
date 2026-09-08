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
    if s == hash_pw(p):
        return True
    return s == p


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


def notify(to, text, kind="messages"):
    if not to:
        return
    db = load_db()
    rec = db["users"].get(to)
    if rec is not None:
        pr = rec.get("notif", {})
        if kind in pr and not pr.get(kind, True):
            return
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
    low = t.lower()
    for w in BAD_WORDS:
        if w in low:
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
                if "messages" not in g:
                    g["messages"] = []
                g["messages"].append(m)
                break
        save_db(db)
        db2 = load_db()
        for g in db2["groups"]:
            if g["id"] == gid:
                for mm in g["members"]:
                    if mm != me:
                        notify(mm, "GROUP: @" + me + " " + text[:25])
                break
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
    p = os.path.join(UPLOAD_DIR,
                     uuid.uuid4().hex + "." + ext)
    with open(p, "wb") as o:
        o.write(f.getbuffer())
    return p


def spil(img):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    p = os.path.join(UPLOAD_DIR,
                     uuid.uuid4().hex + ".png")
    img.save(p, "PNG")
    return p


def av(name, path=None, size=36, border=False):
    bs = ""
    if border:
        bs = "border:4px solid #fff;"
    if path and os.path.exists(path):
        try:
            b = base64.b64encode(
                open(path, "rb").read()).decode()
            s = str(size)
            out = "<img src='data:image/png;base64,"
            out = out + b
            out = out + "' style='width:" + s
            out = out + "px;height:" + s
            out = out + "px;border-radius:50%;"
            out = out + bs + "'>"
            return out
        except Exception:
            pass
    ini = esc(str(name)[:2].upper())
    s = str(size)
    fs = str(int(size * 0.38))
    out = "<div style='width:" + s + "px;height:" + s
    out = out + "px;border-radius:50%;background:"
    out = out + "linear-gradient(135deg,#00B074,"
    out = out + "#056839);color:#fff;display:flex;"
    out = out + "align-items:center;justify-content:"
    out = out + "center;font-weight:bold;" + bs
    out = out + "font-size:" + fs + "px;'>" + ini
    out = out + "</div>"
    return out


def filt(img, name):
    try:
        im = img.convert("RGB")
        if name == "Beauty":
            b = im.filter(ImageFilter.GaussianBlur(3))
            o = Image.blend(im, b, 0.5)
            o = ImageEnhance.Brightness(o).enhance(1.1)
        elif name == "Sepia":
            o = ImageOps.colorize(im.convert("L"),
                                  "#704214", "#ffe8c0")
        elif name == "Vintage":
            o = ImageOps.colorize(im.convert("L"),
                                  "#3a2a1a", "#e8d8b0")
        elif name == "Cool":
            o = ImageOps.colorize(im.convert("L"),
                                  "#20304a", "#c8e0ff")
        elif name == "Gray":
            o = im.convert("L").convert("RGB")
        elif name == "Bright":
            o = ImageEnhance.Brightness(im).enhance(1.4)
        elif name == "Cartoon":
            w = max(1, im.width // 6)
            h = max(1, im.height // 6)
            s = im.resize((w, h))
            s = s.filter(ImageFilter.MedianFilter(7))
            o = s.resize((im.width, im.height))
            o = ImageOps.posterize(o, 5)
            o = ImageEnhance.Color(o).enhance(1.3)
        else:
            o = im
        return o
    except Exception:
        return img


def isfile(r):
    r = str(r or "")
    if r.startswith("http"):
        return False
    return os.path.exists(r)


# ---------- SEED ----------
DB = load_db()
for un, ml, pw, nm in [
        ("demo", "d@h.com", "1234", "Demo User"),
        ("hoor", "h@h.com", "1234", "Hoor Jannat"),
        ("farrukh", "f@h.com", "1234", "Farrukh M")]:
    if un not in DB["users"] and un not in DB["banned"]:
        DB["users"][un] = {
            "email": ml, "password": hash_pw(pw),
            "display_name": nm, "bio": "Hi!",
            "birthday": "Not set", "gender": "Not set",
            "coins": 550, "followers": 200, "blocked": [],
            "avatar": None, "fails": 0, "lock_until": 0,
            "app_lock": False, "app_pin": "",
            "finger_lock": False, "two_fa": False,
            "login_alerts": True, "auto_logout": 0,
            "comment_filter": True, "private": False,
            "feed_sort": "Recent", "show_stories": True,
            "notif": {"likes": True, "comments": True,
                      "follows": True, "messages": True}}
if not DB["posts"]:
    DB["posts"] = [
        {"id": "s1", "user": "hoor", "type": "youtube",
         "ref": "aqz-KE-bpKQ", "cap": "Big Buck Bunny!",
         "likes": {}, "comments": []},
        {"id": "s2", "user": "farrukh", "type": "text",
         "grad": GRADS[0], "txt": "Ludo Night!",
         "cap": "Tonight 8 PM!", "likes": {},
         "comments": []}]
if not DB["events"]:
    DB["events"].append({"id": "ev1", "title":
                         "HMF Meetup", "host": "demo",
                         "location": "Bahawalpur",
                         "date": "15 Mar 2026",
                         "rsvps": []})
if not DB["listings"]:
    DB["listings"].append({"id": "ls1", "seller":
                           "farrukh", "title":
                           "Gaming Mouse",
                           "price": 1500,
                           "category": "Electronics",
                           "description": "RGB",
                           "image": None,
                           "status": "available"})
save_db(DB)


# ---------- SESSION ----------
SS = st.session_state
defaults = {
    "page": "splash", "logged_in": False, "username": "",
    "auth_mode": "login", "tab": "Home",
    "setpage": "menu", "blocked": [],
    "clear_c": "", "clear_m": "",
    "view_user": None, "open_group": "",
    "open_page": "", "open_event": "",
    "open_list": "", "open_reel": "",
    "pin_ok": True, "fin_ok": True, "pin_att": 0,
    "pin_lock": 0, "msg_view": "list",
    "msg_target": "", "msg_ttype": "direct",
    "shot_t": 0, "dark": False, "dice": 0,
    "last_active": 0}
for k, v in defaults.items():
    if k not in SS:
        SS[k] = v


def go(tab):
    SS.tab = tab
    if tab == "Settings":
        SS.setpage = "menu"
    if tab == "Messages":
        SS.msg_view = "list"
    rr()


# ---------- CSS ----------
def css(dark):
    if dark:
        BG = "#0f1110"
        CD = "#1b1e1b"
        BR = "#2a2e2a"
        T1 = "#eef1ee"
        T2 = "#9aa69a"
        LG = "#00e08a"
    else:
        BG = "#f0f2f5"
        CD = "#ffffff"
        BR = "#e5e7eb"
        T1 = "#1f2937"
        T2 = "#4b5563"
        LG = "#00B074"
    c = "<style>"
    c = c + ".stApp{background-color:" + BG + " !important}"
    c = c + "header[data-testid=stHeader],#MainMenu,"
    c = c + "footer,[data-testid=stToolbar],"
    c = c + "[data-testid=stStatusWidget],"
    c = c + "[data-testid=stDecoration]{display:none"
    c = c + " !important}"
    c = c + ".block-container{max-width:430px;"
    c = c + "margin:0 auto;background:" + CD + ";"
    c = c + "padding:0 10px 40px !important;"
    c = c + "min-height:100vh;box-shadow:0 0 35px"
    c = c + " rgba(0,0,0,.18)}"
    c = c + ".tb{position:sticky;top:0;z-index:995;"
    c = c + "display:flex;justify-content:space-"
    c = c + "between;align-items:center;padding:12px"
    c = c + " 14px;background:" + CD + ";border-"
    c = c + "bottom:1px solid " + BR + ";margin:0 -10px}"
    c = c + ".lg{font-size:25px;font-weight:700;"
    c = c + "font-family:Segoe Script,Brush Script MT,"
    c = c + "cursive;color:" + T1 + "}"
    c = c + ".st2{display:flex;gap:14px;padding:10px"
    c = c + " 4px;border-bottom:1px solid " + BR + ";"
    c = c + "overflow-x:auto}"
    c = c + ".sc{display:flex;flex-direction:column;"
    c = c + "align-items:center;min-width:60px}"
    c = c + ".rg{width:54px;height:54px;border-"
    c = c + "radius:50%;padding:2.5px;background:"
    c = c + "linear-gradient(135deg,#00B074,#056839);"
    c = c + "display:flex;align-items:center;"
    c = c + "justify-content:center}"
    c = c + ".rgg{background:#dbdbdb}"
    c = c + ".rm{width:100%;height:100%;border-"
    c = c + "radius:50%;background:" + CD + ";"
    c = c + "border:2px solid " + CD + ";display:"
    c = c + "flex;align-items:center;justify-"
    c = c + "content:center;font-weight:bold;"
    c = c + "color:" + T2 + ";font-size:13px}"
    c = c + ".sn{font-size:11px;color:" + T2 + ";"
    c = c + "margin-top:4px}"
    c = c + ".pc{background:" + CD + ";border-bottom:"
    c = c + "1px solid " + BR + ";margin-bottom:10px}"
    c = c + ".ph2{display:flex;align-items:center;"
    c = c + "padding:10px 4px}"
    c = c + ".pu{font-size:14px;font-weight:700;"
    c = c + "color:" + T1 + "}"
    c = c + ".pph{width:100%;height:270px;background:"
    c = c + "#f3f4f6;display:flex;align-items:center;"
    c = c + "justify-content:center;font-size:15px}"
    c = c + ".lk{padding:6px 2px 0;font-weight:600;"
    c = c + "font-size:13px;color:" + T1 + ";margin:0}"
    c = c + ".pd{padding:0 2px 8px;font-size:14px;"
    c = c + "color:" + T1 + ";margin:0}"
    c = c + ".ph{padding:14px 4px;font-size:20px;"
    c = c + "font-weight:bold;color:" + LG + ";"
    c = c + "border-bottom:1px solid " + BR + ";"
    c = c + "text-align:center}"
    c = c + ".sl{font-weight:700;color:" + T1 + ";"
    c = c + "margin:12px 0 4px}"
    c = c + ".nr{padding:10px 4px;border-bottom:1px"
    c = c + " solid " + BR + ";font-size:14px;"
    c = c + "color:" + T1 + "}"
    c = c + ".ob{background:linear-gradient(135deg,"
    c = c + "#f59e0b,#d97706);color:#fff;padding:2px"
    c = c + " 10px;border-radius:12px;font-size:11px;"
    c = c + "font-weight:bold}"
    c = c + ".ci{display:flex;align-items:center;"
    c = c + "padding:11px 4px;border-bottom:1px solid"
    c = c + " " + BR + "}"
    c = c + ".aw{margin-right:8px;position:relative}"
    c = c + ".cn{flex:1;min-width:0}"
    c = c + ".nm{font-weight:700;font-size:14px;"
    c = c + "color:" + T1 + "}"
    c = c + ".pv{font-size:12px;color:" + T2 + ";"
    c = c + "overflow:hidden;text-overflow:ellipsis;"
    c = c + "white-space:nowrap;margin-top:2px}"
    c = c + ".ub{background:#00B074;color:#fff;border-"
    c = c + "radius:50%;min-width:20px;height:20px;"
    c = c + "display:inline-flex;align-items:center;"
    c = c + "justify-content:center;font-size:11px;"
    c = c + "font-weight:700;padding:0 6px}"
    c = c + ".bm{background:#00B074;color:#fff;"
    c = c + "padding:8px 13px;border-radius:18px 18px"
    c = c + " 4px 18px;max-width:78%;margin:3px 0 3px"
    c = c + " auto;font-size:14px;display:block;"
    c = c + "width:fit-content}"
    c = c + ".bh{background:" + BR + ";color:" + T1 + ";"
    c = c + "padding:8px 13px;border-radius:18px 18px"
    c = c + " 18px 4px;max-width:78%;margin:3px auto"
    c = c + " 3px 0;font-size:14px;display:block;"
    c = c + "width:fit-content}"
    c = c + ".bt{font-size:10px;opacity:.75;display:"
    c = c + "block;text-align:right;margin-top:2px}"
    c = c + ".en{text-align:center;font-size:11px;"
    c = c + "color:" + T2 + ";background:rgba(0,176,"
    c = c + "116,.07);border-radius:10px;padding:6px;"
    c = c + "margin:6px 0}"
    c = c + ".fr{display:flex;align-items:center;"
    c = c + "padding:10px 4px;border-bottom:1px solid"
    c = c + " " + BR + "}"
    c = c + ".gc{border:1px solid " + BR + ";border-"
    c = c + "radius:12px;padding:12px;margin-bottom:"
    c = c + "10px}"
    c = c + ".gv{height:60px;border-radius:8px;"
    c = c + "background:linear-gradient(135deg,"
    c = c + "#00B074,#056839);margin-bottom:8px}"
    c = c + ".gn{font-weight:800;font-size:15px;"
    c = c + "color:" + T1 + "}"
    c = c + ".gs{font-size:12px;color:" + T2 + "}"
    c = c + ".ad{border:2px solid #f59e0b;border-"
    c = c + "radius:12px;padding:12px;margin:10px 0;"
    c = c + "background:rgba(245,158,11,.06)}"
    c = c + ".at{background:#f59e0b;color:#fff;"
    c = c + "padding:2px 8px;border-radius:8px;"
    c = c + "font-size:10px;font-weight:700}"
    c = c + ".fbc{height:110px;border-radius:0 0 14px"
    c = c + " 14px;background:linear-gradient(135deg,"
    c = c + "#00B074,#056839);margin:0 -10px}"
    c = c + "div[data-testid=stButton]>button{"
    c = c + "background:#00B074 !important;color:#fff"
    c = c + " !important;font-weight:600 !important;"
    c = c + "border:none !important;border-radius:12px"
    c = c + " !important}"
    c = c + "</style>"
    return c


# ================= SPLASH =================
if SS.page == "splash":
    st.markdown(css(False), unsafe_allow_html=True)
    st.markdown(
        "<div style='display:flex;flex-direction:"
        "column;align-items:center;justify-content:"
        "center;height:60vh;text-align:center;'>"
        "<h1 style='font-size:90px;font-weight:900;"
        "color:#1f2937;letter-spacing:4px;margin:0;'>"
        "HMF</h1><p style='font-size:24px;color:"
        "#4b5563;'>HMF Book</p></div>",
        unsafe_allow_html=True)
    if st.button("Get Started", use_container_width=True):
        SS.page = "auth"
        rr()


# ================= AUTH =================
elif SS.page == "auth":

    sup = SS.auth_mode == "signup"
    if sup:
        ttl = "Create Account"
        btn = "Sign Up"
    else:
        ttl = "Welcome Back"
        btn = "Login"

    st.markdown(css(False), unsafe_allow_html=True)
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
    if sup:
        em = st.text_input("Email")
    pw = st.text_input("Password", type="password")

    if st.button(btn, use_container_width=True):
        u = un.strip().lower()
        db = load_db()
        if not u or not pw:
            st.error("Dono fields bharin!")
        elif u in db["banned"]:
            st.error("BANNED account!")
        elif sup:
            if u in db["users"]:
                st.error("Username taken!")
            else:
                own = not db.get("owner")
                if own:
                    db["owner"] = u
                db["users"][u] = {
                    "email": em, "password": hash_pw(pw),
                    "display_name": u.title(), "bio": "Hi!",
                    "coins": 100, "blocked": [],
                    "avatar": None, "fails": 0,
                    "app_lock": False, "app_pin": "",
                    "finger_lock": False, "two_fa": False,
                    "login_alerts": True,
                    "auto_logout": 0,
                    "comment_filter": True,
                    "notif": {}}
                save_db(db)
                SS.logged_in = True
                SS.username = u
                SS.page = "app"
                if own:
                    st.balloons()
                rr()
        else:
            rec = db["users"].get(u)
            if rec and rec.get("lock_until", 0) > \
                    time.time():
                st.error("Locked! Wait 60s")
            elif rec and pw_ok(rec.get("password", ""),
                               pw):
                rec["fails"] = 0
                save_db(db)
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
                st.error("Wrong password!")
            else:
                st.error("Invalid username!")

    if st.button("Switch to " +
                 ("Login" if sup else "Sign Up")):
        SS.auth_mode = "login" if sup else "signup"
        rr()
    st.caption("Demo: demo/1234 • hoor/1234")


# ================= MAIN =================
elif SS.page == "app" and SS.logged_in:

    db = load_db()
    me = db["users"].get(SS.username, {})
    is_owner = SS.username == db.get("owner", "")

    st.markdown(css(SS.dark), unsafe_allow_html=True)

    al = me.get("auto_logout", 0)
    if al > 0 and SS.last_active > 0:
        if time.time() - SS.last_active > al * 60:
            SS.logged_in = False
            SS.page = "auth"
            rr()
    SS.last_active = time.time()

    # ---- LOCK SCREENS ----
    if me.get("app_lock") and not SS.pin_ok:
        st.markdown(
            "<div style='text-align:center;padding:"
            "25vh 0;'><div style='font-size:70px;'>"
            "🔒</div><h2>App Locked</h2></div>",
            unsafe_allow_html=True)
        if SS.pin_lock > time.time():
            st.error("Locked! Wait...")
        else:
            pi = st.text_input("PIN", type="password",
                               max_chars=4)
            if st.button("Unlock",
                         use_container_width=True):
                if pi == me.get("app_pin"):
                    SS.pin_ok = True
                    rr()
                else:
                    SS.pin_att = SS.pin_att + 1
                    if SS.pin_att >= 3:
                        SS.pin_lock = time.time() + 30
                        SS.pin_att = 0
                    st.error("Wrong PIN!")

    elif me.get("finger_lock") and not SS.fin_ok:
        st.markdown(
            "<div style='text-align:center;padding:"
            "25vh 0;'><div style='font-size:70px;'>"
            "👆</div><h2>Fingerprint Lock</h2></div>",
            unsafe_allow_html=True)
        if st.button("Scan", use_container_width=True):
            time.sleep(1.2)
            SS.fin_ok = True
            rr()
        if st.button("Logout", use_container_width=True):
            SS.logged_in = False
            SS.page = "auth"
            rr()

    else:
        # ---- TOPBAR ----
        unread = unread_count(SS.username)
        st.markdown("<div class='tb'><div class='lg'>"
                    "HMF Book</div></div>",
                    unsafe_allow_html=True)
        tq = st.columns(6)
        if tq[0].button("✉️", key="tbm",
                        use_container_width=True):
            go("Messages")
        if tq[1].button("🔔" + str(unread) if unread
                        else "🔔", key="tbn",
                        use_container_width=True):
            go("Notifications")
        if tq[2].button("🌙" if not SS.dark else "☀️",
                        key="tbd",
                        use_container_width=True):
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

        # ---- NAV ----
        nv = st.columns(8)
        navitems = [("Home", "🏠"), ("Search", "🔍"),
                    ("Reels", "🎬"), ("Market", "🛒"),
                    ("Messages", "✉️"), ("Create", "➕"),
                    ("Friends", "👥"), ("Profile", "👤")]
        for i, (t, ic) in enumerate(navitems):
            mark = ic
            if SS.tab == t:
                mark = "🔹"
            if nv[i].button(mark, key="nv_" + t,
                            use_container_width=True):
                go(t)
        st.markdown("<div style='height:6px;'></div>",
                    unsafe_allow_html=True)

        # ---- VIEW USER ----
        if SS.view_user and SS.view_user != SS.username:
            vu = SS.view_user
            if vu not in db["users"]:
                SS.view_user = None
                rr()
            ud = db["users"][vu]
            mp = []
            for p in db["posts"]:
                if p["user"] == vu:
                    mp.append(p)
            fr = db["friends"].get(vu, [])
            st.markdown("<div class='fbc'></div>",
                        unsafe_allow_html=True)
            st.markdown(
                "<div style='text-align:center;margin-"
                "top:-50px;'>" +
                av(vu, ud.get("avatar"), 100,
                   border=True) + "</div>",
                unsafe_allow_html=True)
            st.markdown(
                "<h3 style='text-align:center;margin:8px"
                " 0 2px;'>" +
                esc(ud.get("display_name", vu)) +
                "</h3><p style='text-align:center;color:"
                "#6b7280;font-size:13px;'>" +
                str(len(fr)) + " friends · " +
                str(len(mp)) + " posts</p>",
                unsafe_allow_html=True)
            v1, v2, v3 = st.columns(3)
            if v1.button("➕ Add", key="vfa"):
                db = load_db()
                db["friend_requests"].append(
                    {"from": SS.username, "to": vu,
                     "time": time.time()})
                save_db(db)
                notify(vu, "@" + SS.username +
                       " requested!", "follows")
                rr()
            if v2.button("✉️", key="vfm"):
                SS.msg_view = "chat"
                SS.msg_target = vu
                SS.msg_ttype = "direct"
                SS.view_user = None
                go("Messages")
            if v3.button("📞", key="vfc"):
                toast("Call sent!")
            if st.button("← Back", key="vbk"):
                SS.view_user = None
                rr()

        else:
            if SS.view_user == SS.username:
                SS.view_user = None
                SS.tab = "Profile"

            # ============ HOME ============
            if SS.tab == "Home":

                if me.get("show_stories", True):
                    st.markdown(
                        "<div class='st2'>"
                        "<div class='sc'><div class='rg"
                        " rgg'><div class='rm'>+</div>"
                        "</div><div class='sn'>Story</div>"
                        "</div>"
                        "<div class='sc'><div class='rg'>"
                        "<div class='rm'>HJ</div></div>"
                        "<div class='sn'>hoor</div></div>"
                        "<div class='sc'><div class='rg'>"
                        "<div class='rm'>FM</div></div>"
                        "<div class='sn'>farrukh</div>"
                        "</div></div>",
                        unsafe_allow_html=True)

                q1, q2, q3, q4 = st.columns(4)
                if q1.button("👥 Groups", key="hq1",
                             use_container_width=True):
                    go("Groups")
                if q2.button("📄 Pages", key="hq2",
                             use_container_width=True):
                    go("Pages")
                if q3.button("📅 Events", key="hq3",
                             use_container_width=True):
                    go("Events")
                if q4.button("🎲 Games", key="hq4",
                             use_container_width=True):
                    go("Games")

                vis = []
                for p in db["posts"]:
                    if p.get("type") == "reel":
                        continue
                    if p["user"] in SS.blocked:
                        continue
                    vis.append(p)

                ads = []
                for a in db["ads"]:
                    if a.get("status") == "active":
                        ads.append(a)

                if SS.clear_c:
                    SS[SS.clear_c] = ""
                    SS.clear_c = ""

                for idx, p in enumerate(vis):

                    st.markdown(
                        "<div class='pc'><div class='ph2'>"
                        + av(p["user"], p.get("avatar")) +
                        "<div class='pu'>" + esc(p["user"]) +
                        "</div></div></div>",
                        unsafe_allow_html=True)
                    pt = p.get("type", "text")
                    if pt == "text":
                        gr = p.get("grad", "#f0f0f0")
                        tx = esc(p.get("txt", ""))
                        st.markdown(
                            "<div class='pph' style="
                            "'background:" + gr + ";color:"
                            "#056839;font-weight:bold;'>"
                            + tx + "</div>",
                            unsafe_allow_html=True)
                    elif pt == "youtube":
                        yt = ("<iframe width='100%' "
                              "height='225' src='https://"
                              "www.youtube.com/embed/")
                        yt = yt + p["ref"]
                        yt = yt + ("' frameborder='0' "
                                   "allowfullscreen></iframe>")
                        components.html(yt, height=235)
                    elif pt == "image" and isfile(p["ref"]):
                        st.image(p["ref"],
                                 use_container_width=True)
                    elif pt == "video":
                        st.video(p["ref"])

                    liked = SS.username in p.get("likes", {})
                    c1, c2, c3, c4 = st.columns(4)
                    if liked:
                        ic = "❤️"
                    else:
                        ic = "🤍"
                    if c1.button(ic, key="lk_" + p["id"],
                                 use_container_width=True):
                        db = load_db()
                        for po in db["posts"]:
                            if po["id"] == p["id"]:
                                lk = po.setdefault(
                                    "likes", {})
                                if SS.username in lk:
                                    del lk[SS.username]
                                else:
                                    lk[SS.username] = True
                                break
                        save_db(db)
                        rr()
                    if c2.button("💬", key="cm_" + p["id"],
                                 use_container_width=True):
                        st.info("Box neeche.")
                    if c3.button("👤", key="vu_" + p["id"],
                                 use_container_width=True):
                        SS.view_user = p["user"]
                        rr()
                    if c4.button("🚫", key="bl_" + p["id"],
                                 use_container_width=True):
                        db = load_db()
                        rec = db["users"].get(SS.username)
                        if rec is not None:
                            bl = rec.setdefault(
                                "blocked", [])
                            if p["user"] not in bl:
                                bl.append(p["user"])
                            save_db(db)
                            SS.blocked = list(bl)
                        rr()

                    nl = str(len(p.get("likes", {})))
                    st.markdown("<p class='lk'>" + nl +
                                " likes</p><p class="
                                "'pd'><b>" + esc(p["user"]) +
                                "</b> " + esc(p.get("cap",
                                                    "")) +
                                "</p>",
                                unsafe_allow_html=True)

                    cm = st.text_input("comment",
                                       key="c_" + p["id"],
                                       placeholder=
                                       "Comment...",
                                       label_visibility=
                                       "collapsed")
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
                                            {"user":
                                             SS.username,
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
                            esc(ad["title"]) + "</b><br>" +
                            esc(ad.get("text", "")) +
                            "</div>", unsafe_allow_html=True)

            # ============ REELS ============
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
                    else:
                        if st.button("← Back", key="rbk"):
                            SS.open_reel = ""
                            rr()
                        st.markdown(
                            "<div class='ph2'>" +
                            av(rp["user"],
                               rp.get("avatar")) +
                            "<div class='pu'>@" +
                            esc(rp["user"]) + "</div>"
                            "</div>",
                            unsafe_allow_html=True)
                        st.video(rp["ref"])
                        liked = SS.username in \
                            rp.get("likes", {})
                        l1, l2, l3 = st.columns(3)
                        if liked:
                            ic = "❤️"
                        else:
                            ic = "🤍"
                        nl = str(len(rp.get("likes", {})))
                        if l1.button(ic + " " + nl,
                                     key="rlk"):
                            db = load_db()
                            for po in db["posts"]:
                                if po["id"] == rp["id"]:
                                    lk = po.setdefault(
                                        "likes", {})
                                    if SS.username in lk:
                                        del lk[SS.username]
                                    else:
                                        lk[SS.username] \
                                            = True
                                    break
                            save_db(db)
                            rr()
                        if l2.button("👤", key="rlu"):
                            SS.view_user = rp["user"]
                            rr()
                        if l3.button("✈️", key="rls"):
                            toast("Copied!")
                        st.markdown("<p class='pd'><b>@" +
                                    esc(rp["user"]) +
                                    "</b> " +
                                    esc(rp.get("cap", "")) +
                                    "</p>",
                                    unsafe_allow_html=True)
                        rc = st.text_input(
                            "comment",
                            key="r_" + rp["id"],
                            placeholder="Comment...")
                        if st.button("Post",
                                     key="rp_" + rp["id"]):
                            if rc.strip():
                                db = load_db()
                                for po in db["posts"]:
                                    if po["id"] == \
                                            rp["id"]:
                                        po.setdefault(
                                            "comments",
                                            []).append(
                                            {"user":
                                             SS.username,
                                             "text": rc})
                                        break
                                save_db(db)
                                SS.clear_c = "r_" + \
                                    rp["id"]
                                rr()
                        for c in rp.get("comments", []):
                            st.markdown(
                                "<p class='pd' style="
                                "'color:#6b7280;'><b>" +
                                esc(c["user"]) + "</b> " +
                                esc(c["text"]) + "</p>",
                                unsafe_allow_html=True)
                else:
                    st.markdown("<div class='ph'>🎬 Reels"
                                "</div>",
                                unsafe_allow_html=True)
                    rl = []
                    for p in db["posts"]:
                        if p.get("type") in ("reel",
                                             "video"):
                            rl.append(p)
                    if not rl:
                        st.info("No reels - upload video!")
                    g1, g2 = st.columns(2)
                    for i, r in enumerate(reversed(rl)):
                        col = g1
                        if i % 2 == 1:
                            col = g2
                        with col:
                            cap = r.get("cap", "Reel")[:15]
                            if st.button("▶ " + cap,
                                         key="rop_" +
                                         r["id"],
                                         use_container_width
                                         =True):
                                SS.open_reel = r["id"]
                                rr()
                            nl = str(len(r.get("likes", {})))
                            st.markdown(
                                "<p class='pv'>❤️ " + nl +
                                " · @" + esc(r["user"]) +
                                "</p>", unsafe_allow_html=True)

            # ============ SEARCH ============
            elif SS.tab == "Search":
                st.markdown("<div class='ph'>🔍 Search"
                            "</div>",
                            unsafe_allow_html=True)
                q = st.text_input(
                    "Users, posts, reels...",
                    key="sq")
                if q.strip():
                    ql = q.strip().lower()
                    res = []
                    for u in db["users"]:
                        if ql in u.lower():
                            res.append(u)
                    if res:
                        st.markdown("<p class='sl'>👥 Users"
                                    "</p>",
                                    unsafe_allow_html=True)
                        for u in res:
                            ud = db["users"][u]
                            r1, r2 = st.columns(
                                [0.7, 0.3])
                            r1.markdown(
                                "<div class='fr'>" +
                                av(u, ud.get("avatar"),
                                   40) +
                                "<div><b>@" + u + "</b>"
                                "</div></div>",
                                unsafe_allow_html=True)
                            if r2.button("Open",
                                         key="so_" + u,
                                         use_container_width
                                         =True):
                                SS.view_user = u
                                rr()
                    pres = []
                    for p in db["posts"]:
                        cp = p.get("cap", "") or ""
                        if ql in cp.lower():
                            pres.append(p)
                    if pres:
                        st.markdown("<p class='sl'>📱 Posts"
                                    "</p>",
                                    unsafe_allow_html=True)
                        for p in pres:
                            cap = p.get("cap", "Post")[:20]
                            if st.button("▶ " + cap,
                                         key="spo_" +
                                         p["id"],
                                         use_container_width
                                         =True):
                                if p.get("type") in \
                                        ("reel", "video"):
                                    SS.open_reel = p["id"]
                                    SS.tab = "Reels"
                                else:
                                    SS.tab = "Home"
                                rr()
                    lres = []
                    for l in db["listings"]:
                        if ql in l["title"].lower():
                            lres.append(l)
                    if lres:
                        st.markdown("<p class='sl'>🛒 "
                                    "Listings</p>",
                                    unsafe_allow_html=True)
                        for l in lres:
                            btn_t = "PKR " + str(l["price"])
                            btn_t = btn_t + " - "
                            btn_t = btn_t + l["title"][:20]
                            if st.button(btn_t,
                                         key="slo_" +
                                         l["id"],
                                         use_container_width
                                         =True):
                                SS.open_list = l["id"]
                                SS.tab = "Market"
                                rr()
                    if not res and not pres and not lres:
                        st.info("Kuch nahi mila!")
                else:
                    st.caption("Kuch bhi likhein...")

            # ============ FRIENDS ============
            elif SS.tab == "Friends":
                st.markdown("<div class='ph'>👥 Friends"
                            "</div>",
                            unsafe_allow_html=True)
                db = load_db()
                inr = []
                for r in db["friend_requests"]:
                    if r["to"] == SS.username:
                        inr.append(r)
                frs = db["friends"].get(SS.username, [])
                if inr:
                    st.markdown("### 📨 Requests")
                    for i, r in enumerate(inr):
                        f = r["from"]
                        r1, r2, r3 = st.columns(3)
                        r1.markdown(
                            "<div class='fr'>" +
                            av(f, None, 40) +
                            "<b>@" + f + "</b></div>",
                            unsafe_allow_html=True)
                        if r2.button("✅",
                                     key="fa_" + str(i)):
                            db = load_db()
                            db["friend_requests"] = [
                                x for x in db[
                                    "friend_requests"]
                                if not (x["from"] == f
                                        and x["to"] ==
                                        SS.username)]
                            fa = db["friends"].setdefault(
                                SS.username, [])
                            fb = db["friends"].setdefault(
                                f, [])
                            if f not in fa:
                                fa.append(f)
                            if SS.username not in fb:
                                fb.append(SS.username)
                            save_db(db)
                            notify(f, "Accepted!",
                                   "follows")
                            rr()
                        if r3.button("❌",
                                     key="fr_" + str(i)):
                            db = load_db()
                            db["friend_requests"] = [
                                x for x in db[
                                    "friend_requests"]
                                if not (x["from"] == f
                                        and x["to"] ==
                                        SS.username)]
                            save_db(db)
                            rr()
                st.markdown("### Friends (" + str(len(frs))
                            + ")")
                for f in frs:
                    r1, r2, r3 = st.columns(3)
                    r1.markdown(
                        "<div class='fr'>" + av(f, None,
                                               40) +
                        "<b>@" + f + "</b></div>",
                        unsafe_allow_html=True)
                    if r2.button("✉️", key="fm_" + f):
                        SS.msg_view = "chat"
                        SS.msg_target = f
                        SS.msg_ttype = "direct"
                        go("Messages")
                    if r3.button("👤", key="fu_" + f):
                        SS.view_user = f
                        rr()
                st.markdown("### 🌟 Suggestions")
                for u in db["users"]:
                    if u == SS.username or u in frs:
                        continue
                    skip = False
                    for x in db["friend_requests"]:
                        if x["from"] == SS.username and \
                                x["to"] == u:
                            skip = True
                    if skip:
                        continue
                    r1, r2 = st.columns(2)
                    r1.markdown(
                        "<div class='fr'>" + av(u, None,
                                               40) +
                        "<b>@" + u + "</b></div>",
                        unsafe_allow_html=True)
                    if r2.button("➕", key="sg_" + u):
                        db = load_db()
                        db["friend_requests"].append(
                            {"from": SS.username, "to": u,
                             "time": time.time()})
                        save_db(db)
                        notify(u, "Request!", "follows")
                        rr()

            # ============ GROUPS ============
            elif SS.tab == "Groups":
                if SS.open_group:
                    g = None
                    for x in db["groups"]:
                        if x["id"] == SS.open_group:
                            g = x
                            break
                    if g is None:
                        SS.open_group = ""
                        rr()
                    if st.button("← Back", key="gbk"):
                        SS.open_group = ""
                        rr()
                    nm = esc(g["name"])
                    mc = str(len(g["members"]))
                    st.markdown(
                        "<div class='gc'><div class="
                        "'gv'></div><div class='gn'>👥 "
                        + nm + "</div><div class='gs'>" +
                        mc + " members</div></div>",
                        unsafe_allow_html=True)
                    ism = SS.username in g["members"]
                    if st.button("Leave" if ism
                                 else "Join",
                                 key="gjn",
                                 use_container_width=True):
                        db = load_db()
                        for x in db["groups"]:
                            if x["id"] == g["id"]:
                                if ism:
                                    x["members"].remove(
                                        SS.username)
                                else:
                                    x["members"].append(
                                        SS.username)
                                break
                        save_db(db)
                        rr()
                    gt = st.text_input("Post...", key="gpt")
                    if st.button("Post", key="gpb",
                                 use_container_width=True):
                        if gt.strip() and ism:
                            db = load_db()
                            db["posts"].insert(0, {
                                "id": uuid.uuid4()
                                .hex[:8],
                                "user": SS.username,
                                "type": "text",
                                "grad": random.choice(
                                    GRADS),
                                "txt": esc(gt)[:40],
                                "cap": gt,
                                "groupId": g["id"],
                                "likes": {},
                                "comments": []})
                            save_db(db)
                            rr()
                    for p in db["posts"]:
                        if p.get("groupId") == g["id"]:
                            st.markdown(
                                "<div class='gc'><b>@"
                                + esc(p["user"]) +
                                "</b><br>" +
                                esc(p.get("cap", "")) +
                                "</div>",
                                unsafe_allow_html=True)
                else:
                    st.markdown("<div class='ph'>👥 Groups"
                                "</div>",
                                unsafe_allow_html=True)
                    with st.expander("➕ Create"):
                        gn = st.text_input("Name", key="gn")
                        if st.button("Create", key="gcr",
                                     use_container_width
                                     =True):
                            if gn.strip():
                                db = load_db()
                                db["groups"].append({
                                    "id": uuid.uuid4()
                                    .hex[:8],
                                    "name": gn.strip(),
                                    "members":
                                    [SS.username],
                                    "messages": []})
                                save_db(db)
                                rr()
                    for g in db["groups"]:
                        mc = str(len(g["members"]))
                        st.markdown(
                            "<div class='gc'><div class="
                            "'gv'></div><div class='gn'>"
                            + esc(g["name"]) +
                            "</div><div class='gs'>" + mc
                            + " members</div></div>",
                            unsafe_allow_html=True)
                        if st.button("Open",
                                     key="go_" + g["id"],
                                     use_container_width
                                     =True):
                            SS.open_group = g["id"]
                            rr()

            # ============ PAGES ============
            elif SS.tab == "Pages":
                if SS.open_page:
                    pg = None
                    for x in db["pages"]:
                        if x["id"] == SS.open_page:
                            pg = x
                            break
                    if pg is None:
                        SS.open_page = ""
                        rr()
                    if st.button("← Back", key="pbk"):
                        SS.open_page = ""
                        rr()
                    st.markdown(
                        "<h3 style='text-align:center;'>📄 "
                        + esc(pg["name"]) + "</h3>",
                        unsafe_allow_html=True)
                    if pg["owner"] == SS.username:
                        pt2 = st.text_input("Post as page",
                                            key="ppt")
                        if st.button("Post", key="ppb",
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
                                    "cap": pt2,
                                    "likes": {},
                                    "comments": []})
                                save_db(db)
                                rr()
                    for p in db["posts"]:
                        if p.get("pageId") == pg["id"]:
                            st.markdown(
                                "<div class='gc'><b>📄 "
                                + esc(p["user"]) +
                                "</b><br>" +
                                esc(p.get("cap", "")) +
                                "</div>",
                                unsafe_allow_html=True)
                else:
                    st.markdown("<div class='ph'>📄 Pages"
                                "</div>",
                                unsafe_allow_html=True)
                    with st.expander("➕ Create"):
                        pn = st.text_input("Name", key="pn")
                        if st.button("Create", key="pcr",
                                     use_container_width
                                     =True):
                            if pn.strip():
                                db = load_db()
                                db["pages"].append({
                                    "id": uuid.uuid4()
                                    .hex[:8],
                                    "name": pn.strip(),
                                    "owner": SS.username,
                                    "followers": []})
                                save_db(db)
                                rr()
                    for pg in db["pages"]:
                        st.markdown(
                            "<div class='gc'><div class="
                            "'gn'>📄 " + esc(pg["name"]) +
                            "</div></div>",
                            unsafe_allow_html=True)
                        if st.button("Open",
                                     key="po_" + pg["id"],
                                     use_container_width
                                     =True):
                            SS.open_page = pg["id"]
                            rr()

            # ============ EVENTS ============
            elif SS.tab == "Events":
                if SS.open_event:
                    ev = None
                    for x in db["events"]:
                        if x["id"] == SS.open_event:
                            ev = x
                            break
                    if ev is None:
                        SS.open_event = ""
                        rr()
                    if st.button("← Back", key="ebk"):
                        SS.open_event = ""
                        rr()
                    loc = esc(ev.get("location", ""))
                    st.markdown(
                        "<div class='gc'><div class="
                        "'gv'></div><div class='gn'>📅 "
                        + esc(ev["title"]) +
                        "</div><div class='gs'>📍 " + loc
                        + "</div></div>",
                        unsafe_allow_html=True)
                    e1, e2 = st.columns(2)
                    if e1.button("✅ Going", key="eg"):
                        db = load_db()
                        for x in db["events"]:
                            if x["id"] == ev["id"]:
                                x["rsvps"] = [
                                    r for r in x.get(
                                        "rsvps", [])
                                    if r["user"] !=
                                    SS.username]
                                x["rsvps"].append(
                                    {"user": SS.username,
                                     "status": "going"})
                        save_db(db)
                        rr()
                    if e2.button("🌟 Maybe", key="em"):
                        db = load_db()
                        for x in db["events"]:
                            if x["id"] == ev["id"]:
                                x["rsvps"] = [
                                    r for r in x.get(
                                        "rsvps", [])
                                    if r["user"] !=
                                    SS.username]
                                x["rsvps"].append(
                                    {"user": SS.username,
                                     "status":
                                     "interested"})
                        save_db(db)
                        rr()
                else:
                    st.markdown("<div class='ph'>📅 Events"
                                "</div>",
                                unsafe_allow_html=True)
                    with st.expander("➕ Create"):
                        et = st.text_input("Title", key="et")
                        el = st.text_input("Location",
                                           key="el")
                        if st.button("Create", key="ecr",
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
                                    "rsvps": []})
                                save_db(db)
                                rr()
                    for ev in db["events"]:
                        loc = esc(ev.get("location", ""))
                        st.markdown(
                            "<div class='gc'><div class="
                            "'gn'>📅 " + esc(ev["title"]) +
                            "</div><div class='gs'>📍 "
                            + loc + "</div></div>",
                            unsafe_allow_html=True)
                        if st.button("Open",
                                     key="eo_" + ev["id"],
                                     use_container_width
                                     =True):
                            SS.open_event = ev["id"]
                            rr()

            # ============ MARKET ============
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
                                "</div>",
                                unsafe_allow_html=True)
                    if ls.get("image") and \
                            isfile(ls["image"]):
                        st.image(ls["image"],
                                 use_container_width=True)
                    pr = str(ls["price"])
                    st.markdown("<h2 style='color:#00B074;"
                                "'>PKR " + pr + "</h2>",
                                unsafe_allow_html=True)
                    st.write(ls.get("description", ""))
                    st.caption("@" + ls["seller"] + " · " +
                               ls["status"])
                    if ls["seller"] != SS.username:
                        if st.button("✉️ Message Seller",
                                     key="msl",
                                     use_container_width
                                     =True):
                            smsg(False, "",
                                 ls["seller"],
                                 "Interested in '" +
                                 ls["title"] + "'")
                            SS.msg_view = "chat"
                            SS.msg_target = ls["seller"]
                            SS.msg_ttype = "direct"
                            SS.open_list = ""
                            go("Messages")
                    else:
                        if st.button("Mark Sold",
                                     key="msd",
                                     use_container_width
                                     =True):
                            db = load_db()
                            for x in db["listings"]:
                                if x["id"] == ls["id"]:
                                    x["status"] = "sold"
                                    break
                            save_db(db)
                            rr()
                else:
                    st.markdown("<div class='ph'>🛒 Market"
                                "</div>",
                                unsafe_allow_html=True)
                    with st.expander("➕ Sell"):
                        st_ = st.text_input("Title",
                                            key="st")
                        sd = st.text_area("Desc",
                                          key="sd",
                                          height=60)
                        sp = st.number_input("PKR",
                                             min_value=0,
                                             key="sp")
                        si = st.file_uploader(
                            "Photo", type=["png", "jpg",
                                           "jpeg"],
                            key="si")
                        if st.button("List", key="slb",
                                     use_container_width
                                     =True):
                            if st_.strip():
                                img = None
                                if si is not None:
                                    img = supload(si)
                                db = load_db()
                                db["listings"].insert(0, {
                                    "id": uuid.uuid4()
                                    .hex[:8],
                                    "seller": SS.username,
                                    "title": st_.strip(),
                                    "description": sd,
                                    "price": int(sp),
                                    "image": img,
                                    "status":
                                    "available"})
                                save_db(db)
                                rr()
                    for l in db["listings"]:
                        if l["status"] == "available":
                            stt = "✅"
                        else:
                            stt = "❌"
                        pr = str(l["price"])
                        st.markdown(
                            "<div class='gc'><div class="
                            "'gn'>" + stt + " " +
                            esc(l["title"]) +
                            "</div><div class='gs'>PKR "
                            + pr + " · @" +
                            esc(l["seller"]) +
                            "</div></div>",
                            unsafe_allow_html=True)
                        if st.button("Open",
                                     key="lo_" + l["id"],
                                     use_container_width
                                     =True):
                            SS.open_list = l["id"]
                            rr()

            # ============ ADS ============
            elif SS.tab == "Ads":
                st.markdown("<div class='ph'>📢 Ads"
                            "</div>",
                            unsafe_allow_html=True)
                with st.expander("➕ Create Ad"):
                    at = st.text_input("Title", key="at")
                    ax = st.text_area("Text", key="ax",
                                      height=60)
                    ab = st.number_input("Coins",
                                         min_value=10,
                                         value=50,
                                         key="ab")
                    if st.button("Submit", key="asb",
                                 use_container_width=True):
                        if at.strip():
                            db = load_db()
                            u = db["users"].get(
                                SS.username)
                            if u is not None and \
                                    u.get("coins",
                                          0) >= int(ab):
                                u["coins"] -= int(ab)
                                db["ads"].append({
                                    "id": uuid.uuid4()
                                    .hex[:8],
                                    "advertiser":
                                    SS.username,
                                    "title": at.strip(),
                                    "text": ax,
                                    "status": "pending"})
                                save_db(db)
                                st.success("Submitted!")
                                rr()
                            else:
                                st.warning("Coins kam!")
                        else:
                            st.warning("Title!")
                for a in db["ads"]:
                    if a["advertiser"] == SS.username or \
                            is_owner:
                        st.markdown(
                            "<div class='ad'><span class="
                            "'at'>" + a["status"].upper()
                            + "</span><br><b>" +
                            esc(a["title"]) + "</b></div>",
                            unsafe_allow_html=True)
                        if is_owner and \
                                a["status"] == "pending":
                            if st.button("Approve",
                                         key="aap_" +
                                         a["id"],
                                         use_container_width
                                         =True):
                                db = load_db()
                                for x in db["ads"]:
                                    if x["id"] == a["id"]:
                                        x["status"] = \
                                            "active"
                                        break
                                save_db(db)
                                rr()

            # ============ CHANNEL ============
            elif SS.tab == "Channel":
                st.markdown("<div class='ph'>📺 Channel"
                            "</div>",
                            unsafe_allow_html=True)
                with st.expander("➕ Add YouTube"):
                    yl = st.text_input("Link", key="yl")
                    if st.button("Add", key="yb",
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
                                "cap": "Video",
                                "likes": {},
                                "comments": []})
                            save_db(db)
                            rr()
                        else:
                            st.error("Invalid!")
                for p in db["posts"]:
                    if p.get("type") == "youtube":
                        yt = ("<iframe width='100%' "
                              "height='190' src='https://"
                              "www.youtube.com/embed/")
                        yt = yt + p["ref"]
                        yt = yt + ("' frameborder='0' "
                                   "allowfullscreen></iframe>")
                        components.html(yt, height=200)

            # ============ CREATE ============
            elif SS.tab == "Create":
                st.markdown("<div class='ph'>➕ Create"
                            "</div>",
                            unsafe_allow_html=True)
                kind = st.radio("Type:",
                                ["Photo", "Video",
                                 "Camera 🎨",
                                 "YouTube"],
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
                            st.warning("Photo lein!")
                        else:
                            db = load_db()
                            db["posts"].insert(0, {
                                "id": uuid.uuid4()
                                .hex[:8],
                                "user": SS.username,
                                "type": "image",
                                "ref": spil(fi),
                                "cap": cap,
                                "likes": {},
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
                                "id": uuid.uuid4()
                                .hex[:8],
                                "user": SS.username,
                                "type": "youtube",
                                "ref": vid,
                                "cap": cap,
                                "likes": {},
                                "comments": []})
                            save_db(db)
                            go("Home")
                        else:
                            st.error("Invalid link!")
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
                                "id": uuid.uuid4()
                                .hex[:8],
                                "user": SS.username,
                                "type": pt,
                                "ref": supload(f),
                                "cap": cap,
                                "likes": {},
                                "comments": []})
                            save_db(db)
                            go("Home")

            # ============ MESSAGES ============
            elif SS.tab == "Messages":

                if HAS_REFRESH:
                    st_autorefresh(interval=4000,
                                   key="mr")
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

                    hb, ha, hi, hc = st.columns(
                        [0.1, 0.15, 0.5, 0.25])
                    if hb.button("←", key="cbk"):
                        SS.msg_view = "list"
                        rr()
                    if isg and grp is not None:
                        ha.markdown(
                            av(grp["name"], None, 40),
                            unsafe_allow_html=True)
                        hi.markdown(
                            "<b>" + esc(grp["name"]) +
                            "</b>", unsafe_allow_html=True)
                        msgs = grp.get("messages", [])
                    elif tgt in db["users"]:
                        ud = db["users"][tgt]
                        seen(SS.username, tgt)
                        ha.markdown(
                            av(tgt, ud.get("avatar"), 40),
                            unsafe_allow_html=True)
                        dn = esc(ud.get("display_name",
                                        tgt))
                        hi.markdown("<b>" + dn + "</b>",
                                    unsafe_allow_html=True)
                        if hc.button("📞", key="ccl"):
                            toast("Call!")
                        msgs = []
                        for m in db["messages"]:
                            if (m["from"] == SS.username
                                    and m["to"] == tgt):
                                msgs.append(m)
                            elif (m["from"] == tgt
                                  and m["to"] ==
                                  SS.username):
                                msgs.append(m)

                    st.markdown(
                        "<div class='en'>🔒 encrypted"
                        " (demo)</div>",
                        unsafe_allow_html=True)

                    if SS.clear_m:
                        SS[SS.clear_m] = ""
                        SS.clear_m = ""

                    for m in sorted(msgs,
                                    key=lambda x:
                                    x["time"]):
                        mine = m["from"] == SS.username
                        ts = time.strftime(
                            "%I:%M %p",
                            time.localtime(
                                m["time"])).lower()
                        if m.get("photo") and \
                                isfile(m["photo"]):
                            st.image(m["photo"], width=180)
                        if mine:
                            cls = "bm"
                        else:
                            cls = "bh"
                        snd = ""
                        if isg and not mine:
                            snd = "<b>@" + esc(m["from"])
                            snd = snd + "</b><br>"
                        st.markdown(
                            "<span class='" + cls + "'>"
                            + snd + esc(m.get("text", ""))
                            + "<span class='bt'>" + ts +
                            "</span></span>",
                            unsafe_allow_html=True)
                        r = m.get("reactions", [])
                        mk = m.get("id",
                                   str(m["time"]))
                        if r:
                            lb = "👍 " + str(len(r))
                        else:
                            lb = "👍"
                        if st.button(lb, key="rx_" + mk):
                            tog_rx(isg, tgt,
                                   m.get("id"),
                                   SS.username)
                            rr()

                    with st.expander("📷 Photo"):
                        ph = st.file_uploader(
                            "Photo", type=["png", "jpg",
                                           "jpeg"],
                            key="cph")
                        if st.button("Send", key="csp",
                                     use_container_width
                                     =True):
                            if ph is None:
                                st.warning("Choose!")
                            else:
                                smsg(isg, tgt, tgt,
                                     "📷 Photo",
                                     photo=supload(ph))
                                rr()

                    if hasattr(st, "audio_input"):
                        au = st.audio_input("🎙️",
                                            key="cvc")
                        if au is not None:
                            st.audio(au)
                            if st.button("Send Voice",
                                         key="csv",
                                         use_container_width
                                         =True):
                                smsg(isg, tgt, tgt,
                                     "🎤 Voice")
                                rr()

                    tx = st.text_input("Message...",
                                       key="ctx")
                    if st.button("Send", key="csd",
                                 use_container_width=True):
                        if tx.strip():
                            smsg(isg, tgt, tgt,
                                 tx.strip())
                            SS.clear_m = "ctx"
                            rr()

                else:
                    st.markdown("<div class='ph'>✉️ Chats"
                                "</div>",
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
                        if p == SS.username:
                            continue
                        if p in SS.blocked:
                            continue
                        cn = []
                        for m in db["messages"]:
                            if (m["from"] == SS.username
                                    and m["to"] == p):
                                cn.append(m)
                            elif (m["from"] == p
                                  and m["to"] ==
                                  SS.username):
                                cn.append(m)
                        if cn:
                            last = cn[-1]
                        else:
                            last = None
                        convs.append({"u": p, "last": last,
                                      "un": unseen(
                                          SS.username,
                                          p)})
                    for g in db["groups"]:
                        if SS.username in g["members"]:
                            gms = g.get("messages", [])
                            if gms:
                                last = gms[-1]
                            else:
                                last = None
                            convs.append({"g": g,
                                          "last": last})
                    convs.sort(
                        key=lambda c: (
                            c["last"]["time"]
                            if c["last"] else 0),
                        reverse=True)
                    if not convs:
                        st.info("No chats!")
                    for c in convs:
                        isg2 = False
                        if "u" in c:
                            p = c["u"]
                            ud = db["users"].get(p, {})
                            nm = esc(ud.get(
                                "display_name", p))
                            avh = av(p,
                                     ud.get("avatar"),
                                     46)
                            kid = p
                            if c["last"]:
                                if c["last"]["from"] == \
                                        SS.username:
                                    pre = "You: "
                                else:
                                    pre = ""
                                pv = pre + esc(
                                    c["last"].get(
                                        "text", ""))[:28]
                            else:
                                pv = "Say hello 👋"
                            bd = ""
                            if c["un"] > 0:
                                bd = ("<span class="
                                      "'ub'>" +
                                      str(c["un"]) +
                                      "</span>")
                        else:
                            g = c["g"]
                            nm = "👥 " + esc(g["name"])
                            avh = av(g["name"], None, 46)
                            kid = g["id"]
                            isg2 = True
                            pv = "Group chat"
                            bd = ""
                        st.markdown(
                            "<div class='ci'><div class="
                            "'aw'>" + avh + "</div><div "
                            "class='cn'><div class='nm'>"
                            + nm + "</div><div class="
                            "'pv'>" + pv + "</div></div>"
                            + bd + "</div>",
                            unsafe_allow_html=True)
                        if st.button("💬", key="op_" + kid,
                                     use_container_width
                                     =True):
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
                        pick = st.selectbox("Chat:",
                                            others,
                                            key="ncs")
                        if st.button("Start", key="ncb",
                                     use_container_width
                                     =True):
                            SS.msg_view = "chat"
                            SS.msg_target = pick
                            SS.msg_ttype = "direct"
                            rr()
                        gn = st.text_input("Group name",
                                           key="gn2")
                        gm = st.multiselect("Members",
                                            others,
                                            key="gm2")
                        if st.button("Create Group",
                                     key="gcb",
                                     use_container_width
                                     =True):
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

            # ============ NOTIFICATIONS ============
            elif SS.tab == "Notifications":
                st.markdown("<div class='ph'>🔔 Notifs"
                            "</div>",
                            unsafe_allow_html=True)
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

            # ============ GAMES ============
            elif SS.tab == "Games":
                st.markdown("<div class='ph'>🎲 Games"
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
                    rr()
                if SS.dice:
                    extra = ""
                    if SS.dice == 6:
                        extra = " (+5!)"
                    st.markdown(
                        "<h2 style='text-align:center;"
                        "color:#00B074;'>🎯 " +
                        str(SS.dice) + extra + "</h2>",
                        unsafe_allow_html=True)

            # ============ PROFILE ============
            elif SS.tab == "Profile":
                me = db["users"].get(SS.username, {})
                mp = []
                for p in db["posts"]:
                    if p["user"] == SS.username:
                        mp.append(p)
                fr = db["friends"].get(SS.username, [])
                st.markdown("<div class='fbc'></div>",
                            unsafe_allow_html=True)
                st.markdown(
                    "<div style='text-align:center;"
                    "margin-top:-50px;'>" +
                    av(SS.username, me.get("avatar"), 100,
                       border=True) + "</div>",
                    unsafe_allow_html=True)
                nm = esc(me.get("display_name",
                                SS.username))
                co = str(me.get("coins", 0))
                st.markdown(
                    "<h3 style='text-align:center;margin:"
                    "8px 0 2px;'>" + nm +
                    "</h3><p style='text-align:center;"
                    "color:#6b7280;font-size:13px;'>" +
                    str(len(fr)) + " friends · " +
                    str(len(mp)) + " posts · 💰" + co +
                    "</p>", unsafe_allow_html=True)
                if is_owner:
                    st.markdown(
                        "<p style='text-align:center;'>"
                        "<span class='ob'>👑 OWNER"
                        "</span></p>",
                        unsafe_allow_html=True)
                b1, b2 = st.columns(2)
                if b1.button("✏️ Edit", key="pe"):
                    go("Settings")
                    SS.setpage = "personal"
                    rr()
                if b2.button("💰 Payout (100)", key="pp"):
                    db = load_db()
                    u = db["users"].get(SS.username)
                    if u is not None and \
                            u.get("coins", 0) >= 100:
                        u["coins"] -= 100
                        save_db(db)
                        st.success("Payout!")
                        rr()
                    else:
                        st.warning("Min 100 coins!")
                with st.expander("🖼️ Pic"):
                    fl = st.selectbox("Filter:", FILTERS,
                                      key="pf")
                    pi = st.file_uploader(
                        "Upload", type=["png", "jpg",
                                        "jpeg"],
                        key="pi")
                    if st.button("Update", key="pu",
                                 use_container_width=True):
                        if pi is None:
                            st.warning("Choose!")
                        else:
                            pil = Image.open(pi)
                            setp(SS.username, "avatar",
                                 spil(filt(pil, fl)))
                            st.success("Updated!")
                            rr()
                for p in mp[:6]:
                    if p.get("type") == "text":
                        gr = p.get("grad", "#f0f0f0")
                        tx = esc(p.get("txt", ""))
                        st.markdown(
                            "<div class='pph' style="
                            "'background:" + gr + ";"
                            "height:90px;'>" + tx +
                            "</div>",
                            unsafe_allow_html=True)
                    elif p.get("type") == "image" and \
                            isfile(p["ref"]):
                        st.image(p["ref"],
                                 use_container_width=True)

            # ============ SETTINGS ============
            elif SS.tab == "Settings":

                if SS.setpage == "menu":
                    st.markdown("<div class='ph'>⚙️ "
                                "Settings</div>",
                                unsafe_allow_html=True)
                    st.caption("@" + SS.username)
                    items = [
                        ("🔐 Security", "security"),
                        ("📋 Personal", "personal"),
                        ("📰 Feed", "feed"),
                        ("🚫 Blocked", "blocked"),
                        ("⚠️ Report", "reports"),
                        ("ℹ️ About", "about")]
                    for label, pg in items:
                        if st.button(label + " ›",
                                     key="m_" + pg,
                                     use_container_width
                                     =True):
                            SS.setpage = pg
                            rr()
                    if is_owner:
                        if st.button("🛡️ OWNER PANEL ›",
                                     key="mown",
                                     use_container_width
                                     =True):
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
                    st.markdown("<p class='sl'>🔢 App Lock"
                                "</p>",
                                unsafe_allow_html=True)
                    if not me.get("app_lock"):
                        npin = st.text_input(
                            "4-digit PIN",
                            type="password",
                            max_chars=4, key="spn")
                        if st.button("Enable", key="sae",
                                     use_container_width
                                     =True):
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
                        st.success("ON")
                        l1, l2 = st.columns(2)
                        if l1.button("Lock Now",
                                     key="sln",
                                     use_container_width
                                     =True):
                            SS.pin_ok = False
                            rr()
                        if l2.button("Disable",
                                     key="sdn",
                                     use_container_width
                                     =True):
                            setp(SS.username,
                                 "app_lock", False)
                            setp(SS.username,
                                 "app_pin", "")
                            rr()

                    st.markdown("<p class='sl'>👆 "
                                "Fingerprint</p>",
                                unsafe_allow_html=True)
                    cf = me.get("finger_lock", False)
                    nf = st.checkbox("Enable",
                                     value=cf,
                                     key="sfl")
                    if nf != cf:
                        setp(SS.username,
                             "finger_lock", nf)
                        if nf:
                            SS.fin_ok = False
                        else:
                            SS.fin_ok = True
                        rr()

                    st.markdown("<p class='sl'>⏱️ Auto "
                                "Logout</p>",
                                unsafe_allow_html=True)
                    opts = [0, 5, 10, 30]
                    cur = me.get("auto_logout", 0)
                    if cur in opts:
                        ci = opts.index(cur)
                    else:
                        ci = 0
                    nal = st.selectbox("Min:", opts,
                                       index=ci,
                                       key="sal")
                    if nal != cur:
                        setp(SS.username,
                             "auto_logout", nal)
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
                        setp(SS.username,
                             "display_name", dn)
                        setp(SS.username, "bio", bio)
                        st.success("Saved!")

                elif SS.setpage == "feed":
                    if st.button("← Back", key="bf"):
                        SS.setpage = "menu"
                        rr()
                    cs = st.checkbox(
                        "Show Stories",
                        value=me.get("show_stories",
                                     True),
                        key="nss")
                    if cs != me.get("show_stories",
                                    True):
                        setp(SS.username,
                             "show_stories", cs)
                        rr()
                    cc = st.checkbox(
                        "Word Filter",
                        value=me.get("comment_filter",
                                     True),
                        key="ncf")
                    if cc != me.get("comment_filter",
                                    True):
                        setp(SS.username,
                             "comment_filter", cc)
                        rr()

                elif SS.setpage == "blocked":
                    if st.button("← Back", key="bbl"):
                        SS.setpage = "menu"
                        rr()
                    bi = st.text_input("Username",
                                       key="bki")
                    if st.button("Block", key="bkb",
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
                            rr()
                    for i, u in enumerate(SS.blocked):
                        b1, b2 = st.columns(
                            [0.6, 0.4])
                        b1.markdown("🚫 @" + u)
                        if b2.button("Unblock",
                                     key="ubk_" +
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
                            rr()

                elif SS.setpage == "reports":
                    if st.button("← Back", key="brp"):
                        SS.setpage = "menu"
                        rr()
                    ri = st.text_input("User ID",
                                       key="rki")
                    if st.button("Report", key="rkb",
                                 use_container_width=True):
                        u = ri.strip().lower()
                        if u:
                            db = load_db()
                            db["reports"].append(
                                {"from": SS.username,
                                 "user": u,
                                 "reason": "report",
                                 "time":
                                 time.time()})
                            save_db(db)
                            st.success("Sent!")
                        else:
                            st.warning("ID!")

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
                        "**📅 Founded:** Feb 2026\n\n"
                        "© 2026 HMF Group")

                elif SS.setpage == "admin":
                    if st.button("← Back", key="bad"):
                        SS.setpage = "menu"
                        rr()
                    st.markdown("<div class='ph'>🛡️ "
                                "Owner</div>",
                                unsafe_allow_html=True)
                    db = load_db()
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Users",
                              len(db["users"]))
                    c2.metric("Posts",
                              len(db["posts"]))
                    c3.metric("Reports",
                              len(db["reports"]))
                    st.markdown("### 🚩 Reports")
                    for i, r in enumerate(
                            reversed(db["reports"]
                                     [:10])):
                        r1, r2 = st.columns(
                            [0.6, 0.4])
                        r1.markdown("🚩 @" +
                                    esc(r.get("user",
                                              "")))
                        if r.get("user") in \
                                db["banned"]:
                            if r2.button("Unban",
                                         key="ru_" +
                                         str(i),
                                         use_container_
                                         width=True):
                                db = load_db()
                                db["banned"].remove(
                                    r["user"])
                                save_db(db)
                                rr()
                        else:
                            if r2.button("BAN",
                                         key="rbn_" +
                                         str(i),
                                         use_container_
                                         width=True):
                                db = load_db()
                                db["banned"].append(
                                    r["user"])
                                save_db(db)
                                rr()


# ---------- SAFETY ----------
else:
    SS.page = "splash"
    rr()

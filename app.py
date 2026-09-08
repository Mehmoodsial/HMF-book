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
                           "status

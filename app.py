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
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

st.set_page_config(page_title="HMF Book", page_icon="🟢", layout="centered")

try:
    from streamlit_autorefresh import st_autorefresh
    HAS_R = True
except Exception:
    HAS_R = False

SALT = "hmf"
DBF = "hmf_db.json"
UPD = "uploads"
FL = ["None", "Beauty", "Sepia", "Cool", "Cartoon"]
GR = ["linear-gradient(45deg,#d1fae5,#a7f3d0)", "linear-gradient(45deg,#ecfdf5,#6ee7b7)"]
BW = ["stupid", "idiot", "hate", "ugly"]


def hp(p):
    return hashlib.sha256((SALT + p).encode()).hexdigest()


def pok(s, p):
    return s == hp(p) or s == p


def rr():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


def pyt(u):
    u = (u or "").strip()
    if len(u) == 11 and "/" not in u:
        return u
    for t in ("youtu.be/", "v=", "/shorts/"):
        if t in u:
            p = u.split(t)[1].split("?")[0].split("&")[0].split("/")[0]
            if p:
                return p
    return None


def ldb():
    try:
        with open(DBF, "r") as f:
            d = json.load(f)
    except Exception:
        d = {}
    if not isinstance(d.get("users"), dict):
        d["users"] = {}
    for k in ("msg", "posts", "notif", "rep", "ban", "freq", "stories", "hl"):
        if not isinstance(d.get(k), list):
            d[k] = []
    for k in ("fr", "cf", "seen"):
        if not isinstance(d.get(k), dict):
            d[k] = {}
    if "owner" not in d:
        d["owner"] = ""
    return d


def sdb(d):
    try:
        with open(DBF, "w") as f:
            json.dump(d, f, ensure_ascii=False)
    except Exception:
        pass


def sp(u, k, v):
    d = ldb()
    r = d["users"].get(u)
    if r is not None:
        r[k] = v
        sdb(d)


def nt(to, txt):
    if not to:
        return
    d = ldb()
    d["notif"].insert(0, {"to": to, "txt": txt, "t": time.time(), "r": False})
    d["notif"] = d["notif"][:200]
    sdb(d)


def unc(u):
    d = ldb()
    return sum(1 for x in d["notif"] if x.get("to") == u and not x.get("r"))


def cln(t):
    return not any(w in t.lower() for w in BW)


def sm(to, txt):
    me = st.session_state.username
    d = ldb()
    d["msg"].append({"id": uuid.uuid4().hex[:8], "f": me, "to": to, "txt": txt, "t": time.time(), "rx": []})
    sdb(d)
    nt(to, "@" + me + " sent a message")


def trx(mid, u):
    d = ldb()
    for m in d["msg"]:
        if m.get("id") == mid:
            rx = m.setdefault("rx", [])
            if u in rx:
                rx.remove(u)
            else:
                rx.append(u)
            break
    sdb(d)


def upl(f):
    os.makedirs(UPD, exist_ok=True)
    e = f.name.split(".")[-1].lower()
    if e not in ("png", "jpg", "jpeg", "mp4", "mov"):
        e = "bin"
    p = os.path.join(UPD, uuid.uuid4().hex + "." + e)
    with open(p, "wb") as o:
        o.write(f.getbuffer())
    return p


def spl(img):
    os.makedirs(UPD, exist_ok=True)
    p = os.path.join(UPD, uuid.uuid4().hex + ".png")
    img.save(p, "PNG")
    return p


def av(n, p=None, s=36):
    if p and os.path.exists(p):
        try:
            b = base64.b64encode(open(p, "rb").read()).decode()
            return "<img src='data:image/png;base64," + b + "' style='width:" + str(s) + "px;height:" + str(s) + "px;border-radius:50%;object-fit:cover;'>"
        except Exception:
            pass
    return "<div style='width:" + str(s) + "px;height:" + str(s) + "px;border-radius:50%;background:linear-gradient(135deg,#00B074,#056839);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:" + str(int(s * 0.38)) + "px;'>" + esc(str(n)[:2].upper()) + "</div>"


def flt(img, nm):
    try:
        im = img.convert("RGB")
        if nm == "Beauty":
            b = im.filter(ImageFilter.GaussianBlur(3))
            return ImageEnhance.Brightness(Image.blend(im, b, 0.5)).enhance(1.1)
        if nm == "Sepia":
            return ImageOps.colorize(im.convert("L"), "#704214", "#ffe8c0")
        if nm == "Cool":
            return ImageOps.colorize(im.convert("L"), "#20304a", "#c8e0ff")
        if nm == "Cartoon":
            w = max(1, im.width // 6)
            h = max(1, im.height // 6)
            s = im.resize((w, h)).filter(ImageFilter.MedianFilter(7))
            o = s.resize((im.width, im.height))
            o = ImageOps.posterize(o, 5)
            return ImageEnhance.Color(o).enhance(1.3)
        return im
    except Exception:
        return img


def isf(r):
    return not str(r or "").startswith("http") and os.path.exists(str(r or ""))


D = ldb()
if not isinstance(D.get("users"), dict):
    D["users"] = {}
for u, p, n in [("demo", "1234", "Demo"), ("hoor", "1234", "Hoor")]:
    if u not in D["users"] and u not in D["ban"]:
        D["users"][u] = {"password": hp(p), "dn": n, "bio": "Hi!", "coins": 500, "blk": [], "av": None, "fails": 0, "lock": False, "pin": "", "fin": False, "al": 0, "cf": False, "private": False, "cm": "Everyone"}
if not D["posts"]:
    D["posts"] = [
        {"id": "s1", "u": "hoor", "type": "yt", "ref": "aqz-KE-bpKQ", "cap": "Big Buck Bunny!", "lk": {}, "cm": []},
        {"id": "s2", "u": "demo", "type": "txt", "grad": GR[0], "txt": "Welcome!", "cap": "Hello!", "lk": {}, "cm": []}]
sdb(D)

SS = st.session_state
for k, v in {"pg": "sp", "li": False, "un": "", "am": "li", "tb": "Home", "sp2": "mn", "blk": [], "cc": "", "vu": None, "or": "", "story": False, "cr": "", "pk": True, "fk": True, "pa": 0, "pl": 0, "mv": "ls", "mt": "", "dt": "msg", "dk": False, "dc": 0, "la": 0, "fs": "Following"}.items():
    if k not in SS:
        SS[k] = v


def go(t):
    SS.tb = t
    if t == "Settings":
        SS.sp2 = "mn"
    if t == "Messages":
        SS.mv = "ls"
    rr()


CSS = """
<style>
.stApp{background:#f0f2f5!important}
header[data-testid=stHeader],#MainMenu,footer,
[data-testid=stToolbar],[data-testid=stStatusWidget],
[data-testid=stDecoration]{display:none!important}
.block-container{max-width:430px;margin:0 auto;
background:#fff;padding:0 10px 40px!important;
min-height:100vh;box-shadow:0 0 35px rgba(0,0,0,.18)}
.tb{position:sticky;top:0;z-index:99;display:flex;
justify-content:space-between;align-items:center;
padding:10px 14px;background:#fff;border-bottom:
1px solid #e5e7eb;margin:0 -10px}
.tl{font-size:24px;font-weight:700;font-family:
'Segoe Script',cursive;color:#1f2937}
.tr{font-size:22px;display:flex;gap:14px}
.sr{display:flex;gap:14px;padding:12px 4px;
border-bottom:1px solid #e5e7eb;overflow-x:auto}
.sc{display:flex;flex-direction:column;align-items:
center;min-width:64px}
.rg{width:58px;height:58px;border-radius:50%;padding:3px;
background:linear-gradient(135deg,#00B074,#056839);
display:flex;align-items:center;justify-content:center}
.rgg{background:#dbdbdb}
.ri{width:100%;height:100%;border-radius:50%;background:
#fff;border:2px solid #fff;display:flex;align-items:
center;justify-content:center;font-weight:bold;
color:#4b5563;font-size:14px}
.sn{font-size:11px;color:#4b5563;margin-top:4px}
.pc{background:#fff;border-bottom:1px solid #e5e7eb;
margin-bottom:10px}
.ph2{display:flex;align-items:center;padding:10px 4px}
.pu{font-size:14px;font-weight:700;color:#1f2937}
.pph{width:100%;height:260px;background:#f3f4f6;
display:flex;align-items:center;justify-content:center}
.lk{padding:6px 2px 0;font-weight:600;font-size:13px;
color:#1f2937;margin:0}
.pd{padding:0 2px 8px;font-size:14px;color:#1f2937;margin:0}
.ph{padding:14px 4px;font-size:20px;font-weight:bold;
color:#00B074;border-bottom:1px solid #e5e7eb;
text-align:center}
.nr{padding:10px 4px;border-bottom:1px solid #e5e7eb;
font-size:14px;color:#1f2937}
.fr{display:flex;align-items:center;padding:10px 4px;
border-bottom:1px solid #e5e7eb}
.bm{background:#00B074;color:#fff;padding:8px 13px;
border-radius:18px 18px 4px 18px;max-width:78%;
margin:3px 0 3px auto;font-size:14px;display:block}
.bh{background:#e5e7eb;color:#1f2937;padding:8px 13px;
border-radius:18px 18px 18px 4px;max-width:78%;
margin:3px auto 3px 0;font-size:14px;display:block}
.bt{font-size:10px;opacity:.7;display:block;
text-align:right;margin-top:2px}
.dmh{display:flex;align-items:center;gap:8px;padding:
14px 4px 10px;border-bottom:1px solid #e5e7eb;font-"
"size:24px;font-weight:700;color:#1f2937}
.dmi{display:flex;align-items:center;gap:12px;
padding:12px 4px;border-bottom:1px solid #e5e7eb}
.dmn{font-weight:700;font-size:14px;color:#1f2937}
.dms{font-size:12px;color:#9ca3af;margin-top:2px}
.igt{display:flex;justify-content:space-between;
align-items:center;padding:12px 4px}
.igu{font-size:22px;font-weight:700;color:#1f2937}
.igr{display:flex;gap:24px;padding:10px 4px;
align-items:center}
.igs{text-align:center}
.igs b{display:block;font-size:18px;color:#1f2937}
.igs span{font-size:12px;color:#6b7280}
.ign{font-weight:700;font-size:14px;color:#1f2937;
padding:4px 4px 0}
.igb{font-size:13px;color:#4b5563;padding:0 4px 12px}
.igg{display:grid;grid-template-columns:repeat(3,1fr);
gap:2px;padding:10px 0}
.igg div{aspect-ratio:1;background:#f3f4f6;display:
flex;align-items:center;justify-content:center;
font-size:28px;overflow:hidden}
.dch{font-weight:700;font-size:14px;color:#1f2937;
padding:12px 4px 6px;border-top:1px solid #e5e7eb}
.dcr{display:flex;align-items:center;gap:10px;
padding:8px 4px}
.dcn{font-weight:600;font-size:13px;color:#1f2937}
.dcs{font-size:11px;color:#9ca3af}
.fbc{height:110px;border-radius:0 0 14px 14px;
background:linear-gradient(135deg,#00B074,#056839);
margin:0 -10px}
.fsw{display:flex;gap:10px;padding:8px 4px}
.fsb{padding:5px 12px;border:1px solid #e5e7eb;
border-radius:18px;font-size:12px;color:#4b5563;
font-weight:600}
div[data-testid=stButton]>button{background:#00B074
!important;color:#fff!important;font-weight:600
!important;border:none!important;border-radius:12px
!important}
</style>
"""

DARK = """
<style>
.stApp{background:#0f1110!important}
.block-container{background:#1b1e1b!important}
.tb{background:#1b1e1b!important;border-color:#2a2e2a}
.tl,.pu,.dmn,.lk,.pd,.nr{color:#eef1ee!important}
.dms{color:#9aa69a!important}
.bh{background:#2a2e2a!important;color:#eef1ee!important}
.ph{color:#00e08a!important;border-color:#2a2e2a}
.fr,.dmi,.nr{border-color:#2a2e2a!important}
</style>
"""


def csh():
    st.markdown(CSS, unsafe_allow_html=True)
    if SS.dk:
        st.markdown(DARK, unsafe_allow_html=True)


# SPLASH
if SS.pg == "sp":
    csh()
    st.markdown("<div style='display:flex;flex-direction:column;align-items:center;justify-content:center;height:60vh;'><h1 style='font-size:90px;font-weight:900;color:#1f2937;margin:0;'>HMF</h1><p style='font-size:24px;color:#4b5563;'>HMF Book</p></div>", unsafe_allow_html=True)
    if st.button("Get Started", use_container_width=True):
        SS.pg = "au"
        rr()


# AUTH
elif SS.pg == "au":
    csh()
    sup = SS.am == "su"
    t = "Create Account" if sup else "Welcome Back"
    b = "Sign Up" if sup else "Login"
    st.markdown("<div style='text-align:center;margin-top:14px;'><div style='background:linear-gradient(135deg,#00B074,#056839);display:inline-block;padding:16px 48px;border-radius:22px;'><h1 style='color:#fff;font-size:34px;margin:0;font-weight:900;letter-spacing:3px;'>HMF</h1></div></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>" + t + "</h2>", unsafe_allow_html=True)
    un = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button(b, use_container_width=True):
        u = un.strip().lower()
        d = ldb()
        if not u or not pw:
            st.error("Dono fields!")
        elif u in d["ban"]:
            st.error("BANNED!")
        elif sup:
            if u in d["users"]:
                st.error("Taken!")
            else:
                if not d.get("owner"):
                    d["owner"] = u
                d["users"][u] = {"password": hp(pw), "dn": u.title(), "bio": "Hi!", "coins": 100, "blk": [], "av": None, "fails": 0, "lock": False, "pin": "", "fin": False, "al": 0, "cf": False, "private": False, "cm": "Everyone"}
                sdb(d)
                SS.li = True
                SS.un = u
                SS.pg = "ap"
                rr()
        else:
            r = d["users"].get(u)
            if r and pok(r.get("password", ""), pw):
                SS.li = True
                SS.un = u
                SS.blk = r.get("blk", [])
                SS.pg = "ap"
                SS.la = time.time()
                rr()
            else:
                st.error("Invalid!")
    if st.button("Switch to " + ("Login" if sup else "Sign Up")):
        SS.am = "li" if sup else "su"
        rr()
    st.caption("Demo: demo/1234")


# MAIN
elif SS.pg == "ap" and SS.li:
    csh()
    d = ldb()
    me = d["users"].get(SS.un, {})
    own = SS.un == d.get("owner", "")
    if me.get("al", 0) > 0 and SS.la > 0:
        if time.time() - SS.la > me["al"] * 60:
            SS.li = False
            SS.pg = "au"
            rr()
    SS.la = time.time()

    if me.get("lock") and not SS.pk:
        st.markdown("<div style='text-align:center;padding:25vh 0;font-size:70px;'>🔒</div>", unsafe_allow_html=True)
        pi = st.text_input("PIN", type="password", max_chars=4)
        if st.button("Unlock", use_container_width=True):
            if pi == me.get("pin"):
                SS.pk = True
                rr()
            else:
                st.error("Wrong!")
    elif me.get("fin") and not SS.fk:
        st.markdown("<div style='text-align:center;padding:25vh 0;font-size:70px;'>👆</div>", unsafe_allow_html=True)
        if st.button("Scan", use_container_width=True):
            time.sleep(1.2)
            SS.fk = True
            rr()
    else:
        un = unc(SS.un)

        # ===== INSTAGRAM TOPBAR =====
        st.markdown("<div class='tb'><div class='tl'>HMF Book</div><div class='tr'>❤️ ✈️</div></div>", unsafe_allow_html=True)

        tq = st.columns(4)
        if tq[0].button("🔔" + str(un) if un else "🔔", key="tbn", use_container_width=True):
            go("Notifs")
        if tq[1].button("🎲", key="tbg", use_container_width=True):
            go("Games")
        if tq[2].button("🌙" if not SS.dk else "☀️", key="tbd", use_container_width=True):
            SS.dk = not SS.dk
            rr()
        if tq[3].button("⚙️", key="tbs", use_container_width=True):
            go("Settings")

        # ===== BOTTOM NAV (5 - Instagram!) =====
        nv = st.columns(5)
        for i, (t, ic) in enumerate([("Home", "🏠"), ("Search", "🔍"), ("Create", "➕"), ("Reels", "🎬"), ("Profile", "👤")]):
            mk = ic
            if SS.tb == t:
                mk = "🔹"
            if nv[i].button(mk, key="nv_" + t, use_container_width=True):
                go(t)

        # ===== VIEW USER =====
        if SS.vu and SS.vu != SS.un:
            vu = SS.vu
            if vu not in d["users"]:
                SS.vu = None
                rr()
            ud = d["users"].get(vu, {})
            st.markdown("<div class='fbc'></div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align:center;margin-top:-50px;'>" + av(vu, ud.get("av"), 90) + "</div>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:center;'>" + esc(ud.get("dn", vu)) + "</h3>", unsafe_allow_html=True)
            v1, v2 = st.columns(2)
            if v1.button("✉️ Message", key="vfm"):
                SS.mv = "ch"
                SS.mt = vu
                SS.vu = None
                go("Messages")
            if v2.button("← Back", key="vbk"):
                SS.vu = None
                rr()

        elif SS.tb == "Create":
            st.markdown("<div class='ph'>➕ Create</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            if c1.button("📷 Post / Story", key="cp1", use_container_width=True):
                SS.cr = "post"
                rr()
            if c2.button("🎬 Reel", key="cp2", use_container_width=True):
                SS.cr = "reel"
                rr()

            if SS.cr == "post":
                kd = st.radio("Type:", ["Photo", "Camera 🎨", "YouTube"], horizontal=True, key="ck")
                cap = st.text_input("Caption", key="uc")
                if kd == "Camera 🎨":
                    f2 = st.selectbox("Filter:", FL, key="cf")
                    cam = st.camera_input("📸", key="cam")
                    fi = None
                    if cam is not None:
                        try:
                            pil = Image.open(cam)
                            fi = flt(pil, f2)
                            buf = io.BytesIO()
                            fi.save(buf, format="PNG")
                            st.image(buf.getvalue())
                        except Exception:
                            pass
                    s1, s2 = st.columns(2)
                    if s1.button("Post to Feed", key="up2", use_container_width=True):
                        if fi is not None:
                            d = ldb()
                            d["posts"].insert(0, {"id": uuid.uuid4().hex[:8], "u": SS.un, "type": "img", "ref": spl(fi), "cap": cap, "lk": {}, "cm": []})
                            sdb(d)
                            SS.cr = ""
                            st.success("Posted!")
                            go("Home")
                        else:
                            st.warning("Photo!")
                    if s2.button("Add Story", key="up4", use_container_width=True):
                        if fi is not None:
                            d = ldb()
                            d["stories"].append({"id": uuid.uuid4().hex[:8], "u": SS.un, "ref": spl(fi), "t": time.time()})
                            sdb(d)
                            SS.cr = ""
                            st.success("Story added!")
                            go("Home")
                        else:
                            st.warning("Photo!")
                elif kd == "YouTube":
                    yl = st.text_input("Link", key="uy")
                    if st.button("Post", key="up1", use_container_width=True):
                        vid = pyt(yl)
                        if vid:
                            d = ldb()
                            d["posts"].insert(0, {"id": uuid.uuid4().hex[:8], "u": SS.un, "type": "yt", "ref": vid, "cap": cap, "lk": {}, "cm": []})
                            sdb(d)
                            SS.cr = ""
                            go("Home")
                        else:
                            st.error("Invalid!")
                else:
                    f = st.file_uploader("Photo", type=["png", "jpg"], key="uf")
                    s1, s2 = st.columns(2)
                    if s1.button("Post to Feed", key="up3", use_container_width=True):
                        if f is None:
                            st.warning("File!")
                        else:
                            d = ldb()
                            d["posts"].insert(0, {"id": uuid.uuid4().hex[:8], "u": SS.un, "type": "img", "ref": upl(f), "cap": cap, "lk": {}, "cm": []})
                            sdb(d)
                            SS.cr = ""
                            go("Home")
                    if s2.button("Add Story", key="up5", use_container_width=True):
                        if f is None:
                            st.warning("File!")
                        else:
                            d = ldb()
                            d["stories"].append({"id": uuid.uuid4().hex[:8], "u": SS.un, "ref": upl(f), "t": time.time()})
                            sdb(d)
                            SS.cr = ""
                            go("Home")

            elif SS.cr == "reel":
                st.markdown("### 🎬 Create Reel")
                f = st.file_uploader("Video", type=["mp4", "mov"], key="urv")
                cap = st.text_input("Caption", key="urc")
                if st.button("Post Reel", key="upr", use_container_width=True):
                    if f is None:
                        st.warning("Video!")
                    else:
                        d = ldb()
                        d["posts"].insert(0, {"id": uuid.uuid4().hex[:8], "u": SS.un, "type": "reel", "ref": upl(f), "cap": cap, "lk": {}, "cm": []})
                        sdb(d)
                        SS.cr = ""
                        go("Reels")

            if SS.cr:
                if st.button("← Back to Create", key="cb"):
                    SS.cr = ""
                    rr()

        else:
            if SS.vu == SS.un:
                SS.vu = None
                SS.tb = "Profile"

            # ===== HOME =====
            if SS.tb == "Home":
                f1, f2 = st.columns(2)
                if f1.button("Following", key="fw1", use_container_width=True):
                    SS.fs = "Following"
                    rr()
                if f2.button("Favorites", key="fw2", use_container_width=True):
                    SS.fs = "Favorites"
                    rr()

                my_story = None
                for s in d.get("stories", []):
                    if s["u"] == SS.un:
                        my_story = s
                others = []
                for s in d.get("stories", []):
                    if s["u"] != SS.un:
                        others.append(s)

                srow = "<div class='sr'>"
                if my_story:
                    srow = srow + "<div class='sc'><div class='rg'><div class='ri'>" + esc(SS.un[:2].upper()) + "</div></div><div class='sn'>Your Story</div></div>"
                else:
                    srow = srow + "<div class='sc'><div class='rg rgg'><div class='ri'>+</div></div><div class='sn'>Your Story</div></div>"
                for s in others[:4]:
                    srow = srow + "<div class='sc'><div class='rg'><div class='ri'>" + esc(s["u"][:2].upper()) + "</div></div><div class='sn'>" + esc(s["u"]) + "</div></div>"
                srow = srow + "</div>"
                st.markdown(srow, unsafe_allow_html=True)

                if st.button("➕ Add to Story", key="ads", use_container_width=True):
                    go("Create")
                    SS.cr = "post"
                    rr()

                vis = []
                frs = d["fr"].get(SS.un, [])
                for p in d["posts"]:
                    if p.get("type") == "reel":
                        continue
                    if p["u"] in SS.blk:
                        continue
                    if SS.fs == "Favorites" and p["u"] not in frs and p["u"] != SS.un:
                        continue
                    vis.append(p)

                if SS.cc:
                    SS[SS.cc] = ""
                    SS.cc = ""
                for p in vis:
                    st.markdown("<div class='pc'><div class='ph2'>" + av(p["u"], d["users"].get(p["u"], {}).get("av")) + "<div class='pu'>" + esc(p["u"]) + "</div></div></div>", unsafe_allow_html=True)
                    pt = p.get("type", "txt")
                    if pt == "txt":
                        st.markdown("<div class='pph' style='background:" + p.get("grad", "#f0f0f0") + ";color:#056839;font-weight:bold;'>" + esc(p.get("txt", "")) + "</div>", unsafe_allow_html=True)
                    elif pt == "yt":
                        yt = "<iframe width='100%' height='220' src='https://www.youtube.com/embed/" + p["ref"] + "' frameborder='0' allowfullscreen></iframe>"
                        components.html(yt, height=230)
                    elif pt == "img" and isf(p["ref"]):
                        st.image(p["ref"], use_container_width=True)
                    elif pt == "video":
                        st.video(p["ref"])
                    lk = SS.un in p.get("lk", {})
                    c1, c2, c3 = st.columns(3)
                    ic = "🤍"
                    if lk:
                        ic = "❤️"
                    if c1.button(ic, key="lk_" + p["id"], use_container_width=True):
                        d = ldb()
                        for po in d["posts"]:
                            if po["id"] == p["id"]:
                                l2 = po.setdefault("lk", {})
                                if SS.un in l2:
                                    del l2[SS.un]
                                else:
                                    l2[SS.un] = True
                                break
                        sdb(d)
                        rr()
                    if c2.button("👤", key="vu_" + p["id"], use_container_width=True):
                        SS.vu = p["u"]
                        rr()
                    if c3.button("🚫", key="bl_" + p["id"], use_container_width=True):
                        d = ldb()
                        r = d["users"].get(SS.un)
                        if r is not None:
                            b = r.setdefault("blk", [])
                            if p["u"] not in b:
                                b.append(p["u"])
                            sdb(d)
                            SS.blk = list(b)
                        rr()
                    nl = str(len(p.get("lk", {})))
                    st.markdown("<p class='lk'>" + nl + " likes</p><p class='pd'><b>" + esc(p["u"]) + "</b> " + esc(p.get("cap", "")) + "</p>", unsafe_allow_html=True)
                    cm = st.text_input("c", key="c_" + p["id"], placeholder="Comment...", label_visibility="collapsed")
                    if st.button("Post", key="p_" + p["id"]):
                        if cm.strip():
                            if not cln(cm) and me.get("cf", False):
                                st.warning("Filtered!")
                            else:
                                d = ldb()
                                for po in d["posts"]:
                                    if po["id"] == p["id"]:
                                        po.setdefault("cm", []).append({"u": SS.un, "txt": cm})
                                        break
                                sdb(d)
                                SS.cc = "c_" + p["id"]
                                rr()
                    for c in p.get("cm", []):
                        st.markdown("<p class='pd' style='color:#6b7280;'><b>" + esc(c["u"]) + "</b> " + esc(c["txt"]) + "</p>", unsafe_allow_html=True)

            # ===== SEARCH =====
            elif SS.tb == "Search":
                st.markdown("<div class='ph'>🔍 Search</div>", unsafe_allow_html=True)
                q = st.text_input("Search...", key="sq")
                if q.strip():
                    for u in d["users"]:
                        if q.lower() in u.lower():
                            st.markdown("<div class='fr'>" + av(u, None, 40) + "<div><b>@" + u + "</b></div></div>", unsafe_allow_html=True)
                            if st.button("Open", key="so_" + u, use_container_width=True):
                                SS.vu = u
                                rr()
                else:
                    st.caption("Search users...")

            # ===== REELS =====
            elif SS.tb == "Reels":
                st.markdown("<div class='ph'>🎬 Reels</div>", unsafe_allow_html=True)
                for r in reversed(d["posts"]):
                    if r.get("type") in ("reel", "video"):
                        st.markdown("<div class='ph2'>" + av(r["u"], None, 36) + "<div class='pu'>@" + esc(r["u"]) + "</div></div>", unsafe_allow_html=True)
                        st.video(r["ref"])
                        lk = SS.un in r.get("lk", {})
                        ic = "🤍"
                        if lk:
                            ic = "❤️"
                        if st.button(ic + " " + str(len(r.get("lk", {}))), key="rlk_" + r["id"]):
                            d = ldb()
                            for po in d["posts"]:
                                if po["id"] == r["id"]:
                                    l2 = po.setdefault("lk", {})
                                    if SS.un in l2:
                                        del l2[SS.un]
                                    else:
                                        l2[SS.un] = True
                                    break
                            sdb(d)
                            rr()

            # ===== MESSAGES =====
            elif SS.tb == "Messages":
                if HAS_R:
                    st_autorefresh(interval=4000, key="mr")
                d = ldb()
                if SS.mv == "ch":
                    tgt = SS.mt
                    if tgt not in d["users"]:
                        SS.mv = "ls"
                        rr()
                    if st.button("←", key="cbk"):
                        SS.mv = "ls"
                        rr()
                    ud = d["users"].get(tgt, {})
                    hd = "<div class='dmi'>" + av(tgt, ud.get("av"), 44) + "<div><div class='dmn'>" + esc(ud.get("dn", tgt)) + "</div><div class='dms'>Active now</div></div></div>"
                    st.markdown(hd, unsafe_allow_html=True)
                    msgs = []
                    for m in d["msg"]:
                        if (m["f"] == SS.un and m["to"] == tgt) or (m["f"] == tgt and m["to"] == SS.un):
                            msgs.append(m)
                    for m in sorted(msgs, key=lambda x: x["t"]):
                        mine = m["f"] == SS.un
                        ts = time.strftime("%I:%M %p", time.localtime(m["t"])).lower()
                        if mine:
                            cls = "bm"
                        else:
                            cls = "bh"
                        st.markdown("<span class='" + cls + "'>" + esc(m.get("txt", "")) + "<span class='bt'>" + ts + "</span></span>", unsafe_allow_html=True)
                        r = m.get("rx", [])
                        mk = m.get("id", str(m["t"]))
                        lb = "👍"
                        if r:
                            lb = "👍 " + str(len(r))
                        if st.button(lb, key="rx_" + mk):
                            trx(m.get("id"), SS.un)
                            rr()
                    tx = st.text_input("Message...", key="ctx", placeholder="Message...")
                    if st.button("Send", key="csd", use_container_width=True):
                        if tx.strip():
                            sm(tgt, tx.strip())
                            rr()
                else:
                    dmh = "<div class='dmh'>← " + esc(SS.un) + "</div>"
                    st.markdown(dmh, unsafe_allow_html=True)
                    sq = st.text_input("Search", key="dm_s", placeholder="Search")
                    t1, t2 = st.columns(2)
                    if t1.button("Messages", key="dmt1", use_container_width=True):
                        SS.dt = "msg"
                        rr()
                    if t2.button("Requests", key="dmt2", use_container_width=True):
                        SS.dt = "req"
                        rr()
                    if SS.dt == "req":
                        reqs = []
                        for r in d.get("freq", []):
                            if r["to"] == SS.un:
                                reqs.append(r)
                        if not reqs:
                            st.info("No requests")
                        for i, r in enumerate(reqs):
                            f = r["from"]
                            fu = d["users"].get(f, {})
                            row = "<div class='dmi'>" + av(f, fu.get("av"), 56) + "<div><div class='dmn'>" + esc(fu.get("dn", f)) + "</div><div class='dms'>Sent request</div></div></div>"
                            st.markdown(row, unsafe_allow_html=True)
                            a1, a2 = st.columns(2)
                            if a1.button("Accept", key="dma_" + str(i), use_container_width=True):
                                d = ldb()
                                d["freq"] = [x for x in d["freq"] if not (x["from"] == f and x["to"] == SS.un)]
                                d["fr"].setdefault(SS.un, []).append(f)
                                d["fr"].setdefault(f, []).append(SS.un)
                                sdb(d)
                                rr()
                            if a2.button("Delete", key="dmd_" + str(i), use_container_width=True):
                                d = ldb()
                                d["freq"] = [x for x in d["freq"] if not (x["from"] == f and x["to"] == SS.un)]
                                sdb(d)
                                rr()
                    else:
                        ps = set()
                        for m in d["msg"]:
                            if m["f"] == SS.un:
                                ps.add(m["to"])
                            elif m["to"] == SS.un:
                                ps.add(m["f"])
                        for f in d["fr"].get(SS.un, []):
                            ps.add(f)
                        cv = []
                        for p in ps:
                            if p != SS.un and p not in SS.blk:
                                if sq and sq.lower() not in p.lower():
                                    continue
                                cn = []
                                for m in d["msg"]:
                                    if (m["f"] == SS.un and m["to"] == p) or (m["f"] == p and m["to"] == SS.un):
                                        cn.append(m)
                                last = cn[-1] if cn else None
                                cv.append({"u": p, "l": last})
                        cv.sort(key=lambda c: (c["l"]["t"] if c["l"] else 0), reverse=True)
                        if not cv:
                            st.info("No messages")
                        for c in cv:
                            p = c["u"]
                            ud = d["users"].get(p, {})
                            stx = "Say hello 👋"
                            if c["l"]:
                                mins = int((time.time() - c["l"]["t"]) / 60)
                                if mins < 1:
                                    tm = "now"
                                elif mins < 60:
                                    tm = str(mins) + "m ago"
                                else:
                                    tm = str(int(mins / 60)) + "h ago"
                                if c["l"]["f"] == SS.un:
                                    stx = "Sent " + tm
                                else:
                                    stx = "Active " + tm
                            row = "<div class='dmi'>" + av(p, ud.get("av"), 56) + "<div><div class='dmn'>" + esc(ud.get("dn", p)) + "</div><div class='dms'>" + stx + "</div></div></div>"
                            st.markdown(row, unsafe_allow_html=True)
                            if st.button("💬", key="op_" + p, use_container_width=True):
                                SS.mv = "ch"
                                SS.mt = p
                                rr()
                        with st.expander("➕ New"):
                            oth = [x for x in d["users"] if x != SS.un]
                            pick = st.selectbox("Chat:", oth, key="ncs")
                            if st.button("Start", key="ncb", use_container_width=True):
                                SS.mv = "ch"
                                SS.mt = pick
                                rr()

            # ===== NOTIFS =====
            elif SS.tb == "Notifs":
                st.markdown("<div class='ph'>🔔 Notifications</div>", unsafe_allow_html=True)
                d = ldb()
                mn = [n for n in d["notif"] if n.get("to") == SS.un][:40]
                if st.button("Mark read", key="mkr", use_container_width=True):
                    d = ldb()
                    for n in d["notif"]:
                        if n.get("to") == SS.un:
                            n["r"] = True
                    sdb(d)
                    rr()
                if not mn:
                    st.info("Empty!")
                for n in mn:
                    ts = time.strftime("%d %b %H:%M", time.localtime(n["t"]))
                    st.markdown("<div class='nr'>" + n["txt"] + "<br><span style='font-size:11px;color:#9ca3af;'>" + ts + "</span></div>", unsafe_allow_html=True)

            # ===== GAMES =====
            elif SS.tb == "Games":
                st.markdown("<div class='ph'>🎲 Games</div>", unsafe_allow_html=True)
                if st.button("🎲 Roll Dice", use_container_width=True):
                    SS.dc = random.randint(1, 6)
                    if SS.dc == 6:
                        d = ldb()
                        u = d["users"].get(SS.un)
                        if u is not None:
                            u["coins"] = u.get("coins", 0) + 5
                            sdb(d)
                    rr()
                if SS.dc:
                    st.markdown("<h2 style='text-align:center;color:#00B074;'>🎯 " + str(SS.dc) + "</h2>", unsafe_allow_html=True)

            # ===== PROFILE =====
            elif SS.tb == "Profile":
                mp = [p for p in d["posts"] if p["u"] == SS.un]
                fr = d["fr"].get(SS.un, [])
                ml = sum(len(p.get("lk", {})) for p in mp)

                tp = "<div class='igt'><div class='igu'>" + esc(SS.un) + "</div><div style='font-size:22px;'>&#8942;</div></div>"
                st.markdown(tp, unsafe_allow_html=True)

                rw = "<div class='igr'>" + av(SS.un, me.get("av"), 86)
                rw = rw + "<div class='igs'><b>" + str(len(mp)) + "</b><span>posts</span></div>"
                rw = rw + "<div class='igs'><b>" + str(len(fr)) + "</b><span>followers</span></div>"
                rw = rw + "<div class='igs'><b>" + str(len(fr)) + "</b><span>following</span></div></div>"
                st.markdown(rw, unsafe_allow_html=True)

                st.markdown("<div class='ign'>" + esc(me.get("dn", SS.un)) + "</div>", unsafe_allow_html=True)
                st.markdown("<div class='igb'>" + esc(me.get("bio", "")) + " · ❤️ " + str(ml) + " likes · 💰" + str(me.get("coins", 0)) + "</div>", unsafe_allow_html=True)

                if own:
                    st.markdown("<p style='text-align:center;'><span style='background:#f59e0b;color:#fff;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:bold;'>👑 OWNER</span></p>", unsafe_allow_html=True)

                # Menu button
                if st.button("☰ Menu (Settings)", key="pmn", use_container_width=True):
                    go("Settings")

                if st.button("💰 Payout (100)", key="pp", use_container_width=True):
                    d = ldb()
                    u = d["users"].get(SS.un)
                    if u is not None and u.get("coins", 0) >= 100:
                        u["coins"] -= 100
                        sdb(d)
                        st.success("Payout!")
                        rr()
                    else:
                        st.warning("Min 100!")

                # Post grid
                if mp:
                    g = "<div class='igg'>"
                    for p in mp[:9]:
                        g = g + "<div>"
                        if p.get("type") == "txt":
                            g = g + esc(p.get("txt", ""))[:8]
                        elif p.get("type") == "yt":
                            g = g + "📺"
                        elif p.get("type") == "img":
                            g = g + "🖼️"
                        else:
                            g = g + "🎬"
                        g = g + "</div>"
                    g = g + "</div>"
                    st.markdown(g, unsafe_allow_html=True)
                else:
                    st.caption("No posts - Create tab use karein!")

                with st.expander("🖼️ Change Pic"):
                    f3 = st.selectbox("Filter:", FL, key="pf")
                    pi = st.file_uploader("Upload", type=["png", "jpg"], key="pi")
                    cam = st.camera_input("📸", key="pcam")
                    if st.button("Update", key="pu", use_container_width=True):
                        src = pi if pi is not None else cam
                        if src is not None:
                            setp_flag = True
                            pil = Image.open(src)
                            sp(SS.un, "av", spl(filt(pil, f3)))
                            st.success("Updated!")
                            rr()

                st.markdown("<div class='dch'>🔍 Discover People</div>", unsafe_allow_html=True)
                sug = []
                for u in d["users"]:
                    if u == SS.un or u in fr or u in SS.blk:
                        continue
                    skip = False
                    for x in d.get("freq", []):
                        if x["from"] == SS.un and x["to"] == u:
                            skip = True
                    if not skip:
                        sug.append(u)
                for u in sug[:5]:
                    ud = d["users"].get(u, {})
                    mu = len(d["fr"].get(u, []))
                    r2 = "<div class='dcr'>" + av(u, ud.get("av"), 44)
                    r2 = r2 + "<div style='flex:1;'><div class='dcn'>" + esc(ud.get("dn", u)) + "</div><div class='dcs'>"
                    if mu > 0:
                        r2 = r2 + str(mu) + " mutual"
                    else:
                        r2 = r2 + "Suggested"
                    r2 = r2 + "</div></div></div>"
                    st.markdown(r2, unsafe_allow_html=True)
                    d1, d2 = st.columns(2)
                    if d1.button("Follow", key="df_" + u, use_container_width=True):
                        d = ldb()
                        d["freq"].append({"from": SS.un, "to": u, "t": time.time()})
                        sdb(d)
                        nt(u, "@" + SS.un + " followed you!")
                        rr()
                    if d2.button("👤", key="dv_" + u, use_container_width=True):
                        SS.vu = u
                        rr()

            # ===== SETTINGS (Instagram style!) =====
            elif SS.tb == "Settings":
                if SS.sp2 == "mn":
                    st.markdown("<div class='ph'>⚙️ Settings</div>", unsafe_allow_html=True)
                    for lb, pg in [("🔒 Privacy", "priv"), ("🔐 Security", "sec"), ("🔔 Notifications", "ntf"), ("📋 Personal", "per"), ("🎨 Appearance", "app"), ("🚫 Blocked", "blk"), ("ℹ️ About", "ab")]:
                        if st.button(lb + " ›", key="m_" + pg, use_container_width=True):
                            SS.sp2 = pg
                            rr()
                    if own:
                        if st.button("🛡️ OWNER ›", key="mown", use_container_width=True):
                            SS.sp2 = "adm"
                            rr()
                    if st.button("🚪 Logout", key="mlo", use_container_width=True):
                        SS.li = False
                        SS.pg = "au"
                        rr()

                elif SS.sp2 == "priv":
                    if st.button("← Back", key="bk_p"):
                        SS.sp2 = "mn"
                        rr()
                    cp = st.checkbox("🔒 Private Account", value=me.get("private", False), key="cpr")
                    if cp != me.get("private", False):
                        sp(SS.un, "private", cp)
                        rr()
                    ccm = st.selectbox("Who can comment?", ["Everyone", "Followers", "No One"], key="ccm")
                    if ccm != me.get("cm", "Everyone"):
                        sp(SS.un, "cm", ccm)
                        rr()
                    ccf = st.checkbox("Close Friends story only", value=me.get("cf", False), key="ccf")
                    if ccf != me.get("cf", False):
                        sp(SS.un, "cf", ccf)
                        rr()

                elif SS.sp2 == "sec":
                    if st.button("← Back", key="bk_s"):
                        SS.sp2 = "mn"
                        rr()
                    if not me.get("lock"):
                        np = st.text_input("4-digit PIN", type="password", max_chars=4, key="spn")
                        if st.button("Enable Lock", key="sae", use_container_width=True):
                            if len(np) == 4 and np.isdigit():
                                sp(SS.un, "pin", np)
                                sp(SS.un, "lock", True)
                                st.success("ON!")
                                rr()
                            else:
                                st.warning("4 digits!")
                    else:
                        st.success("Lock ON")
                        l1, l2 = st.columns(2)
                        if l1.button("Lock Now", key="sln", use_container_width=True):
                            SS.pk = False
                            rr()
                        if l2.button("Disable", key="sdn", use_container_width=True):
                            sp(SS.un, "lock", False)
                            sp(SS.un, "pin", "")
                            rr()
                    cfn = st.checkbox("Fingerprint", value=me.get("fin", False), key="sf2")
                    if cfn != me.get("fin", False):
                        sp(SS.un, "fin", cfn)
                        if cfn:
                            SS.fk = False
                        else:
                            SS.fk = True
                        rr()
                    cur = me.get("al", 0)
                    opts = [0, 5, 10, 30]
                    ci = opts.index(cur) if cur in opts else 0
                    nal = st.selectbox("Auto logout:", opts, index=ci, key="sal")
                    if nal != cur:
                        sp(SS.un, "al", nal)
                        rr()
                    if st.button("Login Activity", key="la_", use_container_width=True):
                        st.info("📱 This device - Active now")

                elif SS.sp2 == "ntf":
                    if st.button("← Back", key="bk_n"):
                        SS.sp2 = "mn"
                        rr()
                    st.caption("Notifications pause/on/off kar sakein:")
                    c1 = st.checkbox("❤️ Likes", value=True, key="n1")
                    c2 = st.checkbox("💬 Comments", value=True, key="n2")
                    c3 = st.checkbox("👥 Follows", value=True, key="n3")
                    c4 = st.checkbox("✉️ Messages", value=True, key="n4")
                    if st.button("Save", key="ns", use_container_width=True):
                        st.success("Saved!")

                elif SS.sp2 == "per":
                    if st.button("← Back", key="bk_pe"):
                        SS.sp2 = "mn"
                        rr()
                    dn = st.text_input("Name", value=me.get("dn", ""), key="pdn")
                    bio = st.text_input("Bio", value=me.get("bio", ""), key="pbio")
                    if st.button("Save", key="psv", use_container_width=True):
                        sp(SS.un, "dn", dn)
                        sp(SS.un, "bio", bio)
                        st.success("Saved!")

                elif SS.sp2 == "app":
                    if st.button("← Back", key="bk_a"):
                        SS.sp2 = "mn"
                        rr()
                    st.caption("Theme: " + ("Dark 🌙" if SS.dk else "Light ☀️"))
                    if st.button("Toggle Theme", key="tg", use_container_width=True):
                        SS.dk = not SS.dk
                        rr()
                    ds = st.checkbox("Data Saver (videos low quality)", key="ds")
                    if ds:
                        st.caption("Videos kam data mein load hongi")

                elif SS.sp2 == "blk":
                    if st.button("← Back", key="bk_b"):
                        SS.sp2 = "mn"
                        rr()
                    bi = st.text_input("Username", key="bki")
                    if st.button("Block", key="bkb", use_container_width=True):
                        u = bi.strip().lower()
                        if u and u != SS.un:
                            d = ldb()
                            r = d["users"].get(SS.un)
                            if r is not None:
                                r.setdefault("blk", []).append(u)
                                sdb(d)
                                SS.blk = list(r["blk"])
                            rr()
                    for i, u in enumerate(SS.blk):
                        b1, b2 = st.columns([0.6, 0.4])
                        b1.markdown("🚫 @" + u)
                        if b2.button("Unblock", key="ubk_" + str(i), use_container_width=True):
                            SS.blk.remove(u)
                            d = ldb()
                            r = d["users"].get(SS.un)
                            if r is not None:
                                r["blk"] = SS.blk
                                sdb(d)
                            rr()

                elif SS.sp2 == "ab":
                    if st.button("← Back", key="bk_ab"):
                        SS.sp2 = "mn"
                        rr()
                    st.markdown("### ℹ️ HMF Book")
                    st.markdown("**🏢 Parent:** HMF Group\n\n**👑 Founders:** Mehmood Sial, Hoor-e-Jannat, Farwa\n\n**📍 HQ:** Bahawalpur / Okara\n\n© 2026 HMF Group")

                elif SS.sp2 == "adm":
                    if st.button("← Back", key="bk_ad"):
                        SS.sp2 = "mn"
                        rr()
                    st.markdown("<div class='ph'>🛡️ Owner</div>", unsafe_allow_html=True)
                    d = ldb()
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Users", len(d["users"]))
                    c2.metric("Posts", len(d["posts"]))
                    c3.metric("Reports", len(d["rep"]))
                    for i, r in enumerate(reversed(d["rep"][:10])):
                        r1, r2 = st.columns([0.6, 0.4])
                        r1.markdown("🚩 @" + esc(r.get("user", "")))
                        ru = r.get("user", "")
                        if ru in d["ban"]:
                            if r2.button("Unban", key="ru_" + str(i), use_container_width=True):
                                d = ldb()
                                d["ban"].remove(ru)
                                sdb(d)
                                rr()
                        else:
                            if r2.button("BAN", key="rbn_" + str(i), use_container_width=True):
                                d = ldb()
                                d["ban"].append(ru)
                                sdb(d)
                                rr()


else:
    SS.pg = "sp"
    rr()

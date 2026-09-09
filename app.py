import streamlit as st
import re

st.set_page_config(page_title="HMF book", page_icon="💚",
                   layout="centered", initial_sidebar_state="collapsed")

# ─────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────
ss = st.session_state
ss.setdefault("screen", "welcome")      # welcome | signup | login
ss.setdefault("users", {})              # demo users (browser refresh pe reset)
ss.setdefault("logged_in", False)
ss.setdefault("current_user", None)
ss.setdefault("show_pw", False)

# URL se screen change: ?screen=signup / ?screen=login
qp = st.query_params
if qp.get("screen") in ("welcome", "signup", "login"):
    ss.screen = qp["screen"]

# ─────────────────────────────────────────────
# Icons (SVG data-URI) — input ke andar left side
# ─────────────────────────────────────────────
IC_USER = "%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='%239aa3af' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='12' cy='7' r='4'/%3E%3C/svg%3E"
IC_MAIL = "%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='%239aa3af' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z'/%3E%3Cpolyline points='22,6 12,13 2,6'/%3E%3C/svg%3E"
IC_LOCK = "%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='%239aa3af' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='11' width='18' height='11' rx='2' ry='2'/%3E%3Cpath d='M7 11V7a5 5 0 0 1 10 0v4'/%3E%3C/svg%3E"

# ─────────────────────────────────────────────
# Geometric decoration (triangles, dots, lines) — mockup jaisa
# ─────────────────────────────────────────────
VLINES = "".join(
    f"<line x1='{295+i*6}' y1='170' x2='{295+i*6}' y2='255'/>" for i in range(11)
)
DECOR = f"""
<svg class='decor' viewBox='0 0 400 700' preserveAspectRatio='xMidYMid slice'
     xmlns='http://www.w3.org/2000/svg'>
  <defs>
    <pattern id='dots' width='13' height='13' patternUnits='userSpaceOnUse'>
      <circle cx='2' cy='2' r='1.5' fill='rgba(255,255,255,.35)'/>
    </pattern>
  </defs>
  <rect x='16'  y='70'  width='92'  height='72' fill='url(#dots)'/>
  <rect x='300' y='130' width='78'  height='95' fill='url(#dots)'/>
  <rect x='55'  y='470' width='112' height='82' fill='url(#dots)'/>
  <path d='M55 35 l72 42 -72 42 z'  fill='none' stroke='rgba(255,255,255,.45)' stroke-width='1.5'/>
  <path d='M328 55 l62 36 -62 36 z' fill='none' stroke='rgba(255,255,255,.38)' stroke-width='1.5'/>
  <path d='M35 555 l62 36 -62 36 z' fill='none' stroke='rgba(255,255,255,.32)' stroke-width='1.5'/>
  <path d='M298 415 l56 33 -56 33 z'fill='none' stroke='rgba(255,255,255,.36)' stroke-width='1.5'/>
  <line x1='8'   y1='145' x2='150' y2='58'  stroke='rgba(255,255,255,.5)'  stroke-width='1.5'/>
  <line x1='255' y1='645' x2='385' y2='558' stroke='rgba(255,255,255,.42)' stroke-width='1.5'/>
  <g stroke='rgba(255,255,255,.35)' stroke-width='1'>{VLINES}</g>
  <path d='M338 292 l22 13 0 26 -22 13 -22 -13 0 -26 z' fill='none'
        stroke='rgba(255,255,255,.42)' stroke-width='1.5'/>
  <path d='M0 635 C 120 595, 265 685, 400 615 L400 700 L0 700 Z' fill='rgba(255,255,255,.08)'/>
  <path d='M0 668 C 140 628, 245 700, 400 652 L400 700 L0 700 Z' fill='rgba(255,255,255,.10)'/>
</svg>
"""

# ─────────────────────────────────────────────
# SHARED CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&family=Nunito:wght@500;600;700;800&display=swap');

#MainMenu, footer {{visibility:hidden;}}
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {{display:none!important;}}
.stApp {{background:#e4e8ee; font-family:'Nunito',sans-serif;}}
[data-testid="stWidgetLabel"] {{display:none!important;}}
.decor {{position:absolute; inset:0; width:100%; height:100%; pointer-events:none;}}

/* ── Inputs: white card field + icon ── */
.stTextInput input {{
    width:100%!important;
    border:1.6px solid #e2e5ea!important;
    border-radius:14px!important;
    padding:15px 16px 15px 50px!important;
    font-size:16px!important; font-family:'Nunito',sans-serif!important;
    color:#1f2430!important; background-color:#fff!important;
    box-shadow:0 1px 2px rgba(16,24,40,.05);
}}
.stTextInput input:focus {{border-color:#10b35f!important;
    box-shadow:0 0 0 3px rgba(16,179,95,.14)!important;}}
input[aria-label="Username"] {{
    background-image:url("data:image/svg+xml,{IC_USER}");
    background-repeat:no-repeat; background-position:15px center; background-size:20px 20px;}}
input[aria-label="Email"] {{
    background-image:url("data:image/svg+xml,{IC_MAIL}");
    background-repeat:no-repeat; background-position:15px center; background-size:20px 20px;}}
input[aria-label="Password"], input[aria-label="Username or Email"] {{
    background-repeat:no-repeat; background-position:15px center; background-size:20px 20px;}}
input[aria-label="Password"] {{
    background-image:url("data:image/svg+xml,{IC_LOCK}");
    padding-right:60px!important;}}
input[aria-label="Username or Email"] {{
    background-image:url("data:image/svg+xml,{IC_USER}");}}
[data-testid="stTextInput"] {{margin:0 0 14px;}}

/* ── Green pill buttons (Sign Up / Login / Logout) ── */
.stButton > button {{
    width:100%;
    background:linear-gradient(135deg,#14cd70,#0aa455)!important;
    color:#fff!important; font-weight:800!important; font-size:18px!important;
    font-family:'Nunito',sans-serif!important;
    border:none!important; border-radius:999px!important;
    padding:14px 0!important; box-shadow:0 10px 22px rgba(10,164,85,.35)!important;
    transition:transform .15s, filter .15s;
}}
.stButton > button:hover {{filter:brightness(1.06); transform:translateY(-1px);}}

/* ── Eye toggle: input ke upar right side overlap ── */
[data-testid="stColumn"]:nth-of-type(2) .stButton > button,
[data-testid="column"]:nth-of-type(2) .stButton > button {{
    background:transparent!important; border:none!important;
    box-shadow:none!important; width:auto!important;
    padding:8px 2px!important; font-size:22px!important;
    margin:4px 0 0 -58px!important; color:#8b93a1!important;
}}
</style>
""", unsafe_allow_html=True)

valid_email = lambda e: re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+", e or "")

# ═════════════════════════════════════════════
#  HOME (login ke baad)
# ═════════════════════════════════════════════
if ss.logged_in:
    st.markdown("""<style>
        .block-container{max-width:430px!important;margin:0 auto;padding-top:3rem!important;
        background:#fff;border-radius:0 0 26px 26px;
        box-shadow:0 12px 40px rgba(2,20,10,.14);padding-bottom:2.4rem!important;}
        </style>""", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='text-align:center;padding:30px 10px 6px;'>
          <div style="font-family:'Baloo 2';font-weight:800;font-size:56px;
                      color:#0aa455;line-height:1;">HMF</div>
          <h2 style="margin-top:14px;">🎉 Welcome, <b>{ss.current_user}</b>!</h2>
          <p style="color:#6b7280;">Aapka account ban gaya.<br>
          Yahan apna HMF-book feed + bottom-nav code paste karo.</p>
        </div>""", unsafe_allow_html=True)
    if st.button("Logout"):
        ss.logged_in, ss.current_user, ss.screen = False, None, "welcome"
        st.rerun()
    st.stop()

# ═════════════════════════════════════════════
#  SCREEN 1 — WELCOME / SPLASH
# ═════════════════════════════════════════════
if ss.screen == "welcome":
    st.markdown("""<style>
        .block-container{max-width:430px!important;margin:0 auto;padding:0!important;
        background:transparent!important;box-shadow:none!important;}
        .splash{position:relative;height:94vh;min-height:620px;overflow:hidden;
          display:flex;flex-direction:column;border-radius:0 0 34px 34px;
          background:radial-gradient(120% 90% at 85% 8%,rgba(255,255,255,.18),transparent 55%),
                     radial-gradient(130% 100% at 8% 100%,rgba(0,85,38,.30),transparent 60%),
                     linear-gradient(150deg,#2fe081 0%,#12c76b 42%,#07a254 100%);
          box-shadow:0 14px 44px rgba(2,40,18,.28);}
        .splash-logo{flex:1;display:flex;flex-direction:column;align-items:center;
          justify-content:center;position:relative;z-index:2;}
        .logo-big{font-family:'Baloo 2',cursive;font-weight:800;font-size:96px;
          color:#fff;letter-spacing:3px;line-height:1;
          text-shadow:0 6px 20px rgba(0,60,25,.28);}
        .logo-sub{font-family:'Baloo 2',cursive;font-weight:700;font-size:31px;
          color:#fff;margin-top:2px;text-shadow:0 4px 14px rgba(0,60,25,.25);}
        .btn-start{position:relative;z-index:2;margin:0 auto 7vh;
          background:#fff;color:#0aa455;font-weight:800;font-size:19px;
          font-family:'Nunito',sans-serif;padding:15px 52px;border-radius:999px;
          text-decoration:none;box-shadow:0 12px 28px rgba(0,50,20,.30);
          transition:transform .15s;}
        .btn-start:hover{transform:translateY(-3px);}
        </style>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="splash">
        {DECOR}
        <div class="splash-logo">
            <div class="logo-big">HMF</div>
            <div class="logo-sub">HMF book</div>
        </div>
        <a class="btn-start" href="?screen=signup">Get Started</a>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ═════════════════════════════════════════════
#  AUTH LAYOUT (signup / login dono ke liye)
# ═════════════════════════════════════════════
st.markdown("""<style>
.block-container{max-width:430px!important;margin:0 auto;
  padding:0 0 2.2rem!important;background:#fff;border-radius:0 0 26px 26px;
  box-shadow:0 12px 40px rgba(2,20,10,.14);}
[data-testid="stTextInput"],[data-testid="stButton"],
[data-testid="stAlert"],[data-testid="stColumns"],
[data-testid="stHorizontalBlock"]{padding-left:24px;padding-right:24px;}
.hero{position:relative;overflow:hidden;height:285px;
  display:flex;align-items:center;justify-content:center;
  background:radial-gradient(120% 90% at 85% 8%,rgba(255,255,255,.18),transparent 55%),
             radial-gradient(130% 100% at 8% 100%,rgba(0,85,38,.30),transparent 60%),
             linear-gradient(150deg,#2fe081 0%,#12c76b 42%,#07a254 100%);}
.logo-md{font-family:'Baloo 2',cursive;font-weight:800;font-size:68px;color:#fff;
  letter-spacing:3px;position:relative;z-index:2;
  text-shadow:0 6px 20px rgba(0,60,25,.28);}
.card-top{background:#fff;border-radius:34px 34px 0 0;height:44px;
  margin-top:-44px;position:relative;z-index:3;}
.card-title{font-family:'Nunito',sans-serif;font-weight:800;font-size:28px;
  color:#1f2430;margin:6px 24px 18px;}
.divider{display:flex;align-items:center;gap:12px;color:#9aa1ab;
  font-size:14px;padding:16px 24px 4px;}
.divider::before,.divider::after{content:"";flex:1;height:1px;background:#e5e8ec;}
.socials{display:flex;justify-content:center;gap:24px;padding:16px 0 4px;}
.soc{width:54px;height:54px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;cursor:pointer;transition:transform .15s;
  box-shadow:0 5px 14px rgba(0,0,0,.14);text-decoration:none;}
.soc:hover{transform:translateY(-4px) scale(1.06);}
.soc.g{background:#fff;border:1px solid #ececec;}
.soc.s{background:#FFFC00;font-size:26px;}
.soc.f{background:#1877F2;}
.switch-line{text-align:center;color:#6b7280;font-size:14.5px;
  padding:16px 0 2px;margin:0;}
.switch-line a{color:#0aa455;font-weight:800;text-decoration:none;}
[data-testid="stAlert"]{border-radius:14px!important;}
</style>""", unsafe_allow_html=True)

# ═════════════════════════════════════════════
#  SCREEN 2 — CREATE ACCOUNT (Sign Up)
# ═════════════════════════════════════════════
if ss.screen == "signup":
    st.markdown(f"""
    <div class="hero">{DECOR}<div class="logo-md">HMF</div></div>
    <div class="card-top"></div>
    <div class="card-title">Create Account</div>""", unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Username",
                             label_visibility="collapsed", key="su_u")
    email    = st.text_input("Email", placeholder="Email",
                             label_visibility="collapsed", key="su_e")

    pc1, pc2 = st.columns([6, 1])
    with pc1:
        password = st.text_input(
            "Password", placeholder="Password",
            type="default" if ss.show_pw else "password",
            label_visibility="collapsed", key="su_p")
    with pc2:
        if st.button("👁" if not ss.show_pw else "🙈", key="su_eye"):
            ss.show_pw = not ss.show_pw

    st.write("")
    if st.button("Sign Up"):
        errs = []
        if len(username.strip()) < 3:          errs.append("Username kam se kam 3 letters ka ho")
        if username.strip() in ss.users:       errs.append("Ye username already taken hai")
        if not valid_email(email):             errs.append("Sahi email daalo")
        if len(password) < 6:                  errs.append("Password kam se kam 6 characters")
        if errs:
            st.error("  •  ".join(errs))
        else:
            # ⚠ Demo: plain-text. Production mein hashlib.sha256 use karo + DB.
            ss.users[username.strip()] = {"email": email.strip(), "password": password}
            ss.current_user = username.strip()
            ss.logged_in = True
            st.rerun()

    st.markdown("""
    <div class="divider"><span>Or continue with</span></div>
    <div class="socials">
      <a class="soc g" title="Google (demo)">
        <svg viewBox="0 0 48 48" width="26" height="26"><path fill="#FFC107" d="M43.6 20.1H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3l5.7-5.7C34.5 6.1 29.5 4 24 4 13 4 4 13 4 24s9 20 20 20 20-9 20-20c0-1.3-.1-2.7-.4-3.9z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.9 1.2 8 3l5.7-5.7C34.5 6.1 29.5 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.1H42V20H24v8h11.3c-.8 2.3-2.3 4.3-4.1 5.7l6.2 5.2C36.9 39.2 44 34 44 24c0-1.3-.1-2.7-.4-3.9z"/></svg>
      </a>
      <a class="soc s" title="Snapchat (demo)">👻</a>
      <a class="soc f" title="Facebook (demo)">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="#fff"><path d="M13.5 21v-8h2.7l.4-3.1h-3.1V7.9c0-.9.3-1.5 1.6-1.5h1.7V3.6C16.5 3.5 15.5 3.4 14.4 3.4c-2.4 0-4 1.5-4 4.2v2.3H7.7V13h2.7v8h3.1z"/></svg>
      </a>
    </div>
    <p class="switch-line">Already have an account? <a href="?screen=login">Log in</a></p>
    """, unsafe_allow_html=True)

# ═════════════════════════════════════════════
#  SCREEN 3 — LOGIN
# ═════════════════════════════════════════════
elif ss.screen == "login":
    st.markdown(f"""
    <div class="hero">{DECOR}<div class="logo-md">HMF</div></div>
    <div class="card-top"></div>
    <div class="card-title">Welcome Back</div>""", unsafe_allow_html=True)

    user_or_email = st.text_input("Username or Email", placeholder="Username or Email",
                                  label_visibility="collapsed", key="li_u")
    pc1, pc2 = st.columns([6, 1])
    with pc1:
        password = st.text_input(
            "Password", placeholder="Password",
            type="default" if ss.show_pw else "password",
            label_visibility="collapsed", key="li_p")
    with pc2:
        if st.button("👁" if not ss.show_pw else "🙈", key="li_eye"):
            ss.show_pw = not ss.show_pw

    st.write("")
    if st.button("Log In"):
        u   = user_or_email.strip()
        rec = ss.users.get(u) or next(
            (v for v in ss.users.values() if v["email"].lower() == u.lower()), None)
        if rec and rec["password"] == password:
            ss.current_user = next(k for k, v in ss.users.items() if v is rec)
            ss.logged_in = True
            st.rerun()
        else:
            st.error("Galat username/email ya password")

    st.markdown("""
    <p class="switch-line">New here? <a href="?screen=signup">Create account</a></p>
    """, unsafe_allow_html=True)

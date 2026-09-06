import streamlit as st

st.set_page_config(page_title="HMF book", page_icon="🟢", layout="centered")

# ---------- SAFE RERUN (har Streamlit version par chalta hai) ----------
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# ---------- NAVIGATION HELPER ----------
def go_tab(t):
    st.session_state.tab = t

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "splash"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"
if "likes" not in st.session_state:
    st.session_state.likes = {}
if "tab" not in st.session_state:
    st.session_state.tab = "home"

# ---------- SAMPLE DATA ----------
POSTS = [
    {"id": "p1", "user": "hamza_official", "av": "😎", "grad": "linear-gradient(135deg,#00B074,#056839)", "emoji": "🌿",
     "cap": "Green vibes only! 🌿 Loving this new HMF app #hmfbook", "likes": 128},
    {"id": "p2", "user": "ayesha.99", "av": "🌸", "grad": "linear-gradient(135deg,#43e97b,#38f9d7)", "emoji": "🍃",
     "cap": "Nature walk today ☘️ beautiful weather mashallah", "likes": 96},
    {"id": "p3", "user": "bilal_plays", "av": "🎮", "grad": "linear-gradient(135deg,#0f3443,#34e89e)", "emoji": "🏆",
     "cap": "New high score in Quiz Rush — 2500 points! Can you beat me? 🏆", "likes": 214},
]

STORIES = [("Your story", "👤"), ("hamza", "😎"), ("ayesha.99", "🌸"),
           ("bilal", "🎮"), ("zara", "🌟"), ("usman", "🔥"), ("fatima", "🌻")]

USERS = [("hamza_official", "😎", "120K followers"), ("ayesha.99", "🌸", "89K followers"),
         ("bilal_plays", "🎮", "45K followers"), ("zara_x", "🌟", "230K followers")]

GAMES = [("🧠", "Quiz Rush", "Fast answers = coins!", "PLAY"),
         ("🔢", "2048", "Merge numbers, earn", "PLAY"),
         ("🎲", "Ludo Online", "Multiplayer (Module 7)", "SOON"),
         ("🎁", "Daily Bonus", "Free coins daily", "SOON")]

# ================= 1) SPLASH SCREEN =================
if st.session_state.page == "splash":

    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #00B074 0%, #056839 100%) !important; }
    header[data-testid="stHeader"], #MainMenu, footer { visibility: hidden !important; }
    .mid { display:flex; flex-direction:column; align-items:center; justify-content:center; height:70vh; text-align:center; }
    .logo { font-size:90px; font-weight:900; color:#fff; letter-spacing:4px; text-shadow:0 4px 14px rgba(0,0,0,.25); margin:0; }
    .sub { font-size:24px; color:rgba(255,255,255,.92); margin:5px 0 0; letter-spacing:2px; }
    div[data-testid="stButton"] > button, div.stButton > button {
        background:#fff !important; color:#00B074 !important; font-size:18px !important;
        font-weight:bold !important; padding:12px 45px !important;
        border-radius:30px !important; border:none !important;
        box-shadow:0 4px 15px rgba(0,0,0,.25) !important;
    }
    </style>
    <div class="mid"><h1 class="logo">HMF</h1><p class="sub">HMF book</p></div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        if st.button("Get Started", use_container_width=True):
            st.session_state.page = "auth"
            safe_rerun()


# ================= 2) LOGIN / SIGNUP =================
elif st.session_state.page == "auth":

    is_signup = st.session_state.auth_mode == "signup"
    title = "Create Account" if is_signup else "Welcome Back"
    subtitle = "Sign up to continue to HMF book" if is_signup else "Login to continue to HMF book"
    btn = "Sign Up" if is_signup else "Login"
    switch_txt = "New here? Create an account" if not is_signup else "Already have an account? Login"

    st.markdown("""
    <style>
    .stApp { background:#F3FAF6 !important; }
    header[data-testid="stHeader"], #MainMenu, footer { visibility:hidden !important; }
    .badge { background:linear-gradient(135deg,#00B074,#056839); display:inline-block;
             padding:18px 52px; border-radius:22px; box-shadow:0 6px 18px rgba(0,176,116,.35); }
    .badge h1 { color:#fff; font-size:36px; font-weight:900; letter-spacing:3px; margin:0; }
    .title { text-align:center; font-size:24px; font-weight:700; color:#222; margin:26px 0 4px; }
    .sub2 { text-align:center; color:#889; font-size:14px; margin:0 0 22px; }
    div[data-testid="stButton"] > button, div.stButton > button {
        background:#00B074 !important; color:#fff !important; font-weight:600 !important;
        border:none !important; border-radius:12px !important;
    }
    .or { text-align:center; color:#99a; font-size:13px; margin:20px 0 8px; }
    </style>
    <div style="text-align:center; margin-top:14px;"><div class="badge"><h1>HMF</h1></div></div>
    """, unsafe_allow_html=True)

    st.markdown(f"<h2 class='title'>{title}</h2><p class='sub2'>{subtitle}</p>", unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter username")
    if is_signup:
        st.text_input("Email", placeholder="Enter email")
    password = st.text_input("Password", type="password", placeholder="Enter password")

    if st.button(btn, use_container_width=True):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "app"
            safe_rerun()
        else:
            st.error("Username aur password dono likhein!")

    if st.button(switch_txt):
        st.session_state.auth_mode = "signup" if not is_signup else "login"
        safe_rerun()

    st.markdown("<p class='or'>Or continue with</p>", unsafe_allow_html=True)
    g, s, f = st.columns(3)
    g.button("Google", use_container_width=True)
    s.button("Snapchat", use_container_width=True)
    f.button("Facebook", use_container_width=True)


# ================= 3) MAIN APP (INSTAGRAM STYLE) =================
elif st.session_state.page == "app" and st.session_state.logged_in:

    st.markdown("""
    <style>
    .stApp { background:#fff !important; }
    header[data-testid="stHeader"], #MainMenu, footer { visibility:hidden !important; }
    .block-container { padding-top:0 !important; padding-bottom:40px !important; max-width:680px; }

    /* TOP NAVBAR */
    .topnav { position:sticky; top:0; z-index:1000; background:#fff; border-bottom:1px solid #efefef;
              display:flex; align-items:center; justify-content:space-between; padding:12px 14px; }
    .brand { color:#00B074; font-size:28px; font-weight:900; letter-spacing:1px;
             font-family:'Segoe Script','Brush Script MT',cursive; }
    .nico { font-size:22px; }

    /* STORIES */
    .stories { display:flex; gap:14px; padding:14px 8px; overflow-x:auto; border-bottom:1px solid #efefef; }
    .story { text-align:center; min-width:66px; }
    .ring { width:62px; height:62px; border-radius:50%; padding:3px;
            background:linear-gradient(45deg,#00B074,#7bed9f); margin:0 auto; }
    .ring.gray { background:#dbdbdb; }
    .ring-in { width:100%; height:100%; border-radius:50%; background:#fff;
               display:flex; align-items:center; justify-content:center; font-size:26px; }
    .sname { font-size:11px; color:#444; margin-top:4px; }

    /* POSTS */
    .post { border:1px solid #efefef; border-radius:14px; overflow:hidden; margin:20px auto; max-width:480px; }
    .phead { display:flex; align-items:center; gap:10px; padding:10px 12px; }
    .pav { width:34px; height:34px; border-radius:50%; background:linear-gradient(45deg,#00B074,#056839);
           color:#fff; display:flex; align-items:center; justify-content:center; font-size:15px; }
    .puser { font-weight:700; font-size:13px; }
    .pdots { margin-left:auto; color:#999; font-weight:bold; }
    .pimg { height:330px; display:flex; align-items:center; justify-content:center; font-size:85px; }
    .likes { margin:6px 8px 0; font-weight:600; font-size:13px; }
    .cap { margin:4px 8px 8px; font-size:13px; color:#262626; }

    /* plain buttons */
    div[data-testid="stButton"] > button, div.stButton > button {
        border:none !important; background:transparent !important; box-shadow:none !important;
        font-size:18px !important; padding:4px 10px !important; color:#000 !important;
    }
    div[data-testid="stButton"] > button:hover, div.stButton > button:hover {
        background:#f0f0f0 !important; border-radius:12px !important;
    }

    /* PROFILE */
    .banner { height:110px; background:linear-gradient(135deg,#00B074,#056839); border-radius:0 0 18px 18px; }
    .bigav { width:86px; height:86px; border-radius:50%; background:#fff; border:4px solid #00B074;
             margin:-45px auto 0; display:flex; align-items:center; justify-content:center;
             font-size:34px; font-weight:800; color:#00B074; }
    .pname { text-align:center; font-weight:800; font-size:18px; margin:8px 0 2px; }
    .pbio { text-align:center; color:#777; font-size:13px; margin:0 0 14px; }
    .stats { display:flex; justify-content:center; gap:34px; margin-bottom:16px; }
    .stats div { text-align:center; }
    .stats b { display:block; font-size:16px; }
    .stats span { font-size:12px; color:#888; }
    .pgrid { display:grid; grid-template-columns:repeat(3,1fr); gap:3px; }

    /* SEARCH */
    .sav { width:46px; height:46px; border-radius:50%; background:linear-gradient(45deg,#00B074,#056839);
           color:#fff; display:flex; align-items:center; justify-content:center; font-size:20px; }
    .sname2 { font-weight:700; font-size:14px; }
    .ssub { color:#999; font-size:12px; }

    /* GAMES */
    .gcard { border:1px solid #e3f0e9; border-radius:16px; padding:18px; text-align:center; background:#F6FCF9; }
    .gi { font-size:40px; }
    .gt { font-weight:800; margin:8px 0 2px; }
    .gs { color:#889; font-size:12px; margin-bottom:10px; }
    .gplay { background:#00B074; color:#fff; border-radius:20px; padding:6px 22px;
             font-size:13px; font-weight:700; display:inline-block; }
    .gsoon { background:#e3e7ea; color:#667; border-radius:20px; padding:6px 22px; font-size:13px; display:inline-block; }
    </style>
    """, unsafe_allow_html=True)

    # ---------- TOP NAVBAR ----------
    st.markdown("""
    <div class="topnav">
        <div class="brand">HMF</div>
        <div class="nico">❤️ &nbsp;&nbsp; ✉️ &nbsp;&nbsp; 🔔</div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- NAV BAR (buttons — ab 100% kaam karta hai) ----------
    nav_cols = st.columns(5)
    nav_data = [("🏠", "home"), ("🔍", "search"), ("➕", "create"), ("🎮", "games"), ("👤", "profile")]
    for col, (icon, t) in zip(nav_cols, nav_data):
        col.button(icon, key=f"nav_{t}", use_container_width=True,
                   on_click=go_tab, args=(t,))

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # ================= TAB: HOME =================
    if st.session_state.tab == "home":

        stories_html = ""
        for name, av in STORIES:
            gray = " gray" if name == "Your story" else ""
            stories_html += f'<div class="story"><div class="ring{gray}"><div class="ring-in">{av}</div></div><div class="sname">{name}</div></div>'
        st.markdown(f'<div class="stories">{stories_html}</div>', unsafe_allow_html=True)

        for p in POSTS:
            st.markdown(f"""
            <div class="post">
                <div class="phead">
                    <div class="pav">{p['av']}</div>
                    <span class="puser">{p['user']}</span>
                    <span class="pdots">···</span>
                </div>
                <div class="pimg" style="background:{p['grad']};">{p['emoji']}</div>
            </div>
            """, unsafe_allow_html=True)

            liked = st.session_state.likes.get(p["id"], False)
            b1, b2, b3, _ = st.columns([0.5, 0.5, 0.5, 4])
            if b1.button("❤️" if liked else "🤍", key=f"lk_{p['id']}"):
                st.session_state.likes[p["id"]] = not liked
                safe_rerun()
            b2.button("💬", key=f"cm_{p['id']}")
            b3.button("✈️", key=f"sh_{p['id']}")

            n = p["likes"] + (1 if liked else 0)
            st.markdown(f"<p class='likes'>{n} likes</p><p class='cap'><b>{p['user']}</b> {p['cap']}</p>", unsafe_allow_html=True)
            st.text_input("comment", key=f"cmt_{p['id']}", label_visibility="collapsed", placeholder="Add a comment…")

    # ================= TAB: SEARCH =================
    elif st.session_state.tab == "search":
        st.text_input("search", placeholder="🔍 Search", label_visibility="collapsed")
        for i, (name, av, sub) in enumerate(USERS):
            r1, r2, r3 = st.columns([0.15, 0.55, 0.3])
            r1.markdown(f'<div class="sav">{av}</div>', unsafe_allow_html=True)
            r2.markdown(f'<div class="sname2">{name}</div><div class="ssub">{sub}</div>', unsafe_allow_html=True)
            r3.button("Follow", key=f"fw_{i}")

    # ================= TAB: CREATE =================
    elif st.session_state.tab == "create":
        st.markdown("""
        <div style="text-align:center; padding:60px 0; color:#889;">
            <div style="font-size:50px;">➕</div>
            <h3>Create Post</h3>
            <p>Photo/Video upload — agla module</p>
        </div>
        """, unsafe_allow_html=True)

    # ================= TAB: GAMES =================
    elif st.session_state.tab == "games":
        cA, cB = st.columns(2)
        with cA:
            for gm in GAMES[:2]:
                badge = '<span class="gplay">▶ PLAY</span>' if gm[3] == "PLAY" else '<span class="gsoon">SOON</span>'
                st.markdown(f'<div class="gcard"><div class="gi">{gm[0]}</div><div class="gt">{gm[1]}</div><div class="gs">{gm[2]}</div>{badge}</div><div style="height:12px;"></div>', unsafe_allow_html=True)
        with cB:
            for gm in GAMES[2:]:
                badge = '<span class="gplay">▶ PLAY</span>' if gm[3] == "PLAY" else '<span class="gsoon">SOON</span>'
                st.markdown(f'<div class="gcard"><div class="gi">{gm[0]}</div><div class="gt">{gm[1]}</div><div class="gs">{gm[2]}</div>{badge}</div><div style="height:12px;"></div>', unsafe_allow_html=True)

    # ================= TAB: PROFILE =================
    elif st.session_state.tab == "profile":
        u = st.session_state.username or "user"
        initial = u[0].upper()
        st.markdown(f"""
        <div class="banner"></div>
        <div class="bigav">{initial}</div>
        <h2 class="pname">@{u}</h2>
        <p class="pbio">HMF book user 🌱 | Playing games & earning coins</p>
        <div class="stats">
            <div><b>9</b><span>Posts</span></div>
            <div><b>1,240</b><span>Followers</span></div>
            <div><b>356</b><span>Following</span></div>
        </div>
        """, unsafe_allow_html=True)

        e1, e2 = st.columns(2)
        e1.button("✏️ Edit Profile", use_container_width=True)
        if e2.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = "auth"
            safe_rerun()

        tiles = ["#00B074,#056839", "#43e97b,#38f9d7", "#0f3443,#34e89e",
                 "#11998e,#38ef7d", "#00B074,#7bed9f", "#056839,#a8ff78",
                 "#134e5e,#71b280", "#00B09B,#96C93D", "#1D976C,#93F9B9"]
        grid = "".join(f'<div style="aspect-ratio:1; background:linear-gradient(135deg,{t});"></div>' for t in tiles)
        st.markdown(f'<div class="pgrid">{grid}</div>', unsafe_allow_html=True)

# ---------- SAFETY ----------
else:
    st.session_state.page = "splash"
    safe_rerun()

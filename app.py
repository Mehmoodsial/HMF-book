import streamlit as st
import random

st.set_page_config(
    page_title="HMF book",
    page_icon="🟢",
    layout="centered",
)


# ---------- SAFE RERUN ----------
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


# ---------- SESSION STATE ----------
SS = st.session_state

defaults = {
    "page": "splash",
    "logged_in": False,
    "username": "",
    "email": "",
    "auth_mode": "login",
    "current_tab": "Home",
    "settings_page": "menu",
    "privacy_step": 0,
    "post_visibility": "Friends",
    "searchable": True,
    "two_factor": False,
    "login_alerts": False,
    "feed_sort": "Most Recent",
    "show_stories": True,
    "likes": {},
    "comments": {},
    "room_code": "",
    "joined": False,
    "dice": 0,
    "coins": 550,
    "display_name": "Hoor Jannat",
    "bio": "Living life one post at a time.",
    "withdraw_msg": "",
    "social_msg": "",
    "clear_cmt": "",
    "block_msg": "",
    "report_msg": "",
    "help_msg": "",
    "blocked": [],
    "reports": [],
    "tx_history": [],
    "dark_mode": False,
    "language": "English",
    "region": "Worldwide",
    "private_account": False,
    "activity_status": True,
    "notif": {
        "likes": True,
        "comments": True,
        "follows": True,
        "messages": True,
    },
}

for k, v in defaults.items():
    if k not in SS:
        SS[k] = v


# ---------- HELPERS ----------
def settings_back(key):
    if st.button("← Back to Settings", key=key):
        SS.settings_page = "menu"
        SS.privacy_step = 0
        safe_rerun()


def do_withdrawal():
    if SS.coins >= 100:
        SS.coins = SS.coins - 100
        entry = {
            "type": "Withdrawal Payout",
            "amount": "-100 coins",
            "time": "Just now",
        }
        SS.tx_history.insert(0, entry)
        SS.withdraw_msg = (
            "✅ Withdrawal request submitted! 100 coins deducted - "
            "processing within 3-5 business days."
        )
    else:
        SS.withdraw_msg = (
            "⚠️ Minimum 100 coins required for withdrawal!"
        )


# ---------- FEED DATA ----------
POSTS = [
    {
        "id": "p1",
        "user": "hoor_jannat",
        "ini": "HJ",
        "grad": "linear-gradient(45deg,#e6f7f0,#b3e6cc)",
        "txt": "🖼️ HMF Network Framework Live",
        "cap": "Framework switching logic is now fully integrated!",
        "likes": 128,
    },
    {
        "id": "p2",
        "user": "farrukh_m",
        "ini": "FM",
        "grad": "linear-gradient(45deg,#d1fae5,#a7f3d0)",
        "txt": "🎲 Ludo Night Tournament",
        "cap": "Tonight 8 PM - winner takes all coins!",
        "likes": 96,
    },
    {
        "id": "p3",
        "user": "hamza_official",
        "ini": "HA",
        "grad": "linear-gradient(45deg,#ecfdf5,#6ee7b7)",
        "txt": "🌿 Green Vibes Only",
        "cap": "Loving this new HMF book app!",
        "likes": 214,
    },
]

KNOWN_MEMBERS = [
    "hoor_jannat",
    "farrukh_m",
    "hamza_official",
    "zara_x",
    "ayesha.99",
    "bilal_plays",
]


# ---------- MAIN APP CSS (Light + Dark) ----------
def build_main_css(dark):
    if dark:
        APPBG = "#0f1110"
        CARDBG = "#1b1e1b"
        BORDERC = "#2a2e2a"
        TXT1 = "#eef1ee"
        TXT2 = "#9aa69a"
        LOGOC = "#00e08a"
    else:
        APPBG = "#f0f2f5"
        CARDBG = "#ffffff"
        BORDERC = "#e5e7eb"
        TXT1 = "#1f2937"
        TXT2 = "#4b5563"
        LOGOC = "#00B074"

    css = f"""
    <style>
    .stApp {{ background-color:{APPBG} !important; }}
    header[data-testid="stHeader"], #MainMenu, footer {{
        visibility:hidden !important; }}
    [data-testid="stToolbar"] {{ visibility:hidden !important; }}
    [data-testid="stStatusWidget"] {{ visibility:hidden !important; }}

    .block-container, [data-testid="block-container"] {{
        max-width:460px;
        margin:0 auto;
        background:{CARDBG};
        padding-top:0 !important;
        padding-bottom:30px !important;
        min-height:100vh;
        box-shadow:0 0 25px rgba(0,0,0,.12);
    }}

    .insta-header {{
        position:sticky;
        top:0;
        z-index:100;
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding:14px 18px;
        background:{CARDBG};
        border-bottom:1px solid {BORDERC};
    }}
    .brand-logo {{
        font-size:28px;
        font-weight:900;
        color:{LOGOC};
        letter-spacing:-1px;
    }}
    .nico {{ font-size:20px; }}

    .stories-container {{
        display:flex;
        gap:15px;
        padding:12px 15px;
        background:{CARDBG};
        border-bottom:1px solid {BORDERC};
        overflow-x:auto;
    }}
    .story-card {{
        display:flex;
        flex-direction:column;
        align-items:center;
        text-align:center;
        min-width:65px;
    }}
    .story-ring {{
        width:60px;
        height:60px;
        border-radius:50%;
        padding:2.5px;
        background:linear-gradient(135deg,#00B074 0%,#056839 100%);
        display:flex;
        align-items:center;
        justify-content:center;
    }}
    .story-img {{
        width:100%;
        height:100%;
        border-radius:50%;
        background:{CARDBG};
        border:2px solid {CARDBG};
        display:flex;
        align-items:center;
        justify-content:center;
        font-weight:bold;
        color:{TXT2};
        font-size:14px;
    }}
    .story-name {{
        font-size:11px;
        color:{TXT2};
        margin-top:4px;
        max-width:65px;
        overflow:hidden;
        text-overflow:ellipsis;
        white-space:nowrap;
    }}

    .post-card {{
        background:{CARDBG};
        margin-bottom:12px;
        border-bottom:1px solid {BORDERC};
    }}
    .post-header {{
        display:flex;
        align-items:center;
        padding:12px 15px;
    }}
    .post-avatar {{
        width:36px;
        height:36px;
        border-radius:50%;
        background:#00B074;
        color:#fff;
        display:flex;
        align-items:center;
        justify-content:center;
        font-weight:bold;
        margin-right:10px;
        font-size:13px;
    }}
    .post-username {{
        font-size:14px;
        font-weight:700;
        color:{TXT1};
    }}
    .post-image-placeholder {{
        width:100%;
        height:300px;
        background:#f3f4f6;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:16px;
    }}
    .likes-txt {{
        padding:8px 15px 2px;
        font-weight:600;
        font-size:13px;
        color:{TXT1};
        margin:0;
    }}
    .post-details {{
        padding:0 15px 10px 15px;
        font-size:14px;
        color:{TXT1};
        margin:0;
    }}

    .panel-header {{
        padding:18px;
        font-size:22px;
        font-weight:bold;
        color:{LOGOC};
        border-bottom:1px solid {BORDERC};
        text-align:center;
    }}

    .ludo-board-mock {{
        width:280px;
        height:280px;
        margin:30px auto;
        background:#f59e0b;
        border:10px solid #d97706;
        border-radius:20px;
        display:flex;
        align-items:center;
        justify-content:center;
        color:white;
        font-size:40px;
        font-weight:bold;
        box-shadow:0 10px 15px -3px rgba(0,0,0,0.1);
    }}

    .set-label {{
        font-weight:700;
        color:{TXT1};
        margin:14px 0 4px;
    }}
    .sec-label {{
        font-size:12px;
        font-weight:800;
        letter-spacing:1px;
        color:{TXT2};
        margin:18px 6px 8px;
    }}
    .privacy-card {{
        display:flex;
        gap:14px;
        align-items:center;
        background:rgba(0,176,116,0.10);
        border:1px solid #00B074;
        border-radius:14px;
        padding:14px 16px;
        margin:10px 0 4px;
    }}
    .privacy-card b {{ color:{TXT1}; font-size:15px; }}
    .privacy-card p {{ margin:2px 0 0; font-size:12px; color:{TXT2}; }}
    .member-chip {{
        display:inline-block;
        background:{CARDBG};
        border:1px solid {BORDERC};
        border-radius:20px;
        padding:4px 12px;
        margin:3px;
        font-size:12px;
        color:{TXT2};
    }}
    .session-row {{
        display:flex;
        align-items:center;
        gap:12px;
        padding:10px 4px;
        border-bottom:1px solid {BORDERC};
        font-size:13px;
        color:{TXT1};
    }}

    div[data-testid="stButton"] > button, div.stButton > button {{
        background:#00B074 !important;
        color:#fff !important;
        font-weight:600 !important;
        border:none !important;
        border-radius:12px !important;
    }}
    div[data-testid="stButton"] > button:hover,
    div.stButton > button:hover {{
        background:#056839 !important;
        color:#fff !important;
    }}
    </style>
    """

    if dark:
        css += """
        <style>
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea {{
            background:#242824 !important;
            color:#fff !important;
            border-color:#3a3f3a !important;
        }}
        [data-testid="stCheckbox"] label p,
        [data-testid="stRadio"] label p {{
            color:#e5e9e5 !important;
        }}
        [data-baseweb="select"] > div {{
            background:#242824 !important;
            color:#fff !important;
        }}
        hr {{ border-color:#2a2e2a !important; }}
        </style>
        """

    return css


# ================= 1) SPLASH SCREEN =================
if SS.page == "splash":

    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #00B074 0%, #056839 100%) !important;
        }
        header[data-testid="stHeader"], #MainMenu, footer {
            visibility:hidden !important;
        }
        [data-testid="stToolbar"] { visibility:hidden !important; }
        [data-testid="stStatusWidget"] { visibility:hidden !important; }
        .mid {
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;
            height:70vh;
            text-align:center;
        }
        .logo {
            font-size:90px;
            font-weight:900;
            color:#fff;
            letter-spacing:4px;
            text-shadow:0 4px 14px rgba(0,0,0,.25);
            margin:0;
        }
        .sub {
            font-size:24px;
            color:rgba(255,255,255,.92);
            margin:5px 0 0;
            letter-spacing:2px;
        }
        div[data-testid="stButton"] > button, div.stButton > button {
            background:#fff !important;
            color:#00B074 !important;
            font-size:18px !important;
            font-weight:bold !important;
            padding:12px 45px !important;
            border-radius:30px !important;
            border:none !important;
            box-shadow:0 4px 15px rgba(0,0,0,.25) !important;
        }
        </style>
        <div class="mid">
            <h1 class="logo">HMF</h1>
            <p class="sub">HMF book</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        if st.button("Get Started", use_container_width=True):
            SS.page = "auth"
            safe_rerun()


# ================= 2) LOGIN / SIGNUP =================
elif SS.page == "auth":

    is_signup = SS.auth_mode == "signup"

    if is_signup:
        title = "Create Account"
        subtitle = "Sign up to continue to HMF book"
        btn_label = "Sign Up"
        switch_txt = "Already have an account? Login"
    else:
        title = "Welcome Back"
        subtitle = "Login to continue to HMF book"
        btn_label = "Login"
        switch_txt = "New here? Create an account"

    st.markdown(
        """
        <style>
        .stApp { background:#F3FAF6 !important; }
        header[data-testid="stHeader"], #MainMenu, footer {
            visibility:hidden !important;
        }
        [data-testid="stToolbar"] { visibility:hidden !important; }
        [data-testid="stStatusWidget"] { visibility:hidden !important; }
        .badge {
            background:linear-gradient(135deg,#00B074,#056839);
            display:inline-block;
            padding:18px 52px;
            border-radius:22px;
            box-shadow:0 6px 18px rgba(0,176,116,.35);
        }
        .badge h1 {
            color:#fff;
            font-size:36px;
            font-weight:900;
            letter-spacing:3px;
            margin:0;
        }
        .title {
            text-align:center;
            font-size:24px;
            font-weight:700;
            color:#222;
            margin:26px 0 4px;
        }
        .sub2 {
            text-align:center;
            color:#889;
            font-size:14px;
            margin:0 0 22px;
        }
        div[data-testid="stButton"] > button, div.stButton > button {
            background:#00B074 !important;
            color:#fff !important;
            font-weight:600 !important;
            border:none !important;
            border-radius:12px !important;
        }
        .or {
            text-align:center;
            color:#99a;
            font-size:13px;
            margin:20px 0 8px;
        }
        </style>
        <div style="text-align:center; margin-top:14px;">
            <div class="badge"><h1>HMF</h1></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    head = f"<h2 class='title'>{title}</h2><p class='sub2'>{subtitle}</p>"
    st.markdown(head, unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter username")

    if is_signup:
        email = st.text_input("Email", placeholder="Enter email")
    else:
        email = SS.email

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password",
    )

    if st.button(btn_label, use_container_width=True):
        if username and password:
            SS.logged_in = True
            SS.username = username
            if email:
                SS.email = email
            SS.page = "app"
            safe_rerun()
        else:
            st.error("Please enter both username and password!")

    if st.button(switch_txt):
        if is_signup:
            SS.auth_mode = "login"
        else:
            SS.auth_mode = "signup"
        safe_rerun()

    st.markdown(
        "<p class='or'>Or continue with</p>",
        unsafe_allow_html=True,
    )

    g, s, f = st.columns(3)

    if g.button("Google", use_container_width=True):
        SS.social_msg = "Google sign-in will be available soon."
        safe_rerun()

    if s.button("Snapchat", use_container_width=True):
        SS.social_msg = "Snapchat login will be available soon."
        safe_rerun()

    if f.button("Facebook", use_container_width=True):
        SS.social_msg = "Facebook login will be available soon."
        safe_rerun()

    if SS.social_msg:
        st.info(SS.social_msg)


# ================= 3) MAIN APP =================
elif SS.page == "app" and SS.logged_in:

    st.markdown(build_main_css(SS.dark_mode), unsafe_allow_html=True)

    # ---------- TOP BAR ----------
    topbar = """
    <div class="insta-header">
        <div class="brand-logo">HMF book</div>
        <div class="nico">❤️ &nbsp; ✉️ &nbsp; 🔔</div>
    </div>
    """
    st.markdown(topbar, unsafe_allow_html=True)

    # ---------- QUICK ICON ROW ----------
    q1, q2, q3, q4, q5 = st.columns([0.6, 0.6, 0.6, 0.6, 1.6])

    if q1.button("⚙️", key="top_set", use_container_width=True,
                 help="Open Settings"):
        SS.current_tab = "Settings"
        safe_rerun()

    if q2.button("🔔", key="top_bell", use_container_width=True,
                 help="Notifications"):
        st.toast("You have 3 new notifications!")

    if q3.button("✉️", key="top_mail", use_container_width=True,
                 help="Messages"):
        st.toast("You have 2 new messages!")

    if q4.button("🌙", key="top_dark", use_container_width=True,
                 help="Toggle Dark Mode"):
        SS.dark_mode = not SS.dark_mode
        safe_rerun()

    if SS.current_tab == "Settings":
        q5.markdown(
            "<b style='color:#00B074;'>⚙️ Settings</b>",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

    # ================= TAB: HOME =================
    if SS.current_tab == "Home":

        if SS.show_stories:
            stories_html = """
            <div class="stories-container">
                <div class="story-card">
                    <div class="story-ring" style="background:#6b7280;">
                        <div class="story-img"
                             style="background-color:#056839;color:#fff;">+
                        </div>
                    </div>
                    <div class="story-name">Your Story</div>
                </div>
                <div class="story-card">
                    <div class="story-ring"><div class="story-img">HJ</div></div>
                    <div class="story-name">hoor_jannat</div>
                </div>
                <div class="story-card">
                    <div class="story-ring"><div class="story-img">FM</div></div>
                    <div class="story-name">farrukh_m</div>
                </div>
                <div class="story-card">
                    <div class="story-ring"><div class="story-img">ZX</div></div>
                    <div class="story-name">zara_x</div>
                </div>
                <div class="story-card">
                    <div class="story-ring"><div class="story-img">HA</div></div>
                    <div class="story-name">hamza</div>
                </div>
            </div>
            """
            st.markdown(stories_html, unsafe_allow_html=True)

        if SS.block_msg:
            st.success(SS.block_msg)
            SS.block_msg = ""

        visible_posts = []
        for p in POSTS:
            if p["user"].lower() not in SS.blocked:
                visible_posts.append(p)

        if SS.feed_sort == "Top Posts":
            visible_posts = sorted(
                visible_posts,
                key=lambda x: x["likes"],
                reverse=True,
            )
        else:
            visible_posts = list(reversed(visible_posts))

        hidden = len(POSTS) - len(visible_posts)

        if hidden > 0:
            st.info(
                "🚫 " + str(hidden) +
                " post(s) from blocked members are hidden."
            )

        if SS.clear_cmt:
            SS[SS.clear_cmt] = ""
            SS.clear_cmt = ""

        for p in visible_posts:

            post_html = f"""
            <div class="post-card">
                <div class="post-header">
                    <div class="post-avatar">{p['ini']}</div>
                    <div class="post-username">{p['user']}</div>
                </div>
                <div class="post-image-placeholder"
                     style="background:{p['grad']};
                            color:#056839;
                            font-weight:bold;">
                    {p['txt']}
                </div>
            </div>
            """
            st.markdown(post_html, unsafe_allow_html=True)

            liked = SS.likes.get(p["id"], False)

            a1, a2, a3, a4 = st.columns(4)

            like_icon = "❤️" if liked else "🤍"
            if a1.button(
                like_icon,
                key="lk_" + p["id"],
                use_container_width=True,
            ):
                SS.likes[p["id"]] = not liked
                safe_rerun()

            if a2.button(
                "💬",
                key="cm_" + p["id"],
                use_container_width=True,
            ):
                st.info("Type your comment in the box below.")

            if a3.button(
                "✈️",
                key="sh_" + p["id"],
                use_container_width=True,
            ):
                st.info("Post link copied!")

            if a4.button(
                "🚫",
                key="bl_" + p["id"],
                use_container_width=True,
            ):
                SS.blocked.append(p["user"].lower())
                SS.block_msg = (
                    "✅ @" + p["user"] + " has been blocked - "
                    "their posts will no longer appear in your feed."
                )
                safe_rerun()

            n = p["likes"]
            if liked:
                n = n + 1

            likes_html = (
                "<p class='likes-txt'>" + str(n) + " likes</p>"
                "<p class='post-details'><b>" + p["user"] +
                "</b> " + p["cap"] + "</p>"
            )
            st.markdown(likes_html, unsafe_allow_html=True)

            cmt = st.text_input(
                "comment",
                key="cmt_" + p["id"],
                placeholder="Add a comment...",
                label_visibility="collapsed",
            )

            if st.button("Post Comment", key="pc_" + p["id"]):
                if cmt.strip():
                    if p["id"] not in SS.comments:
                        SS.comments[p["id"]] = []
                    entry = "<b>" + SS.username + "</b> " + cmt
                    SS.comments[p["id"]].append(entry)
                    SS.clear_cmt = "cmt_" + p["id"]
                    safe_rerun()
                else:
                    st.warning("Comment cannot be empty!")

            for c in SS.comments.get(p["id"], []):
                cmt_html = (
                    "<p class='post-details' style='color:#6b7280;'>"
                    + c + "</p>"
                )
                st.markdown(cmt_html, unsafe_allow_html=True)

    # ================= TAB: LUDO =================
    elif SS.current_tab == "Ludo":

        st.markdown(
            '<div class="panel-header">🎲 HMF Ludo Club</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="ludo-board-mock"> LUDO </div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "🏆 Create Private Room Code",
            use_container_width=True,
        ):
            letters = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
            SS.room_code = "".join(random.choices(letters, k=6))
            safe_rerun()

        if SS.room_code:
            room_txt = (
                "Room Code: **" + SS.room_code +
                "** - share this code with your friends!"
            )
            st.success(room_txt)

        if st.button(
            "👥 Play with Online Friends",
            use_container_width=True,
        ):
            SS.joined = True
            safe_rerun()

        if SS.joined:
            st.info(
                "✅ You and 3 players have joined the table. "
                "Full multiplayer mode coming soon!"
            )

        if st.button("🎲 Roll Dice", use_container_width=True):
            SS.dice = random.randint(1, 6)
            if SS.dice == 6:
                SS.coins = SS.coins + 5
                entry = {
                    "type": "Ludo Dice Bonus",
                    "amount": "+5 coins",
                    "time": "Just now",
                }
                SS.tx_history.insert(0, entry)
            safe_rerun()

        if SS.dice:
            extra = ""
            if SS.dice == 6:
                extra = " - Six! +5 coins earned"
            dice_txt = (
                "<h3 style='text-align:center; color:#00B074;'>"
                "🎯 You rolled " + str(SS.dice) + extra +
                "</h3>"
            )
            st.markdown(dice_txt, unsafe_allow_html=True)

    # ================= TAB: PROFILE =================
    elif SS.current_tab == "Profile":

        st.markdown(
            '<div class="panel-header">👤 User Profile</div>',
            unsafe_allow_html=True,
        )
        st.info("Logged in as: **@" + SS.username + "**")

        initial = SS.username[:1].upper()

        profile_html = f"""
        <div style="text-align:center; margin:10px 0;">
            <div style="width:86px;height:86px;border-radius:50%;
                 background:linear-gradient(135deg,#00B074,#056839);
                 color:#fff;font-size:34px;font-weight:800;
                 display:flex;align-items:center;
                 justify-content:center;margin:0 auto;">
                 {initial}
            </div>
            <h3 style="margin:10px 0 2px;">{SS.display_name}</h3>
            <p style="color:#6b7280; font-size:13px; margin:0;">{SS.bio}</p>
            <p style="color:#6b7280; font-size:12px; margin:8px 0 0;">
                9 Posts &nbsp;•&nbsp; 1,240 Followers &nbsp;•&nbsp; 356 Following
            </p>
        </div>
        """
        st.markdown(profile_html, unsafe_allow_html=True)

        bal = "💰 Current Wallet Balance: **" + str(SS.coins) + " Coins**"
        st.success(bal)

        if st.button(
            "💳 Request Withdrawal",
            key="prof_wd",
            use_container_width=True,
        ):
            do_withdrawal()
            safe_rerun()

        if SS.withdraw_msg:
            wm = (
                "<p style='text-align:center; color:#056839;'>"
                + SS.withdraw_msg + "</p>"
            )
            st.markdown(wm, unsafe_allow_html=True)
            SS.withdraw_msg = ""

        p1, p2 = st.columns(2)

        if p1.button("⚙️ Open Settings", use_container_width=True):
            SS.current_tab = "Settings"
            SS.settings_page = "menu"
            safe_rerun()

        if p2.button("🚪 Logout", use_container_width=True):
            SS.logged_in = False
            SS.page = "auth"
            SS.current_tab = "Home"
            safe_rerun()

    # ================= TAB: SETTINGS & PRIVACY =================
    elif SS.current_tab == "Settings":

        # ---------- SETTINGS MENU ----------
        if SS.settings_page == "menu":

            st.markdown(
                '<div class="panel-header">⚙️ Settings & Privacy</div>',
                unsafe_allow_html=True,
            )
            st.caption("@" + SS.username + " - Manage your account")

            # Privacy Checkup banner
            st.markdown(
                """
                <div class='privacy-card'>
                    <div style='font-size:28px;'>🛡️</div>
                    <div>
                        <b>Privacy Checkup</b>
                        <p>Review who can see your posts
                        and manage your privacy settings.</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                "🛡️ Get Started",
                key="privacy_start",
                use_container_width=True,
            ):
                SS.settings_page = "privacy"
                SS.privacy_step = 0
                safe_rerun()

            # ----- ACCOUNT -----
            st.markdown(
                "<p class='sec-label'>ACCOUNT</p>",
                unsafe_allow_html=True,
            )
            if st.button(
                "📋 Personal and Account Information   ›",
                key="m_personal",
                use_container_width=True,
            ):
                SS.settings_page = "personal"
                safe_rerun()

            if st.button(
                "🔐 Password and Security   ›",
                key="m_password",
                use_container_width=True,
            ):
                SS.settings_page = "password"
                safe_rerun()

            if st.button(
                "💰 Payments and Wallet   ›",
                key="m_payments",
                use_container_width=True,
            ):
                SS.settings_page = "payments"
                safe_rerun()

            # ----- PREFERENCES -----
            st.markdown(
                "<p class='sec-label'>PREFERENCES</p>",
                unsafe_allow_html=True,
            )
            if st.button(
                "📰 News Feed   ›",
                key="m_feed",
                use_container_width=True,
            ):
                SS.settings_page = "feed"
                safe_rerun()

            if st.button(
                "🔔 Notifications   ›",
                key="m_notif",
                use_container_width=True,
            ):
                SS.settings_page = "notifications"
                safe_rerun()

            if st.button(
                "🌐 Language and Region   ›",
                key="m_lang",
                use_container_width=True,
            ):
                SS.settings_page = "language"
                safe_rerun()

            # ----- PRIVACY -----
            st.markdown(
                "<p class='sec-label'>PRIVACY</p>",
                unsafe_allow_html=True,
            )
            if st.button(
                "🚫 Blocked Members   ›",
                key="m_blocked",
                use_container_width=True,
            ):
                SS.settings_page = "blocked"
                safe_rerun()

            if st.button(
                "⚠️ Your Reports   ›",
                key="m_reports",
                use_container_width=True,
            ):
                SS.settings_page = "reports"
                safe_rerun()

            # ----- SUPPORT -----
            st.markdown(
                "<p class='sec-label'>SUPPORT</p>",
                unsafe_allow_html=True,
            )
            if st.button(
                "❓ Help Center   ›",
                key="m_help",
                use_container_width=True,
            ):
                SS.settings_page = "help"
                safe_rerun()

            if st.button(
                "ℹ️ About   ›",
                key="m_about",
                use_container_width=True,
            ):
                SS.settings_page = "about"
                safe_rerun()

            # ----- LOGOUT -----
            st.markdown(
                "<div style='height:12px;'></div>",
                unsafe_allow_html=True,
            )
            if st.button(
                "🚪 Logout",
                key="m_logout",
                use_container_width=True,
            ):
                SS.logged_in = False
                SS.page = "auth"
                SS.current_tab = "Home"
                safe_rerun()

        # ---------- SUB-PAGE: PERSONAL INFO ----------
        elif SS.settings_page == "personal":

            settings_back("bk_personal")
            st.markdown(
                '<div class="panel-header">📋 Personal and Account Information</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                "<p class='set-label'>Account Details</p>",
                unsafe_allow_html=True,
            )

            st.text_input(
                "Username",
                value=SS.username,
                disabled=True,
                key="pi_user",
            )
            st.text_input(
                "Email",
                value=SS.email if SS.email else "user@hmfbook.com",
                key="pi_email",
            )
            dn = st.text_input(
                "Display Name",
                value=SS.display_name,
                key="st_dn",
            )
            bio = st.text_input("Bio", value=SS.bio, key="st_bio")

            if st.button(
                "💾 Save Changes",
                key="st_save",
                use_container_width=True,
            ):
                SS.display_name = dn
                SS.bio = bio
                st.success("Profile saved successfully!")

            st.markdown("---")
            st.markdown(
                "<p class='set-label'>⚠️ Danger Zone</p>",
                unsafe_allow_html=True,
            )

            del_chk = st.checkbox(
                "I want to delete my account",
                key="del_chk",
            )

            if del_chk:
                if st.button(
                    "🗑️ Delete My Account Permanently",
                    key="del_btn",
                    use_container_width=True,
                ):
                    SS.logged_in = False
                    SS.page = "splash"
                    SS.username = ""
                    safe_rerun()

        # ---------- SUB-PAGE: PASSWORD & SECURITY ----------
        elif SS.settings_page == "password":

            settings_back("bk_password")
            st.markdown(
                '<div class="panel-header">🔐 Password and Security</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                "<p class='set-label'>Change Password</p>",
                unsafe_allow_html=True,
            )
            cur_pw = st.text_input(
                "Current Password",
                type="password",
                key="cur_pw",
            )
            new_pw = st.text_input(
                "New Password",
                type="password",
                key="new_pw",
            )
            conf_pw = st.text_input(
                "Confirm New Password",
                type="password",
                key="conf_pw",
            )

            if st.button(
                "🔐 Update Password",
                key="pw_btn",
                use_container_width=True,
            ):
                if cur_pw and new_pw:
                    if new_pw == conf_pw:
                        st.success("Password updated successfully!")
                    else:
                        st.warning("New passwords do not match!")
                else:
                    st.warning("Please fill in the password fields!")

            st.markdown(
                "<p class='set-label'>Security Settings</p>",
                unsafe_allow_html=True,
            )
            SS.two_factor = st.checkbox(
                "🔑 Two-Factor Authentication (2FA)",
                value=SS.two_factor,
                key="tf_chk",
            )
            SS.login_alerts = st.checkbox(
                "📩 Login Alerts - notify me on new logins",
                value=SS.login_alerts,
                key="la_chk",
            )

            st.markdown(
                "<p class='set-label'>Where You're Logged In</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                <div class="session-row">💻 <div>
                <b>Windows PC</b> - Chrome<br>
                <span style="color:#00B074;">Active now</span></div></div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                <div class="session-row">📱 <div>
                <b>Samsung Galaxy</b> - HMF app<br>
                <span style="color:#9ca3af;">2 hours ago</span></div></div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                "🚪 Log Out of All Sessions",
                key="logout_all",
                use_container_width=True,
            ):
                st.success("You have been logged out of other sessions!")

        # ---------- SUB-PAGE: PAYMENTS & WALLET ----------
        elif SS.settings_page == "payments":

            settings_back("bk_payments")
            st.markdown(
                '<div class="panel-header">💰 Payments and Wallet</div>',
                unsafe_allow_html=True,
            )

            bal = "💰 Current Balance: **" + str(SS.coins) + " Coins**"
            st.success(bal)

            if st.button(
                "💳 Request Payout",
                key="pay_wd",
                use_container_width=True,
            ):
                do_withdrawal()
                safe_rerun()

            if SS.withdraw_msg:
                st.info(SS.withdraw_msg)
                SS.withdraw_msg = ""

            st.markdown(
                "<p class='set-label'>📜 Transaction History</p>",
                unsafe_allow_html=True,
            )
            if SS.tx_history:
                for i, t in enumerate(SS.tx_history):
                    h1, h2, h3 = st.columns([0.5, 0.3, 0.2])
                    h1.markdown("<b>" + t["type"] + "</b>",
                                unsafe_allow_html=True)
                    h2.markdown(t["amount"])
                    h3.caption(t["time"])
            else:
                st.caption(
                    "No transactions yet. "
                    "Play games and withdraw to see history here."
                )

            st.markdown(
                "<p class='set-label'>➕ Add Coins</p>",
                unsafe_allow_html=True,
            )
            st.caption(
                "Coin purchases coming soon. "
                "Earn coins by playing games and winning matches!"
            )

        # ---------- SUB-PAGE: NEWS FEED ----------
        elif SS.settings_page == "feed":

            settings_back("bk_feed")
            st.markdown(
                '<div class="panel-header">📰 News Feed Preferences</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                "<p class='set-label'>Feed Order</p>",
                unsafe_allow_html=True,
            )
            SS.feed_sort = st.radio(
                "Sort your feed by:",
                ["Most Recent", "Top Posts"],
                index=0 if SS.feed_sort == "Most Recent" else 1,
                key="feed_sort_radio",
            )

            st.markdown(
                "<p class='set-label'>Feed Content</p>",
                unsafe_allow_html=True,
            )
            SS.show_stories = st.checkbox(
                "📱 Show Stories row",
                value=SS.show_stories,
                key="stories_chk",
            )

            info = (
                "🚫 Posts from " + str(len(SS.blocked)) +
                " blocked member(s) are hidden from your feed."
            )
            st.caption(info)
            st.caption("Changes are saved automatically.")

        # ---------- SUB-PAGE: NOTIFICATIONS ----------
        elif SS.settings_page == "notifications":

            settings_back("bk_notif")
            st.markdown(
                '<div class="panel-header">🔔 Notifications</div>',
                unsafe_allow_html=True,
            )

            SS.notif["likes"] = st.checkbox(
                "❤️ Likes",
                value=SS.notif["likes"],
                key="ntf_l",
            )
            SS.notif["comments"] = st.checkbox(
                "💬 Comments",
                value=SS.notif["comments"],
                key="ntf_c",
            )
            SS.notif["follows"] = st.checkbox(
                "👥 New Followers",
                value=SS.notif["follows"],
                key="ntf_f",
            )
            SS.notif["messages"] = st.checkbox(
                "✉️ Messages",
                value=SS.notif["messages"],
                key="ntf_m",
            )

            if st.button(
                "🔔 Test Notification",
                key="ntf_test",
                use_container_width=True,
            ):
                on = []
                for k, v in SS.notif.items():
                    if v:
                        on.append(k)
                if on:
                    joined = ", ".join(on)
                    st.info(
                        "🔔 Demo: '@hoor_jannat liked your post!' "
                        "(On: " + joined + ")"
                    )
                else:
                    st.warning("All notifications are off!")

        # ---------- SUB-PAGE: LANGUAGE & REGION ----------
        elif SS.settings_page == "language":

            settings_back("bk_lang")
            st.markdown(
                '<div class="panel-header">🌐 Language and Region</div>',
                unsafe_allow_html=True,
            )

            lang = st.radio(
                "App Language:",
                ["English", "Urdu"],
                index=0 if SS.language == "English" else 1,
                key="lang_radio",
            )
            SS.language = lang

            regions = [
                "Worldwide",
                "Pakistan",
                "United Arab Emirates",
                "United Kingdom",
                "United States",
                "Saudi Arabia",
            ]
            if SS.region in regions:
                r_index = regions.index(SS.region)
            else:
                r_index = 0
            SS.region = st.selectbox(
                "Region:",
                regions,
                index=r_index,
                key="region_sel",
            )
            st.caption("Language and region are saved automatically.")

        # ---------- SUB-PAGE: PRIVACY CHECKUP ----------
        elif SS.settings_page == "privacy":

            settings_back("bk_privacy")
            st.markdown(
                '<div class="panel-header">🛡️ Privacy Checkup</div>',
                unsafe_allow_html=True,
            )

            prog = min(SS.privacy_step / 4, 1.0)
            st.progress(prog)

            if SS.privacy_step == 0:
                st.markdown(
                    "Take a minute to review your key privacy settings "
                    "and make sure you share only what you want."
                )
                st.info("🔒 Your data is private by default.")
                if st.button(
                    "🚀 Get Started",
                    key="pc_start",
                    use_container_width=True,
                ):
                    SS.privacy_step = 1
                    safe_rerun()

            elif SS.privacy_step == 1:
                st.markdown(
                    "<p class='set-label'>Step 1 of 3 - Who can see your posts?</p>",
                    unsafe_allow_html=True,
                )
                options = ["Public", "Friends", "Only Me"]
                SS.post_visibility = st.radio(
                    "Post visibility:",
                    options,
                    index=options.index(SS.post_visibility),
                    key="vis_radio",
                )
                if st.button(
                    "Next →",
                    key="pc_next1",
                    use_container_width=True,
                ):
                    SS.privacy_step = 2
                    safe_rerun()

            elif SS.privacy_step == 2:
                st.markdown(
                    "<p class='set-label'>Step 2 of 3 - Review blocked members</p>",
                    unsafe_allow_html=True,
                )
                if SS.blocked:
                    for u in SS.blocked:
                        st.markdown("🚫 **@" + u + "**")
                else:
                    st.caption("No one is blocked. Great job!")
                if st.button(
                    "Next →",
                    key="pc_next2",
                    use_container_width=True,
                ):
                    SS.privacy_step = 3
                    safe_rerun()

            elif SS.privacy_step == 3:
                st.markdown(
                    "<p class='set-label'>Step 3 of 3 - How people can find you</p>",
                    unsafe_allow_html=True,
                )
                SS.searchable = st.checkbox(
                    "Allow people to search for your profile",
                    value=SS.searchable,
                    key="search_chk",
                )
                SS.activity_status = st.checkbox(
                    "Show your online status",
                    value=SS.activity_status,
                    key="act_chk2",
                )
                if st.button(
                    "Finish Checkup ✓",
                    key="pc_finish",
                    use_container_width=True,
                ):
                    SS.privacy_step = 4
                    safe_rerun()

            else:
                st.success("🎉 Privacy Checkup complete!")
                srch = "Yes" if SS.searchable else "No"
                act = "Visible" if SS.activity_status else "Hidden"
                st.markdown(
                    "✅ Post visibility: **" + SS.post_visibility + "**\n\n"
                    "✅ Blocked members: **" + str(len(SS.blocked)) + "**\n\n"
                    "✅ Searchable: **" + srch + "**\n\n"
                    "✅ Activity status: **" + act + "**"
                )
                if st.button(
                    "Done",
                    key="pc_done",
                    use_container_width=True,
                ):
                    SS.settings_page = "menu"
                    SS.privacy_step = 0
                    safe_rerun()

        # ---------- SUB-PAGE: BLOCKED MEMBERS ----------
        elif SS.settings_page == "blocked":

            settings_back("bk_blocked")
            st.markdown(
                '<div class="panel-header">🚫 Blocked Members</div>',
                unsafe_allow_html=True,
            )

            if SS.block_msg:
                st.success(SS.block_msg)
                SS.block_msg = ""

            st.markdown(
                "<p class='set-label'>Member IDs (copy the exact ID):</p>",
                unsafe_allow_html=True,
            )
            chips = ""
            for m in KNOWN_MEMBERS:
                chips += "<span class='member-chip'>👤 @" + m + "</span>"
            st.markdown(chips, unsafe_allow_html=True)

            st.markdown(
                "<p class='set-label'>Enter username/ID to block:</p>",
                unsafe_allow_html=True,
            )
            block_input = st.text_input(
                "Username / ID",
                key="block_input",
                placeholder="e.g. farrukh_m",
            )

            if st.button(
                "🚫 Block This Member",
                key="block_btn",
                use_container_width=True,
            ):
                u = block_input.strip().lower()
                if not u:
                    st.warning("Please enter an ID first!")
                elif u == SS.username.lower():
                    st.warning("You cannot block your own ID!")
                elif u in SS.blocked:
                    st.warning("This member is already blocked!")
                else:
                    SS.blocked.append(u)
                    SS.block_msg = (
                        "✅ @" + u + " has been blocked - "
                        "their posts and comments will no longer appear."
                    )
                    safe_rerun()

            st.markdown(
                "<p class='set-label'>🚫 Blocked List:</p>",
                unsafe_allow_html=True,
            )
            if SS.blocked:
                for i, u in enumerate(SS.blocked):
                    bc1, bc2 = st.columns([0.65, 0.35])
                    bc1.markdown("**🚫 @" + u + "**")
                    if bc2.button(
                        "✅ Unblock",
                        key="ub_" + str(i),
                        use_container_width=True,
                    ):
                        SS.blocked.remove(u)
                        SS.block_msg = (
                            "@" + u + " has been unblocked - "
                            "their posts will reappear in your feed."
                        )
                        safe_rerun()
            else:
                st.caption(
                    "No members are blocked yet. "
                    "You can also block directly from the feed."
                )

        # ---------- SUB-PAGE: REPORTS ----------
        elif SS.settings_page == "reports":

            settings_back("bk_reports")
            st.markdown(
                '<div class="panel-header">⚠️ Report a Member</div>',
                unsafe_allow_html=True,
            )

            if SS.report_msg:
                st.success(SS.report_msg)
                SS.report_msg = ""

            rep_id = st.text_input(
                "Member ID to report",
                key="rep_id",
                placeholder="e.g. bilal_plays",
            )
            reasons = [
                "Harassment / Bullying",
                "Abusive Language",
                "Spam or Fake Posts",
                "Fake Account",
                "Scam / Fraud",
                "Other",
            ]
            reason = st.selectbox("Reason", reasons, key="rep_reason")
            rep_detail = st.text_area(
                "Details (optional)",
                key="rep_detail",
                height=80,
            )

            if st.button(
                "🚩 Submit Report",
                key="rep_btn",
                use_container_width=True,
            ):
                r = rep_id.strip().lower()
                if r:
                    report = {
                        "user": r,
                        "reason": reason,
                        "detail": rep_detail,
                    }
                    SS.reports.append(report)
                    SS.report_msg = (
                        "✅ Report against @" + r + " submitted - "
                        "our team will review it within 24 hours."
                    )
                    safe_rerun()
                else:
                    st.warning("Please enter a member ID!")

            if SS.reports:
                st.markdown(
                    "<p class='set-label'>📋 Your Reports:</p>",
                    unsafe_allow_html=True,
                )
                for i, r in enumerate(SS.reports):
                    line = (
                        "<p style='font-size:12px; color:#6b7280;'>"
                        + str(i + 1) + ". 🚩 <b>@" + r["user"] +
                        "</b> - " + r["reason"] + "</p>"
                    )
                    st.markdown(line, unsafe_allow_html=True)

        # ---------- SUB-PAGE: HELP CENTER ----------
        elif SS.settings_page == "help":

            settings_back("bk_help")
            st.markdown(
                '<div class="panel-header">❓ Help Center</div>',
                unsafe_allow_html=True,
            )

            st.markdown("**❓ Frequently Asked Questions:**")
            st.markdown(
                "• **How do I earn coins?** - Play games, daily login, and win matches\n"
                "• **How do withdrawals work?** - Request from Payments with 100+ coins\n"
                "• **Someone is bothering me?** - Privacy → Blocked Members\n"
                "• **How do I report someone?** - Privacy → Your Reports"
            )

            bug = st.text_area(
                "🐞 Describe the bug or issue:",
                key="bug_txt",
                height=80,
            )

            if st.button(
                "✉️ Send to Support",
                key="sup_btn",
                use_container_width=True,
            ):
                if bug.strip():
                    SS.help_msg = (
                        "✅ Your message has been sent to our support team - "
                        "you will receive a reply within 24-48 hours."
                    )
                else:
                    SS.help_msg = "⚠️ Please describe your issue first."
                safe_rerun()

            if SS.help_msg:
                st.info(SS.help_msg)
                SS.help_msg = ""

        # ---------- SUB-PAGE: ABOUT ----------
        elif SS.settings_page == "about":

            settings_back("bk_about")
            st.markdown(
                '<div class="panel-header">ℹ️ About</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                "**HMF book** v1.3.0 🟢\n\n"
                "Social feed • Games • Coins • Live streaming (coming soon)\n\n"
                "© 2025 HMF - All rights reserved."
            )

    # ---------- BOTTOM NAVIGATION ----------
    hr_html = (
        "<hr style='border:none; border-top:1px solid #e5e7eb; "
        "margin:25px 0 10px;'>"
    )
    st.markdown(hr_html, unsafe_allow_html=True)

    n1, n2, n3, n4 = st.columns(4)

    if n1.button("🏠 Home", use_container_width=True):
        SS.current_tab = "Home"
        safe_rerun()

    if n2.button("🎮 Ludo", use_container_width=True):
        SS.current_tab = "Ludo"
        safe_rerun()

    if n3.button("👤 Profile", use_container_width=True):
        SS.current_tab = "Profile"
        safe_rerun()

    if n4.button("⚙️ Settings", use_container_width=True):
        SS.current_tab = "Settings"
        SS.settings_page = "menu"
        safe_rerun()


# ---------- SAFETY ----------
else:
    SS.page = "splash"
    safe_rerun()

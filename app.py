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
    "auth_mode": "login",
    "current_tab": "Home",
    "likes": {},
    "comments": {},
    "room_code": "",
    "joined": False,
    "dice": 0,
    "coins": 550,
    "display_name": "Hoor Jannat",
    "bio": "Building my premium minimalist layer apps.",
    "withdraw_msg": "",
    "social_msg": "",
    "clear_cmt": "",
    "block_msg": "",
    "report_msg": "",
    "help_msg": "",
    "blocked": [],
    "reports": [],
    "dark_mode": False,
    "language": "English",
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
        [data-testid="stExpander"] {{
            background:#1b1e1b !important;
            border:1px solid #2a2e2a !important;
            border-radius:10px;
        }}
        [data-testid="stExpander"] summary p {{
            color:#fff !important;
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
        st.text_input("Email", placeholder="Enter email")

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password",
    )

    if st.button(btn_label, use_container_width=True):
        if username and password:
            SS.logged_in = True
            SS.username = username
            SS.page = "app"
            safe_rerun()
        else:
            st.error("Username aur password dono likhein!")

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
        SS.social_msg = "Google sign-in Module 10 mein OAuth se add hoga."
        safe_rerun()

    if s.button("Snapchat", use_container_width=True):
        SS.social_msg = "Snapchat login agli modules mein add hoga."
        safe_rerun()

    if f.button("Facebook", use_container_width=True):
        SS.social_msg = "Facebook OAuth setup Module 10 mein add hoga."
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

    # ================= TAB: HOME =================
    if SS.current_tab == "Home":

        stories_html = """
        <div class="stories-container">
            <div class="story-card">
                <div class="story-ring" style="background:#6b7280;">
                    <div class="story-img" style="background-color:#056839;color:#fff;">+</div>
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

        hidden = len(POSTS) - len(visible_posts)

        if hidden > 0:
            st.info(
                "🚫 " + str(hidden) +
                " blocked member ki post(s) chhupa di gayi hain."
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
                st.info("Neeche comment box se apna comment likhein.")

            if a3.button(
                "✈️",
                key="sh_" + p["id"],
                use_container_width=True,
            ):
                st.info("Post link copy ho gaya (demo)!")

            if a4.button(
                "🚫",
                key="bl_" + p["id"],
                use_container_width=True,
            ):
                SS.blocked.append(p["user"].lower())
                SS.block_msg = (
                    "✅ @" + p["user"] + " block ho gaya - "
                    "ab uski posts feed mein nahi dikhengi."
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
                    st.warning("Comment khali hai!")

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
                "** - is code se dost room join karenge!"
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
                "✅ Aap + 3 players table par join ho gaye. "
                "Real game Module 7 mein aayega."
            )

        if st.button("🎲 Roll Dice", use_container_width=True):
            SS.dice = random.randint(1, 6)
            if SS.dice == 6:
                SS.coins = SS.coins + 5
            safe_rerun()

        if SS.dice:
            extra = ""
            if SS.dice == 6:
                extra = " - Chhakka! +5 coins milay"
            dice_txt = (
                "<h3 style='text-align:center; color:#00B074;'>"
                "🎯 Aapne " + str(SS.dice) + " nikala" + extra +
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
            "💳 Request Withdrawal Cashout",
            use_container_width=True,
        ):
            if SS.coins >= 100:
                SS.coins = SS.coins - 100
                SS.withdraw_msg = (
                    "✅ Withdrawal request submit! 100 coins kat gaye - "
                    "3-5 din mein process hoga."
                )
            else:
                SS.withdraw_msg = (
                    "⚠️ Withdrawal ke liye kam se kam 100 coins chahiye!"
                )
            safe_rerun()

        if SS.withdraw_msg:
            wm = (
                "<p style='text-align:center; color:#056839;'>"
                + SS.withdraw_msg + "</p>"
            )
            st.markdown(wm, unsafe_allow_html=True)

        p1, p2 = st.columns(2)

        if p1.button("⚙️ Settings kholein", use_container_width=True):
            SS.current_tab = "Settings"
            safe_rerun()

        if p2.button("🚪 Logout", use_container_width=True):
            SS.logged_in = False
            SS.page = "auth"
            SS.current_tab = "Home"
            safe_rerun()

    # ================= TAB: SETTINGS =================
    elif SS.current_tab == "Settings":

        st.markdown(
            '<div class="panel-header">⚙️ Settings</div>',
            unsafe_allow_html=True,
        )
        st.caption("@" + SS.username + " - HMF book Settings")

        if SS.block_msg:
            st.success(SS.block_msg)
            SS.block_msg = ""

        if SS.report_msg:
            st.success(SS.report_msg)
            SS.report_msg = ""

        # ---------- ACCOUNT ----------
        with st.expander("👤 Account"):

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
                st.success("Profile saved ✅")

            st.markdown("---")
            st.markdown(
                "<p class='set-label'>⚠️ Danger Zone</p>",
                unsafe_allow_html=True,
            )

            del_chk = st.checkbox(
                "Main apna account delete karna chahta hoon",
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

        # ---------- PRIVACY & SECURITY ----------
        with st.expander("🔒 Privacy & Security"):

            SS.private_account = st.checkbox(
                "🔒 Private Account - sirf followers posts dekh sakte hain",
                value=SS.private_account,
                key="priv_chk",
            )
            SS.activity_status = st.checkbox(
                "🟢 Activity Status dikhayein (Online status)",
                value=SS.activity_status,
                key="act_chk",
            )

            st.markdown("---")
            st.markdown(
                "<p class='set-label'>🔐 Change Password</p>",
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

            if st.button(
                "🔐 Update Password",
                key="pw_btn",
                use_container_width=True,
            ):
                if cur_pw and new_pw:
                    st.success(
                        "Password update ho gaya! (Real hashing Module 10 mein)"
                    )
                else:
                    st.warning("Dono fields bharin!")

        # ---------- NOTIFICATIONS ----------
        with st.expander("🔔 Notifications"):

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
                        "🔔 Demo: '@hoor_jannat ne aapki post like ki!' "
                        "(On: " + joined + ")"
                    )
                else:
                    st.warning("Sab notifications off hain!")

        # ---------- BLOCKED MEMBERS ----------
        with st.expander("🚫 Blocked Members - Tang karne walon ko block karein"):

            st.markdown(
                "<p class='set-label'>Members ki IDs (check kar ke exact ID likhein):</p>",
                unsafe_allow_html=True,
            )

            chips = ""
            for m in KNOWN_MEMBERS:
                chips += "<span class='member-chip'>👤 @" + m + "</span>"
            st.markdown(chips, unsafe_allow_html=True)

            st.markdown(
                "<p class='set-label'>Block karne ke liye username/ID likhein:</p>",
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
                    st.warning("Pehle ID likhein!")
                elif u == SS.username.lower():
                    st.warning("Apni khud ki ID block nahi kar sakte!")
                elif u in SS.blocked:
                    st.warning("Ye member pehle se blocked hai!")
                else:
                    SS.blocked.append(u)
                    SS.block_msg = (
                        "✅ @" + u + " block kar diya gaya - "
                        "ab uski posts/comments feed mein nahi dikhenge."
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
                            "@" + u + " unblock ho gaya - "
                            "ab uski posts wapas feed mein dikhengi."
                        )
                        safe_rerun()
            else:
                st.caption(
                    "Abhi koi member blocked nahi hai. "
                    "Feed par 🚫 button se bhi block kar sakte hain."
                )

        # ---------- REPORT MEMBER ----------
        with st.expander("⚠️ Report a Member - Complaint karein"):

            rep_id = st.text_input(
                "Jis member ki shikayat hai uski ID",
                key="rep_id",
                placeholder="e.g. bilal_plays",
            )

            reasons = [
                "Tang karna / Harassment",
                "Gali / Abusive language",
                "Spam ya fake posts",
                "Fake account",
                "Scam / Fraud",
                "Other",
            ]
            reason = st.selectbox("Reason", reasons, key="rep_reason")

            rep_detail = st.text_area(
                "Detail likhein (optional)",
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
                        "✅ Report against @" + r + " submit ho gayi - "
                        "admin 24 ghante mein review karega."
                    )
                    safe_rerun()
                else:
                    st.warning("Member ki ID likhein!")

            if SS.reports:
                st.markdown(
                    "<p class='set-label'>📋 Aapki Reports:</p>",
                    unsafe_allow_html=True,
                )
                for i, r in enumerate(SS.reports):
                    line = (
                        "<p style='font-size:12px; color:#6b7280;'>"
                        + str(i + 1) + ". 🚩 <b>@" + r["user"] +
                        "</b> - " + r["reason"] + "</p>"
                    )
                    st.markdown(line, unsafe_allow_html=True)

        # ---------- APPEARANCE ----------
        with st.expander("🌙 Appearance"):

            new_dark = st.checkbox(
                "🌙 Dark Mode on karein",
                value=SS.dark_mode,
                key="dark_chk",
            )

            if new_dark != SS.dark_mode:
                SS.dark_mode = new_dark
                safe_rerun()

            st.caption(
                "Instagram jaisa dark theme - poori app ka rang badal jata hai!"
            )

        # ---------- LANGUAGE ----------
        with st.expander("🌐 Language"):

            lang = st.radio(
                "Apni pasand ki zaban chunein:",
                ["English", "Urdu"],
                index=0 if SS.language == "English" else 1,
                key="lang_radio",
                horizontal=True,
            )

            if lang == "English":
                SS.language = "English"
                st.caption("English selected.")
            else:
                SS.language = "Urdu"
                st.caption("Urdu select ho gayi - translation agli module mein aayegi.")

        # ---------- HELP & SUPPORT ----------
        with st.expander("❓ Help & Support"):

            st.markdown("**❓ Common Questions:**")
            st.markdown(
                "• **Coins kaise kamayein?** - Ludo khelen, daily login, games jeeten\n"
                "• **Withdrawal kaise hoti hai?** - 100+ coins par Profile se\n"
                "• **Koi tang kare to?** - Settings → Blocked Members se ID block karein\n"
                "• **Report kaise karein?** - Settings → Report a Member"
            )

            bug = st.text_area(
                "🐞 Bug ya masla likhein:",
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
                        "✅ Aapka message support team ko chala gaya - "
                        "24-48 ghante mein jawab milega."
                    )
                else:
                    SS.help_msg = "⚠️ Pehle apna masla likhein."
                safe_rerun()

            if SS.help_msg:
                st.info(SS.help_msg)
                SS.help_msg = ""

        # ---------- ABOUT ----------
        with st.expander("ℹ️ About"):

            st.markdown(
                "**HMF book** v1.0.0 🟢\n\n"
                "Social feed • Games • Coins • Live streaming (coming soon)\n\n"
                "© 2025 HMF - All rights reserved."
            )

        # ---------- LOGOUT ----------
        st.markdown(
            "<div style='height:10px;'></div>",
            unsafe_allow_html=True,
        )

        if st.button(
            "🚪 Logout",
            key="set_logout",
            use_container_width=True,
        ):
            SS.logged_in = False
            SS.page = "auth"
            SS.current_tab = "Home"
            safe_rerun()

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
        safe_rerun()


# ---------- SAFETY ----------
else:
    SS.page = "splash"
    safe_rerun()

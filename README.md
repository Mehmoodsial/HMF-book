import streamlit as st
import json, os
import html as html_mod

st.set_page_config(page_title="HMF Book", page_icon="🟢", layout="centered")

# ---------------- Data Helpers ----------------
DATA_DIR = "/tmp" if os.path.isdir("/tmp") else "."
USERS_FILE = os.path.join(DATA_DIR, "hmf_users.json")
POSTS_FILE = os.path.join(DATA_DIR, "hmf_posts.json")

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception:
        pass

def rerun():
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()

DEMO_POSTS = [
    {"name": "Ahmed Khan", "time": "2 hrs", "text": "HMF book is amazing! 🔥",
     "likes": ["Sara Ali"], "comments": [{"n": "Sara Ali", "t": "Totally agree!"}]},
    {"name": "Sara Ali", "time": "5 hrs", "text": "Good morning everyone ☀️ Have a great day!",
     "likes": [], "comments": []},
    {"name": "Bilal Ahmed", "time": "1 day", "text": "Just joined HMF book. Loving it so far!",
     "likes": [], "comments": [{"n": "Fatima", "t": "Welcome! 👋"}]},
]

# ---------------- Session State ----------------
for k, v in {
    "page": "splash",
    "user": None,
    "users": load_json(USERS_FILE, []),
    "posts": load_json(POSTS_FILE, DEMO_POSTS),
    "post_n": 0,
    "c_n": 0,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- CSS (Design) ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
#MainMenu, footer, header {visibility:hidden;}
[data-testid="stToolbar"] {display:none;}
html, body, .stApp {font-family:'Poppins',sans-serif; background:#eef2f5;}
.block-container {padding-top:1.5rem; padding-bottom:3rem; max-width:700px;}
div.stButton > button {border:none; border-radius:50px; font-weight:600; font-size:15px; padding:10px 0; width:100%;}
div.stButton > button[kind="primary"] {background:#00b86e; color:#fff; box-shadow:0 4px 14px rgba(0,184,110,.35);}
div.stButton > button[kind="primary"]:hover {background:#00a05a; color:#fff;}
div.stButton > button[kind="secondary"] {background:#f0f2f5; color:#444; box-shadow:none;}
div.stButton > button[kind="secondary"]:hover {background:#e2e7ec; color:#111;}
.stTextInput input, .stTextArea textarea {
  border:1.5px solid #dfe3e8 !important; border-radius:14px !important;
  padding:12px 16px !important; font-size:15px !important; background:#fff !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {border-color:#00b86e !important; box-shadow:none !important;}
.logo-band {background:linear-gradient(135deg,#00a05a 0%,#00c47e 55%,#00d68f 100%);
  border-radius:0 0 30px 30px; text-align:center; padding:34px 0 28px; margin-bottom:10px;}
.logo-band .lg {font-size:58px; font-weight:800; color:#fff; letter-spacing:1px; line-height:1;}
.avatar {width:42px; height:42px; border-radius:50%;
  background:linear-gradient(135deg,#00b86e,#00d68f); color:#fff;
  display:inline-flex; align-items:center; justify-content:center; font-weight:700; font-size:18px; flex:none;}
.post-card {background:#fff; border-radius:16px; padding:16px;
  box-shadow:0 1px 4px rgba(0,0,0,.08); margin-bottom:6px;}
.post-name {font-weight:600; font-size:15px; color:#1c1e21;}
.post-time {font-size:12px; color:#8a8d91;}
.post-text {font-size:15px; color:#1c1e21; margin:8px 0 6px; white-space:pre-wrap;}
.post-stats {font-size:13px; color:#65676b; border-bottom:1px solid #eef2f5;
  padding-bottom:8px; margin-bottom:4px;}
.comment {background:#f0f2f5; border-radius:14px; padding:8px 12px;
  margin-bottom:6px; font-size:14px; color:#1c1e21;}
.comment b {display:block; font-size:13px; margin-bottom:2px; color:#00a05a;}
.topbar {display:flex; align-items:center; gap:12px; margin-bottom:6px;}
.topbar .brand {font-size:34px; font-weight:800; color:#00b86e;}
.chip {background:#eef2f5; border-radius:50px; padding:6px 14px;
  font-weight:600; font-size:14px; color:#333;}
</style>
""", unsafe_allow_html=True)

# ================= SPLASH SCREEN =================
if st.session_state.page == "splash":
    st.markdown("<style>.stApp{background:linear-gradient(160deg,#00915a 0%,#00c47e 55%,#0ad697 100%);}</style>",
                unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding-top:14vh;">
      <div style="font-size:96px;font-weight:800;color:#fff;letter-spacing:2px;line-height:1;">HMF</div>
      <div style="font-size:34px;font-weight:600;color:#fff;margin-top:4px;">HMF book</div>
    </div>
    """, unsafe_allow_html=True)
    st.write(""); st.write(""); st.write(""); st.write("")
    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        if st.button("Get Started", type="primary"):
            st.session_state.page = "signup"
            rerun()

# ================= SIGN UP =================
elif st.session_state.page == "signup":
    st.markdown("<style>.stApp{background:#ffffff;}</style>", unsafe_allow_html=True)
    st.markdown('<div class="logo-band"><div class="lg">HMF</div></div>', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#222;margin:4px 0 12px;">Create Account</h2>', unsafe_allow_html=True)

    su_name = st.text_input("Username", placeholder="Username", label_visibility="collapsed", key="su_name")
    su_email = st.text_input("Email", placeholder="Email", label_visibility="collapsed", key="su_email")
    su_pass = st.text_input("Password", placeholder="Password", type="password",
                            label_visibility="collapsed", key="su_pass")
    st.caption("Password must be at least 6 characters long")

    if st.button("Sign Up", type="primary"):
        name, email, pw = su_name.strip(), su_email.strip(), su_pass
        if not name or not email or not pw:
            st.error("⚠️ Please fill all fields")
        elif len(pw) < 6:
            st.error("⚠️ Password must be at least 6 characters")
        elif any(u["email"] == email for u in st.session_state.users):
            st.error("⚠️ This email is already registered")
        else:
            st.session_state.users.append({"name": name, "email": email, "pass": pw})
            save_json(USERS_FILE, st.session_state.users)
            st.session_state.user = {"name": name, "email": email}
            st.session_state.page = "home"
            rerun()

    st.write("")
    if st.button("Already have an account? Log In", type="secondary"):
        st.session_state.page = "login"
        rerun()

# ================= LOGIN =================
elif st.session_state.page == "login":
    st.markdown("<style>.stApp{background:#ffffff;}</style>", unsafe_allow_html=True)
    st.markdown('<div class="logo-band"><div class="lg">HMF</div></div>', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#222;margin:4px 0 12px;">Log In</h2>', unsafe_allow_html=True)

    li_id = st.text_input("Email or Username", placeholder="Email or Username",
                          label_visibility="collapsed", key="li_id")
    li_pass = st.text_input("Password", placeholder="Password", type="password",
                            label_visibility="collapsed", key="li_pass")

    if st.button("Log In", type="primary"):
        uid = li_id.strip()
        found = None
        for u in st.session_state.users:
            if (u["email"] == uid or u["name"] == uid) and u["pass"] == li_pass:
                found = u
                break
        if found:
            st.session_state.user = {"name": found["name"], "email": found["email"]}
            st.session_state.page = "home"
            rerun()
        else:
            st.error("⚠️ Invalid email/username or password")

    st.write("")
    if st.button("Don't have an account? Sign Up", type="secondary"):
        st.session_state.page = "signup"
        rerun()

# ================= HOME / FEED =================
else:
    # Safety: agar session reset ho jaye to wapis splash par jao
    if st.session_state.user is None:
        st.session_state.page = "splash"
        rerun()

    user = st.session_state.user
    posts = st.session_state.posts

    tb1, tb2 = st.columns([4, 1])
    with tb1:
        st.markdown(
            f'<div class="topbar"><span class="brand">HMF</span>'
            f'<span class="chip">👋 {html_mod.escape(user["name"])}</span></div>',
            unsafe_allow_html=True,
        )
    with tb2:
        if st.button("Logout", type="secondary"):
            st.session_state.user = None
            st.session_state.page = "splash"
            rerun()

    st.markdown("**✍️ What's on your mind?**")
    np_key = f"np_{st.session_state.post_n}"
    np = st.text_area("Post", placeholder="Share something with your friends...",
                      label_visibility="collapsed", key=np_key, height=70)
    p1, p2, p3 = st.columns([1, 1, 1])
    with p2:
        if st.button("🚀 Post", type="primary"):
            txt = np.strip()
            if txt:
                posts.insert(0, {"name": user["name"], "time": "Just now", "text": txt,
                                 "likes": [], "comments": []})
                save_json(POSTS_FILE, posts)
                st.session_state.post_n += 1  # naya key = input box khali ho jayega
                rerun()
            else:
                st.warning("Please write something first!")

    st.write("---")
    st.markdown("#### 📰 Feed")

    for i, p in reversed(list(enumerate(posts))):
        # Purana data safe rehne ke liye
        if "likes" not in p:
            p["likes"] = []
        if "comments" not in p:
            p["comments"] = []
        liked = user["name"] in p["likes"]

        st.markdown(f"""
<div class="post-card">
  <div style="display:flex;align-items:center;gap:10px;">
    <div class="avatar">{html_mod.escape(p["name"][0].upper())}</div>
    <div>
      <div class="post-name">{html_mod.escape(p["name"])}</div>
      <div class="post-time">{html_mod.escape(p["time"])}</div>
    </div>
  </div>
  <div class="post-text">{html_mod.escape(p["text"])}</div>
  <div class="post-stats">👍❤️ {len(p["likes"])} likes &nbsp;·&nbsp; 💬 {len(p["comments"])} comments</div>
</div>
""", unsafe_allow_html=True)

        a1, a2 = st.columns(2)
        with a1:
            if st.button("💚 Liked" if liked else "👍 Like", key=f"like{i}", type="secondary"):
                if liked:
                    posts[i]["likes"].remove(user["name"])
                else:
                    posts[i]["likes"].append(user["name"])
                save_json(POSTS_FILE, posts)
                rerun()
        with a2:
            if st.button("💬 Comments", key=f"cbtn{i}", type="secondary"):
                st.session_state[f"open{i}"] = not st.session_state.get(f"open{i}", False)
                rerun()

        if st.session_state.get(f"open{i}", False):
            for c in p["comments"]:
                st.markdown(f'<div class="comment"><b>{html_mod.escape(c["n"])}</b>'
                            f'{html_mod.escape(c["t"])}</div>', unsafe_allow_html=True)
            ck = f"c{i}_{st.session_state.c_n}"
            nc = st.text_input("Comment", placeholder="Write a comment...",
                               label_visibility="collapsed", key=ck)
            s1, s2, s3 = st.columns([1, 1, 1])
            with s2:
                if st.button("Send", key=f"s{i}_{st.session_state.c_n}", type="primary"):
                    if nc.strip():
                        posts[i]["comments"].append({"n": user["name"], "t": nc.strip()})
                        save_json(POSTS_FILE, posts)
                        st.session_state.c_n += 1  # naya key = comment box khali
                        rerun()
        st.write("")

import streamlit as st
import streamlit.components.v1 as components
import random, time, copy

st.set_page_config(page_title="SnapReel 👻", page_icon="👻", layout="centered")

# ---------- SAMPLE DATA ----------
FEED_POSTS = [
    {"user": "Ali 🧑", "time": "2 ghante pehle",
     "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
     "caption": "Mera naya video! 🎉"},
    {"user": "Sara 👧", "time": "5 ghante pehle",
     "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
     "caption": "Road trip vibes 🚗"},
]

YT_REELS = [
    {"type": "yt", "id": "dQw4w9WgXcQ", "user": "YouTube", "caption": "Classic 😄", "likes": "1.4B"},
    {"type": "yt", "id": "kJQP7kiw5Fk", "user": "YouTube", "caption": "Top song 🎶", "likes": "8B"},
    {"type": "yt", "id": "3JZ_D3ELwOQ", "user": "YouTube", "caption": "Music vibes 🎵", "likes": "892K"},
    {"type": "video", "src": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
     "user": "Bilal 🧔", "caption": "Nature 🌿", "likes": "12K"},
]

STORIES = {
    "Aap ➕": {"text": "📸 Snap banane ke liye Upload tab use karein"},
    "Ali 🧑": {"bg": "#8338ec", "text": "Snap 👻"},
    "Sara 👧": {"bg": "#ff7b00", "text": "Good morning ☀️"},
    "Bilal 🧔": {"bg": "#0077b6", "text": "Cricket 🏏"},
}

AUTO_REPLIES = ["Haha 😂", "Sahi hai!", "Bilkul 👍", "Acha ji", "Wow 🤩", "Phir baat karte hain"]

# ---------- SESSION STATE ----------
DEFAULTS = {
    "logged_in": False, "username": "",
    "my_reels": [], "my_videos": [],
    "chats": {
        "Ali 🧑": [{"me": False, "t": "Kya haal hai?"}],
        "Sara 👧": [{"me": False, "t": "Reels dekhi? 😂"}],
        "Bilal 🧔": [{"me": False, "t": "Match dekhoge aaj? 🏏"}],
    },
    "reel_i": 0, "likes": set(), "show_story": None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = copy.deepcopy(v)

# ---------- LOGIN PAGE ----------
if not st.session_state.logged_in:
    st.markdown("## 👻 SnapReel")
    st.caption("Videos • Reels • Chat • Stories")
    with st.form("login"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        ok = st.form_submit_button("Login", use_container_width=True, type="primary")
    if ok:
        if u.strip() and p.strip():
            st.session_state.logged_in = True
            st.session_state.username = u.strip()
            st.rerun()
        else:
            st.error("Username aur password dono likhein!")

    st.divider()
    st.caption("Ya continue karein:")
    c1, c2, c3 = st.columns(3)
    if c1.button("Google", use_container_width=True):
        st.session_state.logged_in = True; st.session_state.username = "Google User"; st.rerun()
    if c2.button("Snapchat", use_container_width=True):
        st.session_state.logged_in = True; st.session_state.username = "Snap User"; st.rerun()
    if c3.button("Facebook", use_container_width=True):
        st.session_state.logged_in = True; st.session_state.username = "FB User"; st.rerun()
    st.stop()

# ---------- SIDEBAR ----------
with st.sidebar:
    st.write(f"🙂 **{st.session_state.username}**")
    if st.button("🚪 Logout", use_container_width=True):
        for k, v in DEFAULTS.items():
            st.session_state[k] = copy.deepcopy(v)
        st.rerun()

# ---------- MAIN TABS ----------
tab_home, tab_reels, tab_up, tab_chat, tab_prof = st.tabs(
    ["🏠 Home", "🎬 Reels", "➕ Upload", "💬 Chat", "👤 Profile"])

# ===== HOME (Stories + Feed) =====
with tab_home:
    st.subheader("👻 Stories")
    cols = st.columns(len(STORIES))
    for col, name in zip(cols, STORIES.keys()):
        if col.button(name, use_container_width=True):
            st.session_state.show_story = name
    if st.session_state.show_story:
        s = STORIES[st.session_state.show_story]
        bg = s.get("bg", "#111")
        st.markdown(
            f"<div style='background:{bg};border-radius:16px;padding:70px 20px;"
            f"text-align:center;font-size:26px;font-weight:bold'>{s['text']}</div>",
            unsafe_allow_html=True)
        if st.button("✕ Story band karein"):
            st.session_state.show_story = None
            st.rerun()

    st.subheader("🏠 Feed")
    for i, p in enumerate(FEED_POSTS):
        with st.container(border=True):
            st.write(f"**{p['user']}** · {p['time']}")
            st.video(p["video"])
            lk = f"feed-{i}"
            cA, cB = st.columns([1, 5])
            if cA.button("❤️" if lk in st.session_state.likes else "🤍", key=lk):
                if lk in st.session_state.likes:
                    st.session_state.likes.discard(lk)
                else:
                    st.session_state.likes.add(lk)
                st.rerun()
            cB.write(f"**{p['user']}** {p['caption']}")

# ===== REELS (YouTube + uploaded, ek ek karke) =====
with tab_reels:
    st.subheader("🎬 Reels")
    all_reels = st.session_state.my_reels + YT_REELS
    n = len(all_reels)
    i = st.session_state.reel_i % n
    r = all_reels[i]
    st.caption(f"Reel {i+1}/{n}")
    if r["type"] == "yt":
        # YouTube video khud chalti hai (autoplay, mute start — player se sound on karein)
        components.iframe(
            f"https://www.youtube.com/embed/{r['id']}?autoplay=1&mute=1&playsinline=1&rel=0",
            height=620, scrolling=False)
    else:
        st.video(r["src"])
    st.markdown(f"**@{r['user']}**  \n{r['caption']}")
    c1, c2, c3 = st.columns(3)
    if c1.button("⬅️ Pichla", use_container_width=True):
        st.session_state.reel_i = (i - 1) % n; st.rerun()
    lk = f"reel-{i}"
    if c2.button("❤️" if lk in st.session_state.likes else "🤍", use_container_width=True):
        if lk in st.session_state.likes:
            st.session_state.likes.discard(lk)
        else:
            st.session_state.likes.add(lk)
        st.rerun()
    if c3.button("Agla ➡️", use_container_width=True):
        st.session_state.reel_i = (i + 1) % n; st.rerun()

# ===== UPLOAD =====
with tab_up:
    st.subheader("➕ Video Upload")
    f = st.file_uploader("Video choose karein", type=["mp4", "mov", "webm"])
    cap = st.text_input("Caption likhein")
    if f is not None:
        st.video(f)
        a, b = st.columns(2)
        if a.button("🎬 Reels par daalein", use_container_width=True):
            st.session_state.my_reels.insert(0, {
                "type": "video", "src": f.getvalue(),
                "user": st.session_state.username,
                "caption": cap or "Meri reel 🎬", "likes": "0"})
            st.session_state.reel_i = 0
            st.success("Reels mein add ho gayi! 🎬 Reels tab mein dekhein")
        if b.button("👤 Profile par daalein", use_container_width=True):
            st.session_state.my_videos.insert(0, {"src": f.getvalue(), "caption": cap or "Meri video 🎬"})
            st.success("Profile par add ho gayi! 👤 Profile tab mein dekhein")
    st.info("⚠️ Videos sirf is session tak rehti hain. Permanent ke liye database chahiye.")

# ===== CHAT =====
with tab_chat:
    st.subheader("💬 Messages")
    names = list(st.session_state.chats.keys())
    sel = st.selectbox("Dost select karein", names)
    msgs = st.session_state.chats[sel]
    box = st.container(height=380)
    with box:
        for m in msgs:
            if m["me"]:
                with st.chat_message("user", avatar="🙂"):
                    st.write(m["t"])
            else:
                with st.chat_message("assistant", avatar=sel.split()[-1]):
                    st.write(m["t"])
    with st.form("msgf", clear_on_submit=True):
        t = st.text_input("Message likhein...", label_visibility="collapsed")
        sent = st.form_submit_button("➤ Bhejein", use_container_width=True)
    if sent and t.strip():
        msgs.append({"me": True, "t": t.strip()})
        time.sleep(0.6)
        msgs.append({"me": False, "t": random.choice(AUTO_REPLIES)})
        st.rerun()

# ===== PROFILE =====
with tab_prof:
    st.subheader(f"👤 {st.session_state.username}")
    a, b, c = st.columns(3)
    a.metric("Videos", len(st.session_state.my_videos))
    b.metric("Followers", "1.2K")
    c.metric("Following", "348")
    st.divider()
    vids = st.session_state.my_videos
    if vids:
        for j in range(0, len(vids), 2):
            pair = vids[j:j + 2]
            c2 = st.columns(2)
            for col, v in zip(c2, pair):
                with col:
                    st.video(v["src"])
                    st.caption(v["caption"])
    else:
        st.info("Abhi koi video nahi. ➕ Upload tab se video daalein!")

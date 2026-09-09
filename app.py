import streamlit as st

st.set_page_config(
    page_title="HMF book",
    page_icon="❤️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── 1. Streamlit ka default header/menu/footer hide karo ──
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stStatusWidget"] {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 6rem !important;}
</style>
""", unsafe_allow_html=True)

# ── 2. Current page query params se lo ──
qp = st.query_params
current_page = qp.get("page", "home")

# ── 3. Instagram-style Bottom Nav Bar ──
st.markdown(f"""
<style>
    .ig-bottom-nav {{
        position: fixed;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 500px;
        background: #ffffff;
        border-top: 1px solid #dbdbdb;
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 10px 0;
        z-index: 99999;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.06);
    }}
    .ig-bottom-nav a {{
        text-decoration: none;
        font-size: 26px;
        color: #262626;
        padding: 6px 14px;
        border-radius: 10px;
        transition: background .2s, transform .2s;
        line-height: 1;
    }}
    .ig-bottom-nav a:hover {{
        background: #f0f0f0;
        transform: translateY(-2px);
    }}
    .ig-bottom-nav a.active {{
        color: #00913f;   /* HMF green — apni theme ka color */
        background: #e6f7ee;
        font-weight: bold;
    }}
    @media (max-width: 520px) {{
        .ig-bottom-nav {{ max-width: 100%; }}
    }}
</style>

<div class="ig-bottom-nav">
    <a href="?page=home"          class="{'active' if current_page=='home' else ''}">🏠</a>
    <a href="?page=search"        class="{'active' if current_page=='search' else ''}">🔍</a>
    <a href="?page=reels"         class="{'active' if current_page=='reels' else ''}">🎬</a>
    <a href="?page=notifications" class="{'active' if current_page=='notifications' else ''}">❤️</a>
    <a href="?page=profile"       class="{'active' if current_page=='profile' else ''}">👤</a>
</div>
""", unsafe_allow_html=True)

# ── 4. Page Router ──
if current_page == "home":
    # 👇 Yahan apna existing home/feed code daalein
    st.title("HMF book")
    st.success("Home feed loaded")

elif current_page == "search":
    st.title("🔍 Search")
    q = st.text_input("Search users, reels, posts...")
    st.write(f"Results for: {q}")

elif current_page == "reels":
    st.title("🎬 Reels")
    st.video("https://www.youtube.com/watch?v=aqz-KE-bpKQ")

elif current_page == "notifications":
    st.title("❤️ Notifications")
    st.info("Aapke posts ko logo ne like kiya")

elif current_page == "profile":
    st.title("👤 Profile")
    st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=hoor_jannat")
    st.subheader("hoor_jannat")
    st.caption("Bio yahan likhein...")

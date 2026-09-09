import streamlit as st

# ---------------- CSS ----------------
st.markdown("""
<style>
/* Default: bottom nav desktop pe chhupa rahe */
.bottom-nav { display: none; }

@media (max-width: 768px) {
    /* Mobile pe top nav chhupao */
    .top-nav { display: none !important; }

    /* Bottom nav dikhao — Instagram style */
    .bottom-nav {
        display: flex;
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #ffffff;
        border-top: 1px solid #dbdbdb;
        justify-content: space-around;
        align-items: center;
        padding: 8px 0 14px 0;
        z-index: 999999;
    }
    .bottom-nav a {
        text-decoration: none;
        font-size: 26px;
        padding: 6px 16px;
        border-radius: 12px;
    }
    .bottom-nav a.active { background: #f2f2f2; }

    /* Content ke niche space, warna last post nav ke niche chhup jayega */
    .stApp { padding-bottom: 90px !important; }

    /* Streamlit ka default header hide karo mobile pe */
    header[data-testid="stHeader"] { display: none; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAV ----------------
PAGES = {
    "home":      "🏠",
    "search":    "🔍",
    "add":       "➕",
    "reels":     "🎬",
    "profile":   "👤",
}

# Current page read karo (aapka app already ?page=home use karta hai)
page = st.query_params.get("page", "home")

# ---- Desktop top nav ----
top = "".join(
    f'<a href="?page={k}" style="margin:0 10px;text-decoration:none;'
    f'color:{"#000" if k == page else "#555"};font-weight:{"700" if k == page else "400"}">{k.title()}</a>'
    for k in PAGES
)
st.markdown(f'<div class="top-nav">{top}</div>', unsafe_allow_html=True)

# ---- Mobile bottom nav (Instagram style) ----
bottom = "".join(
    f'<a href="?page={k}" class="{"active" if k == page else ""}">{icon}</a>'
    for k, icon in PAGES.items()
)
st.markdown(f'<div class="bottom-nav">{bottom}</div>', unsafe_allow_html=True)

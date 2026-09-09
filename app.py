def render_bottom_nav():
    """Instagram-style bottom menu bar (mobile friendly)."""
    items = [
        ("Home", "🏠"),
        ("Ludo", "🎲"),
        ("Create", "➕"),
        ("Reels", "🎬"),
        ("Profile", "👤"),
    ]

    if hasattr(st, "bottom"):
        nav = st.bottom          # naya Streamlit (fixed bottom bar)
    else:
        nav = st.container()     # purana Streamlit (page ke end me)

    with nav:
        cols = st.columns(len(items))
        for col, (tab, ico) in zip(cols, items):
            with col:
                active = (SS.current_tab == tab)

                # upar wala chhota dot (active pe green)
                if active:
                    st.markdown(
                        "<div class='nav-dot nav-dot-on'></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        "<div class='nav-dot'></div>",
                        unsafe_allow_html=True,
                    )

                # icon button
                if st.button(ico, key="nav_" + tab,
                             use_container_width=True):
                    SS.current_tab = tab
                    safe_rerun()

                # neeche wala label
                if active:
                    st.markdown(
                        "<div class='nav-label nav-label-on'>" + tab + "</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        "<div class='nav-label'>" + tab + "</div>",
                        unsafe_allow_html=True,
                    )

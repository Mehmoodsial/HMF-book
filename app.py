            # PROFILE (Instagram style)
            elif SS.tab == "Profile":
                me = db["users"].get(SS.username, {})
                my_posts = []
                for p in db["posts"]:
                    if p["user"] == SS.username:
                        my_posts.append(p)
                fr = db["friends"].get(SS.username, [])
                my_likes = 0
                for p in my_posts:
                    my_likes = my_likes + len(p.get("likes", {}))

                # ---- Top bar: username ----
                top = "<div class='igtop'><div class="
                top = top + "'iguser'>"
                top = top + esc(SS.username)
                top = top + "</div><div style="
                top = top + "'font-size:22px;'>⋮</div>"
                top = top + "</div>"
                st.markdown(top, unsafe_allow_html=True)

                # ---- Pic + Stats row ----
                row = "<div class='igrow'>"
                row = row + av(SS.username,
                               me.get("avatar"), 86)
                row = row + "<div class='igstat'><b>"
                row = row + str(len(my_posts))
                row = row + "</b><span>posts</span></div>"
                row = row + "<div class='igstat'><b>"
                row = row + str(len(fr))
                row = row + "</b><span>followers</span>"
                row = row + "</div>"
                row = row + "<div class='igstat'><b>"
                row = row + str(len(fr))
                row = row + "</b><span>following</span>"
                row = row + "</div></div>"
                st.markdown(row, unsafe_allow_html=True)

                # ---- Name + Bio ----
                st.markdown("<div class='igname'>"
                            + esc(me.get("display_name",
                                         SS.username))
                            + "</div>",
                            unsafe_allow_html=True)
                st.markdown("<div class='igbio'>"
                            + esc(me.get("bio", ""))
                            + " · ❤️ " + str(my_likes)
                            + " total likes</div>",
                            unsafe_allow_html=True)

                if is_owner:
                    st.markdown(
                        "<p style='text-align:center;"
                        "margin:4px 0;'><span style="
                        "'background:#f59e0b;color:#fff;"
                        "padding:2px 10px;border-radius:12px;"
                        "font-size:11px;font-weight:bold;'>"
                        "👑 OWNER</span></p>",
                        unsafe_allow_html=True)

                # ---- Buttons ----
                b1, b2 = st.columns(2)
                if b1.button("✏️ Edit Profile", key="pe"):
                    go("Settings")
                    SS.setpage = "personal"
                if b2.button("💰 " + str(me.get("coins", 0))
                             + " Coins", key="pp"):
                    db = load_db()
                    u = db["users"].get(SS.username)
                    if u is not None and \
                            u.get("coins", 0) >= 100:
                        u["coins"] -= 100
                        save_db(db)
                        st.success("Payout submitted!")
                        rr()
                    else:
                        st.warning("Min 100 coins!")

                # ---- Post Grid (3 columns) ----
                if my_posts:
                    grid = "<div class='iggrid'>"
                    for p in my_posts[:9]:
                        grid = grid + "<div>"
                        if p.get("type") == "text":
                            gr = p.get("grad", "#f0f0f0")
                            grid = grid + "<div style="
                            grid = grid + "'background:"
                            grid = grid + gr
                            grid = grid + ";width:100%;"
                            grid = grid + "height:100%;"
                            grid = grid + "display:flex;"
                            grid = grid + "align-items:"
                            grid = grid + "center;justify-"
                            grid = grid + "content:center;"
                            grid = grid + "font-size:22px;"
                            grid = grid + "color:#056839;"
                            grid = grid + "font-weight:bold;"
                            grid = grid + ";'>"
                            grid = grid + esc(p.get("txt",
                                                    ""))[:8]
                            grid = grid + "</div>"
                        elif p.get("type") == "youtube":
                            grid = grid + "📺"
                        elif p.get("type") == "image":
                            grid = grid + "🖼️"
                        elif p.get("type") in ("video",
                                               "reel"):
                            grid = grid + "🎬"
                        grid = grid + "</div>"
                    grid = grid + "</div>"
                    st.markdown(grid,
                                unsafe_allow_html=True)
                else:
                    st.caption("No posts yet")

                # ---- Change Pic ----
                with st.expander("🖼️ Change Profile Pic"):
                    fl = st.selectbox("Filter:", FILTERS,
                                      key="pf")
                    pi = st.file_uploader(
                        "Upload", type=["png", "jpg"],
                        key="pi")
                    cam = st.camera_input("📸 Camera",
                                          key="pcam")
                    if st.button("💾 Update", key="pu",
                                 use_container_width=True):
                        src = pi
                        if src is None:
                            src = cam
                        if src is not None:
                            pil = Image.open(src)
                            setp(SS.username, "avatar",
                                 spil(filt(pil, fl)))
                            st.success("Updated!")
                            rr()
                        else:
                            st.warning("Photo choose!")

                # ---- Discover People ----
                st.markdown("<div class='dischead'>"
                            "🔍 Discover People</div>",
                            unsafe_allow_html=True)
                suggestions = []
                for u in db["users"]:
                    if u == SS.username:
                        continue
                    if u in fr:
                        continue
                    if u in SS.blocked:
                        continue
                    skip = False
                    for x in db.get("friend_requests",
                                    []):
                        if x["from"] == SS.username \
                                and x["to"] == u:
                            skip = True
                    if not skip:
                        suggestions.append(u)

                if not suggestions:
                    st.caption("No suggestions")
                for u in suggestions[:5]:
                    ud = db["users"].get(u, {})
                    mutual = len(db["friends"].get(u, []))
                    row2 = "<div class='discrow'>"
                    row2 = row2 + av(u, ud.get("avatar"),
                                    44)
                    row2 = row2 + "<div style="
                    row2 = row2 + "'flex:1;'><div class="
                    row2 = row2 + "'discnm'>"
                    row2 = row2 + esc(ud.get("display_name",
                                             u))
                    row2 = row2 + "</div><div class="
                    row2 = row2 + "'discsub'>"
                    if mutual > 0:
                        row2 = row2 + str(mutual)
                        row2 = row2 + " mutual"
                    else:
                        row2 = row2 + "Suggested for you"
                    row2 = row2 + "</div></div></div>"
                    st.markdown(row2,
                                unsafe_allow_html=True)
                    d1, d2 = st.columns(2)
                    if d1.button("Follow", key="df_"
                                 + u,
                                 use_container_width=True):
                        db = load_db()
                        db["friend_requests"].append(
                            {"from": SS.username,
                             "to": u,
                             "time": time.time()})
                        save_db(db)
                        notify(u, "@" + SS.username
                               + " started following!")
                        rr()
                    if d2.button("👤", key="dv_" + u,
                                 use_container_width=True):
                        SS.view_user = u
                        rr()

                # ---- Settings shortcut ----
                if st.button("⚙️ Settings", key="pset",
                             use_container_width=True):
                    go("Settings")

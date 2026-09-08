            # ===== MESSAGES (Instagram DM) =====
            elif SS.tab == "Messages":

                if HAS_REFRESH:
                    st_autorefresh(interval=4000, key="mr")
                db = load_db()

                if SS.msg_view == "chat":
                    tgt = SS.msg_target
                    if tgt not in db["users"]:
                        SS.msg_view = "list"
                        rr()

                    if st.button("←", key="cbk"):
                        SS.msg_view = "list"
                        rr()

                    ud = db["users"].get(tgt, {})
                    if SS.username in db.get("friends", {}).get(
                            tgt, []):
                        act = "Active now"
                    else:
                        act = "Active 1h ago"

                    hd = "<div class='dmi'>"
                    hd = hd + av(tgt, ud.get("avatar"), 44)
                    hd = hd + "<div><div class='dmn'>"
                    hd = hd + esc(ud.get("display_name", tgt))
                    hd = hd + "</div><div class='dms'>"
                    hd = hd + act
                    hd = hd + "</div></div></div>"
                    st.markdown(hd, unsafe_allow_html=True)

                    msgs = []
                    for m in db["messages"]:
                        if (m["from"] == SS.username
                                and m["to"] == tgt):
                            msgs.append(m)
                        elif (m["from"] == tgt
                              and m["to"] == SS.username):
                            msgs.append(m)

                    for m in sorted(msgs,
                                    key=lambda x: x["time"]):
                        mine = m["from"] == SS.username
                        ts = time.strftime(
                            "%I:%M %p",
                            time.localtime(m["time"])).lower()
                        if mine:
                            cls = "bm"
                        else:
                            cls = "bh"
                        st.markdown(
                            "<span class='" + cls + "'>" +
                            esc(m.get("text", "")) +
                            "<span class='bt'>" + ts +
                            "</span></span>",
                            unsafe_allow_html=True)
                        r = m.get("reactions", [])
                        mk = m.get("id", str(m["time"]))
                        if r:
                            lb = "👍 " + str(len(r))
                        else:
                            lb = "👍"
                        if st.button(lb, key="rx_" + mk):
                            tog_rx(m.get("id"), SS.username)
                            rr()

                    tx = st.text_input("Message...",
                                       key="ctx",
                                       placeholder=
                                       "Message...")
                    if st.button("Send", key="csd",
                                 use_container_width=True):
                        if tx.strip():
                            smsg(tgt, tx.strip())
                            rr()

                else:
                    dmh = "<div class='dmh'>← "
                    dmh = dmh + esc(SS.username)
                    dmh = dmh + "</div>"
                    st.markdown(dmh, unsafe_allow_html=True)

                    sq = st.text_input("Search",
                                       key="dm_srch",
                                       placeholder="Search")
                    dm_tab = st.columns(2)
                    if dm_tab[0].button("Messages",
                                        key="dmt1",
                                        use_container_width=True):
                        SS.dm_tab = "msgs"
                        rr()
                    if dm_tab[1].button("Requests",
                                        key="dmt2",
                                        use_container_width=True):
                        SS.dm_tab = "reqs"
                        rr()
                    if "dm_tab" not in SS:
                        SS.dm_tab = "msgs"

                    if SS.dm_tab == "reqs":
                        reqs = []
                        for r in db["friend_requests"]:
                            if r["to"] == SS.username:
                                reqs.append(r)
                        if not reqs:
                            st.info("No requests")
                        for i, r in enumerate(reqs):
                            f = r["from"]
                            fu = db["users"].get(f, {})
                            row = "<div class='dmi'>"
                            row = row + av(f, fu.get("avatar"),
                                           56)
                            row = row + "<div><div class='dmn'>"
                            row = row + esc(fu.get("display_name",
                                                   f))
                            row = row + "</div><div class='dms'>"
                            row = row + "Sent " + str(
                                int((time.time() -
                                     r.get("time", 0)) / 60))
                            row = row + "m ago"
                            row = row + "</div></div></div>"
                            st.markdown(row,
                                        unsafe_allow_html=True)
                            a1, a2 = st.columns(2)
                            if a1.button("Accept",
                                         key="dma_" + str(i),
                                         use_container_width
                                         =True):
                                db = load_db()
                                db["friend_requests"] = [
                                    x for x in
                                    db["friend_requests"]
                                    if not (x["from"] == f
                                            and x["to"] ==
                                            SS.username)]
                                db["friends"].setdefault(
                                    SS.username,
                                    []).append(f)
                                db["friends"].setdefault(
                                    f, []).append(SS.username)
                                save_db(db)
                                rr()
                            if a2.button("Delete",
                                         key="dmd_" + str(i),
                                         use_container_width
                                         =True):
                                db = load_db()
                                db["friend_requests"] = [
                                    x for x in
                                    db["friend_requests"]
                                    if not (x["from"] == f
                                            and x["to"] ==
                                            SS.username)]
                                save_db(db)
                                rr()
                    else:
                        partners = set()
                        for m in db["messages"]:
                            if m["from"] == SS.username:
                                partners.add(m["to"])
                            elif m["to"] == SS.username:
                                partners.add(m["from"])
                        for f in db.get("friends", {}).get(
                                SS.username, []):
                            partners.add(f)

                        convs = []
                        for p in partners:
                            if p == SS.username:
                                continue
                            if p in SS.blocked:
                                continue
                            if sq and sq.lower() not in p.lower():
                                continue
                            cn = []
                            for m in db["messages"]:
                                if (m["from"] == SS.username
                                        and m["to"] == p):
                                    cn.append(m)
                                elif (m["from"] == p
                                      and m["to"] ==
                                      SS.username):
                                    cn.append(m)
                            last = None
                            if cn:
                                last = cn[-1]
                            convs.append({"u": p, "last": last})

                        convs.sort(key=lambda c: (
                            c["last"]["time"] if c["last"]
                            else 0), reverse=True)

                        if not convs:
                            st.info("No messages yet")

                        for c in convs:
                            p = c["u"]
                            ud = db["users"].get(p, {})
                            if SS.username in db.get(
                                    "friends", {}).get(p, []):
                                dot = "●"
                                dotc = "#31a24c"
                            else:
                                dot = ""
                                dotc = "#9ca3af"

                            row = "<div class='dmi'>"
                            row = row + av(p, ud.get("avatar"),
                                           56)

                            if c["last"]:
                                mins = int((time.time() -
                                            c["last"]["time"])
                                           / 60)
                                if mins < 1:
                                    st2 = "now"
                                elif mins < 60:
                                    st2 = str(mins) + "m ago"
                                else:
                                    hrs = int(mins / 60)
                                    st2 = str(hrs) + "h ago"
                                if c["last"]["from"] == \
                                        SS.username:
                                    stx = "Sent " + st2
                                else:
                                    stx = "Active " + st2
                            else:
                                stx = "Say hello 👋"

                            row = row + "<div><div class="
                            row = row + "'dmn'>"
                            row = row + esc(ud.get("display_name",
                                                   p))
                            row = row + "</div><div class="
                            row = row + "'dms'>"
                            row = row + stx
                            row = row + "</div></div>"
                            if dot:
                                row = row + "<span style="
                                row = row + "'color:" + dotc
                                row = row + ";font-size:10px;"
                                row = row + ";margin-left:"
                                row = row + "auto;'>●</span>"
                            row = row + "</div>"
                            st.markdown(row,
                                        unsafe_allow_html=True)

                            if st.button("💬", key="op_" + p,
                                         use_container_width
                                         =True):
                                SS.msg_view = "chat"
                                SS.msg_target = p
                                SS.msg_ttype = "direct"
                                rr()

                    with st.expander("➕ New Chat"):
                        others = []
                        for x in db["users"]:
                            if x != SS.username:
                                others.append(x)
                        pick = st.selectbox("Chat:", others,
                                            key="ncs")
                        if st.button("Start", key="ncb",
                                     use_container_width=True):
                            SS.msg_view = "chat"
                            SS.msg_target = pick
                            SS.msg_ttype = "direct"
                            rr()

def ldb():
    try:
        with open(DBF, "r") as f:
            d = json.load(f)
    except Exception:
        d = {}
    if "messages" in d and "msg" not in d:
        d["msg"] = d.pop("messages")
    if "notifications" in d and "notif" not in d:
        d["notif"] = d.pop("notifications")
    if "friend_requests" in d and "freq" not in d:
        d["freq"] = d.pop("friend_requests")
    if "friends" in d and "fr" not in d:
        d["fr"] = d.pop("friends")
    if "banned" in d and "ban" not in d:
        d["ban"] = d.pop("banned")
    if "reports" in d and "rep" not in d:
        d["rep"] = d.pop("reports")
    for p in d.get("posts", []):
        if "user" in p:
            p["u"] = p["user"]
        if "likes" in p:
            p["lk"] = p["likes"]
        if "comments" in p:
            p["cm"] = p["comments"]
        if p.get("type") == "youtube":
            p["type"] = "yt"
        if p.get("type") == "image":
            p["type"] = "img"
        if p.get("type") == "text":
            p["type"] = "txt"
    for k, r in d.get("users", {}).items():
        if "display_name" in r:
            r["dn"] = r["display_name"]
        if "avatar" in r:
            r["av"] = r["avatar"]
        if "blocked" in r:
            r["blk"] = r["blocked"]
        if "app_lock" in r:
            r["lock"] = r["app_lock"]
        if "app_pin" in r:
            r["pin"] = r["app_pin"]
        if "finger_lock" in r:
            r["fin"] = r["finger_lock"]
        if "auto_logout" in r:
            r["al"] = r["auto_logout"]
        if "comment_filter" in r:
            r["cf"] = r["comment_filter"]
    for m in d.get("msg", []):
        if "from" in m:
            m["f"] = m["from"]
        if "reactions" in m:
            m["rx"] = m["reactions"]
        if "time" in m:
            m["t"] = m["time"]
    for n in d.get("notif", []):
        if "time" in n:
            n["t"] = n["time"]
        if "read" in n:
            n["r"] = n["read"]
    if not isinstance(d.get("users"), dict):
        d["users"] = {}
    for k in ("msg", "posts", "notif", "rep", "ban", "freq", "stories", "hl"):
        if not isinstance(d.get(k), list):
            d[k] = []
    for k in ("fr", "cf", "seen"):
        if not isinstance(d.get(k), dict):
            d[k] = {}
    if "owner" not in d:
        d["owner"] = ""
    return d

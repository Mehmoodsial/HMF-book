def av(name, path=None, size=36):
    if path and os.path.exists(path):
        try:
            b = base64.b64encode(open(path, "rb").read())
            s = str(size)
            r = "<img src='data:image/png;base64,"
            r = r + b.decode()
            r = r + "' style='width:" + s
            r = r + "px;height:" + s
            r = r + "px;border-radius:50%;"
            r = r + "object-fit:cover;'>"
            return r
        except Exception:
            pass
    s = str(size)
    fs = str(int(size * 0.38))
    ini = esc(str(name)[:2].upper())
    r = "<div style='width:" + s
    r = r + "px;height:" + s
    r = r + "px;border-radius:50%;background:"
    r = r + "linear-gradient(135deg,#00B074,"
    r = r + "#056839);color:#fff;display:flex;"
    r = r + "align-items:center;justify-content:"
    r = r + "center;font-weight:bold;font-size:"
    r = r + fs + "px;'>"
    r = r + ini + "</div>"
    return r

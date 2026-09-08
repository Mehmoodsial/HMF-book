import streamlit as st
import streamlit.components.v1 as components
import random
import json
import os
import io
import time
import uuid
import base64
import hashlib
from html import escape as esc
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

st.set_page_config(page_title="HMF Book", page_icon="🟢",
                   layout="centered")

try:
    from streamlit_autorefresh import st_autorefresh
    HAS_REFRESH = True
except Exception:
    HAS_REFRESH = False

SALT = "hmf_secret_2025"
DB_FILE = "hmf_db.json"
UPLOAD_DIR = "uploads"
FILTERS = ["None", "Beauty", "Sepia", "Vintage", "Cool",
           "Gray", "Bright", "Cartoon"]
GRADS = ["linear-gradient(45deg,#d1fae5,#a7f3d0)",
         "linear-gradient(45deg,#ecfdf5,#6ee7b7)",
         "linear-gradient(45deg,#e6f7f0,#b3e6cc)"]
BAD_WORDS = ["stupid", "idiot", "hate", "dumb", "ugly"]


def hash_pw(p):
    return hashlib.sha256((SALT + p).encode()).hexdigest()


def pw_ok(s, p):
    if s == hash_pw(p):
        return True
    return s == p


def rr():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


def toast(m):
    if hasattr(st, "toast"):
        st.toast(m)
    else:
        st.info(m)


def parse_yt(u):
    u = (u or "").strip()
    if not u:
        return None
    if len(u) == 11 and "/" not in u:
        return u
    for t in ("youtu.be/", "v=", "/shorts/", "/embed/"):
        if t in u:
            p = u.split(t)[1]
            p = p.split("?")[0]
            p = p.split("&")[0]
            p = p.split("/")[0]
            if p:
                return p
    return None


def load_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
    except Exception:
        db = {}
    if not isinstance(db.get("users"), dict):
        db["users"] = {}
    for k in ("messages", "posts", "groups",
              "notifications", "reports", "banned",
              "friend_requests", "pages", "events",
              "listings", "ads"):
        if not isinstance(db.get(k), list):
            db[k] = []
    for k in ("friends", "seen"):
        if not isinstance(db.get(k), dict):
            db[k] = {}
    if "owner" not in db:
        db["owner"] = ""
    return db


def save_db(db):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=1)
    except Exception:
        pass


def setp(u, k, v):
    db = load_db()
    rec = db["users"].get(u)
    if rec is not None:
        rec[k] = v
        save_db(db)


def notify(to, text):
    if not to:
        return
    db = load_db()
    db["notifications"].insert(0, {"to": to, "text": text,
                                   "time": time.time(),
                                   "read

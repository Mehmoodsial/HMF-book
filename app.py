import streamlit as st

# Page ki settings aur title set karna
st.set_page_config(page_title="EarnSocial - Login", page_icon="📱", layout="centered")

# Custom Green Gradient Styling (Aapki vibrant green theme ke liye)
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: white;
        padding: 30px;
        border-radius: 15px;
    }
    h1 {
        text-align: center;
        color: white !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton>button {
        background-color: #ffffff !important;
        color: #11998e !important;
        font-weight: bold;
        width: 100%;
        border-radius: 10px;
        border: none;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #38ef7d !important;
        color: white !important;
    }
    label {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Login Box ka container
st.markdown('<div class="main">', unsafe_allow_html=True)

st.title("💚 EarnSocial")
st.write("<p style='text-align: center; color: white;'>Make Friends, Play Games & Earn Money</p>", unsafe_allow_html=True)

st.write("---")

# Username aur Password ke input boxes
username = st.text_input("Email ya Username")
password = st.text_input("Password", type="password")

st.write("")

# Login Button
if st.button("Log In"):
    if username == "admin" and password == "12345":
        st.success("Login Kamyab! Aap app ke andar aa chuke hain.")
    else:
        st.error("Ghalat Email ya Password! Dubara koshish karein.")

st.markdown('</div>', unsafe_allow_html=True)

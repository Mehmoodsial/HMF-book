import streamlit as st

# Page Configuration
st.set_page_config(page_title="EarnSocial - Login", page_icon="💚", layout="centered")

# Custom Green Design
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #11998e, #38ef7d);
    }
    .login-container {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
        color: #333333;
    }
    h1, p {
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
    }
    /* Input label text color fix for dark/light theme */
    label {
        color: white !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Main Login Card
st.markdown("""
    <div class="login-container">
        <h1 style="color: #11998e; margin-bottom: 5px;">💚 EarnSocial</h1>
        <p style="color: #666666; font-size: 16px; margin-bottom: 10px;">Play Games & Earn Money</p>
    </div>
    """, unsafe_allow_html=True)

st.write("") 

# English Input Fields
username = st.text_input("📧 Email or Username")
password = st.text_input("🔒 Password", type="password")

st.write("")

# Login Button
if st.button("Log In", use_container_width=True):
    # Ab aap apni is Email aur neeche diye gaye password se login kar sakte hain
    if username == "msunderstore83@gmail.com" and password == "pakistan123":
        st.success("🎉 Login Successful! Welcome to EarnSocial.")
    else:
        st.error("❌ Invalid Email or Password! Please try again.")

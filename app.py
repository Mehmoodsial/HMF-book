import streamlit as st

# Page Configuration
st.set_page_config(page_title="EarnSocial - Login", page_icon="💚", layout="centered")

# Custom Green Design (CSS styling jo background aur buttons ko pyara banaye gi)
st.markdown("""
    <style>
    /* Poore page ka background color */
    .stApp {
        background: linear-gradient(135deg, #11998e, #38ef7d);
    }
    /* Login Box ki styling */
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
    </style>
    """, unsafe_allow_html=True)

# Main Login Card HTML Ke Zariye
st.markdown("""
    <div class="login-container">
        <h1 style="color: #11998e; margin-bottom: 5px;">💚 EarnSocial</h1>
        <p style="color: #666666; font-size: 16px; margin-bottom: 20px;">Dost Banayein, Games Khelein aur Paise Kamayein</p>
    </div>
    """, unsafe_allow_html=True)

st.write("") # Thodi khali jagah

# Email aur Password ke asli Input Fields (Jo Streamlit handle karega)
username = st.text_input("📧 Email ya Username")
password = st.text_input("🔒 Password", type="password")

st.write("")

# Login Button
if st.button("Log In", use_container_width=True):
    # Test karne ke liye humne ek dummy id/password rakha hai
    if username == "admin" and password == "12345":
        st.success("🎉 Login Kamyab! Aap app ke andar aa chuke hain.")
    else:
        st.error("❌ Ghalat Email ya Password! Dubara koshish karein.")

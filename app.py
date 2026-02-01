import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Personal Health Coach",
    page_icon="💗",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.main {
    background: linear-gradient(180deg, #fde2e8 0%, #fff5f8 100%);
}

.title {
    font-size: 48px;
    font-weight: 600;
    color: #7a1c3a;
    text-align: center;
    margin-top: 40px;
}

.subtitle {
    text-align: center;
    color: #6b3a4a;
    font-size: 18px;
    margin-bottom: 40px;
}

.card {
    background-color: white;
    padding: 30px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;
}

.card:hover {
    transform: scale(1.03);
}

.card-title {
    font-size: 20px;
    font-weight: 600;
    color: #7a1c3a;
}

.card-text {
    color: #555;
    font-size: 14px;
    margin-bottom: 20px;
}

button {
    background-color: #f472b6 !important;
    color: white !important;
    border-radius: 10px !important;
    height: 45px;
    font-weight: 500;
}

button:hover {
    background-color: #ec4899 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='title'>💗 Personal Health Coach</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>A warm, caring AI companion for your mental & physical well-being</div>",
    unsafe_allow_html=True
)

# ---------------- OPTIONS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>💬 Chat as a Friend</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='card-text'>Talk freely with an empathetic AI who listens without judgment.</div>",
        unsafe_allow_html=True
    )
    st.button("Start Chat")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>🩺 Health Diagnosis</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='card-text'>Share symptoms or medical history and get safe, guided insights.</div>",
        unsafe_allow_html=True
    )
    st.button("Get Diagnosis")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>📅 Wellness Timetable</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='card-text'>Create a realistic daily routine that fits your lifestyle.</div>",
        unsafe_allow_html=True
    )
    st.button("Build Timetable")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown(
    "<p style='text-align:center; color:#9a4c68; margin-top:40px;'>You are not alone. Your health matters.</p>",
    unsafe_allow_html=True
)

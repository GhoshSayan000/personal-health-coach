import streamlit as st
from agent.coach_agent import HealthCoachAgent
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Chat with Health Coach",
    page_icon="💖",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #fff1f6;
}
.chat-box {
    padding: 10px;
    border-radius: 12px;
}
.user-msg {
    background-color: #ffd6e8;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 8px;
}
.agent-msg {
    background-color: #ffffff;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 8px;
    border-left: 5px solid #ff4b91;
}
.stat-card {
    background: white;
    padding: 15px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE SECTION ----------------
st.markdown("## 💬 Chat with Your Personal Health Coach")
st.markdown(
    "This is a **safe, friendly space**. You can talk freely — "
    "about stress, health, routine, or just how your day feels."
)

st.divider()

# ---------------- SESSION STATE ----------------
if "agent" not in st.session_state:
    st.session_state.agent = HealthCoachAgent()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- CHAT DISPLAY ----------------
for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"<div class='user-msg'><b>You:</b> {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='agent-msg'><b>Coach:</b> {msg}</div>", unsafe_allow_html=True)

# ---------------- CHAT INPUT ----------------
user_input = st.chat_input("Type here... I’m listening 💗")

if user_input:
    # show typing effect
    with st.spinner("Coach is thinking..."):
        time.sleep(0.6)
        reply = st.session_state.agent.reply(user_input)

    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Coach", reply))
    st.rerun()

st.divider()

# ---------------- QUICK ACTION BUTTONS ----------------
st.markdown("### 🌱 Quick Conversation Starters")

col1, col2, col3 = st.columns(3)

if col1.button("😔 I feel low"):
    st.session_state.chat_history.append(
        ("Coach", st.session_state.agent.reply("I feel sad and low these days"))
    )
    st.rerun()

if col2.button("😰 I’m stressed"):
    st.session_state.chat_history.append(
        ("Coach", st.session_state.agent.reply("I am stressed and overwhelmed"))
    )
    st.rerun()

if col3.button("💪 I want to be healthier"):
    st.session_state.chat_history.append(
        ("Coach", st.session_state.agent.reply("I want to improve my lifestyle and health"))
    )
    st.rerun()

st.divider()

# ---------------- CHAT STATS ----------------
st.markdown("### 📊 Conversation Insights")

total_msgs = len(st.session_state.agent.memory)
sad = sum(1 for m in st.session_state.agent.memory if m["mood"] == "sad")
stress = sum(1 for m in st.session_state.agent.memory if m["mood"] == "stress")
healthy = sum(1 for m in st.session_state.agent.memory if m["mood"] == "healthy")

c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"<div class='stat-card'><h3>{total_msgs}</h3><p>Total Messages</p></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='stat-card'><h3>{sad}</h3><p>Low Mood Signals</p></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='stat-card'><h3>{stress}</h3><p>Stress Signals</p></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='stat-card'><h3>{healthy}</h3><p>Positive Signals</p></div>", unsafe_allow_html=True)

st.divider()

# ---------------- REPORT GENERATION ----------------
st.markdown("### 📄 Generate Wellness Report")

st.caption(
    "This summary is created from your conversation patterns. "
    "It is **not a medical diagnosis**."
)

if st.button("🩺 Generate My Health Summary"):
    report = st.session_state.agent.generate_report()
    st.text_area(
        "Your Personal Health Summary",
        report,
        height=260
    )

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("💖 Personal Health Coach — Built with care, empathy, and responsibility.")

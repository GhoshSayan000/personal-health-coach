import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Personal Health Coach",
    page_icon="💙",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #f4f7fb;
}

.main {
    background-color: #f4f7fb;
}

.chat-box {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 10px;
}

.user-msg {
    background-color: #e6f0ff;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 8px;
}

.ai-msg {
    background-color: #f1f5f9;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 8px;
}

h1 {
    color: #1f2937;
}

.subtitle {
    color: #6b7280;
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1>💙 Personal Health Coach</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>A calm, empathetic AI companion for mental & physical wellness</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello 🌱 I’m your Personal Health Coach. You can talk to me about how you're feeling—mentally or physically. I’m here to listen."
        }
    ]

# ---------------- CHAT DISPLAY ----------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='ai-msg'><b>Coach:</b> {msg['content']}</div>", unsafe_allow_html=True)

# ---------------- USER INPUT ----------------
user_input = st.chat_input("Share what’s on your mind...")

# ---------------- AI LOGIC (TEMP – RULE BASED) ----------------
def ai_reply(user_text):
    text = user_text.lower()

    if any(word in text for word in ["sad", "depressed", "anxious", "low", "stress"]):
        return (
            "I’m really glad you shared this 🤍\n\n"
            "Feeling this way can be heavy. Try slowing your breathing for a minute and remind yourself "
            "that what you’re feeling is valid. If these feelings continue, speaking to a mental health professional can help a lot."
        )

    if any(word in text for word in ["pain", "fever", "headache", "tired", "sleep"]):
        return (
            "Thanks for telling me. Based on what you shared, it’s important to rest, stay hydrated, "
            "and observe your symptoms. If the discomfort increases or lasts long, please consult a doctor."
        )

    if any(word in text for word in ["fit", "healthy", "exercise", "diet", "routine"]):
        return (
            "That’s great to hear 🌟\n\n"
            "A balanced routine with regular exercise, proper sleep, and mindful eating can do wonders. "
            "If you want, I can help you design a simple daily wellness schedule."
        )

    return (
        "Thank you for sharing 🤍\n\n"
        "Tell me a bit more about how you’re feeling physically or emotionally. "
        "I’m here to understand and guide you safely."
    )

# ---------------- HANDLE MESSAGE ----------------
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = ai_reply(user_input)

    st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()

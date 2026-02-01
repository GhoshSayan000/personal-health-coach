import streamlit as st
from openai import OpenAI
import os

# ---------- Page Config ----------
st.set_page_config(
    page_title="Chat with Coach",
    page_icon="💬",
    layout="centered"
)

# ---------- Background & Style ----------
st.markdown("""
<style>
body {
    background-color: #fdecef;
}
.chat-box {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}
.user {
    color: #b30059;
    font-weight: bold;
}
.coach {
    color: #333333;
}
</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown("## 💬 Chat with Your AI Coach")
st.markdown("Talk freely. I'm here to listen, support, and guide you 🤍")

# ---------- OpenAI Client ----------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- Session State ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a warm, friendly, supportive mental health coach. Talk like a caring friend."}
    ]

# ---------- Display Chat ----------
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(
            f"<div class='chat-box user'>You: {msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='chat-box coach'>Coach: {msg['content']}</div>",
            unsafe_allow_html=True
        )

# ---------- Input ----------
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        temperature=0.8
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()

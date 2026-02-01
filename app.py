import streamlit as st
import openai
import json
from datetime import datetime

# ----------------------------
# CONFIG
# ----------------------------
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your key

st.set_page_config(page_title="Personal Health Coach", page_icon="💚")

st.title("💚 Personal Health Coach")
st.subheader("Your AI Wellness Companion")

# ----------------------------
# WELCOME
# ----------------------------
if "conversation" not in st.session_state:
    st.session_state.conversation = []

st.write("Hello! I'm your AI health coach. I can help you with wellness guidance, mental health assessment, and personalized lifestyle plans. Let's start!")

# ----------------------------
# MEDICAL HISTORY INPUT
# ----------------------------
st.header("Step 1: Your Medical History")

history_option = st.radio("Do you have previous medical history?", ["Yes", "No"])

if history_option == "Yes":
    uploaded_file = st.file_uploader("Upload your medical history (PDF or TXT)")
    if uploaded_file:
        st.success("Medical history uploaded!")
        try:
            history_text = uploaded_file.read().decode("utf-8")
        except:
            history_text = str(uploaded_file)
        st.session_state.medical_history = history_text
else:
    st.write("Let's create your medical history interactively.")
    name = st.text_input("Your Name")
    age = st.number_input("Age", 0, 120)
    weight = st.number_input("Weight (kg)", 0, 300)
    height = st.number_input("Height (cm)", 0, 250)
    lifestyle = st.text_area("Describe your lifestyle habits (exercise, diet, sleep, stress)")
    
    if st.button("Save History"):
        st.session_state.medical_history = {
            "name": name,
            "age": age,
            "weight": weight,
            "height": height,
            "lifestyle": lifestyle
        }
        st.success("Medical history saved!")

# ----------------------------
# STEP 2: Chat / Mental Health Assessment
# ----------------------------
st.header("Step 2: Chat with your Health Coach")

user_input = st.text_input("Type your message here...")

if st.button("Send") and user_input:
    st.session_state.conversation.append({"role": "user", "content": user_input})
    
    conversation_text = ""
    for msg in st.session_state.conversation:
        conversation_text += f"{msg['role']}: {msg['content']}\n"
    
    if "medical_history" in st.session_state:
        conversation_text += f"Medical History: {st.session_state.medical_history}\n"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful, empathetic AI health coach. You never prescribe medicines or make diagnoses. You give lifestyle, wellness, and preventive health guidance."},
            {"role": "user", "content": conversation_text}
        ],
        max_tokens=300
    )
    
    answer = response.choices[0].message.content
    st.session_state.conversation.append({"role": "assistant", "content": answer})
    
# ----------------------------
# DISPLAY CONVERSATION
# ----------------------------
st.header("Conversation")
for msg in st.session_state.conversation:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Coach:** {msg['content']}")

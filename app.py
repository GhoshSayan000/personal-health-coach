import streamlit as st
import openai
from datetime import datetime

# ----------------------------
# CONFIG
# ----------------------------
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your key
st.set_page_config(page_title="Personal Health Coach", page_icon="💚", layout="wide")

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.header("ℹ️ About")
st.sidebar.markdown("""
Welcome to **Personal Health Coach!**  
- Enter your medical history  
- Chat with your AI coach  
- Complete mental health assessment  
- Get personalized wellness timetable  
""")

# ----------------------------
# HEADER
# ----------------------------
st.markdown("<h1 style='color:green;'>💚 Personal Health Coach</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color:gray;'>Your AI wellness companion for mind & body</h3>", unsafe_allow_html=True)
st.write("---")

# ----------------------------
# SESSION STATE
# ----------------------------
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "medical_history" not in st.session_state:
    st.session_state.medical_history = {}

# ----------------------------
# SECTION 1: MEDICAL HISTORY
# ----------------------------
with st.container():
    st.markdown("<h2 style='color:blue;'>📝 Medical History</h2>", unsafe_allow_html=True)
    history_option = st.radio("Do you have previous medical history?", ["Yes", "No"], horizontal=True)

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
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name")
            age = st.number_input("Age", 0, 120)
        with col2:
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

st.write("---")

# ----------------------------
# SECTION 2: AI CHAT
# ----------------------------
with st.container():
    st.markdown("<h2 style='color:purple;'>💬 Chat with your AI Coach</h2>", unsafe_allow_html=True)
    user_input = st.text_input("Type your message here...")

    if st.button("Send") and user_input:
        st.session_state.conversation.append({"role": "user", "content": user_input})

        conversation_text = ""
        for msg in st.session_state.conversation:
            conversation_text += f"{msg['role']}: {msg['content']}\n"

        if st.session_state.medical_history:
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

    # Display conversation
    for msg in st.session_state.conversation:
        if msg["role"] == "user":
            st.markdown(f"<div style='background-color:#D0E8FF; padding:10px; border-radius:10px; color:#0000FF; margin-bottom:5px;'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color:#DFFFD6; padding:10px; border-radius:10px; color:#008000; margin-bottom:5px;'><b>Coach:</b> {msg['content']}</div>", unsafe_allow_html=True)

st.write("---")

# ----------------------------
# SECTION 3: MENTAL HEALTH TEST (Creative Feature)
# ----------------------------
with st.container():
    st.markdown("<h2 style='color:orange;'>🧠 Mental Health Self-Test</h2>", unsafe_allow_html=True)
    st.write("Answer a few questions to check your mental wellness:")

    q1 = st.slider("On a scale of 1-10, how stressed do you feel?", 1, 10)
    q2 = st.slider("How many hours do you sleep on average?", 0, 12)
    q3 = st.radio("Do you feel anxious often?", ["Yes", "No"])
    q4 = st.radio("Do you feel low energy frequently?", ["Yes", "No"])

    if st.button("Get Mental Health Insight"):
        score = 0
        score += q1
        score += 10 - q2  # less sleep = higher score
        score += 5 if q3 == "Yes" else 0
        score += 5 if q4 == "Yes" else 0

        if score < 10:
            st.success("✅ Your mental wellness seems good!")
        elif score < 20:
            st.info("⚠️ Moderate stress detected. Try relaxation and balanced lifestyle.")
        else:
            st.warning("❌ High stress/anxiety detected. Consider professional consultation.")

st.write("---")

# ----------------------------
# SECTION 4: WELLNESS TIMETABLE (Creative Feature)
# ----------------------------
with st.container():
    st.markdown("<h2 style='color:teal;'>📅 Personalized Wellness Timetable</h2>", unsafe_allow_html=True)
    st.write("Your AI coach can suggest a simple daily schedule based on your goals:")

    goal = st.radio("Choose your main goal:", ["Improve Fitness", "Reduce Stress", "Balanced Lifestyle"])

    if st.button("Generate Timetable"):
        if goal == "Improve Fitness":
            st.markdown("""
- **Morning:** 30 min exercise  
- **Afternoon:** Healthy meal + walk  
- **Evening:** Stretching + meditation  
- **Night:** Sleep 7-8 hours
""")
        elif goal == "Reduce Stress":
            st.markdown("""
- **Morning:** Meditation 15 min  
- **Afternoon:** Light walk + hydration  
- **Evening:** Journaling / relaxation  
- **Night:** Sleep 7-8 hours
""")
        else:
            st.markdown("""
- **Morning:** Light exercise + healthy breakfast  
- **Afternoon:** Work + short breaks  
- **Evening:** Meditation + light dinner  
- **Night:** Sleep 7-8 hours
""")

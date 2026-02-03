# pages/2_Diagnosis.py

import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="AI Health Diagnosis",
    page_icon="🩺",
    layout="wide"
)

# -------------------- UI HEADER --------------------
st.markdown(
    """
    <h1 style="text-align:center;">🩺 AI Health Diagnosis & Guidance</h1>
    <p style="text-align:center; color:gray;">
    This assistant provides medical guidance and decision support — not a medical diagnosis.
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# -------------------- SESSION STATE --------------------
if "stage" not in st.session_state:
    st.session_state.stage = 1

if "followup_count" not in st.session_state:
    st.session_state.followup_count = 0

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.header("📌 Progress")
    st.progress(st.session_state.stage / 4)
    st.markdown(
        """
        **Steps**
        1. Medical History  
        2. Symptoms  
        3. AI Follow-up  
        4. Guidance  
        """
    )

# -------------------- STEP 1: MEDICAL HISTORY --------------------
if st.session_state.stage == 1:
    st.subheader("1️⃣ Medical History")

    col1, col2 = st.columns(2)

    with col1:
        medical_history = st.text_area(
            "Past medical conditions, allergies, medications",
            placeholder="e.g. Diabetes, asthma, BP, surgery in 2021",
            height=180
        )

    with col2:
        uploaded_docs = st.file_uploader(
            "Upload prescriptions / reports (optional)",
            type=["pdf", "png", "jpg", "jpeg"],
            accept_multiple_files=True
        )

        if uploaded_docs:
            st.success(f"{len(uploaded_docs)} document(s) uploaded")

    consent = st.checkbox(
        "I understand this is not a medical diagnosis and agree to proceed"
    )

    if st.button("➡️ Continue"):
        if not consent:
            st.warning("Please accept the disclaimer to continue.")
        else:
            st.session_state.stage = 2
            st.rerun()

# -------------------- STEP 2: SYMPTOMS --------------------
elif st.session_state.stage == 2:
    st.subheader("2️⃣ Current Symptoms")

    symptoms = st.text_area(
        "Describe what you are experiencing right now",
        placeholder="e.g. fever, cough, pain, dizziness, fatigue...",
        height=200
    )

    duration = st.selectbox(
        "How long have you had these symptoms?",
        ["Less than 24 hours", "1–3 days", "4–7 days", "More than a week"]
    )

    severity = st.slider(
        "How severe do the symptoms feel?",
        1, 10, 5
    )

    if st.button("🧠 Analyze Symptoms"):
        if not symptoms.strip():
            st.warning("Please describe your symptoms.")
        else:
            st.session_state.symptoms = symptoms
            st.session_state.stage = 3
            st.rerun()

# -------------------- DEMO AI ENGINE --------------------
def demo_ai(symptoms, followups=0):
    s = symptoms.lower()

    if "chest pain" in s:
        return {
            "condition": "⚠️ Possible cardiac or muscular issue",
            "questions": [
                "Is the pain sharp, dull, or crushing?",
                "Does it spread to arm, jaw, or back?",
                "Do you feel breathless or sweaty?"
            ],
            "risk": "high",
            "advice": [
                "Avoid exertion immediately",
                "Seek urgent medical evaluation"
            ]
        }

    if "fever" in s and "cough" in s:
        return {
            "condition": "Possible respiratory or viral infection",
            "questions": [
                "Is the cough dry or with mucus?",
                "Do you have shortness of breath?",
                "Is fever persistent despite medication?"
            ],
            "risk": "medium",
            "advice": [
                "Rest and hydrate well",
                "Monitor temperature twice daily",
                "Consult a doctor if fever lasts >3 days"
            ]
        }

    if "headache" in s and ("stress" in s or "tension" in s):
        return {
            "condition": "Likely tension or stress-related headache",
            "questions": [
                "Do you have long screen exposure?",
                "Is sleep disturbed?",
                "Any nausea or vision issues?"
            ],
            "risk": "low",
            "advice": [
                "Improve sleep routine",
                "Limit screen exposure",
                "Practice relaxation exercises"
            ]
        }

    return {
        "condition": "Symptoms unclear — more information needed",
        "questions": [
            "When did the symptoms begin?",
            "Are they worsening or improving?",
            "Any recent illness, travel, or injury?"
        ],
        "risk": "unknown",
        "advice": [
            "Track symptoms carefully",
            "Consult a healthcare professional"
        ]
    }

# -------------------- STEP 3: FOLLOW-UP --------------------
elif st.session_state.stage == 3:
    st.subheader("3️⃣ AI Follow-up Assessment")

    result = demo_ai(st.session_state.symptoms, st.session_state.followup_count)

    st.markdown(f"### 🔍 Initial Assessment")
    st.info(result["condition"])

    st.markdown("### ❓ Follow-up Questions")
    for q in result["questions"]:
        st.text_input(q, key=q)

    if st.button("➡️ Generate Guidance"):
        st.session_state.stage = 4
        st.rerun()

# -------------------- STEP 4: GUIDANCE --------------------
elif st.session_state.stage == 4:
    st.subheader("4️⃣ Guidance & Next Steps")

    result = demo_ai(st.session_state.symptoms)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🧠 Possible Condition")
        st.success(result["condition"])

        st.markdown("### 🚦 Risk Level")
        if result["risk"] == "high":
            st.error("HIGH — Seek medical attention immediately")
        elif result["risk"] == "medium":
            st.warning("MODERATE — Monitor closely")
        else:
            st.info("LOW / UNCLEAR")

    with col2:
        st.markdown("### 🧘 Recommended Actions")
        for a in result["advice"]:
            st.write("•", a)

    st.markdown("---")
    st.caption(
        f"Generated on {datetime.now().strftime('%d %b %Y, %I:%M %p')}"
    )

    st.warning(
        "⚠️ This tool does NOT replace a doctor. "
        "If symptoms worsen or feel dangerous, seek professional medical help immediately."
    )

    if st.button("🔁 Start New Assessment"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

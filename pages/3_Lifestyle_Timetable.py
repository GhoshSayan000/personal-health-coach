# pages/3_Lifestyle_Timetable.py

import streamlit as st
from datetime import datetime, time

st.set_page_config(
    page_title="Lifestyle Timetable",
    page_icon="⏰",
    layout="wide"
)

# -------------------- HEADER --------------------
st.markdown(
    """
    <h1 style="text-align:center;">⏰ AI Lifestyle & Recovery Timetable</h1>
    <p style="text-align:center; color:gray;">
    Personalized daily routine based on your concern (sleep, stress, fatigue, focus, etc.)
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# -------------------- SESSION STATE --------------------
if "routine_generated" not in st.session_state:
    st.session_state.routine_generated = False

# -------------------- USER INPUT --------------------
st.subheader("🧠 Tell us what you’re struggling with")

problem = st.text_area(
    "Describe your issue (example: sleep deficiency, anxiety, low energy, burnout, poor focus)",
    placeholder="e.g. I sleep very late, wake up tired, feel sleepy during the day...",
    height=140
)

wake_time = st.time_input("Usual wake-up time", value=time(7, 0))
sleep_time = st.time_input("Usual sleep time", value=time(23, 30))

activity_level = st.selectbox(
    "Daily activity level",
    ["Low (mostly sedentary)", "Moderate", "High (physically demanding)"]
)

if st.button("🧠 Generate My Timetable"):
    if not problem.strip():
        st.warning("Please describe your concern first.")
    else:
        st.session_state.problem = problem.lower()
        st.session_state.routine_generated = True

# -------------------- DEMO AI TIMETABLE ENGINE --------------------
def demo_timetable(problem: str):
    if "sleep" in problem or "insomnia" in problem or "tired" in problem:
        return [
            ("06:30 – 07:00", "Wake up, sunlight exposure (balcony / walk)", "Resets circadian rhythm"),
            ("07:00 – 07:30", "Light stretching / breathing", "Activates nervous system gently"),
            ("07:30 – 08:00", "Breakfast (protein + carbs)", "Stabilizes energy levels"),
            ("09:00 – 12:00", "Focused work / study", "Peak alertness window"),
            ("12:30 – 13:00", "Lunch (avoid heavy food)", "Prevents afternoon crash"),
            ("13:30 – 14:00", "Short walk / power nap (20 min max)", "Restores alertness"),
            ("15:00 – 17:00", "Light work / creative tasks", "Lower cognitive load period"),
            ("18:00 – 18:30", "Exercise (not intense)", "Improves sleep quality"),
            ("19:30 – 20:00", "Dinner (light, no caffeine)", "Supports melatonin release"),
            ("21:00 – 21:30", "Screen-free wind-down (reading, journaling)", "Signals sleep readiness"),
            ("22:30", "Sleep", "Optimal recovery window"),
        ]

    if "stress" in problem or "anxiety" in problem:
        return [
            ("07:00", "Wake up + breathing exercise", "Reduces cortisol spike"),
            ("08:00", "Morning walk", "Calms nervous system"),
            ("09:00 – 12:00", "Primary work block", "Mental clarity window"),
            ("12:30", "Balanced lunch", "Blood sugar stability"),
            ("14:00", "5-min grounding exercise", "Stress regulation"),
            ("17:30", "Physical activity / yoga", "Releases tension"),
            ("20:30", "Digital detox", "Prevents mental overload"),
            ("22:00", "Sleep routine", "Restores emotional balance"),
        ]

    return [
        ("Morning", "Healthy routine (hydration, movement)", "Builds baseline energy"),
        ("Midday", "Focused work + breaks", "Prevents burnout"),
        ("Evening", "Relaxation & reflection", "Mental recovery"),
        ("Night", "Consistent sleep time", "Physical restoration"),
    ]

# -------------------- OUTPUT --------------------
if st.session_state.routine_generated:
    st.subheader("📅 Your Personalized Daily Timetable")

    timetable = demo_timetable(st.session_state.problem)

    st.markdown(
        """
        <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px;
            border: 1px solid #ddd;
            text-align: left;
        }
        th {
            background-color: #f0f2f6;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <table>
            <tr>
                <th>⏰ Time</th>
                <th>📝 Activity</th>
                <th>🎯 Purpose</th>
            </tr>
        """ +
        "".join(
            f"<tr><td>{t}</td><td>{a}</td><td>{p}</td></tr>"
            for t, a, p in timetable
        ) +
        "</table>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.success("✅ Routine generated using evidence-based wellness principles (demo AI)")

    st.caption(
        f"Generated on {datetime.now().strftime('%d %b %Y, %I:%M %p')}"
    )

    st.warning(
        "⚠️ This timetable is guidance only. Adjust based on your body and consult a professional if needed."
    )

    if st.button("🔁 Generate Another Routine"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

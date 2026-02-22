import streamlit as st
from shared.api_cient import simulate_api

st.title("🧪 What-If Simulation")

st.sidebar.header("Original Student Data")

attendance = st.sidebar.slider("Attendance %", 0, 100, 60)
assignment = st.sidebar.slider("Assignment Avg", 0, 100, 60)
quiz = st.sidebar.slider("Quiz Avg", 0, 100, 60)
midterm = st.sidebar.slider("Midterm Score", 0, 100, 60)
previous = st.sidebar.slider("Previous Score", 0, 100, 60)

student_payload = {
    "attendance_percentage": attendance,
    "assignment_avg": assignment,
    "quiz_avg": quiz,
    "midterm_score": midterm,
    "previous_semester_score": previous
}

st.subheader("Modify Scenario")

new_attendance = st.slider("New Attendance %", 0, 100, attendance)
new_quiz = st.slider("New Quiz Avg", 0, 100, quiz)

if st.button("Run Simulation"):

    payload = {
        "student": student_payload,
        "new_attendance": new_attendance,
        "new_quiz": new_quiz
    }

    res = simulate_api(payload)

    if res.status_code == 200:
        data = res.json()

        col1, col2 = st.columns(2)

        col1.metric("Original Risk", data["original"])
        col2.metric("New Risk", data["new"])

        st.markdown("### Simulation Insight")
        st.write(data["simulation_explanation"])
    else:
        st.error("Simulation Error")

import streamlit as st
from shared.api_cient import copilot_api

st.title("🤖 Academic Copilot Chat")

st.sidebar.header("Student Input")

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

question = st.text_area(
    "Ask Academic Question",
    placeholder="Why am I at risk? How can I improve?"
)

if st.button("Ask Copilot"):

    payload = {
        "student": student_payload,
        "question": question
    }

    res = copilot_api(payload)

    if res.status_code == 200:
        data = res.json()

        st.success(f"Prediction: {data['prediction']}")
        st.info(f"Confidence: {round(data['confidence']*100,2)} %")

        st.markdown("### Copilot Response")
        st.write(data["copilot_response"])
    else:
        st.error("Copilot Error")

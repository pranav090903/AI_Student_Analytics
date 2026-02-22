import streamlit as st
from shared.api_cient import predict_api

st.title("📈 Risk Prediction")

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

if st.button("Predict"):

    res = predict_api(student_payload)

    if res.status_code == 200:
        data = res.json()
        st.success(f"Prediction: {data['prediction']}")
        
        col1, col2 = st.columns(2)
        col1.info(f"Confidence: {round(data['confidence']*100,2)} %")
        col2.info(f"Model Accuracy: {round(data.get('accuracy', 0)*100,2)} %")
    else:
        st.error("Backend Error")

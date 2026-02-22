import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8002"

# Role Protection
if not st.session_state.get("logged_in"):
    st.error("Login Required")
    st.stop()

if st.session_state.role != "Student":
    st.error("Student Access Only")
    st.stop()

st.title("📊 My Academic Record")

if st.button("Load My Record"):

    res = requests.get(
        f"{BACKEND_URL}/records/my-record",
        headers={
            "Authorization": f"Bearer {st.session_state.token}"
        }
    )

    if res.status_code == 200:
        data = res.json()

        st.subheader("📋 Academic Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Attendance", f"{data['attendance_percentage']}%")
        col2.metric("Quiz Avg", f"{data['quiz_avg']}%")
        col3.metric("Assignment", f"{data['assignment_avg']}%")
        col4.metric("Midterm", f"{data['midterm_score']}%")

        st.divider()
        st.subheader("🤖 AI Analysis")
        m1, m2, m3 = st.columns(3)
        m1.metric("Current Status", data.get("risk_level", "Unknown"))
        m2.metric("Confidence", f"{round(data.get('confidence_score', 0)*100, 1)}%")
        m3.metric("Model Accuracy", f"{round(data.get('model_accuracy', 0)*100, 1)}%")
        
        st.info(f"Last Updated: {data.get('updated_at', 'Never')}")

    else:
        st.error(f"Record Not Found: {res.text}")

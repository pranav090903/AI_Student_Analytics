import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8002"


# ================= ROLE PROTECTION =================

if not st.session_state.get("logged_in"):
    st.error("Login Required")
    st.stop()

if st.session_state.role != "Teacher":
    st.error("Teacher Access Only")
    st.stop()


st.title("📚 Teacher — Enter Student Academic Records")


# ================= PRE-FILL LOGIC =================
edit_id = st.session_state.get("edit_student_id")
default_values = {
    "student_id": "",
    "attendance": 50.0,
    "quiz": 50.0,
    "assignment": 50.0,
    "midterm": 50.0,
    "previous": 50.0
}

if edit_id:
    try:
        res = requests.get(
            f"{BACKEND_URL}/records/{edit_id}",
            headers={"Authorization": f"Bearer {st.session_state.token}"}
        )
        if res.status_code == 200:
            existing = res.json()
            default_values.update({
                "student_id": existing.get("student_id", ""),
                "attendance": float(existing.get("attendance_percentage", 50.0)),
                "quiz": float(existing.get("quiz_avg", 50.0)),
                "assignment": float(existing.get("assignment_avg", 50.0)),
                "midterm": float(existing.get("midterm_score", 50.0)),
                "previous": float(existing.get("previous_semester_score", 50.0))
            })
            st.info(f"Editing record for: {edit_id}")
    except Exception as e:
        st.error(f"Error fetching existing record: {e}")

# ================= FORM =================

with st.form("student_record_form"):

    student_username = st.text_input("Student Username", value=default_values["student_id"])

    attendance = st.number_input(
        "Attendance %",
        min_value=0.0,
        max_value=100.0,
        value=default_values["attendance"]
    )

    quiz = st.number_input(
        "Quiz Average",
        min_value=0.0,
        max_value=100.0,
        value=default_values["quiz"]
    )

    assignment = st.number_input(
        "Assignment Average",
        min_value=0.0,
        max_value=100.0,
        value=default_values["assignment"]
    )

    midterm = st.number_input(
        "Midterm Score",
        min_value=0.0,
        max_value=100.0,
        value=default_values["midterm"]
    )
    previous_semester_score = st.number_input(
        "previous semester score",
        min_value=0.0,
        max_value=100.0,
        value=default_values["previous"]
    )

    submitted = st.form_submit_button("💾 Save Record")


# ================= API CALL =================

if submitted:
    # Clear edit state on submit
    if "edit_student_id" in st.session_state:
        del st.session_state["edit_student_id"]

    payload = {
        "student_id": student_username,
        "attendance_percentage": attendance,
        "quiz_avg": quiz,
        "assignment_avg": assignment,
        "midterm_score": midterm,
        "previous_semester_score": previous_semester_score
    }

    try:
        res = requests.post(
            f"{BACKEND_URL}/records/upsert",
            json=payload,
            headers={
                "Authorization": f"Bearer {st.session_state.token}"
            }
        )

        if res.status_code == 200:
            data = res.json()
            st.success("✅ Student Record Saved Successfully")
            
            # Display Prediction Results
            st.divider()
            st.subheader("🤖 AI Analysis Result")
            col1, col2, col3 = st.columns(3)
            col1.metric("Predicted Status", data["prediction"])
            col2.metric("Confidence", f"{round(data['confidence']*100, 1)}%")
            col3.metric("Model Accuracy", f"{round(data['accuracy']*100, 1)}%")
            
            st.info(f"The system is {round(data['confidence']*100, 1)}% sure about this prediction based on a model with {round(data['accuracy']*100, 1)}% historical accuracy.")

        else:
            st.error(f"Error: {res.text}")

    except Exception as e:
        st.error(f"Connection Error: {str(e)}")

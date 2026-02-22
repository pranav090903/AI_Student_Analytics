import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://127.0.0.1:8002"

if st.session_state.role != "Teacher":
    st.error("Unauthorized Access")
    st.stop()

st.title("👨‍🏫 Teacher Dashboard")
st.write("Overview of all student academic records.")

# ================= FETCH DATA =================
try:
    response = requests.get(
        f"{BACKEND_URL}/records/all/students",
        headers={
            "Authorization": f"Bearer {st.session_state.token}"
        }
    )

    if response.status_code == 200:
        data = response.json()
        
        if data:
            df = pd.DataFrame(data)
            
            # Reorder columns for better view
            cols = ["student_id", "risk_level", "confidence_score", "model_accuracy", "attendance_percentage", "quiz_avg", "assignment_avg", "midterm_score", "updated_at"]
            # Filter cols that exist in df
            cols = [c for c in cols if c in df.columns]
            
            st.dataframe(df[cols], use_container_width=True)

            # ================= MANAGEMENT SECTION =================
            st.divider()
            st.subheader("🛠️ Manage Records")
            
            col_sel, col_del, col_upd = st.columns([2, 1, 1])
            
            with col_sel:
                # Filter out any NaN student IDs
                id_list = df["student_id"].dropna().unique().tolist()
                selected_student = st.selectbox("Select Student ID to Manage", id_list)
            
            with col_del:
                if st.button("🗑️ Delete Record", use_container_width=True):
                    try:
                        del_res = requests.delete(
                            f"{BACKEND_URL}/records/{selected_student}",
                            headers={"Authorization": f"Bearer {st.session_state.token}"}
                        )
                        if del_res.status_code == 200:
                            st.success(f"Deleted {selected_student}")
                            st.rerun()
                        else:
                            st.error(f"Failed to delete: {del_res.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")

            with col_upd:
                if st.button("✏️ Update Record", use_container_width=True):
                    # Save selected student to session state and use navigation or a flag
                    # Since we use st.Page in streamlit_app.py, we can't easily switch page from code without st.switch_page
                    # But we can at least set the state so when they click "Enter Records" manually it's filled.
                    # Or we can use st.switch_page if it's available in this version of streamlit.
                    st.session_state["edit_student_id"] = selected_student
                    st.info(f"Student {selected_student} selected for update. Please go to 'Enter Records' page.")
                    # If switch_page is available:
                    try:
                        st.switch_page("features/teacher/enter_records.py")
                    except:
                        pass

        else:
            st.info("No student records found.")

    else:
        st.error(f"Error fetching data: {response.text}")

except Exception as e:
    st.error(f"Connection Error: {str(e)}")

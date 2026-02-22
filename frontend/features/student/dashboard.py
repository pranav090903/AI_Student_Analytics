import streamlit as st
import requests

if st.session_state.role != "Student":
    st.error("Unauthorized Access")
    st.stop()

st.title(f"🎓 Welcome, {st.session_state.username}!")

BACKEND_URL = "http://127.0.0.1:8002"

# Automatically fetch and display current status
try:
    res = requests.get(
        f"{BACKEND_URL}/records/{st.session_state.username}",
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )
    
    if res.status_code == 200:
        data = res.json()
        
        st.subheader("📊 Your Current Academic Status")
        
        # Risk Indicator
        risk = data.get("risk_level", "Unknown")
        if risk == "Safe":
            st.success(f"Current Status: {risk}")
        else:
            st.warning(f"Current Status: {risk}")
            
        # Score Summary
        col1, col2, col3 = st.columns(3)
        col1.metric("Attendance", f"{data.get('attendance_percentage', 0)}%")
        col2.metric("Quiz Avg", data.get('quiz_avg', 0))
        col3.metric("Assignment", data.get('assignment_avg', 0))
        
        st.info("💡 You can use the **Copilot Chat** for personalized advice or the **Simulation** tab to see how improving your scores might change your status.")
    
    else:
        st.info("👋 Your academic record hasn't been entered by a teacher yet. Check back soon!")

except Exception as e:
    st.error(f"Error connecting to server: {e}")

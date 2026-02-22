import streamlit as st

from features.auth.login import login_page
from features.auth.registration import register_page
from shared.session_manager import init_session, logout

init_session()

st.set_page_config(page_title="EduPulse AI", page_icon="🎓")

if not st.session_state.logged_in:
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        login_page()
    
    with tab2:
        register_page()

else:
    
    role = st.session_state.role
    
    st.sidebar.title("EduPulse AI")
    st.sidebar.write(f"👤 {st.session_state.username}")
    st.sidebar.write(f"🎭 Role: {role}")
    
    if st.sidebar.button("Logout"):
        logout()
        st.rerun()
    
    # Define pages based on role
    student_pages = [
        st.Page("features/student/dashboard.py", title="📊 My Dashboard"),
        st.Page("features/student/prediction.py", title="📈 Performance Predictor"),
        st.Page("features/student/copilot.py", title="🤖 Success Assistant"),
        st.Page("features/student/simulation.py", title="🧪 Success Simulator"),
        st.Page("features/student/my_record.py", title="📜 Academic Profile")
    ]
    
    teacher_pages = [
        st.Page("features/teacher/dashboard.py", title="📊 Teacher Dashboard"),
        st.Page("features/teacher/copilot.py", title="🤖 AI Student Insights"),
        st.Page("features/teacher/enter_records.py", title="📝 Record Entry")
    ]
    
    # Navigate based on role
    if role == "Student":
        pg = st.navigation(student_pages)
    elif role == "Teacher":
        pg = st.navigation(teacher_pages)
    else:
        st.error("Invalid Role")
        st.stop()
    
    pg.run()

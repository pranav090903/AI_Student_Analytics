import streamlit as st
from shared.auth_api import register_api


def register_page():

    st.header("🏢 EduPulse AI")
    st.title("📝 Register")

    username = st.text_input("Username", key="reg_user")
    password = st.text_input("Password", type="password", key="reg_pass")
    role = st.selectbox("Role", ["Student", "Teacher"], key="reg_role")

    if st.button("Register", key="reg_btn"):

        res = register_api(username, password, role)

        if res.status_code == 200:
            st.success("User Registered")
        else:
            try:
                error_msg = res.json().get("detail", "Registration Failed")
            except Exception:
                error_msg = f"Server Error ({res.status_code})"
            st.error(f"Error: {error_msg}")

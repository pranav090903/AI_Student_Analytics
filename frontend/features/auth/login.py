import streamlit as st
from shared.auth_api import login_api
from shared.session_manager import save_login


def login_page():

    st.header("🏢 EduPulse AI")
    st.title("🔐 Login")

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", key="login_btn"):

        res = login_api(username, password)         #control goes to frontend/utils/auth_api.py

        if res.status_code == 200:
            data = res.json()

            save_login(
                token=data["access_token"],
                role=data["role"],
                username=username
            )

            st.success("Login Success")
            st.rerun()

        else:
            try:
                error_msg = res.json().get("detail", "Login Failed")
            except Exception:
                error_msg = f"Server Error ({res.status_code})"
            st.error(f"Error: {error_msg}")


    st.divider()
    st.info("💡 Try logging in as **shubham** if you have checked the password in terminal logs.")

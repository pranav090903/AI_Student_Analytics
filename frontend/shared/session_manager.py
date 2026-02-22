import streamlit as st


def init_session():
    if "token" not in st.session_state:
        st.session_state.token = None
        st.session_state.role = None
        st.session_state.username = None
        st.session_state.logged_in = False


def save_login(token, role, username):
    st.session_state.token = token
    st.session_state.role = role
    st.session_state.username = username
    st.session_state.logged_in = True


def logout():
    st.session_state.token = None
    st.session_state.logged_in = False

import streamlit as st
import requests

# ================= CONFIG =================

BACKEND_URL = "http://127.0.0.1:8002"


# ================= ROLE PROTECTION =================

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please Login First")
    st.stop()

if st.session_state.role != "Teacher":
    st.error("Unauthorized Access - Teacher Only")
    st.stop()


# ================= PAGE UI =================

st.title("🤖 Teacher AI Academic Copilot")
st.write("Ask questions about student performance, trends, or academic insights.")


# ================= CHAT HISTORY INIT =================

if "teacher_chat_history" not in st.session_state:
    st.session_state.teacher_chat_history = []


# ================= DISPLAY OLD CHAT =================

for msg in st.session_state.teacher_chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ================= CHAT INPUT =================

user_input = st.chat_input("Ask AI about student performance...")


# ================= SEND MESSAGE =================

if user_input:

    # Show user message
    st.chat_message("user").markdown(user_input)

    # Save to history
    st.session_state.teacher_chat_history.append({
        "role": "user",
        "content": user_input
    })

    # ================= API CALL =================

    try:
        response = requests.post(
            f"{BACKEND_URL}/copilot/chat",
            json={
                "message": user_input
            },
            headers={
                "Authorization": f"Bearer {st.session_state.token}"
            },
            timeout=60
        )

        if response.status_code == 200:

            ai_response = response.json()["response"]

        else:
            ai_response = f"Error: {response.text}"

    except Exception as e:
        ai_response = f"Connection Error: {str(e)}"


    # ================= SHOW AI RESPONSE =================

    with st.chat_message("assistant"):
        st.markdown(ai_response)

    # Save AI message
    st.session_state.teacher_chat_history.append({
        "role": "assistant",
        "content": ai_response
    })


# ================= SIDEBAR ACTIONS =================

st.sidebar.title("Teacher Tools")

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.teacher_chat_history = []
    st.rerun()

st.sidebar.info("AI Copilot helps analyze student performance trends.")

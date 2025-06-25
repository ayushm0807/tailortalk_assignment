import streamlit as st
import requests
import uuid

st.title("📅 BookMySlot: AI Meeting Scheduler")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Initialize chat session
if "chat" not in st.session_state:
    st.session_state.chat = []
    # Show greeting message only on first load
    st.session_state.chat.append(("agent", "👋 Hello! I can help you book a slot."))

# User input
user_input = st.chat_input("Ask me to schedule a meeting...")

if user_input:
    st.session_state.chat.append(("user", user_input))

    try:
        res = requests.post("http://localhost:8000/chat", json={
            "message": user_input,
            "session_id": st.session_state.session_id
        })
        res.raise_for_status()
        response = res.json().get("response", "⚠️ No response from agent.")
    except requests.exceptions.ConnectionError:
        response = "❌ Could not connect to backend (FastAPI)"
    except requests.exceptions.RequestException as e:
        response = f"⚠️ Request error: {str(e)}"

    st.session_state.chat.append(("agent", response))

# 💬 Render chat history
for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.markdown(msg)

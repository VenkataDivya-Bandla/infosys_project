import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Document Chat", layout="wide")
st.title("AI Document Search & Chat")

st.info(
    "📂 Documents are loaded automatically from the server's /data folder.\n\n"
    "Ask questions about the documents. Chat history will persist until you close this browser tab."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = "default"


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


user_input = st.chat_input("Ask a question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    payload = {
        "q": user_input,
        "session_id": st.session_state.session_id
    }

    r = requests.post(f"{API_URL}/query", json=payload)

    if r.status_code == 200:
        data = r.json()
        answer = data.get("answer", str(data))
    else:
        answer = f"Query failed: {r.text}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()

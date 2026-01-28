import streamlit as st
from backend_main import query_handler

st.set_page_config(page_title="AI Document Chat", layout="wide")
st.title("AI Document Search & Chat")

st.info(
    "📂 Documents are loaded automatically from the server's /data folder.\n\n"
    "Ask questions about the documents. Chat history will persist until you close this browser tab."
)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = "default"

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Ask a question...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    try:
        answer = query_handler(
            question=user_input,
            session_id=st.session_state.session_id
        )
    except Exception as e:
        answer = f"❌ Error: {e}"

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    st.rerun()

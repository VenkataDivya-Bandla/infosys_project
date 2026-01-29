import streamlit as st
import os
from backend_main import query_handler
from ingestion import ingest_document

st.set_page_config(page_title="AI Document Chat", layout="wide")
st.title("AI Document Search & Chat")

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

st.info(
    "📂 Upload documents or ask questions about already ingested files.\n\n"
    "Supported formats: PDF, DOCX, TXT"
)

# -------------------------
# 📤 FILE UPLOAD SECTION
# -------------------------
uploaded_file = st.file_uploader(
    "Upload a document",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    file_path = os.path.join(DATA_DIR, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Ingesting document..."):
        ingest_document(file_path)

    st.success(f"✅ {uploaded_file.name} uploaded and ingested successfully")

# -------------------------
# 💬 CHAT SECTION
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = "default"

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

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

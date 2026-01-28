import os

from ingestion import ingest_document
from retriever import query_documents, load_index
from memory import ConversationMemory

# -----------------------------
# Global initialization
# -----------------------------

memory = ConversationMemory()

DATA_DIR = "data"
ORG_NAME = "ABC Corp"


def ingest_existing_documents():
    if not os.path.exists(DATA_DIR):
        print("No data directory found. Skipping ingestion.")
        return

    for fname in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, fname)
        if fname.lower().endswith((".pdf", ".docx", ".txt")):
            print(f"Ingesting existing file: {fname}")
            ingest_document(path)


# Load FAISS index if exists
load_index()

# Ingest documents at startup
ingest_existing_documents()

# -----------------------------
# 🔥 STREAMLIT ENTRY FUNCTION
# -----------------------------

def query_handler(question: str, session_id: str = "default") -> str:
    """
    Handles a user query and returns an answer string.
    This function is called directly from Streamlit UI.
    """
    history = memory.get(session_id)

    result = query_documents(question, history)

    answer = result.get("answer", "")
    answer = answer.replace("{ORGANIZATION NAME}", ORG_NAME)

    memory.add(session_id, question, answer)

    return answer

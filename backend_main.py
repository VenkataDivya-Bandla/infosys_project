import os

from ingestion import ingest_document
from retriever import query_documents, load_index
from memory import ConversationMemory

# -----------------------------
# Global objects (SAFE)
# -----------------------------
memory = ConversationMemory()

DATA_DIR = "data"
ORG_NAME = "ABC Corp"

_backend_initialized = False


# -----------------------------
# Lazy initialization
# -----------------------------
def ingest_existing_documents():
    if not os.path.exists(DATA_DIR):
        print("No data directory found. Skipping ingestion.")
        return

    for fname in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, fname)
        if fname.lower().endswith((".pdf", ".docx", ".txt")):
            print(f"Ingesting file: {fname}")
            ingest_document(path)


def init_backend():
    """
    Runs ONLY once, on first query.
    Prevents Streamlit startup crash.
    """
    global _backend_initialized

    if _backend_initialized:
        return

    print("Initializing backend (FAISS + documents)...")
    load_index()
    ingest_existing_documents()

    _backend_initialized = True
    print("Backend initialized successfully.")


# -----------------------------
# Streamlit entry function
# -----------------------------
def query_handler(question: str, session_id: str) -> str:
    init_backend()  # 🔥 critical

    history = memory.get(session_id)
    result = query_documents(question, history)

    answer = result.get("answer", "No answer generated.")
    answer = answer.replace("{ORGANIZATION NAME}", ORG_NAME)

    memory.add(session_id, question, answer)
    return answer

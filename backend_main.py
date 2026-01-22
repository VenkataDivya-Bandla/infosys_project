import os
from fastapi import FastAPI
from pydantic import BaseModel

from ingestion import ingest_document
from retriever import query_documents, load_index
from memory import ConversationMemory

app = FastAPI()
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

# Ingest on startup
ingest_existing_documents()


class QueryRequest(BaseModel):
    q: str
    session_id: str = "default"


@app.post("/query")
async def query(req: QueryRequest):
    try:
        history = memory.get(req.session_id)

        result = query_documents(req.q, history)

        answer = result["answer"]
        answer = answer.replace("{ORGANIZATION NAME}", ORG_NAME)

        memory.add(req.session_id, req.q, answer)

        return {
            "answer": answer,
            "sources": result.get("sources", [])
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/")
async def root():
    return {
        "status": "AI Document Search API is running. Documents are loaded from /data on startup."
    }

import os
import faiss
import numpy as np
import pickle

from embeddings import embed_texts
from llm import generate_answer

INDEX_FILE = "faiss.index"
META_FILE = "meta.pkl"

dim = 384
index = faiss.IndexFlatL2(dim)

texts = []
metadatas = []

TOP_K = 4
MIN_CHUNK_LEN = 50


def save_index():
    faiss.write_index(index, INDEX_FILE)
    with open(META_FILE, "wb") as f:
        pickle.dump((texts, metadatas), f)


def load_index():
    global index, texts, metadatas
    if os.path.exists(INDEX_FILE) and os.path.exists(META_FILE):
        index = faiss.read_index(INDEX_FILE)
        with open(META_FILE, "rb") as f:
            texts, metadatas = pickle.load(f)


def add_embeddings(chunks, embeddings, metas):
    global texts, metadatas

    index.add(np.array(embeddings).astype("float32"))
    texts.extend(chunks)
    metadatas.extend(metas)

    save_index()


def query_documents(query, history=None):
    if index.ntotal == 0:
        return {
            "answer": "No documents loaded.",
            "sources": []
        }

    history = history or []

    q_emb = embed_texts([query])[0]
    D, I = index.search(np.array([q_emb]).astype("float32"), TOP_K)

    retrieved_chunks = []
    retrieved_sources = []

    for idx in I[0]:
        if idx < 0 or idx >= len(texts):
            continue

        chunk = texts[idx].strip()
        if len(chunk) < MIN_CHUNK_LEN:
            continue

        retrieved_chunks.append(chunk)
        retrieved_sources.append(metadatas[idx])

    if not retrieved_chunks:
        return {
            "answer": "I could not find relevant information in the documents.",
            "sources": []
        }

    memory_context = []
    for h in history[-3:]:
        memory_context.append(
            f"Previous question: {h['q']}\nPrevious answer: {h['a']}"
        )

    final_context = []
    final_context.extend(memory_context)
    final_context.extend(retrieved_chunks)

    answer = generate_answer(
        query=query,
        context=final_context,
        history=history
    )

    return {
        "answer": answer,
        "sources": retrieved_sources
    }

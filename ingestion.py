import os
import fitz  # PyMuPDF
import docx

from embeddings import embed_texts
from retriever import add_embeddings


def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def ingest_document(path):
    if path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(path)
    elif path.lower().endswith(".docx"):
        text = extract_text_from_docx(path)
    elif path.lower().endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        return

    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)

    metas = [{"source": os.path.basename(path)} for _ in chunks]

    add_embeddings(chunks, embeddings, metas)

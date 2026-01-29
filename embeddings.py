from sentence_transformers import SentenceTransformer

_model = None  # lazy-loaded model


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_texts(texts):
    model = get_model()
    embeddings = model.encode(texts)
    return embeddings.tolist()

"""
Builds and loads a FAISS vector index over the target database's schema
(table names, column names/types, and descriptions), enabling semantic
retrieval of "which tables are relevant to this question" in rag.py.
"""
import json
import logging
import os

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import settings

logger = logging.getLogger(__name__)

_model: SentenceTransformer | None = None


def get_embedding_model() -> SentenceTransformer:
    """Lazily loads the sentence-transformer model once per process."""
    global _model
    if _model is None:
        logger.info(f"Loading embedding model: {settings.embedding_model}")
        _model = SentenceTransformer(settings.embedding_model)
    return _model


def embed_texts(texts: list[str]) -> np.ndarray:
    model = get_embedding_model()
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return embeddings.astype("float32")


def build_schema_index(schema_chunks: list[dict]) -> None:
    """
    schema_chunks: list of {"table_name": str, "text": str} where `text` is a
    human-readable description of the table + its columns, used as the
    embedding source. Persists both the FAISS index and a sidecar metadata
    JSON (FAISS only stores vectors, not the original text/table names).
    """
    texts = [chunk["text"] for chunk in schema_chunks]
    vectors = embed_texts(texts)

    dimension = vectors.shape[1]
    index = faiss.IndexFlatIP(dimension)  # inner product on normalized vectors = cosine similarity
    index.add(vectors)

    os.makedirs(os.path.dirname(settings.faiss_index_path), exist_ok=True)
    faiss.write_index(index, f"{settings.faiss_index_path}.index")

    with open(f"{settings.faiss_index_path}.meta.json", "w") as f:
        json.dump(schema_chunks, f)

    logger.info(f"Built FAISS index with {len(schema_chunks)} schema chunks.")


def load_schema_index() -> tuple[faiss.Index, list[dict]]:
    index_path = f"{settings.faiss_index_path}.index"
    meta_path = f"{settings.faiss_index_path}.meta.json"

    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        raise FileNotFoundError(
            "Schema index not found. Run `python embeddings/build_index.py` first."
        )

    index = faiss.read_index(index_path)
    with open(meta_path) as f:
        metadata = json.load(f)

    return index, metadata


def search_schema(query: str, top_k: int = 4) -> list[dict]:
    index, metadata = load_schema_index()
    query_vector = embed_texts([query])
    scores, indices = index.search(query_vector, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        chunk = metadata[idx].copy()
        chunk["similarity"] = float(score)
        results.append(chunk)
    return results
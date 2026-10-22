"""
Retrieval-Augmented Generation layer: turns a user's natural-language
question into a compact, relevant slice of the database schema to hand
the LLM, instead of dumping the entire schema into every prompt.
"""
import logging

from app.exceptions import SchemaRetrievalError
from app.services.embeddings import search_schema
from app.utils import truncate_text

logger = logging.getLogger(__name__)


def retrieve_schema_context(question: str, top_k: int = 4) -> str:
    """
    Returns a formatted string of the top-k most relevant table schemas
    for this question, ready to be injected into the SQL generation prompt.
    """
    try:
        results = search_schema(question, top_k=top_k)
    except FileNotFoundError as exc:
        logger.error(str(exc))
        raise SchemaRetrievalError(str(exc)) from exc

    if not results:
        raise SchemaRetrievalError("No relevant schema found for this question.")

    formatted_chunks = []
    for chunk in results:
        formatted_chunks.append(
            f"Table: {chunk['table_name']}\n{truncate_text(chunk['text'], 800)}"
        )

    return "\n\n".join(formatted_chunks)


def get_known_table_names(question: str, top_k: int = 4) -> set[str]:
    """Used by the validator to check the generated SQL only references
    tables that were actually retrieved (defense against hallucinated tables
    outside what was even offered as context)."""
    results = search_schema(question, top_k=top_k)
    return {r["table_name"].lower() for r in results}
"""
Offline build step: introspects the target analytics database's schema,
turns each table into a human-readable text description, embeds those
descriptions, and persists a FAISS index for rag.py to query at runtime.

Run this once after seeding the database, and again any time the schema
changes:
    python embeddings/build_index.py
"""
import logging
import sys
from pathlib import Path

from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError

sys.path.append(str(Path(__file__).resolve().parent.parent / "backend"))

from app.config import settings                       # noqa: E402
from app.services.embeddings import build_schema_index  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# Tables belonging to QueryPilot's own app (auth/history), not the
# end-user analytics data — must be excluded so the LLM never generates
# SQL against them.
EXCLUDED_TABLES = {"users", "query_history"}


def _describe_table(inspector, table_name: str) -> dict:
    """Builds a natural-language-ish description of one table's structure,
    which is what actually gets embedded (not the raw DDL) — descriptive
    text embeds more meaningfully than raw SQL syntax."""
    columns = inspector.get_columns(table_name)
    pk_columns = set(inspector.get_pk_constraint(table_name).get("constrained_columns", []))
    fks = inspector.get_foreign_keys(table_name)

    column_descriptions = []
    column_meta = []
    for col in columns:
        col_name = col["name"]
        col_type = str(col["type"])
        flags = []
        if col_name in pk_columns:
            flags.append("primary key")
        for fk in fks:
            if col_name in fk.get("constrained_columns", []):
                flags.append(f"foreign key -> {fk['referred_table']}.{fk['referred_columns'][0]}")
        flag_str = f" ({', '.join(flags)})" if flags else ""
        column_descriptions.append(f"{col_name} [{col_type}]{flag_str}")
        column_meta.append({"name": col_name, "type": col_type})

    text_description = (
        f"Table '{table_name}' has columns: {', '.join(column_descriptions)}."
    )

    return {
        "table_name": table_name,
        "text": text_description,
        "columns": column_meta,
    }


def build_index_from_live_schema() -> None:
    logger.info(f"Connecting to database to introspect schema...")
    engine = create_engine(settings.database_url)

    try:
        inspector = inspect(engine)
        all_tables = inspector.get_table_names()
    except SQLAlchemyError as exc:
        logger.error(f"Failed to introspect database schema: {exc}")
        sys.exit(1)

    target_tables = [t for t in all_tables if t not in EXCLUDED_TABLES]

    if not target_tables:
        logger.error(
            "No analytics tables found to index. Did you run `python database/seed.py` first?"
        )
        sys.exit(1)

    logger.info(f"Found {len(target_tables)} analytics tables to index: {target_tables}")

    schema_chunks = []
    for table_name in target_tables:
        try:
            schema_chunks.append(_describe_table(inspector, table_name))
        except SQLAlchemyError as exc:
            logger.warning(f"Skipping table '{table_name}' due to introspection error: {exc}")
            continue

    try:
        build_schema_index(schema_chunks)
    except Exception as exc:
        logger.error(f"Failed to build/persist FAISS index: {exc}", exc_info=True)
        sys.exit(1)

    logger.info(f"Schema index built and saved to '{settings.faiss_index_path}.index'")


if __name__ == "__main__":
    build_index_from_live_schema()
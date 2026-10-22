"""
Runs schema.sql then seed_data.sql against DATABASE_URL.
Idempotent: safe to re-run (schema uses IF NOT EXISTS, seed data uses
ON CONFLICT DO NOTHING).
"""
import logging
import sys
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Allow running this script directly (python database/seed.py) by adding
# backend/ to the path so we can reuse the app's config instead of
# duplicating the DATABASE_URL parsing logic.
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend"))

from app.config import settings  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

SCHEMA_PATH = Path(__file__).parent / "schema.sql"
SEED_DATA_PATH = Path(__file__).parent / "seed_data.sql"


def _run_sql_file(engine, path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"SQL file not found: {path}")

    sql_text = path.read_text(encoding="utf-8")
    with engine.begin() as conn:  # single transaction: all-or-nothing
        conn.execute(text(sql_text))
    logger.info(f"Executed {path.name} successfully.")


def main() -> None:
    logger.info(f"Connecting to database: {settings.database_url.split('@')[-1]}")  # avoid logging credentials
    engine = create_engine(settings.database_url)

    try:
        _run_sql_file(engine, SCHEMA_PATH)
        _run_sql_file(engine, SEED_DATA_PATH)
    except FileNotFoundError as exc:
        logger.error(str(exc))
        sys.exit(1)
    except SQLAlchemyError as exc:
        logger.error(f"Database error while seeding: {exc}")
        sys.exit(1)
    else:
        logger.info("Database seeding complete.")


if __name__ == "__main__":
    main()
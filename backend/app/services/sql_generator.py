"""
Orchestrates LLM calls for SQL generation, self-correction, and
plain-English explanation. Does not execute SQL or validate safety —
that's sql_validator.py and sql_executor.py's job respectively.
"""
import logging

from app.prompts import SQL_GENERATION_PROMPT, SQL_CORRECTION_PROMPT, SQL_EXPLANATION_PROMPT
from app.services.llm_client import generate
from app.config import settings

logger = logging.getLogger(__name__)


def generate_sql(question: str, schema_context: str) -> str:
    prompt = SQL_GENERATION_PROMPT.format(
        schema_context=schema_context,
        question=question,
        max_rows=settings.max_query_rows,
    )
    sql = generate(prompt, temperature=0.1)
    logger.info(f"Generated SQL for question '{question[:60]}...': {sql[:120]}")
    return sql


def correct_sql(question: str, schema_context: str, failed_sql: str, error_message: str) -> str:
    prompt = SQL_CORRECTION_PROMPT.format(
        question=question,
        schema_context=schema_context,
        failed_sql=failed_sql,
        error_message=error_message,
    )
    corrected = generate(prompt, temperature=0.1)
    logger.info(f"Corrected SQL after error '{error_message[:80]}': {corrected[:120]}")
    return corrected


def explain_sql(sql: str) -> str:
    prompt = SQL_EXPLANATION_PROMPT.format(sql=sql)
    return generate(prompt, temperature=0.3, max_tokens=200)
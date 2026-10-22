"""
Guardrail layer: inspects generated SQL before it's ever executed.
This is the single most safety-critical file in the backend.
"""
import re
import logging

import sqlparse

from app.config import settings
from app.exceptions import DangerousSQLError
from app.utils import extract_table_names_from_sql

logger = logging.getLogger(__name__)

BLOCKED_KEYWORDS = {
    "DELETE", "UPDATE", "DROP", "ALTER", "TRUNCATE", "INSERT",
    "CREATE", "GRANT", "REVOKE", "EXEC", "EXECUTE", "MERGE",
}


def _strip_code_fences(sql: str) -> str:
    """LLMs sometimes wrap SQL in ```sql ... ``` despite instructions not to."""
    sql = re.sub(r"^```sql\s*|^```\s*|```$", "", sql.strip(), flags=re.IGNORECASE | re.MULTILINE)
    return sql.strip().rstrip(";").strip()


def validate_sql(raw_sql: str, known_tables: set[str] | None = None) -> str:
    """
    Runs the full guardrail pipeline. Returns cleaned, validated SQL,
    or raises DangerousSQLError. This function never executes SQL itself
    — it only inspects the text.
    """
    sql = _strip_code_fences(raw_sql)

    if not sql:
        raise DangerousSQLError("Generated SQL was empty.")

    # 1. Must be a single statement (block statement chaining / SQL injection via ';')
    statements = [s for s in sqlparse.split(sql) if s.strip()]
    if len(statements) != 1:
        raise DangerousSQLError("Only a single SQL statement is allowed.")

    parsed = sqlparse.parse(sql)[0]
    statement_type = parsed.get_type()

    # 2. Must be SELECT only
    if statement_type != "SELECT":
        raise DangerousSQLError(f"Only SELECT statements are allowed, got: {statement_type}")

    # 3. Keyword denylist as a second, belt-and-suspenders check
    upper_sql = sql.upper()
    for keyword in BLOCKED_KEYWORDS:
        if re.search(rf"\b{keyword}\b", upper_sql):
            raise DangerousSQLError(f"Disallowed keyword detected: {keyword}")

    # 4. Enforce LIMIT
    if "LIMIT" not in upper_sql:
        sql = f"{sql}\nLIMIT {settings.max_query_rows}"
    else:
        # if a LIMIT exists but exceeds the configured cap, clamp it
        match = re.search(r"LIMIT\s+(\d+)", upper_sql)
        if match and int(match.group(1)) > settings.max_query_rows:
            sql = re.sub(r"LIMIT\s+\d+", f"LIMIT {settings.max_query_rows}", sql, flags=re.IGNORECASE)

    # 5. Hallucinated table check (only if we were given retrieved tables to check against)
    if known_tables:
        referenced_tables = extract_table_names_from_sql(sql)
        unknown = referenced_tables - known_tables
        if unknown:
            raise DangerousSQLError(
                f"Query references tables not found in schema context: {', '.join(unknown)}"
            )

    logger.info(f"SQL validated successfully: {sql[:120]}...")
    return sql
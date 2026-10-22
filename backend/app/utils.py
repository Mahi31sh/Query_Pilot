"""
Small stateless helper functions shared across services.
"""
import re
import time
from functools import wraps


def slugify_table_name(name: str) -> str:
    """Normalize a table/column name for safe comparison (lowercase, no quotes)."""
    return re.sub(r'[`"\[\]]', "", name).strip().lower()


def extract_table_names_from_sql(sql: str) -> set[str]:
    """
    Best-effort extraction of table names referenced after FROM/JOIN.
    Used by the validator to check for hallucinated tables — not a full
    SQL parser, but it covers explicit joins, comma-separated table lists,
    and subqueries more reliably than a single regex.
    """

    try:
        import sqlparse
        from sqlparse.sql import Identifier, IdentifierList, Parenthesis, Statement
        from sqlparse.tokens import Keyword
    except Exception:
        pattern = re.compile(r"\b(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_\.]*)", re.IGNORECASE)
        matches = pattern.findall(sql)
        return {slugify_table_name(m.split(".")[-1]) for m in matches}

    def collect_from_token(token) -> set[str]:
        tables: set[str] = set()
        if isinstance(token, IdentifierList):
            for identifier in token.get_identifiers():
                tables.update(collect_from_token(identifier))
        elif isinstance(token, Identifier):
            real_name = token.get_real_name() or token.get_name() or token.value
            if real_name:
                tables.add(slugify_table_name(real_name.split(".")[-1]))
        elif isinstance(token, Parenthesis):
            inner_sql = token.value[1:-1].strip()
            if inner_sql:
                tables.update(extract_table_names_from_sql(inner_sql))
        return tables

    parsed = sqlparse.parse(sql)
    if not parsed:
        return set()

    statement: Statement = parsed[0]
    tables: set[str] = set()
    for index, token in enumerate(statement.tokens):
        token_value = getattr(token, "value", "")
        upper_value = token_value.upper() if token_value else ""
        if token.ttype is Keyword and (upper_value == "FROM" or "JOIN" in upper_value):
            next_index, next_token = statement.token_next(index, skip_ws=True, skip_cm=True)
            if next_token is not None:
                tables.update(collect_from_token(next_token))

    return tables


def timed(func):
    """Decorator that measures execution time in milliseconds and attaches
    it to the return value if the return value is a dict with an 'meta' key,
    otherwise just logs it via return tuple for the caller to use."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1000
        return result, elapsed_ms
    return wrapper


def truncate_text(text: str, max_len: int = 2000) -> str:
    """Prevent runaway prompt sizes when embedding table descriptions or errors."""
    return text if len(text) <= max_len else text[: max_len - 3] + "..."
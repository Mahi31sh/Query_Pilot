"""
All LLM prompt templates in one place, so tone, format constraints,
and few-shot examples are easy to iterate on without touching service logic.
"""

SQL_GENERATION_PROMPT = """You are a senior data analyst who writes precise, safe PostgreSQL queries.

DATABASE SCHEMA CONTEXT (retrieved as relevant to the question):
{schema_context}

RULES:
- Only use tables and columns that appear in the schema context above. Never invent table or column names.
- Only generate a single SELECT statement. Never generate INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE.
- Always include a LIMIT clause (max {max_rows} rows) unless the question asks for an aggregate that returns one row.
- Use explicit JOIN syntax, not comma joins.
- Return ONLY the raw SQL query. No markdown code fences, no explanation, no trailing semicolon commentary.

USER QUESTION:
{question}

SQL QUERY:"""


SQL_CORRECTION_PROMPT = """The following PostgreSQL query failed when executed.

ORIGINAL QUESTION:
{question}

SCHEMA CONTEXT:
{schema_context}

FAILED SQL:
{failed_sql}

DATABASE ERROR:
{error_message}

Fix the query. Follow the same rules as before: only tables/columns from the schema context,
SELECT-only, include a LIMIT clause, explicit JOINs. Return ONLY the corrected raw SQL query."""


SQL_EXPLANATION_PROMPT = """Explain the following SQL query in 2-3 plain-English sentences,
for a non-technical business user. Do not repeat the raw SQL back. Focus on what data
it retrieves and how it's filtered/aggregated.

SQL:
{sql}"""


CHART_TYPE_PROMPT = """Given this user question and the resulting column names, decide the single
best chart type to visualize the result. Respond with ONLY one word, no punctuation:
bar, pie, line, scatter, table, or kpi.

Guidance:
- kpi: result is a single row with one or two aggregate numbers (e.g. total revenue).
- pie: categorical breakdown of parts of a whole, few categories (<=8).
- bar: categorical comparison across many categories.
- line: a time-series / trend over dates or sequential periods.
- scatter: two numeric columns being compared for correlation.
- table: anything else, or result has many columns / doesn't fit the above.

QUESTION: {question}
COLUMNS: {columns}
SAMPLE ROW: {sample_row}

CHART TYPE:"""
"""
Decides how to visualize a query result and shapes the data into the
exact structure the frontend's Recharts components expect.
"""
import logging

from app.prompts import CHART_TYPE_PROMPT
from app.services.llm_client import generate

logger = logging.getLogger(__name__)

VALID_CHART_TYPES = {"bar", "pie", "line", "scatter", "table", "kpi"}


def _decide_chart_type(question: str, columns: list[str], sample_row: dict) -> str:
    if len(columns) == 0:
        return "table"

    prompt = CHART_TYPE_PROMPT.format(question=question, columns=columns, sample_row=sample_row)
    raw = generate(prompt, temperature=0.0, max_tokens=10).strip().lower()

    return raw if raw in VALID_CHART_TYPES else "table"


def build_chart_spec(question: str, columns: list[str], rows: list[dict]) -> dict:
    """Returns a dict matching the frontend's ChartSpec shape."""
    if not rows:
        return {"chart_type": "table", "data": [], "x_key": None, "y_key": None, "label": None}

    chart_type = _decide_chart_type(question, columns, rows[0])

    if chart_type == "kpi":
        return {
            "chart_type": "kpi",
            "data": rows[:1],
            "x_key": None,
            "y_key": columns[0] if columns else None,
            "label": columns[0].replace("_", " ").title() if columns else None,
        }

    if chart_type in {"bar", "pie", "line", "scatter"} and len(columns) >= 2:
        return {
            "chart_type": chart_type,
            "data": rows,
            "x_key": columns[0],
            "y_key": columns[1],
            "label": None,
        }

    # fallback: not enough columns for a meaningful chart, show a table instead
    return {"chart_type": "table", "data": rows, "x_key": None, "y_key": None, "label": None}
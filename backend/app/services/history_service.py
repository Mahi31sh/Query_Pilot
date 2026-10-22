"""
Thin service layer between the query pipeline / history router and crud.py,
so routers never touch the ORM directly.
"""
from uuid import UUID

from sqlalchemy.orm import Session

from app import crud


def log_query(
    db: Session,
    user_id: UUID,
    question: str,
    generated_sql: str,
    explanation: str,
    success: bool,
    error_message: str | None,
    retry_count: int,
    row_count: int | None,
    chart_type: str | None,
):
    return crud.create_query_history(
        db=db,
        user_id=user_id,
        question=question,
        generated_sql=generated_sql,
        explanation=explanation,
        success=success,
        error_message=error_message,
        retry_count=retry_count,
        row_count=row_count,
        chart_type=chart_type,
    )


def get_history(db: Session, user_id: UUID, limit: int = 50, offset: int = 0):
    return crud.get_user_history(db, user_id, limit=limit, offset=offset)
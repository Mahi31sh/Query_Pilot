"""
Database access functions — the only place raw SQLAlchemy queries
against QueryPilot's own app tables (users, query_history) should live.
"""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app import models, schemas
from app.auth import hash_password


# ---------- Users ----------

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: str) -> Optional[models.User]:
    try:
        return db.query(models.User).filter(models.User.id == UUID(user_id)).first()
    except ValueError:
        return None


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    user = models.User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        full_name=user_in.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------- Query history ----------

def create_query_history(
    db: Session,
    user_id: UUID,
    question: str,
    generated_sql: str,
    explanation: str,
    success: bool,
    error_message: Optional[str],
    retry_count: int,
    row_count: Optional[int],
    chart_type: Optional[str],
) -> models.QueryHistory:
    entry = models.QueryHistory(
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
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_user_history(db: Session, user_id: UUID, limit: int = 50, offset: int = 0):
    return (
        db.query(models.QueryHistory)
        .filter(models.QueryHistory.user_id == user_id)
        .order_by(desc(models.QueryHistory.created_at))
        .offset(offset)
        .limit(limit)
        .all()
    )
"""
SQLAlchemy ORM models for QueryPilot's own application database
(users, query history) — separate from whatever end-user database
the user connects QueryPilot to for analytics.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Text, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    queries = relationship("QueryHistory", back_populates="user", cascade="all, delete-orphan")


class QueryHistory(Base):
    __tablename__ = "query_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    question = Column(Text, nullable=False)
    generated_sql = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)

    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)

    row_count = Column(Integer, nullable=True)
    chart_type = Column(String, nullable=True)  # bar | pie | line | scatter | table | kpi

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="queries")
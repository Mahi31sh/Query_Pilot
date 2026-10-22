"""
Pydantic schemas — the request/response contracts for the API.
Kept separate from models.py (ORM) so DB structure and API surface
can evolve independently.
"""
from datetime import datetime
from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


# ---------- Auth ----------

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    full_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Query pipeline ----------

class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)


class ChartSpec(BaseModel):
    chart_type: str          # bar | pie | line | scatter | table | kpi
    data: list[dict[str, Any]]
    x_key: Optional[str] = None
    y_key: Optional[str] = None
    label: Optional[str] = None


class QueryResponse(BaseModel):
    question: str
    generated_sql: str
    explanation: str
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int
    chart: ChartSpec
    retry_count: int
    execution_time_ms: float


# ---------- History ----------

class QueryHistoryOut(BaseModel):
    id: UUID
    question: str
    generated_sql: str
    success: bool
    error_message: Optional[str] = None
    retry_count: int
    row_count: Optional[int] = None
    chart_type: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Schema introspection ----------

class TableSchemaOut(BaseModel):
    table_name: str
    columns: list[dict[str, str]]
    description: Optional[str] = None
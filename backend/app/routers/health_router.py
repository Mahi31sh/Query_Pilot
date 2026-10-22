"""
Liveness/readiness check, including a real DB connectivity test —
what a load balancer or uptime monitor would hit.
"""
from fastapi import APIRouter
from sqlalchemy import text

from app.database import engine

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check():
    db_status = "ok"
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        db_status = "unreachable"

    return {"status": "ok" if db_status == "ok" else "degraded", "database": db_status}
"""
Read-only endpoint for a user's past queries.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import schemas, models
from app.auth import get_current_user
from app.database import get_db
from app.services.history_service import get_history

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("", response_model=list[schemas.QueryHistoryOut])
def list_history(
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_history(db, current_user.id, limit=limit, offset=offset)
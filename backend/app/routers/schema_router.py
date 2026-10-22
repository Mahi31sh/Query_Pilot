"""
Exposes the database schema QueryPilot has indexed, mainly to power a
"suggested questions" / schema browser feature on the frontend.
"""
from fastapi import APIRouter, Depends

from app import models, schemas
from app.auth import get_current_user
from app.services.embeddings import load_schema_index

router = APIRouter(prefix="/api/schema", tags=["schema"])


@router.get("/tables", response_model=list[schemas.TableSchemaOut])
def list_indexed_tables(current_user: models.User = Depends(get_current_user)):
    _, metadata = load_schema_index()
    return [
        schemas.TableSchemaOut(
            table_name=chunk["table_name"],
            columns=chunk.get("columns", []),
            description=chunk.get("text"),
        )
        for chunk in metadata
    ]
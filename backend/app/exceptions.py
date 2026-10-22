"""
Custom exception types and their FastAPI exception handlers.
Keeps error semantics consistent across the whole API instead of
ad-hoc HTTPException calls scattered through routers.
"""
import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class QueryPilotException(Exception):
    """Base class for all app-specific exceptions."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class DangerousSQLError(QueryPilotException):
    """Raised when generated SQL contains a blocked operation."""
    def __init__(self, message: str = "Generated SQL contains a disallowed operation."):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)


class SQLGenerationError(QueryPilotException):
    """Raised when the LLM fails to produce usable SQL after all retries."""
    def __init__(self, message: str = "Could not generate a valid SQL query for this question."):
        super().__init__(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class SchemaRetrievalError(QueryPilotException):
    """Raised when the RAG layer can't retrieve relevant schema context."""
    def __init__(self, message: str = "Could not retrieve database schema context."):
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def querypilot_exception_handler(request: Request, exc: QueryPilotException):
    logger.warning(f"{exc.__class__.__name__} on {request.url.path}: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.__class__.__name__, "message": exc.message},
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "InternalServerError", "message": "Something went wrong. Please try again."},
    )
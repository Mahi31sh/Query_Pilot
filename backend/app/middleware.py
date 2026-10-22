"""
Custom ASGI middleware: request timing and request logging.
"""
import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs every request with a correlation ID and duration, and attaches
    an X-Process-Time-Ms header to the response for client-side visibility."""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        start_time = time.perf_counter()

        logger.info(f"[{request_id}] --> {request.method} {request.url.path}")

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000
        response.headers["X-Process-Time-Ms"] = f"{duration_ms:.2f}"
        response.headers["X-Request-ID"] = request_id

        logger.info(
            f"[{request_id}] <-- {response.status_code} "
            f"{request.method} {request.url.path} ({duration_ms:.2f}ms)"
        )
        return response
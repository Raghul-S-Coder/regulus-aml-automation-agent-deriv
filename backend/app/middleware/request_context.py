import asyncio
import time
import uuid

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.config.settings import settings
from app.utils.datetime_utils import utc_now


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Middleware that extracts standard headers, binds request context to loguru,
    and enforces a fail-fast timeout on all API requests."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Extract or generate request ID
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        forwarded_for = request.headers.get("X-Forwarded-For", "unknown")
        device_id = request.headers.get("X-Device-Id", "unknown")

        # Store on request state for use in exception handlers and controllers
        request.state.request_id = request_id
        request.state.forwarded_for = forwarded_for
        request.state.device_id = device_id

        # Bind request_id to loguru context
        with logger.contextualize(request_id=request_id):
            logger.info(f"Incoming {request.method} {request.url.path} | IP: {forwarded_for} | Device: {device_id}")

            start_time = time.perf_counter()
            try:
                response = await asyncio.wait_for(
                    call_next(request),
                    timeout=settings.API_TIMEOUT_SECONDS,
                )
            except asyncio.TimeoutError:
                duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
                logger.error(
                    f"Request timeout after {duration_ms}ms | "
                    f"{request.method} {request.url.path} exceeded {settings.API_TIMEOUT_SECONDS}s limit"
                )
                response = JSONResponse(
                    status_code=504,
                    content={
                        "success": False,
                        "error_code": "REQUEST_TIMEOUT",
                        "message": f"Request timed out after {settings.API_TIMEOUT_SECONDS} seconds",
                        "request_id": request_id,
                        "timestamp": utc_now().isoformat(),
                    },
                )

            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.info(
                f"Completed {request.method} {request.url.path} | Status: {response.status_code} | Duration: {duration_ms}ms"
            )

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        return response

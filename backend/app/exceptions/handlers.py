from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger

from app.exceptions.base_exception import AMLException
from app.exceptions.error_codes import INTERNAL_ERROR, VALIDATION_ERROR
from app.utils.datetime_utils import utc_now


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers on the FastAPI app."""

    @app.exception_handler(AMLException)
    async def aml_exception_handler(request: Request, exc: AMLException) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "unknown")
        logger.bind(request_id=request_id).warning(f"{exc.error_code}: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error_code": exc.error_code,
                "message": exc.message,
                "request_id": request_id,
                "timestamp": utc_now().isoformat(),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "unknown")
        errors = exc.errors()
        message = "; ".join(f"{e['loc'][-1]}: {e['msg']}" for e in errors) if errors else "Validation error"
        logger.bind(request_id=request_id).warning(f"{VALIDATION_ERROR}: {message}")
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error_code": VALIDATION_ERROR,
                "message": message,
                "request_id": request_id,
                "timestamp": utc_now().isoformat(),
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "unknown")
        logger.bind(request_id=request_id).exception(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error_code": INTERNAL_ERROR,
                "message": "Internal server error",
                "request_id": request_id,
                "timestamp": utc_now().isoformat(),
            },
        )

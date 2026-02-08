from typing import Any, Generic, TypeVar

from fastapi import Header
from pydantic import BaseModel

T = TypeVar("T")


class StandardHeaders:
    """Standard API headers extracted via FastAPI Depends()."""

    def __init__(
        self,
        x_request_id: str = Header(default=None, alias="X-Request-ID"),
        x_forwarded_for: str = Header(default="unknown", alias="X-Forwarded-For"),
        x_device_id: str = Header(default="unknown", alias="X-Device-Id"),
    ):
        self.request_id = x_request_id
        self.forwarded_for = x_forwarded_for
        self.device_id = x_device_id


class ErrorResponse(BaseModel):
    success: bool = False
    error_code: str
    message: str
    request_id: str
    timestamp: str


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T
    request_id: str
    timestamp: str


class PaginatedData(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    data: PaginatedData[T]
    request_id: str
    timestamp: str


def success_response(data: Any, request_id: str, timestamp: str) -> dict:
    """Build a standard success response dict."""
    return {
        "success": True,
        "data": data,
        "request_id": request_id,
        "timestamp": timestamp,
    }


def paginated_response(
    items: list,
    total: int,
    page: int,
    page_size: int,
    request_id: str,
    timestamp: str,
) -> dict:
    """Build a standard paginated response dict."""
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    return {
        "success": True,
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        },
        "request_id": request_id,
        "timestamp": timestamp,
    }

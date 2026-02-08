class AMLException(Exception):
    """Base exception for all AML application errors."""

    def __init__(self, error_code: str, message: str, status_code: int = 400):
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(AMLException):
    """Resource not found."""

    def __init__(self, error_code: str, message: str):
        super().__init__(error_code=error_code, message=message, status_code=404)


class ConflictException(AMLException):
    """Resource conflict (e.g., duplicate)."""

    def __init__(self, error_code: str, message: str):
        super().__init__(error_code=error_code, message=message, status_code=409)


class ValidationException(AMLException):
    """Validation error."""

    def __init__(self, error_code: str, message: str):
        super().__init__(error_code=error_code, message=message, status_code=422)

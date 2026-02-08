import sys
from pathlib import Path

from loguru import logger
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./regulus_aml.db"

    # AML Rule Thresholds
    DEPOSIT_THRESHOLD: float = 10000.0
    NEGLIGIBLE_PROFIT_THRESHOLD: float = 1.0
    RAPID_CYCLE_HOURS: int = 24
    VELOCITY_TXN_COUNT: int = 5
    VELOCITY_WINDOW_MINUTES: int = 60
    CROSS_BORDER_ALERT_SEVERITY: str = "high"

    # LLM Configuration
    LLM_PROVIDER: str = "gemini"  # "gemini" or "openai"
    GEMINI_API_KEY: str = "your-gemini-key-here"
    GEMINI_MODEL: str = "gemini-2.5-flash"
    OPENAI_API_KEY: str = "your-openai-key-here"
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Simulation
    SIMULATION_MAX_TXN_PER_SCENARIO: int = 3

    # API Timeout (seconds)
    API_TIMEOUT_SECONDS: int = 30

    # Logging
    LOG_LEVEL: str = "DEBUG"

    # CORS
    FRONTEND_ORIGINS: str = "http://localhost:5173"

    # JWT Auth
    JWT_SECRET: str = "change-this-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 15

    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.FRONTEND_ORIGINS.split(",") if origin.strip()]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


settings = Settings()


def setup_logging() -> None:
    """Configure loguru with custom format and request-context injection."""
    logger.remove()

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{extra[request_id]}</cyan> | "
        "<blue>{name}</blue>:<blue>{line}</blue> | "
        "<level>{message}</level>"
    )

    logger.configure(extra={"request_id": "no-request-id"})

    logger.add(
        sys.stderr,
        format=log_format,
        level=settings.LOG_LEVEL,
        colorize=True,
    )

    # File logging (plain, no color)
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger.add(
        log_dir / "regulus_aml.log",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {extra[request_id]} | {name}:{line} | {message}",
        level=settings.LOG_LEVEL,
        rotation="10 MB",
        retention="7 days",
        compression="gz",
    )

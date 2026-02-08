from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.config.database import init_db
from app.controllers import (
    account_controller,
    alert_controller,
    auth_controller,
    case_controller,
    customer_controller,
    simulation_controller,
    transaction_controller,
    user_controller,
)
from app.config.settings import settings, setup_logging
from app.exceptions.handlers import register_exception_handlers
from app.middleware.request_context import RequestContextMiddleware
from app.utils.datetime_utils import utc_now


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    setup_logging()
    logger.info("Starting Regulus AML application...")
    init_db()
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown")


def create_app() -> FastAPI:
    """FastAPI application factory."""
    app = FastAPI(
        title="Regulus AML - Transaction Monitoring System",
        description="AI-powered Anti-Money Laundering workflow automation",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request context middleware
    app.add_middleware(RequestContextMiddleware)

    # Exception handlers
    register_exception_handlers(app)

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {
            "success": True,
            "data": {"status": "healthy", "service": "regulus-aml"},
            "timestamp": utc_now().isoformat(),
        }

    # Register routers
    app.include_router(customer_controller.router, prefix="/api/v1/customers", tags=["Customers"])
    app.include_router(account_controller.router, prefix="/api/v1/accounts", tags=["Accounts"])
    app.include_router(transaction_controller.router, prefix="/api/v1/transactions", tags=["Transactions"])
    app.include_router(alert_controller.router, prefix="/api/v1/alerts", tags=["Alerts"])
    app.include_router(case_controller.router, prefix="/api/v1/cases", tags=["Cases"])
    app.include_router(simulation_controller.router, prefix="/api/v1/simulate", tags=["Simulation"])
    app.include_router(user_controller.router, prefix="/api/v1/users", tags=["Users"])
    app.include_router(auth_controller.router, prefix="/api/v1/auth", tags=["Auth"])

    return app


app = create_app()

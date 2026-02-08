from app.controllers.account_controller import router as account_router
from app.controllers.alert_controller import router as alert_router
from app.controllers.case_controller import router as case_router
from app.controllers.customer_controller import router as customer_router
from app.controllers.transaction_controller import router as transaction_router
from app.controllers.simulation_controller import router as simulation_router
from app.controllers.user_controller import router as user_router
from app.controllers.auth_controller import router as auth_router

__all__ = [
    "account_router",
    "alert_router",
    "case_router",
    "customer_router",
    "transaction_router",
    "simulation_router",
    "user_router",
    "auth_router",
]

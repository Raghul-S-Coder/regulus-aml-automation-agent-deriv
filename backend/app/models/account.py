from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Account(Base):
    __tablename__ = "accounts"

    account_number: Mapped[str] = mapped_column(String, primary_key=True)  # ACC-XXXXXXXXX
    customer_id: Mapped[str] = mapped_column(String, ForeignKey("customers.customer_id"), nullable=False)
    account_type: Mapped[str] = mapped_column(String, nullable=False)
    account_status: Mapped[str] = mapped_column(String, nullable=False)
    opened_date: Mapped[str] = mapped_column(String, nullable=False)
    branch_code: Mapped[str] = mapped_column(String, nullable=False)
    balance_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    balance_currency: Mapped[str] = mapped_column(String, nullable=False)

    created_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )
    created_by: Mapped[str] = mapped_column(String, nullable=False, default="system")
    updated_by: Mapped[str] = mapped_column(String, nullable=False, default="system")

    # Relationships
    customer = relationship("Customer", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")
    high_risk_accounts = relationship("HighRiskAccount", back_populates="account")
    alerts = relationship("Alert", back_populates="account")
    cases = relationship("Case", back_populates="account")

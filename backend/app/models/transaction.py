from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[str] = mapped_column(String, primary_key=True)  # TXN-XXXXXXX
    account_number: Mapped[str] = mapped_column(String, ForeignKey("accounts.account_number"), nullable=False)
    transaction_amount: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_currency: Mapped[str] = mapped_column(String, nullable=False)
    transaction_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    transaction_type: Mapped[str] = mapped_column(String, nullable=False)  # deposit/withdrawal/trade-buy/trade-sell
    transaction_status: Mapped[str] = mapped_column(String, nullable=False, default="pending")
    purpose: Mapped[str | None] = mapped_column(String, nullable=True)
    deposit_source_type: Mapped[str | None] = mapped_column(String, nullable=True)
    deposit_source_value: Mapped[str | None] = mapped_column(String, nullable=True)
    deposit_source_country: Mapped[str | None] = mapped_column(String, nullable=True)

    created_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )
    created_by: Mapped[str] = mapped_column(String, nullable=False, default="system")
    updated_by: Mapped[str] = mapped_column(String, nullable=False, default="system")

    # Relationships
    account = relationship("Account", back_populates="transactions")
    alerts = relationship("Alert", back_populates="transaction")
    cases = relationship("Case", back_populates="transaction")

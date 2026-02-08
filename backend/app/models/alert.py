from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    alert_id: Mapped[str] = mapped_column(String, primary_key=True)  # ALERT-XXXXXX
    account_number: Mapped[str] = mapped_column(String, ForeignKey("accounts.account_number"), nullable=False)
    transaction_id: Mapped[str | None] = mapped_column(String, ForeignKey("transactions.transaction_id"), nullable=True)
    alert_type: Mapped[str] = mapped_column(String, nullable=False)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    rule_id: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    triggered_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    created_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )
    created_by: Mapped[str] = mapped_column(String, nullable=False, default="system")
    updated_by: Mapped[str] = mapped_column(String, nullable=False, default="system")

    # Relationships
    account = relationship("Account", back_populates="alerts")
    transaction = relationship("Transaction", back_populates="alerts")
    cases = relationship("Case", back_populates="alert")

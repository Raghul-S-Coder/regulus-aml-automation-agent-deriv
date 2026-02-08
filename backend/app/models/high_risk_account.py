from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class HighRiskAccount(Base):
    __tablename__ = "high_risk_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_number: Mapped[str] = mapped_column(String, ForeignKey("accounts.account_number"), nullable=False)
    high_risk_flag: Mapped[int] = mapped_column(Integer, nullable=False, default=1)  # 0=revoked, 1=still risk
    overall_risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_source: Mapped[str] = mapped_column(String, nullable=False)
    risk_reason: Mapped[str] = mapped_column(String, nullable=False)
    detected_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    created_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )
    created_by: Mapped[str] = mapped_column(String, nullable=False, default="system")
    updated_by: Mapped[str] = mapped_column(String, nullable=False, default="system")

    # Relationships
    account = relationship("Account", back_populates="high_risk_accounts")

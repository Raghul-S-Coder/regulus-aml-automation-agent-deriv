from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class CaseDecision(Base):
    __tablename__ = "case_decisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_id: Mapped[str] = mapped_column(String, ForeignKey("cases.case_id"), nullable=False)
    decision: Mapped[str] = mapped_column(String, nullable=False)  # ACCEPT/REJECT
    decision_by: Mapped[str] = mapped_column(String, nullable=False)
    decision_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    decision_reason: Mapped[str] = mapped_column(Text, nullable=False)
    next_action: Mapped[str] = mapped_column(String, nullable=False)

    created_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )
    created_by: Mapped[str] = mapped_column(String, nullable=False, default="system")
    updated_by: Mapped[str] = mapped_column(String, nullable=False, default="system")

    # Relationships
    case = relationship("Case", back_populates="decisions")

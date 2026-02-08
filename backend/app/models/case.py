from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Case(Base):
    __tablename__ = "cases"

    case_id: Mapped[str] = mapped_column(String, primary_key=True)  # CASE-XXXXXX
    alert_id: Mapped[str] = mapped_column(String, ForeignKey("alerts.alert_id"), nullable=False)
    account_number: Mapped[str] = mapped_column(String, ForeignKey("accounts.account_number"), nullable=False)
    transaction_id: Mapped[str | None] = mapped_column(String, ForeignKey("transactions.transaction_id"), nullable=True)
    case_status: Mapped[str] = mapped_column(String, nullable=False, default="OPEN")  # OPEN/CLOSE

    case_score_percentage: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # Agent scores and summaries — note: "behavoir" matches DatabaseModel.md spelling
    behavoir_agent_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    behavoir_agent_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    network_agent_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    network_agent_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    contextual_agent_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    contextual_agent_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    evidence_agent_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    evidence_agent_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    false_positive_agent_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    false_positive_agent_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    assigned_to: Mapped[str | None] = mapped_column(String, nullable=True)
    assigned_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    case_opened_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    case_closed_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    case_summary: Mapped[str] = mapped_column(Text, nullable=False)

    created_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )
    created_by: Mapped[str] = mapped_column(String, nullable=False, default="system")
    updated_by: Mapped[str] = mapped_column(String, nullable=False, default="system")

    # Relationships
    alert = relationship("Alert", back_populates="cases")
    account = relationship("Account", back_populates="cases")
    transaction = relationship("Transaction", back_populates="cases")
    documents = relationship("CaseDocumentContent", back_populates="case")
    decisions = relationship("CaseDecision", back_populates="case")

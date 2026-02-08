from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class CaseDocumentContent(Base):
    __tablename__ = "case_document_contents"

    document_id: Mapped[str] = mapped_column(String, primary_key=True)  # DOC-XXXXXX
    case_id: Mapped[str] = mapped_column(String, ForeignKey("cases.case_id"), nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)  # sar_draft/evidence_summary/timeline
    content: Mapped[str] = mapped_column(Text, nullable=False)
    generated_by: Mapped[str] = mapped_column(String, nullable=False)  # document_generator_agent
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    created_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )
    created_by: Mapped[str] = mapped_column(String, nullable=False, default="system")
    updated_by: Mapped[str] = mapped_column(String, nullable=False, default="system")

    # Relationships
    case = relationship("Case", back_populates="documents")

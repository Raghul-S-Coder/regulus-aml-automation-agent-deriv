from datetime import UTC, datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    organization_id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="active")

    created_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )
    created_by: Mapped[str] = mapped_column(String, nullable=False, default="system")
    updated_by: Mapped[str] = mapped_column(String, nullable=False, default="system")

    # Relationships
    users = relationship("User", back_populates="organization")

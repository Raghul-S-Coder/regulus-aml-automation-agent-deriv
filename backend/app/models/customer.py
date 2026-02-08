from datetime import UTC, datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[str] = mapped_column(String, primary_key=True)  # CUST-XXXXXX
    customer_type: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    date_of_birth: Mapped[str] = mapped_column(String, nullable=False)
    nationality: Mapped[str] = mapped_column(String, nullable=False)
    residency_country: Mapped[str] = mapped_column(String, nullable=False)
    id_type: Mapped[str] = mapped_column(String, nullable=False)
    id_number: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    address_line1: Mapped[str] = mapped_column(String, nullable=False)
    address_city: Mapped[str] = mapped_column(String, nullable=False)
    address_country: Mapped[str] = mapped_column(String, nullable=False)
    kyc_status: Mapped[str] = mapped_column(String, nullable=False)
    kyc_verified_date: Mapped[str | None] = mapped_column(String, nullable=True)
    kyc_expired_date: Mapped[str | None] = mapped_column(String, nullable=True)
    risk_rating: Mapped[str] = mapped_column(String, nullable=False)

    created_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )
    created_by: Mapped[str] = mapped_column(String, nullable=False, default="system")
    updated_by: Mapped[str] = mapped_column(String, nullable=False, default="system")

    # Relationships
    accounts = relationship("Account", back_populates="customer")

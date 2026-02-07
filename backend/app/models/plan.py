"""Quarterly planning ORM model."""

import uuid

from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class QuarterlyPlan(Base, TimestampMixin):
    """Leadership planning artifact stored as structured JSON data."""

    __tablename__ = "quarterly_plans"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    quarter: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    objectives: Mapped[list[dict[str, str]]] = mapped_column(JSON, default=list, nullable=False)
    created_by_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    created_by = relationship("User", back_populates="plans")

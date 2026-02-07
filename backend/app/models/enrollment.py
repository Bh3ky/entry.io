"""Enrollment ORM model."""

import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Enrollment(Base, TimestampMixin):
    """Represents a class enrollment for a member."""

    __tablename__ = "enrollments"
    __table_args__ = (UniqueConstraint("user_id", "class_id", name="uq_enrollments_user_class"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    class_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("classes.id"), nullable=False, index=True)

    user = relationship("User", back_populates="enrollments")
    class_ = relationship("LearningClass", back_populates="enrollments")

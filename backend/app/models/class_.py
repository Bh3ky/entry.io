"""Learning class ORM model."""

import uuid

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class LearningClass(Base, TimestampMixin):
    """Represents a class that contains one or more sessions."""

    __tablename__ = "classes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_by_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    created_by = relationship("User", back_populates="classes_created")
    sessions = relationship("ClassSession", back_populates="class_", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="class_", cascade="all, delete-orphan")

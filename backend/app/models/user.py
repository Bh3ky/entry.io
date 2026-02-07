"""User ORM model and role definitions."""

import enum
import uuid

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


def enum_values(enum_class: type[enum.Enum]) -> list[str]:
    """Return enum values so SQLAlchemy stores lowercase enum values in Postgres."""

    return [str(member.value) for member in enum_class]


class UserRole(str, enum.Enum):
    """Roles used by RBAC checks."""

    MEMBER = "member"
    LEAD = "lead"
    ADMIN = "admin"


class User(Base, TimestampMixin):
    """Application user account."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_roles", values_callable=enum_values),
        default=UserRole.MEMBER,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    classes_created = relationship("LearningClass", back_populates="created_by")
    sessions_created = relationship("ClassSession", back_populates="created_by")
    enrollments = relationship("Enrollment", back_populates="user")
    attendance_records = relationship(
        "Attendance",
        back_populates="user",
        foreign_keys="Attendance.user_id",
    )
    announcements = relationship("Announcement", back_populates="created_by")
    questions = relationship("QnAQuestion", back_populates="author")
    replies = relationship("QnAReply", back_populates="author")
    plans = relationship("QuarterlyPlan", back_populates="created_by")

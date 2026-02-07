"""Attendance ORM model."""

import enum
import uuid

from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


def enum_values(enum_class: type[enum.Enum]) -> list[str]:
    """Return enum values so SQLAlchemy stores lowercase enum values in Postgres."""

    return [str(member.value) for member in enum_class]


class AttendanceStatus(str, enum.Enum):
    """Allowed attendance statuses."""

    PRESENT = "present"
    ABSENT = "absent"
    EXCUSED = "excused"


class Attendance(Base, TimestampMixin):
    """Attendance state for one user in one class session."""

    __tablename__ = "attendance"
    __table_args__ = (UniqueConstraint("session_id", "user_id", name="uq_attendance_session_user"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    marked_by_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[AttendanceStatus] = mapped_column(
        Enum(AttendanceStatus, name="attendance_status", values_callable=enum_values),
        nullable=False,
    )

    session = relationship("ClassSession", back_populates="attendance_records")
    user = relationship("User", back_populates="attendance_records", foreign_keys=[user_id])

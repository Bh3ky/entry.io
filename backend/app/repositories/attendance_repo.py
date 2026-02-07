"""Repository for attendance persistence operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attendance import Attendance, AttendanceStatus


class AttendanceRepository:
    """Database operations for attendance records."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_existing(self, session_id: uuid.UUID, user_id: uuid.UUID) -> Attendance | None:
        """Return attendance record if it already exists."""

        statement = select(Attendance).where(
            Attendance.session_id == session_id,
            Attendance.user_id == user_id,
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def upsert(
        self,
        session_id: uuid.UUID,
        user_id: uuid.UUID,
        marked_by_id: uuid.UUID,
        status: AttendanceStatus,
    ) -> Attendance:
        """Create or update attendance for a user in a session."""

        existing = await self.get_existing(session_id=session_id, user_id=user_id)
        if existing is None:
            existing = Attendance(
                session_id=session_id,
                user_id=user_id,
                marked_by_id=marked_by_id,
                status=status,
            )
            self.session.add(existing)
        else:
            existing.status = status
            existing.marked_by_id = marked_by_id

        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    async def list_by_session(self, session_id: uuid.UUID) -> list[Attendance]:
        """List attendance entries for a specific session."""

        statement = select(Attendance).where(Attendance.session_id == session_id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

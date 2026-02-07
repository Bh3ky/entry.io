"""Service layer for attendance tracking."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attendance import Attendance, AttendanceStatus
from app.repositories.attendance_repo import AttendanceRepository
from app.repositories.session_repo import SessionRepository


class AttendanceService:
    """Business logic for attendance marking and retrieval."""

    def __init__(self, session: AsyncSession) -> None:
        self.session_repo = SessionRepository(session)
        self.repo = AttendanceRepository(session)

    async def mark_attendance(
        self,
        session_id: uuid.UUID,
        user_id: uuid.UUID,
        marked_by_id: uuid.UUID,
        status: AttendanceStatus,
    ) -> Attendance:
        """Create or update attendance for a session/user pair."""

        session = await self.session_repo.get_by_id(session_id)
        if session is None:
            raise LookupError("Session not found")

        return await self.repo.upsert(
            session_id=session_id,
            user_id=user_id,
            marked_by_id=marked_by_id,
            status=status,
        )

    async def list_for_session(self, session_id: uuid.UUID) -> list[Attendance]:
        """List attendance records for a session."""

        session = await self.session_repo.get_by_id(session_id)
        if session is None:
            raise LookupError("Session not found")

        return await self.repo.list_by_session(session_id)

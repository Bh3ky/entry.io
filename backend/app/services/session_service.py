"""Service layer for class sessions."""

import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session import ClassSession
from app.repositories.class_repo import ClassRepository
from app.repositories.session_repo import SessionRepository


class SessionService:
    """Business logic for session scheduling and management."""

    def __init__(self, session: AsyncSession) -> None:
        self.class_repo = ClassRepository(session)
        self.session_repo = SessionRepository(session)

    async def create_session(
        self,
        class_id: uuid.UUID,
        title: str,
        description: str | None,
        starts_at: datetime,
        ends_at: datetime,
        created_by_id: uuid.UUID,
    ) -> ClassSession:
        """Create a session under an existing class."""

        if ends_at <= starts_at:
            raise ValueError("Session end time must be after start time")

        class_ = await self.class_repo.get_by_id(class_id)
        if class_ is None:
            raise LookupError("Class not found")

        return await self.session_repo.create(
            class_id=class_id,
            title=title,
            description=description,
            starts_at=starts_at,
            ends_at=ends_at,
            created_by_id=created_by_id,
        )

    async def list_sessions(self, class_id: uuid.UUID | None = None) -> list[ClassSession]:
        """List sessions, optionally by class."""

        return await self.session_repo.list_sessions(class_id=class_id)

    async def get_session(self, session_id: uuid.UUID) -> ClassSession:
        """Return one session by id."""

        session = await self.session_repo.get_by_id(session_id)
        if session is None:
            raise LookupError("Session not found")
        return session

    async def update_session(
        self,
        session_id: uuid.UUID,
        updates: dict[str, object],
    ) -> ClassSession:
        """Update a session and ensure time range remains valid."""

        session = await self.get_session(session_id)

        starts_at = updates.get("starts_at", session.starts_at)
        ends_at = updates.get("ends_at", session.ends_at)
        if isinstance(starts_at, datetime) and isinstance(ends_at, datetime) and ends_at <= starts_at:
            raise ValueError("Session end time must be after start time")

        return await self.session_repo.update(session, updates)

    async def delete_session(self, session_id: uuid.UUID) -> None:
        """Delete one session."""

        session = await self.get_session(session_id)
        await self.session_repo.delete(session)

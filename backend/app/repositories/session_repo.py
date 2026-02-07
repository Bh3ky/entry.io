"""Repository for class session persistence operations."""

import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session import ClassSession


class SessionRepository:
    """Database operations for class sessions."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        class_id: uuid.UUID,
        title: str,
        description: str | None,
        starts_at: datetime,
        ends_at: datetime,
        created_by_id: uuid.UUID,
    ) -> ClassSession:
        """Create and persist a class session."""

        session = ClassSession(
            class_id=class_id,
            title=title,
            description=description,
            starts_at=starts_at,
            ends_at=ends_at,
            created_by_id=created_by_id,
        )
        self.session.add(session)
        await self.session.commit()
        await self.session.refresh(session)
        return session

    async def get_by_id(self, session_id: uuid.UUID) -> ClassSession | None:
        """Fetch a session by id."""

        return await self.session.get(ClassSession, session_id)

    async def list_sessions(self, class_id: uuid.UUID | None = None) -> list[ClassSession]:
        """List sessions, optionally filtered by class id."""

        statement = select(ClassSession)
        if class_id is not None:
            statement = statement.where(ClassSession.class_id == class_id)
        statement = statement.order_by(ClassSession.starts_at.asc())
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def update(self, session: ClassSession, updates: dict[str, object]) -> ClassSession:
        """Update session fields and persist changes."""

        for key, value in updates.items():
            setattr(session, key, value)
        await self.session.commit()
        await self.session.refresh(session)
        return session

    async def delete(self, session: ClassSession) -> None:
        """Delete a session record."""

        await self.session.delete(session)
        await self.session.commit()

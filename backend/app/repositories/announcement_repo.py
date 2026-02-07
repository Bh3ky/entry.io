"""Repository for announcement persistence operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.announcement import Announcement


class AnnouncementRepository:
    """Database operations for announcements."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, title: str, body: str, created_by_id: uuid.UUID) -> Announcement:
        """Create a new announcement."""

        announcement = Announcement(title=title, body=body, created_by_id=created_by_id)
        self.session.add(announcement)
        await self.session.commit()
        await self.session.refresh(announcement)
        return announcement

    async def list_announcements(self) -> list[Announcement]:
        """List all announcements sorted by newest first."""

        statement = select(Announcement).order_by(Announcement.created_at.desc())
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_id(self, announcement_id: uuid.UUID) -> Announcement | None:
        """Get one announcement by id."""

        return await self.session.get(Announcement, announcement_id)

    async def delete(self, announcement: Announcement) -> None:
        """Delete one announcement."""

        await self.session.delete(announcement)
        await self.session.commit()

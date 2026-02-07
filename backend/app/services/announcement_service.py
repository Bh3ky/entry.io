"""Service layer for community announcements."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.announcement import Announcement
from app.repositories.announcement_repo import AnnouncementRepository


class AnnouncementService:
    """Business logic for creating and managing announcements."""

    def __init__(self, session: AsyncSession) -> None:
        self.repo = AnnouncementRepository(session)

    async def create_announcement(
        self,
        title: str,
        body: str,
        created_by_id: uuid.UUID,
    ) -> Announcement:
        """Create a new announcement."""

        return await self.repo.create(title=title, body=body, created_by_id=created_by_id)

    async def list_announcements(self) -> list[Announcement]:
        """List announcements."""

        return await self.repo.list_announcements()

    async def delete_announcement(self, announcement_id: uuid.UUID) -> None:
        """Delete announcement by id."""

        announcement = await self.repo.get_by_id(announcement_id)
        if announcement is None:
            raise LookupError("Announcement not found")

        await self.repo.delete(announcement)

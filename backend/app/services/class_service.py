"""Service layer for learning classes."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.class_ import LearningClass
from app.repositories.class_repo import ClassRepository


class ClassService:
    """Business logic for class management."""

    def __init__(self, session: AsyncSession) -> None:
        self.repo = ClassRepository(session)

    async def create_class(
        self,
        title: str,
        description: str | None,
        is_published: bool,
        created_by_id: uuid.UUID,
    ) -> LearningClass:
        """Create a class."""

        return await self.repo.create(title, description, is_published, created_by_id)

    async def list_classes(self) -> list[LearningClass]:
        """List classes."""

        return await self.repo.list_classes()

    async def get_class(self, class_id: uuid.UUID) -> LearningClass:
        """Get class by id or raise error."""

        class_ = await self.repo.get_by_id(class_id)
        if class_ is None:
            raise LookupError("Class not found")
        return class_

    async def update_class(self, class_id: uuid.UUID, updates: dict[str, object]) -> LearningClass:
        """Update an existing class."""

        class_ = await self.get_class(class_id)
        return await self.repo.update(class_, updates)

    async def delete_class(self, class_id: uuid.UUID) -> None:
        """Delete an existing class."""

        class_ = await self.get_class(class_id)
        await self.repo.delete(class_)

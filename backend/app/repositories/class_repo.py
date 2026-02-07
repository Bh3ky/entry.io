"""Repository for class persistence operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.class_ import LearningClass


class ClassRepository:
    """Database operations for learning classes."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        title: str,
        description: str | None,
        is_published: bool,
        created_by_id: uuid.UUID,
    ) -> LearningClass:
        """Create and persist a new class."""

        class_ = LearningClass(
            title=title,
            description=description,
            is_published=is_published,
            created_by_id=created_by_id,
        )
        self.session.add(class_)
        await self.session.commit()
        await self.session.refresh(class_)
        return class_

    async def get_by_id(self, class_id: uuid.UUID) -> LearningClass | None:
        """Fetch a class by id."""

        return await self.session.get(LearningClass, class_id)

    async def list_classes(self) -> list[LearningClass]:
        """List classes ordered by newest first."""

        statement = select(LearningClass).order_by(LearningClass.created_at.desc())
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def update(self, class_: LearningClass, updates: dict[str, object]) -> LearningClass:
        """Update fields on a class and persist changes."""

        for key, value in updates.items():
            setattr(class_, key, value)
        await self.session.commit()
        await self.session.refresh(class_)
        return class_

    async def delete(self, class_: LearningClass) -> None:
        """Delete a class record."""

        await self.session.delete(class_)
        await self.session.commit()

"""Repository for enrollment persistence operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enrollment import Enrollment


class EnrollmentRepository:
    """Database operations for enrollments."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_existing(self, user_id: uuid.UUID, class_id: uuid.UUID) -> Enrollment | None:
        """Return existing enrollment for a user/class pair."""

        statement = select(Enrollment).where(
            Enrollment.user_id == user_id,
            Enrollment.class_id == class_id,
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, user_id: uuid.UUID, class_id: uuid.UUID) -> Enrollment:
        """Create a new enrollment."""

        enrollment = Enrollment(user_id=user_id, class_id=class_id)
        self.session.add(enrollment)
        await self.session.commit()
        await self.session.refresh(enrollment)
        return enrollment

    async def list_by_class(self, class_id: uuid.UUID) -> list[Enrollment]:
        """List enrollments for a class."""

        statement = select(Enrollment).where(Enrollment.class_id == class_id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def list_by_user(self, user_id: uuid.UUID) -> list[Enrollment]:
        """List enrollments for a user."""

        statement = select(Enrollment).where(Enrollment.user_id == user_id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def delete(self, enrollment: Enrollment) -> None:
        """Delete an enrollment."""

        await self.session.delete(enrollment)
        await self.session.commit()

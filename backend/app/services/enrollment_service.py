"""Service layer for class enrollment flows."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enrollment import Enrollment
from app.repositories.class_repo import ClassRepository
from app.repositories.enrollment_repo import EnrollmentRepository


class EnrollmentService:
    """Business logic for enrollment and unenrollment."""

    def __init__(self, session: AsyncSession) -> None:
        self.class_repo = ClassRepository(session)
        self.repo = EnrollmentRepository(session)

    async def enroll(self, user_id: uuid.UUID, class_id: uuid.UUID) -> Enrollment:
        """Enroll a user in a class unless already enrolled."""

        class_ = await self.class_repo.get_by_id(class_id)
        if class_ is None:
            raise LookupError("Class not found")

        existing = await self.repo.get_existing(user_id=user_id, class_id=class_id)
        if existing is not None:
            raise ValueError("User is already enrolled in this class")

        return await self.repo.create(user_id=user_id, class_id=class_id)

    async def unenroll(self, user_id: uuid.UUID, class_id: uuid.UUID) -> None:
        """Remove an enrollment if it exists."""

        existing = await self.repo.get_existing(user_id=user_id, class_id=class_id)
        if existing is None:
            raise LookupError("Enrollment not found")

        await self.repo.delete(existing)

    async def list_for_class(self, class_id: uuid.UUID) -> list[Enrollment]:
        """List enrollments for one class."""

        return await self.repo.list_by_class(class_id)

    async def list_for_user(self, user_id: uuid.UUID) -> list[Enrollment]:
        """List enrollments for one user."""

        return await self.repo.list_by_user(user_id)

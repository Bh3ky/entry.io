"""Repository for quarterly planning persistence operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.plan import QuarterlyPlan


class PlanRepository:
    """Database operations for quarterly plans."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        quarter: str,
        objectives: list[dict[str, str]],
        created_by_id: uuid.UUID,
    ) -> QuarterlyPlan:
        """Create and persist a quarterly plan."""

        plan = QuarterlyPlan(
            quarter=quarter,
            objectives=objectives,
            created_by_id=created_by_id,
        )
        self.session.add(plan)
        await self.session.commit()
        await self.session.refresh(plan)
        return plan

    async def list_plans(self) -> list[QuarterlyPlan]:
        """List all plans sorted by latest first."""

        statement = select(QuarterlyPlan).order_by(QuarterlyPlan.created_at.desc())
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_id(self, plan_id: uuid.UUID) -> QuarterlyPlan | None:
        """Fetch one plan by id."""

        return await self.session.get(QuarterlyPlan, plan_id)

    async def update(self, plan: QuarterlyPlan, updates: dict[str, object]) -> QuarterlyPlan:
        """Update a plan and persist changes."""

        for key, value in updates.items():
            setattr(plan, key, value)
        await self.session.commit()
        await self.session.refresh(plan)
        return plan

    async def delete(self, plan: QuarterlyPlan) -> None:
        """Delete one plan."""

        await self.session.delete(plan)
        await self.session.commit()

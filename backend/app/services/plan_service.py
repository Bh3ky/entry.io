"""Service layer for quarterly planning flows."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.plan import QuarterlyPlan
from app.repositories.plan_repo import PlanRepository


class PlanService:
    """Business logic for quarterly plans."""

    def __init__(self, session: AsyncSession) -> None:
        self.repo = PlanRepository(session)

    async def create_plan(
        self,
        quarter: str,
        objectives: list[dict[str, str]],
        created_by_id: uuid.UUID,
    ) -> QuarterlyPlan:
        """Create a quarterly plan."""

        return await self.repo.create(quarter=quarter, objectives=objectives, created_by_id=created_by_id)

    async def list_plans(self) -> list[QuarterlyPlan]:
        """List all plans."""

        return await self.repo.list_plans()

    async def get_plan(self, plan_id: uuid.UUID) -> QuarterlyPlan:
        """Get one plan by id."""

        plan = await self.repo.get_by_id(plan_id)
        if plan is None:
            raise LookupError("Plan not found")
        return plan

    async def update_plan(self, plan_id: uuid.UUID, updates: dict[str, object]) -> QuarterlyPlan:
        """Update one plan by id."""

        plan = await self.get_plan(plan_id)
        return await self.repo.update(plan, updates)

    async def delete_plan(self, plan_id: uuid.UUID) -> None:
        """Delete one plan by id."""

        plan = await self.get_plan(plan_id)
        await self.repo.delete(plan)

    async def export_plan(self, plan_id: uuid.UUID) -> dict[str, object]:
        """Export one plan as JSON-serializable payload."""

        plan = await self.get_plan(plan_id)
        return {
            "id": str(plan.id),
            "quarter": plan.quarter,
            "objectives": plan.objectives,
            "created_by_id": str(plan.created_by_id),
            "created_at": plan.created_at.isoformat(),
            "updated_at": plan.updated_at.isoformat(),
        }

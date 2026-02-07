"""Aggregate API router definitions."""

from fastapi import APIRouter

from app.api.routes import (
    announcements,
    attendance,
    auth,
    classes,
    enrollment,
    health,
    plans,
    qna,
    sessions,
    users,
)
from app.core.config import get_settings

settings = get_settings()

api_router = APIRouter()
api_router.include_router(health.router)

v1_router = APIRouter(prefix=settings.api_v1_prefix)
v1_router.include_router(auth.router)
v1_router.include_router(users.router)
v1_router.include_router(classes.router)
v1_router.include_router(sessions.router)
v1_router.include_router(enrollment.router)
v1_router.include_router(attendance.router)
v1_router.include_router(announcements.router)
v1_router.include_router(qna.router)
v1_router.include_router(plans.router)

api_router.include_router(v1_router)

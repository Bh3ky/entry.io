"""Community Q&A endpoints."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.common import MessageResponse
from app.schemas.qna import QuestionCreate, QuestionRead, ReplyCreate, ReplyRead
from app.services.qna_service import QnAService

router = APIRouter(prefix="/qna", tags=["qna"])


@router.post("/questions", response_model=QuestionRead, status_code=status.HTTP_201_CREATED)
async def create_question(
    payload: QuestionCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> QuestionRead:
    """Post a technical question."""

    question = await QnAService(db).create_question(
        author_id=current_user.id,
        title=payload.title,
        body=payload.body,
        tags=payload.tags,
    )
    return QuestionRead.model_validate(question)


@router.get("/questions", response_model=list[QuestionRead])
async def list_questions(
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    search: str | None = Query(default=None),
    tag: str | None = Query(default=None),
) -> list[QuestionRead]:
    """List questions with optional search and tag filtering."""

    questions = await QnAService(db).list_questions(search=search, tag=tag)
    return [QuestionRead.model_validate(question) for question in questions]


@router.post(
    "/questions/{question_id}/replies",
    response_model=ReplyRead,
    status_code=status.HTTP_201_CREATED,
)
async def reply_to_question(
    question_id: uuid.UUID,
    payload: ReplyCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ReplyRead:
    """Post a reply to a question."""

    service = QnAService(db)
    try:
        reply = await service.reply_to_question(
            question_id=question_id,
            author_id=current_user.id,
            body=payload.body,
        )
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return ReplyRead.model_validate(reply)


@router.get("/questions/{question_id}/replies", response_model=list[ReplyRead])
async def list_replies(
    question_id: uuid.UUID,
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ReplyRead]:
    """List replies for a question."""

    service = QnAService(db)
    try:
        replies = await service.list_replies(question_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return [ReplyRead.model_validate(reply) for reply in replies]


@router.delete("/questions/{question_id}", response_model=MessageResponse)
async def delete_question(
    question_id: uuid.UUID,
    _: Annotated[User, Depends(require_roles(UserRole.LEAD, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> MessageResponse:
    """Moderate (soft-delete) a question."""

    service = QnAService(db)
    try:
        await service.delete_question(question_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return MessageResponse(message="Question deleted")

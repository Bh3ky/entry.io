"""Repository for Q&A persistence operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.qna import QnAQuestion, QnAReply


class QnARepository:
    """Database operations for Q&A questions and replies."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_question(
        self,
        author_id: uuid.UUID,
        title: str,
        body: str,
        tags: list[str],
    ) -> QnAQuestion:
        """Create a new question."""

        question = QnAQuestion(author_id=author_id, title=title, body=body, tags=tags)
        self.session.add(question)
        await self.session.commit()
        await self.session.refresh(question)
        return question

    async def list_questions(
        self,
        search: str | None = None,
        tag: str | None = None,
    ) -> list[QnAQuestion]:
        """List non-deleted questions with optional search and tag filters."""

        statement = select(QnAQuestion).where(QnAQuestion.is_deleted.is_(False))
        if search:
            like_value = f"%{search}%"
            statement = statement.where(
                QnAQuestion.title.ilike(like_value) | QnAQuestion.body.ilike(like_value)
            )
        if tag:
            statement = statement.where(QnAQuestion.tags.contains([tag]))

        statement = statement.order_by(QnAQuestion.created_at.desc())
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_question_by_id(self, question_id: uuid.UUID) -> QnAQuestion | None:
        """Fetch one question by id."""

        return await self.session.get(QnAQuestion, question_id)

    async def soft_delete_question(self, question: QnAQuestion) -> QnAQuestion:
        """Soft-delete a question."""

        question.is_deleted = True
        await self.session.commit()
        await self.session.refresh(question)
        return question

    async def create_reply(self, question_id: uuid.UUID, author_id: uuid.UUID, body: str) -> QnAReply:
        """Create a reply under an existing question."""

        reply = QnAReply(question_id=question_id, author_id=author_id, body=body)
        self.session.add(reply)
        await self.session.commit()
        await self.session.refresh(reply)
        return reply

    async def list_replies(self, question_id: uuid.UUID) -> list[QnAReply]:
        """List non-deleted replies for a question."""

        statement = select(QnAReply).where(
            QnAReply.question_id == question_id,
            QnAReply.is_deleted.is_(False),
        )
        statement = statement.order_by(QnAReply.created_at.asc())
        result = await self.session.execute(statement)
        return list(result.scalars().all())

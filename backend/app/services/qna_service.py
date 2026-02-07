"""Service layer for community Q&A flows."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.qna import QnAQuestion, QnAReply
from app.repositories.qna_repo import QnARepository


class QnAService:
    """Business logic for posting and moderating questions/replies."""

    def __init__(self, session: AsyncSession) -> None:
        self.repo = QnARepository(session)

    async def create_question(
        self,
        author_id: uuid.UUID,
        title: str,
        body: str,
        tags: list[str],
    ) -> QnAQuestion:
        """Create a technical question."""

        sanitized_tags = [tag.strip().lower() for tag in tags if tag.strip()]
        return await self.repo.create_question(author_id, title, body, sanitized_tags)

    async def list_questions(
        self,
        search: str | None = None,
        tag: str | None = None,
    ) -> list[QnAQuestion]:
        """List questions with optional filters."""

        normalized_tag = tag.strip().lower() if tag else None
        return await self.repo.list_questions(search=search, tag=normalized_tag)

    async def reply_to_question(
        self,
        question_id: uuid.UUID,
        author_id: uuid.UUID,
        body: str,
    ) -> QnAReply:
        """Post a reply to an existing question."""

        question = await self.repo.get_question_by_id(question_id)
        if question is None or question.is_deleted:
            raise LookupError("Question not found")

        return await self.repo.create_reply(question_id=question_id, author_id=author_id, body=body)

    async def list_replies(self, question_id: uuid.UUID) -> list[QnAReply]:
        """List replies for one question."""

        question = await self.repo.get_question_by_id(question_id)
        if question is None or question.is_deleted:
            raise LookupError("Question not found")

        return await self.repo.list_replies(question_id=question_id)

    async def delete_question(self, question_id: uuid.UUID) -> QnAQuestion:
        """Soft-delete a question."""

        question = await self.repo.get_question_by_id(question_id)
        if question is None or question.is_deleted:
            raise LookupError("Question not found")

        return await self.repo.soft_delete_question(question)

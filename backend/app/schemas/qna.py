"""Q&A schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class QuestionCreate(BaseModel):
    """Create payload for technical questions."""

    title: str = Field(min_length=3, max_length=255)
    body: str = Field(min_length=3)
    tags: list[str] = Field(default_factory=list)


class ReplyCreate(BaseModel):
    """Create payload for question replies."""

    body: str = Field(min_length=1)


class ReplyRead(ORMModel):
    """Q&A reply schema."""

    id: uuid.UUID
    question_id: uuid.UUID
    author_id: uuid.UUID
    body: str
    created_at: datetime
    updated_at: datetime


class QuestionRead(ORMModel):
    """Q&A question schema."""

    id: uuid.UUID
    author_id: uuid.UUID
    title: str
    body: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime

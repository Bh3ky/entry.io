"""Common schema utilities shared across API modules."""

from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    """Base model configured for ORM serialization."""

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    """Simple response envelope for status messages."""

    message: str

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class QueueCreate(BaseModel):
    project_id: UUID
    name: str = Field(..., min_length=3, max_length=100)
    priority: int = Field(default=0, ge=0, le=10)
    concurrency_limit: int = Field(default=5, ge=1, le=100)


class QueueUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=100)
    priority: int | None = Field(default=None, ge=0, le=10)
    concurrency_limit: int | None = Field(default=None, ge=1, le=100)
    is_paused: bool | None = None


class QueueResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    name: str
    priority: int
    concurrency_limit: int
    is_paused: bool
    created_at: datetime
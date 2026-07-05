from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class JobCreate(BaseModel):
    queue_id: UUID
    retry_policy_id: UUID | None = None

    type: str = Field(..., min_length=3, max_length=100)

    payload: dict

    priority: int = Field(default=0, ge=0, le=10)

    run_after: datetime | None = None


class JobUpdate(BaseModel):
    type: str | None = Field(default=None, min_length=3, max_length=100)

    payload: dict | None = None

    priority: int | None = Field(default=None, ge=0, le=10)

    state: str | None = None

    run_after: datetime | None = None


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    queue_id: UUID

    retry_policy_id: UUID | None

    type: str

    payload: dict

    state: str

    priority: int

    attempts: int

    run_after: datetime

    created_at: datetime

    updated_at: datetime
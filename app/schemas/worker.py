from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class WorkerRegister(BaseModel):
    hostname: str = Field(..., min_length=2, max_length=100)


class WorkerHeartbeat(BaseModel):
    status: str


class WorkerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    hostname: str
    status: str
    heartbeat: datetime
    created_at: datetime
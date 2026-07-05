import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, JSON, String
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base


class DeadLetterQueue(Base):
    __tablename__ = "dead_letter_queue"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    original_job_id = Column(UUID(as_uuid=True))

    payload = Column(JSON)

    reason = Column(String(255))

    failed_at = Column(DateTime, default=datetime.utcnow)
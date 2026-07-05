import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    queue_id = Column(
        UUID(as_uuid=True),
        ForeignKey("queues.id", ondelete="CASCADE"),
        nullable=False,
    )

    retry_policy_id = Column(
        UUID(as_uuid=True),
        ForeignKey("retry_policies.id"),
        nullable=True,
    )

    type = Column(String(100), nullable=False)

    payload = Column(JSON, nullable=False)

    state = Column(String(30), default="queued")

    priority = Column(Integer, default=0)

    attempts = Column(Integer, default=0)

    run_after = Column(DateTime, default=datetime.utcnow)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    queue = relationship("Queue", back_populates="jobs")

    retry_policy = relationship("RetryPolicy", back_populates="jobs")

    execution_logs = relationship(
        "ExecutionLog",
        back_populates="job",
        cascade="all, delete-orphan",
    )
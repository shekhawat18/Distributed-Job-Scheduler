import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class Queue(Base):
    __tablename__ = "queues"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )

    name = Column(String(100), nullable=False)

    priority = Column(Integer, default=0)

    concurrency_limit = Column(Integer, default=5)

    is_paused = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="queues")

    jobs = relationship(
        "Job",
        back_populates="queue",
        cascade="all, delete-orphan",
    )
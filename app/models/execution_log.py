import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    job_id = Column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
    )

    message = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="execution_logs")
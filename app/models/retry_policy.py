import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class RetryPolicy(Base):
    __tablename__ = "retry_policies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(100), nullable=False)

    max_attempts = Column(Integer, default=3)

    strategy = Column(String(30), default="exponential")

    initial_delay = Column(Integer, default=5)

    created_at = Column(DateTime, default=datetime.utcnow)

    jobs = relationship("Job", back_populates="retry_policy")
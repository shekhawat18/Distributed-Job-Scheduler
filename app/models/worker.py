import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base


class Worker(Base):
    __tablename__ = "workers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    hostname = Column(String(100), nullable=False)

    status = Column(String(30), default="idle")

    heartbeat = Column(DateTime, default=datetime.utcnow)

    created_at = Column(DateTime, default=datetime.utcnow)
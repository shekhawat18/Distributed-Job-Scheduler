import uuid
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    full_name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False, index=True)

    password_hash = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)

    is_admin = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    projects = relationship(
    "Project",
    back_populates="owner",
    cascade="all, delete-orphan",
)
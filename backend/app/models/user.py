from sqlalchemy import Column, String, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    GUARD = "guard"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.GUARD)
    is_active = Column(String, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

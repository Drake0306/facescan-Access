from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.core.database import Base


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    phone = Column(String)
    email = Column(String)
    company = Column(String)
    vehicle_number = Column(String)
    purpose = Column(String)
    host_name = Column(String)
    valid_from = Column(DateTime)
    valid_until = Column(DateTime)
    is_active = Column(String, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    faces = relationship("Face", back_populates="visitor", cascade="all, delete-orphan")
    visits = relationship("Visit", back_populates="visitor", cascade="all, delete-orphan")

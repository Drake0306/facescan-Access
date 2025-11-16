from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum

from app.core.database import Base


class VisitStatus(str, enum.Enum):
    INSIDE = "inside"
    OUTSIDE = "outside"


class Visit(Base):
    __tablename__ = "visits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    visitor_id = Column(UUID(as_uuid=True), ForeignKey("visitors.id"), nullable=False)
    entry_time = Column(DateTime, default=datetime.utcnow)
    exit_time = Column(DateTime, nullable=True)
    status = Column(SQLEnum(VisitStatus), nullable=False, default=VisitStatus.OUTSIDE)
    gate_id = Column(String, default="gate-1")
    entry_snapshot_path = Column(String)
    exit_snapshot_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    visitor = relationship("Visitor", back_populates="visits")

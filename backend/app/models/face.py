from sqlalchemy import Column, String, DateTime, ForeignKey, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.core.database import Base


class Face(Base):
    __tablename__ = "faces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    visitor_id = Column(UUID(as_uuid=True), ForeignKey("visitors.id"), nullable=False)
    embedding = Column(LargeBinary, nullable=False)  # Store as binary
    photo_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    visitor = relationship("Visitor", back_populates="faces")

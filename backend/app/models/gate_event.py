from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum

from app.core.database import Base


class GateAction(str, enum.Enum):
    OPENED = "opened"
    CLOSED = "closed"


class GateTrigger(str, enum.Enum):
    SYSTEM = "system"
    MANUAL = "manual"


class GateEvent(Base):
    __tablename__ = "gate_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gate_id = Column(String, nullable=False)
    action = Column(SQLEnum(GateAction), nullable=False)
    triggered_by = Column(SQLEnum(GateTrigger), nullable=False)
    triggered_by_user = Column(String)
    visitor_id = Column(UUID(as_uuid=True), nullable=True)
    visitor_name = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

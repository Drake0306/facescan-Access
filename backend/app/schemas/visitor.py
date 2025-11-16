from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class VisitorBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    vehicle_number: Optional[str] = None
    purpose: Optional[str] = None
    host_name: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None


class VisitorCreate(VisitorBase):
    pass


class VisitorUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    vehicle_number: Optional[str] = None
    purpose: Optional[str] = None
    host_name: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    is_active: Optional[bool] = None


class Visitor(VisitorBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

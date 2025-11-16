from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.visit import Visit, VisitStatus
from app.api.routes.auth import get_current_user

router = APIRouter()


@router.get("/")
async def get_visits(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    visits = db.query(Visit).order_by(Visit.entry_time.desc()).offset(skip).limit(limit).all()
    return visits


@router.get("/active")
async def get_active_visits(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    visits = db.query(Visit).filter(Visit.status == VisitStatus.INSIDE).all()
    return visits

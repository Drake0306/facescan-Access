from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.models.visitor import Visitor
from app.schemas.visitor import Visitor as VisitorSchema, VisitorCreate, VisitorUpdate
from app.api.routes.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[VisitorSchema])
async def get_visitors(
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = db.query(Visitor)

    if search:
        query = query.filter(
            (Visitor.name.ilike(f"%{search}%")) |
            (Visitor.company.ilike(f"%{search}%")) |
            (Visitor.phone.ilike(f"%{search}%"))
        )

    visitors = query.offset(skip).limit(limit).all()
    return visitors


@router.get("/{visitor_id}", response_model=VisitorSchema)
async def get_visitor(
    visitor_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return visitor


@router.post("/", response_model=VisitorSchema, status_code=status.HTTP_201_CREATED)
async def create_visitor(
    visitor: VisitorCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_visitor = Visitor(**visitor.model_dump())
    db.add(db_visitor)
    db.commit()
    db.refresh(db_visitor)
    return db_visitor


@router.put("/{visitor_id}", response_model=VisitorSchema)
async def update_visitor(
    visitor_id: UUID,
    visitor_update: VisitorUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if not db_visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")

    update_data = visitor_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_visitor, field, value)

    db.commit()
    db.refresh(db_visitor)
    return db_visitor


@router.delete("/{visitor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_visitor(
    visitor_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if not db_visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")

    db.delete(db_visitor)
    db.commit()
    return None

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.routes.auth import get_current_user

router = APIRouter()


@router.post("/{gate_id}/open")
async def open_gate(
    gate_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # TODO: Implement gate control logic
    return {"status": "success", "gate_id": gate_id, "action": "opened"}


@router.post("/{gate_id}/close")
async def close_gate(
    gate_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # TODO: Implement gate control logic
    return {"status": "success", "gate_id": gate_id, "action": "closed"}


@router.get("/{gate_id}/status")
async def get_gate_status(
    gate_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # TODO: Implement gate status logic
    return {"gate_id": gate_id, "status": "closed", "last_action": None}

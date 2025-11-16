from fastapi import APIRouter
import asyncio

from app.core.controller import gate_controller
from app.core.config import settings

router = APIRouter()


@router.post("/open")
async def open_gate():
    """Open the gate"""
    success = gate_controller.open()

    if success:
        # Auto-close after configured duration
        asyncio.create_task(auto_close_gate())

        return {
            "status": "success",
            "action": "opened",
            "auto_close_in": settings.GATE_OPEN_DURATION
        }

    return {
        "status": "error",
        "message": "Failed to open gate"
    }


@router.post("/close")
async def close_gate():
    """Close the gate"""
    success = gate_controller.close()

    if success:
        return {
            "status": "success",
            "action": "closed"
        }

    return {
        "status": "error",
        "message": "Failed to close gate"
    }


@router.get("/status")
async def get_status():
    """Get gate status"""
    status = gate_controller.get_status()
    return status


async def auto_close_gate():
    """Auto-close gate after configured duration"""
    await asyncio.sleep(settings.GATE_OPEN_DURATION)
    gate_controller.close()
    print(f"Gate auto-closed after {settings.GATE_OPEN_DURATION} seconds")

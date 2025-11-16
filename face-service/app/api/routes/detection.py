from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import cv2
import numpy as np

from app.core.face_detector import face_detector
from app.core.camera_manager import camera_manager

router = APIRouter()


@router.post("/detect")
async def detect_faces(file: UploadFile = File(...)):
    """Detect faces in uploaded image"""
    try:
        # Read image file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid image file"}
            )

        # Preprocess image
        image = face_detector.preprocess_image(image)

        # Detect faces
        face_locations = face_detector.detect_faces(image)

        return {
            "faces_detected": len(face_locations),
            "face_locations": face_locations,
            "is_night_mode": face_detector.is_night_mode(image)
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@router.post("/encode")
async def encode_face(file: UploadFile = File(...)):
    """Generate face encoding from uploaded image"""
    try:
        # Read image file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid image file"}
            )

        # Preprocess image
        image = face_detector.preprocess_image(image)

        # Generate encoding
        encoding = face_detector.encode_face(image)

        if encoding is None:
            return JSONResponse(
                status_code=400,
                content={"error": "No face detected in image"}
            )

        return {
            "encoding": encoding.tolist(),
            "success": True
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@router.get("/camera/status")
async def camera_status():
    """Get camera connection status"""
    return {
        "entry_camera": camera_manager.entry_camera.is_connected if camera_manager.entry_camera else False,
        "exit_camera": camera_manager.exit_camera.is_connected if camera_manager.exit_camera else False
    }

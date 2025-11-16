from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import cv2
import numpy as np

from app.core.face_detector import face_detector

router = APIRouter()


@router.post("/compare")
async def compare_faces(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    """Compare two face images"""
    try:
        # Read first image
        contents1 = await file1.read()
        nparr1 = np.frombuffer(contents1, np.uint8)
        image1 = cv2.imdecode(nparr1, cv2.IMREAD_COLOR)

        # Read second image
        contents2 = await file2.read()
        nparr2 = np.frombuffer(contents2, np.uint8)
        image2 = cv2.imdecode(nparr2, cv2.IMREAD_COLOR)

        if image1 is None or image2 is None:
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid image file"}
            )

        # Generate encodings
        encoding1 = face_detector.encode_face(image1)
        encoding2 = face_detector.encode_face(image2)

        if encoding1 is None or encoding2 is None:
            return JSONResponse(
                status_code=400,
                content={"error": "No face detected in one or both images"}
            )

        # Compare faces
        is_match, distance = face_detector.compare_faces(encoding1, encoding2)

        return {
            "is_match": is_match,
            "distance": distance,
            "confidence": max(0, 1 - distance)
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@router.post("/identify")
async def identify_face(file: UploadFile = File(...)):
    """Identify a face against database (TODO: implement database lookup)"""
    try:
        # Read image file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, np.uint8)

        if image is None:
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid image file"}
            )

        # Generate encoding
        encoding = face_detector.encode_face(image)

        if encoding is None:
            return JSONResponse(
                status_code=400,
                content={"error": "No face detected in image"}
            )

        # TODO: Compare with database encodings
        # This will be implemented when integrating with the backend

        return {
            "identified": False,
            "visitor": None,
            "confidence": 0.0
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

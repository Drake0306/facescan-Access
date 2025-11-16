from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import platform
import subprocess

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


def get_camera_names_windows():
    """Get camera names on Windows using PowerShell"""
    try:
        # Use PowerShell to get camera names - use list to avoid shell escaping issues
        cmd = ['powershell', '-Command', 'Get-PnpDevice -Class Camera | Select-Object -ExpandProperty FriendlyName']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

        if result.returncode == 0:
            # Parse the output - each line is a camera name
            names = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
            return names
        return []
    except Exception as e:
        print(f"Error getting camera names: {e}")
        return []


@router.get("/cameras/list")
async def list_available_cameras():
    """List all available camera devices"""
    try:
        available_cameras = []
        camera_names = []

        # Get camera names if on Windows
        if platform.system() == "Windows":
            camera_names = get_camera_names_windows()
            print(f"Camera names from Windows: {camera_names}")

        # Check up to 10 camera indices
        # Don't break on first failure - some indices might be skipped
        for index in range(10):
            try:
                print(f"Checking camera index {index}...")
                # Try without DirectShow first - it might be more reliable
                cap = cv2.VideoCapture(index)
                is_open = cap.isOpened()
                print(f"  Camera {index} isOpened: {is_open}")

                if is_open:
                    # Use friendly name if available, otherwise fallback to generic name
                    if index < len(camera_names) and camera_names[index]:
                        camera_name = camera_names[index]
                    else:
                        camera_name = f"Camera {index}"

                    print(f"  Adding camera: {camera_name}")
                    available_cameras.append({
                        "index": index,
                        "name": camera_name,
                        "type": "webcam",
                        "available": True
                    })
                    cap.release()
                else:
                    cap.release()
            except Exception as e:
                print(f"Error checking camera {index}: {e}")

        return {
            "cameras": available_cameras,
            "count": len(available_cameras)
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@router.post("/cameras/configure")
async def configure_cameras(entry_index: int = None, exit_index: int = None):
    """Update camera configuration"""
    try:
        result = camera_manager.update_cameras(
            entry_index=entry_index,
            exit_index=exit_index
        )

        return {
            "success": result,
            "message": "Cameras configured successfully" if result else "Failed to configure cameras",
            "entry_camera_connected": camera_manager.entry_camera.is_connected if camera_manager.entry_camera else False,
            "exit_camera_connected": camera_manager.exit_camera.is_connected if camera_manager.exit_camera else False
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import JSONResponse, Response
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
                is_open = False
                cap = None
                # Try multiple backends to detect availability
                backends = [
                    getattr(cv2, 'CAP_DSHOW', 700),
                    getattr(cv2, 'CAP_MSMF', 1400),
                    getattr(cv2, 'CAP_V4L2', 200),
                    getattr(cv2, 'CAP_AVFOUNDATION', 1200),
                    getattr(cv2, 'CAP_ANY', 0),
                ]
                for b in backends:
                    try:
                        cap = cv2.VideoCapture(index, b)
                        if cap.isOpened():
                            is_open = True
                            break
                        cap.release()
                    except Exception:
                        pass
                print(f"  Camera {index} isOpened: {is_open}")

                if is_open and cap is not None:
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
                    if cap is not None:
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


@router.get("/cameras/frame")
async def get_camera_frame(camera: str = Query("entry")):
    """Return a single JPEG frame from the requested camera.

    Query params:
    - camera: 'entry' or 'exit'
    """
    try:
        frame = None
        if camera == "entry":
            frame = camera_manager.get_entry_frame()
        elif camera == "exit":
            frame = camera_manager.get_exit_frame()
        else:
            return JSONResponse(status_code=400, content={"error": "Invalid camera. Use 'entry' or 'exit'"})

        if frame is None:
            return JSONResponse(status_code=404, content={"error": "No frame available"})

        # Encode frame as JPEG
        success, encoded = cv2.imencode('.jpg', frame)
        if not success:
            return JSONResponse(status_code=500, content={"error": "Failed to encode frame"})

        return Response(content=encoded.tobytes(), media_type="image/jpeg")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.post("/cameras/reset")
async def reset_cameras(entry_index: int = None, exit_index: int = None, restart_services: bool = False):
    """Attempt to fix stuck cameras by disconnecting and reconnecting using alternative backends.

    Optionally accepts indices to target specific cameras. If none provided, resets configured ones.
    On Windows and if restart_services is True, attempts to restart camera services (best-effort).
    """
    try:
        service_restart = False
        service_error = None

        # Try OS-specific freeing techniques similar to terminal fixes
        if restart_services:
            system = platform.system()
            try:
                if system == "Windows":
                    # Restart Windows Camera Frame Server
                    cmd = ['powershell', '-Command', 'Restart-Service -Name FrameServer -Force']
                    res = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
                    service_restart = res.returncode == 0
                    if not service_restart:
                        service_error = res.stderr.strip() or res.stdout.strip()
                    # Also attempt to restart PnP camera devices (best-effort, may need admin)
                    try:
                        cmd2 = ['powershell', '-Command', 'Get-PnpDevice -Class Camera | Restart-PnpDevice -Confirm:$false']
                        subprocess.run(cmd2, capture_output=True, text=True, timeout=8)
                    except Exception:
                        pass
                elif system == "Linux":
                    # Kill processes using /dev/videoX for targeted indices
                    for idx in set([i for i in [entry_index, exit_index] if i is not None]):
                        try:
                            dev = f"/dev/video{idx}"
                            subprocess.run(['fuser', '-k', dev], capture_output=True, text=True, timeout=5)
                        except Exception:
                            pass
                elif system == "Darwin":
                    # Restart macOS camera daemons
                    try:
                        subprocess.run(['killall', 'VDCAssistant'], capture_output=True, text=True, timeout=5)
                    except Exception:
                        pass
                    try:
                        subprocess.run(['killall', 'AppleCameraAssistant'], capture_output=True, text=True, timeout=5)
                    except Exception:
                        pass
            except Exception as e:
                service_error = str(e)

        # Now attempt reconnects using multi-backend strategy
        reset_result = camera_manager.reset_cameras(entry_index=entry_index, exit_index=exit_index)

        return {
            "success": True,
            "entry_camera_connected": reset_result.get("entry", False),
            "exit_camera_connected": reset_result.get("exit", False),
            "service_restart_attempted": restart_services,
            "service_restart_success": service_restart,
            "service_error": service_error,
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

import cv2
import numpy as np
from typing import Optional
from app.core.config import settings


class CameraStream:
    def __init__(self, camera_type: str, rtsp_url: str = "", camera_index: int = 0):
        self.camera_type = camera_type
        self.rtsp_url = rtsp_url
        self.camera_index = camera_index
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_connected = False

    def connect(self) -> bool:
        """Connect to camera stream"""
        try:
            if self.camera_type == "rtsp" and self.rtsp_url:
                self.cap = cv2.VideoCapture(self.rtsp_url)
            else:
                self.cap = cv2.VideoCapture(self.camera_index)

            if self.cap.isOpened():
                self.is_connected = True
                return True
            return False
        except Exception as e:
            print(f"Error connecting to camera: {e}")
            return False

    def disconnect(self):
        """Disconnect from camera stream"""
        if self.cap:
            self.cap.release()
            self.is_connected = False

    def get_frame(self) -> Optional[np.ndarray]:
        """Get current frame from camera"""
        if not self.is_connected or not self.cap:
            return None

        ret, frame = self.cap.read()
        if ret:
            return frame
        return None

    def reconnect(self) -> bool:
        """Reconnect to camera"""
        self.disconnect()
        return self.connect()


class CameraManager:
    def __init__(self):
        self.entry_camera: Optional[CameraStream] = None
        self.exit_camera: Optional[CameraStream] = None

    def initialize(self):
        """Initialize camera streams"""
        # Entry camera
        self.entry_camera = CameraStream(
            camera_type=settings.ENTRY_CAMERA_TYPE,
            rtsp_url=settings.ENTRY_CAMERA_RTSP,
            camera_index=settings.ENTRY_CAMERA_INDEX
        )

        # Exit camera
        self.exit_camera = CameraStream(
            camera_type=settings.EXIT_CAMERA_TYPE,
            rtsp_url=settings.EXIT_CAMERA_RTSP,
            camera_index=settings.EXIT_CAMERA_INDEX
        )

        # Connect cameras
        entry_connected = self.entry_camera.connect()
        exit_connected = self.exit_camera.connect()

        return {
            "entry": entry_connected,
            "exit": exit_connected
        }

    def get_entry_frame(self) -> Optional[np.ndarray]:
        """Get frame from entry camera"""
        if self.entry_camera:
            return self.entry_camera.get_frame()
        return None

    def get_exit_frame(self) -> Optional[np.ndarray]:
        """Get frame from exit camera"""
        if self.exit_camera:
            return self.exit_camera.get_frame()
        return None

    def update_cameras(self, entry_index: int = None, exit_index: int = None) -> bool:
        """Update camera configuration with new indices"""
        try:
            success = True

            # Update entry camera if index provided
            if entry_index is not None:
                if self.entry_camera:
                    self.entry_camera.disconnect()

                self.entry_camera = CameraStream(
                    camera_type="webcam",
                    camera_index=entry_index
                )
                entry_connected = self.entry_camera.connect()
                if not entry_connected:
                    success = False
                    print(f"Failed to connect to entry camera at index {entry_index}")

            # Update exit camera if index provided
            if exit_index is not None:
                if self.exit_camera:
                    self.exit_camera.disconnect()

                self.exit_camera = CameraStream(
                    camera_type="webcam",
                    camera_index=exit_index
                )
                exit_connected = self.exit_camera.connect()
                if not exit_connected:
                    success = False
                    print(f"Failed to connect to exit camera at index {exit_index}")

            return success

        except Exception as e:
            print(f"Error updating cameras: {e}")
            return False

    def shutdown(self):
        """Disconnect all cameras"""
        if self.entry_camera:
            self.entry_camera.disconnect()
        if self.exit_camera:
            self.exit_camera.disconnect()


# Singleton instance
camera_manager = CameraManager()

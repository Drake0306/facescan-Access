import cv2
import face_recognition
import numpy as np
from typing import List, Tuple, Optional

from app.core.config import settings


class FaceDetector:
    def __init__(self):
        self.detection_model = settings.FACE_DETECTION_MODEL
        self.encoding_model = settings.FACE_ENCODING_MODEL

    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in an image.
        Returns list of face locations as (top, right, bottom, left)
        """
        # Convert BGR to RGB (OpenCV uses BGR, face_recognition uses RGB)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect faces
        face_locations = face_recognition.face_locations(
            rgb_image,
            model=self.detection_model
        )

        return face_locations

    def encode_face(self, image: np.ndarray, face_location: Optional[Tuple] = None) -> Optional[np.ndarray]:
        """
        Generate face encoding from image.
        If face_location is provided, use it; otherwise detect faces first.
        """
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if face_location is None:
            # Detect faces first
            face_locations = face_recognition.face_locations(rgb_image, model=self.detection_model)
            if not face_locations:
                return None
            face_location = face_locations[0]  # Use first detected face

        # Generate encoding
        encodings = face_recognition.face_encodings(
            rgb_image,
            known_face_locations=[face_location],
            model=self.encoding_model
        )

        if encodings:
            return encodings[0]
        return None

    def compare_faces(
        self,
        known_encoding: np.ndarray,
        unknown_encoding: np.ndarray,
        tolerance: float = None
    ) -> Tuple[bool, float]:
        """
        Compare two face encodings.
        Returns (is_match, distance)
        """
        if tolerance is None:
            tolerance = settings.FACE_RECOGNITION_THRESHOLD

        # Calculate face distance
        distance = face_recognition.face_distance([known_encoding], unknown_encoding)[0]

        # Check if match
        is_match = distance <= tolerance

        return is_match, float(distance)

    def enhance_image(self, image: np.ndarray) -> np.ndarray:
        """
        Enhance image for better face detection (especially for low light)
        """
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)

        # Merge channels
        enhanced_lab = cv2.merge([l, a, b])

        # Convert back to BGR
        enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

        return enhanced

    def is_night_mode(self, image: np.ndarray) -> bool:
        """
        Determine if image is in low light conditions
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Calculate average brightness
        avg_brightness = np.mean(gray)

        return avg_brightness < settings.NIGHT_MODE_THRESHOLD

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image before face detection
        """
        if settings.ENABLE_FACE_ENHANCEMENT and self.is_night_mode(image):
            image = self.enhance_image(image)

        return image


# Singleton instance
face_detector = FaceDetector()

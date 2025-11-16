from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Face Recognition
    FACE_RECOGNITION_THRESHOLD: float = 0.6
    FACE_DETECTION_MODEL: str = "hog"  # Options: hog, cnn
    FACE_ENCODING_MODEL: str = "large"  # Options: small, large

    # Camera Configuration
    ENTRY_CAMERA_TYPE: str = "webcam"  # Options: rtsp, webcam
    ENTRY_CAMERA_RTSP: str = ""
    ENTRY_CAMERA_INDEX: int = 0

    EXIT_CAMERA_TYPE: str = "webcam"
    EXIT_CAMERA_RTSP: str = ""
    EXIT_CAMERA_INDEX: int = 1

    # Image Processing
    NIGHT_MODE_THRESHOLD: int = 50
    ENABLE_FACE_ALIGNMENT: bool = True
    ENABLE_FACE_ENHANCEMENT: bool = True

    # Database
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_NAME: str = "facescan_db"
    DB_USER: str = "facescan_user"
    DB_PASSWORD: str = "changeme"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

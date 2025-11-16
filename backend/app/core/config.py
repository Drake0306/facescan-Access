from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Project info
    PROJECT_NAME: str = "FaceScan Access API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_NAME: str = "facescan_db"
    DB_USER: str = "facescan_user"
    DB_PASSWORD: str = "changeme"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

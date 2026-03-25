from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # Security and JWT settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Database connection URL
    DATABASE_URL: str = "sqlite:///./job_portal.db"

    # Directory for file uploads
    UPLOAD_DIR: str = "./uploads"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create an instance of Settings
settings = Settings()

# Ensure upload directory exists
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

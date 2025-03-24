from typing import Any, Dict, Optional, List, Union
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, validator, AnyHttpUrl, EmailStr, HttpUrl, field_validator
import os
import json
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Pledge"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    SERVER_NAME: str = os.getenv("SERVER_NAME", "Pledge API")
    SERVER_HOST: AnyHttpUrl = os.getenv("SERVER_HOST", "http://localhost:8000")
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # Database
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "pledge")
    SQLALCHEMY_DATABASE_URI: PostgresDsn = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: str) -> str:
        if isinstance(v, str):
            return v
        return str(v)

    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))

    # JWT
    ALGORITHM: str = "HS256"

    # SMS Configuration
    ADVANTA_SMS_API_KEY: str = os.getenv("ADVANTA_SMS_API_KEY", "")
    ADVANTA_SMS_SENDER_ID: str = os.getenv("ADVANTA_SMS_SENDER_ID", "CHURCH")

    # Celery Configuration
    CELERY_BROKER_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    CELERY_RESULT_BACKEND: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

    # Email Settings
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    EMAILS_FROM_EMAIL: EmailStr = os.getenv("EMAILS_FROM_EMAIL", "noreply@pledge.com")
    EMAILS_FROM_NAME: str = "Pledge"

    # SMS Settings
    SMS_API_KEY: str = os.getenv("SMS_API_KEY", "")
    SMS_API_URL: str = os.getenv("SMS_API_URL", "https://api.sms-provider.com/v1")
    SMS_SENDER_ID: str = os.getenv("SMS_SENDER_ID", "Pledge")

    # File Upload Settings
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB
    ALLOWED_FILE_EXTENSIONS: List[str] = os.getenv("ALLOWED_FILE_EXTENSIONS", ["pdf", "doc", "docx", "xls", "xlsx", "jpg", "jpeg", "png"])

    # Stripe Settings
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            try:
                # Try to parse as JSON array
                return json.loads(v)
            except json.JSONDecodeError:
                # If not JSON, try comma-separated string
                return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(v)

    DESCRIPTION: str = "Pledge API for managing contributions and pledges"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 
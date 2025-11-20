"""Configuration settings for the financial analysis application."""

import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings."""

    # Base directory
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/financial_analysis.db")

    # Application Settings
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    # API Settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    # CORS Settings
    CORS_ORIGINS: List[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:5173,http://localhost:5174,http://localhost:5175,http://localhost:5176,http://127.0.0.1:3000,http://127.0.0.1:5173,http://127.0.0.1:5174,http://127.0.0.1:5175,http://127.0.0.1:5176"
    ).split(",")

    # Data Import Settings
    DEFAULT_IMPORT_PATH: str = os.getenv("DEFAULT_IMPORT_PATH", str(BASE_DIR / "data" / "transactions.xlsx"))
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB default

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", str(BASE_DIR / "logs" / "app.log"))

    # Database Settings
    DB_ECHO: bool = DEBUG  # Echo SQL statements in debug mode


# Create settings instance
settings = Settings()

# Legacy exports for backward compatibility
BASE_DIR = settings.BASE_DIR
DATABASE_URL = settings.DATABASE_URL
APP_ENV = settings.APP_ENV
DEBUG = settings.DEBUG
DEFAULT_IMPORT_PATH = settings.DEFAULT_IMPORT_PATH
LOG_LEVEL = settings.LOG_LEVEL
LOG_FILE = settings.LOG_FILE
DB_ECHO = settings.DB_ECHO


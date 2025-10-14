import os

from typing import Literal, cast
from pydantic_settings import BaseSettings

class EnvironmentSettings(BaseSettings):
    """
    Application configuration settings loaded from environment variables or defaults.

    Args:
        BaseSettings: Pydantic BaseSettings class that provides environment variable parsing and validation.
    """
    # --- General ---
    ENVIRONMENT: str = cast(Literal['production', 'development', 'approval', 'local'], os.getenv('ENVIRONMENT'))
    DEBUG: bool = bool(os.getenv('DEBUG', False))

    # --- Logging ---
    LOG_LEVEL: str = cast(Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], os.getenv('LOG_LEVEL'))
    LOG_PATH: str = os.getenv('LOG_PATH', '')

    # --- Database ---
    DB_DIR: str = os.getenv('DB_DIR', '')
    DB_FILE: str = os.getenv('DB_FILE', '')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

# --- Singleton Instance ---
settings = EnvironmentSettings()
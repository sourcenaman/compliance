"""Configuration management for the RMF Compliance Engine."""

from dotenv import load_dotenv
from functools import lru_cache
import os
from pydantic_settings import BaseSettings

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "compliance")


class Settings:
    """Application settings loaded from environment variables."""
    
    # Database
    database_host: str = DB_HOST
    database_port: int = int(DB_PORT)
    database_user: str = DB_USER
    database_password: str = DB_PASSWORD
    database_name: str = DB_NAME
    
    # Application
    debug: bool = False
    log_level: str = "INFO"
    
    # API
    api_title: str = "RMF Compliance Engine"
    api_version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

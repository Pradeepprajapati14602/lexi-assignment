"""
Application configuration using Pydantic settings.
Loads environment variables and provides app-wide config.
"""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union
import os


class Settings(BaseSettings):
    """Application settings - UOIONHHC"""
    
    # API Keys
    GEMINI_API_KEY: str = ""
    EXA_API_KEY: str = ""
    
    # Database
    DATABASE_URL: str = "sqlite:///./lexi.db"
    
    # Server
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    
    # CORS
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".doc"]
    UPLOAD_DIR: str = "uploads"
    
    # Gemini Settings
    GEMINI_MODEL: str = "gemini-1.5-flash"
    GEMINI_EMBEDDING_MODEL: str = "models/embedding-001"
    GEMINI_MAX_TOKENS: int = 8192
    GEMINI_TEMPERATURE: float = 0.3
    
    # Template Processing
    CHUNK_SIZE: int = 4000  # characters per chunk
    MIN_CONFIDENCE_THRESHOLD: float = 0.6
    
    # Exa Settings
    EXA_NUM_RESULTS: int = 5
    EXA_TEXT_LENGTH: int = 2000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

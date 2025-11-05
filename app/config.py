from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379"
    database_url: str = "sqlite:///./healthlens.db"
    ai_service_url: str = "https://vertex-ai-endpoint"
    cors_origins: List[str] = [
        "http://localhost:8080", 
        "http://localhost:3000",
        "http://localhost:5173",
        "https://localhost:3000",
        "https://localhost:5173",
        "https://healthlens-ui-main-320501699885.us-central1.run.app"
    ]
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Gemini AI Configuration
    gemini_api_key: str = ""
    gemini_model: str = "models/gemini-2.5-flash"
    gemini_endpoint: str = "https://generativelanguage.googleapis.com/v1beta/models"
    
    # Cache Configuration
    cache_ttl: int = 3600

    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields from environment

settings = Settings()
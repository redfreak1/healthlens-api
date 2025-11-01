from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379"
    database_url: str = "sqlite:///./healthlens.db"
    ai_service_url: str = "https://vertex-ai-endpoint"
    cors_origins: List[str] = ["http://localhost:8080", "http://localhost:3000"]
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
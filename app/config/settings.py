"""
HealthLens API Configuration with Corporate Proxy Support and Gemini AI
"""
import os
from typing import Dict, List

class Settings:
    """Application settings with proxy configuration and Gemini AI"""
    
    # API Configuration
    API_HOST: str = "localhost"
    API_PORT: int = 8000
    DEBUG: bool = True
    API_VERSION: str = "v1"
    
    # Corporate Proxy Configuration
    PROXY_URL: str = "http://tproxy02.qdx.com:9090"
    NO_PROXY: str = "localhost,127.0.0.1,::1"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Create React App
        "http://localhost:8080",  # Alternative dev server
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://healthlens-ui-main-320501699885.us-central1.run.app",  # Cloud Run frontend
    ]
    
    # Redis Configuration (optional)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./healthlens.db"
    
    # Gemini AI Configuration
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY', '')
    GEMINI_MODEL: str = os.getenv('GEMINI_MODEL', 'gemini-pro')
    GEMINI_ENDPOINT: str = os.getenv('GEMINI_ENDPOINT', 'https://generativelanguage.googleapis.com/v1beta/models')
    
    # Cache Configuration
    CACHE_TTL: int = int(os.getenv('CACHE_TTL', '3600'))
    
    @property
    def proxy_dict(self) -> Dict[str, str]:
        """Return proxy configuration for HTTP clients"""
        return {
            'http': self.PROXY_URL,
            'https': self.PROXY_URL,
        }
    
    @property
    def proxy_env_vars(self) -> Dict[str, str]:
        """Return environment variables for proxy configuration"""
        return {
            'HTTP_PROXY': self.PROXY_URL,
            'HTTPS_PROXY': self.PROXY_URL,
            'http_proxy': self.PROXY_URL,
            'https_proxy': self.PROXY_URL,
            'no_proxy': self.NO_PROXY,
        }
    
    def setup_proxy_environment(self):
        """Set up proxy environment variables"""
        for key, value in self.proxy_env_vars.items():
            os.environ[key] = value

# Create global settings instance
settings = Settings()

# Auto-setup proxy environment when module is imported
settings.setup_proxy_environment()
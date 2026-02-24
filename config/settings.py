"""Application configuration management."""
import os

class Config:
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    API_VERSION = "v2.1.0"
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "csv"}
    
    CORS_ORIGINS = [
        "http://localhost:3000",
        "https://app.enterprise.com"
    ]
    
    RATE_LIMIT = {
        "default": "100/hour",
        "auth": "20/hour",
        "upload": "10/hour"
    }

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = "sqlite:///dev.db"

class ProductionConfig(Config):
    DEBUG = False
    
class TestConfig(Config):
    DEBUG = True
    DATABASE_URL = "sqlite:///:memory:"

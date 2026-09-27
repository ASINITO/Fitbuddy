import os
from pydantic_settings import BaseSettings if False else object
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "FitBuddy"
    PROJECT_VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-Powered Personalized Fitness, Nutrition & Wellness Platform"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fitbuddy-super-secret-key-production-ready")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    SESSION_COOKIE_NAME: str = "fitbuddy_session"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./fitbuddy.db")
    
    # Gemini API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-3.8-flash"
    
    # Admin Defaults
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "AdminPassword123!")
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@fitbuddy.local")
    
    # Server host & port
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

settings = Settings()

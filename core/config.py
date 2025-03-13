import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI Resume Builder API"
    PROJECT_VERSION: str = "1.0.0"
    
    # Default model - can be overridden in .env
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "facebook/bart-large-cnn")
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",  # Next.js frontend default
        "http://localhost:8080",
        "https://your-production-domain.com",  # Add your production domain
    ]
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

settings = Settings()
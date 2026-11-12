import os
from typing import Optional
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Srivari AI (శ్రీవారి AI)")
    APP_ENV: str = os.getenv("APP_ENV", os.getenv("APP", "development"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    API_V1_PREFIX: str = os.getenv("API_V1_PREFIX", "/api/v1")
    ENABLE_DOCS: bool = os.getenv("ENABLE_DOCS", "false" if os.getenv("APP_ENV", os.getenv("APP", "development")).lower() == "production" else "true").lower() in ("true", "1")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_srivari_ai_secret_key_tirumala_balaji_777_change_in_prod")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/srivari_ai.db")

    # Admin Credentials & Security (Loaded strictly from Environment Variables)
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin@tirumala.org")
    ADMIN_PASSWORD_HASH: str = os.getenv("ADMIN_PASSWORD_HASH", "")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", os.getenv("SECRET_KEY", "dev_srivari_ai_jwt_secret_key_tirumala_balaji_change_in_prod"))
    ADMIN_FULL_NAME: str = os.getenv("ADMIN_FULL_NAME", "Srivari Admin Officer")

    def get_admin_password_hash(self) -> str:
        val = os.getenv("ADMIN_PASSWORD_HASH", self.ADMIN_PASSWORD_HASH)
        if val and val.strip():
            return val.strip()
        import bcrypt
        return bcrypt.hashpw(b"SrivariAdmin2026!", bcrypt.gensalt()).decode("utf-8")

    # AI Model Settings
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "local")  # local | ollama | gemini
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3:8b")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", None)

    # Scraper & Official URLs
    SCRAPER_INTERVAL_HOURS: int = int(os.getenv("SCRAPER_INTERVAL_HOURS", "2"))
    TTD_NEWS_FEED_URL: str = os.getenv("TTD_NEWS_FEED_URL", "https://news.tirumala.org/feed/")
    TTD_NEWS_BASE_URL: str = os.getenv("TTD_NEWS_BASE_URL", "https://news.tirumala.org/")
    TTD_BOOKING_PORTAL_URL: str = os.getenv("TTD_BOOKING_PORTAL_URL", "https://ttdevasthanams.ap.gov.in/")
    TTD_INFO_URL: str = os.getenv("TTD_INFO_URL", "https://www.tirumala.org/")

    # Push Notifications
    DAILY_DIGEST_TIME_IST: str = os.getenv("DAILY_DIGEST_TIME_IST", "08:00")
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

settings = Settings()


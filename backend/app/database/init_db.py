import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.database.base import Base
from app.database.session import engine, SessionLocal
from app.models.admin import Admin
from app.models.announcement import AnnouncementCategory
from app.models.setting import ApplicationSetting
from app.security.hashing import hash_password
from app.config import settings
from app.scraper.ttd_scraper import TTDScraperService

logger = logging.getLogger("srivari.init_db")

DEFAULT_CATEGORIES = [
    {
        "name_en": "Darshan",
        "name_te": "దర్శనం",
        "slug": "darshan",
        "icon_name": "visibility",
        "color_hex": "#D4AF37",
        "display_order": 1
    },
    {
        "name_en": "Srivari Seva",
        "name_te": "శ్రీవారి సేవ",
        "slug": "srivari-seva",
        "icon_name": "volunteer_activism",
        "color_hex": "#800000",
        "display_order": 2
    },
    {
        "name_en": "Quota Release",
        "name_te": "కోటా విడుదల",
        "slug": "quota-release",
        "icon_name": "calendar_month",
        "color_hex": "#FF9933",
        "display_order": 3
    },
    {
        "name_en": "Accommodation",
        "name_te": "వసతి & గదులు",
        "slug": "accommodation",
        "icon_name": "hotel",
        "color_hex": "#138808",
        "display_order": 4
    },
    {
        "name_en": "Festivals & Events",
        "name_te": "ఉత్సవాలు & పండుగలు",
        "slug": "festivals",
        "icon_name": "celebration",
        "color_hex": "#9C27B0",
        "display_order": 5
    },
    {
        "name_en": "Laddu Prasadam",
        "name_te": "లడ్డూ ప్రసాదం",
        "slug": "laddu-prasadam",
        "icon_name": "restaurant",
        "color_hex": "#E65100",
        "display_order": 6
    },
    {
        "name_en": "Recruitment",
        "name_te": "ఉద్యోగ ప్రకటనలు",
        "slug": "recruitment",
        "icon_name": "work",
        "color_hex": "#0288D1",
        "display_order": 7
    },
    {
        "name_en": "General Notice",
        "name_te": "సాధారణ ప్రకటనలు",
        "slug": "general-notice",
        "icon_name": "info",
        "color_hex": "#607D8B",
        "display_order": 8
    }
]

def init_database():
    """
    Initializes database schema, seed categories, initial admin, and seeds verified announcements.
    """
    logger.info("Initializing Srivari AI database schema...")
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # 1. Seed Categories
        for cat in DEFAULT_CATEGORIES:
            existing_cat = db.query(AnnouncementCategory).filter(AnnouncementCategory.slug == cat["slug"]).first()
            if not existing_cat:
                new_cat = AnnouncementCategory(**cat)
                db.add(new_cat)
        db.commit()

        # 2. Seed Super Admin
        existing_admin = db.query(Admin).filter(Admin.username == settings.ADMIN_USERNAME).first()
        if not existing_admin:
            super_admin = Admin(
                username=settings.ADMIN_USERNAME,
                email="admin@tirumala.org",
                hashed_password=hash_password(settings.ADMIN_PASSWORD),
                full_name=settings.ADMIN_FULL_NAME,
                role="super_admin",
                created_at=datetime.now(timezone.utc)
            )
            db.add(super_admin)
            db.commit()
            logger.info(f"Created default Super Admin: {settings.ADMIN_USERNAME}")

        # 3. Seed Default Application Settings
        default_settings = {
            "scraper_interval_hours": str(settings.SCRAPER_INTERVAL_HOURS),
            "ai_provider": settings.AI_PROVIDER,
            "daily_digest_time_ist": settings.DAILY_DIGEST_TIME_IST,
            "system_disclaimer": "Srivari AI is an independent informational guide and is not officially affiliated with TTD."
        }
        for k, v in default_settings.items():
            if not db.query(ApplicationSetting).filter(ApplicationSetting.key == k).first():
                db.add(ApplicationSetting(key=k, value=v))
        db.commit()

        # 4. Ingest and Sync Official TTD Announcements into DB and RAG index
        scraper = TTDScraperService(db)
        scraper.sync_news_sync()
        logger.info("Database initialization and verified TTD announcements ingestion complete.")
    finally:
        db.close()

if __name__ == "__main__":
    init_database()


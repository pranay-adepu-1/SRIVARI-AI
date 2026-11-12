import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.database.base import Base
from app.database.session import engine, SessionLocal
from sqlalchemy import text
from app.models.admin import Admin
from app.models.announcement import AnnouncementCategory
from app.models.document import KnowledgeDocument
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

        # 4. Safe SQLite migration helper for is_pinned column
        try:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE announcements ADD COLUMN is_pinned BOOLEAN DEFAULT 0"))
                conn.commit()
        except Exception:
            pass  # Column already exists

        # 5. Seed Initial Knowledge Documents if empty
        if db.query(KnowledgeDocument).count() == 0:
            seed_docs = [
                {
                    "filename": "TTD_Darshan_Rules_and_Quotas_2026.txt",
                    "title": "TTD ₹300 Special Entry Darshan Regulations & Reporting Rules",
                    "source_type": "Official TTD Manual",
                    "status": "Indexed",
                    "chunk_count": 3,
                    "content": (
                        "The ₹300 Special Entry Darshan (Seeghra Darshan) is introduced by TTD to provide quick and organized darshan of Lord Venkateswara at Tirumala hills. Devotees must book slots strictly online in advance through the official portal https://ttdevasthanams.ap.gov.in/.\n\n"
                        "Reporting details: Devotees must report at the Vaikuntam Queue Complex-1 (ATC Car Parking area) strictly according to the time slot printed on their booking receipt. Every devotee including children above 12 years must produce an original government identity card (Aadhaar, Passport, or Voter ID).\n\n"
                        "Dress code for darshan: Strict traditional attire is mandatory. Men must wear Dhoti with Uttariyam, Kurta with Pyjama, or Lungi with Shirt. Women must wear Saree, Half-Saree (Pavada), or Chudidar with Dupatta/Chunni. Jeans, T-shirts, western outfits, shorts, and skirts are strictly prohibited."
                    )
                },
                {
                    "filename": "Srivari_Seva_Voluntary_Guidelines.txt",
                    "title": "Srivari Seva Voluntary Service Guidelines & Reporting Sadan",
                    "source_type": "Official TTD Manual",
                    "status": "Indexed",
                    "chunk_count": 3,
                    "content": (
                        "Srivari Seva is a self-less voluntary service dedicated to Lord Venkateswara. Devotees aged between 18 and 60 years who are physically and mentally fit can register online for General Srivari Seva and Parakamani Seva at https://ttdevasthanams.ap.gov.in/.\n\n"
                        "Service tenure: General Srivari Seva is conducted for 7 days in Tirumala and Tirupati temples. Sevaks assist pilgrims at Laddu distribution counters, Annaprasadam complexes, queue lines, water distribution, and pilgrim guidance desks.\n\n"
                        "Reporting rules: All selected Sevaks must assemble at Srivari Seva Sadan in Tirumala one day prior to service commencement. Sevaks must carry original Aadhaar card and printed registration slip. Traditional uniform (white Dhoti/Kurta for men, yellow or maroon Saree with scarf for women) is mandatory throughout the seva period."
                    )
                },
                {
                    "filename": "Tirumala_Accommodation_Rules.txt",
                    "title": "Tirumala Accommodation Caution Deposit & Checkout Policy",
                    "source_type": "Official TTD Manual",
                    "status": "Indexed",
                    "chunk_count": 3,
                    "content": (
                        "Accommodation in Tirumala is allotted for a maximum duration of 24 hours only. Devotees holding confirmed online darshan tickets can book rooms online at https://ttdevasthanams.ap.gov.in/. Offline current booking counters are available at CRO (Central Reservation Office) Tirumala subject to availability.\n\n"
                        "Caution deposit policy: A refundable caution deposit is collected at the time of allotment along with room tariff. If the room is vacated within 24 hours in good condition, the caution deposit is automatically refunded to the original payment source within 3 to 7 working days.\n\n"
                        "Guest house rules: All occupants must be present with original ID cards at the sub-allotment counter. Alcohol, smoking, non-vegetarian food, and gambling are strictly prohibited across all Tirumala guest houses and cottages."
                    )
                },
                {
                    "filename": "TTD_Traditional_Dress_Code_Mandate.txt",
                    "title": "TTD Sacred Dress Code Mandate & Prohibited Electronics",
                    "source_type": "Official TTD Manual",
                    "status": "Indexed",
                    "chunk_count": 2,
                    "content": (
                        "TTD strictly enforces Vedic and traditional dress code for all pilgrims entering Vaikuntam Queue Complex and the sanctum sanctorum of Lord Venkateswara temple.\n\n"
                        "Mandatory dress code: Men: White or cream Dhoti / Vesti with Melangi / Uttariyam, or Kurta with Pyjama. Women: Saree, Half-Saree (Langa Voni), or Chudidar / Salwar Kameez with Dupatta / Chunni properly draped. Children: Traditional dress or decent modest clothing.\n\n"
                        "Prohibited items: Mobile phones, smart watches, digital cameras, audio/video recorders, earphones, power banks, tobacco, matchboxes, and sharp objects are strictly prohibited beyond the scanning security gates at Vaikuntam Queue Complex."
                    )
                }
            ]
            for doc_item in seed_docs:
                db.add(KnowledgeDocument(**doc_item))
            db.commit()
            logger.info("Default TTD knowledge documents seeded.")

        # 6. Ingest and Sync Official TTD Announcements into DB and RAG index
        scraper = TTDScraperService(db)
        scraper.sync_news_sync()
        logger.info("Database initialization and verified TTD announcements ingestion complete.")
    finally:
        db.close()

if __name__ == "__main__":
    init_database()


import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.config import settings
from app.database.session import SessionLocal
from app.scraper.ttd_scraper import TTDScraperService

logger = logging.getLogger("srivari.scheduler")
scheduler = AsyncIOScheduler()

async def scheduled_scraper_job():
    logger.info("Starting scheduled TTD news synchronization...")
    db = SessionLocal()
    try:
        service = TTDScraperService(db)
        result = await service.fetch_and_sync_news()
        logger.info(f"Scheduled sync complete: {result}")
    except Exception as e:
        logger.error(f"Error in scheduled sync job: {e}")
    finally:
        db.close()

def start_scraper_scheduler():
    interval = max(1, min(24, settings.SCRAPER_INTERVAL_HOURS))
    scheduler.add_job(
        scheduled_scraper_job,
        'interval',
        hours=interval,
        id='ttd_news_poller',
        replace_existing=True
    )
    scheduler.start()
    logger.info(f"Scraper scheduler started. Polling every {interval} hour(s).")

def stop_scraper_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scraper scheduler stopped.")


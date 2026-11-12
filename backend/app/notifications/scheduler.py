import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database.session import SessionLocal
from app.notifications.fcm_service import FCMNotificationService

logger = logging.getLogger("srivari.daily_digest")
digest_scheduler = AsyncIOScheduler()

async def send_daily_digest_job():
    logger.info("Executing 8:00 AM IST Daily Tirumala Update Digest...")
    db = SessionLocal()
    try:
        service = FCMNotificationService(db)
        service.broadcast_notification(
            title_en="Daily Tirumala Update - Srivari AI",
            title_te="నేటి తిరుమల సమాచారం - శ్రీవారి AI",
            body_en="Om Namo Venkatesaya! Today's SSD token status, waiting times, and upcoming seva quota schedule are now updated in the app.",
            body_te="ఓం నమో వేంకటేశాయ! నేటి సర్వ దర్శనం టోకెన్ల వివరాలు, కంపార్ట్‌మెంట్ల సమాచారం మరియు కోటా వివరాలు యాప్‌లో చూడండి.",
            notification_type="daily_digest"
        )
    except Exception as e:
        logger.error(f"Failed to dispatch daily digest: {e}")
    finally:
        db.close()

def start_daily_digest_scheduler():
    # 8:00 AM IST is 02:30 AM UTC
    digest_scheduler.add_job(
        send_daily_digest_job,
        'cron',
        hour=2,
        minute=30,
        id='daily_tirumala_digest',
        replace_existing=True
    )
    digest_scheduler.start()
    logger.info("Daily 8:00 AM IST digest notification scheduler initiated.")

def stop_daily_digest_scheduler():
    if digest_scheduler.running:
        digest_scheduler.shutdown()


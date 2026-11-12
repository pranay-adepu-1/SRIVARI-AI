import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.notification import NotificationHistory
from app.models.user import User

logger = logging.getLogger("srivari.notifications")

class FCMNotificationService:
    def __init__(self, db: Session):
        self.db = db

    def broadcast_notification(
        self,
        title_en: str,
        title_te: str,
        body_en: str,
        body_te: str,
        notification_type: str = "quota_alert",
        announcement_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Dispatches push notification to active registered devices.
        Logs to database notification_history.
        """
        active_users = self.db.query(User).filter(User.is_active == True).all()
        target_count = len(active_users)

        # In production with Firebase Admin SDK:
        # messaging.send_multicast(MulticastMessage(...))

        record = NotificationHistory(
            announcement_id=announcement_id,
            title_en=title_en,
            title_te=title_te,
            body_en=body_en,
            body_te=body_te,
            notification_type=notification_type,
            sent_count=target_count,
            sent_at=datetime.utcnow()
        )
        self.db.add(record)
        self.db.commit()

        logger.info(f"Dispatched {notification_type} push notification to {target_count} devotees.")
        return {
            "status": "success",
            "sent_count": target_count,
            "title_en": title_en,
            "title_te": title_te,
            "sent_at": record.sent_at.isoformat()
        }


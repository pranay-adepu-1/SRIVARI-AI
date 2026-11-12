from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.notification import NotificationHistory, NotificationSubscription
from app.schemas.notification import NotificationHistoryResponse, NotificationPreferenceUpdate

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/history", response_model=List[NotificationHistoryResponse])
def get_notification_history(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Returns dispatched notifications history.
    """
    return db.query(NotificationHistory).order_by(desc(NotificationHistory.sent_at)).limit(limit).all()

@router.post("/preferences")
def update_preferences(
    payload: NotificationPreferenceUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates notification category subscriptions for the current devotee.
    """
    sub = db.query(NotificationSubscription).filter(NotificationSubscription.user_id == user.id).first()
    if not sub:
        sub = NotificationSubscription(
            user_id=user.id,
            category_id=payload.category_id,
            daily_digest=payload.daily_digest,
            instant_quota_alerts=payload.instant_quota_alerts
        )
        db.add(sub)
    else:
        sub.category_id = payload.category_id
        sub.daily_digest = payload.daily_digest
        sub.instant_quota_alerts = payload.instant_quota_alerts

    db.commit()
    return {"status": "success", "message": "Preferences updated successfully"}


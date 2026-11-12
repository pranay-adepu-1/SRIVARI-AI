from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class NotificationPreferenceUpdate(BaseModel):
    category_id: Optional[str] = None
    daily_digest: bool = True
    instant_quota_alerts: bool = True

class NotificationHistoryResponse(BaseModel):
    id: str
    announcement_id: Optional[str] = None
    title_en: str
    title_te: str
    body_en: str
    body_te: str
    notification_type: str
    sent_count: int
    sent_at: datetime

    class Config:
        from_attributes = True

class NotificationBroadcastRequest(BaseModel):
    title_en: str
    title_te: str
    body_en: str
    body_te: str
    notification_type: str = "quota_alert"
    announcement_id: Optional[str] = None


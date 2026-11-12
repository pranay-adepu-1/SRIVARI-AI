import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, ForeignKey
from app.database.base import Base

class NotificationSubscription(Base):
    __tablename__ = "notification_subscriptions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(String(36), ForeignKey("announcement_categories.id", ondelete="CASCADE"), nullable=True)
    daily_digest = Column(Boolean, nullable=False, default=True)
    instant_quota_alerts = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

class NotificationHistory(Base):
    __tablename__ = "notification_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    announcement_id = Column(String(36), ForeignKey("announcements.id", ondelete="SET NULL"), nullable=True)
    title_en = Column(String(255), nullable=False)
    title_te = Column(String(255), nullable=False)
    body_en = Column(Text, nullable=False)
    body_te = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False, default="quota_alert")  # daily_digest, quota_alert, breaking
    sent_count = Column(Integer, nullable=False, default=0)
    sent_at = Column(DateTime, nullable=False, default=datetime.utcnow)


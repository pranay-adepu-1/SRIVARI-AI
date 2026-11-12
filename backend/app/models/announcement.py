import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class AnnouncementCategory(Base):
    __tablename__ = "announcement_categories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name_en = Column(String(100), unique=True, nullable=False)
    name_te = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    icon_name = Column(String(50), nullable=False, default="notifications")
    color_hex = Column(String(10), nullable=False, default="#D4AF37")
    display_order = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)

    announcements = relationship("Announcement", back_populates="category", cascade="all, delete-orphan")

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    category_id = Column(String(36), ForeignKey("announcement_categories.id", ondelete="SET NULL"), nullable=True)
    title_en = Column(Text, nullable=False)
    title_te = Column(Text, nullable=False)
    content_en = Column(Text, nullable=False)
    content_te = Column(Text, nullable=False)
    source_url = Column(Text, nullable=False)
    source_domain = Column(String(100), nullable=False, default="news.tirumala.org")
    content_hash = Column(String(64), unique=True, nullable=False, index=True)
    publication_date = Column(DateTime, nullable=False, index=True)
    is_verified = Column(Boolean, nullable=False, default=True)
    is_quota_alert = Column(Boolean, nullable=False, default=False)
    quota_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("AnnouncementCategory", back_populates="announcements")
    bookmarks = relationship("Bookmark", back_populates="announcement", cascade="all, delete-orphan")

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    announcement_id = Column(String(36), ForeignKey("announcements.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    announcement = relationship("Announcement", back_populates="bookmarks")


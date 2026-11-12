from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name_en: str
    name_te: str
    slug: str
    icon_name: str
    color_hex: str
    display_order: int = 0
    is_active: bool = True

class CategoryResponse(CategoryBase):
    id: str

    class Config:
        from_attributes = True

class AnnouncementBase(BaseModel):
    category_id: Optional[str] = None
    title_en: str
    title_te: str
    content_en: str
    content_te: str
    source_url: str
    source_domain: str = "news.tirumala.org"
    publication_date: datetime
    is_verified: bool = True
    is_quota_alert: bool = False
    is_pinned: bool = False
    quota_date: Optional[datetime] = None

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(BaseModel):
    title_en: Optional[str] = None
    title_te: Optional[str] = None
    content_en: Optional[str] = None
    content_te: Optional[str] = None
    category_id: Optional[str] = None
    is_verified: Optional[bool] = None
    is_quota_alert: Optional[bool] = None
    is_pinned: Optional[bool] = None
    quota_date: Optional[datetime] = None

class AnnouncementResponse(AnnouncementBase):
    id: str
    content_hash: str
    created_at: datetime
    updated_at: datetime
    is_bookmarked: bool = False

    class Config:
        from_attributes = True

class AnnouncementListResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: List[AnnouncementResponse]


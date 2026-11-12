from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.announcement import Announcement, AnnouncementCategory, Bookmark
from app.schemas.announcement import AnnouncementCreate, AnnouncementUpdate
from app.scraper.parser import generate_content_hash
from app.ai.embeddings import search_engine

class AnnouncementService:
    def __init__(self, db: Session):
        self.db = db

    def list_announcements(
        self,
        category_slug: Optional[str] = None,
        search_query: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        query = self.db.query(Announcement).filter(Announcement.is_verified == True)

        if category_slug and category_slug != "all":
            category = self.db.query(AnnouncementCategory).filter(AnnouncementCategory.slug == category_slug).first()
            if category:
                query = query.filter(Announcement.category_id == category.id)

        if search_query:
            term = f"%{search_query}%"
            query = query.filter(
                (Announcement.title_en.ilike(term)) |
                (Announcement.title_te.ilike(term)) |
                (Announcement.content_en.ilike(term)) |
                (Announcement.content_te.ilike(term))
            )

        total = query.count()
        offset = (page - 1) * limit
        items = query.order_by(desc(Announcement.is_pinned), desc(Announcement.publication_date)).offset(offset).limit(limit).all()

        bookmarked_ids = set()
        if user_id:
            user_bms = self.db.query(Bookmark.announcement_id).filter(Bookmark.user_id == user_id).all()
            bookmarked_ids = {b[0] for b in user_bms}

        result_items = []
        for a in items:
            data = {
                "id": a.id,
                "category_id": a.category_id,
                "title_en": a.title_en,
                "title_te": a.title_te,
                "content_en": a.content_en,
                "content_te": a.content_te,
                "source_url": a.source_url,
                "source_domain": a.source_domain,
                "content_hash": a.content_hash,
                "publication_date": a.publication_date,
                "is_verified": a.is_verified,
                "is_quota_alert": a.is_quota_alert,
                "is_pinned": getattr(a, "is_pinned", False),
                "quota_date": a.quota_date,
                "created_at": a.created_at,
                "updated_at": a.updated_at,
                "is_bookmarked": a.id in bookmarked_ids
            }
            result_items.append(data)

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "items": result_items
        }

    def get_announcement(self, announcement_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        a = self.db.query(Announcement).filter(Announcement.id == announcement_id).first()
        if not a:
            return None

        is_bm = False
        if user_id:
            bm = self.db.query(Bookmark).filter(Bookmark.user_id == user_id, Bookmark.announcement_id == announcement_id).first()
            is_bm = bm is not None

        return {
            "id": a.id,
            "category_id": a.category_id,
            "title_en": a.title_en,
            "title_te": a.title_te,
            "content_en": a.content_en,
            "content_te": a.content_te,
            "source_url": a.source_url,
            "source_domain": a.source_domain,
            "content_hash": a.content_hash,
            "publication_date": a.publication_date,
            "is_verified": a.is_verified,
            "is_quota_alert": a.is_quota_alert,
            "quota_date": a.quota_date,
            "created_at": a.created_at,
            "updated_at": a.updated_at,
            "is_bookmarked": is_bm
        }

    def toggle_bookmark(self, user_id: str, announcement_id: str) -> bool:
        bm = self.db.query(Bookmark).filter(Bookmark.user_id == user_id, Bookmark.announcement_id == announcement_id).first()
        if bm:
            self.db.delete(bm)
            self.db.commit()
            return False  # Unbookmarked
        else:
            new_bm = Bookmark(user_id=user_id, announcement_id=announcement_id)
            self.db.add(new_bm)
            self.db.commit()
            return True  # Bookmarked

    def list_bookmarks(self, user_id: str) -> List[Dict[str, Any]]:
        bms = self.db.query(Bookmark).filter(Bookmark.user_id == user_id).all()
        results = []
        for b in bms:
            a = b.announcement
            if a:
                results.append({
                    "id": a.id,
                    "category_id": a.category_id,
                    "title_en": a.title_en,
                    "title_te": a.title_te,
                    "content_en": a.content_en,
                    "content_te": a.content_te,
                    "source_url": a.source_url,
                    "source_domain": a.source_domain,
                    "content_hash": a.content_hash,
                    "publication_date": a.publication_date,
                    "is_verified": a.is_verified,
                    "is_quota_alert": a.is_quota_alert,
                    "quota_date": a.quota_date,
                    "created_at": a.created_at,
                    "updated_at": a.updated_at,
                    "is_bookmarked": True
                })
        return results


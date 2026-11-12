from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.api.deps import get_current_user_optional, get_current_user
from app.models.user import User
from app.models.announcement import AnnouncementCategory
from app.schemas.announcement import AnnouncementResponse, AnnouncementListResponse, CategoryResponse
from app.services.announcement_service import AnnouncementService

router = APIRouter(prefix="/announcements", tags=["Announcements"])

@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """
    Returns all active announcement categories.
    """
    return db.query(AnnouncementCategory).filter(AnnouncementCategory.is_active == True).order_by(AnnouncementCategory.display_order).all()

@router.get("", response_model=AnnouncementListResponse)
def list_announcements(
    category: Optional[str] = Query(None, description="Category slug"),
    search: Optional[str] = Query(None, description="Search keyword"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    Retrieves paginated verified announcements with optional category filter and keyword search.
    """
    service = AnnouncementService(db)
    user_id = user.id if user else None
    return service.list_announcements(
        category_slug=category,
        search_query=search,
        page=page,
        limit=limit,
        user_id=user_id
    )

@router.get("/saved", response_model=List[AnnouncementResponse])
def get_saved_announcements(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns all bookmarked announcements for the current devotee.
    """
    service = AnnouncementService(db)
    return service.list_bookmarks(user.id)

@router.get("/{announcement_id}", response_model=AnnouncementResponse)
def get_announcement(
    announcement_id: str,
    user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    Retrieves single announcement by ID.
    """
    service = AnnouncementService(db)
    user_id = user.id if user else None
    result = service.get_announcement(announcement_id, user_id=user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Announcement not found")
    return result

@router.post("/{announcement_id}/bookmark")
def toggle_bookmark(
    announcement_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Toggles bookmark status of an announcement for current devotee.
    """
    service = AnnouncementService(db)
    is_bookmarked = service.toggle_bookmark(user.id, announcement_id)
    return {"status": "success", "is_bookmarked": is_bookmarked}


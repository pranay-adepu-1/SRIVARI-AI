from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.announcement import Bookmark
from app.schemas.user import UserProfileResponse, UserProfileUpdate

router = APIRouter(prefix="/users", tags=["Devotee Profile"])

@router.get("/profile", response_model=UserProfileResponse)
def get_profile(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns devotee profile details and bookmarks count.
    """
    bm_count = db.query(Bookmark).filter(Bookmark.user_id == user.id).count()
    return {
        "id": user.id,
        "email": user.email,
        "phone_number": user.phone_number,
        "device_id": user.device_id,
        "preferred_language": user.preferred_language,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "last_active_at": user.last_active_at,
        "bookmarks_count": bm_count
    }

@router.patch("/profile", response_model=UserProfileResponse)
def update_profile(
    payload: UserProfileUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates devotee preferred language or details.
    """
    if payload.preferred_language:
        user.preferred_language = payload.preferred_language
    if payload.email is not None:
        user.email = payload.email
    if payload.phone_number is not None:
        user.phone_number = payload.phone_number
    if payload.fcm_token is not None:
        user.fcm_token = payload.fcm_token

    db.commit()
    db.refresh(user)

    bm_count = db.query(Bookmark).filter(Bookmark.user_id == user.id).count()
    return {
        "id": user.id,
        "email": user.email,
        "phone_number": user.phone_number,
        "device_id": user.device_id,
        "preferred_language": user.preferred_language,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "last_active_at": user.last_active_at,
        "bookmarks_count": bm_count
    }


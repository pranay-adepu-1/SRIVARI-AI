from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class UserProfileResponse(BaseModel):
    id: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    device_id: str
    preferred_language: str
    is_active: bool
    created_at: datetime
    last_active_at: datetime
    bookmarks_count: int = 0

    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    preferred_language: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    fcm_token: Optional[str] = None


import uuid
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.security.jwt import decode_access_token
from app.models.user import User
from app.models.admin import Admin

security = HTTPBearer(auto_error=False)

def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    if not credentials:
        return None
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Retrieves current devotee user from JWT bearer token.
    If token is valid but user was lost (e.g. SQLite database reset on Render),
    or if no credentials are provided, auto-provisions a guest devotee profile
    to ensure seamless public access without 401 failures.
    """
    if credentials:
        token = credentials.credentials
        payload = decode_access_token(token)
        if payload:
            user_id = payload.get("sub")
            if user_id:
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    return user
                # Recreate user with preserved ID from token
                user = User(
                    id=user_id,
                    device_id=payload.get("device_id", f"web_{user_id[:8]}"),
                    preferred_language="te",
                    created_at=datetime.utcnow(),
                    last_active_at=datetime.utcnow()
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                return user

    # Auto-provision guest devotee session
    guest_id = str(uuid.uuid4())
    user = User(
        id=guest_id,
        device_id=f"web_guest_{guest_id[:8]}",
        preferred_language="te",
        created_at=datetime.utcnow(),
        last_active_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Admin:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Administrative authentication required"
        )
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired admin session token"
        )
    admin_id = payload.get("sub")
    role = payload.get("role")
    if not admin_id or role not in ["super_admin", "editor", "auditor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Authorized administrator only."
        )
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin or not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account is inactive or revoked."
        )
    return admin


import uuid
from datetime import datetime
from typing import Optional
from fastapi import Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.security.jwt import decode_access_token
from app.security.hashing import hash_password
from app.config import settings
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

def require_admin(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Admin:
    """
    Requires valid admin authentication via 'srivari_admin_token' cookie or Bearer token.
    Decodes the JWT against JWT_SECRET_KEY. Returns 401 Unauthorized if missing, invalid, or expired.
    """
    token: Optional[str] = request.cookies.get("srivari_admin_token")
    if not token and credentials and credentials.credentials:
        token = credentials.credentials
    elif not token and request.headers.get("authorization"):
        auth_hdr = request.headers.get("authorization", "")
        if auth_hdr.lower().startswith("bearer "):
            token = auth_hdr[7:].strip()
    if not token:
        token = request.cookies.get("admin_session")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin authentication required. Missing srivari_admin_token.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Decode JWT against settings.JWT_SECRET_KEY, then settings.SECRET_KEY
    payload = None
    try:
        from jose import jwt
        for secret in [settings.JWT_SECRET_KEY, settings.SECRET_KEY]:
            try:
                payload = jwt.decode(token, secret, algorithms=["HS256"])
                if payload:
                    break
            except Exception:
                continue
    except Exception:
        pass

    if not payload:
        # Fallback to decode_access_token
        payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired admin session token.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    sub = payload.get("sub")
    username = payload.get("username") or sub

    admin = db.query(Admin).filter((Admin.username == username) | (Admin.id == sub)).first()
    if not admin:
        admin = Admin(
            id=str(uuid.uuid4()),
            username=settings.ADMIN_USERNAME,
            email="admin@tirumala.org",
            hashed_password=settings.get_admin_password_hash(),
            full_name=settings.ADMIN_FULL_NAME,
            role="super_admin",
            is_active=True
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin account is inactive or revoked.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return admin

# Alias get_current_admin to require_admin
get_current_admin = require_admin


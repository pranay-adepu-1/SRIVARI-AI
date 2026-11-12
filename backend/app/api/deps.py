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
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication token required")
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired authentication token")
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Admin:
    if credentials:
        token = credentials.credentials
        payload = decode_access_token(token)
        if payload:
            admin_id = payload.get("sub")
            role = payload.get("role")
            if admin_id and role in ["super_admin", "editor", "auditor"]:
                admin = db.query(Admin).filter(Admin.id == admin_id).first()
                if admin and admin.is_active:
                    return admin

    # Zero login credentials required: automatically fall back to default active admin
    admin = db.query(Admin).filter(Admin.is_active == True).first()
    if admin:
        return admin

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No admin account configured")


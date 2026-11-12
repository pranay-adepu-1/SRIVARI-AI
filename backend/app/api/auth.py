from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.auth import DevoteeInitRequest, DevoteeInitResponse, AdminLoginRequest, AdminLoginResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/devotee-init", response_model=DevoteeInitResponse)
def devotee_init(payload: DevoteeInitRequest, db: Session = Depends(get_db)):
    """
    Initializes or retrieves devotee profile by device_id and issues access token.
    """
    service = AuthService(db)
    result = service.devotee_init(
        device_id=payload.device_id,
        preferred_language=payload.preferred_language,
        fcm_token=payload.fcm_token
    )
    return result

@router.post("/admin-login", response_model=AdminLoginResponse)
def admin_login(payload: AdminLoginRequest, db: Session = Depends(get_db)):
    """
    Authenticates administrator and issues JWT token.
    """
    service = AuthService(db)
    result = service.admin_login(username=payload.username, password=payload.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid administrative credentials"
        )
    return result

@router.post("/admin-quick-access", response_model=AdminLoginResponse)
def admin_quick_access(db: Session = Depends(get_db)):
    """
    Convenience endpoint for instant administrative demo access without manual credentials.
    """
    service = AuthService(db)
    return service.admin_quick_access()



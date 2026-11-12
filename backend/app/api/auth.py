from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.auth import DevoteeInitRequest, DevoteeInitResponse, AdminLoginRequest, AdminLoginResponse
from app.services.auth_service import AuthService
from app.security.rate_limiter import admin_login_rate_limiter
from app.config import settings

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
def admin_login(
    payload: AdminLoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Authenticates administrator and issues JWT token and HTTP-only session cookie.
    Rate-limited to 5 attempts per 15 minutes per IP.
    """
    client_ip = request.client.host if request.client else "127.0.0.1"
    if not admin_login_rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many admin login attempts. Please try again after 15 minutes."
        )

    service = AuthService(db)
    result = service.admin_login(username=payload.username, password=payload.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid administrative credentials"
        )

    # Set HTTP-only session cookie
    response.set_cookie(
        key="admin_session",
        value=result["access_token"],
        httponly=True,
        samesite="lax",
        secure=False if settings.DEBUG else True,
        max_age=86400,
        path="/"
    )
    return result

@router.post("/admin-quick-access", response_model=AdminLoginResponse)
def admin_quick_access(response: Response, db: Session = Depends(get_db)):
    """
    Convenience endpoint for instant administrative demo access without manual credentials.
    Sets HTTP-only session cookie.
    """
    service = AuthService(db)
    result = service.admin_quick_access()
    response.set_cookie(
        key="admin_session",
        value=result["access_token"],
        httponly=True,
        samesite="lax",
        secure=False if settings.DEBUG else True,
        max_age=86400,
        path="/"
    )
    return result

@router.post("/admin-logout")
def admin_logout(response: Response):
    """
    Clears administrative HTTP-only session cookie.
    """
    response.delete_cookie(key="admin_session", path="/")
    return {"status": "success", "message": "Logged out successfully"}




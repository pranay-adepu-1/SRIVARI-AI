import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.admin import Admin
from app.security.hashing import verify_password, hash_password
from app.security.jwt import create_access_token

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def devotee_init(self, device_id: str, preferred_language: str = "te", fcm_token: str = None):
        user = self.db.query(User).filter(User.device_id == device_id).first()
        if not user:
            user = User(
                id=str(uuid.uuid4()),
                device_id=device_id,
                preferred_language=preferred_language,
                fcm_token=fcm_token,
                created_at=datetime.utcnow(),
                last_active_at=datetime.utcnow()
            )
            self.db.add(user)
        else:
            user.last_active_at = datetime.utcnow()
            if fcm_token:
                user.fcm_token = fcm_token
            if preferred_language:
                user.preferred_language = preferred_language

        self.db.commit()
        self.db.refresh(user)

        token = create_access_token({"sub": user.id, "role": "devotee", "device_id": user.device_id})
        return {
            "user_id": user.id,
            "access_token": token,
            "token_type": "bearer",
            "preferred_language": user.preferred_language
        }

    def admin_login(self, username: str, password: str):
        admin = self.db.query(Admin).filter(Admin.username == username).first()
        if not admin or not verify_password(password, admin.hashed_password):
            return None

        admin.last_login_at = datetime.utcnow()
        self.db.commit()

        token = create_access_token({"sub": admin.id, "role": admin.role, "username": admin.username})
        return {
            "access_token": token,
            "token_type": "bearer",
            "admin": {
                "id": admin.id,
                "username": admin.username,
                "full_name": admin.full_name,
                "role": admin.role
            }
        }


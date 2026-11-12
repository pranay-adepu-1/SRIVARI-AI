from typing import Optional
from pydantic import BaseModel, EmailStr

class DevoteeInitRequest(BaseModel):
    device_id: str
    preferred_language: str = "te"
    fcm_token: Optional[str] = None

class DevoteeInitResponse(BaseModel):
    user_id: str
    access_token: str
    token_type: str = "bearer"
    preferred_language: str

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class AdminResponse(BaseModel):
    id: str
    username: str
    full_name: str
    role: str

class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin: AdminResponse


from app.api.auth import router as auth_router
from app.api.announcements import router as announcements_router
from app.api.chat import router as chat_router
from app.api.darshan import router as darshan_router
from app.api.notifications import router as notifications_router
from app.api.users import router as users_router
from app.api.admin import router as admin_router
from app.api.system import router as system_router

__all__ = [
    "auth_router",
    "announcements_router",
    "chat_router",
    "darshan_router",
    "notifications_router",
    "users_router",
    "admin_router",
    "system_router"
]


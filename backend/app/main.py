import logging
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database.init_db import init_database
from app.scraper.scheduler import start_scraper_scheduler, stop_scraper_scheduler
from app.notifications.scheduler import start_daily_digest_scheduler, stop_daily_digest_scheduler
from app.security.rate_limiter import rate_limiter

from app.api.auth import router as auth_router
from app.api.announcements import router as announcements_router
from app.api.chat import router as chat_router
from app.api.darshan import router as darshan_router
from app.api.notifications import router as notifications_router
from app.api.users import router as users_router
from app.api.admin import router as admin_router
from app.api.system import router as system_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("srivari.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Database & RAG Search Engine
    logger.info("Initializing Srivari AI backend application...")
    init_database()
    
    # Start Schedulers
    start_scraper_scheduler()
    start_daily_digest_scheduler()
    
    yield
    
    # Shutdown
    logger.info("Shutting down background schedulers...")
    stop_scraper_scheduler()
    stop_daily_digest_scheduler()

app = FastAPI(
    title=settings.APP_NAME,
    description="Intelligent bilingual (English & Telugu) Tirumala Devotee Assistant powered by RAG and official TTD data.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting Middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "127.0.0.1"
    # Skip rate limiting for static assets and documentation
    if not request.url.path.startswith(settings.API_V1_PREFIX):
        return await call_next(request)

    if not rate_limiter.is_allowed(client_ip):
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Too many requests. Please slow down your requests."}
        )
    return await call_next(request)

# Include API Routers under prefix
api_prefix = settings.API_V1_PREFIX
app.include_router(auth_router, prefix=api_prefix)
app.include_router(announcements_router, prefix=api_prefix)
app.include_router(chat_router, prefix=api_prefix)
app.include_router(darshan_router, prefix=api_prefix)
app.include_router(notifications_router, prefix=api_prefix)
app.include_router(users_router, prefix=api_prefix)
app.include_router(admin_router, prefix=api_prefix)
app.include_router(system_router, prefix=api_prefix)

# Mount Admin Dashboard UI
admin_dir = Path(__file__).resolve().parent.parent.parent / "admin"
if admin_dir.exists():
    app.mount("/admin-ui", StaticFiles(directory=str(admin_dir), html=True), name="admin_ui")

@app.get("/")
def root():
    return {
        "app": "Srivari AI (శ్రీవారి AI)",
        "tagline": "Your Intelligent Tirumala Assistant",
        "official_disclaimer": "Independent devotional informational assistant. Not affiliated with TTD.",
        "api_docs": "/docs",
        "admin_portal": "/admin-ui/"
    }


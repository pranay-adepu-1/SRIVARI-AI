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
    try:
        init_database()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization warning: {e}")

    # Start Background Schedulers
    try:
        start_scraper_scheduler()
    except Exception as e:
        logger.warning(f"Scraper scheduler warning: {e}")

    try:
        start_daily_digest_scheduler()
    except Exception as e:
        logger.warning(f"Digest scheduler warning: {e}")

    yield

    # Shutdown
    logger.info("Shutting down background schedulers...")
    try:
        stop_scraper_scheduler()
        stop_daily_digest_scheduler()
    except Exception as e:
        logger.warning(f"Scheduler shutdown warning: {e}")

docs_url = "/docs" if settings.ENABLE_DOCS else None
redoc_url = "/redoc" if settings.ENABLE_DOCS else None
openapi_url = "/openapi.json" if settings.ENABLE_DOCS else None

app = FastAPI(
    title=settings.APP_NAME,
    description="Intelligent bilingual (English & Telugu) Tirumala Devotee Assistant powered by RAG and official TTD data.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url
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
admin_dirs = [
    Path(__file__).resolve().parent.parent.parent / "admin",
    Path(__file__).resolve().parent.parent / "admin",
    Path.cwd() / "admin",
    Path.cwd() / ".." / "admin"
]
admin_dir = next((d for d in admin_dirs if d.exists()), None)
if admin_dir:
    app.mount("/admin-ui", StaticFiles(directory=str(admin_dir), html=True), name="admin_ui")

# Mount Public Devotee Portal UI
devotee_dirs = [
    Path(__file__).resolve().parent.parent.parent / "devotee-portal",
    Path(__file__).resolve().parent.parent / "devotee-portal",
    Path.cwd() / "devotee-portal",
    Path.cwd() / ".." / "devotee-portal"
]
devotee_dir = next((d for d in devotee_dirs if d.exists()), None)
if devotee_dir:
    app.mount("/portal", StaticFiles(directory=str(devotee_dir), html=True), name="devotee_portal")

@app.get("/")
def root(request: Request):
    accept = request.headers.get("accept", "")
    if "text/html" in accept and devotee_dir and (devotee_dir / "index.html").exists():
        return FileResponse(str(devotee_dir / "index.html"))

    resp = {
        "app": "Srivari AI (శ్రీవారి AI)",
        "tagline": "Your Intelligent Tirumala Assistant",
        "official_disclaimer": "Independent devotional informational assistant. Not affiliated with TTD.",
        "devotee_portal": "/portal",
        "official_sources": [
            "https://news.tirumala.org/",
            "https://ttdevasthanams.ap.gov.in/",
            "https://www.tirumala.org/"
        ]
    }
    if settings.ENABLE_DOCS:
        resp["api_docs"] = "/docs"
    return resp


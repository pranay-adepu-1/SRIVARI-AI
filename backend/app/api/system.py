from fastapi import APIRouter
from app.config import settings

router = APIRouter(prefix="/system", tags=["System & Health"])

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": "1.0.0",
        "ai_provider": settings.AI_PROVIDER,
        "official_sources": [
            "https://news.tirumala.org/",
            "https://ttdevasthanams.ap.gov.in/",
            "https://www.tirumala.org/"
        ]
    }

@router.get("/disclaimer")
def get_disclaimer():
    return {
        "disclaimer_en": "Srivari AI (శ్రీవారి AI) is an independent, non-commercial informational assistant developed to assist devotees with verified temple guidelines. It is NOT officially affiliated with or endorsed by Tirumala Tirupati Devasthanams (TTD). Official online bookings must be completed exclusively on https://ttdevasthanams.ap.gov.in/.",
        "disclaimer_te": "శ్రీవారి AI అనేది భక్తులకు ఖచ్చితమైన మరియు అధికారిక సమాచారాన్ని అందించడానికి రూపొందించబడిన స్వతంత్ర సమాచార వేదిక. దీనికి తిరుమల తిరుపతి దేవస్థానం (టీటీడీ) తో ఎలాంటి ప్రత్యక్ష అధికారిక అనుబంధం లేదు. భక్తులు తమ టికెట్లు, దర్శనం, సేవలు మరియు వసతి బుకింగ్స్ కోసం అధికారిక పోర్టల్ https://ttdevasthanams.ap.gov.in/ మాత్రమే ఉపయోగించాలి."
    }


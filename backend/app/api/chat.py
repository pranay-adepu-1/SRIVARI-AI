import logging
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.chat import ChatQueryRequest, ChatQueryResponse, ChatSessionResponse, ChatMessageResponse
from app.services.chat_service import ChatService

logger = logging.getLogger("srivari.chat")
router = APIRouter(prefix="/chat", tags=["AI Chatbot"])

@router.post("/query", response_model=ChatQueryResponse)
async def ask_question(
    payload: ChatQueryRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submits a devotee question to Srivari AI RAG engine.
    Supports Telugu and English, cites official TTD sources, and verifies against hallucinations.
    """
    try:
        service = ChatService(db)
        result = await service.handle_query(
            user_id=user.id,
            query=payload.query,
            session_id=payload.session_id,
            language=payload.language or user.preferred_language,
            is_voice=payload.is_voice
        )
        return result
    except Exception as e:
        logger.exception("Error processing chat query '%s': %s", payload.query, e)
        # Return graceful devotional response instead of unhandled error
        is_te = (payload.language == "te") or (user.preferred_language == "te")
        error_answer = (
            "ఓం నమో వేంకటేశాయ! ప్రస్తుతం సర్వర్‌లో సమాచారం ప్రాసెస్ చేయడంలో సాంకేతిక అంతరాయం ఏర్పడింది. "
            "దయచేసి అధికారిక వివరాల కోసం https://ttdevasthanams.ap.gov.in/ ని చూడండి."
            if is_te else
            "Om Namo Venkatesaya! We encountered a temporary technical issue retrieving verified temple details. "
            "Please check the official TTD portal directly at https://ttdevasthanams.ap.gov.in/."
        )
        return {
            "session_id": payload.session_id or str(uuid.uuid4()),
            "answer": error_answer,
            "reply": error_answer,
            "response": error_answer,
            "language": "te" if is_te else "en",
            "is_verified": False,
            "citations": [
                {
                    "title": "టీటీడీ అధికారిక పోర్టల్" if is_te else "TTD Official Booking Portal",
                    "url": "https://ttdevasthanams.ap.gov.in/",
                    "source": "ttdevasthanams.ap.gov.in"
                }
            ],
            "suggested_questions": [
                "రూ. 300 ప్రత్యేక ప్రవేశ దర్శనం నియమాలు ఏమిటి?" if is_te else "What are the rules for ₹300 Special Entry Darshan?",
                "శ్రీవారి సేవకు ఎలా రిజిస్టర్ చేసుకోవాలి?" if is_te else "How do I register for Srivari Seva voluntary service?"
            ]
        }

@router.get("/sessions", response_model=List[ChatSessionResponse])
def get_user_sessions(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns devotee conversation history sessions.
    """
    service = ChatService(db)
    return service.list_sessions(user.id)

@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
def get_session_messages(
    session_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns messages within a specific chat session.
    """
    service = ChatService(db)
    return service.get_messages(user.id, session_id)


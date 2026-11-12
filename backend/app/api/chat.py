from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.chat import ChatQueryRequest, ChatQueryResponse, ChatSessionResponse, ChatMessageResponse
from app.services.chat_service import ChatService

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
    service = ChatService(db)
    result = await service.handle_query(
        user_id=user.id,
        query=payload.query,
        session_id=payload.session_id,
        language=payload.language or user.preferred_language,
        is_voice=payload.is_voice
    )
    return result

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


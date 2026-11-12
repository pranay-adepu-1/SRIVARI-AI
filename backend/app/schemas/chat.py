from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class CitationItem(BaseModel):
    title: str
    url: str
    source: str
    published_date: Optional[str] = None

class ChatQueryRequest(BaseModel):
    session_id: Optional[str] = None
    query: str
    language: Optional[str] = None  # if None, auto-detected
    is_voice: bool = False

class ChatQueryResponse(BaseModel):
    session_id: str
    answer: str
    reply: Optional[str] = None
    response: Optional[str] = None
    language: str
    is_verified: bool
    citations: List[CitationItem] = []
    suggested_questions: List[str] = []

class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    sender: str
    content: str
    language: str
    citations: Optional[List[Dict[str, Any]]] = None
    is_voice: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ChatSessionResponse(BaseModel):
    id: str
    title: str
    language: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

    class Config:
        from_attributes = True


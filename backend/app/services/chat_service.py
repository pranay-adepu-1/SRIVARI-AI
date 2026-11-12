import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.chat import ChatSession, ChatMessage
from app.ai.rag_engine import rag_engine

class ChatService:
    def __init__(self, db: Session):
        self.db = db

    async def handle_query(
        self,
        user_id: str,
        query: str,
        session_id: Optional[str] = None,
        language: Optional[str] = None,
        is_voice: bool = False
    ) -> Dict[str, Any]:
        # Retrieve or create session
        session = None
        if session_id:
            session = self.db.query(ChatSession).filter(ChatSession.id == session_id, ChatSession.user_id == user_id).first()

        if not session:
            title = query[:30] + ("..." if len(query) > 30 else "")
            session = ChatSession(
                id=str(uuid.uuid4()),
                user_id=user_id,
                title=title,
                language=language or "te",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)

        # Store user query
        user_msg = ChatMessage(
            id=str(uuid.uuid4()),
            session_id=session.id,
            sender="user",
            content=query,
            language=language or "te",
            is_voice=is_voice,
            created_at=datetime.utcnow()
        )
        self.db.add(user_msg)
        self.db.commit()

        # Run RAG generation
        rag_output = await rag_engine.generate_answer(query=query, user_language=language)

        # Store assistant response
        bot_msg = ChatMessage(
            id=str(uuid.uuid4()),
            session_id=session.id,
            sender="assistant",
            content=rag_output["answer"],
            language=rag_output["language"],
            citations=rag_output["citations"],
            is_voice=False,
            created_at=datetime.utcnow()
        )
        self.db.add(bot_msg)
        session.updated_at = datetime.utcnow()
        self.db.commit()

        ans = rag_output["answer"]
        return {
            "session_id": session.id,
            "answer": ans,
            "reply": ans,
            "response": ans,
            "language": rag_output["language"],
            "is_verified": rag_output["is_verified"],
            "citations": rag_output["citations"],
            "suggested_questions": rag_output["suggested_questions"]
        }

    def list_sessions(self, user_id: str):
        sessions = self.db.query(ChatSession).filter(ChatSession.user_id == user_id).order_by(ChatSession.updated_at.desc()).all()
        return [
            {
                "id": s.id,
                "title": s.title,
                "language": s.language,
                "created_at": s.created_at,
                "updated_at": s.updated_at,
                "message_count": len(s.messages)
            }
            for s in sessions
        ]

    def get_messages(self, user_id: str, session_id: str):
        session = self.db.query(ChatSession).filter(ChatSession.id == session_id, ChatSession.user_id == user_id).first()
        if not session:
            return []
        return [
            {
                "id": m.id,
                "session_id": m.session_id,
                "sender": m.sender,
                "content": m.content,
                "language": m.language,
                "citations": m.citations,
                "is_voice": m.is_voice,
                "created_at": m.created_at
            }
            for m in session.messages
        ]


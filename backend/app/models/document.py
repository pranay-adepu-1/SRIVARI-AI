import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime
from app.database.base import Base

class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    chunk_count = Column(Integer, nullable=False, default=1)
    status = Column(String(50), nullable=False, default="Indexed")  # "Indexed" | "Failed"
    source_type = Column(String(50), nullable=False, default="Manual Upload")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


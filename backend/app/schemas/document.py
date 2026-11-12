from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class DocumentUploadRequest(BaseModel):
    title: str
    filename: Optional[str] = None
    content: str
    source_type: Optional[str] = "Manual Upload"

class DocumentResponse(BaseModel):
    id: str
    filename: str
    title: str
    chunk_count: int
    status: str
    source_type: str
    created_at: datetime
    updated_at: datetime
    preview: Optional[str] = None

    class Config:
        from_attributes = True

class DocumentListResponse(BaseModel):
    total: int
    items: List[DocumentResponse]

class RAGTestRequest(BaseModel):
    query: str
    top_k: int = 4

class RAGChunkResult(BaseModel):
    rank: int
    title: str
    source_type: str
    source_url: str
    filename: Optional[str] = None
    score: float
    chunk_content: str
    publication_date: Optional[str] = None

class RAGTestResponse(BaseModel):
    query: str
    total_retrieved: int
    results: List[RAGChunkResult]

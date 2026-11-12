import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database.session import get_db
from app.api.deps import get_current_admin
from app.models.admin import Admin
from app.models.announcement import Announcement, AnnouncementCategory
from app.models.user import User
from app.models.chat import ChatMessage, ChatSession
from app.models.notification import NotificationHistory
from app.models.audit import AuditLog
from app.models.document import KnowledgeDocument
from app.schemas.announcement import AnnouncementCreate, AnnouncementUpdate, AnnouncementResponse
from app.schemas.notification import NotificationBroadcastRequest
from app.schemas.document import DocumentUploadRequest, DocumentResponse, DocumentListResponse, RAGTestRequest, RAGTestResponse
from app.scraper.ttd_scraper import TTDScraperService
from app.scraper.parser import generate_content_hash
from app.notifications.fcm_service import FCMNotificationService
from app.services.audit_service import AuditService

router = APIRouter(prefix="/admin", tags=["Admin Portal"])

@router.get("/dashboard-stats")
def get_dashboard_stats(
    admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Returns platform key metrics for administrative dashboard.
    """
    total_announcements = db.query(Announcement).count()
    verified_announcements = db.query(Announcement).filter(Announcement.is_verified == True).count()
    quota_alerts = db.query(Announcement).filter(Announcement.is_quota_alert == True).count()
    total_users = db.query(User).count()
    total_chat_sessions = db.query(ChatSession).count()
    total_messages = db.query(ChatMessage).count()
    total_notifications = db.query(NotificationHistory).count()

    return {
        "total_announcements": total_announcements,
        "verified_announcements": verified_announcements,
        "quota_alerts": quota_alerts,
        "total_users": total_users,
        "total_chat_sessions": total_chat_sessions,
        "total_messages": total_messages,
        "total_notifications": total_notifications,
        "admin": {
            "id": admin.id,
            "username": admin.username,
            "full_name": admin.full_name,
            "role": admin.role
        }
    }

@router.post("/scraper/sync")
async def trigger_manual_scraper_sync(
    admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Triggers immediate synchronization from official TTD news feeds.
    """
    scraper = TTDScraperService(db)
    result = await scraper.fetch_and_sync_news()

    AuditService.log(
        db=db,
        action="manual_scraper_sync",
        entity_type="scraper",
        admin_id=admin.id,
        details=result
    )

    return result

@router.post("/announcements", response_model=AnnouncementResponse)
def create_announcement(
    payload: AnnouncementCreate,
    admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Creates a new official announcement.
    """
    content_hash = generate_content_hash(payload.source_url, payload.title_en)
    existing = db.query(Announcement).filter(Announcement.content_hash == content_hash).first()
    if existing:
        raise HTTPException(status_code=400, detail="Announcement with this title and URL already exists.")

    new_item = Announcement(
        id=str(uuid.uuid4()),
        category_id=payload.category_id,
        title_en=payload.title_en,
        title_te=payload.title_te,
        content_en=payload.content_en,
        content_te=payload.content_te,
        source_url=payload.source_url,
        source_domain=payload.source_domain,
        content_hash=content_hash,
        publication_date=payload.publication_date,
        is_verified=payload.is_verified,
        is_quota_alert=payload.is_quota_alert,
        is_pinned=payload.is_pinned,
        quota_date=payload.quota_date,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    # Refresh RAG search engine
    TTDScraperService(db).refresh_search_index()

    AuditService.log(
        db=db,
        action="create_announcement",
        entity_type="announcement",
        admin_id=admin.id,
        entity_id=new_item.id
    )

    return new_item

@router.put("/announcements/{announcement_id}", response_model=AnnouncementResponse)
def update_announcement(
    announcement_id: str,
    payload: AnnouncementUpdate,
    admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Updates an existing announcement.
    """
    item = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Announcement not found")

    if payload.title_en is not None:
        item.title_en = payload.title_en
    if payload.title_te is not None:
        item.title_te = payload.title_te
    if payload.content_en is not None:
        item.content_en = payload.content_en
    if payload.content_te is not None:
        item.content_te = payload.content_te
    if payload.category_id is not None:
        item.category_id = payload.category_id
    if payload.is_verified is not None:
        item.is_verified = payload.is_verified
    if payload.is_quota_alert is not None:
        item.is_quota_alert = payload.is_quota_alert
    if payload.is_pinned is not None:
        item.is_pinned = payload.is_pinned
    if payload.quota_date is not None:
        item.quota_date = payload.quota_date

    item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(item)

    # Refresh RAG index
    TTDScraperService(db).refresh_search_index()

    AuditService.log(
        db=db,
        action="update_announcement",
        entity_type="announcement",
        admin_id=admin.id,
        entity_id=item.id
    )

    return item

@router.delete("/announcements/{announcement_id}")
def delete_announcement(
    announcement_id: str,
    admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Deletes an announcement.
    """
    item = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Announcement not found")

    db.delete(item)
    db.commit()

    # Refresh RAG index
    TTDScraperService(db).refresh_search_index()

    AuditService.log(
        db=db,
        action="delete_announcement",
        entity_type="announcement",
        admin_id=admin.id,
        entity_id=announcement_id
    )

    return {"status": "success", "message": "Announcement deleted successfully"}

@router.post("/notifications/broadcast")
def broadcast_push(
    payload: NotificationBroadcastRequest,
    admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Dispatches push notification broadcast to active devotees.
    """
    fcm = FCMNotificationService(db)
    result = fcm.broadcast_notification(
        title_en=payload.title_en,
        title_te=payload.title_te,
        body_en=payload.body_en,
        body_te=payload.body_te,
        notification_type=payload.notification_type,
        announcement_id=payload.announcement_id
    )

    AuditService.log(
        db=db,
        action="broadcast_notification",
        entity_type="notification",
        admin_id=admin.id,
        details=result
    )

    return result

@router.get("/audit-logs")
def list_audit_logs(
    limit: int = 50,
    admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Returns audit trail of administrative actions.
    """
    logs = db.query(AuditLog).order_by(desc(AuditLog.created_at)).limit(limit).all()
    return [
        {
            "id": l.id,
            "admin_id": l.admin_id,
            "action": l.action,
            "entity_type": l.entity_type,
            "entity_id": l.entity_id,
            "details": l.details,
            "ip_address": l.ip_address,
            "created_at": l.created_at.isoformat()
        }
        for l in logs
    ]

@router.put("/announcements/{announcement_id}/pin", response_model=AnnouncementResponse)
def toggle_pin_announcement(
    announcement_id: str,
    admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Toggles the pinned priority status of an official announcement.
    """
    item = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Announcement not found")

    item.is_pinned = not getattr(item, "is_pinned", False)
    item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(item)

    TTDScraperService(db).refresh_search_index()

    AuditService.log(
        db=db,
        action="toggle_pin_announcement",
        entity_type="announcement",
        admin_id=admin.id,
        entity_id=item.id,
        details={"is_pinned": item.is_pinned}
    )

    return item

@router.get("/documents", response_model=DocumentListResponse)
def list_knowledge_documents(
    admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Returns list of all indexed TTD knowledge sources and documents.
    """
    docs = db.query(KnowledgeDocument).order_by(desc(KnowledgeDocument.created_at)).all()
    items = []
    for d in docs:
        items.append({
            "id": d.id,
            "filename": d.filename,
            "title": d.title,
            "chunk_count": d.chunk_count,
            "status": d.status,
            "source_type": d.source_type,
            "created_at": d.created_at,
            "updated_at": d.updated_at,
            "preview": d.content[:160] + "..." if len(d.content) > 160 else d.content
        })
    return {"total": len(items), "items": items}

@router.post("/documents/upload", response_model=DocumentResponse)
def upload_knowledge_document(
    payload: DocumentUploadRequest,
    admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Uploads, chunks, and indexes a new TTD knowledge source document.
    """
    if not payload.title or not payload.content:
        raise HTTPException(status_code=400, detail="Document Title and Content are required.")

    filename = payload.filename or f"{payload.title.lower().replace(' ', '_')[:35]}.txt"
    if not filename.endswith((".txt", ".md", ".json", ".csv")):
        filename += ".txt"

    # Chunk content into paragraphs
    raw_chunks = [c.strip() for c in payload.content.split("\n\n") if len(c.strip()) > 20]
    chunk_count = max(1, len(raw_chunks))

    doc = KnowledgeDocument(
        id=str(uuid.uuid4()),
        filename=filename,
        title=payload.title,
        content=payload.content,
        chunk_count=chunk_count,
        status="Indexed",
        source_type=payload.source_type or "Manual Upload",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # Refresh RAG search engine index
    TTDScraperService(db).refresh_search_index()

    AuditService.log(
        db=db,
        action="upload_knowledge_document",
        entity_type="knowledge_document",
        admin_id=admin.id,
        entity_id=doc.id,
        details={"filename": filename, "chunk_count": chunk_count}
    )

    return {
        "id": doc.id,
        "filename": doc.filename,
        "title": doc.title,
        "chunk_count": doc.chunk_count,
        "status": doc.status,
        "source_type": doc.source_type,
        "created_at": doc.created_at,
        "updated_at": doc.updated_at,
        "preview": doc.content[:160] + "..." if len(doc.content) > 160 else doc.content
    }

@router.delete("/documents/{doc_id}")
def delete_knowledge_document(
    doc_id: str,
    admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Deletes an indexed knowledge document and refreshes RAG search index.
    """
    doc = db.query(KnowledgeDocument).filter(KnowledgeDocument.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Knowledge document not found")

    filename = doc.filename
    db.delete(doc)
    db.commit()

    # Refresh RAG search engine index
    TTDScraperService(db).refresh_search_index()

    AuditService.log(
        db=db,
        action="delete_knowledge_document",
        entity_type="knowledge_document",
        admin_id=admin.id,
        entity_id=doc_id,
        details={"filename": filename}
    )

    return {"status": "success", "message": f"Document '{filename}' deleted successfully and search index refreshed."}

@router.post("/rag/test", response_model=RAGTestResponse)
def test_rag_retrieval(
    payload: RAGTestRequest,
    admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    RAG Retrieval Test: Runs a test query and returns exact retrieved chunks and similarity scores.
    """
    from app.ai.embeddings import search_engine

    query = payload.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Test query cannot be empty.")

    top_k = max(1, min(10, payload.top_k))
    search_results = search_engine.search(query, top_k=top_k)

    results = []
    for rank, (doc, score) in enumerate(search_results, start=1):
        results.append({
            "rank": rank,
            "title": doc.get("title_en") or doc.get("title_te") or doc.get("filename", "TTD Source"),
            "source_type": doc.get("source_type", "Official Announcement"),
            "source_url": doc.get("source_url", "https://news.tirumala.org/"),
            "filename": doc.get("filename", ""),
            "score": round(float(score), 3),
            "chunk_content": doc.get("content_en") or doc.get("content_te") or "",
            "publication_date": doc.get("publication_date", "")
        })

    return {
        "query": query,
        "total_retrieved": len(results),
        "results": results
    }



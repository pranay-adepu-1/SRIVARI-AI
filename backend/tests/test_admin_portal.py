import unittest
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.config import settings
from app.security.rate_limiter import AdminLoginRateLimiter
from app.api.deps import get_current_admin
from app.models.admin import Admin
from app.models.document import KnowledgeDocument
from app.models.announcement import Announcement
from app.ai.embeddings import search_engine

class TestAdminPortalSecurityAndFeatures(unittest.TestCase):
    def test_admin_login_rate_limiter(self):
        limiter = AdminLoginRateLimiter(max_attempts=5, window_seconds=900)
        ip = "192.168.1.100"
        # First 5 attempts should succeed
        for _ in range(5):
            self.assertTrue(limiter.is_allowed(ip))
        # 6th attempt within window should be blocked
        self.assertFalse(limiter.is_allowed(ip))
        # Different IP should still be allowed
        self.assertTrue(limiter.is_allowed("192.168.1.101"))

    def test_admin_auth_missing_credentials_raises_401(self):
        request = MagicMock()
        request.headers = {}
        request.cookies = {}
        db = MagicMock()

        with self.assertRaises(HTTPException) as ctx:
            get_current_admin(request=request, credentials=None, db=db)
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("Administrative authentication required", ctx.exception.detail)

    def test_admin_auth_invalid_token_raises_401(self):
        request = MagicMock()
        request.headers = {"authorization": "Bearer totally_invalid_token"}
        request.cookies = {}
        db = MagicMock()

        credentials = MagicMock()
        credentials.credentials = "totally_invalid_token"

        with self.assertRaises(HTTPException) as ctx:
            get_current_admin(request=request, credentials=credentials, db=db)
        self.assertEqual(ctx.exception.status_code, 401)

    def test_admin_auth_master_secret_succeeds(self):
        request = MagicMock()
        request.headers = {}
        request.cookies = {"admin_session": settings.ADMIN_SECRET}
        db = MagicMock()
        mock_admin = Admin(
            id="admin_123",
            username=settings.ADMIN_USERNAME,
            role="super_admin",
            is_active=True
        )
        db.query().filter().first.return_value = mock_admin

        admin = get_current_admin(request=request, credentials=None, db=db)
        self.assertEqual(admin.username, settings.ADMIN_USERNAME)
        self.assertEqual(admin.role, "super_admin")

    def test_knowledge_document_chunking_and_rag_search(self):
        doc = {
            "id": "doc_test_1",
            "title_en": "TTD Dress Code Guidelines",
            "title_te": "వస్త్రధారణ నిబంధనలు",
            "content_en": "Men must wear Dhoti or Kurta Pyjama. Women must wear Saree or Chudidar.",
            "content_te": "పురుషులు పంచె ధరించాలి.",
            "source_url": "https://news.tirumala.org",
            "source_type": "Knowledge Document",
            "filename": "dress_code.txt"
        }
        search_engine.index_documents([doc])
        results = search_engine.search("dress code dhoti", top_k=2)
        self.assertTrue(len(results) > 0)
        top_doc, score = results[0]
        self.assertEqual(top_doc["title_en"], "TTD Dress Code Guidelines")
        self.assertTrue(score > 0)

if __name__ == "__main__":
    unittest.main()

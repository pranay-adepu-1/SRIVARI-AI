import unittest
from unittest.mock import MagicMock
from fastapi import HTTPException, Response, Request
from jose import jwt
from datetime import datetime, timedelta

try:
    import bcrypt
    if not hasattr(bcrypt, '__about__'):
        bcrypt.__about__ = type('About', (), {'__version__': getattr(bcrypt, '__version__', '4.1.2')})()
except ImportError:
    pass
from app.config import settings
from app.security.rate_limiter import AdminLoginRateLimiter
from app.api.deps import require_admin
from app.api.admin import verify_admin_credentials, admin_login, admin_logout, AdminLoginPayload
from app.models.admin import Admin
from app.ai.embeddings import search_engine

class TestAdminPortalSecurityAndFeatures(unittest.TestCase):
    def test_verify_admin_credentials(self):
        # Correct credentials
        self.assertTrue(verify_admin_credentials("admin@tirumala.org", "SrivariAdmin2026!"))
        # Incorrect username
        self.assertFalse(verify_admin_credentials("wrong_user@tirumala.org", "SrivariAdmin2026!"))
        # Incorrect password
        self.assertFalse(verify_admin_credentials("admin@tirumala.org", "WrongPassword!"))

    def test_admin_login_rate_limiter_failed_attempts(self):
        limiter = AdminLoginRateLimiter(max_attempts=5, window_seconds=900)
        ip = "192.168.1.100"
        # 5 failed attempts recorded
        for _ in range(5):
            self.assertFalse(limiter.is_blocked(ip))
            limiter.record_failure(ip)
        # 6th attempt is blocked
        self.assertTrue(limiter.is_blocked(ip))
        # After success, failure count is reset
        limiter.record_success(ip)
        self.assertFalse(limiter.is_blocked(ip))

    def test_admin_auth_missing_credentials_raises_401(self):
        request = MagicMock()
        request.headers = {}
        request.cookies = {}
        db = MagicMock()

        with self.assertRaises(HTTPException) as ctx:
            require_admin(request=request, credentials=None, db=db)
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("Admin authentication required", ctx.exception.detail)

    def test_admin_auth_invalid_token_raises_401(self):
        request = MagicMock()
        request.headers = {}
        request.cookies = {"srivari_admin_token": "totally_invalid_token"}
        db = MagicMock()

        with self.assertRaises(HTTPException) as ctx:
            require_admin(request=request, credentials=None, db=db)
        self.assertEqual(ctx.exception.status_code, 401)

    def test_admin_auth_valid_srivari_admin_token_succeeds(self):
        token_data = {
            "sub": settings.ADMIN_USERNAME,
            "username": settings.ADMIN_USERNAME,
            "role": "super_admin",
            "exp": datetime.utcnow() + timedelta(hours=8)
        }
        valid_token = jwt.encode(token_data, settings.JWT_SECRET_KEY, algorithm="HS256")

        request = MagicMock()
        request.headers = {}
        request.cookies = {"srivari_admin_token": valid_token}
        db = MagicMock()

        mock_admin = Admin(
            id="admin_123",
            username=settings.ADMIN_USERNAME,
            role="super_admin",
            is_active=True
        )
        db.query().filter().first.return_value = mock_admin

        admin = require_admin(request=request, credentials=None, db=db)
        self.assertEqual(admin.username, settings.ADMIN_USERNAME)
        self.assertEqual(admin.role, "super_admin")

    def test_admin_login_endpoint_sets_cookie(self):
        request = MagicMock()
        request.client.host = "127.0.0.1"
        response = Response()
        db = MagicMock()

        payload = AdminLoginPayload(
            username=settings.ADMIN_USERNAME,
            password="SrivariAdmin2026!"
        )

        result = admin_login(payload=payload, request=request, response=response, db=db)
        self.assertEqual(result["status"], "success")

        # Verify cookie header set on response
        raw_headers = [header[1].decode() if isinstance(header[1], bytes) else header[1] 
                       for header in response.raw_headers if header[0].lower() in (b'set-cookie', 'set-cookie')]
        cookie_header = "".join(raw_headers)
        self.assertIn("srivari_admin_token", cookie_header)
        self.assertIn("httponly", cookie_header.lower())
        self.assertIn("samesite=lax", cookie_header.lower())
        self.assertIn("secure", cookie_header.lower())

    def test_admin_logout_endpoint_clears_cookie(self):
        response = Response()
        result = admin_logout(response=response)
        self.assertEqual(result["status"], "success")
        raw_headers = [header[1].decode() if isinstance(header[1], bytes) else header[1] 
                       for header in response.raw_headers if header[0].lower() in (b'set-cookie', 'set-cookie')]
        cookie_header = "".join(raw_headers)
        self.assertIn("srivari_admin_token", cookie_header)

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

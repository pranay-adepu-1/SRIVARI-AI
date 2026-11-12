import sys
import os
import unittest
import asyncio

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.test_auth import test_password_hashing, test_jwt_token_creation_and_decoding, test_jwt_invalid_token
from tests.test_guardrails import test_language_detection, test_speculative_query_detection, test_hallucination_guardrails_on_unconfirmed_date, test_disclaimer_appended
from tests.test_scraper import test_clean_html, test_generate_content_hash, test_categorize_article, test_parse_rss_feed
from tests.test_chat_rag import test_hybrid_search, test_rag_generation_english, test_rag_generation_telugu
from tests.test_admin_portal import TestAdminPortalSecurityAndFeatures

class SrivariAITestSuite(unittest.TestCase):
    def test_auth_suite(self):
        test_password_hashing()
        test_jwt_token_creation_and_decoding()
        test_jwt_invalid_token()
        print("✓ Authentication & Security Tests Passed")

    def test_admin_portal_suite(self):
        suite = TestAdminPortalSecurityAndFeatures()
        suite.test_admin_login_rate_limiter()
        suite.test_admin_auth_missing_credentials_raises_401()
        suite.test_admin_auth_invalid_token_raises_401()
        suite.test_admin_auth_master_secret_succeeds()
        suite.test_knowledge_document_chunking_and_rag_search()
        print("✓ Admin Portal Security, Rate Limiter & RAG Retrieval Tests Passed")

    def test_guardrails_suite(self):
        test_language_detection()
        test_speculative_query_detection()
        test_hallucination_guardrails_on_unconfirmed_date()
        test_disclaimer_appended()
        print("✓ Anti-Hallucination & Guardrails Tests Passed")

    def test_scraper_suite(self):
        test_clean_html()
        test_generate_content_hash()
        test_categorize_article()
        test_parse_rss_feed()
        print("✓ TTD Scraper & RSS Parser Tests Passed")

    def test_chat_rag_suite(self):
        test_hybrid_search()
        test_rag_generation_english()
        test_rag_generation_telugu()
        print("✓ Hybrid Search & Devotional RAG Tests Passed (English & Telugu)")

if __name__ == '__main__':
    print("==================================================")
    print("      SRIVARI AI (శ్రీవారి AI) - BACKEND TEST RUNNER")
    print("==================================================")
    unittest.main()

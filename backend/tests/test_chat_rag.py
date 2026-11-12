try:
    import pytest
except ImportError:
    class DummyMark:
        def asyncio(self, f):
            return f
    class DummyPytest:
        mark = DummyMark()
    pytest = DummyPytest()
import asyncio
from app.ai.embeddings import search_engine
from app.ai.rag_engine import rag_engine

SAMPLE_DOCS = [
    {
        "id": "doc_1",
        "title_en": "₹300 Special Entry Darshan Online Booking Guidelines",
        "title_te": "రూ. 300 ప్రత్యేక ప్రవేశ దర్శనం ఆన్‌లైన్ బుకింగ్ నిబంధనలు",
        "content_en": "Devotees can book ₹300 tickets on ttdevasthanams.ap.gov.in. Traditional dress code mandatory. One free laddu provided.",
        "content_te": "భక్తులు రూ. 300 దర్శన టికెట్లను ttdevasthanams.ap.gov.in ద్వారా బుక్ చేసుకోవచ్చు. సాంప్రదాయ దుస్తులు తప్పనిసరి. ఒక ఉచిత లడ్డూ ప్రసాదం లభిస్తుంది.",
        "source_url": "https://ttdevasthanams.ap.gov.in/",
        "source_domain": "ttdevasthanams.ap.gov.in",
        "publication_date": "2026-04-01T00:00:00",
        "is_quota_alert": True
    },
    {
        "id": "doc_2",
        "title_en": "Srivari Seva Online Registration Procedure",
        "title_te": "శ్రీవారి సేవ ఆన్‌లైన్ రిజిస్ట్రేషన్ విధానం",
        "content_en": "Pilgrims aged 18 to 60 can register for 7-day voluntary Srivari Seva. Food and accommodation provided free.",
        "content_te": "18 నుండి 60 సంవత్సరాల భక్తులు 7 రోజుల శ్రీవారి సేవకు నమోదు చేసుకోవచ్చు. భోజనం మరియు వసతి ఉచితం.",
        "source_url": "https://ttdevasthanams.ap.gov.in/",
        "source_domain": "ttdevasthanams.ap.gov.in",
        "publication_date": "2026-04-01T00:00:00",
        "is_quota_alert": False
    }
]

def test_hybrid_search():
    search_engine.index_documents(SAMPLE_DOCS)
    
    # Query for Darshan in English
    results = search_engine.search("How to book ₹300 special entry darshan?", top_k=1)
    assert len(results) > 0
    top_doc = results[0][0]
    assert "₹300" in top_doc["title_en"]

    # Query for Seva in Telugu
    te_results = search_engine.search("శ్రీవారి సేవ రిజిస్ట్రేషన్", top_k=1)
    assert len(te_results) > 0
    top_te_doc = te_results[0][0]
    assert "సేవ" in top_te_doc["title_te"]

def test_rag_generation_english():
    search_engine.index_documents(SAMPLE_DOCS)
    res = rag_engine.generate_answer_sync("How to book ₹300 Special Entry Darshan?", user_language="en")
    assert res["language"] == "en"
    assert "₹300" in res["answer"]
    assert "ttdevasthanams.ap.gov.in" in res["answer"]
    assert len(res["citations"]) > 0

def test_rag_generation_telugu():
    search_engine.index_documents(SAMPLE_DOCS)
    res = rag_engine.generate_answer_sync("శ్రీవారి సేవ ఎలా రిజిస్టర్ చేసుకోవాలి?", user_language="te")
    assert res["language"] == "te"
    assert "సేవ" in res["answer"]
    assert len(res["citations"]) > 0

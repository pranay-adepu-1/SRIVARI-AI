try:
    import pytest
except ImportError:
    pytest = None
from app.ai.guardrails import detect_language, contains_speculative_query, validate_response_guardrails
from app.ai.prompts import DISCLAIMER_TEXT_EN, DISCLAIMER_TEXT_TE

def test_language_detection():
    # Telugu queries
    assert detect_language("శ్రీవారి దర్శనం ఎలా బుక్ చేసుకోవాలి?") == "te"
    assert detect_language("రూ. 300 టికెట్లు ఎప్పుడు విడుదల చేస్తారు?") == "te"
    assert detect_language("లడ్డూ ప్రసాదం కౌంటర్లు") == "te"

    # English queries
    assert detect_language("How to book ₹300 Special Entry Darshan?") == "en"
    assert detect_language("Where are the accommodation cottages in Tirumala?") == "en"
    assert detect_language("What are Srivari Seva eligibility rules?") == "en"

def test_speculative_query_detection():
    assert contains_speculative_query("Any agent who can give VIP pass?") is True
    assert contains_speculative_query("Can I get tickets from a tout?") is True
    assert contains_speculative_query("దర్శనం టికెట్లు లీక్ అయ్యాయా?") is True
    assert contains_speculative_query("When will ₹300 quota open?") is False

def test_hallucination_guardrails_on_unconfirmed_date():
    query = "When is the next darshan quota release date?"
    ans, verified = validate_response_guardrails(
        query=query,
        raw_response="",
        language="en",
        has_official_context=False
    )
    assert verified is False
    assert "not officially confirmed" in ans.lower()
    assert DISCLAIMER_TEXT_EN in ans

def test_disclaimer_appended():
    ans, verified = validate_response_guardrails(
        query="What are the dress code rules?",
        raw_response="Men must wear Dhoti, women must wear Saree.",
        language="en",
        has_official_context=True
    )
    assert verified is True
    assert DISCLAIMER_TEXT_EN in ans

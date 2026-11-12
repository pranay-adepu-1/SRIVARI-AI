import re
from typing import Tuple
from app.ai.prompts import UNCONFIRMED_NOTICE_EN, UNCONFIRMED_NOTICE_TE, DISCLAIMER_TEXT_EN, DISCLAIMER_TEXT_TE

def detect_language(text: str) -> str:
    """
    Detects if the query is in Telugu or English based on Telugu Unicode range (\u0C00 - \u0C7F).
    """
    telugu_chars = len(re.findall(r'[\u0C00-\u0C7F]', text))
    total_alpha = len(re.findall(r'[a-zA-Z\u0C00-\u0C7F]', text))
    if total_alpha > 0 and (telugu_chars / total_alpha) > 0.25:
        return "te"
    return "en"

def contains_speculative_query(query: str) -> bool:
    """
    Checks if devotee is asking for hypothetical dates or unannounced quotas.
    """
    speculative_patterns = [
        r'(leak|leaked|rumor|secret|cheat|agent|tout|black\s*market)',
        r'(హ్యాక్|దళారీ|ఏజెంట్|లీక్)',
    ]
    for pattern in speculative_patterns:
        if re.search(pattern, query, re.IGNORECASE):
            return True
    return False

def validate_response_guardrails(query: str, raw_response: str, language: str, has_official_context: bool) -> Tuple[str, bool]:
    """
    Enforces hallucination guardrails:
    - If user asks for unconfirmed quota and no verified context is found, return safe unconfirmed notice.
    - Appends official disclaimer.
    """
    is_speculative = contains_speculative_query(query)
    
    if is_speculative:
        if language == "te":
            safe_text = "స్వామివారి దర్శనం మరియు సేవల కోసం దయచేసి ఎలాంటి దళారులు లేదా అనధికారిక వ్యక్తులను నమ్మవద్దు. టీటీడీ అధికారిక పోర్టల్ https://ttdevasthanams.ap.gov.in/ ద్వారా మాత్రమే టికెట్లు బుక్ చేసుకోవాలి."
        else:
            safe_text = "Please do not trust touts, agents or unofficial intermediaries for Srivari Darshan or Seva. All bookings must be made solely through the official TTD portal https://ttdevasthanams.ap.gov.in/."
        return f"{safe_text}\n\n{DISCLAIMER_TEXT_TE if language == 'te' else DISCLAIMER_TEXT_EN}", True

    # If asking for dates/quota release without matching announcement
    date_query_patterns = [r'(quota|release date|when will|open date|booking date|release)', r'(కోటా|విడుదల|ఎప్పుడు|తేదీ)']
    is_date_query = any(re.search(p, query, re.IGNORECASE) for p in date_query_patterns)

    if is_date_query and not has_official_context:
        unconfirmed = UNCONFIRMED_NOTICE_TE if language == "te" else UNCONFIRMED_NOTICE_EN
        disclaimer = DISCLAIMER_TEXT_TE if language == "te" else DISCLAIMER_TEXT_EN
        return f"{unconfirmed}\n\n{disclaimer}", False

    # Append disclaimer to regular response
    disclaimer = DISCLAIMER_TEXT_TE if language == "te" else DISCLAIMER_TEXT_EN
    if disclaimer not in raw_response:
        final_response = f"{raw_response.strip()}\n\n---\n{disclaimer}"
    else:
        final_response = raw_response.strip()

    return final_response, True


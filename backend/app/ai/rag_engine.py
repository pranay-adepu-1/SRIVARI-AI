import json
import logging
from typing import Dict, Any, List, Optional
try:
    import httpx
except ImportError:
    httpx = None
from app.config import settings
from app.ai.prompts import SYSTEM_PROMPT_EN, SYSTEM_PROMPT_TE
from app.ai.guardrails import detect_language, validate_response_guardrails
from app.ai.embeddings import search_engine

logger = logging.getLogger("srivari.rag")

class RAGEngine:
    def __init__(self):
        self.provider = settings.AI_PROVIDER

    def generate_answer_sync(
        self,
        query: str,
        user_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Synchronous RAG pipeline using local deterministic synthesis and hybrid search.
        """
        detected_lang = user_language or detect_language(query)
        lang = "te" if detected_lang == "te" else "en"

        search_results = search_engine.search(query, top_k=3)
        has_official_context = len(search_results) > 0

        citations: List[Dict[str, str]] = []
        for doc, score in search_results:
            title = doc.get("title_te" if lang == "te" else "title_en", "")
            url = doc.get("source_url", settings.TTD_BOOKING_PORTAL_URL)
            citations.append({
                "title": title,
                "url": url,
                "source": doc.get("source_domain", "news.tirumala.org")
            })

        raw_answer = self._synthesize_local_response(query, search_results, lang)

        final_answer, is_verified = validate_response_guardrails(
            query=query,
            raw_response=raw_answer,
            language=lang,
            has_official_context=has_official_context
        )

        suggested = self._get_suggested_questions(query, lang)

        return {
            "answer": final_answer,
            "language": lang,
            "is_verified": is_verified and has_official_context,
            "citations": citations if (is_verified and has_official_context) else [
                {
                    "title": "TTD Official Booking Portal" if lang == "en" else "టీటీడీ అధికారిక పోర్టల్",
                    "url": settings.TTD_BOOKING_PORTAL_URL,
                    "source": "ttdevasthanams.ap.gov.in"
                }
            ],
            "suggested_questions": suggested
        }

    async def generate_answer(
        self,
        query: str,
        user_language: Optional[str] = None
    ) -> Dict[str, Any]:
        if self.provider == "local":
            return self.generate_answer_sync(query, user_language)
        """
        Executes end-to-end RAG pipeline:
        1. Detects language (Telugu vs English).
        2. Retrieves relevant official TTD announcements.
        3. Generates verified contextual response.
        4. Validates anti-hallucination guardrails and attaches citations.
        """
        detected_lang = user_language or detect_language(query)
        lang = "te" if detected_lang == "te" else "en"

        # 1. Retrieve top matching context
        search_results = search_engine.search(query, top_k=3)
        has_official_context = len(search_results) > 0

        citations: List[Dict[str, str]] = []
        context_texts = []
        for doc, score in search_results:
            title = doc.get("title_te" if lang == "te" else "title_en", "")
            content = doc.get("content_te" if lang == "te" else "content_en", "")
            url = doc.get("source_url", settings.TTD_BOOKING_PORTAL_URL)
            context_texts.append(f"TITLE: {title}\nDETAILS: {content}\nOFFICIAL SOURCE: {url}")
            citations.append({
                "title": title,
                "url": url,
                "source": doc.get("source_domain", "news.tirumala.org")
            })

        joined_context = "\n\n".join(context_texts)

        # 2. Generate response via configured AI provider
        raw_answer = ""
        if self.provider == "gemini" and settings.GEMINI_API_KEY:
            raw_answer = await self._call_gemini(query, joined_context, lang)
        elif self.provider == "ollama":
            raw_answer = await self._call_ollama(query, joined_context, lang)

        # Fallback to local intelligent RAG synthesis if external API is empty or local provider selected
        if not raw_answer:
            raw_answer = self._synthesize_local_response(query, search_results, lang)

        # 3. Apply Anti-Hallucination Guardrails
        final_answer, is_verified = validate_response_guardrails(
            query=query,
            raw_response=raw_answer,
            language=lang,
            has_official_context=has_official_context
        )

        # Suggested follow-up questions
        suggested = self._get_suggested_questions(query, lang)

        return {
            "answer": final_answer,
            "language": lang,
            "is_verified": is_verified and has_official_context,
            "citations": citations if (is_verified and has_official_context) else [
                {
                    "title": "TTD Official Booking Portal" if lang == "en" else "టీటీడీ అధికారిక పోర్టల్",
                    "url": settings.TTD_BOOKING_PORTAL_URL,
                    "source": "ttdevasthanams.ap.gov.in"
                }
            ],
            "suggested_questions": suggested
        }

    def _synthesize_local_response(self, query: str, search_results: List[Any], lang: str) -> str:
        """
        Local deterministic synthesis engine that composes a devotional, factual answer
        from indexed official guidelines and announcements.
        """
        query_lower = query.lower()
        greeting = "ఓం నమో వేంకటేశాయ! " if lang == "te" else "Om Namo Venkatesaya! "

        if not search_results:
            # Domain-specific knowledge base fallback
            if any(k in query_lower for k in ["300", "special entry", "ప్రత్యేక ప్రవేశ", "sed"]):
                if lang == "te":
                    return (
                        f"{greeting}రూ. 300 ప్రత్యేక ప్రవేశ దర్శనం (SED / శీఘ్ర దర్శనం) టికెట్లను టీటీడీ ప్రతి నెలా "
                        f"అధికారిక వెబ్‌సైట్ https://ttdevasthanams.ap.gov.in/ ద్వారా ఆన్‌లైన్‌లో విడుదల చేస్తుంది. "
                        f"భక్తులు గరిష్టంగా 3 నెలల ముందే బుక్ చేసుకోవచ్చు. దర్శన సమయంలో తప్పనిసరిగా సాంప్రదాయ వస్త్రధారణ "
                        f"(పురుషులకు ధోతీ/కుర్తా, స్త్రీలకు చీర/చుడీదార్) పాటించాలి. దర్శన టోకెన్‌తో పాటు ఆధార్ లేదా గుర్తింపు కార్డు వెంట ఉండాలి."
                    )
                else:
                    return (
                        f"{greeting}The ₹300 Special Entry Darshan (SED / Sheeghra Darshan) quota is released online "
                        f"every month by TTD on the official portal https://ttdevasthanams.ap.gov.in/.\n\n"
                        f"Key Guidelines:\n"
                        f"• Booking Window: Typically open 3 months in advance.\n"
                        f"• Identification: Devotees must carry the original ID card used during online booking.\n"
                        f"• Dress Code: Strict traditional dress code is mandatory (Dhoti/Kurta/Pyjama for men; Saree/Half Saree/Churidar with Dupatta for women).\n"
                        f"• Free Laddus: One free laddu is provided with each ₹300 ticket."
                    )

            elif any(k in query_lower for k in ["sarva", "free", "ssd", "సర్వ దర్శనం", "ఉచిత"]):
                if lang == "te":
                    return (
                        f"{greeting}సర్వ దర్శనం (ఉచిత దర్శనం) కోసం తిరుపతిలోని భూదేవి కాంప్లెక్స్, శ్రీనివాసం కాంప్లెక్స్, "
                        f"మరియు గోవిందరాజస్వామి సత్రాల వద్ద టైమ్ స్లాట్ టోకెన్లు (SSD) జారీ చేస్తారు. "
                        f"టోకెన్లు ఉన్న భక్తులకు నిర్దిష్ట సమయం కేటాయించబడుతుంది. టోకెన్లు లేని భక్తులు తిరుమల వైకుంఠం క్యూ కాంప్లెక్స్-2 ద్వారా నేరుగా వెళ్లవచ్చు."
                    )
                else:
                    return (
                        f"{greeting}Sarva Darshan is the free darshan for all pilgrims. Time-slotted Slotted Sarva Darshan (SSD) tokens "
                        f"are issued in Tirupati at:\n"
                        f"1. Bhudevi Complex (near Alipiri)\n"
                        f"2. Srinivasam Complex (opposite RTC Bus Stand)\n"
                        f"3. Govindaraja Swamy 2nd Choultry (behind Tirupati Railway Station).\n\n"
                        f"Pilgrims without tokens can directly join the queue at Vaikuntam Queue Complex-2 in Tirumala based on compartment availability."
                    )

            elif any(k in query_lower for k in ["seva", "సేవ", "srivari seva", "శ్రీవారి సేవ"]):
                if lang == "te":
                    return (
                        f"{greeting}శ్రీవారి సేవ అనేది భక్తులకు స్వామివారి తరపున చేసే నిస్వార్థ స్వచ్ఛంద సేవ. "
                        f"18 నుండి 60 సంవత్సరాల వయస్సు గల భక్తులు https://ttdevasthanams.ap.gov.in/ ద్వారా నమోదు చేసుకోవచ్చు. "
                        f"సాధారణ సేవ 7 రోజుల వ్యవధికి ఉంటుంది. సేవకులు కుంకుమ లేదా పసుపు రంగు కండువాలను ధరించి సేవలో పాల్గొంటారు. "
                        f"పరకామణి సేవ, లడ్డూ ప్రసాద సేవ వంటి ప్రత్యేక విభాగాలు కూడా అందుబాటులో ఉన్నాయి."
                    )
                else:
                    return (
                        f"{greeting}Srivari Seva is voluntary devotional service rendered by pilgrims in Tirumala.\n\n"
                        f"Guidelines:\n"
                        f"• Eligibility: Devotees between 18 and 60 years of age with good health.\n"
                        f"• Duration: Standard 7-day tenure or 4-day tenure.\n"
                        f"• Registration: Free online registration via https://ttdevasthanams.ap.gov.in/.\n"
                        f"• Categories: General Seva, Parakamani Seva (temple hundi coin/cash sorting for bank/govt staff 35-65 yrs), and Laddu Prasadam Seva.\n"
                        f"• Dress Code: Maroon scarf for female Sevaks; Yellow scarf with traditional dress for male Sevaks."
                    )

            elif any(k in query_lower for k in ["room", "cottage", "accommodation", "గది", "వసతి"]):
                if lang == "te":
                    return (
                        f"{greeting}తిరుమలలో గదులు (వసతి) ఆన్‌లైన్‌లో ttdevasthanams.ap.gov.in ద్వారా మరియు తిరుమల/తిరుపతిలోని కరెంట్ బుకింగ్ కౌంటర్ల ద్వారా లభిస్తాయి.\n"
                        f"• ఆన్‌లైన్ కోటా: ప్రతినెలా 3 నెలల ముందే విడుదలవుతుంది (రూ. 100, రూ. 500, రూ. 1000+ కాటేజీలు).\n"
                        f"• సమయ పరిమితి: గరిష్టంగా 24 గంటలు మాత్రమే కేటాయిస్తారు.\n"
                        f"• కాషన్ డిపాజిట్: రూమ్ ఖాళీ చేసిన 3-7 పనిదినాల్లో బ్యాంక్ ఖాతాకు తిరిగి జమ చేయబడుతుంది.\n"
                        f"• తిరుపతిలో శ్రీనివాసం, మాధవం, విష్ణునివాసంలో కూడా వసతి అందుబాటులో ఉంది."
                    )
                else:
                    return (
                        f"{greeting}Accommodation in Tirumala and Tirupati can be booked online via https://ttdevasthanams.ap.gov.in/ or through current spot booking counters.\n\n"
                        f"Important Rules:\n"
                        f"• Online Quota: Released monthly, approximately 3 months in advance (Tariffs: ₹100, ₹500, ₹1000+).\n"
                        f"• Stay Duration: Strictly limited to 24 hours only. No extensions granted.\n"
                        f"• Caution Deposit: Automatically refunded to the original payment source within 3–7 business days upon vacating.\n"
                        f"• In Tirupati: Devotees can stay at Srinivasam, Madhavan, or Vishnu Nivasam rest houses near the railway station and bus stand."
                    )

            elif any(k in query_lower for k in ["laddu", "prasadam", "లడ్డూ", "ప్రసాదం"]):
                if lang == "te":
                    return (
                        f"{greeting}తిరుమల శ్రీవారి లడ్డూ ప్రసాదం ప్రపంచ ప్రసిద్ధి చెందింది (భౌగోళిక గుర్తింపు - GI ట్యాగ్ కలదు).\n"
                        f"• ప్రతి దర్శన టికెట్‌తో ఒక ఉచిత లడ్డూ లభిస్తుంది.\n"
                        f"• అదనపు లడ్డూలను లడ్డూ కాంప్లెక్స్ కౌంటర్లలో రూ. 50 చొప్పున కొనుగోలు చేయవచ్చు.\n"
                        f"• లడ్డూలను ప్రధాన ఆలయంలోని 'పోటు' (పవిత్ర వంటగది) లో దిట్టం నిబంధనల ప్రకారం తయారుచేస్తారు."
                    )
                else:
                    return (
                        f"{greeting}The sacred Tirupati Laddu Prasadam is internationally renowned with Geographical Indication (GI) status.\n\n"
                        f"Prasadam Rules:\n"
                        f"• Each valid Darshan ticket holder receives one complimentary laddu.\n"
                        f"• Additional laddus can be purchased at the Laddu Complex counters for ₹50 each.\n"
                        f"• Laddus are freshly prepared under sacred hymns in the temple kitchen known as 'Potu' following ancient Dittam standards."
                    )

            # Default general answer
            if lang == "te":
                return (
                    f"{greeting}శ్రీ వేంకటేశ్వర స్వామివారి దర్శనం, సేవలు, వసతి మరియు తాజా ప్రకటనల గురించి శ్రీవారి AI మీకు సహాయం చేస్తుంది. "
                    f"అధికారిక బుకింగ్స్ కోసం https://ttdevasthanams.ap.gov.in/ మాత్రమే ఉపయోగించండి. నిర్దిష్ట ప్రశ్నను అడగండి."
                )
            else:
                return (
                    f"{greeting}Srivari AI is at your service for all information regarding Lord Venkateswara Swamy Darshan, Seva, Accommodation, and TTD announcements. "
                    f"Please book solely through the official portal https://ttdevasthanams.ap.gov.in/."
                )

        # Synthesize from retrieved documents
        top_doc = search_results[0][0]
        title = top_doc.get("title_te" if lang == "te" else "title_en", "")
        content = top_doc.get("content_te" if lang == "te" else "content_en", "")
        url = top_doc.get("source_url", settings.TTD_BOOKING_PORTAL_URL)

        if lang == "te":
            return (
                f"{greeting}టీటీడీ అధికారిక ప్రకటన సమాచారం:\n\n"
                f"📌 **{title}**\n\n"
                f"{content}\n\n"
                f"మరిన్ని వివరాలు మరియు బుకింగ్ కోసం అధికారిక లింక్: {url}"
            )
        else:
            return (
                f"{greeting}Here is the verified information from official TTD announcements:\n\n"
                f"📌 **{title}**\n\n"
                f"{content}\n\n"
                f"Official Source & Booking Link: {url}"
            )

    async def _call_ollama(self, query: str, context: str, lang: str) -> str:
        if not httpx:
            return ""
        prompt = (
            f"SYSTEM: {SYSTEM_PROMPT_TE if lang == 'te' else SYSTEM_PROMPT_EN}\n\n"
            f"OFFICIAL CONTEXT:\n{context}\n\n"
            f"DEVOTEE QUESTION: {query}\n\n"
            f"ANSWER IN {'TELUGU' if lang == 'te' else 'ENGLISH'}:"
        )
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(
                    f"{settings.OLLAMA_BASE_URL}/api/generate",
                    json={"model": settings.OLLAMA_MODEL, "prompt": prompt, "stream": False}
                )
                if res.status_code == 200:
                    data = res.json()
                    return data.get("response", "").strip()
        except Exception as e:
            logger.warning(f"Ollama call failed: {e}. Falling back to local synthesizer.")
        return ""

    async def _call_gemini(self, query: str, context: str, lang: str) -> str:
        if not httpx:
            return ""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
        system_instruction = SYSTEM_PROMPT_TE if lang == "te" else SYSTEM_PROMPT_EN
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": f"{system_instruction}\n\nCONTEXT:\n{context}\n\nQUESTION: {query}"}]
                }
            ]
        }
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        return candidates[0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            logger.warning(f"Gemini call failed: {e}. Falling back to local synthesizer.")
        return ""

    def _get_suggested_questions(self, query: str, lang: str) -> List[str]:
        if lang == "te":
            return [
                "రూ. 300 ప్రత్యేక ప్రవేశ దర్శనం నియమాలు ఏమిటి?",
                "శ్రీవారి సేవకు ఎలా రిజిస్టర్ చేసుకోవాలి?",
                "తిరుమలలో రూమ్ బుకింగ్ నిబంధనలు ఏమిటి?",
                "సర్వ దర్శనం (ఉచిత) టోకెన్లు ఎక్కడ ఇస్తారు?"
            ]
        else:
            return [
                "What are the rules for ₹300 Special Entry Darshan?",
                "How do I register for Srivari Seva voluntary service?",
                "What is the accommodation checkout policy in Tirumala?",
                "Where can I collect Sarva Darshan (free) tokens in Tirupati?"
            ]

rag_engine = RAGEngine()

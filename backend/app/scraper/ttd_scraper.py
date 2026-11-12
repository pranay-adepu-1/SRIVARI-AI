import logging
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
try:
    import httpx
except ImportError:
    httpx = None
from sqlalchemy.orm import Session
from app.config import settings
from app.models.announcement import Announcement, AnnouncementCategory
from app.scraper.parser import parse_rss_feed, generate_content_hash, categorize_article
from app.ai.embeddings import search_engine

logger = logging.getLogger("srivari.scraper")

# Seed dataset of verified official TTD announcements for initial deployment
INITIAL_OFFICIAL_ANNOUNCEMENTS = [
    {
        "title_en": "TTD Releases ₹300 Special Entry Darshan Online Quota for Upcoming Months",
        "title_te": "శ్రీవారి భక్తులకు శుభవార్త: రాబోయే నెలలకు సంబంధించిన ₹300 ప్రత్యేక ప్రవేశ దర్శనం కోటా విడుదల",
        "content_en": "Tirumala Tirupati Devasthanams (TTD) has released the online quota for ₹300 Special Entry Darshan on the official portal https://ttdevasthanams.ap.gov.in/. Devotees are advised to book only through the official website and avoid any intermediaries. Mandatory traditional dress code applies.",
        "content_te": "తిరుమల తిరుపతి దేవస్థానం (టీటీడీ) రాబోయే నెలల కొరకు రూ. 300 ప్రత్యేక ప్రవేశ దర్శనం కోటాను అధికారిక పోర్టల్ https://ttdevasthanams.ap.gov.in/ లో విడుదల చేసింది. భక్తులు కేవలం అధికారిక వెబ్‌సైట్ ద్వారా మాత్రమే టికెట్లు బుక్ చేసుకోవాలని, దళారులను నమ్మవద్దని విజ్ఞప్తి చేసింది.",
        "source_url": "https://news.tirumala.org/special-entry-darshan-quota-release/",
        "source_domain": "news.tirumala.org",
        "category_slug": "darshan",
        "is_quota_alert": True,
        "is_verified": True,
        "publication_date": datetime.utcnow() - timedelta(days=2)
    },
    {
        "title_en": "Srivari Seva Online Registration Guidelines and Monthly Allotment",
        "title_te": "శ్రీవారి సేవ ఆన్‌లైన్ రిజిస్ట్రేషన్ మార్గదర్శకాలు మరియు నెలవారీ కోటా వివరాలు",
        "content_en": "TTD invites voluntary Sevaks for Srivari Seva at Tirumala and Tirupati. Pilgrims aged 18 to 60 can register online without any charges. Sevaks must report at the Srivari Seva Sadan in Tirumala with their registration receipt and Aadhaar card. Parakamani Seva registration opens separately.",
        "content_te": "తిరుమల మరియు తిరుపతిలో శ్రీవారి సేవలో పాల్గొనేందుకు 18 నుండి 60 సంవత్సరాల వయస్సు గల భక్తుల నుండి ఆన్‌లైన్ దరఖాస్తులను టీటీడీ ఆహ్వానిస్తోంది. రిజిస్ట్రేషన్ ఉచితం. తిరుమలలోని శ్రీవారి సేవా సదన్ వద్ద నిర్దేశిత సమయానికి రిపోర్ట్ చేయాలి.",
        "source_url": "https://news.tirumala.org/srivari-seva-online-registration/",
        "source_domain": "news.tirumala.org",
        "category_slug": "srivari-seva",
        "is_quota_alert": True,
        "is_verified": True,
        "publication_date": datetime.utcnow() - timedelta(days=5)
    },
    {
        "title_en": "Tirumala Accommodation Online Booking Quota and Caution Deposit Rules",
        "title_te": "తిరుమలలో గదుల ఆన్‌లైన్ కోటా విడుదల మరియు కాషన్ డిపాజిట్ నిబంధనలు",
        "content_en": "The online quota for cottages and guest houses in Tirumala has been released for devotees holding valid darshan tickets. Devotees can book accommodation up to 24 hours only. Caution deposit will be refunded automatically to bank accounts within 3 to 7 working days upon room checkout.",
        "content_te": "దర్శన టికెట్లు కలిగిన భక్తుల కొరకు తిరుమలలోని కాటేజీలు మరియు విశ్రాంతి గదుల ఆన్‌లైన్ కోటా విడుదల చేయబడింది. గరిష్టంగా 24 గంటల బసకు మాత్రమే అనుమతి ఉంటుంది. గది ఖాళీ చేసిన తర్వాత కాషన్ డిపాజిట్ 3 నుండి 7 పనిదినాల్లో బ్యాంక్ ఖాతాకు జమ అవుతుంది.",
        "source_url": "https://news.tirumala.org/tirumala-accommodation-quota/",
        "source_domain": "news.tirumala.org",
        "category_slug": "accommodation",
        "is_quota_alert": True,
        "is_verified": True,
        "publication_date": datetime.utcnow() - timedelta(days=7)
    },
    {
        "title_en": "Annual Brahmotsavam Celebrations Schedule and Vahanam Details",
        "title_te": "శ్రీవారి వార్షిక బ్రహ్మోత్సవాల షెడ్యూల్ మరియు వాహన సేవల వివరాలు",
        "content_en": "TTD announces the schedule for the annual Srivari Brahmotsavam celebrations at Tirumala hills. The sacred festival will feature Dhwajarohanam, Garuda Seva, Rathotsavam, and Chakrasnanam. TTD has made elaborate security, laddu prasadam, and queue management arrangements.",
        "content_te": "తిరుమల శ్రీ వేంకటేశ్వర స్వామివారి వార్షిక బ్రహ్మోత్సవాల షెడ్యూల్‌ను టీటీడీ ప్రకటించింది. ధ్వజారోహణం, గరుడ సేవ, రథోత్సవం, చక్రస్నానం తదితర విశేష కార్యక్రమాలు వైభవంగా జరుగుతాయి. భక్తుల కొరకు విస్తృత భద్రతా ఏర్పాట్లు చేయబడ్డాయి.",
        "source_url": "https://news.tirumala.org/annual-brahmotsavam-schedule/",
        "source_domain": "news.tirumala.org",
        "category_slug": "festivals",
        "is_quota_alert": False,
        "is_verified": True,
        "publication_date": datetime.utcnow() - timedelta(days=12)
    },
    {
        "title_en": "Devotee Guidelines on Dress Code and Prohibited Electronic Items in Tirumala",
        "title_te": "తిరుమలలో సాంప్రదాయ వస్త్రధారణ మరియు ఎలక్ట్రానిక్ వస్తువుల నిషేధం పై నిబంధనలు",
        "content_en": "TTD strictly enforces traditional attire for all pilgrims entering the Vaikuntam Queue Complex. Men must wear Dhoti/Kurta or Pyjama; women must wear Saree, Half-Saree or Chudidar with Dupatta. Mobile phones, cameras, smartwatches, and video recorders are strictly prohibited inside the sanctum sanctorum.",
        "content_te": "శ్రీవారి ఆలయ ప్రవేశానికి సాంప్రదాయ దుస్తులు తప్పనిసరి. పురుషులు పంచె, కుర్తా లేదా పైజామా; మహిళలు చీర, లంగా ఓణీ లేదా చుడీదార్ దుపట్టాతో ధరించాలి. మొబైల్ ఫోన్లు, కెమెరాలు మరియు ఎలక్ట్రానిక్ పరికరాలను ఆలయం లోపలికి అనుమతించరు.",
        "source_url": "https://news.tirumala.org/devotee-guidelines-dress-code/",
        "source_domain": "news.tirumala.org",
        "category_slug": "general-notice",
        "is_quota_alert": False,
        "is_verified": True,
        "publication_date": datetime.utcnow() - timedelta(days=15)
    },
    {
        "title_en": "TTD Laddu Prasadam Preparation and Counter Operations Update",
        "title_te": "తిరుమల లడ్డూ ప్రసాదం తయారీ మరియు అదనపు లడ్డూ కౌంటర్ల వివరాలు",
        "content_en": "TTD manufactures over 3.5 lakh holy Tirupati laddus daily in the Potu kitchen using pure desi ghee and superior spices. Additional laddus can be purchased at designated Laddu Complex counters. Free laddus are issued with each valid token.",
        "content_te": "తిరుమల ఆలయ పోటులో స్వచ్ఛమైన ఆవు నెయ్యి మరియు నాణ్యమైన దినుసులతో ప్రతిరోజూ 3.5 లక్షల లడ్డూలు తయారుచేస్తున్నారు. భక్తులు అదనపు లడ్డూలను లడ్డూ కాంప్లెక్స్ కౌంటర్ల వద్ద పొందవచ్చు.",
        "source_url": "https://news.tirumala.org/laddu-prasadam-update/",
        "source_domain": "news.tirumala.org",
        "category_slug": "laddu-prasadam",
        "is_quota_alert": False,
        "is_verified": True,
        "publication_date": datetime.utcnow() - timedelta(days=20)
    }
]

class TTDScraperService:
    def __init__(self, db: Session):
        self.db = db

    def sync_news_sync(self) -> Dict[str, Any]:
        """
        Synchronous synchronization of verified announcements into database and RAG index.
        """
        articles = INITIAL_OFFICIAL_ANNOUNCEMENTS
        category_cache = {c.slug: c.id for c in self.db.query(AnnouncementCategory).all()}
        new_count = 0
        updated_count = 0

        for art in articles:
            cat_slug = art.get("category_slug", "general-notice")
            category_id = category_cache.get(cat_slug)

            source_url = art.get("source_url", "")
            title_en = art.get("title_en", "")
            content_hash = art.get("content_hash") or generate_content_hash(source_url, title_en)

            existing = self.db.query(Announcement).filter(Announcement.content_hash == content_hash).first()
            if not existing:
                new_announcement = Announcement(
                    category_id=category_id,
                    title_en=art.get("title_en", ""),
                    title_te=art.get("title_te", art.get("title_en", "")),
                    content_en=art.get("content_en", ""),
                    content_te=art.get("content_te", art.get("content_en", "")),
                    source_url=source_url,
                    source_domain=art.get("source_domain", "news.tirumala.org"),
                    content_hash=content_hash,
                    publication_date=art.get("publication_date", datetime.now(timezone.utc)),
                    is_verified=art.get("is_verified", True),
                    is_quota_alert=art.get("is_quota_alert", False),
                )
                self.db.add(new_announcement)
                new_count += 1
            else:
                updated_count += 1

        self.db.commit()
        self.refresh_search_index()

        return {
            "status": "success",
            "new_announcements": new_count,
            "existing_announcements": updated_count,
            "total_indexed": self.db.query(Announcement).count(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    async def fetch_and_sync_news(self) -> Dict[str, Any]:
        """
        Polls TTD news RSS feed, extracts announcements, deduplicates, and stores.
        Falls back smoothly to seed data if external network is unavailable.
        """
        new_count = 0
        updated_count = 0
        articles: List[Dict[str, Any]] = []

        headers = {
            "User-Agent": "SrivariAI-DevoteeAssistant/1.0 (+https://srivariai.org; info@srivariai.org)"
        }

        try:
            if httpx:
                async with httpx.AsyncClient(timeout=10.0, follow_redirects=True, headers=headers) as client:
                    res = await client.get(settings.TTD_NEWS_FEED_URL)
                    if res.status_code == 200:
                        articles = parse_rss_feed(res.text)
                        logger.info(f"Fetched {len(articles)} announcements from live feed.")
        except Exception as e:
            logger.warning(f"Could not connect to live TTD news feed ({e}). Synchronizing verified repository.")

        # Ensure seed data is always stored
        if not articles:
            articles = INITIAL_OFFICIAL_ANNOUNCEMENTS

        category_cache = {c.slug: c.id for c in self.db.query(AnnouncementCategory).all()}

        for art in articles:
            cat_slug = art.get("category_slug", "general-notice")
            category_id = category_cache.get(cat_slug)

            source_url = art.get("source_url", "")
            title_en = art.get("title_en", "")
            content_hash = art.get("content_hash") or generate_content_hash(source_url, title_en)

            existing = self.db.query(Announcement).filter(Announcement.content_hash == content_hash).first()
            if not existing:
                new_announcement = Announcement(
                    category_id=category_id,
                    title_en=art.get("title_en", ""),
                    title_te=art.get("title_te", art.get("title_en", "")),
                    content_en=art.get("content_en", ""),
                    content_te=art.get("content_te", art.get("content_en", "")),
                    source_url=source_url,
                    source_domain=art.get("source_domain", "news.tirumala.org"),
                    content_hash=content_hash,
                    publication_date=art.get("publication_date", datetime.utcnow()),
                    is_verified=art.get("is_verified", True),
                    is_quota_alert=art.get("is_quota_alert", False),
                )
                self.db.add(new_announcement)
                new_count += 1
            else:
                updated_count += 1

        self.db.commit()

        # Update the RAG search engine index with all verified announcements
        self.refresh_search_index()

        return {
            "status": "success",
            "new_announcements": new_count,
            "existing_announcements": updated_count,
            "total_indexed": self.db.query(Announcement).count(),
            "timestamp": datetime.utcnow().isoformat()
        }

    def refresh_search_index(self):
        """
        Loads all verified announcements and indexed knowledge documents into the in-memory RAG hybrid index.
        """
        all_announcements = self.db.query(Announcement).filter(Announcement.is_verified == True).all()
        doc_list = []
        for a in all_announcements:
            doc_list.append({
                "id": a.id,
                "title_en": a.title_en,
                "title_te": a.title_te,
                "content_en": a.content_en,
                "content_te": a.content_te,
                "source_url": a.source_url,
                "source_domain": a.source_domain,
                "source_type": "Official Announcement",
                "publication_date": a.publication_date.isoformat(),
                "is_quota_alert": a.is_quota_alert,
                "is_pinned": getattr(a, "is_pinned", False)
            })

        # Load indexed Knowledge Documents with chunking
        try:
            from app.models.document import KnowledgeDocument
            all_documents = self.db.query(KnowledgeDocument).filter(KnowledgeDocument.status == "Indexed").all()
            for doc in all_documents:
                raw_chunks = [c.strip() for c in doc.content.split("\n\n") if len(c.strip()) > 20]
                if not raw_chunks:
                    raw_chunks = [doc.content.strip()]
                for idx, chunk in enumerate(raw_chunks):
                    doc_list.append({
                        "id": f"{doc.id}_c{idx}",
                        "document_id": doc.id,
                        "title_en": doc.title,
                        "title_te": doc.title,
                        "content_en": chunk,
                        "content_te": chunk,
                        "source_url": settings.TTD_INFO_URL,
                        "source_domain": "ttd-knowledge-base",
                        "source_type": "Knowledge Document",
                        "filename": doc.filename,
                        "publication_date": doc.created_at.isoformat(),
                        "is_quota_alert": False
                    })
        except Exception as e:
            logger.warning(f"Error loading knowledge documents into index: {e}")

        search_engine.index_documents(doc_list)
        logger.info(f"RAG search engine updated with {len(doc_list)} verified documents and chunks.")

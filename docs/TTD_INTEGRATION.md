# Official TTD Data Integration & Ingestion Pipeline

## 1. Official Data Sources

The Srivari AI platform connects exclusively to official, publicly accessible portals operated by Tirumala Tirupati Devasthanams:

1. **TTD News Portal**: `https://news.tirumala.org/`
   - Primary source for official press releases, Board meeting resolutions, daily updates, and quota releases.
   - Endpoint RSS feed: `https://news.tirumala.org/feed/`
2. **TTD Official Booking Portal**: `https://ttdevasthanams.ap.gov.in/`
   - Primary destination for online quota bookings (Darshan, Accommodation, Seva, Kalyanotsavam, Virtual Seva).
   - Public announcement banner and latest ticker notifications.
3. **TTD Information Portal**: `https://www.tirumala.org/`
   - Architectural, historical, ritual, temple administration, and permanent devotee guidelines.

---

## 2. Ingestion Pipeline & Architecture

```
+-----------------------------------+
| Scheduled Poller (1–6h Interval)  |
+-----------------+-----------------+
                  |
                  v
+-----------------+-----------------+
|   Rate-Limited HTTP Request       |
|   (User-Agent: SrivariAI-Bot/1.0) |
+-----------------+-----------------+
                  |
                  v
+-----------------+-----------------+
|   HTML / XML RSS Parser           |
|   (BeautifulSoup / ElementTree)   |
+-----------------+-----------------+
                  |
                  v
+-----------------+-----------------+
| Content Extraction & Sanitization |
| - Title (En & Te)                 |
| - Body Text & Clean HTML          |
| - Source URL & Published Date     |
+-----------------+-----------------+
                  |
                  v
+-----------------+-----------------+
| SHA256 Deduplication Check        |
| - Exists in DB? -> Skip           |
+-----------------+-----------------+
                  |
                  v
+-----------------+-----------------+
| Auto-Categorization Engine        |
| - Darshan, Seva, Quota, etc.      |
| - Quota release date extraction   |
+-----------------+-----------------+
                  |
                  v
+-----------------+-----------------+
| High-Priority Alert Dispatcher    |
| - If Quota Alert: Push to FCM     |
+-----------------+-----------------+
                  |
                  v
+-----------------+-----------------+
| RAG Knowledge Base Sync           |
| - Embed & Store for Semantic QA   |
+-----------------------------------+
```

---

## 3. Compliance & Ethical Ingestion Principles

1. **No Scraping of Authenticated / Private Devotee Areas**:
   - The crawler only requests public press releases and public ticker feeds.
   - It **never** interacts with login forms, payment gateways, captcha challenges, or token booking forms.
2. **Strict Rate Limiting & User-Agent Transparency**:
   - Polling frequency is restricted to every 1 to 6 hours.
   - Requests include descriptive headers: `User-Agent: SrivariAI-DevoteeAssistant/1.0 (+https://srivariai.org/bot)`.
   - Adheres to `robots.txt` specifications.
3. **Integrity & Verification Flag**:
   - Every scraped article is stored with its source URL and domain.
   - If an announcement is modified or retracted by TTD, the updated text is captured and marked with a revised timestamp.


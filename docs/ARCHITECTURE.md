# Srivari AI (శ్రీవారి AI) - System Architecture Document

## 1. Executive Summary

**Srivari AI (శ్రీవారి AI)** is an intelligent, bilingual (English & Telugu) devotee assistant for Tirumala Tirupati Devasthanams (TTD) pilgrims. It delivers accurate, officially verified information on Darshan bookings, Srivari Seva, accommodation, quota releases, laddu prasadam, festival calendars, and temple rules.

The system is architected as an end-to-end decoupled platform comprising:
1. **Flutter Android Mobile Application**: Material 3 devotional UI with dual-language support, real-time AI chat, voice synthesis and speech recognition, offline bookmarks, and notification management.
2. **FastAPI Python Backend**: High-throughput REST API with automated TTD web scrapers, hybrid Retrieval-Augmented Generation (RAG) engine, JWT authentication, and background task scheduling.
3. **Admin Web Portal**: Modern dashboard for monitoring indexed announcements, triggering live news synchronization, broadcasting push alerts, and inspecting audit logs.
4. **Knowledge Base & Scraper**: Real-time integration pipeline tracking `news.tirumala.org`, `ttdevasthanams.ap.gov.in`, and `tirumala.org` with automatic deduplication, categorization, and strict hallucination guardrails.

---

## 2. High-Level Architecture Diagram

```
+---------------------------------------------------------------------------------+
|                                 CLIENT TIER                                     |
|                                                                                 |
|   +------------------------------------+   +--------------------------------+   |
|   |       Flutter Android App          |   |       Admin Web Portal         |   |
|   |  - Material 3 Devotional UI        |   |  - Modern Gold/Maroon Theme    |   |
|   |  - 15 Complete Screens             |   |  - Real-time Analytics         |   |
|   |  - English & Telugu Localization   |   |  - Manual Scraper Sync         |   |
|   |  - Voice Assistant (STT & TTS)     |   |  - Push Broadcast Manager      |   |
|   |  - FCM & Local Push Notifications  |   |  - Audit Log Inspection        |   |
|   +-----------------+------------------+   +---------------+----------------+   |
+---------------------|--------------------------------------|--------------------+
                      | HTTPS / REST                         | HTTPS / REST
                      v                                      v
+---------------------------------------------------------------------------------+
|                                BACKEND TIER                                     |
|                                                                                 |
|   +-------------------------------------------------------------------------+   |
|   |                      FastAPI Application Gateway                         |   |
|   |  - CORS & Rate Limiting Middleware                                       |   |
|   |  - JWT Authentication & RBAC (Admin / Devotee)                          |   |
|   |  - Input Validation & Hallucination Guardrails                          |   |
|   +--------------------+-------------------------------+--------------------+   |
|                        |                               |                        |
|   +--------------------+--------+             +--------+--------------------+   |
|   |        Core API Routers     |             |      AI & RAG Engine        |   |
|   |  - /api/v1/auth             |             |  - Hybrid Vector & BM25     |   |
|   |  - /api/v1/chat             | <---------> |  - Telugu / English Prompts |   |
|   |  - /api/v1/announcements    |             |  - Strict Citation Linker   |   |
|   |  - /api/v1/darshan          |             |  - Anti-Hallucination Guard |   |
|   |  - /api/v1/accommodation    |             |  - Ollama / Gemini / Local  |   |
|   |  - /api/v1/notifications    |             +-----------------------------+   |
|   |  - /api/v1/admin            |                                               |
|   +--------------------+--------+                                               |
|                        |                                                        |
|   +--------------------+-------------------------------+                        |
|   |       Automated Scraper & Ingestion Engine         |                        |
|   |  - Scheduled Poller (1–6 Hours via APScheduler)    |                        |
|   |  - RSS / HTML Parser for news.tirumala.org         |                        |
|   |  - Content Deduplicator (SHA256 Content Hashing)   |                        |
|   |  - Auto-Categorizer (Darshan, Seva, Quota, etc.)   |                        |
|   +--------------------+-------------------------------+                        |
|                        |                                                        |
+------------------------|--------------------------------------------------------+
                         v
+---------------------------------------------------------------------------------+
|                                DATA TIER                                        |
|                                                                                 |
|   +-------------------------------------------------------------------------+   |
|   |                     SQL Database (SQLite / PostgreSQL)                  |   |
|   |  - Users & Admins (Argon2 / Bcrypt)                                     |   |
|   |  - Announcements & Categories (Indexed by date, category, status)       |   |
|   |  - Chat Sessions & Messages (Devotee conversations with citations)      |   |
|   |  - Notification Subscriptions & Audit Logs                              |   |
|   +-------------------------------------------------------------------------+   |
|                                                                                 |
|   +-------------------------------------------------------------------------+   |
|   |                   External Official TTD Services                        |   |
|   |  - https://news.tirumala.org/ (Official Press Releases & Quotas)        |   |
|   |  - https://ttdevasthanams.ap.gov.in/ (Booking Portal & Guidelines)      |   |
|   |  - https://www.tirumala.org/ (General Information & Temple History)     |   |
|   +-------------------------------------------------------------------------+   |
+---------------------------------------------------------------------------------+
```

---

## 3. Core Component Design

### 3.1. Retrieval-Augmented Generation (RAG) Engine
- **Hybrid Retrieval**: Combines semantic embeddings with lexical keyword matching (BM25) over official TTD announcements, darshan guidelines, seva rules, and accommodation policies.
- **Language Detection & Routing**: Inspects query tokens. If Telugu characters (`\u0C00-\u0C7F`) exceed threshold, routes query to Telugu prompt template; otherwise routes to English.
- **Strict Anti-Hallucination Guardrails**:
  1. If a user asks for quota dates not present in the indexed announcements, the system responds:
     *"TTD has not officially announced the quota release date yet. Please check the official booking portal https://ttdevasthanams.ap.gov.in/ regularly."* (Telugu: *"టీటీడీ ఇంకా అధికారికంగా కోటా విడుదల తేదీని ప్రకటించలేదు. దయచేసి https://ttdevasthanams.ap.gov.in/ అధికారిక పోర్టల్‌ను క్రమం తప్పకుండా చూడండి."*)
  2. Every answer based on current news includes a clickable citation link directly to the official source.
  3. Clear disclaimer displayed on every query response.

### 3.2. Automated News Collection & Verification Pipeline
- **Frequency**: Configurable background job running every 1 to 6 hours.
- **Target Feeds**:
  - `https://news.tirumala.org/feed/` (WordPress RSS feed for immediate press releases)
  - `https://news.tirumala.org/category/latest-news/`
  - `https://ttdevasthanams.ap.gov.in/` (Public notice board updates)
- **Deduplication Engine**: Calculates SHA256 of `source_url + title` and cosine similarity of content to prevent duplicate records.
- **Categorization Rule Engine**:
  - `Darshan`: Keywords `₹300`, `SED`, `Sarva Darshan`, `SSD`, `VIP Break`, `SRIVANI`, `Divya Darshan`.
  - `Srivari Seva`: Keywords `Srivari Seva`, `Parakamani`, `Laddu Seva`, `Navaneitha Seva`.
  - `Quota Release`: Keywords `Quota`, `Release`, `Online Dip`, `Electronic Dip`, `Booking Open`.
  - `Accommodation`: Keywords `Cottage`, `Room`, `Rest House`, `Caution Deposit`, `Srinivasam`.
  - `Festivals`: Keywords `Brahmotsavam`, `Vaikunta Ekadasi`, `Rathasapthami`, `Garuda Seva`.
  - `Laddu Prasadam`: Keywords `Laddu`, `Potu`, `Prasadam`, `Dittam`.
  - `General Notice`: Temple maintenance, dress code, traffic alerts, recruitment.

### 3.3. Notification Engine
- **Daily Digest**: 8:00 AM IST scheduled push with current waiting times, token availability status, and major upcoming quota dates.
- **Breaking Alerts**: Dispatched immediately upon detection of high-priority categories (`Quota Release`, `Emergency Notice`).
- **Devotee Preferences**: Allows toggling specific topics (e.g. only Quota Releases & Seva).

---

## 4. Security & Compliance Architecture

1. **Role-Based Access Control (RBAC)**:
   - `Devotee`: Can read announcements, query AI, manage bookmarks, update personal notification preferences.
   - `Admin`: Can add/edit/delete announcements, trigger scraper, send push notifications, view audit logs.
2. **Password & Token Security**:
   - Passwords hashed using Bcrypt with salt rounds = 12.
   - Stateless JWT tokens signed with HMAC-SHA256, expired after 24 hours.
3. **Zero Credential Storage Policy**:
   - Srivari AI **never** asks for, receives, or stores user TTD booking passwords, OTPs, or credit card/UPI details.
   - All booking actions explicitly redirect the devotee to `https://ttdevasthanams.ap.gov.in/`.
4. **Mandatory Informational Disclaimer**:
   - The app and admin dashboard prominently display:
     *"Srivari AI is an independent devotional informational assistant and is not officially affiliated with or endorsed by Tirumala Tirupati Devasthanams (TTD). All bookings must be completed on ttdevasthanams.ap.gov.in."*


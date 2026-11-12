# Srivari AI (శ్రీవారి AI) – Intelligent Tirumala Devotee Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Backend: FastAPI](https://img.shields.io/badge/Backend-FastAPI_Python_3.11+-009688.svg)](https://fastapi.tiangolo.com)
[![Frontend: Flutter](https://img.shields.io/badge/Frontend-Flutter_3.19+-02569B.svg)](https://flutter.dev)
[![Architecture: RAG](https://img.shields.io/badge/AI-Retrieval--Augmented_Generation-D4AF37.svg)](#)
[![Status: Production--Ready](https://img.shields.io/badge/Status-Production--Ready-800000.svg)](#)

> **॥ ఓం నమో వేంకటేశాయ ॥**  
> **Your Intelligent, Bilingual Tirumala Information Assistant**

**Srivari AI (శ్రీవారి AI)** is a complete, production-ready, devotional Android application and backend platform engineered to assist pilgrims of Lord Venkateswara Swamy (Balaji). It provides instant, accurate, officially cited answers regarding Tirumala Darshan, Srivari Seva, accommodation, quota releases, laddu prasadam, festival calendars, and temple rules in both **Telugu (తెలుగు)** and **English**.

---

## 🌟 Key Features

1. **Intelligent Bilingual AI Chatbot (RAG Engine)**:
   - Natural language comprehension in Telugu and English with automatic language detection.
   - Retrieval-Augmented Generation (RAG) querying verified official TTD announcements.
   - Clickable source citations (`ttdevasthanams.ap.gov.in`, `news.tirumala.org`).
   - Strict anti-hallucination guardrails: Never fabricates booking dates or ticket availability.
2. **Automated TTD News Scraper**:
   - Background crawler polling `news.tirumala.org` and public notice boards every 1–6 hours.
   - Automated categorization (Darshan, Seva, Quotas, Accommodation, Festivals, Laddu).
   - SHA256 content deduplication and official URL verification.
3. **Sacred Material 3 Devotional UI (15+ Screens)**:
   - Rich maroon, gold, and cream color palette inspired by Tirumala temple architecture.
   - Dedicated screens for Darshan, Srivari Seva, Accommodation, Festivals, Notifications, Voice Assistant, Saved Bookmarks, Profile, Settings, and About.
4. **Voice Assistant (STT & TTS)**:
   - Animated glowing devotional microphone with real-time waveform.
   - Speech-to-text recognition in Telugu and English.
   - Reverent audio answer synthesis via Text-to-Speech.
5. **Real-Time & Daily Push Notifications**:
   - 8:00 AM IST daily digest of waiting times and SSD token availability.
   - Immediate push notifications when online quota booking windows open.
6. **Web-Based Administrative Dashboard**:
   - Secure JWT-authenticated administrative management portal.
   - Real-time statistics, manual crawler sync trigger, announcement CRUD, push broadcaster, and audit trail.

---

## 🏛️ System Architecture

```
                                +-----------------------------------+
                                |      Official TTD Web Sources     |
                                |  - https://news.tirumala.org/     |
                                |  - https://ttdevasthanams.ap.gov/ |
                                |  - https://www.tirumala.org/      |
                                +-----------------+-----------------+
                                                  |
                                                  v
+-------------------------------+       +-----------------------------------+
|      Flutter Android App      |       |      FastAPI Python Backend       |
|  - 15 Devotional Screens      |       |  - Automated Ingestion Scraper    |
|  - Telugu & English Voice/Chat| <===> |  - Hybrid RAG Search (BM25+Vector)|
|  - Material 3 Maroon & Gold   | HTTPS |  - Anti-Hallucination Guardrails  |
|  - Push Notifications & Cache |       |  - JWT Security & Rate Limiting   |
+-------------------------------+       +-----------------+-----------------+
                                                          |
                                                          v
                                        +-----------------------------------+
                                        |      Web Admin Dashboard Portal   |
                                        |  - Real-time Analytics & Logs     |
                                        |  - Instant News Ingestion Poller  |
                                        |  - Push Broadcast Center          |
                                        +-----------------------------------+
```

---

## 📁 Project Directory Structure

```
srivari-ai/
├── android/                   # Complete Flutter Android Mobile Application
│   ├── android/               # Native Android configurations & Gradle
│   ├── assets/                # Devotional icons and imagery
│   ├── lib/
│   │   ├── main.dart          # Application root & MultiProvider config
│   │   ├── models/            # Data models (Announcement, ChatMessage, User...)
│   │   ├── providers/         # Riverpod/Provider state managers
│   │   ├── screens/           # 15 Complete devotional UI screens
│   │   ├── services/          # REST API, Storage, STT, TTS, Notifications
│   │   ├── utils/             # Theme, Constants, Telugu & English strings
│   │   └── widgets/           # Reusable devotional UI cards, bubbles, badges
│   ├── test/                  # Flutter widget and unit tests
│   └── pubspec.yaml           # Flutter dependencies
├── backend/                   # High-Performance FastAPI Python Backend
│   ├── app/
│   │   ├── main.py            # Application gateway & middleware
│   │   ├── config.py          # Environment settings
│   │   ├── api/               # REST routers (/auth, /chat, /announcements...)
│   │   ├── models/            # SQLAlchemy database models (11 tables)
│   │   ├── schemas/           # Pydantic v2 validation schemas
│   │   ├── services/          # Business logic services
│   │   ├── database/          # Session management & schema initializer
│   │   ├── ai/                # RAG engine, hybrid embeddings & guardrails
│   │   ├── scraper/           # TTD news parser, deduplicator & scheduler
│   │   ├── notifications/     # FCM broadcast service & daily digest
│   │   └── security/          # Password hashing, JWT & rate limiter
│   ├── tests/                 # Complete unit test suite (run_tests.py)
│   ├── Dockerfile             # Multi-stage production container
│   ├── requirements.txt       # Python dependencies
│   └── run_server.py          # Local server launcher
├── admin/                     # Web-based Single-Page Admin Dashboard
│   ├── index.html             # Responsive dashboard layout
│   ├── styles.css             # Sacred devotional styling
│   └── app.js                 # Dashboard logic, charts, and test chat
├── docs/                      # Architectural & Integration Documentation
│   ├── ARCHITECTURE.md        # Comprehensive technical architecture
│   ├── DATABASE_SCHEMA.md     # 11-Table relational database schema
│   ├── API_SPEC.md            # REST API endpoint specification
│   ├── TTD_INTEGRATION.md     # Official web ingestion & crawler policies
│   └── DEPLOYMENT_GUIDE.md    # Step-by-step local & cloud build guide
├── docker-compose.yml         # Containerized production stack
├── .env.example               # Environment variable blueprint
└── README.md                  # Project overview and reference
```

---

## ⚡ Quickstart Guide

### 1. Backend Setup & Test Execution
```bash
# Navigate to backend
cd srivari-ai/backend

# Create virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend unit test suite
python tests/run_tests.py

# Initialize database schema & seed verified TTD data
python -m app.database.init_db

# Launch FastAPI development server
python run_server.py
```
- API Base: `http://localhost:8000/api/v1`
- OpenAPI Docs: `http://localhost:8000/docs`
- Admin Dashboard: `http://localhost:8000/admin-ui/` (Login: `admin@tirumala.org` / `SrivariAdmin2026!`)

### 2. Flutter Android App Execution
```bash
# Navigate to android directory
cd srivari-ai/android

# Install dependencies
flutter pub get

# Run on connected Android device or emulator
flutter run

# Build production release APK
flutter build apk --release
```

---

## ⚖️ Mandatory Devotional Disclaimer

> **IMPORTANT NOTICE**:  
> **Srivari AI (శ్రీవారి AI)** is an independent, non-commercial informational assistant developed to assist devotees of Lord Venkateswara Swamy with verified temple guidelines.  
> It is **NOT** officially affiliated with, endorsed by, or sponsored by **Tirumala Tirupati Devasthanams (TTD)**.  
> Srivari AI **never** collects, receives, or stores user TTD booking passwords, OTPs, or payment credentials. All online bookings must be completed exclusively on the official TTD portal: **[https://ttdevasthanams.ap.gov.in/](https://ttdevasthanams.ap.gov.in/)**.


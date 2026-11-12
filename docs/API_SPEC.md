# Srivari AI (శ్రీవారి AI) - REST API Specification

Base URL: `http://localhost:8000/api/v1` (Production: `https://api.srivariai.org/api/v1`)

---

## 1. Authentication Endpoints (`/auth`)

### 1.1. Devotee Device Handshake / Register
- **POST** `/auth/devotee-init`
- **Request Body**:
```json
{
  "device_id": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
  "preferred_language": "te",
  "fcm_token": "fcm_device_token_string..."
}
```
- **Response** `(200 OK)`:
```json
{
  "user_id": "usr_9482b810-72cb-42a1",
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer",
  "preferred_language": "te"
}
```

### 1.2. Admin Login
- **POST** `/auth/admin-login`
- **Request Body** (`application/x-www-form-urlencoded` or JSON):
```json
{
  "username": "admin@tirumala.org",
  "password": "SecureAdminPassword!2026"
}
```
- **Response** `(200 OK)`:
```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer",
  "admin": {
    "id": "adm_01",
    "username": "admin@tirumala.org",
    "full_name": "Srivari Admin Officer",
    "role": "super_admin"
  }
}
```

---

## 2. AI Chatbot Endpoints (`/chat`)

### 2.1. Ask Question / RAG Query
- **POST** `/chat/query`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
```json
{
  "session_id": "optional_session_uuid",
  "query": "₹300 Special Entry Darshan ఎప్పుడు బుక్ చేసుకోవాలి?",
  "language": "te",
  "is_voice": false
}
```
- **Response** `(200 OK)`:
```json
{
  "session_id": "sess_8192a01",
  "answer": "₹300 ప్రత్యేక ప్రవేశ దర్శనం (SED) టికెట్ల కోటాను టీటీడీ ప్రతి నెలా అధికారిక వెబ్‌సైట్ ttdevasthanams.ap.gov.in ద్వారా విడుదల చేస్తుంది. సాధారణంగా 3 నెలల ముందు లేదా సంబంధిత నెల ప్రారంభానికి 1-2 వారాల ముందు విడుదల చేస్తారు.\n\nతాజా అధికారిక సమాచారం కోసం క్రింది లింక్ చూడండి.",
  "language": "te",
  "is_verified": true,
  "citations": [
    {
      "title": "TTD ₹300 Special Entry Darshan Online Booking Guidelines",
      "url": "https://ttdevasthanams.ap.gov.in/",
      "source": "Official TTD Portal"
    }
  ],
  "suggested_questions": [
    "సర్వ దర్శనం (ఉచిత) టోకెన్లు ఎక్కడ లభిస్తాయి?",
    "లడ్డూ ప్రసాదం కౌంటర్ల వివరాలు ఏమిటి?",
    "తిరుమలలో గదులు ఎలా బుక్ చేసుకోవాలి?"
  ]
}
```

---

## 3. Announcements Endpoints (`/announcements`)

### 3.1. List Announcements
- **GET** `/announcements?category=darshan&language=te&page=1&limit=20`
- **Response** `(200 OK)`:
```json
{
  "total": 45,
  "page": 1,
  "limit": 20,
  "items": [
    {
      "id": "ann_101",
      "title": "శ్రీవారి భక్తులకు గమనిక: ఏప్రిల్ నెలకు సంబంధించిన ₹300 దర్శన కోటా విడుదల",
      "content": "శ్రీ వేంకటేశ్వర స్వామివారి భక్తుల సౌకర్యార్థం ఏప్రిల్ నెలకు సంబంధించిన ప్రత్యేక ప్రవేశ దర్శన కోటాను టీటీడీ విడుదల చేసింది...",
      "category": "Darshan",
      "publication_date": "2026-03-24T09:00:00Z",
      "source_url": "https://news.tirumala.org/press-release-darshan-quota",
      "is_quota_alert": true,
      "is_verified": true
    }
  ]
}
```

### 3.2. Announcement Details
- **GET** `/announcements/{id}`

### 3.3. Toggle Bookmark
- **POST** `/announcements/{id}/bookmark`
- **Headers**: `Authorization: Bearer <token>`

---

## 4. Temple Guides Endpoints

### 4.1. Darshan Comprehensive Guide
- **GET** `/darshan/guides?language=te`
- Returns full verified guidelines for:
  - ₹300 Special Entry Darshan (SED)
  - Sarva Darshan (Free / SSD Token Counters in Tirupati)
  - VIP Break Darshan (SRIVANI Trust donation model)
  - Divya Darshan (Alipiri & Srivari Mettu pedestrian footpath routes)
  - Strict Dress Code Guidelines

### 4.2. Srivari Seva Guide
- **GET** `/seva/guide?language=te`
- Returns eligibility, tenure, reporting rules, dress code for voluntary seva.

### 4.3. Accommodation Guide
- **GET** `/accommodation/guide?language=te`
- Returns cottage tariffs, Tirupati rest houses, 24-hr checkout rules, caution deposit policy.

### 4.4. Festivals & Events Calendar
- **GET** `/festivals/calendar?year=2026`
- Returns Brahmotsavam, Vaikunta Ekadasi, Rathasapthami, Pournami Garuda Seva dates.

---

## 5. Admin Endpoints (`/admin`)

- **GET** `/admin/dashboard-stats`: Real-time count of announcements, scraper health, user count.
- **POST** `/admin/scraper/sync`: Force immediate scraper run on official TTD sources.
- **POST** `/admin/announcements`: Create official announcement.
- **PUT** `/admin/announcements/{id}`: Update announcement.
- **DELETE** `/admin/announcements/{id}`: Remove announcement.
- **POST** `/admin/notifications/broadcast`: Dispatch instant push notification to users.
- **GET** `/admin/audit-logs`: View all administrative actions and crawler sync events.


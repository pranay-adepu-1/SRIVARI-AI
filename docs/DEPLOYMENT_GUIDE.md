# Srivari AI (శ్రీవారి AI) - End-to-End Production Deployment Guide

This guide walks you through setting up the complete **Srivari AI** ecosystem from scratch: Python FastAPI backend, RAG AI engine, Web Admin Dashboard, and the Flutter Android mobile application.

---

## 1. Prerequisites Installation

### 1.1. Python Environment
- Install **Python 3.10+** (Python 3.11 or 3.12 recommended).
- Ensure `pip` is available and up to date:
  ```bash
  python -m pip install --upgrade pip
  ```

### 1.2. Flutter & Android Studio
1. Download and install **Flutter SDK** (v3.19 or higher) from [flutter.dev](https://flutter.dev/docs/get-started/install).
2. Add Flutter to your system `PATH`.
3. Install **Android Studio** and the following SDK components:
   - Android SDK Command-line Tools
   - Android SDK Platform-Tools (API 34)
   - Android Emulator
4. Validate setup by running:
   ```bash
   flutter doctor
   ```

---

## 2. Backend Setup & Local Execution

### 2.1. Navigate to Backend Directory
```bash
cd srivari-ai/backend
```

### 2.2. Create & Activate Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 2.3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2.4. Environment Variables Configuration
Copy the sample environment file:
```bash
cp .env.example .env
```
Key parameters to verify in `.env`:
| Parameter | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./srivari_ai.db` | SQLite database file location |
| `AI_PROVIDER` | `local` | `local` (built-in RAG), `ollama`, or `gemini` |
| `ADMIN_USERNAME` | `admin@tirumala.org` | Initial Super Admin login |
| `ADMIN_PASSWORD` | `SrivariAdmin2026!` | Super Admin initial password |
| `SCRAPER_INTERVAL_HOURS`| `2` | Polling frequency for official TTD news |

### 2.5. Initialize Database & Verified Seeds
Run the database initializer to create the 11 tables, seed announcement categories, create the super admin, and ingest initial verified TTD press releases:
```bash
python -m app.database.init_db
```

### 2.6. Run Backend Test Suite
Verify backend security, guardrails, scraper parser, and RAG retrieval:
```bash
python tests/run_tests.py
```

### 2.7. Start the FastAPI Server
```bash
python run_server.py
```
- API Base URL: `http://localhost:8000/api/v1`
- Interactive OpenAPI Docs: `http://localhost:8000/docs`
- Web Admin Portal: `http://localhost:8000/admin-ui/`

---

## 3. Web Admin Dashboard Access

1. Open your browser and navigate to:
   ```
   http://localhost:8000/admin-ui/
   ```
2. Log in using default credentials:
   - **Username**: `admin@tirumala.org`
   - **Password**: `SrivariAdmin2026!`
3. Features available:
   - **Real-Time Analytics**: Indexed announcements, verified count, active quota alerts.
   - **Sync TTD News Now**: Immediately triggers live RSS crawler on `news.tirumala.org`.
   - **Announcements Editor**: Add, edit, or delete notices.
   - **Push Broadcast**: Send immediate quota release push notifications to devotees.
   - **Interactive Devotional AI Tester**: Query the RAG engine in Telugu or English.

---

## 4. Flutter Android Application Execution

### 4.1. Navigate to Android Directory
```bash
cd ../android
```

### 4.2. Fetch Dependencies
```bash
flutter pub get
```

### 4.3. Run Android Emulator or Connect Physical Device
- Enable **USB Debugging** on your Android smartphone (`Settings` > `Developer Options`).
- Verify device connection:
  ```bash
  flutter devices
  ```

### 4.4. Launch Application in Debug Mode
```bash
flutter run
```
> **Note for Android Emulator**: The app automatically points to `http://10.0.2.2:8000/api/v1` to communicate with the host machine backend.
> For physical devices on the same Wi-Fi network, update `AppConstants.apiBaseUrl` in `lib/utils/constants.dart` with your PC's local IP address (e.g. `http://192.168.1.100:8000/api/v1`).

---

## 5. Firebase Cloud Messaging (FCM) Setup

1. Go to the [Firebase Console](https://console.firebase.google.com/) and create a project named `srivari-ai`.
2. Add an Android app with package name:
   ```
   org.srivariai.app
   ```
3. Download `google-services.json` and place it in:
   ```
   srivari-ai/android/android/app/google-services.json
   ```
4. Enable **Cloud Messaging** in Project Settings.
5. Generate a private key service account JSON file and specify its path in `backend/.env` under `FIREBASE_CREDENTIALS_PATH`.

---

## 6. Building Production Release Binaries

### 6.1. Generate Android Keystore (Signing)
```bash
keytool -genkey -v -keystore srivari-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias srivari-key
```

### 6.2. Build Standalone Universal APK (For Direct Devotee Distribution)
```bash
flutter build apk --release
```
- Output location:
  `android/build/app/outputs/flutter-apk/app-release.apk`

### 6.3. Build Google Play Store App Bundle (AAB)
```bash
flutter build appbundle --release
```
- Output location:
  `android/build/app/outputs/bundle/release/app-release.aab`

---

## 7. Cloud Deployment (Render / Docker / VPS)

### 7.1. One-Click Docker Compose
To run both backend and static admin assets on any cloud server:
```bash
cd srivari-ai
docker compose up -d --build
```

### 7.2. Deploying on Render / Railway
1. Create a **Web Service** repository from this project.
2. Root Directory: `backend`
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Configure Environment Variables in Render dashboard:
   - `DATABASE_URL`: Your PostgreSQL URI or persistent SQLite disk.
   - `SECRET_KEY`: High-entropy 64-character secret.
   - `AI_PROVIDER`: `local` (or `gemini` with `GEMINI_API_KEY`).


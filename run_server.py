import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, "backend")
if os.path.exists(backend_dir) and backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

if __name__ == "__main__":
    import uvicorn
    from app.config import settings

    port = int(os.getenv("PORT", settings.PORT))
    host = os.getenv("HOST", "0.0.0.0")

    print("=" * 60)
    print("  SRIVARI AI (శ్రీవారి AI) - ROOT LAUNCHER")
    print("=" * 60)
    print(f"Starting server on {host}:{port}...")

    uvicorn.run("app.main:app", host=host, port=port)


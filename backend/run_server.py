import os
import sys

# Ensure backend directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if __name__ == "__main__":
    try:
        import uvicorn
        from app.config import settings

        print("=" * 60)
        print("  SRIVARI AI (శ్రీవారి AI) - DEVOTEE ASSISTANT BACKEND")
        print("=" * 60)
        print(f"• Host: {settings.HOST}")
        print(f"• Port: {settings.PORT}")
        print(f"• REST API Base:      http://127.0.0.1:{settings.PORT}/api/v1")
        print(f"• Interactive Docs:   http://127.0.0.1:{settings.PORT}/docs")
        print(f"• Web Admin Portal:   http://127.0.0.1:{settings.PORT}/admin-ui/")
        print("=" * 60)
        print("Starting server... Press Ctrl+C to stop.")
        print()

        uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
    except ImportError as e:
        print(f"Dependency Error: {e}")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)


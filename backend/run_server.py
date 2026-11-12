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

        port = int(os.getenv("PORT", settings.PORT))
        host = os.getenv("HOST", "0.0.0.0")

        print("=" * 60)
        print("  SRIVARI AI (శ్రీవారి AI) - DEVOTEE ASSISTANT BACKEND")
        print("=" * 60)
        print(f"• Host: {host}")
        print(f"• Port: {port}")
        print(f"• REST API Base:      http://{host}:{port}/api/v1")
        print(f"• Interactive Docs:   http://{host}:{port}/docs")
        print(f"• Web Admin Portal:   http://{host}:{port}/admin-ui/")
        print("=" * 60)
        print(f"Starting server on {host}:{port}...")

        uvicorn.run("app.main:app", host=host, port=port)
    except ImportError as e:
        print(f"Dependency Error: {e}")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)


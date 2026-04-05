"""
OpenEnv Server - Entry point for email triage environment
"""

from fastapi import FastAPI
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.main import app as api_app

# Create/reference the main app
if isinstance(api_app, FastAPI):
    app = api_app
else:
    app = FastAPI(title="Email Triage Environment", version="1.0.0")
    if hasattr(api_app, 'router'):
        app.include_router(api_app.router)


def main():
    """Entry point for OpenEnv server"""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()

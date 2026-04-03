"""
HuggingFace Spaces entry point for Email Triage Environment
This file is required for HF Spaces to recognize the app.
The actual API is defined in api/main.py
"""

import sys
import os

# Ensure the app directory is in the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.main import app

# This allows HF Spaces to find and run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

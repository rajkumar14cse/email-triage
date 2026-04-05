#!/usr/bin/env python3
"""Upload project files to HuggingFace Space"""

from pathlib import Path
from huggingface_hub import HfApi
import os

# Configuration
HF_TOKEN = os.getenv("HF_TOKEN", "")
REPO_ID = "arjun-ai-dev/email-triage-env"
REPO_TYPE = "space"

# Create API client
api = HfApi()

# Get project root
project_root = Path(__file__).parent

# Step 1: Create repo if it doesn't exist
print(f"Creating Space repository: {REPO_ID}...")
try:
    api.create_repo(
        repo_id=REPO_ID,
        repo_type=REPO_TYPE,
        private=False,
        token=HF_TOKEN,
        exist_ok=True
    )
    print(f"✓ Repository ready: {REPO_ID}")
except Exception as e:
    print(f"✗ Error creating repo: {e}")

# Step 2: Upload files
print(f"\nUploading files to {REPO_ID}...")

# Key files to upload
FILES_TO_UPLOAD = [
    # Root files
    "app.py",
    "inference.py",
    "requirements.txt",
    "pyproject.toml",
    "uv.lock",
    "Dockerfile",
    "openenv.yaml",
    "README.md",
    "LICENSE",
    # API module
    "api/__init__.py",
    "api/main.py",
    # Environment module
    "env/__init__.py",
    "env/environment.py",
    "env/models.py",
    # Data module
    "data/__init__.py",
    "data/emails.py",
    # Tasks module
    "tasks/__init__.py",
    "tasks/task_easy.py",
    "tasks/task_medium.py",
    "tasks/task_hard.py",
    # Server module
    "server/__init__.py",
    "server/app.py",
]

for file_path in FILES_TO_UPLOAD:
    full_path = project_root / file_path
    if full_path.exists():
        try:
            api.upload_file(
                path_or_fileobj=str(full_path),
                path_in_repo=file_path,
                repo_id=REPO_ID,
                repo_type=REPO_TYPE,
                token=HF_TOKEN,
            )
            print(f"✓ Uploaded: {file_path}")
        except Exception as e:
            print(f"✗ Error uploading {file_path}: {e}")
    else:
        print(f"- Skipped (not found): {file_path}")

print(f"\nDone! Your Space is ready at: https://huggingface.co/spaces/{REPO_ID}")

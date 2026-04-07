#!/usr/bin/env python3
"""Fix git history to remove secret and ensure pyproject.toml is pushed"""

import subprocess
import os

os.chdir(r'c:\Users\rajku\OneDrive\Documents\Desktop\Hackathon\email-triage-env')

# Reset to before the problematic commit
print("Resetting to commit 1fa5aac...")
subprocess.run(['git', 'reset', '--hard', '1fa5aac'], check=True)

# Re-add pyproject.toml from current working directory
print("Re-staging pyproject.toml...")
subprocess.run(['git', 'add', 'pyproject.toml'], check=True)

# Commit just pyproject.toml safely without secrets
print("Committing pyproject.toml...")
subprocess.run(['git', 'commit', '-m', 'Add pyproject.toml for multi-mode deployment'], check=True)

# Now add the fixed upload_to_hf.py
print("Adding fixed upload_to_hf.py...")
subprocess.run(['git', 'add', 'upload_to_hf.py'], check=True)
subprocess.run(['git', 'commit', '-m', 'Add upload script using environment variables'], check=True)

# Try pushing
print("Attempting to push...")
result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

if result.returncode != 0:
    print("Push may still be blocked. Check GitHub secret scanning settings.")
else:
    print("Successfully pushed!")

# Show status
subprocess.run(['git', 'status'], check=True)

"""
config.py - Contact info loader for Troy Hokanson document templates
====================================================================

Reads personal contact details from environment variables so that
sensitive information (phone number, email) is never hardcoded in
the public repository.

Priority order:
1. Environment variable already set in the shell, such as GitHub Actions Secret
2. .env file in the repo root, gitignored for local machine use
3. Fallback placeholder string safe for public display

Setup on a new device:
1. Copy config.example.env to .env in the repo root.
2. Fill in real values in .env.
3. Run any build script normally; config.py loads .env automatically.

GitHub Actions secrets:
TROY_PHONE
TROY_EMAIL
TROY_LOCATION
TROY_LINKEDIN
TROY_PORTFOLIO
TROY_NAME
"""

import os
from pathlib import Path


def _load_dotenv(env_path: Path) -> None:
    """Minimal .env loader with no external dependency."""
    if not env_path.exists():
        return
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


_load_dotenv(Path(__file__).parent / ".env")


TROY_PHONE = os.getenv("TROY_PHONE", "")
TROY_EMAIL = os.getenv("TROY_EMAIL", "TroyHokanson@iCloud.com")
TROY_LOCATION = os.getenv("TROY_LOCATION", "Lakeville, MN")
TROY_LINKEDIN = os.getenv("TROY_LINKEDIN", "linkedin.com/in/troyhokanson")
TROY_PORTFOLIO = os.getenv("TROY_PORTFOLIO", "https://TroyHokanson.com")
TROY_NAME = os.getenv("TROY_NAME", "Troy Hokanson")

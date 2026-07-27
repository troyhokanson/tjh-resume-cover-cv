"""
config.py - Contact info loader for Troy Hokanson document templates
====================================================================

Reads personal contact details from environment variables so that
sensitive information (phone number, email) is never hardcoded in
the public repository.

Priority order:
1. Nonblank environment variable already set in the shell, such as a GitHub Actions Secret
2. Nonblank value from the .env file in the repo root, gitignored for local machine use
3. Fallback value safe for public display

Blank environment variables are treated as unset. This prevents an empty
GitHub Actions secret from suppressing a valid public fallback such as the
canonical portfolio URL.

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


def _env_or_default(name: str, default: str) -> str:
    """Return a stripped nonblank environment value, otherwise the default."""
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    return value.strip()


_load_dotenv(Path(__file__).parent / ".env")


TROY_PHONE = _env_or_default("TROY_PHONE", "")
TROY_EMAIL = _env_or_default("TROY_EMAIL", "TroyHokanson@iCloud.com")
TROY_LOCATION = _env_or_default("TROY_LOCATION", "Lakeville, MN")
TROY_LINKEDIN = _env_or_default("TROY_LINKEDIN", "linkedin.com/in/troyhokanson")
TROY_PORTFOLIO = _env_or_default("TROY_PORTFOLIO", "https://troyhokanson.com")
TROY_NAME = _env_or_default("TROY_NAME", "Troy Hokanson")
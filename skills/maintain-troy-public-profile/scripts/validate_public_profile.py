#!/usr/bin/env python3
"""Validate Troy's public-profile contract and privacy-sensitive public text."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


CANONICAL_CAREER_REPO = "troyhokanson/tjh-resume-cover-cv"
CANONICAL_PRODUCTION_REPO = "troyhokanson/troyhokanson.github.io"
UNUSED_DUPLICATE_REPO = "troy-hokanson/portfolio"
REQUIRED_BLOCKED_IDS = {
    "fto_duration",
    "ftk_bootcamp_hours",
    "digital_evidence_volume",
    "cumulative_training_hours",
    "public_credential_identifiers",
}
TEXT_SUFFIXES = {".html", ".htm", ".md", ".txt", ".json", ".yml", ".yaml"}

PROHIBITED_PUBLIC_PATTERNS = [
    ("credential identifier", re.compile(r"\bCredential\s+ID\b", re.IGNORECASE)),
    ("license number", re.compile(r"\bLicense\s+(?:No\.?|Number)\b", re.IGNORECASE)),
    ("POST credential", re.compile(r"Minnesota\s+(?:Board\s+of\s+)?Peace\s+Officer\s+Standards", re.IGNORECASE)),
    ("POST credential", re.compile(r"\bMN\s+POST\b", re.IGNORECASE)),
    ("responder identifier", re.compile(r"\bFirst\s+Responder\b.{0,120}\b(?:ID|No\.?|Number)\b", re.IGNORECASE | re.DOTALL)),
    ("CCCI identifier", re.compile(r"\bCCCI\b.{0,40}\b(?:No\.?|ID|Number|#)\b", re.IGNORECASE | re.DOTALL)),
    ("blocked digital-evidence total", re.compile(r"\b5,(?:304|336|368)\s*GB\b", re.IGNORECASE)),
    ("blocked cumulative training total", re.compile(r"\b1,(?:238\.75|280\.75)\b")),
    ("unresolved FTO duration", re.compile(r"\b(?:18|19)[- ]year(?:s)?\b.{0,40}\b(?:FTO|Field Training Officer)\b", re.IGNORECASE)),
    ("unresolved FTO duration", re.compile(r"\b(?:FTO|Field Training Officer)\b.{0,40}\b(?:18|19)[- ]year(?:s)?\b", re.IGNORECASE)),
    ("unresolved FTK hours", re.compile(r"\bFTK\b.{0,80}\b(?:21|25)\s+hours?\b", re.IGNORECASE | re.DOTALL)),
    ("obsolete real-estate status", re.compile(r"\breferral-only\b", re.IGNORECASE)),
    ("incorrect military duration", re.compile(r"\b9[- ]year(?:s)?\b.{0,30}\bArmy\b", re.IGNORECASE)),
    ("unreviewed Google Drive link", re.compile(r"https?://(?:drive|docs)\.google\.com/", re.IGNORECASE)),
    ("unused portfolio route", re.compile(r"troy-hokanson(?:\.github\.io/portfolio|/portfolio)", re.IGNORECASE)),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--scan", type=Path, action="append", default=[])
    return parser.parse_args()


def iter_text_files(paths: list[Path]):
    for path in paths:
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            yield path
        elif path.is_dir():
            for candidate in sorted(path.rglob("*")):
                if candidate.is_file() and candidate.suffix.lower() in TEXT_SUFFIXES:
                    yield candidate


def validate_contract(contract: dict) -> list[str]:
    errors: list[str] = []
    if contract.get("candidate") != "Troy J. Hokanson":
        errors.append("Contract candidate must be Troy J. Hokanson.")

    authority = contract.get("authority", {})
    if authority.get("career_repository") != CANONICAL_CAREER_REPO:
        errors.append(f"Career repository must be {CANONICAL_CAREER_REPO}.")

    surfaces = contract.get("public_surfaces", {})
    if surfaces.get("production_repository") != CANONICAL_PRODUCTION_REPO:
        errors.append(f"Production repository must be {CANONICAL_PRODUCTION_REPO}.")
    duplicate = surfaces.get("unused_duplicate_repository", {})
    if duplicate.get("repository") != UNUSED_DUPLICATE_REPO:
        errors.append(f"Unused duplicate must be recorded as {UNUSED_DUPLICATE_REPO}.")
    if duplicate.get("required_visibility") != "private":
        errors.append("Unused duplicate must require private visibility.")

    claims = contract.get("approved_public_claims", [])
    ids = [claim.get("id") for claim in claims]
    if len(ids) != len(set(ids)):
        errors.append("Approved public claim IDs must be unique.")
    for claim in claims:
        if not claim.get("id") or not claim.get("public_text") or not claim.get("source"):
            errors.append("Every approved claim needs id, public_text, and source.")
        if not str(claim.get("status", "")).startswith("approved"):
            errors.append(f"Approved claim {claim.get('id')} has a non-approved status.")
        for label, pattern in PROHIBITED_PUBLIC_PATTERNS:
            if pattern.search(str(claim.get("public_text", ""))):
                errors.append(f"Approved claim {claim.get('id')} contains {label}.")

    blocked_ids = {item.get("id") for item in contract.get("unresolved_or_blocked_claims", [])}
    missing = sorted(REQUIRED_BLOCKED_IDS - blocked_ids)
    if missing:
        errors.append("Missing blocked claims: " + ", ".join(missing))
    return errors


def scan_public_text(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in iter_text_files(paths):
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in PROHIBITED_PUBLIC_PATTERNS:
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{path}:{line}: prohibited {label}")
    return errors


def main() -> int:
    args = parse_args()
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    errors = validate_contract(contract)
    errors.extend(scan_public_text(args.scan))
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: public-profile contract and scanned public text satisfy current controls")
    return 0


if __name__ == "__main__":
    sys.exit(main())

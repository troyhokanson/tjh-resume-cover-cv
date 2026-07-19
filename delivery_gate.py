"""Hard delivery gate for a Troy Hokanson resume and cover-letter pair."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pdfplumber

from anti_ai_scan import scan_pdf


PORTFOLIO_LABEL = "TroyHokanson.com"
LINKEDIN_LABEL = "linkedin.com/in/troyhokanson"


def first_page_text(path: Path) -> str:
    with pdfplumber.open(path) as pdf:
        if not pdf.pages:
            return ""
        return pdf.pages[0].extract_text() or ""


def check_header_text(text: str) -> list[str]:
    compact = " ".join(text.split())
    failures: list[str] = []
    linkedin_index = compact.find(LINKEDIN_LABEL)
    portfolio_index = compact.find(PORTFOLIO_LABEL)
    if linkedin_index < 0:
        failures.append(f"Missing required header item: {LINKEDIN_LABEL}")
    if portfolio_index < 0:
        failures.append(f"Missing required header item: {PORTFOLIO_LABEL}")
    elif linkedin_index >= 0 and portfolio_index < linkedin_index:
        failures.append("Portfolio must appear after LinkedIn in the page-one contact row.")
    return failures


def check_header(path: Path) -> list[str]:
    return check_header_text(first_page_text(path))


def run_gate(path: Path, doc_type: str, profile: str, allow_icac: bool) -> list[str]:
    failures = check_header(path)
    failures.extend(
        scan_pdf(
            str(path),
            doc_type=doc_type,
            profile=profile,
            strict=False,
            allow_icac=allow_icac,
        )
    )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a final resume and cover-letter pair.")
    parser.add_argument("resume_pdf", type=Path)
    parser.add_argument("cover_letter_pdf", type=Path)
    parser.add_argument("--profile", default="vendor-solutions")
    parser.add_argument("--icac", action="store_true")
    args = parser.parse_args()

    all_failures: list[str] = []
    for path, doc_type in ((args.resume_pdf, "resume"), (args.cover_letter_pdf, "cover")):
        if not path.exists():
            all_failures.append(f"Missing file: {path}")
            continue
        failures = run_gate(path, doc_type, args.profile, args.icac)
        all_failures.extend(f"{path.name}: {item}" for item in failures)

    if all_failures:
        print("[APPLICATION DELIVERY GATE - FAIL]")
        for failure in all_failures:
            print(f"  * {failure}")
        return 1

    print("[APPLICATION DELIVERY GATE - PASS]")
    print(f"  * Header contains {LINKEDIN_LABEL}, followed by {PORTFOLIO_LABEL}")
    print("  * Resume and cover letter passed the anti-AI / voice scan")
    return 0


if __name__ == "__main__":
    sys.exit(main())

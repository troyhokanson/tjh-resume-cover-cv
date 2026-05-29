"""
scan_and_report.py - Friendly wrapper around anti_ai_scan.scan_pdf.

Designed to be the single command run at the share-file delivery gate. Emits a
plain, readable report that names the profile, lists each violation with a
suggested fix hint, and returns a non-zero exit code on failure so it can be
wired into CI or pre-commit.

Usage:
    python scan_and_report.py /path/to/Hokanson_Cover_ThomsonReuters_JREQ200166.pdf cover
    python scan_and_report.py /path/to/Hokanson_Cover_GEICO_SIU_42.pdf cover --profile siu-fraud
    python scan_and_report.py /path/to/Hokanson_Resume_Stripe_TIA.pdf resume --profile analyst-intelligence
    python scan_and_report.py /path/to/Hokanson_Resume_Roblox.pdf resume --icac

Exit codes:
    0 - PASS (no violations)
    1 - FAIL (one or more violations)
    2 - ERROR (bad arguments, file not found, unreadable PDF)
"""

from __future__ import annotations
import sys
from pathlib import Path

from anti_ai_scan import (
    scan_pdf,
    FailedScan,
    DEFAULT_PROFILE,
    VALID_PROFILES,
    PROFILE_RULES,
)


FIX_HINTS = {
    "Em dash": "Replace with a period and start a new sentence, or restructure the clause.",
    "En dash": "Use 'to' in prose (e.g. '1998 to 2024'). Plain hyphen is OK in date fields only.",
    "Exclamation point": "Strip every exclamation point. Period or restructure.",
    "Ellipsis": "Use a period or rewrite the thought as a complete sentence.",
    "Curly/smart quotes": "Open the source in a plain editor and replace with straight quotes.",
    "Semicolon": "Split into two sentences. Semicolons read as essay-AI in cover letters and bios.",
    "Forbidden phrase": "See VOICE_STANDARD.md Layer 1 banned list. Replace with a plainer verb or restructure.",
    "Wrong-lane phrase": "This phrase belongs to a different profile. See PROFILES.md for the right vocabulary for this lane.",
    "As a [Title]": "Rewrite the opener. Start with the credential and the years, or with a concrete case.",
    "I look forward": "Strip it. Cover letters close on the human-connection sentence, then 'Respectfully,'.",
    "contractions": "Resumes and CVs: zero contractions. Cover letters: max two. Expand 'I'm' to 'I am' etc.",
    "PTSD-scope violation (always blocked)": "These terms are never used in any Hokanson document. Rewrite without them.",
    "PTSD-scope violation (ICAC-gated)": "If this is a child-safety platform role, pass --icac on the CLI. Otherwise rewrite.",
    "Protected veteran / VEVRAA": "Strip the VEVRAA / protected-veteran phrasing. Troy directed this be omitted.",
    "Cover letter uses": "Closing salutation must be exactly 'Respectfully,'.",
}


def _hint_for(violation: str) -> str:
    for key, hint in FIX_HINTS.items():
        if key.lower() in violation.lower():
            return hint
    return "See VOICE_STANDARD.md and PROFILES.md."


def _print_banner(name: str, doc_type: str, profile: str, allow_icac: bool) -> None:
    gate = "OPEN" if allow_icac else "CLOSED"
    print("=" * 72)
    print(f"  Troy Hokanson Anti-AI / Voice Scan")
    print(f"  File:      {name}")
    print(f"  Doc type:  {doc_type}")
    print(f"  Profile:   {profile}  ({PROFILE_RULES[profile]['description']})")
    print(f"  ICAC gate: {gate}")
    print("=" * 72)


def _parse_args(argv: list[str]) -> tuple[str, str, str, bool]:
    if not argv:
        print(
            "Usage:\n"
            "  python scan_and_report.py <pdf_path> [doc_type] [--profile NAME] [--icac]\n\n"
            f"Valid doc_type: resume | cover | cv | bio\n"
            f"Valid --profile: {' | '.join(VALID_PROFILES)} (default: {DEFAULT_PROFILE})\n"
            "Pass --icac only for child-safety platform roles (Roblox T&S, NCMEC, etc.)"
        )
        sys.exit(2)

    pdf = argv[0]
    doc_type = "resume"
    profile = DEFAULT_PROFILE
    allow_icac = False

    # First positional after pdf path, if it doesn't start with --, is doc_type
    if len(argv) > 1 and not argv[1].startswith("--"):
        doc_type = argv[1].lower()

    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--profile" and i + 1 < len(argv):
            profile = argv[i + 1].lower()
            i += 2
            continue
        if a.startswith("--profile="):
            profile = a.split("=", 1)[1].lower()
        elif a == "--icac":
            allow_icac = True
        i += 1

    if profile not in VALID_PROFILES:
        print(f"ERROR: invalid --profile '{profile}'. Must be one of: {', '.join(VALID_PROFILES)}")
        sys.exit(2)
    if doc_type not in ("resume", "cover", "cv", "bio"):
        print(f"ERROR: invalid doc_type '{doc_type}'. Must be one of: resume | cover | cv | bio")
        sys.exit(2)

    return pdf, doc_type, profile, allow_icac


def main(argv: list[str]) -> int:
    pdf_path, doc_type, profile, allow_icac = _parse_args(argv)

    p = Path(pdf_path)
    if not p.exists():
        print(f"ERROR: file not found: {pdf_path}")
        return 2

    _print_banner(p.name, doc_type, profile, allow_icac)

    try:
        failures = scan_pdf(
            str(p),
            doc_type=doc_type,
            profile=profile,
            strict=False,
            allow_icac=allow_icac,
        )
    except Exception as e:
        print(f"\nERROR running scan: {e}")
        return 2

    if not failures:
        print(f"\nRESULT: PASS  ({p.name})")
        print("This document cleared every Layer 1 and Layer 2 rule for the selected profile.")
        print("Manual read-aloud review still required before sharing.")
        return 0

    print(f"\nRESULT: FAIL  ({len(failures)} violation(s))\n")
    for idx, v in enumerate(failures, 1):
        print(f"  {idx}. {v}")
        print(f"     -> Fix: {_hint_for(v)}\n")

    print("=" * 72)
    print("DELIVERY GATE: BLOCKED. Fix the source text, rebuild the PDF, rescan.")
    print("Do not share this file with Troy or any recruiter until the scan passes.")
    print("=" * 72)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

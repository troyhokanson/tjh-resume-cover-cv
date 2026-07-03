"""
Anti-AI / Voice scan - MANDATORY automatic gate for every Hokanson document.

Codifies the rules from VOICE_STANDARD.md (Layer 1 + Layer 2), PROFILES.md,
and PRIVACY_STANDARD.md.
Run BEFORE share_file on any resume, cover letter, CV, recruiter packet, bio,
or one-pager.

Voice baseline: 54-year-old Gen-X medically retired Minnesota detective,
M.A. (GPA 3.94), 19 years adjunct teaching, empathetic + investigator-precise.

Usage:
    from anti_ai_scan import scan_pdf, FailedScan

    # Default profile is vendor-solutions:
    scan_pdf("/path/to/Hokanson_Resume_Foo.pdf", doc_type="resume")

    # Explicit profile selection:
    scan_pdf("/path/to/cover.pdf", doc_type="cover", profile="siu-fraud")
    scan_pdf("/path/to/cover.pdf", doc_type="cover", profile="analyst-intelligence")

    # ICAC / child-safety role build (gate opens for CSAM / exploitation terms):
    scan_pdf("/path/to/Hokanson_Resume_Roblox.pdf", doc_type="resume", allow_icac=True)

doc_type   = "resume" | "cover" | "cv" | "bio"
profile    = "vendor-solutions" (default) | "siu-fraud" | "analyst-intelligence"
allow_icac = False (default) | True
             When True, CSAM / child-exploitation / ICAC training references
             are permitted. All other PTSD-scope terms (homicide, lethal force,
             sexual assault, criminal sexual conduct, human trafficking) remain
             blocked regardless of this flag.

Privacy enforcement (PRIVACY_STANDARD.md):
    Suspect names, case control numbers, court case numbers, DOBs, victim names,
    judge names, and probation officer names are hard-blocked in all output
    documents. See PRIVACY_STANDARD.md for the full rationale and permitted
    element table. CASE_BANK.md is the internal source of truth and may retain
    full identifiers; application output documents must never reproduce them.
"""

from __future__ import annotations
import re
import sys
from pathlib import Path

try:
    from config import TROY_NAME, TROY_PHONE, TROY_EMAIL
except ImportError:
    TROY_NAME = "Troy J. Hokanson"
    TROY_PHONE = ""
    TROY_EMAIL = ""

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


class FailedScan(Exception):
    """Raised when a document fails the anti-AI / voice scan."""


VALID_PROFILES = ("VALID_PROFILES = (
    "vendor-solutions",
    "siu-fraud",
    "analyst-intelligence",
    "corporate-security-investigations")
DEFAULT_PROFILE = "vendor-solutions"


# =========================================================================
# LAYER 1 - HARD RULES (apply to every document, every profile)
# =========================================================================

# ---- Forbidden phrases ----
FORBIDDEN_PHRASES = [
    "I bring", "I offer", "leveraged", "harnessed", "spearheaded", "championed",
    "passionate about", "dynamic", "synergy", "synergies", "robust",
    "comprehensive", "cutting-edge", "best-in-class", "results-driven",
    "detail-oriented", "proven track record", "in today's environment",
    "in conclusion", "to summarize", "it is worth noting", "I am excited to",
    "I would be remiss", "at the end of the day", "needless to say",
    "with that said", "that being said", "moving forward", "going forward",
    "touch base", "circle back", "value-add", "value add", "impactful",
    "game-changer", "paradigm shift", "holistic approach", "deep dive",
    "bandwidth", "optimized", "streamlined", "facilitated", "delivered value",
    "implemented solutions", "drove outcomes", "empowered", "transformed",
    "transforming", "I look forward to discussing",
]

# Phrases the user has explicitly flagged as AI-sounding in this lineage
EXTRA_FLAGGED = [
    "ramping on",          # AI-business cliche substitute for "learning"
    "fundamentally",       # AI throat-clearing adverb in cover letters
    "in order to",         # filler - use "to"
    "utilize", "utilized", "utilizing",  # use "use"
    "utilization",
    "myriad of",
    "plethora",
    "delve into", "delving",
    "tapestry",
    "navigate the complexities",
    "ever-evolving", "ever-changing",
    "seamlessly",
    "elevate",
    "unlock",
    "world-class",
    "best practices",      # only flagged in flowing prose, not section headings

    # Redundant skill terminology (X and Y where Y is already inside X)
    "OSINT and open-source",         # use OSINT only
    "interviews and interrogations",  # use investigative interviewing
    "surveillance and monitoring",    # use surveillance
    "training and mentoring",         # use field training or mentorship per context
    "remote and online",              # use remote instruction
    "research and analysis",          # use investigative analysis
    "leadership and management",      # use leadership
    "planning and coordination",      # use operational coordination
]

ALL_FORBIDDEN = FORBIDDEN_PHRASES + EXTRA_FLAGGED


# ---- PTSD-scope term sets ----
# Always-blocked: never appropriate in any Hokanson document regardless of role.
PTSD_TERMS_ALWAYS_BLOCKED = [
    "homicide",
    "death investigation",
    "lethal force",
    "sexual assault",
    "criminal sexual conduct",
    "human trafficking",
]

# ICAC-gated: blocked by default. Pass allow_icac=True for documents targeting
# child-safety / ICAC platform roles (e.g. Roblox Trust & Safety, NCMEC,
# tech platform child-safety teams) where this experience and ICAC training
# is directly relevant and expected by the hiring team.
PTSD_TERMS_ICAC_GATED = [
    "CSAM",
    "child sexual",
    "child abuse",
    "child exploitation",
    "ICAC",
]


# =========================================================================
# PRIVACY STANDARD - CASE IDENTIFIER SUPPRESSION
# Enforces PRIVACY_STANDARD.md Section 1 and Section 6.
#
# Hard rule: suspect names, case control numbers, court case numbers, DOBs,
# victim names, judge names, and probation officer names must NEVER appear
# in any application output document.
#
# CASE_BANK.md is the internal source and may retain full identifiers.
# Application output documents (resume, cover, cv, bio) must never
# reproduce them. See PRIVACY_STANDARD.md for the full rationale,
# permitted element table, and expungement special rule.
#
# MAINTENANCE: When a new case is added to CASE_BANK.md, add the subject's
# full name and any judicial/PO names to SUPPRESSED_NAMES below. Keep this
# list synchronized with PRIVACY_STANDARD.md Section 6.
# =========================================================================

# Subject names, victim names, judicial names, and PO names from case files.
# Full names and likely partial matches (last name alone) are both listed
# where the last name is uncommon enough to be uniquely identifying.
# Generic first names alone (e.g., "Matt") are not listed as they create
# false positives in unrelated text.
SUPPRESSED_NAMES = [
    # Case 2 - Occupational fraud (MCI Paint and Drywall)
    "Condello Wall",
    # Case 4 - Commercial burglary
    "Matt Garwood",
    "Matthew Garwood",
    "Matthew Scott Garwood",
    # Judicial names from Cases 2 and 4
    "Arlene Perkkio",
    "Perkkio",
]

# Regex patterns for structural case identifiers.
# These are hard-blocked regardless of content around them.
# Pattern: Lakeville PD / Dakota County internal control number format
_CONTROL_NUMBER_PATTERN = re.compile(r"Control\s*#\s*\d+", re.IGNORECASE)

# Pattern: Minnesota district court case number format (e.g., 19HA-CR-11-907)
_COURT_CASE_PATTERN = re.compile(
    r"\b\d{2}[A-Z]{2}-[A-Z]{2}-\d{2}-\d{4}\b", re.IGNORECASE
)

# Pattern: Date of birth in MM/DD/YYYY format used as a subject identifier
_DOB_PATTERN = re.compile(r"\bDOB\s*[:\-]?\s*\d{2}/\d{2}/\d{4}\b", re.IGNORECASE)


# =========================================================================
# LAYER 2 - PROFILE-SPECIFIC RULES (selected by --profile flag)
# =========================================================================
#
# Each profile defines additional banned phrases that read as the WRONG lane
# for the target audience. Layer 1 bans always apply on top of these.
#
# See PROFILES.md for the full per-profile vocabulary, framing, and worked
# examples. This dict is the programmatic enforcement surface only.
# =========================================================================

PROFILE_RULES = {
    "vendor-solutions": {
        "description": (
            "Solutions Consultant / Sales Engineer / Solutions Expert / "
            "Public Safety Manager. Vendor-side end-user expertise."
        ),
        "banned_phrases": [
            # Silicon Valley sales cliches that read as performed, not earned
            "evangelize", "evangelist", "evangelizing",
            "rockstar", "ninja", "guru",
            "drive revenue", "drive top-line", "top-of-funnel",
            "thought leadership", "thought leader",
            "passionate practitioner",
            "trusted advisor",
            # SIU / claims vocabulary in wrong lane
            "examination under oath", "recorded statement of the insured",
            "claim file review", "indicator review",
            # Pure intel-cycle vocabulary as primary framing (allowed as occasional
            # reference but not as the dominant verb pattern)
            "F3EAD", "key intelligence question",
        ],
    },
    "siu-fraud": {
        "description": (
            "SIU Investigator / Insurance Fraud Investigator / Fraud Examiner "
            "(claims-side, carrier-side)."
        ),
        "banned_phrases": [
            # Vendor / sales lane
            "evangelize", "evangelist", "evangelizing",
            "demo to the customer", "customer demo",
            "drive revenue", "drive top-line", "top-of-funnel",
            "sales cycle", "deal cycle", "pipeline coverage",
            "thought leadership", "thought leader",
            "trusted advisor",
            # Intel-cycle vocabulary in wrong lane
            "F3EAD", "key intelligence question",
            "finished intelligence", "raw to finished",
            # Overused
            "boots on the ground",
        ],
    },
    "analyst-intelligence": {
        "description": (
            "Investigations and Intelligence Analyst / Financial Crime Analyst "
            "/ Cybersecurity Fraud Analyst / Corporate Security Analyst."
        ),
        "banned_phrases": [
            # Vendor / sales lane
            "evangelize", "evangelist", "evangelizing",
            "demo to the customer", "customer demo",
            "drive revenue", "drive top-line", "top-of-funnel",
            "sales cycle", "deal cycle", "pipeline coverage",
            "thought leadership", "thought leader",
            "trusted advisor",
            # SIU adjuster vocabulary in wrong lane
            "examination under oath", "recorded statement of the insured",
            "claim file review",
            # Overused analyst tells
            "actionable intelligence",
            "boots on the ground",
        ],
    },
}


def _validate_profile(profile: str) -> str:
    profile = (profile or DEFAULT_PROFILE).lower()
    if profile not in VALID_PROFILES:
        raise ValueError(
            f"Unknown profile: '{profile}'. "
            f"Must be one of: {', '.join(VALID_PROFILES)}"
        )
    return profile


def _extract(pdf_path: str) -> str:
    if pdfplumber is None:
        raise RuntimeError("pdfplumber not installed - cannot scan PDF")
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join((p.extract_text() or "") for p in pdf.pages)


def _strip_header(text: str) -> str:
    """Remove the locked navy header repeated rows (name + contact line)
    so they are not falsely flagged."""
    _email_user = TROY_EMAIL.split("@")[0] if "@" in TROY_EMAIL else TROY_EMAIL
    out = []
    for line in text.splitlines():
        s = line.strip()
        if TROY_NAME and s.startswith(TROY_NAME):
            continue
        if s.startswith("---") or set(s) <= {"-", " "}:
            continue
        if TROY_PHONE and TROY_PHONE in s and _email_user and _email_user in s:
            continue
        out.append(line)
    return "\n".join(out)


def scan_text(
    text: str,
    doc_type: str = "resume",
    profile: str = DEFAULT_PROFILE,
    allow_icac: bool = False,
) -> list[str]:
    """Return list of violation strings. Empty list = pass.

    Parameters
    ----------
    text       : raw document text
    doc_type   : "resume" | "cover" | "cv" | "bio"
    profile    : "vendor-solutions" (default) | "siu-fraud" | "analyst-intelligence"
    allow_icac : When True, opens the ICAC gate - permits CSAM / child-
                 exploitation / ICAC training references. Use only for
                 documents targeting ICAC or child-safety platform roles.
                 All other PTSD-scope terms remain blocked.
    """
    doc_type = doc_type.lower()
    profile = _validate_profile(profile)
    body = _strip_header(text)
    failures = []

    # 1. Em / en dashes - never in any document
    if "\u2014" in body:
        failures.append(f"[L1] Em dash found ({body.count(chr(0x2014))}x). Replace with comma, period, or rewrite.")
    if "\u2013" in body:
        failures.append(f"[L1] En dash found ({body.count(chr(0x2013))}x). Use plain hyphen in date fields only.")

    # 1b. Double-hyphen ( -- ) - em dash substitute, equally forbidden
    double_hyphen_count = len(re.findall(r"--", body))
    if double_hyphen_count:
        failures.append(
            f"[L1] Double-hyphen ( -- ) found ({double_hyphen_count}x). "
            f"This is an em dash substitute and is equally forbidden. "
            f"Replace with a comma, period, or restructure the sentence."
        )

    # 1c. Space-hyphen-space ( word - word ) used as a clause separator
    # Exclude valid date ranges like "1998-2024" (no spaces around hyphen)
    # and dimension ranges. Flag only where spaces surround the hyphen.
    space_hyphen_count = len(re.findall(r"(?<=[A-Za-z,)]) - (?=[A-Za-z(])", body))
    if space_hyphen_count:
        failures.append(
            f"[L1] Space-hyphen-space ( - ) used as clause separator "
            f"({space_hyphen_count}x). This is a visual em dash substitute "
            f"and is equally forbidden. Use a comma, period, or semicolon instead."
        )

    # 2. Exclamation points - never
    if "!" in body:
        failures.append(f"[L1] Exclamation point(s) found ({body.count('!')}x). Forbidden in professional content.")

    # 3. Ellipses for stylistic effect
    if "..." in body or "\u2026" in body:
        failures.append("[L1] Ellipsis found. Forbidden - use a period or rewrite.")

    # 4. Curly / smart quotes (Word auto-substitution leakage)
    curly = sum(body.count(c) for c in "\u201c\u201d\u2018\u2019")
    if curly:
        failures.append(f"[L1] Curly/smart quotes found ({curly}x). Use straight quotes only.")

    # 5. Semicolons - forbidden in cover letters and About/bio sections
    if doc_type in ("cover", "bio") and ";" in body:
        failures.append(f"[L1] Semicolon(s) found in {doc_type} ({body.count(';')}x). Forbidden - split into separate sentences.")

    # 6. Layer 1 forbidden phrases (whole-word, case-insensitive)
    for p in ALL_FORBIDDEN:
        pattern = re.escape(p).replace(r"\'", r"[''']")
        if re.search(rf"(?<![A-Za-z]){pattern}(?![A-Za-z])", body, re.IGNORECASE):
            failures.append(f"[L1] Forbidden phrase: '{p}'")

    # 6b. Layer 2 profile-specific banned phrases
    for p in PROFILE_RULES[profile]["banned_phrases"]:
        pattern = re.escape(p).replace(r"\'", r"[''']")
        if re.search(rf"(?<![A-Za-z]){pattern}(?![A-Za-z])", body, re.IGNORECASE):
            failures.append(f"[L2:{profile}] Wrong-lane phrase: '{p}'")

    # 7. "As a [Title]..." paragraph opener
    if re.search(r"(?m)^\s*As an? [A-Z][a-z]+", body):
        failures.append("[L1] Paragraph opens with 'As a [Title]...' - strongest AI opener pattern.")

    # 8. Cover-letter-specific structural rules
    if doc_type == "cover":
        if re.search(r"I look forward", body, re.IGNORECASE):
            failures.append("[L1] Cover letter contains 'I look forward...' - most-overused AI closing.")
        for bad_close in ["Sincerely,", "Best regards,", "Best,", "Thank you,", "Kind regards,", "Warm regards,"]:
            if bad_close in body:
                failures.append(f"[L1] Cover letter uses '{bad_close}' - must be 'Respectfully,'")
        contractions = re.findall(
            r"\b(?:I'm|I've|I'll|I'd|don't|won't|can't|isn't|aren't|wasn't|weren't|haven't|hasn't|hadn't"
            r"|wouldn't|shouldn't|couldn't|it's|that's|there's|here's|what's|who's|let's"
            r"|you're|we're|they're|you'll|we'll|they'll|you've|we've|they've|you'd|we'd|they'd)\b",
            body, re.IGNORECASE,
        )
        if len(contractions) > 2:
            failures.append(f"[L1] Cover letter has {len(contractions)} contractions (max 2): {contractions}")

    # 9. Resume / CV bullet contractions - zero allowed (possessives like Master's exempted)
    if doc_type in ("resume", "cv"):
        bullet_contractions = re.findall(
            r"\b(?:I'm|I've|I'll|I'd|don't|won't|can't|isn't|aren't|wasn't|weren't|haven't|hasn't|hadn't"
            r"|wouldn't|shouldn't|couldn't|it's|that's|there's|here's|let's|you're|we're|they're)\b",
            body, re.IGNORECASE,
        )
        if bullet_contractions:
            failures.append(f"[L1] {doc_type} contains contractions (zero allowed): {bullet_contractions}")

    # 10. PTSD-scope guard
    #
    # Always-blocked: never appropriate in any document regardless of role.
    for term in PTSD_TERMS_ALWAYS_BLOCKED:
        if re.search(rf"\b{re.escape(term)}\b", body, re.IGNORECASE):
            failures.append(f"[L1:PTSD] PTSD-scope violation (always blocked): '{term}' must not appear.")

    # ICAC-gated: blocked by default. Open the gate with allow_icac=True
    # when building documents for child-safety / ICAC platform roles.
    if not allow_icac:
        for term in PTSD_TERMS_ICAC_GATED:
            if re.search(rf"\b{re.escape(term)}\b", body, re.IGNORECASE):
                failures.append(
                    f"[L1:PTSD] PTSD-scope violation (ICAC-gated): '{term}' present. "
                    f"Pass allow_icac=True to permit for child-safety / ICAC role documents."
                )

    # 11. PRIVACY STANDARD - case identifier suppression
    #     Enforces PRIVACY_STANDARD.md Sections 1 and 6.
    #     Hard-blocks suspect names, case control numbers, court case numbers,
    #     DOBs, victim names, judge names, and probation officer names.
    #     CASE_BANK.md is the internal source; application output must never
    #     reproduce these identifiers.
    #
    #     MAINTENANCE: When a new case is added to CASE_BANK.md, add the
    #     subject's name (and any judicial/PO names) to SUPPRESSED_NAMES above.

    # 11a. Suppressed names (subjects, judges, POs from case files)
    for name in SUPPRESSED_NAMES:
        if re.search(rf"\b{re.escape(name)}\b", body, re.IGNORECASE):
            failures.append(
                f"[L1:PRIVACY] Suppressed case identifier present: '{name}'. "
                f"Replace with role descriptor only (e.g., 'the subject', 'the court'). "
                f"See PRIVACY_STANDARD.md Section 1."
            )

    # 11b. Case control numbers (internal department format)
    if _CONTROL_NUMBER_PATTERN.search(body):
        failures.append(
            "[L1:PRIVACY] Case control number found (e.g., 'Control #XXXXXXXX'). "
            "Omit entirely from application documents. "
            "See PRIVACY_STANDARD.md Section 1B."
        )

    # 11c. Minnesota district court case numbers (e.g., 19HA-CR-11-907)
    if _COURT_CASE_PATTERN.search(body):
        failures.append(
            "[L1:PRIVACY] Court case number found (e.g., '19HA-CR-11-907'). "
            "Omit entirely from application documents. "
            "See PRIVACY_STANDARD.md Section 1B."
        )

    # 11d. Date of birth used as subject identifier
    if _DOB_PATTERN.search(body):
        failures.append(
            "[L1:PRIVACY] DOB string found (e.g., 'DOB: MM/DD/YYYY'). "
            "Omit entirely from application documents. "
            "See PRIVACY_STANDARD.md Section 1C."
        )

    # 12. Protected veteran / VEVRAA language guard
    if re.search(r"\b(VEVRAA|protected veteran)\b", body, re.IGNORECASE):
        failures.append("[L1] Protected veteran / VEVRAA language present - Troy directed this be omitted.")

    return failures


def scan_pdf(
    pdf_path: str,
    doc_type: str = "resume",
    profile: str = DEFAULT_PROFILE,
    strict: bool = True,
    allow_icac: bool = False,
) -> list[str]:
    """
    Scan a PDF and return violations.

    Parameters
    ----------
    pdf_path   : path to the PDF file
    doc_type   : "resume" | "cover" | "cv" | "bio"
    profile    : "vendor-solutions" (default) | "siu-fraud" | "analyst-intelligence"
    strict     : If True (default), raises FailedScan on any violation.
                 If False, prints violations and returns the list.
    allow_icac : When True, opens the ICAC gate - permits CSAM / child-
                 exploitation / ICAC training references. Use only for
                 documents targeting ICAC or child-safety platform roles.
                 All other PTSD-scope terms remain blocked.
    """
    if not Path(pdf_path).exists():
        raise FileNotFoundError(pdf_path)
    profile = _validate_profile(profile)
    text = _extract(pdf_path)
    failures = scan_text(text, doc_type=doc_type, profile=profile, allow_icac=allow_icac)

    name = Path(pdf_path).name
    gate_note = " [ICAC gate: OPEN]" if allow_icac else ""
    profile_note = f" [profile: {profile}]"
    if failures:
        msg = (
            f"\n[ANTI-AI SCAN - FAIL] {name}  ({doc_type}){profile_note}{gate_note}\n"
            + "\n".join(f"  * {f}" for f in failures)
        )
        if strict:
            raise FailedScan(msg)
        else:
            print(msg)
    else:
        print(f"[ANTI-AI SCAN - PASS] {name}  ({doc_type}){profile_note}{gate_note}")
    return failures


if __name__ == "__main__":
    # CLI usage:
    #   python anti_ai_scan.py /path/to/file.pdf resume
    #   python anti_ai_scan.py /path/to/file.pdf cover --profile siu-fraud
    #   python anti_ai_scan.py /path/to/file.pdf resume --profile analyst-intelligence --icac
    args = sys.argv[1:]
    if not args:
        print("Usage: python anti_ai_scan.py <pdf_path> [doc_type] [--profile NAME] [--icac]")
        sys.exit(2)
    p = args[0]
    t = args[1] if len(args) > 1 and not args[1].startswith("--") else "resume"

    # Parse flags
    profile = DEFAULT_PROFILE
    icac = False
    for i, a in enumerate(args):
        if a == "--profile" and i + 1 < len(args):
            profile = args[i + 1]
        elif a.startswith("--profile="):
            profile = a.split("=", 1)[1]
        elif a == "--icac":
            icac = True

    scan_pdf(p, doc_type=t, profile=profile, strict=False, allow_icac=icac)

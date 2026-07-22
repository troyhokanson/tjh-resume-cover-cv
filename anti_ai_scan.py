"""
Anti-AI / Voice scan - MANDATORY automatic gate for every Hokanson document.

Codifies the hard safeguards from VOICE_STANDARD.md, ROLE_ADAPTATION_STANDARD.md,
PROFILES.md, and PRIVACY_STANDARD.md. Run BEFORE share_file on any resume, cover letter,
CV, recruiter packet, bio, or one-pager.

Voice baseline: 54-year-old Gen-X medically retired Minnesota detective,
M.A. (GPA 3.94), 19 years adjunct teaching, empathetic + investigator-precise.
"""

from __future__ import annotations
import re
import sys
from pathlib import Path

try:
    from config import TROY_NAME, TROY_PHONE, TROY_EMAIL
except ImportError:
    TROY_NAME = "Troy Hokanson"
    TROY_PHONE = ""
    TROY_EMAIL = ""

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


class FailedScan(Exception):
    """Raised when a document fails the anti-AI / voice scan."""


VALID_PROFILES = (
    "adaptive",
    "vendor-solutions",
    "siu-fraud",
    "analyst-intelligence",
    "corporate-security-investigations",
    "customer-success",
    "technical-account-management",
    "dfir-cyber",
)
DEFAULT_PROFILE = "adaptive"


# =========================================================================
# LAYER 1 - HARD RULES (apply to every document, every profile)
# =========================================================================

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
    "bandwidth", "I look forward to discussing",
]

EXTRA_FLAGGED = [
    "ramping on",
    "fundamentally",
    "in order to",
    "utilize", "utilized", "utilizing",
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
    "OSINT and open-source",
    "interviews and interrogations",
    "surveillance and monitoring",
    "training and mentoring",
    "remote and online",
    "research and analysis",
    "leadership and management",
    "planning and coordination",
]

ALL_FORBIDDEN = FORBIDDEN_PHRASES + EXTRA_FLAGGED


PTSD_TERMS_ALWAYS_BLOCKED = [
    "homicide",
    "death investigation",
    "lethal force",
    "sexual assault",
    "criminal sexual conduct",
    "human trafficking",
]

PTSD_TERMS_ICAC_GATED = [
    "CSAM",
    "child sexual",
    "child abuse",
    "child exploitation",
    "ICAC",
]


# =========================================================================
# PRIVACY STANDARD - CASE IDENTIFIER SUPPRESSION
# =========================================================================

SUPPRESSED_NAMES = [
    "Condello Wall",
    "Matt Garwood",
    "Matthew Garwood",
    "Matthew Scott Garwood",
    "Arlene Perkkio",
    "Perkkio",
]

_CONTROL_NUMBER_PATTERN = re.compile(r"Control\s*#\s*\d+", re.IGNORECASE)
_COURT_CASE_PATTERN = re.compile(
    r"\b\d{2}[A-Z]{2}-[A-Z]{2}-\d{2}-\d{4}\b", re.IGNORECASE
)
_DOB_PATTERN = re.compile(r"\bDOB\s*[:\-]?\s*\d{2}/\d{2}/\d{4}\b", re.IGNORECASE)

_POST_LICENSE_REFERENCE_PATTERN = re.compile(
    r"\b(?:Minnesota\s+|MN\s+)?"
    r"(?:Peace\s+Officer(?:\s+POST)?|POST(?:\s+Board)?)\s+"
    r"(?:License|Licensed|Certification|Certified)\b",
    re.IGNORECASE,
)
_POST_NUMBER_PATTERN = re.compile(
    r"\bPOST\s*(?:#|No\.?|Number|License\s*(?:No\.?|Number)?)\s*\d{4,6}\b",
    re.IGNORECASE,
)


# =========================================================================
# LAYER 2 - PROFILE-SPECIFIC RULES
# =========================================================================

PROFILE_RULES = {
    "adaptive": {
        "description": "Posting-led drafting when no primary lane has been selected yet.",
        "banned_phrases": [],
    },
    "vendor-solutions": {
        "description": (
            "Solutions Consultant / Sales Engineer / Solutions Expert / "
            "Public Safety Manager. Vendor-side end-user expertise."
        ),
        "banned_phrases": [
            "evangelize", "evangelist", "evangelizing",
            "rockstar", "ninja", "guru",
            "drive revenue", "drive top-line", "top-of-funnel",
            "thought leadership", "thought leader",
            "passionate practitioner",
            "trusted advisor",
            "examination under oath", "recorded statement of the insured",
            "claim file review", "indicator review",
            "F3EAD", "key intelligence question",
        ],
    },
    "siu-fraud": {
        "description": (
            "SIU Investigator / Insurance Fraud Investigator / Fraud Examiner "
            "(claims-side, carrier-side)."
        ),
        "banned_phrases": [
            "evangelize", "evangelist", "evangelizing",
            "demo to the customer", "customer demo",
            "drive revenue", "drive top-line", "top-of-funnel",
            "sales cycle", "deal cycle", "pipeline coverage",
            "thought leadership", "thought leader",
            "trusted advisor",
            "F3EAD", "key intelligence question",
            "finished intelligence", "raw to finished",
            "boots on the ground",
        ],
    },
    "analyst-intelligence": {
        "description": (
            "Investigations and Intelligence Analyst / Financial Crime Analyst "
            "/ Cybersecurity Fraud Analyst / Corporate Security Analyst."
        ),
        "banned_phrases": [
            "evangelize", "evangelist", "evangelizing",
            "demo to the customer", "customer demo",
            "drive revenue", "drive top-line", "top-of-funnel",
            "sales cycle", "deal cycle", "pipeline coverage",
            "thought leadership", "thought leader",
            "trusted advisor",
            "examination under oath", "recorded statement of the insured",
            "claim file review",
            "actionable intelligence",
            "boots on the ground",
        ],
    },
    "corporate-security-investigations": {
        "description": (
            "Corporate Security Investigator / Global Special Investigator / "
            "Enterprise Investigations / Insider Threat / Workplace Violence / "
            "Employee Misconduct."
        ),
        "banned_phrases": [
            "end-user side of the workflow",
            "demo to the customer", "customer demo",
            "drive revenue", "drive top-line", "top-of-funnel",
            "sales cycle", "deal cycle", "pipeline coverage",
            "recorded statement of the insured", "examination under oath",
            "claim file review", "policyholders", "premiums",
            "boots on the ground",
            "trusted advisor", "thought leadership", "thought leader",
            "passion for investigations", "lifelong service",
        ],
    },
    "customer-success": {
        "description": "Customer Success Manager / Customer Enablement / Agency Success.",
        "banned_phrases": [
            "examination under oath", "recorded statement of the insured",
            "claim file review", "policyholders", "premiums",
            "F3EAD", "finished intelligence", "boots on the ground",
        ],
    },
    "technical-account-management": {
        "description": "Technical Account Manager / Customer Success Engineer / Service Delivery.",
        "banned_phrases": [
            "examination under oath", "recorded statement of the insured",
            "claim file review", "policyholders", "premiums",
            "boots on the ground",
        ],
    },
    "dfir-cyber": {
        "description": "Digital Forensics / DFIR / Cyber Investigations / Forensic Consulting.",
        "banned_phrases": [
            "recorded statement of the insured", "claim file review",
            "policyholders", "premiums", "top-of-funnel",
            "pipeline coverage", "deal cycle", "boots on the ground",
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
    """Remove the locked navy header repeated rows so they are not falsely flagged."""
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
    """Return list of violation strings. Empty list means pass."""
    doc_type = doc_type.lower()
    profile = _validate_profile(profile)
    body = _strip_header(text)
    failures = []

    if "\u2014" in body:
        failures.append(f"[L1] Em dash found ({body.count(chr(0x2014))}x). Replace with comma, period, or rewrite.")
    if "\u2013" in body:
        failures.append(f"[L1] En dash found ({body.count(chr(0x2013))}x). Use plain hyphen in date fields only.")

    double_hyphen_count = len(re.findall(r"--", body))
    if double_hyphen_count:
        failures.append(
            f"[L1] Double-hyphen ( -- ) found ({double_hyphen_count}x). "
            "This is an em dash substitute and is equally forbidden. "
            "Replace with comma, period, or restructure the sentence."
        )

    space_hyphen_count = len(re.findall(r"(?<=[A-Za-z,)]) - (?=[A-Za-z(])", body))
    if space_hyphen_count:
        failures.append(
            f"[L1] Space-hyphen-space ( - ) used as clause separator ({space_hyphen_count}x). "
            "This is a visual em dash substitute and is equally forbidden. "
            "Use comma, period, or semicolon instead."
        )

    if "!" in body:
        failures.append(f"[L1] Exclamation point(s) found ({body.count('!')}x). Forbidden in professional content.")

    if "..." in body or "\u2026" in body:
        failures.append("[L1] Ellipsis found. Forbidden - use a period or rewrite.")

    curly = sum(body.count(c) for c in "\u201c\u201d\u2018\u2019")
    if curly:
        failures.append(f"[L1] Curly/smart quotes found ({curly}x). Use straight quotes only.")

    if doc_type in ("cover", "bio") and ";" in body:
        failures.append(f"[L1] Semicolon(s) found in {doc_type} ({body.count(';')}x). Forbidden - split into separate sentences.")

    for p in ALL_FORBIDDEN:
        pattern = re.escape(p).replace(r"\'", r"[''']")
        if re.search(rf"(?<![A-Za-z]){pattern}(?![A-Za-z])", body, re.IGNORECASE):
            failures.append(f"[L1] Forbidden phrase: '{p}'")

    for p in PROFILE_RULES[profile]["banned_phrases"]:
        pattern = re.escape(p).replace(r"\'", r"[''']")
        if re.search(rf"(?<![A-Za-z]){pattern}(?![A-Za-z])", body, re.IGNORECASE):
            failures.append(f"[L2:{profile}] Wrong-lane phrase: '{p}'")

    if re.search(r"(?m)^\s*As an? [A-Z][a-z]+", body):
        failures.append("[L1] Paragraph opens with 'As a [Title]...' - strongest AI opener pattern.")

    if doc_type == "cover":
        # Cover-letter opener, paragraph structure, contractions, and professional
        # closing are role-adaptive. High-signal cliches remain covered above.
        pass
    if doc_type in ("resume", "cv"):
        bullet_contractions = re.findall(
            r"\b(?:I'm|I've|I'll|I'd|don't|won't|can't|isn't|aren't|wasn't|weren't|haven't|hasn't|hadn't"
            r"|wouldn't|shouldn't|couldn't|it's|that's|there's|here's|let's|you're|we're|they're)\b",
            body, re.IGNORECASE,
        )
        if bullet_contractions:
            failures.append(f"[L1] {doc_type} contains contractions (zero allowed): {bullet_contractions}")

    for term in PTSD_TERMS_ALWAYS_BLOCKED:
        if re.search(rf"\b{re.escape(term)}\b", body, re.IGNORECASE):
            failures.append(f"[L1:PTSD] PTSD-scope violation (always blocked): '{term}' must not appear.")

    if not allow_icac:
        for term in PTSD_TERMS_ICAC_GATED:
            if re.search(rf"\b{re.escape(term)}\b", body, re.IGNORECASE):
                failures.append(
                    f"[L1:PTSD] PTSD-scope violation (ICAC-gated): '{term}' present. "
                    "Pass allow_icac=True to permit for child-safety / ICAC role documents."
                )

    for name in SUPPRESSED_NAMES:
        if re.search(rf"\b{re.escape(name)}\b", body, re.IGNORECASE):
            failures.append(
                f"[L1:PRIVACY] Suppressed case identifier present: '{name}'. "
                "Replace with role descriptor only. See PRIVACY_STANDARD.md Section 1."
            )

    if _CONTROL_NUMBER_PATTERN.search(body):
        failures.append("[L1:PRIVACY] Case control number found. Omit entirely from application documents.")

    if _COURT_CASE_PATTERN.search(body):
        failures.append("[L1:PRIVACY] Court case number found. Omit entirely from application documents.")

    if _DOB_PATTERN.search(body):
        failures.append("[L1:PRIVACY] DOB string found. Omit entirely from application documents.")

    if _POST_LICENSE_REFERENCE_PATTERN.search(body) or _POST_NUMBER_PATTERN.search(body):
        failures.append(
            "[L1:PRIVACY] POST / peace-officer licensing identifier found. "
            "Omit the entire licensing credential from public and application documents."
        )

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
    """Scan a PDF and return violations."""
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
        print(msg)
    else:
        print(f"[ANTI-AI SCAN - PASS] {name}  ({doc_type}){profile_note}{gate_note}")
    return failures


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: python anti_ai_scan.py <pdf_path> [doc_type] [--profile NAME] [--icac]")
        sys.exit(2)
    p = args[0]
    t = args[1] if len(args) > 1 and not args[1].startswith("--") else "resume"

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

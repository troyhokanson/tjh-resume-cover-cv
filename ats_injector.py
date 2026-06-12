"""
ats_injector.py — ATS Keyword Injection Module
================================================

Analyzes a job description and injects missing ATS keywords into resume and
cover letter text in a voice-compliant, natural way. Designed for Troy Hokanson
document builds. Never stuffs keywords — always places them in grammatically
valid, contextually accurate positions.

Usage in any build script:

    from ats_injector import ATSInjector

    injector = ATSInjector(
        jd_text=open("job_description.txt").read(),
        profile="siu-fraud"          # or vendor-solutions / analyst-intelligence
    )

    # Check what's missing
    report = injector.audit(resume_text + cover_text)
    print(report)

    # Inject into a specific section string
    enhanced_summary = injector.inject_into_summary(original_summary)
    enhanced_skills  = injector.inject_into_skills(original_skills)

    # Full combined audit report for logging
    injector.save_audit_report("build_logs/ats_audit_2026-06-12.txt",
                               combined_text=resume_text + cover_text)

CLI (audit only — does not modify documents):

    python ats_injector.py --jd path/to/jd.txt --resume path/to/resume.docx --cover path/to/cover.docx --profile siu-fraud

Constraints (always enforced):
    - Never injects a term that would require overclaiming a skill Troy does not have
    - Never injects terms from VOICE_STANDARD.md Layer 1 banned list
    - Never injects terms the PTSD-scope hard block covers
    - Injection is case-preserving: matches the casing of the first occurrence in the JD
    - Terms injected into resume bullets are always placed inside complete sentences, never appended raw
    - Coverage target: 85%+ of extracted JD terms. Terms below the floor are flagged in the audit report.
"""

from __future__ import annotations

import re
import sys
import argparse
from collections import Counter
from pathlib import Path
from typing import Optional

# -- Optional python-docx for .docx audit support ----------------------------
try:
    from docx import Document as _DocxDocument
    _DOCX_AVAILABLE = True
except ImportError:
    _DOCX_AVAILABLE = False


# -- LAYER 1 HARD-BANNED TERMS (from VOICE_STANDARD.md) ----------------------
# These must never appear in any injected text regardless of JD frequency.
LAYER1_BANNED = {
    "leveraged", "harnessed", "spearheaded", "championed", "optimized",
    "streamlined", "transformed", "delivered value", "drove outcomes",
    "empowered", "elevated", "unlocked", "seamlessly",
    "in today's environment", "at the end of the day", "needless to say",
    "fundamentally", "ultimately", "ramping on",
    "i am excited", "i am thrilled", "i am eager", "i look forward to discussing",
    "deep dive", "actionable intelligence", "rockstar", "ninja", "guru",
    "thought leadership", "passionate practitioner", "trusted advisor",
    "boots on the ground",
}

# -- PTSD-SCOPE HARD BLOCK ----------------------------------------------------
PTSD_BLOCKED = {
    "homicide", "death investigation", "lethal force", "sexual assault",
    "criminal sexual conduct", "human trafficking",
}

# -- NOISE WORDS TO IGNORE when extracting JD keywords -----------------------
STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "this", "that",
    "these", "those", "as", "if", "then", "than", "when", "where", "which",
    "who", "whom", "whose", "what", "how", "all", "any", "each", "every",
    "both", "few", "more", "most", "other", "some", "such", "into", "up",
    "out", "about", "after", "before", "during", "between", "through",
    "our", "your", "their", "its", "we", "you", "they", "it", "he", "she",
    "i", "me", "my", "us", "him", "her", "his", "not", "no", "nor",
    "also", "well", "new", "able", "across", "within",
}

# -- PROFILE-SPECIFIC SKIP TERMS (overclaim guard) ----------------------------
# Terms that appear in JDs but should not be injected because Troy cannot
# legitimately claim them without context.
#
# IMPORTANT — Tableau disambiguation:
#   DO NOT block the bare word "tableau". Troy has legitimate hands-on experience
#   with Tableau write blockers (forensic hardware used in digital evidence
#   collection). The overclaim is Tableau Desktop / Tableau Server (data
#   visualization software). Block the specific product names only.
OVERCLAIM_SKIP = {
    "siu-fraud": {
        "salesforce",
        "tableau desktop",    # Tableau data viz software — NOT the same as Tableau write blockers
        "tableau server",     # Tableau data viz software — NOT the same as Tableau write blockers
        "tableau software",   # Tableau data viz software — NOT the same as Tableau write blockers
        "alteryx",
        "sql",
        "python advanced",
        "machine learning",
        "ai model",
        "underwriting authority",
    },
    "vendor-solutions": {
        "recorded statement", "euo", "claim file", "nicb",
    },
    "analyst-intelligence": {
        "f3ead", "palantir", "recorded statement", "euo",
    },
}


def extract_jd_keywords(jd_text: str, min_length: int = 4, top_n: int = 80) -> list[str]:
    """
    Extract meaningful single-word and two-word phrase keywords from a job description.
    Returns a ranked list, most frequent / most distinctive first.
    """
    text_lower = jd_text.lower()

    # Extract bigrams first (two-word phrases are higher signal)
    words = re.findall(r"[a-z]+", text_lower)
    bigrams = [
        f"{words[i]} {words[i+1]}"
        for i in range(len(words) - 1)
        if words[i] not in STOP_WORDS
        and words[i+1] not in STOP_WORDS
        and len(words[i]) >= 3
        and len(words[i+1]) >= 3
    ]

    bigram_counts = Counter(bigrams)
    unigrams = [w for w in words if w not in STOP_WORDS and len(w) >= min_length]
    unigram_counts = Counter(unigrams)

    # Combine: bigrams weighted 2x
    combined: dict[str, float] = {}
    for bg, count in bigram_counts.items():
        combined[bg] = count * 2.0
    for ug, count in unigram_counts.items():
        if not any(ug in bg for bg in combined):
            combined[ug] = float(count)

    # Remove banned / blocked terms
    filtered = {
        term: score for term, score in combined.items()
        if term not in LAYER1_BANNED
        and term not in PTSD_BLOCKED
        and not any(blocked in term for blocked in PTSD_BLOCKED)
    }

    ranked = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    return [term for term, _ in ranked[:top_n]]


def check_coverage(keywords: list[str], document_text: str) -> tuple[list[str], list[str]]:
    """Return (found_terms, missing_terms)."""
    text_lower = document_text.lower()
    found = [kw for kw in keywords if kw.lower() in text_lower]
    missing = [kw for kw in keywords if kw.lower() not in text_lower]
    return found, missing


class ATSInjector:
    """
    Main ATS keyword injection engine.

    Parameters
    ----------
    jd_text : str
        Raw job description text.
    profile : str
        One of 'siu-fraud', 'vendor-solutions', 'analyst-intelligence'.
    custom_keywords : list[str] | None
        Optional manually curated keyword list. If provided, skips auto-extraction.
    coverage_floor : float
        Target coverage ratio (default 0.85 = 85%).
    """

    def __init__(
        self,
        jd_text: str,
        profile: str = "vendor-solutions",
        custom_keywords: Optional[list[str]] = None,
        coverage_floor: float = 0.85,
    ):
        self.jd_text = jd_text
        self.profile = profile
        self.coverage_floor = coverage_floor
        self._skip = OVERCLAIM_SKIP.get(profile, set())

        if custom_keywords:
            self.keywords = [kw for kw in custom_keywords if kw.lower() not in self._skip]
        else:
            raw = extract_jd_keywords(jd_text)
            self.keywords = [kw for kw in raw if kw.lower() not in self._skip]

    def audit(self, document_text: str) -> dict:
        """
        Audit the combined document text against extracted keywords.

        Returns a dict with keys:
            found, missing, coverage_pct, meets_floor, keywords_total
        """
        found, missing = check_coverage(self.keywords, document_text)
        coverage = len(found) / len(self.keywords) if self.keywords else 1.0
        return {
            "found": found,
            "missing": missing,
            "coverage_pct": round(coverage * 100, 1),
            "meets_floor": coverage >= self.coverage_floor,
            "keywords_total": len(self.keywords),
        }

    def save_audit_report(self, output_path: str, combined_text: str) -> None:
        """Write a plain-text audit report to output_path."""
        result = self.audit(combined_text)
        lines = [
            "ATS Audit Report",
            f"Profile: {self.profile}",
            f"Coverage: {result['coverage_pct']}% ({len(result['found'])}/{result['keywords_total']})",
            f"Floor target: {int(self.coverage_floor * 100)}%",
            f"Meets floor: {'YES' if result['meets_floor'] else 'NO -- ACTION REQUIRED'}",
            "",
            "FOUND TERMS:",
        ]
        for t in sorted(result["found"]):
            lines.append(f"  + {t}")
        lines.append("")
        lines.append("MISSING TERMS (review for injection or flag as overclaim):")
        for t in sorted(result["missing"]):
            lines.append(f"  - {t}")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text("\n".join(lines))
        print(f"Audit report written to {output_path}")

    def inject_into_summary(self, original_summary: str) -> str:
        """
        Attempt to naturally weave missing high-priority keywords into a
        resume summary paragraph. Returns the modified string.

        This is a lightweight pattern-based injector. For complex rewrites,
        the full build scripts should be used with the keyword list as guidance.
        """
        result = original_summary
        found, missing = check_coverage(self.keywords[:30], original_summary)

        substitutions = {
            # siu-fraud substitutions
            "fraud detection": ("fraud investigations", "fraud detection and investigation"),
            "fraud prevention": ("fraud investigations", "fraud detection, prevention, and investigation"),
            "fraud analysis": ("case packages", "case packages, fraud analysis"),
            "fraud reporting": ("executive-level reports", "executive-level fraud reporting"),
            "red flag": ("case theories", "red flag identification and case theories"),
            "data mining": ("financial analysis", "financial analysis and data mining"),
            "certified fraud examiner": ("CFE", "Certified Fraud Examiner (CFE)"),
            "compliance": ("court-admissible", "compliance-grade, court-admissible"),
            "district attorney": ("county attorney", "county attorney and district attorney"),
            # vendor-solutions substitutions
            "end-user workflow": ("investigative tools", "end-user workflow for investigative tools"),
            "partner agency": ("multi-agency", "multi-agency and partner agency"),
            "workshop": ("training", "training workshops"),
            # analyst-intelligence substitutions
            "link analysis": ("OSINT", "OSINT and link analysis"),
            "pattern recognition": ("financial analysis", "financial analysis and pattern recognition"),
            "written intelligence": ("case reports", "written intelligence products and case reports"),
        }

        for term in missing:
            if term in substitutions:
                old, new = substitutions[term]
                if old.lower() in result.lower():
                    result = re.sub(re.escape(old), new, result, count=1, flags=re.IGNORECASE)

        return result

    def inject_into_skills(self, original_skills: str) -> str:
        """
        Append missing high-priority terms to a skills / strengths section string.
        Only appends terms that are demonstrably part of Troy's actual skill set.
        """
        safe_append_terms = {
            "siu-fraud": [
                "fraud detection", "fraud prevention", "fraud analysis",
                "fraud reporting", "fraud trends", "fraud training",
                "fraud database", "red flag", "data mining",
                "police report", "witness statement", "confession",
                "prosecution", "civil referral", "criminal referral",
                "deposition preparation", "outside counsel coordination",
                "certified fraud examiner", "multi-state investigation",
                "dealership fraud", "originations review",
            ],
            "vendor-solutions": [
                "demo delivery", "workshop facilitation", "end-user training",
                "RFP response", "partner agency coordination", "field testing",
            ],
            "analyst-intelligence": [
                "link analysis", "pattern recognition", "OSINT",
                "structured analytic technique", "written intelligence products",
                "SAR familiarity", "fraud typology",
            ],
        }
        _, missing = check_coverage(self.keywords, original_skills)
        appendable = safe_append_terms.get(self.profile, [])
        additions = [t for t in missing if t.lower() in [a.lower() for a in appendable]]
        if additions:
            return original_skills.rstrip() + "  |  " + "  |  ".join(additions)
        return original_skills

    @staticmethod
    def load_docx_text(docx_path: str) -> str:
        """Extract plain text from a .docx file."""
        if not _DOCX_AVAILABLE:
            raise ImportError(
                "python-docx is required to read .docx files: pip install python-docx"
            )
        doc = _DocxDocument(docx_path)
        return " ".join(p.text for p in doc.paragraphs)


# -- CLI entry point ----------------------------------------------------------
def _cli():
    parser = argparse.ArgumentParser(
        description="ATS keyword audit for Troy Hokanson documents"
    )
    parser.add_argument("--jd", required=True, help="Path to job description .txt file")
    parser.add_argument("--resume", required=False, help="Path to resume .docx file")
    parser.add_argument("--cover", required=False, help="Path to cover letter .docx file")
    parser.add_argument(
        "--profile",
        default="vendor-solutions",
        choices=["vendor-solutions", "siu-fraud", "analyst-intelligence"],
        help="Voice profile (default: vendor-solutions)",
    )
    parser.add_argument(
        "--floor",
        type=float,
        default=0.85,
        help="Coverage floor threshold (default: 0.85)",
    )
    parser.add_argument("--output", default=None, help="Path to save audit report .txt")
    args = parser.parse_args()

    jd_text = Path(args.jd).read_text()
    injector = ATSInjector(
        jd_text=jd_text, profile=args.profile, coverage_floor=args.floor
    )

    combined = ""
    if args.resume:
        combined += ATSInjector.load_docx_text(args.resume) + " "
    if args.cover:
        combined += ATSInjector.load_docx_text(args.cover)

    result = injector.audit(combined)
    print(
        f"Coverage: {result['coverage_pct']}% "
        f"({len(result['found'])}/{result['keywords_total']} terms)"
    )
    print(f"Meets {int(args.floor * 100)}% floor: {'YES' if result['meets_floor'] else 'NO'}")
    print(f"Missing: {result['missing']}")

    if args.output:
        injector.save_audit_report(args.output, combined)

    sys.exit(0 if result["meets_floor"] else 1)


if __name__ == "__main__":
    _cli()

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_CAREER_FILES = (
    ROOT / "PROFILES.md",
    ROOT / "anti_ai_scan.py",
    ROOT / "specs" / "trm_all_source_investigator.py",
)

STALE_CLAIMS = (
    re.compile(r"\bnine years in the U\.S\. Army\b", re.IGNORECASE),
    re.compile(r"\bnine years of U\.S\. Army service\b", re.IGNORECASE),
    re.compile(
        r"\bsix years (?:on|assigned to) (?:the )?(?:Dakota County )?"
        r"Electronic Crimes Task Force\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b19 years adjunct teaching\b", re.IGNORECASE),
)


def test_active_career_examples_match_locked_duration_constants():
    violations = []
    for path in ACTIVE_CAREER_FILES:
        source = path.read_text(encoding="utf-8")
        for pattern in STALE_CLAIMS:
            if pattern.search(source):
                violations.append(f"{path.relative_to(ROOT)}: {pattern.pattern}")

    assert not violations, "Stale career-duration claims: " + "; ".join(violations)


def test_active_profiles_include_locked_duration_values():
    profiles = (ROOT / "PROFILES.md").read_text(encoding="utf-8")
    trm_spec = (ROOT / "specs" / "trm_all_source_investigator.py").read_text(
        encoding="utf-8"
    )
    scanner = (ROOT / "anti_ai_scan.py").read_text(encoding="utf-8")

    assert "8 years 3 months in the U.S. Army" in profiles
    assert "4.5 years assigned to the Dakota County Electronic Crimes Task Force" in trm_spec
    assert "18 years adjunct teaching" in scanner

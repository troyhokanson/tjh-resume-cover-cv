from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_CAREER_FILES = (
    ROOT / "VOICE_STANDARD.md",
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
    re.compile(r"\b25 years? as (?:a )?(?:Minnesota )?detective\b", re.IGNORECASE),
    re.compile(r"\b54 years? old\b", re.IGNORECASE),
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

    assert "prior U.S. Army service" in profiles
    assert "4.5 years assigned to the Dakota County Electronic Crimes Task Force" in trm_spec
    assert "18 years adjunct teaching" in scanner


def test_scanner_blocks_known_fact_drift_and_bec_conflation():
    from anti_ai_scan import scan_text

    detective = scan_text("I spent 25 years as a Minnesota detective.", doc_type="cover")
    assert any("total law-enforcement service" in item for item in detective)

    military = scan_text("I completed nine years of U.S. Army service.", doc_type="cover")
    assert any("exact verified duration" in item for item in military)

    bec = scan_text(
        "The Business Email Compromise case produced a 15-year federal sentence.",
        doc_type="cover",
    )
    assert any("BEC outcome conflation" in item for item in bec)

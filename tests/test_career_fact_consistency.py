from pathlib import Path
import json
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


def test_scanner_uses_private_case_denylist_without_public_values(monkeypatch):
    from anti_ai_scan import scan_text

    monkeypatch.setenv("TROY_PRIVATE_CASE_DENYLIST", "Example Private Subject")
    private_name = scan_text(
        "The investigation concerned Example Private Subject.", doc_type="cover"
    )
    named_judge = scan_text(
        "Judge Example Privateperson denied the motion.", doc_type="cover"
    )

    assert any("private case-denylist term" in item for item in private_name)
    assert any("Named judicial officer" in item for item in named_judge)
    assert all("Example Private Subject" not in item for item in private_name)


def test_current_chronology_and_investigative_tenure_are_locked():
    career = (ROOT / "CAREER_CONSTANTS.md").read_text(encoding="utf-8")

    assert "### Independent Professional" in career
    assert "Dates:      April 2026 - Present" in career
    assert "Dates:      June 2024 - June 2026" in career
    assert "license ended June 30, 2026" in career
    assert "6.5 years (March 2010 - May 2011 and September 2016 - December 2021)" in career
    assert "5.5 years (September 2016 - December 2021)" in career
    assert "6.5 years of direct investigative use across both investigative rotations" in career

    for stale in ("Referral-Only", "referral-only", "June 2024 - March 2026"):
        assert stale not in career


def test_skills_constants_exclude_unverified_capabilities():
    skills = (ROOT / "SKILLS_CONSTANTS.md").read_text(encoding="utf-8").lower()

    assert "i2 analyst" not in skills
    assert "dark web investigation" not in skills
    assert "digital-evidence preservation" in skills
    assert "public-record research" in skills


def test_credentials_catalog_uses_verified_ccci_issue_date():
    catalog = json.loads(
        (ROOT / "skills" / "troy-credentials-library" / "credentials_catalog.json")
        .read_text(encoding="utf-8")
    )
    ccci = next(
        item
        for item in catalog["certifications"]["digital_forensics"]
        if item["id"] == "DF-001"
    )

    assert ccci["credential_id"] == "4793"
    assert ccci["month_year"] == "01/2023"
    assert "year" not in ccci

    for quote in catalog["commendation_quotes"]:
        assert "case_file" not in quote
        assert "nominator" not in quote


def test_general_online_resume_uses_current_reusable_facts():
    resume = (
        ROOT / "applications" / "2026-08-17_general_online_resume" / "resume.md"
    ).read_text(encoding="utf-8")

    assert "### Independent Professional" in resume
    assert "Remote | April 2026 - Present" in resume
    assert "South Metro MN | June 2024 - June 2026" in resume
    assert "6.5 years of direct investigative use across both investigative rotations" in resume
    assert "ACFE application approved and examination preparation in progress" in resume
    assert "Referral-Only" not in resume
    assert "June 2024 - March 2026" not in resume


def test_public_case_bank_enforces_sanitized_external_use():
    case_bank = (ROOT / "CASE_BANK.md").read_text(encoding="utf-8")
    lower = case_bank.lower()

    assert "**External-use gate:**" in case_bank
    assert "an executed sentence of up to 78 months" in case_bank
    assert "concurrent executed sentences of 36, 48, and 78 months" not in case_bank
    assert "Control #" not in case_bank
    assert "Case No." not in case_bank

    for blocked in (
        "homicide",
        "death investigation",
        "lethal force",
        "sexual assault",
        "criminal sexual conduct",
        "human trafficking",
        "csam",
        "child sexual",
        "child abuse",
        "child exploitation",
        "child-exploitation",
        "icac",
    ):
        assert blocked not in lower

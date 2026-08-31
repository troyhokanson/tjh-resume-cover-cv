"""
Unit tests for anti_ai_scan.scan_text.

Run from the repo root (cloned directly):
    python -m pytest tests/ -v

Run from the workspace root (repo symlinked as templates/):
    python -m pytest templates/tests/ -v
"""

import sys
import os
import pytest

# Allow import when run directly from the repo root (not via templates/ symlink)
_here = os.path.dirname(os.path.abspath(__file__))
_repo_root = os.path.dirname(_here)
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

from anti_ai_scan import scan_text, FailedScan, scan_pdf


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _resume(body: str) -> list[str]:
    return scan_text(body, doc_type="resume")


def _cover(body: str) -> list[str]:
    return scan_text(body, doc_type="cover")


def _clean_resume() -> str:
    return (
        "Performed write-blocked acquisition and FTK/IEF analysis of a computer "
        "in a wire-fraud matter and identified responsive artifacts."
    )


def _clean_cover() -> str:
    return (
        "Twenty-five years in public service taught me that fraud erodes the "
        "trust between people and the systems designed to protect them. "
        "Official Minnesota records separately confirm that a broader matter "
        "involved more than $360,000 across three victims.\n\nRespectfully,"
    )


# ---------------------------------------------------------------------------
# Pass cases — clean text must produce zero violations
# ---------------------------------------------------------------------------

class TestCleanTextPasses:
    def test_clean_resume_passes(self):
        assert _resume(_clean_resume()) == []

    def test_clean_cover_passes(self):
        assert _cover(_clean_cover()) == []

    def test_bio_no_semicolon_passes(self):
        body = "Troy Hokanson is a medically retired Minnesota law-enforcement officer."
        assert scan_text(body, doc_type="bio") == []

    def test_attributed_public_wire_fraud_outcome_passes(self):
        body = (
            "Official Minnesota records separately confirm that the broader wire-fraud "
            "matter involved more than $360,000 across three victims, two felony "
            "convictions, five years of probation, and $295,704.11 in restitution."
        )
        assert _resume(body) == []

    def test_unsupported_bec_leadership_is_blocked(self):
        violations = _resume(
            "Led a multi-victim Business Email Compromise investigation to conviction."
        )
        assert any("Unsupported BEC personal-role claim" in item for item in violations)


# ---------------------------------------------------------------------------
# Punctuation rules
# ---------------------------------------------------------------------------

class TestPunctuationRules:
    def test_em_dash_flagged(self):
        violations = _resume("He closed the case\u2014first in the unit.")
        assert any("Em dash" in v for v in violations)

    def test_en_dash_flagged(self):
        violations = _resume("He worked 2019\u20132021 on the task force.")
        assert any("En dash" in v for v in violations)

    def test_exclamation_flagged(self):
        violations = _resume("Outstanding results!")
        assert any("Exclamation" in v for v in violations)

    def test_ellipsis_flagged(self):
        violations = _resume("The case was handled...eventually.")
        assert any("Ellipsis" in v for v in violations)

    def test_unicode_ellipsis_flagged(self):
        violations = _resume("The case was handled\u2026eventually.")
        assert any("Ellipsis" in v for v in violations)

    def test_curly_quotes_flagged(self):
        violations = _resume("\u201cGreat work\u201d on the investigation.")
        assert any("Curly" in v for v in violations)

    def test_semicolon_in_cover_flagged(self):
        body = _clean_cover().replace("\n\nRespectfully,", "; I am done.\n\nRespectfully,")
        violations = _cover(body)
        assert any("Semicolon" in v for v in violations)

    def test_semicolon_in_resume_allowed(self):
        body = _clean_resume() + " Cellebrite UFED; Magnet AXIOM; FTK."
        assert not any("Semicolon" in v for v in _resume(body))


# ---------------------------------------------------------------------------
# Forbidden phrase detection
# ---------------------------------------------------------------------------

class TestForbiddenPhrases:
    @pytest.mark.parametrize("phrase", [
        "leveraged", "harnessed", "spearheaded", "championed",
        "passionate about", "dynamic", "synergy", "robust",
        "comprehensive", "cutting-edge", "results-driven",
        "detail-oriented", "proven track record",
        "in today's environment", "in conclusion", "to summarize",
        "moving forward", "going forward", "touch base", "circle back",
        "impactful", "game-changer", "paradigm shift",
        "holistic approach", "deep dive", "bandwidth",
    ])
    def test_core_forbidden_phrase(self, phrase):
        body = f"The candidate {phrase} the program."
        violations = _resume(body)
        assert any(phrase.lower() in v.lower() for v in violations), \
            f"Expected '{phrase}' to be flagged but got: {violations}"

    @pytest.mark.parametrize("phrase", [
        "utilize", "utilized", "utilizing", "utilization",
        "fundamentally", "in order to", "myriad of", "plethora",
        "delve into", "delving", "tapestry",
        "navigate the complexities", "ever-evolving", "ever-changing",
        "seamlessly", "elevate", "unlock", "world-class",
        "ramping on",
    ])
    def test_extra_forbidden_phrase(self, phrase):
        body = f"The candidate will {phrase} existing processes."
        violations = _resume(body)
        assert any(phrase.lower() in v.lower() for v in violations), \
            f"Expected '{phrase}' to be flagged but got: {violations}"

    def test_ai_opener_pattern(self):
        violations = _cover("As a Detective, I bring twenty years of experience.")
        assert any("As a" in v for v in violations)


# ---------------------------------------------------------------------------
# Cover-letter specific rules
# ---------------------------------------------------------------------------

class TestCoverLetterRules:
    @pytest.mark.parametrize("closing", ["Respectfully,", "Sincerely,", "Thank you,"])
    def test_professional_closing_is_adaptive(self, closing):
        body = _clean_cover().replace("Respectfully,", closing)
        assert _cover(body) == []

    def test_natural_contractions_are_allowed(self):
        body = (
            "I'm interested because the work fits what I've done. "
            "I'd welcome a practical conversation about the role.\n\nSincerely,"
        )
        assert not any("contractions" in v for v in _cover(body))

    def test_formulaic_look_forward_phrase_remains_flagged(self):
        body = _clean_cover() + " I look forward to discussing the role."
        violations = _cover(body)
        assert any("look forward" in v.lower() for v in violations)

# ---------------------------------------------------------------------------
# Resume / CV contraction rules
# ---------------------------------------------------------------------------

class TestResumeContractions:
    def test_contractions_forbidden_in_resume(self):
        body = "I'm a medically retired detective with 25 years of service."
        violations = _resume(body)
        assert any("contractions" in v for v in violations)

    def test_possessive_not_flagged_as_contraction(self):
        body = "Earned a Master's degree in Police Leadership with a 3.94 GPA."
        violations = _resume(body)
        assert not any("contractions" in v for v in violations)


# ---------------------------------------------------------------------------
# PTSD-scope guard
# ---------------------------------------------------------------------------

class TestPtsdScopeGuard:
    @pytest.mark.parametrize("term", [
        "CSAM", "homicide", "lethal force", "sexual assault",
        "human trafficking",
    ])
    def test_ptsd_term_flagged(self, term):
        violations = _resume(f"The investigation involved {term} cases.")
        assert any("PTSD-scope" in v for v in violations)


# ---------------------------------------------------------------------------
# Role-adaptive profile support
# ---------------------------------------------------------------------------

class TestRoleAdaptiveProfiles:
    @pytest.mark.parametrize("profile", [
        "adaptive", "vendor-solutions", "siu-fraud",
        "analyst-intelligence", "corporate-security-investigations",
        "customer-success", "technical-account-management", "dfir-cyber",
    ])
    def test_supported_profile_accepts_clean_text(self, profile):
        assert scan_text("Documented verified outcomes.", profile=profile) == []

    @pytest.mark.parametrize("phrase", [
        "optimized the onboarding workflow",
        "streamlined the escalation process",
        "facilitated customer training",
        "implemented solutions for partner agencies",
        "drove outcomes through careful follow-up",
    ])
    def test_legitimate_industry_language_is_not_globally_blocked(self, phrase):
        assert _resume(phrase) == []

# ---------------------------------------------------------------------------
# POST / peace-officer licensing privacy guard
# ---------------------------------------------------------------------------

class TestPostLicensePrivacyGuard:
    @pytest.mark.parametrize("phrase", [
        "Minnesota Peace Officer License No. 54321",
        "MN Peace Officer POST Certification, License No. 54321",
        "POST Board Certified Peace Officer, License No. 54321",
        "POST # 54321",
    ])
    def test_post_licensing_identifier_flagged(self, phrase):
        violations = _resume(f"Professional Credentials: {phrase}.")
        assert any("licensing identifier" in v for v in violations)


# ---------------------------------------------------------------------------
# VEVRAA guard
# ---------------------------------------------------------------------------

class TestVevraaGuard:
    def test_vevraa_flagged(self):
        violations = _resume("He is a VEVRAA-covered veteran.")
        assert any("VEVRAA" in v for v in violations)

    def test_protected_veteran_flagged(self):
        violations = _resume("He is a protected veteran.")
        assert any("protected veteran" in v.lower() for v in violations)


# ---------------------------------------------------------------------------
# scan_pdf — file-not-found guard
# ---------------------------------------------------------------------------

class TestScanPdfFileGuard:
    def test_missing_file_raises(self):
        with pytest.raises(FileNotFoundError):
            scan_pdf("/nonexistent/path/resume.pdf")

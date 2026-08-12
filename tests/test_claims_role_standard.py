from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_claims_standard_is_linked_from_profile_selector():
    selector = (ROOT / "PROFILE_SELECTOR.md").read_text(encoding="utf-8")
    assert "CLAIMS_ROLE_TARGETING_STANDARD.md" in selector


def test_claims_standard_preserves_transferable_experience_boundaries():
    standard = (ROOT / "CLAIMS_ROLE_TARGETING_STANDARD.md").read_text(
        encoding="utf-8"
    )
    required_guardrails = (
        "They are not evidence of carrier claim ownership.",
        "never claim:",
        "coverage interpretation or coverage decisions",
        "an active adjuster license",
        "never call Troy an experienced adjuster",
        "classification: Direct, Transferable, or Reject",
    )
    for guardrail in required_guardrails:
        assert guardrail in standard

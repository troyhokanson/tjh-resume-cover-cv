import copy

import pytest

from application_quality import (
    GateFailure,
    METRIC_PATTERN,
    build_variation_profile,
    parse_case_bank,
    select_required_cases,
    select_required_training,
    verify_application_draft,
)


def _sample_case_bank() -> str:
    return """
## Case 1 — BEC / Shell Companies
**Victim Loss:** Verified at more than $360,000 across multiple victims
**TAGS:** `BEC` `wire-fraud` `siu-fraud` `analyst-intelligence`

## Case 2 — Occupational Fraud
**Loss Amount:** Approximately $80,000 in unauthorized charges
**TAGS:** `occupational-fraud` `siu-fraud` `analyst-intelligence`

## Program Entry — Probation Liaison Officer Program
**Documented Outcomes:** launched in 2012
**TAGS:** `probation-coordination` `vendor-solutions` `siu-fraud`

## Case Template — Placeholder
**TAGS:** [Select from Tag Taxonomy above. Add new tags to taxonomy first if needed.]
"""


def _sample_catalog() -> dict:
    return {
        "certifications": {
            "digital_forensics": [
                {
                    "id": "DF-001",
                    "name": "NW3C Certified Cyber Crime Investigator (CCCI)",
                    "ptsd_safe": True,
                    "tier": "headline",
                    "profiles": ["siu-fraud", "vendor-solutions"],
                },
                {
                    "id": "DF-002",
                    "name": "FBI CAST Basic Historical Cell Site Analysis",
                    "ptsd_safe": True,
                    "tier": "headline",
                    "profiles": ["siu-fraud"],
                },
            ],
            "investigations": [
                {
                    "id": "INV-001",
                    "name": "Financial Crimes Investigation",
                    "ptsd_safe": True,
                    "tier": "supporting",
                    "profiles": ["siu-fraud"],
                },
                {
                    "id": "INV-002",
                    "name": "Suppressed Example",
                    "ptsd_safe": False,
                    "tier": "suppressed",
                    "profiles": ["siu-fraud"],
                },
            ],
        },
        "training_hours_total": {
            "documented_hours": 1238.75,
        },
    }


def _variation() -> dict:
    return build_variation_profile("Fraud Investigator", "Contoso", "2026-07-03")


class TestCaseSelectionGates:
    def test_metric_pattern_detects_concrete_values(self):
        assert METRIC_PATTERN.search("verified losses exceeded $360,000")
        assert METRIC_PATTERN.search("worked with 10 partner agencies")
        assert METRIC_PATTERN.search("served 10 years probation")

    def test_case_gate_requires_two_qualified_cases(self):
        case_bank = parse_case_bank(_sample_case_bank())
        trimmed = [case_bank[0]]

        with pytest.raises(GateFailure):
            select_required_cases(trimmed, "siu-fraud", "business email compromise and fraud", _variation())

    def test_case_gate_selects_only_profile_and_metric_matched_cases(self):
        case_bank = parse_case_bank(_sample_case_bank())
        result = select_required_cases(case_bank, "siu-fraud", "occupational fraud and bec", _variation())

        assert result["selected_count"] >= 2
        assert all(case["has_metric"] for case in result["required_cases"])
        assert all("siu-fraud" in case["tags"] for case in result["required_cases"])


class TestTrainingSelectionGates:
    def test_training_gate_requires_three_relevant_credentials_or_equivalent(self):
        catalog = _sample_catalog()
        result = select_required_training(catalog, "siu-fraud", "fraud investigation and analysis", minimum_count=3)

        assert result["selected_count"] >= 3
        assert all(item["tier"] in {"headline", "supporting"} for item in result["required_training"])

    def test_training_gate_fails_when_relevant_credentials_insufficient(self):
        catalog = _sample_catalog()
        catalog["certifications"]["investigations"] = []
        catalog["training_hours_total"]["documented_hours"] = 10

        with pytest.raises(GateFailure):
            select_required_training(catalog, "siu-fraud", "fraud investigation and analysis", minimum_count=3)


class TestDraftVerifier:
    def test_verifier_enforces_case_stats_and_training_match(self):
        manifest = {
            "profile": "siu-fraud",
            "required_cases": [
                {
                    "label": "Case 1 — BEC / Shell Companies",
                    "match_terms": ["bec", "shell companies"],
                }
            ],
            "required_training": [
                {"name": "NW3C Certified Cyber Crime Investigator (CCCI)"},
            ],
        }

        resume = "I led BEC cases but removed all numbers from this sentence."
        cover = "Respectfully,"
        result = verify_application_draft(manifest, resume, cover)

        assert not result["passed"]
        assert "Case 1 — BEC / Shell Companies" in result["case_metric_failures"]
        assert "NW3C Certified Cyber Crime Investigator (CCCI)" in result["missing_training"]

    def test_verifier_passes_when_manifest_requirements_are_present(self):
        manifest = {
            "profile": "siu-fraud",
            "required_cases": [
                {
                    "label": "Case 1 — BEC / Shell Companies",
                    "match_terms": ["bec"],
                },
                {
                    "label": "Case 2 — Occupational Fraud",
                    "match_terms": ["occupational fraud"],
                },
            ],
            "required_training": [
                {"name": "NW3C Certified Cyber Crime Investigator (CCCI)"},
                {"name": "FBI CAST Basic Historical Cell Site Analysis"},
            ],
        }

        resume = (
            "Led a BEC case with verified losses of $360,000 and a felony conviction. "
            "Completed NW3C Certified Cyber Crime Investigator (CCCI)."
        )
        cover = (
            "In an occupational fraud case, losses reached $80,000 and the matter closed with restitution. "
            "I also completed FBI CAST Basic Historical Cell Site Analysis.\n\nRespectfully,"
        )

        result = verify_application_draft(manifest, resume, cover)
        assert result["passed"]


class TestVariationProfile:
    def test_variation_profile_is_deterministic(self):
        first = build_variation_profile("Fraud Investigator", "Contoso", "2026-07-03")
        second = build_variation_profile("Fraud Investigator", "Contoso", "2026-07-03")
        assert first == second

    def test_variation_profile_changes_with_seed_input(self):
        base = build_variation_profile("Fraud Investigator", "Contoso", "2026-07-03")
        different = build_variation_profile("Fraud Investigator", "Fabrikam", "2026-07-03")
        assert base != different

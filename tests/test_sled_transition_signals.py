"""Regression tests for the SLED transition-signal calibration."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from validate_sled_transition_signals import validate_config


CONFIG_PATH = REPO_ROOT / "standards" / "sled_transition_signal_matrix.json"


def load_config():
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def test_valid_configuration_passes():
    assert validate_config(load_config()) == []


def test_protected_traits_can_never_add_points():
    data = copy.deepcopy(load_config())
    data["protected_data_policy"]["points"] = 1
    data["caps"]["protected_trait_total"] = 1
    errors = validate_config(data)
    assert any("protected traits" in error for error in errors)
    assert any("protected_trait_total" in error for error in errors)


def test_end_user_evidence_keeps_explicit_claim_boundary():
    data = copy.deepcopy(load_config())
    data["candidate_signals"]["cad_rms_end_user"]["claim_boundary"] = (
        "Strong public-safety software experience."
    )
    errors = validate_config(data)
    assert any("cad_rms_end_user" in error for error in errors)


def test_military_bonus_is_capped():
    data = copy.deepcopy(load_config())
    data["caps"]["military_signal_total"] = 4
    errors = validate_config(data)
    assert any("military_signal_total" in error for error in errors)


def test_role_weight_cannot_exceed_scale():
    data = copy.deepcopy(load_config())
    data["role_family_weights"]["field_deployment"]["combat_arms_11b_19k"] = 5
    errors = validate_config(data)
    assert any("field_deployment.combat_arms_11b_19k" in error for error in errors)


def test_evidence_tiers_require_public_sources():
    data = copy.deepcopy(load_config())
    data["employer_evidence"][0]["source_urls"] = []
    errors = validate_config(data)
    assert any("requires at least one public source URL" in error for error in errors)


def test_locked_army_duration_cannot_drift():
    data = copy.deepcopy(load_config())
    data["candidate_signals"]["us_army_veteran"]["verified_evidence"] = (
        "U.S. Army veteran"
    )
    errors = validate_config(data)
    assert any("8 years 3 months" in error for error in errors)

#!/usr/bin/env python3
"""Validate the SLED transition-signal calibration file.

This validator protects the career system from three failure modes:
1. protected traits entering job-fit scoring;
2. military or agency-user experience being inflated into unsupported expertise; and
3. employer-pathway tiers being assigned without public evidence.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_SIGNALS = {
    "former_sworn_public_safety",
    "detective_investigator",
    "crime_scene_unit",
    "digital_forensic_examiner",
    "adult_instructor_and_fto",
    "agency_side_technology_project",
    "cad_rms_end_user",
    "axon_connected_workflow_end_user",
    "us_army_veteran",
    "military_police_95b",
    "combat_arms_11b_19k",
    "motor_transport_88m",
}

REQUIRED_MAJOR_GAPS = {
    "formal_saas_implementation_years",
    "quota_carrying_sales",
    "deep_sql_api_or_software_engineering",
    "platform_administration_or_configuration",
    "uas_or_part_107",
}

END_USER_SIGNALS = {
    "cad_rms_end_user",
    "axon_connected_workflow_end_user",
}


def _load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_config(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if data.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")

    policy = data.get("protected_data_policy", {})
    if policy.get("never_score") is not True:
        errors.append("protected_data_policy.never_score must be true")
    if policy.get("points") != 0:
        errors.append("protected traits must contribute exactly zero points")
    if not policy.get("storage_rule"):
        errors.append("protected-data storage rule is required")

    caps = data.get("caps", {})
    if caps.get("protected_trait_total") != 0:
        errors.append("protected_trait_total cap must be zero")
    if not isinstance(caps.get("military_signal_total"), int) or caps.get(
        "military_signal_total", 99
    ) > 3:
        errors.append("military_signal_total cap must be an integer no greater than 3")
    if not isinstance(caps.get("transition_signal_total"), int) or caps.get(
        "transition_signal_total", 99
    ) > 12:
        errors.append("transition_signal_total cap must be an integer no greater than 12")

    signals = data.get("candidate_signals", {})
    missing = sorted(REQUIRED_SIGNALS - set(signals))
    if missing:
        errors.append(f"missing candidate signals: {', '.join(missing)}")

    army_text = signals.get("us_army_veteran", {}).get("verified_evidence", "")
    if "8 years 3 months" not in army_text:
        errors.append("Army service must use the locked 8 years 3 months figure")

    for key, signal in signals.items():
        if not signal.get("evidence_status"):
            errors.append(f"{key} is missing evidence_status")
        if not signal.get("verified_evidence"):
            errors.append(f"{key} is missing verified_evidence")
        boundary = signal.get("claim_boundary", "")
        if not boundary:
            errors.append(f"{key} is missing claim_boundary")

    for key in END_USER_SIGNALS:
        boundary = signals.get(key, {}).get("claim_boundary", "").lower()
        if "do not claim" not in boundary:
            errors.append(f"{key} must preserve an explicit do-not-claim boundary")

    role_families = data.get("role_family_weights", {})
    if not role_families:
        errors.append("role_family_weights may not be empty")
    for family, weights in role_families.items():
        unknown = sorted(set(weights) - REQUIRED_SIGNALS)
        if unknown:
            errors.append(f"{family} contains unknown signals: {', '.join(unknown)}")
        for signal, weight in weights.items():
            if not isinstance(weight, int) or not 0 <= weight <= 4:
                errors.append(f"{family}.{signal} weight must be an integer from 0 to 4")

    tiers = data.get("employer_pathway_tiers", {})
    if set(tiers) != {"A", "B", "C"}:
        errors.append("employer_pathway_tiers must define A, B, and C")

    employers = data.get("employer_evidence", [])
    names: set[str] = set()
    for employer in employers:
        name = employer.get("employer", "")
        tier = employer.get("tier")
        if not name:
            errors.append("employer entry is missing employer name")
        elif name in names:
            errors.append(f"duplicate employer entry: {name}")
        names.add(name)
        if tier not in {"A", "B", "C"}:
            errors.append(f"{name or 'unnamed employer'} has invalid tier {tier!r}")
        sources = employer.get("source_urls", [])
        if tier in {"A", "B"} and not sources:
            errors.append(f"{name} tier {tier} requires at least one public source URL")
        if tier == "C" and tiers.get("C", {}).get("points") != 0:
            errors.append("Tier C must contribute zero employer-pathway points")
        for url in sources:
            if not isinstance(url, str) or not url.startswith("https://"):
                errors.append(f"{name} contains an invalid source URL")

    gaps = {item.get("gap") for item in data.get("hard_gap_controls", [])}
    missing_gaps = sorted(REQUIRED_MAJOR_GAPS - gaps)
    if missing_gaps:
        errors.append(f"missing required gap controls: {', '.join(missing_gaps)}")

    if set(data.get("fit_zones", {})) != {"direct", "near", "targeted_stretch", "no_go"}:
        errors.append("fit_zones must define direct, near, targeted_stretch, and no_go")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default="standards/sled_transition_signal_matrix.json",
        type=Path,
    )
    args = parser.parse_args()

    try:
        data = _load(args.path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        return 1

    errors = validate_config(data)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(f"PASS: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

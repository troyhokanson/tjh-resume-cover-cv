from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from anti_ai_scan import scan_text
from ats_injector import OVERCLAIM_SKIP

try:
    from docx import Document as _DocxDocument
except ImportError:  # pragma: no cover
    _DocxDocument = None


METRIC_PATTERN = re.compile(
    r"(?:\$\s?\d[\d,]*(?:\.\d+)?\+?|\b\d[\d,]*(?:\.\d+)?%|\b\d{1,4}\s*(?:years?|year|months?|month|(?:partner[- ]?)?agencies?)\b|\b\d{4}\b)",
    re.IGNORECASE,
)
TOKEN_PATTERN = re.compile(r"[a-z0-9][a-z0-9\-+/]*", re.IGNORECASE)


class GateFailure(RuntimeError):
    """Raised when a mandatory application-quality gate fails."""


@dataclass
class CaseEntry:
    case_id: str
    label: str
    tags: list[str]
    content: str

    @property
    def has_metric(self) -> bool:
        return bool(METRIC_PATTERN.search(self.content))


@dataclass
class TrainingEntry:
    entry_id: str
    name: str
    tier: str
    profiles: list[str]
    ptsd_safe: bool


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_document_text(path: str) -> str:
    source = Path(path)
    suffix = source.suffix.lower()
    if suffix in {".txt", ".md"}:
        return _read_text_file(source)
    if suffix == ".docx":
        if _DocxDocument is None:
            raise RuntimeError("python-docx is required to read .docx files")
        doc = _DocxDocument(str(source))
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError(f"Unsupported document format: {source.suffix}")


def _extract_tags(block: str) -> list[str]:
    line_match = re.search(r"\*\*TAGS:\*\*\s*(.+)", block)
    if not line_match:
        return []
    tags = re.findall(r"`([^`]+)`", line_match.group(1))
    return [t.strip().lower() for t in tags if t.strip()]


def parse_case_bank(case_bank_text: str) -> list[CaseEntry]:
    entries: list[CaseEntry] = []
    section_matches = list(re.finditer(r"(?m)^##\s+(.+)$", case_bank_text))

    for idx, match in enumerate(section_matches):
        heading = match.group(1).strip()
        if not heading.startswith(("Case ", "Program Entry", "Professional Conduct Entry")):
            continue
        start = match.start()
        end = section_matches[idx + 1].start() if idx + 1 < len(section_matches) else len(case_bank_text)
        block = case_bank_text[start:end]
        tags = _extract_tags(block)
        if not tags:
            continue
        case_id = _slugify(heading)
        entries.append(CaseEntry(case_id=case_id, label=heading, tags=tags, content=block))

    return entries


def load_case_bank(path: str | Path) -> list[CaseEntry]:
    return parse_case_bank(Path(path).read_text(encoding="utf-8"))


def _tokenize(text: str) -> set[str]:
    return {tok.lower() for tok in TOKEN_PATTERN.findall(text.lower())}


def _build_case_match_terms(case: CaseEntry) -> list[str]:
    match_terms: set[str] = set()
    clean_label = case.label.lower().replace("—", " ")
    clean_label = re.sub(r"\b(case|program entry|professional conduct entry)\b", " ", clean_label)
    clean_label = re.sub(r"\s+", " ", clean_label).strip(" -")
    if clean_label:
        match_terms.add(clean_label)

    for tag in case.tags:
        normalized = tag.replace("-", " ").strip()
        if len(normalized) >= 4:
            match_terms.add(normalized)
        if tag.isupper() and len(tag) >= 3:
            match_terms.add(tag.lower())

    return sorted(match_terms)


def build_variation_profile(job_title: str, company: str, date_seed: str) -> dict[str, Any]:
    seed_input = f"{job_title}|{company}|{date_seed}".lower()
    digest = hashlib.sha256(seed_input.encode("utf-8")).hexdigest()
    seed_int = int(digest[:16], 16)
    rng = random.Random(seed_int)

    summary_openers = ["outcome-first", "skills-first", "role-fit-first"]
    case_ordering = ["impact-first", "timeline-first", "method-first"]
    training_ordering = ["headline-first", "relevance-first", "recency-first"]
    sentence_rhythm = ["tight", "balanced", "detailed"]

    return {
        "seed_input": seed_input,
        "seed_hash": digest,
        "seed_int": seed_int,
        "summary_opener": summary_openers[rng.randrange(len(summary_openers))],
        "case_order": case_ordering[rng.randrange(len(case_ordering))],
        "training_order": training_ordering[rng.randrange(len(training_ordering))],
        "sentence_rhythm": sentence_rhythm[rng.randrange(len(sentence_rhythm))],
        "case_target_count": 3 if rng.random() >= 0.5 else 2,
    }


def _score_case(case: CaseEntry, profile: str, jd_tokens: set[str]) -> int:
    score = 0
    if profile in case.tags:
        score += 10

    for tag in case.tags:
        tag_token = tag.replace("-", " ")
        tag_parts = set(tag_token.split())
        if tag in jd_tokens or tag_token in jd_tokens:
            score += 3
        elif tag_parts and jd_tokens.intersection(tag_parts):
            score += 1

    if case.has_metric:
        score += 5

    return score


def select_required_cases(
    case_entries: list[CaseEntry],
    profile: str,
    jd_text: str,
    variation_profile: dict[str, Any],
    min_cases: int = 2,
    max_cases: int = 3,
) -> dict[str, Any]:
    jd_tokens = _tokenize(jd_text)

    qualified = [
        c for c in case_entries
        if profile in c.tags and c.has_metric
    ]

    if len(qualified) < min_cases:
        raise GateFailure(
            f"Case gate failed: only {len(qualified)} qualified cases found for profile '{profile}'. "
            f"Minimum required is {min_cases}."
        )

    scored = sorted(
        (
            {
                "case": case,
                "score": _score_case(case, profile, jd_tokens),
            }
            for case in qualified
        ),
        key=lambda item: (-item["score"], item["case"].case_id),
    )

    target_count = min(max_cases, max(min_cases, int(variation_profile.get("case_target_count", min_cases))))
    selected = scored[:target_count]

    required_cases = []
    for item in selected:
        case = item["case"]
        required_cases.append(
            {
                "case_id": case.case_id,
                "label": case.label,
                "tags": case.tags,
                "score": item["score"],
                "has_metric": case.has_metric,
                "match_terms": _build_case_match_terms(case),
            }
        )

    return {
        "minimum_required": min_cases,
        "maximum_allowed": max_cases,
        "qualified_count": len(qualified),
        "selected_count": len(required_cases),
        "required_cases": required_cases,
    }


def _flatten_catalog_credentials(catalog: dict[str, Any]) -> list[TrainingEntry]:
    certs = catalog.get("certifications", {})
    entries: list[TrainingEntry] = []

    for domain_entries in certs.values():
        for item in domain_entries:
            entries.append(
                TrainingEntry(
                    entry_id=str(item.get("id", "")),
                    name=str(item.get("name", "")).strip(),
                    tier=str(item.get("tier", "supporting")).strip().lower(),
                    profiles=[str(p).lower() for p in item.get("profiles", [])],
                    ptsd_safe=bool(item.get("ptsd_safe", False)),
                )
            )

    return entries


def _score_training(entry: TrainingEntry, jd_tokens: set[str]) -> int:
    score = 0
    if entry.tier == "headline":
        score += 5
    elif entry.tier == "supporting":
        score += 2

    entry_tokens = _tokenize(entry.name)
    score += len(entry_tokens.intersection(jd_tokens))
    return score


def select_required_training(
    catalog: dict[str, Any],
    profile: str,
    jd_text: str,
    minimum_count: int = 3,
) -> dict[str, Any]:
    jd_tokens = _tokenize(jd_text)
    entries = _flatten_catalog_credentials(catalog)

    eligible = [
        e for e in entries
        if e.ptsd_safe and e.tier in {"headline", "supporting"} and profile in e.profiles and e.name
    ]

    ranked = sorted(
        (
            {
                "entry": e,
                "score": _score_training(e, jd_tokens),
            }
            for e in eligible
        ),
        key=lambda item: (-item["score"], item["entry"].name.lower()),
    )

    selected = ranked[: max(minimum_count, min(6, len(ranked)))]

    documented_hours = (
        catalog.get("training_hours_total", {})
        .get("documented_hours")
    )

    meets_floor = len(selected) >= minimum_count
    equivalent_training_proof = False
    if not meets_floor and documented_hours is not None:
        try:
            equivalent_training_proof = float(documented_hours) >= 1000 and len(selected) >= 2
        except (TypeError, ValueError):
            equivalent_training_proof = False

    if not meets_floor and not equivalent_training_proof:
        raise GateFailure(
            f"Training gate failed: only {len(selected)} relevant credentials found for profile '{profile}'. "
            f"Minimum required is {minimum_count}."
        )

    return {
        "minimum_required": minimum_count,
        "eligible_count": len(eligible),
        "selected_count": len(selected),
        "equivalent_training_proof": equivalent_training_proof,
        "documented_training_hours": documented_hours,
        "required_training": [
            {
                "id": item["entry"].entry_id,
                "name": item["entry"].name,
                "tier": item["entry"].tier,
                "score": item["score"],
            }
            for item in selected
        ],
    }


def _find_sentences_with_term(text: str, term: str) -> list[str]:
    fragments = re.split(r"(?<=[.!?])\s+|\n+", text)
    term_l = term.lower()
    return [frag for frag in fragments if term_l in frag.lower()]


def verify_application_draft(
    manifest: dict[str, Any],
    resume_text: str,
    cover_text: str,
) -> dict[str, Any]:
    profile = manifest.get("profile", "vendor-solutions")
    combined = f"{resume_text}\n{cover_text}"
    combined_l = combined.lower()

    missing_cases: list[str] = []
    case_metric_failures: list[str] = []

    for case in manifest.get("required_cases", []):
        label = case["label"]
        match_terms = case.get("match_terms") or [label.lower()]

        found_term = None
        for term in match_terms:
            if term.lower() in combined_l:
                found_term = term
                break

        if not found_term:
            missing_cases.append(label)
            continue

        candidate_sentences = _find_sentences_with_term(combined, found_term)
        if not any(METRIC_PATTERN.search(sentence) for sentence in candidate_sentences):
            case_metric_failures.append(label)

    missing_training: list[str] = []
    for training in manifest.get("required_training", []):
        name = training["name"]
        if name.lower() not in combined_l:
            missing_training.append(name)

    overclaim_terms: list[str] = []
    for term in sorted(OVERCLAIM_SKIP.get(profile, set())):
        if term and term.lower() in combined_l:
            overclaim_terms.append(term)

    scan_violations = {
        "resume": scan_text(resume_text, doc_type="resume", profile=profile),
        "cover": scan_text(cover_text, doc_type="cover", profile=profile),
    }

    verification_passed = not (
        missing_cases
        or case_metric_failures
        or missing_training
        or overclaim_terms
        or scan_violations["resume"]
        or scan_violations["cover"]
    )

    return {
        "passed": verification_passed,
        "profile": profile,
        "missing_cases": missing_cases,
        "case_metric_failures": case_metric_failures,
        "missing_training": missing_training,
        "overclaim_terms": overclaim_terms,
        "scan_violations": scan_violations,
    }


def _sanitize_for_storage(value: Any, key: str | None = None) -> Any:
    sensitive_keys = {"jd_file", "resume", "cover", "seed_input"}
    if isinstance(value, dict):
        return {k: _sanitize_for_storage(v, k) for k, v in value.items()}
    if isinstance(value, list):
        return [_sanitize_for_storage(item, key) for item in value]
    if isinstance(value, str) and key in sensitive_keys:
        digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]
        return f"sha256:{digest}"
    return value


def _write_report(path: Path, payload: dict[str, Any]) -> None:
    sanitized_payload = _sanitize_for_storage(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sanitized_payload, indent=2), encoding="utf-8")


def _write_preflight_text_report(path: Path, payload: dict[str, Any]) -> None:
    payload = _sanitize_for_storage(payload)
    lines = [
        "Application Preflight Report",
        f"Generated: {payload['generated_at']}",
        f"Profile: {payload['profile']}",
        f"Employer: {payload['employer']}",
        f"Role: {payload['role']}",
        "",
        "Variation Profile:",
    ]
    for key, value in payload["variation_profile"].items():
        lines.append(f"  - {key}: {value}")

    lines.extend([
        "",
        f"Required cases ({len(payload['required_cases'])}):",
    ])
    for case in payload["required_cases"]:
        lines.append(f"  - {case['label']} [score={case['score']}]")

    lines.extend([
        "",
        f"Required training ({len(payload['required_training'])}):",
    ])
    for training in payload["required_training"]:
        lines.append(f"  - {training['name']} [{training['tier']}]")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_verification_text_report(path: Path, payload: dict[str, Any]) -> None:
    payload = _sanitize_for_storage(payload)
    lines = [
        "Application Draft Verification Report",
        f"Generated: {payload['generated_at']}",
        f"Profile: {payload['verification']['profile']}",
        f"Passed: {'YES' if payload['verification']['passed'] else 'NO'}",
        "",
        "Missing required cases:",
    ]
    if payload["verification"]["missing_cases"]:
        lines.extend(f"  - {v}" for v in payload["verification"]["missing_cases"])
    else:
        lines.append("  - none")

    lines.append("\nCases missing concrete stats:")
    if payload["verification"]["case_metric_failures"]:
        lines.extend(f"  - {v}" for v in payload["verification"]["case_metric_failures"])
    else:
        lines.append("  - none")

    lines.append("\nMissing required training references:")
    if payload["verification"]["missing_training"]:
        lines.extend(f"  - {v}" for v in payload["verification"]["missing_training"])
    else:
        lines.append("  - none")

    lines.append("\nOverclaim terms detected:")
    if payload["verification"]["overclaim_terms"]:
        lines.extend(f"  - {v}" for v in payload["verification"]["overclaim_terms"])
    else:
        lines.append("  - none")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def run_prepare(args: argparse.Namespace) -> int:
    jd_path = Path(args.jd)
    case_bank_path = Path(args.case_bank)
    credentials_path = Path(args.credentials)
    output = Path(args.output)

    jd_text = _read_text_file(jd_path)
    cases = load_case_bank(case_bank_path)
    catalog = json.loads(credentials_path.read_text(encoding="utf-8"))

    variation_profile = build_variation_profile(args.role, args.employer, args.date_seed)
    case_gate = select_required_cases(cases, args.profile, jd_text, variation_profile)
    training_gate = select_required_training(catalog, args.profile, jd_text, minimum_count=args.min_training)

    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "profile": args.profile,
        "employer": args.employer,
        "role": args.role,
        "jd_file": str(jd_path),
        "variation_profile": variation_profile,
        "required_cases": case_gate["required_cases"],
        "required_training": training_gate["required_training"],
        "gates": {
            "case_gate": case_gate,
            "training_gate": training_gate,
        },
    }

    _write_report(output, payload)

    txt_report = output.with_suffix(".txt")
    _write_preflight_text_report(txt_report, payload)

    print(f"Preflight manifest saved to: {output}")
    print(f"Preflight report saved to:   {txt_report}")
    return 0


def run_verify(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest)
    output = Path(args.output)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    resume_text = read_document_text(args.resume)
    cover_text = read_document_text(args.cover)

    verification = verify_application_draft(manifest, resume_text, cover_text)
    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "manifest": str(manifest_path),
        "resume": args.resume,
        "cover": args.cover,
        "verification": verification,
    }

    _write_report(output, payload)
    txt_report = output.with_suffix(".txt")
    _write_verification_text_report(txt_report, payload)

    print(f"Verification report saved to: {output}")
    print(f"Verification summary saved to: {txt_report}")

    if verification["passed"]:
        print("Verification status: PASS")
        return 0

    print("Verification status: FAIL")
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Application quality gates and verification")
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare", help="Run case/training selection gates")
    prepare.add_argument("--jd", required=True, help="Path to job description text file")
    prepare.add_argument("--profile", required=True, help="Selected profile")
    prepare.add_argument("--employer", required=True, help="Employer short name")
    prepare.add_argument("--role", required=True, help="Role short name")
    prepare.add_argument("--date-seed", required=True, help="Date seed (YYYY-MM-DD)")
    prepare.add_argument("--output", required=True, help="Output JSON manifest path")
    prepare.add_argument(
        "--case-bank",
        default="CASE_BANK.md",
        help="Path to CASE_BANK markdown",
    )
    prepare.add_argument(
        "--credentials",
        default="skills/troy-credentials-library/credentials_catalog.json",
        help="Path to credentials catalog JSON",
    )
    prepare.add_argument(
        "--min-training",
        type=int,
        default=3,
        help="Minimum required training credential count",
    )

    verify = sub.add_parser("verify", help="Verify drafted resume and cover against manifest")
    verify.add_argument("--manifest", required=True, help="Manifest JSON from prepare step")
    verify.add_argument("--resume", required=True, help="Path to drafted resume (.txt/.md/.docx)")
    verify.add_argument("--cover", required=True, help="Path to drafted cover letter (.txt/.md/.docx)")
    verify.add_argument("--output", required=True, help="Output JSON report path")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "prepare":
            return run_prepare(args)
        if args.command == "verify":
            return run_verify(args)
        parser.error(f"Unsupported command: {args.command}")
    except GateFailure as exc:
        print(f"ERROR: {exc}")
        return 1

    return 2


if __name__ == "__main__":
    sys.exit(main())

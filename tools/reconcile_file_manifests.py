#!/usr/bin/env python3
"""Reconcile private cloud-file manifests without storing private data in GitHub.

This utility compares one or more source-provider manifests against a Google Drive
manifest and classifies each source item as an exact duplicate, probable duplicate,
name conflict, or net-new candidate. It also assigns a generic evidence-value score.

The script is intentionally provider-neutral. Export manifests locally, run the tool,
and keep the generated outputs in the private evidence environment rather than in the
public repository.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

REQUIRED_COLUMNS = {"provider", "path", "name"}
OPTIONAL_COLUMNS = {
    "size",
    "modified_time",
    "content_hash",
    "mime_type",
    "url",
}

DUPLICATE_SUFFIX_RE = re.compile(
    r"(?:\s*\((?:copy|\d+)\)|\s+-\s+copy|\s+copy|_copy|_final|_revised|_updated)$",
    re.IGNORECASE,
)
NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")

VALUE_RULES: tuple[tuple[re.Pattern[str], int, str], ...] = (
    (re.compile(r"sentenc|judgment|disposition|register of actions|court", re.I), 25, "official court/outcome signal"),
    (re.compile(r"complaint|warrant|return|affidavit|order", re.I), 23, "legal-process signal"),
    (re.compile(r"forensic|examiner|extraction|evidence|ectf|icac", re.I), 22, "digital-forensic evidence signal"),
    (re.compile(r"certificate|certification|transcript|training|course", re.I), 18, "training or credential signal"),
    (re.compile(r"commendation|award|achievement|accomplishment", re.I), 16, "award or recognition signal"),
    (re.compile(r"assignment|case management|case inventory|case list", re.I), 14, "assignment or case-index signal"),
)

AUTHORITATIVE_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".xls", ".csv"}


@dataclass(frozen=True)
class ManifestItem:
    provider: str
    path: str
    name: str
    size: int | None = None
    modified_time: str = ""
    content_hash: str = ""
    mime_type: str = ""
    url: str = ""

    @property
    def suffix(self) -> str:
        return Path(self.name).suffix.lower()

    @property
    def normalized_name(self) -> str:
        stem = Path(self.name).stem.strip().lower()
        while True:
            updated = DUPLICATE_SUFFIX_RE.sub("", stem).strip()
            if updated == stem:
                break
            stem = updated
        normalized_stem = NON_ALNUM_RE.sub(" ", stem).strip()
        return f"{normalized_stem}{self.suffix}"


@dataclass(frozen=True)
class ReconciliationResult:
    source_provider: str
    source_path: str
    source_name: str
    normalized_name: str
    size: int | None
    content_hash: str
    classification: str
    matched_drive_path: str
    evidence_value_score: int
    score_reasons: str
    recommended_action: str


def parse_size(value: str) -> int | None:
    text = (value or "").strip()
    if not text:
        return None
    try:
        parsed = int(float(text))
    except ValueError as exc:
        raise ValueError(f"Invalid size value: {value!r}") from exc
    if parsed < 0:
        raise ValueError(f"Size cannot be negative: {value!r}")
    return parsed


def load_manifest(path: Path) -> list[ManifestItem]:
    if not path.exists():
        raise FileNotFoundError(path)

    if path.suffix.lower() == ".json":
        raw = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            raw = raw.get("items", [])
        if not isinstance(raw, list):
            raise ValueError(f"JSON manifest must contain a list or an 'items' list: {path}")
        rows = raw
    else:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))

    items: list[ManifestItem] = []
    for index, row in enumerate(rows, start=2):
        if not isinstance(row, dict):
            raise ValueError(f"Manifest row {index} is not an object: {path}")
        missing = [column for column in REQUIRED_COLUMNS if not str(row.get(column, "")).strip()]
        if missing:
            raise ValueError(f"Manifest row {index} missing required values {missing}: {path}")
        items.append(
            ManifestItem(
                provider=str(row["provider"]).strip(),
                path=str(row["path"]).strip(),
                name=str(row["name"]).strip(),
                size=parse_size(str(row.get("size", ""))),
                modified_time=str(row.get("modified_time", "")).strip(),
                content_hash=str(row.get("content_hash", "")).strip().lower(),
                mime_type=str(row.get("mime_type", "")).strip(),
                url=str(row.get("url", "")).strip(),
            )
        )
    return items


def hash_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def score_evidence(item: ManifestItem) -> tuple[int, list[str]]:
    searchable = f"{item.name} {item.path} {item.mime_type}"
    score = 10
    reasons = ["baseline retained-file value"]

    for pattern, points, reason in VALUE_RULES:
        if pattern.search(searchable):
            score += points
            reasons.append(reason)

    if item.suffix in AUTHORITATIVE_EXTENSIONS:
        score += 8
        reasons.append("durable evidence-oriented file type")
    if item.content_hash:
        score += 7
        reasons.append("cryptographic hash available")
    if item.size and item.size > 0:
        score += 4
        reasons.append("non-empty file")
    if re.search(r"summary|draft|redacted|copy", searchable, re.I):
        score -= 12
        reasons.append("possible derivative or copy")
    if re.search(r"resume|cover letter|role fit|application", searchable, re.I):
        score -= 10
        reasons.append("application artifact rather than primary evidence")

    return max(1, min(100, score)), reasons


def reconcile(source_items: Iterable[ManifestItem], drive_items: Sequence[ManifestItem]) -> list[ReconciliationResult]:
    drive_by_hash: dict[str, list[ManifestItem]] = {}
    drive_by_name: dict[str, list[ManifestItem]] = {}

    for item in drive_items:
        if item.content_hash:
            drive_by_hash.setdefault(item.content_hash, []).append(item)
        drive_by_name.setdefault(item.normalized_name, []).append(item)

    results: list[ReconciliationResult] = []
    for source in source_items:
        classification = "Net-New Evidence Candidate"
        matched_path = ""
        action = "Review content and destination; transfer only if evidence value is confirmed."

        hash_matches = drive_by_hash.get(source.content_hash, []) if source.content_hash else []
        name_matches = drive_by_name.get(source.normalized_name, [])

        if hash_matches:
            classification = "Exact Duplicate"
            matched_path = hash_matches[0].path
            action = "Do not transfer; register duplicate-group metadata if not already recorded."
        elif name_matches:
            same_size = [item for item in name_matches if source.size is not None and item.size == source.size]
            if same_size:
                classification = "Probable Duplicate"
                matched_path = same_size[0].path
                action = "Compare hashes or content before transfer; prefer the existing canonical copy."
            else:
                classification = "Name Conflict"
                matched_path = name_matches[0].path
                action = "Quarantine for content comparison; do not overwrite the Drive file."

        score, reasons = score_evidence(source)
        if classification == "Exact Duplicate":
            score = min(score, 20)
        elif classification == "Probable Duplicate":
            score = min(score, 35)
        elif classification == "Name Conflict":
            score = min(score, 60)

        results.append(
            ReconciliationResult(
                source_provider=source.provider,
                source_path=source.path,
                source_name=source.name,
                normalized_name=source.normalized_name,
                size=source.size,
                content_hash=source.content_hash,
                classification=classification,
                matched_drive_path=matched_path,
                evidence_value_score=score,
                score_reasons="; ".join(reasons),
                recommended_action=action,
            )
        )

    return sorted(results, key=lambda row: (-row.evidence_value_score, row.source_name.lower()))


def write_csv(path: Path, results: Sequence[ReconciliationResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(asdict(results[0]).keys()) if results else [
        "source_provider",
        "source_path",
        "source_name",
        "normalized_name",
        "size",
        "content_hash",
        "classification",
        "matched_drive_path",
        "evidence_value_score",
        "score_reasons",
        "recommended_action",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(asdict(result))


def write_json(path: Path, results: Sequence[ReconciliationResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"items": [asdict(result) for result in results]}, indent=2),
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        action="append",
        required=True,
        type=Path,
        help="Source-provider CSV or JSON manifest. Repeat for multiple providers.",
    )
    parser.add_argument("--drive", required=True, type=Path, help="Google Drive CSV or JSON manifest.")
    parser.add_argument("--output-csv", required=True, type=Path, help="Reconciliation CSV output path.")
    parser.add_argument("--output-json", type=Path, help="Optional reconciliation JSON output path.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        drive_items = load_manifest(args.drive)
        source_items: list[ManifestItem] = []
        for source_path in args.source:
            source_items.extend(load_manifest(source_path))
        results = reconcile(source_items, drive_items)
        write_csv(args.output_csv, results)
        if args.output_json:
            write_json(args.output_json, results)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    counts: dict[str, int] = {}
    for result in results:
        counts[result.classification] = counts.get(result.classification, 0) + 1
    print(json.dumps({"source_items": len(source_items), "drive_items": len(drive_items), "classifications": counts}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

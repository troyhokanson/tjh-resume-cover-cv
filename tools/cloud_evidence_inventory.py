#!/usr/bin/env python3
"""Read-only inventory and duplicate detector for locally synced cloud folders.

Designed for OneDrive, iCloud Drive, Dropbox, and similar folders on Windows.
It never moves, renames, deletes, or uploads source files. Outputs private CSV/JSON
manifests that can be compared with the Career Evidence Master source registry.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator, Sequence

CHUNK_SIZE = 1024 * 1024
DEFAULT_EXCLUDED_DIRS = {
    ".git", ".svn", ".hg", "node_modules", "__pycache__", "$recycle.bin",
    "system volume information", ".dropbox.cache", ".icloud", ".trash",
}

CATEGORY_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("Court Outcomes", ("sentencing", "court dispo", "register of actions", "judgment", "order")),
    ("Cases", ("case", "complaint", "warrant", "ectf", "forensic", "investigative", "ncmec", "icac")),
    ("Training", ("training", "course", "continuing education", "post credits", "transcript")),
    ("Certifications", ("certificate", "certification", "credential", "credly", "cpr", "cellebrite")),
    ("Commendations & Awards", ("commendation", "award", "achievement", "phoenix500", "faculty of the year", "eagle scout")),
    ("Applications", ("resume", "cover letter", "job description", "role fit", "application")),
]

SENSITIVE_HINTS = (
    "complaint", "warrant", "sentencing", "court dispo", "register of actions",
    "dd214", "da form", "victim", "ncmec", "icac", "ectf", "case",
)


@dataclass
class FileRecord:
    source_label: str
    root_path: str
    relative_path: str
    absolute_path: str
    file_name: str
    extension: str
    size_bytes: int
    modified_utc: str
    sha256: str
    md5: str
    category: str
    sensitivity_hint: str
    duplicate_group: str
    duplicate_count: int
    registry_match: str
    registry_source_id: str
    error: str


def iso_utc(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()


def classify(name: str, relpath: str) -> str:
    haystack = f"{name} {relpath}".lower()
    for category, keywords in CATEGORY_RULES:
        if any(keyword in haystack for keyword in keywords):
            return category
    return "Other"


def sensitivity_hint(name: str, relpath: str) -> str:
    haystack = f"{name} {relpath}".lower()
    return "Likely sensitive - manual review" if any(k in haystack for k in SENSITIVE_HINTS) else "Unclassified"


def hash_file(path: Path) -> tuple[str, str]:
    sha = hashlib.sha256()
    md5 = hashlib.md5()  # nosec B324 - compatibility identifier, not security use
    with path.open("rb") as handle:
        while chunk := handle.read(CHUNK_SIZE):
            sha.update(chunk)
            md5.update(chunk)
    return sha.hexdigest(), md5.hexdigest()


def should_skip_dir(name: str, include_hidden: bool) -> bool:
    lower = name.lower()
    if lower in DEFAULT_EXCLUDED_DIRS:
        return True
    return not include_hidden and name.startswith(".")


def iter_files(root: Path, include_hidden: bool) -> Iterator[Path]:
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as entries:
                for entry in entries:
                    try:
                        if entry.is_dir(follow_symlinks=False):
                            if not should_skip_dir(entry.name, include_hidden):
                                stack.append(Path(entry.path))
                        elif entry.is_file(follow_symlinks=False):
                            if include_hidden or not entry.name.startswith("."):
                                yield Path(entry.path)
                    except OSError:
                        continue
        except OSError:
            continue


def parse_root(value: str) -> tuple[str, Path]:
    if "=" in value:
        label, path_text = value.split("=", 1)
        label = label.strip() or "Cloud"
    else:
        path_text = value
        label = Path(path_text).name or "Cloud"
    return label, Path(os.path.expandvars(path_text)).expanduser()


def default_roots() -> list[tuple[str, Path]]:
    home = Path.home()
    userprofile = Path(os.environ.get("USERPROFILE", str(home)))
    candidates: list[tuple[str, Path]] = []
    for env_name, label in (
        ("OneDrive", "OneDrive"),
        ("OneDriveConsumer", "OneDrive-Personal"),
        ("OneDriveCommercial", "OneDrive-Work"),
    ):
        env_value = os.environ.get(env_name)
        if env_value:
            candidates.append((label, Path(env_value)))
    candidates.extend([
        ("OneDrive", userprofile / "OneDrive"),
        ("iCloudDrive", userprofile / "iCloudDrive"),
        ("iCloudDrive", userprofile / "iCloudDrive" / "Documents"),
        ("Dropbox", userprofile / "Dropbox"),
    ])
    seen: set[str] = set()
    existing: list[tuple[str, Path]] = []
    for label, path in candidates:
        key = str(path.resolve()) if path.exists() else str(path)
        if key not in seen and path.exists() and path.is_dir():
            existing.append((label, path))
            seen.add(key)
    return existing


def load_registry(path: Path | None) -> tuple[dict[str, str], dict[tuple[str, int], str]]:
    by_hash: dict[str, str] = {}
    by_name_size: dict[tuple[str, int], str] = {}
    if path is None:
        return by_hash, by_name_size
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            source_id = (row.get("Source Id") or row.get("Source ID") or "").strip()
            sha = (row.get("SHA-256") or row.get("SHA256") or "").strip().lower()
            name = (row.get("File Name") or row.get("filename") or "").strip().lower()
            size_text = (row.get("File Size Bytes") or row.get("size_bytes") or "").strip()
            if sha:
                by_hash[sha] = source_id
            try:
                size = int(float(size_text))
            except (TypeError, ValueError):
                size = -1
            if name and size >= 0:
                by_name_size[(name, size)] = source_id
    return by_hash, by_name_size


def scan_roots(
    roots: Sequence[tuple[str, Path]],
    include_hidden: bool,
    max_files: int | None,
    registry_hashes: dict[str, str],
    registry_name_size: dict[tuple[str, int], str],
) -> list[FileRecord]:
    records: list[FileRecord] = []
    for label, root in roots:
        root = root.resolve()
        count = 0
        for path in iter_files(root, include_hidden):
            if max_files is not None and count >= max_files:
                break
            count += 1
            try:
                stat = path.stat()
                sha256, md5 = hash_file(path)
                rel = str(path.relative_to(root))
                if sha256 in registry_hashes:
                    match = "Exact SHA-256 match"
                    source_id = registry_hashes[sha256]
                elif (path.name.lower(), stat.st_size) in registry_name_size:
                    match = "Filename + size candidate match"
                    source_id = registry_name_size[(path.name.lower(), stat.st_size)]
                else:
                    match = "New candidate"
                    source_id = ""
                records.append(FileRecord(
                    source_label=label,
                    root_path=str(root),
                    relative_path=rel,
                    absolute_path=str(path),
                    file_name=path.name,
                    extension=path.suffix.lower(),
                    size_bytes=stat.st_size,
                    modified_utc=iso_utc(stat.st_mtime),
                    sha256=sha256,
                    md5=md5,
                    category=classify(path.name, rel),
                    sensitivity_hint=sensitivity_hint(path.name, rel),
                    duplicate_group="",
                    duplicate_count=1,
                    registry_match=match,
                    registry_source_id=source_id,
                    error="",
                ))
            except (OSError, PermissionError) as exc:
                records.append(FileRecord(
                    source_label=label,
                    root_path=str(root),
                    relative_path=str(path),
                    absolute_path=str(path),
                    file_name=path.name,
                    extension=path.suffix.lower(),
                    size_bytes=0,
                    modified_utc="",
                    sha256="",
                    md5="",
                    category=classify(path.name, str(path)),
                    sensitivity_hint="Unclassified",
                    duplicate_group="",
                    duplicate_count=1,
                    registry_match="Unreadable",
                    registry_source_id="",
                    error=f"{type(exc).__name__}: {exc}",
                ))
    groups: dict[str, list[FileRecord]] = defaultdict(list)
    for record in records:
        if record.sha256:
            groups[record.sha256].append(record)
    group_num = 0
    for _, members in sorted(groups.items()):
        if len(members) > 1:
            group_num += 1
            group_id = f"DUP-{group_num:05d}"
            for member in members:
                member.duplicate_group = group_id
                member.duplicate_count = len(members)
    return records


def write_csv(path: Path, records: Iterable[FileRecord]) -> None:
    rows = list(records)
    fields = list(FileRecord.__dataclass_fields__.keys())
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only inventory and duplicate scan for synced cloud folders.")
    parser.add_argument("--root", action="append", default=[], help=r"Repeatable LABEL=PATH or PATH. Example: --root iCloudDrive=%USERPROFILE%\iCloudDrive")
    parser.add_argument("--registry-csv", type=Path, help="Optional export of the Career Evidence Master Sources tab.")
    parser.add_argument("--output-dir", type=Path, default=Path("build_logs/cloud_inventory"))
    parser.add_argument("--include-hidden", action="store_true")
    parser.add_argument("--max-files", type=int, help="Testing cap per root. Omit for full scan.")
    args = parser.parse_args()

    roots = [parse_root(value) for value in args.root] if args.root else default_roots()
    roots = [(label, path) for label, path in roots if path.exists() and path.is_dir()]
    if not roots:
        print("No valid cloud roots found. Supply one or more --root LABEL=PATH arguments.", file=sys.stderr)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)
    registry_hashes, registry_name_size = load_registry(args.registry_csv)
    records = scan_roots(
        roots=roots,
        include_hidden=args.include_hidden,
        max_files=args.max_files,
        registry_hashes=registry_hashes,
        registry_name_size=registry_name_size,
    )

    manifest_path = args.output_dir / "cloud_inventory_manifest.csv"
    duplicates_path = args.output_dir / "cloud_inventory_duplicates.csv"
    candidates_path = args.output_dir / "cloud_inventory_transfer_candidates.csv"
    summary_path = args.output_dir / "cloud_inventory_summary.json"

    write_csv(manifest_path, records)
    write_csv(duplicates_path, [r for r in records if r.duplicate_count > 1])
    write_csv(candidates_path, [r for r in records if r.registry_match == "New candidate" and not r.error])

    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "read_only": True,
        "roots": [{"label": label, "path": str(path.resolve())} for label, path in roots],
        "file_count": len(records),
        "error_count": sum(bool(r.error) for r in records),
        "duplicate_file_count": sum(r.duplicate_count > 1 for r in records),
        "duplicate_group_count": len({r.duplicate_group for r in records if r.duplicate_group}),
        "exact_registry_matches": sum(r.registry_match == "Exact SHA-256 match" for r in records),
        "filename_size_candidate_matches": sum(r.registry_match == "Filename + size candidate match" for r in records),
        "new_candidates": sum(r.registry_match == "New candidate" for r in records),
        "outputs": {
            "manifest": str(manifest_path),
            "duplicates": str(duplicates_path),
            "transfer_candidates": str(candidates_path),
        },
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

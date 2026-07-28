from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import stat
import uuid
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator, Sequence


TEMPORARY_NAMES = (
    re.compile(r"^~\$"),
    re.compile(r"\.tmp$", re.IGNORECASE),
    re.compile(r"\.partial$", re.IGNORECASE),
    re.compile(r"\.crdownload$", re.IGNORECASE),
    re.compile(r"^\.cloudbridge-part-"),
)

FILE_ATTRIBUTE_OFFLINE = 0x1000
FILE_ATTRIBUTE_RECALL_ON_OPEN = 0x40000
FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS = 0x400000


@dataclass(frozen=True)
class Source:
    label: str
    path: Path


@dataclass
class Record:
    source_label: str
    relative_path: str
    size_bytes: int
    modified_utc: str
    sha256: str | None
    destination_path: str
    destination_sha256: str | None
    needs_hydration: bool
    status: str
    detail: str
    inventory_time_utc: str


@dataclass(frozen=True)
class LocalRunResult:
    manifest_csv: Path
    summary_json: Path
    counts: dict[str, int]
    exit_code: int


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_label(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value).strip(" .")
    return cleaned or "Source"


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def is_temporary(path: Path) -> bool:
    return any(pattern.search(path.name) for pattern in TEMPORARY_NAMES)


def is_cloud_placeholder(path: Path) -> bool:
    try:
        attributes = getattr(path.stat(), "st_file_attributes", 0)
    except OSError:
        return False
    mask = (
        FILE_ATTRIBUTE_OFFLINE
        | FILE_ATTRIBUTE_RECALL_ON_OPEN
        | FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS
    )
    return bool(attributes & mask)


def _resolved(path: Path) -> Path:
    return path.expanduser().resolve()


def validate_local_scope(sources: Sequence[Source], destination: Path) -> tuple[list[Source], Path]:
    if not sources:
        raise ValueError("At least one source folder is required.")

    destination = _resolved(destination)
    resolved_sources: list[Source] = []
    seen: set[str] = set()
    for source in sources:
        source_path = _resolved(source.path)
        if not source_path.is_dir():
            raise ValueError(f"Source folder does not exist: {source_path}")
        key = os.path.normcase(str(source_path))
        if key in seen:
            continue
        seen.add(key)
        try:
            destination.relative_to(source_path)
        except ValueError:
            pass
        else:
            raise ValueError(
                f"Destination cannot be inside a source folder: {source_path}"
            )
        resolved_sources.append(Source(safe_label(source.label), source_path))

    for index, source in enumerate(resolved_sources):
        for other in resolved_sources[index + 1 :]:
            try:
                source.path.relative_to(other.path)
            except ValueError:
                pass
            else:
                raise ValueError(
                    f"Source folders cannot overlap: {source.path} and {other.path}"
                )
            try:
                other.path.relative_to(source.path)
            except ValueError:
                pass
            else:
                raise ValueError(
                    f"Source folders cannot overlap: {source.path} and {other.path}"
                )
    return resolved_sources, destination


def iter_files(root: Path) -> Iterator[Path]:
    for current_root, directories, files in os.walk(root, followlinks=False):
        current = Path(current_root)
        directories[:] = [
            name
            for name in directories
            if not (current / name).is_symlink()
            and not name.startswith(".cloudbridge-part-")
        ]
        for name in files:
            path = current / name
            if is_temporary(path):
                continue
            yield path


def _exclusive_copy(source: Path, destination: Path, expected_hash: str) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    descriptor: int | None = None
    try:
        descriptor = os.open(destination, flags, stat.S_IWUSR | stat.S_IRUSR)
        with source.open("rb") as source_handle, os.fdopen(
            descriptor, "wb", closefd=True
        ) as destination_handle:
            descriptor = None
            shutil.copyfileobj(source_handle, destination_handle, 1024 * 1024)
            destination_handle.flush()
            os.fsync(destination_handle.fileno())
        shutil.copystat(source, destination, follow_symlinks=False)
        actual_hash = sha256_file(destination)
        if actual_hash != expected_hash:
            raise IOError("Destination SHA-256 does not match source SHA-256.")
        return actual_hash
    except Exception:
        if descriptor is not None:
            os.close(descriptor)
        try:
            destination.unlink()
        except FileNotFoundError:
            pass
        raise


def _record_for_file(
    source: Source,
    file_path: Path,
    destination_root: Path,
    execute: bool,
    include_cloud_only: bool,
) -> Record:
    relative = file_path.relative_to(source.path)
    destination = destination_root / source.label / relative
    timestamp = utc_now()
    modified = datetime.fromtimestamp(
        file_path.stat().st_mtime, timezone.utc
    ).isoformat()
    hydration = is_cloud_placeholder(file_path)
    base = dict(
        source_label=source.label,
        relative_path=relative.as_posix(),
        size_bytes=file_path.stat().st_size,
        modified_utc=modified,
        sha256=None,
        destination_path=str(destination),
        destination_sha256=None,
        needs_hydration=hydration,
        inventory_time_utc=timestamp,
    )

    if file_path.is_symlink():
        return Record(**base, status="symlink-skipped", detail="Symbolic links are not copied.")
    if hydration and not include_cloud_only:
        return Record(
            **base,
            status="needs-hydration",
            detail="Make the file available offline before copying.",
        )

    try:
        source_hash = sha256_file(file_path)
    except OSError as exc:
        return Record(
            **base,
            status="source-read-error",
            detail=f"{type(exc).__name__}: source could not be read.",
        )
    base["sha256"] = source_hash

    if destination.exists():
        if not destination.is_file():
            return Record(
                **base,
                status="conflict-different",
                detail="Destination path exists and is not a regular file.",
            )
        try:
            destination_hash = sha256_file(destination)
        except OSError as exc:
            return Record(
                **base,
                status="destination-read-error",
                detail=f"{type(exc).__name__}: destination could not be read.",
            )
        base["destination_sha256"] = destination_hash
        if destination_hash == source_hash:
            return Record(
                **base,
                status="duplicate-identical",
                detail="Destination already contains identical bytes.",
            )
        return Record(
            **base,
            status="conflict-different",
            detail="Destination exists with different bytes; nothing was overwritten.",
        )

    if not execute:
        return Record(**base, status="planned-copy", detail="Dry run only.")

    try:
        destination_hash = _exclusive_copy(file_path, destination, source_hash)
    except FileExistsError:
        return Record(
            **base,
            status="conflict-race",
            detail="Destination appeared during copy; nothing was overwritten.",
        )
    except OSError as exc:
        return Record(
            **base,
            status="copy-error",
            detail=f"{type(exc).__name__}: copy failed.",
        )

    base["destination_sha256"] = destination_hash
    return Record(
        **base,
        status="copied-verified",
        detail="Copied and verified with SHA-256.",
    )


def write_local_manifests(
    records: Iterable[Record],
    manifest_dir: Path,
    mode: str,
    destination: Path,
) -> LocalRunResult:
    manifest_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    suffix = uuid.uuid4().hex[:8]
    csv_path = manifest_dir / f"cloudbridge-{stamp}-{suffix}.csv"
    summary_path = manifest_dir / f"cloudbridge-{stamp}-{suffix}.summary.json"
    record_list = list(records)
    fieldnames = list(asdict(record_list[0]).keys()) if record_list else [
        field.name for field in Record.__dataclass_fields__.values()
    ]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(record) for record in record_list)

    counts = dict(sorted(Counter(record.status for record in record_list).items()))
    blocking = {
        "source-read-error",
        "destination-read-error",
        "conflict-different",
        "conflict-race",
        "copy-error",
    }
    exit_code = 2 if any(counts.get(status, 0) for status in blocking) else 0
    summary = {
        "schema_version": 1,
        "created_utc": utc_now(),
        "mode": mode,
        "destination": str(destination),
        "record_count": len(record_list),
        "status_counts": counts,
        "exit_code": exit_code,
        "manifest_csv": str(csv_path),
        "safety": {
            "copy_only": True,
            "source_deletion": False,
            "overwrite": False,
            "sha256_verified_local_copies": True,
        },
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return LocalRunResult(csv_path, summary_path, counts, exit_code)


def run_local_copy(
    sources: Sequence[Source],
    destination: Path,
    manifest_dir: Path,
    execute: bool = False,
    include_cloud_only: bool = False,
) -> LocalRunResult:
    sources, destination = validate_local_scope(sources, destination)
    resolved_manifest_dir = _resolved(manifest_dir)
    for source in sources:
        try:
            resolved_manifest_dir.relative_to(source.path)
        except ValueError:
            pass
        else:
            raise ValueError(
                f"Manifest directory cannot be inside a source folder: {source.path}"
            )
    records: list[Record] = []
    for source in sources:
        for file_path in iter_files(source.path):
            records.append(
                _record_for_file(
                    source,
                    file_path,
                    destination,
                    execute=execute,
                    include_cloud_only=include_cloud_only,
                )
            )
    mode = "copy" if execute else "dry-run"
    return write_local_manifests(records, resolved_manifest_dir, mode, destination)


def discover_local_sources() -> list[Source]:
    candidates: list[Source] = []
    home = Path.home()
    env_candidates = (
        ("OneDrive", os.environ.get("OneDriveConsumer")),
        ("OneDrive", os.environ.get("OneDrive")),
        ("OneDrive", str(home / "OneDrive")),
        ("iCloud Drive", str(home / "iCloudDrive")),
        ("iCloud Drive", str(home / "iCloud Drive")),
        ("iCloud Drive", str(home / "Library" / "Mobile Documents" / "com~apple~CloudDocs")),
    )
    seen: set[str] = set()
    for label, raw_path in env_candidates:
        if not raw_path:
            continue
        path = Path(raw_path).expanduser()
        if not path.is_dir():
            continue
        resolved = path.resolve()
        key = os.path.normcase(str(resolved))
        if key not in seen:
            seen.add(key)
            candidates.append(Source(label, resolved))
    return candidates

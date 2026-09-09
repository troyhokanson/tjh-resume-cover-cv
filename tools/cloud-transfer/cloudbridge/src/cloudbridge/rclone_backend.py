from __future__ import annotations

import json
import re
import shutil
import subprocess
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Sequence


REMOTE_PATTERN = re.compile(r"^[A-Za-z0-9._-]+:")
DEFAULT_EXCLUDES = ("~$*", "*.tmp", "*.partial", "*.crdownload")


@dataclass(frozen=True)
class RcloneResult:
    command_kind: str
    mode: str
    log_path: Path
    summary_path: Path
    exit_code: int


def find_rclone(requested: str | None = None) -> str | None:
    if requested:
        candidate = Path(requested).expanduser()
        if candidate.is_file():
            return str(candidate.resolve())
        return shutil.which(requested)
    return shutil.which("rclone")


def require_remote(value: str, *, destination: bool = False) -> None:
    if not REMOTE_PATTERN.match(value):
        raise ValueError(f"Expected an rclone named remote, such as onedrive:path: {value}")
    if destination:
        _, remote_path = value.split(":", 1)
        if not remote_path.strip("/"):
            raise ValueError("Destination must be a folder below the remote root.")


def remote_name(value: str) -> str:
    return value.split(":", 1)[0].casefold()


def validate_remote_scope(source: str, destination: str) -> None:
    require_remote(source)
    require_remote(destination, destination=True)
    if source.rstrip("/") == destination.rstrip("/"):
        raise ValueError("Source and destination cannot be identical.")
    if remote_name(source) == remote_name(destination):
        source_path = source.split(":", 1)[1].strip("/")
        destination_path = destination.split(":", 1)[1].strip("/")
        if not source_path or destination_path.startswith(source_path + "/"):
            raise ValueError("Destination cannot be inside the source remote path.")


def list_remotes(
    rclone: str,
    config: Path | None = None,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> list[str]:
    command = [rclone, "listremotes"]
    if config:
        command.extend(["--config", str(config)])
    completed = runner(command, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError("rclone could not list configured remotes.")
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def build_copy_command(
    rclone: str,
    source: str,
    destination: str,
    log_path: Path,
    execute: bool,
    config: Path | None = None,
    excludes: Sequence[str] = DEFAULT_EXCLUDES,
    transfers: int = 4,
    checkers: int = 8,
) -> list[str]:
    validate_remote_scope(source, destination)
    command = [
        rclone,
        "copy",
        source,
        destination,
        "--immutable",
        "--check-first",
        "--create-empty-src-dirs",
        "--metadata",
        "--use-json-log",
        "--log-file",
        str(log_path),
        "--log-level",
        "INFO",
        "--stats",
        "30s",
        "--stats-one-line",
        "--retries",
        "3",
        "--low-level-retries",
        "10",
        "--transfers",
        str(transfers),
        "--checkers",
        str(checkers),
    ]
    if not execute:
        command.append("--dry-run")
    if config:
        command.extend(["--config", str(config)])
    for pattern in excludes:
        command.extend(["--exclude", pattern])
    return command


def _private_paths(
    manifest_dir: Path, kind: str, data_extension: str = "jsonl"
) -> tuple[Path, Path]:
    manifest_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    suffix = uuid.uuid4().hex[:8]
    return (
        manifest_dir / f"{kind}-{stamp}-{suffix}.{data_extension}",
        manifest_dir / f"{kind}-{stamp}-{suffix}.summary.json",
    )


def run_remote_copy(
    rclone: str,
    source: str,
    destination: str,
    manifest_dir: Path,
    execute: bool = False,
    config: Path | None = None,
    excludes: Sequence[str] = DEFAULT_EXCLUDES,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> RcloneResult:
    log_path, summary_path = _private_paths(manifest_dir, "remote-copy")
    command = build_copy_command(
        rclone,
        source,
        destination,
        log_path,
        execute,
        config=config,
        excludes=excludes,
    )
    completed = runner(command, text=True, capture_output=True, check=False)
    summary = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "command": "rclone copy",
        "mode": "copy" if execute else "dry-run",
        "source_remote": remote_name(source),
        "destination_remote": remote_name(destination),
        "exit_code": completed.returncode,
        "log_path": str(log_path),
        "safety": {
            "copy_only": True,
            "source_deletion": False,
            "immutable_destination": True,
            "rclone_integrity_checks": True,
            "sha256_end_to_end": False,
        },
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return RcloneResult(
        "copy",
        "copy" if execute else "dry-run",
        log_path,
        summary_path,
        completed.returncode,
    )


def run_remote_scan(
    rclone: str,
    source: str,
    manifest_dir: Path,
    config: Path | None = None,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> RcloneResult:
    require_remote(source)
    inventory_path, summary_path = _private_paths(
        manifest_dir, "remote-inventory", data_extension="json"
    )
    command = [
        rclone,
        "lsjson",
        source,
        "--recursive",
        "--files-only",
        "--metadata",
        "--no-mimetype",
    ]
    if config:
        command.extend(["--config", str(config)])
    with inventory_path.open("w", encoding="utf-8") as inventory:
        completed = runner(
            command,
            text=True,
            stdout=inventory,
            stderr=subprocess.PIPE,
            check=False,
        )
    summary = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "command": "rclone lsjson",
        "source_remote": remote_name(source),
        "exit_code": completed.returncode,
        "inventory_path": str(inventory_path),
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return RcloneResult("scan", "read-only", inventory_path, summary_path, completed.returncode)

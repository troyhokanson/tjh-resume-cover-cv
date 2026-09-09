from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

from . import __version__
from .core import Source, discover_local_sources, run_local_copy
from .rclone_backend import (
    DEFAULT_EXCLUDES,
    find_rclone,
    list_remotes,
    run_remote_copy,
    run_remote_scan,
)


def _source(value: str) -> Source:
    if "=" in value:
        label, raw_path = value.split("=", 1)
        if not label.strip() or not raw_path.strip():
            raise argparse.ArgumentTypeError("Use LABEL=PATH or PATH.")
        return Source(label.strip(), Path(raw_path.strip()))
    path = Path(value)
    return Source(path.name or "Source", path)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cloudbridge",
        description="Copy-only OneDrive and iCloud Drive intake with private manifests.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    subcommands = parser.add_subparsers(dest="command", required=True)

    subcommands.add_parser("doctor", help="Check local sync folders and rclone.")

    discover = subcommands.add_parser(
        "discover", help="List detected local folders and configured rclone remote names."
    )
    discover.add_argument("--rclone")
    discover.add_argument("--config", type=Path)

    configure = subcommands.add_parser(
        "configure", help="Open rclone's interactive configuration; credentials are not logged."
    )
    configure.add_argument("--rclone")

    local = subcommands.add_parser(
        "local-copy",
        help="Inventory or copy locally synchronized folders with SHA-256 verification.",
    )
    local.add_argument(
        "--source",
        action="append",
        type=_source,
        help="Repeatable LABEL=PATH. Auto-detects OneDrive/iCloud when omitted.",
    )
    local.add_argument("--destination", type=Path, required=True)
    local.add_argument(
        "--manifest-dir",
        type=Path,
        default=Path("private-manifests"),
    )
    local.add_argument("--include-cloud-only", action="store_true")
    local.add_argument(
        "--execute",
        action="store_true",
        help="Perform copy. Without this flag the command is a dry run.",
    )

    remote_scan = subcommands.add_parser(
        "remote-scan", help="Inventory one configured rclone remote without copying."
    )
    remote_scan.add_argument("--source", required=True)
    remote_scan.add_argument("--manifest-dir", type=Path, default=Path("private-manifests"))
    remote_scan.add_argument("--rclone")
    remote_scan.add_argument("--config", type=Path)

    remote_copy = subcommands.add_parser(
        "remote-copy",
        help="Copy one rclone remote to another using immutable, copy-only settings.",
    )
    remote_copy.add_argument("--source", required=True)
    remote_copy.add_argument("--destination", required=True)
    remote_copy.add_argument("--manifest-dir", type=Path, default=Path("private-manifests"))
    remote_copy.add_argument("--rclone")
    remote_copy.add_argument("--config", type=Path)
    remote_copy.add_argument(
        "--exclude",
        action="append",
        default=None,
        help="Repeatable rclone exclude pattern. Safe temporary-file excludes are default.",
    )
    remote_copy.add_argument(
        "--execute",
        action="store_true",
        help="Perform copy. Without this flag rclone runs with --dry-run.",
    )
    return parser


def _rclone_or_exit(requested: str | None) -> str:
    executable = find_rclone(requested)
    if not executable:
        raise RuntimeError("rclone was not found. Install it or pass --rclone PATH.")
    return executable


def _doctor() -> int:
    local_sources = discover_local_sources()
    rclone = find_rclone()
    result = {
        "cloudbridge_version": __version__,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "rclone_found": bool(rclone),
        "detected_local_sources": [
            {"label": source.label, "path": str(source.path)} for source in local_sources
        ],
        "ready_for_local_copy": bool(local_sources),
        "ready_for_remote_copy": bool(rclone),
    }
    print(json.dumps(result, indent=2))
    return 0 if (local_sources or rclone) else 2


def _discover(args: argparse.Namespace) -> int:
    rclone = find_rclone(args.rclone)
    remotes: list[str] = []
    remote_error: str | None = None
    if rclone:
        try:
            remotes = list_remotes(rclone, args.config)
        except RuntimeError as exc:
            remote_error = str(exc)
    result = {
        "local_sources": [
            {"label": source.label, "path": str(source.path)}
            for source in discover_local_sources()
        ],
        "rclone_remotes": remotes,
        "rclone_error": remote_error,
    }
    print(json.dumps(result, indent=2))
    return 0 if not remote_error else 2


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "doctor":
            return _doctor()
        if args.command == "discover":
            return _discover(args)
        if args.command == "configure":
            rclone = _rclone_or_exit(args.rclone)
            return subprocess.run([rclone, "config"], check=False).returncode
        if args.command == "local-copy":
            sources = args.source or discover_local_sources()
            result = run_local_copy(
                sources,
                args.destination,
                args.manifest_dir,
                execute=args.execute,
                include_cloud_only=args.include_cloud_only,
            )
            print(
                json.dumps(
                    {
                        "mode": "copy" if args.execute else "dry-run",
                        "status_counts": result.counts,
                        "manifest_csv": str(result.manifest_csv),
                        "summary_json": str(result.summary_json),
                        "exit_code": result.exit_code,
                    },
                    indent=2,
                )
            )
            return result.exit_code
        if args.command == "remote-scan":
            rclone = _rclone_or_exit(args.rclone)
            result = run_remote_scan(
                rclone, args.source, args.manifest_dir, config=args.config
            )
            print(
                json.dumps(
                    {
                        "mode": result.mode,
                        "inventory": str(result.log_path),
                        "summary_json": str(result.summary_path),
                        "exit_code": result.exit_code,
                    },
                    indent=2,
                )
            )
            return result.exit_code
        if args.command == "remote-copy":
            rclone = _rclone_or_exit(args.rclone)
            excludes = tuple(args.exclude) if args.exclude else DEFAULT_EXCLUDES
            result = run_remote_copy(
                rclone,
                args.source,
                args.destination,
                args.manifest_dir,
                execute=args.execute,
                config=args.config,
                excludes=excludes,
            )
            print(
                json.dumps(
                    {
                        "mode": result.mode,
                        "private_log": str(result.log_path),
                        "summary_json": str(result.summary_path),
                        "exit_code": result.exit_code,
                    },
                    indent=2,
                )
            )
            return result.exit_code
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"cloudbridge: {exc}", file=sys.stderr)
        return 2
    parser.error("Unknown command.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

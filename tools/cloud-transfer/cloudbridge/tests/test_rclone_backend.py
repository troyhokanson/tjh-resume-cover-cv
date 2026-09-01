from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from cloudbridge.rclone_backend import (
    build_copy_command,
    list_remotes,
    run_remote_copy,
    validate_remote_scope,
)


class RcloneTests(unittest.TestCase):
    def test_copy_command_is_dry_run_and_immutable_by_default(self) -> None:
        command = build_copy_command(
            "rclone",
            "onedrive:",
            "gdrive:Private Intake/OneDrive",
            Path("private.log"),
            execute=False,
        )
        self.assertIn("copy", command)
        self.assertIn("--dry-run", command)
        self.assertIn("--immutable", command)
        self.assertNotIn("sync", command)
        self.assertNotIn("move", command)

    def test_execute_omits_dry_run_but_keeps_immutable(self) -> None:
        command = build_copy_command(
            "rclone",
            "icloud:",
            "gdrive:Private Intake/iCloud",
            Path("private.log"),
            execute=True,
        )
        self.assertNotIn("--dry-run", command)
        self.assertIn("--immutable", command)

    def test_destination_root_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_remote_scope("onedrive:", "gdrive:")

    def test_destination_inside_source_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_remote_scope("remote:source", "remote:source/child")

    def test_list_remotes_parses_names(self) -> None:
        def fake_runner(*args, **kwargs):
            return subprocess.CompletedProcess(args[0], 0, "onedrive:\nicloud:\n", "")

        self.assertEqual(
            list_remotes("rclone", runner=fake_runner),
            ["onedrive:", "icloud:"],
        )

    def test_remote_copy_writes_summary_without_paths(self) -> None:
        def fake_runner(*args, **kwargs):
            log_path = Path(args[0][args[0].index("--log-file") + 1])
            log_path.write_text('{"msg":"dry run"}\n', encoding="utf-8")
            return subprocess.CompletedProcess(args[0], 0, "", "")

        with tempfile.TemporaryDirectory() as temporary:
            result = run_remote_copy(
                "rclone",
                "onedrive:Sensitive Folder",
                "gdrive:Private Intake/OneDrive",
                Path(temporary),
                runner=fake_runner,
            )
            summary = result.summary_path.read_text(encoding="utf-8")
            self.assertIn('"source_remote": "onedrive"', summary)
            self.assertNotIn("Sensitive Folder", summary)
            self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()

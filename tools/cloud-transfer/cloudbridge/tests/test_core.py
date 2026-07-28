from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from cloudbridge.core import Source, run_local_copy, safe_label, sha256_file


class CoreTests(unittest.TestCase):
    def test_safe_label_removes_path_characters(self) -> None:
        self.assertEqual(safe_label('OneDrive: Troy/Files'), "OneDrive_ Troy_Files")

    def test_dry_run_then_copy_then_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            destination = root / "destination"
            manifests = root / "manifests"
            source.mkdir()
            (source / "nested").mkdir()
            original = source / "nested" / "evidence.txt"
            original.write_text("verified content", encoding="utf-8")

            dry_run = run_local_copy(
                [Source("OneDrive", source)], destination, manifests
            )
            self.assertEqual(dry_run.counts, {"planned-copy": 1})
            self.assertFalse((destination / "OneDrive" / "nested" / "evidence.txt").exists())

            copied = run_local_copy(
                [Source("OneDrive", source)],
                destination,
                manifests,
                execute=True,
            )
            copied_path = destination / "OneDrive" / "nested" / "evidence.txt"
            self.assertEqual(copied.counts, {"copied-verified": 1})
            self.assertEqual(sha256_file(original), sha256_file(copied_path))

            duplicate = run_local_copy(
                [Source("OneDrive", source)],
                destination,
                manifests,
                execute=True,
            )
            self.assertEqual(duplicate.counts, {"duplicate-identical": 1})

    def test_conflict_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            destination = root / "destination"
            manifests = root / "manifests"
            source.mkdir()
            (destination / "iCloud Drive").mkdir(parents=True)
            (source / "same.txt").write_text("source", encoding="utf-8")
            conflict = destination / "iCloud Drive" / "same.txt"
            conflict.write_text("destination", encoding="utf-8")

            result = run_local_copy(
                [Source("iCloud Drive", source)],
                destination,
                manifests,
                execute=True,
            )
            self.assertEqual(result.exit_code, 2)
            self.assertEqual(result.counts, {"conflict-different": 1})
            self.assertEqual(conflict.read_text(encoding="utf-8"), "destination")

            with result.manifest_csv.open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["status"], "conflict-different")

    def test_destination_inside_source_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary)
            with self.assertRaises(ValueError):
                run_local_copy(
                    [Source("OneDrive", source)],
                    source / "destination",
                    source / "manifests",
                )

    def test_overlapping_sources_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            nested = root / "nested"
            nested.mkdir()
            with self.assertRaises(ValueError):
                run_local_copy(
                    [Source("Root", root), Source("Nested", nested)],
                    root.parent / "destination",
                    root.parent / "manifests",
                )

    def test_manifest_inside_source_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaises(ValueError):
                run_local_copy(
                    [Source("OneDrive", root)],
                    root.parent / "destination",
                    root / "private-manifests",
                )


if __name__ == "__main__":
    unittest.main()

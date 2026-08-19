"""Fail fast when the application-formatting source of truth has drifted."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[3]


def require(path: Path, patterns: tuple[str, ...]) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [pattern for pattern in patterns if not re.search(pattern, text, re.MULTILINE)]


def main() -> int:
    checks = {
        ROOT / "HEADER_STANDARD.md": (
            r"#0D1B2A",
            r"#C9A84C",
            r"26 pt",
            r"Body top margin.*1\.55 inch",
            r"(?i)troyhokanson\.com",
        ),
        ROOT / "docx_header.py": (
            r'NAVY\s*=\s*RGBColor\(0x0D,\s*0x1B,\s*0x2A\)',
            r'GOLD\s*=\s*RGBColor\(0xC9,\s*0xA8,\s*0x4C\)',
            r'def build_navy_header\(',
            r'def add_section_heading\(',
            r'def add_bullet\(',
            r'def add_job_block\(',
        ),
        ROOT / "profile_one_pager.py": (
            r"from docx_header import",
            r"build_navy_header",
            r"add_section_heading",
            r"body_top_margin_inches=1\.55",
        ),
    }

    failures: list[str] = []
    for path, patterns in checks.items():
        if not path.exists():
            failures.append(f"missing: {path.relative_to(ROOT)}")
            continue
        missing = require(path, patterns)
        failures.extend(f"{path.relative_to(ROOT)} missing pattern: {item}" for item in missing)

    if failures:
        print("Application-format preflight failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Application-format preflight passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

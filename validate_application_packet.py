#!/usr/bin/env python3
"""
Application packet standards validator for Troy Hokanson resumes, cover letters,
CVs, recruiter packets, bios, and one-pagers.

Purpose:
- Run one checklist-style gate before any document is shared or uploaded.
- Combine anti-AI, privacy, typography, pagination, and header expectations.
- Catch failures like a branded header passing while body typography or page
  breaks fail.

This script is intentionally conservative. It should fail closed when it cannot
inspect something important.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

try:
    import pdfplumber
except Exception:  # pragma: no cover
    pdfplumber = None

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None

try:
    from anti_ai_scan import scan_text
except Exception:  # pragma: no cover
    scan_text = None

NAVY = "#0D1B2A"
GOLD = "#C9A84C"
GARAMOND_FAMILY = ("garamond", "eb garamond", "adobe garamond pro")
DISALLOWED_BODY_FONTS = ("aptos", "calibri", "calibri light", "arial")

SENSITIVE_PATTERNS = {
    "post_number": re.compile(r"\bPOST\s*(?:#|No\.?|Number|License\s*(?:No\.?|Number)?)\s*\d{4,6}\b", re.I),
    "peace_officer_license": re.compile(r"\b(?:Minnesota\s+|MN\s+)?(?:Peace\s+Officer(?:\s+POST)?|POST(?:\s+Board)?)\s+(?:License|Licensed|Certification|Certified)\b", re.I),
    "case_control_number": re.compile(r"\b(?:LA|ICR|CN|Control\s*#)\s*[-#:]?\s*\d{5,}\b", re.I),
    "court_case_number": re.compile(r"\b\d{2}[A-Z]{2}-[A-Z]{2}-\d{2}-\d{4}\b", re.I),
    "dob": re.compile(r"\bDOB\s*[:\-/]?\s*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", re.I),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
}

BLOCKED_TERMS_ALWAYS = (
    "homicide",
    "death investigation",
    "lethal force",
    "sexual assault",
    "criminal sexual conduct",
    "human trafficking",
)

ICAC_GATED_TERMS = (
    "CSAM",
    "child sexual",
    "child abuse",
    "child exploitation",
    "ICAC",
)

ORPHAN_HEADING_PATTERNS = (
    re.compile(r"^\s*(Professional Summary|Core Skills|Selected Experience|Professional Experience|Training|Education|Recognition|Certifications)\s*$", re.I),
    re.compile(r"^\s*(Adjunct Faculty|Detective|Police Officer|Field Training Officer|Real Estate Advisor|Military Service)\b", re.I),
)


@dataclass
class CheckResult:
    name: str
    passed: bool
    severity: str
    detail: str


def result(name: str, passed: bool, detail: str, severity: str = "error") -> CheckResult:
    return CheckResult(name=name, passed=passed, severity=severity, detail=detail)


def read_pdf_text(pdf_path: Path) -> str:
    if pdfplumber is None:
        raise RuntimeError("pdfplumber is required for PDF text extraction")
    with pdfplumber.open(str(pdf_path)) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def inspect_privacy(text: str, allow_icac: bool) -> list[CheckResult]:
    checks: list[CheckResult] = []
    for name, pattern in SENSITIVE_PATTERNS.items():
        hits = pattern.findall(text)
        checks.append(result(f"privacy.{name}", not hits, f"{len(hits)} hit(s)"))
    for term in BLOCKED_TERMS_ALWAYS:
        hits = re.findall(rf"\b{re.escape(term)}\b", text, flags=re.I)
        checks.append(result(f"privacy.blocked_term.{term}", not hits, f"{len(hits)} hit(s)"))
    if not allow_icac:
        for term in ICAC_GATED_TERMS:
            hits = re.findall(rf"\b{re.escape(term)}\b", text, flags=re.I)
            checks.append(result(f"privacy.icac_gated.{term}", not hits, f"{len(hits)} hit(s)"))
    return checks


def inspect_anti_ai(text: str, doc_type: str, profile: str, allow_icac: bool) -> list[CheckResult]:
    if scan_text is None:
        return [result("anti_ai_scan.available", False, "anti_ai_scan.py could not be imported")]
    failures = scan_text(text, doc_type=doc_type, profile=profile, allow_icac=allow_icac)
    return [result("anti_ai_scan", not failures, "pass" if not failures else " | ".join(failures))]


def _xml_files(docx_path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    with zipfile.ZipFile(docx_path) as zf:
        for name in zf.namelist():
            if name.startswith("word/") and name.endswith(".xml"):
                data = zf.read(name).decode("utf-8", errors="replace")
                out[name] = data
    return out


def inspect_docx_font_and_pagination(docx_path: Path) -> list[CheckResult]:
    checks: list[CheckResult] = []
    if not docx_path.exists():
        return [result("docx.exists", False, f"missing DOCX: {docx_path}")]

    xml = _xml_files(docx_path)
    joined = "\n".join(xml.values()).lower()

    # Font gate. This is not a perfect rendered-font test, but it catches the
    # common build failure: default Aptos/Calibri/Arial leaking into styles/runs.
    garamond_present = any(font in joined for font in GARAMOND_FAMILY)
    checks.append(result("font.garamond_family_present", garamond_present, "Garamond-family font reference found" if garamond_present else "No Garamond-family reference found"))

    for font in DISALLOWED_BODY_FONTS:
        # Arial may exist as fallback in design standard references, so this is
        # warning unless it appears repeatedly in document XML.
        count = joined.count(font)
        severity = "warning" if font == "arial" else "error"
        checks.append(result(f"font.disallowed_visible_default.{font}", count == 0, f"{count} XML occurrence(s)", severity=severity))

    keep_next_count = joined.count("w:keepnext")
    checks.append(result("pagination.keep_with_next_present", keep_next_count > 0, f"{keep_next_count} keepNext marker(s)"))

    page_breaks = joined.count("w:br w:type=\"page\"") + joined.count("w:type=\"page\"")
    checks.append(result("pagination.explicit_or_structural_page_breaks_detected", True, f"{page_breaks} page-break marker(s) detected", severity="info"))

    # Header section gate.
    header_xml = "\n".join(v for k, v in xml.items() if k.startswith("word/header"))
    checks.append(result("header.xml_header_section_present", bool(header_xml.strip()), "header XML found" if header_xml.strip() else "No Word header XML found"))
    checks.append(result("header.navy_color_in_header", "0d1b2a" in header_xml.lower(), "navy color found in header XML" if "0d1b2a" in header_xml.lower() else "navy color missing from header XML"))
    checks.append(result("header.gold_color_in_header", "c9a84c" in header_xml.lower(), "gold color found in header XML" if "c9a84c" in header_xml.lower() else "gold color missing from header XML"))

    body_xml = xml.get("word/document.xml", "")
    body_has_navy = "0d1b2a" in body_xml.lower()
    checks.append(result("header.navy_not_in_body", not body_has_navy, "navy found only outside document body" if not body_has_navy else "navy color appears in document body XML"))

    return checks


def inspect_rendered_header_png(png_path: Path, expected: str = NAVY) -> list[CheckResult]:
    if Image is None:
        return [result("render.pillow_available", False, "Pillow unavailable")]
    if not png_path.exists():
        return [result("render.header_png_exists", False, f"missing PNG: {png_path}")]

    image = Image.open(png_path).convert("RGB")
    width, height = image.size
    # Sample top, left, and right edges inside first 70 px to catch white-strip failures.
    sample_y = min(20, height - 1)
    edge_points = [
        image.getpixel((0, sample_y)),
        image.getpixel((width // 2, sample_y)),
        image.getpixel((width - 1, sample_y)),
    ]
    expected_rgb = tuple(int(expected[i:i + 2], 16) for i in (1, 3, 5))

    def close(px: tuple[int, int, int], target: tuple[int, int, int], tolerance: int = 18) -> bool:
        return all(abs(px[i] - target[i]) <= tolerance for i in range(3))

    edges_ok = all(close(px, expected_rgb) for px in edge_points)
    return [
        result("render.header_png_exists", True, str(png_path), severity="info"),
        result("render.header_top_left_right_navy", edges_ok, f"sampled edge pixels: {edge_points}, expected near {expected_rgb}"),
    ]


def inspect_pdf_page_orphans(pdf_path: Path) -> list[CheckResult]:
    checks: list[CheckResult] = []
    if pdfplumber is None:
        return [result("pagination.pdfplumber_available", False, "pdfplumber unavailable")]
    with pdfplumber.open(str(pdf_path)) as pdf:
        for idx, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            tail = lines[-3:] if len(lines) >= 3 else lines
            tail_text = " | ".join(tail)
            orphan_hits = []
            if tail:
                last = tail[-1]
                for pattern in ORPHAN_HEADING_PATTERNS:
                    if pattern.search(last):
                        orphan_hits.append(last)
            checks.append(result(f"pagination.page_{idx}.orphan_heading_tail", not orphan_hits, f"tail: {tail_text}"))
    return checks


def maybe_render_docx_to_pdf(docx_path: Path, output_dir: Path) -> Path | None:
    """Best-effort LibreOffice rendering. Returns PDF path when successful."""
    soffice = "soffice"
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(output_dir), str(docx_path)]
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    except Exception:
        return None
    if completed.returncode != 0:
        return None
    pdf_path = output_dir / (docx_path.stem + ".pdf")
    return pdf_path if pdf_path.exists() else None


def validate_one(args: argparse.Namespace) -> dict[str, Any]:
    pdf_path = Path(args.pdf) if args.pdf else None
    docx_path = Path(args.docx) if args.docx else None
    header_pngs = [Path(p) for p in args.header_png]

    checks: list[CheckResult] = []

    if pdf_path and pdf_path.exists():
        text = read_pdf_text(pdf_path)
        checks.extend(inspect_anti_ai(text, args.doc_type, args.profile, args.allow_icac))
        checks.extend(inspect_privacy(text, args.allow_icac))
        checks.extend(inspect_pdf_page_orphans(pdf_path))
    else:
        checks.append(result("pdf.exists", False if args.pdf else True, f"PDF not provided or missing: {args.pdf}", severity="error" if args.pdf else "info"))

    if docx_path:
        checks.extend(inspect_docx_font_and_pagination(docx_path))
    else:
        checks.append(result("docx.provided", False, "DOCX path not provided", severity="warning"))

    for png in header_pngs:
        checks.extend(inspect_rendered_header_png(png))

    failed_errors = [c for c in checks if not c.passed and c.severity == "error"]
    failed_warnings = [c for c in checks if not c.passed and c.severity == "warning"]

    return {
        "document_type": args.doc_type,
        "profile": args.profile,
        "pdf": str(pdf_path) if pdf_path else None,
        "docx": str(docx_path) if docx_path else None,
        "header_pngs": [str(p) for p in header_pngs],
        "passed": len(failed_errors) == 0,
        "failed_error_count": len(failed_errors),
        "failed_warning_count": len(failed_warnings),
        "checks": [asdict(c) for c in checks],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Troy Hokanson application document against GitHub standards.")
    parser.add_argument("--pdf", help="Rendered PDF path")
    parser.add_argument("--docx", help="Source DOCX path")
    parser.add_argument("--header-png", action="append", default=[], help="Rendered page PNG to check for zero-bleed navy header. May be repeated.")
    parser.add_argument("--doc-type", default="resume", choices=["resume", "cover", "cv", "bio"], help="Document type for scan rules")
    parser.add_argument("--profile", default="analyst-intelligence", help="Role profile for anti-AI lane rules")
    parser.add_argument("--allow-icac", action="store_true", help="Open ICAC-gated terminology only for appropriate child-safety platform roles")
    parser.add_argument("--json-out", help="Optional JSON report path")
    args = parser.parse_args()

    report = validate_one(args)
    payload = json.dumps(report, indent=2)
    if args.json_out:
        Path(args.json_out).write_text(payload, encoding="utf-8")
    print(payload)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

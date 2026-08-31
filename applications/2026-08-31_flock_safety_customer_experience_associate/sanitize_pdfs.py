#!/usr/bin/env python3

from pathlib import Path

from pypdf import PdfReader, PdfWriter


APP_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = APP_DIR / "output"


def sanitize(path: Path, label: str) -> None:
    reader = PdfReader(path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata({
        "/Title": f"Troy Hokanson - Flock Safety - Customer Experience Associate - {label} - 2026-08-31",
        "/Author": "Troy Hokanson",
        "/Subject": "Application for Flock Safety Customer Experience Associate, requisition 1cabec78-f1bd-4615-95d2-5d8196eb46e0",
        "/Keywords": f"Troy Hokanson, Flock Safety, Customer Experience Associate, 1cabec78-f1bd-4615-95d2-5d8196eb46e0, {label}, 2026-08-31",
        "/Creator": "Troy Hokanson",
        "/Producer": "Troy Hokanson",
    })
    temporary = path.with_suffix(".sanitized.pdf")
    with temporary.open("wb") as stream:
        writer.write(stream)
    temporary.replace(path)


def main() -> None:
    sanitize(OUTPUT_DIR / "2026-08-31_Troy-Hokanson_Flock-Customer-Experience-Associate_1cabec78_Resume.pdf", "Resume")
    sanitize(OUTPUT_DIR / "2026-08-31_Troy-Hokanson_Flock-Customer-Experience-Associate_1cabec78_Cover-Letter.pdf", "Cover Letter")


if __name__ == "__main__":
    main()

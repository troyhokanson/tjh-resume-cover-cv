"""
Build a reference DOCX showing the locked header.
Used as the visual ground truth and as a smoke test for docx_header.py.

Run: python3 templates/build_reference.py
Output: templates/reference_header.docx
"""

import os, sys
from pathlib import Path

# Allow running directly from the repo root (`python build_reference.py`) as
# well as via the workspace/templates symlink (`python templates/build_reference.py`).
# In both cases __file__ resolves to the repo directory when made absolute.
_here = os.path.dirname(os.path.abspath(__file__))
if _here not in sys.path:
    sys.path.insert(0, _here)

from docx_header import (
    new_document, build_navy_header,
    add_section_heading, add_bullet, add_job_block,
)

UNIVERSITY_OF_PHOENIX_DATES = "2007-2025"
INVESTIGATIVE_DATE_RANGES = ("2010-2011", "2016-2021")


def build(output_path: str | os.PathLike[str] | None = None):
    doc = new_document()
    build_navy_header(doc)

    add_section_heading(doc, "Professional Summary")
    p = doc.add_paragraph(
        "This is a reference document used to verify the locked navy/gold header "
        "for Troy J. Hokanson's DOCX resumes, cover letters, and CVs. The header "
        "above must match the UHG reference exactly: full-bleed navy bar with zero "
        "whitespace above, white serif name centered, inset gold horizontal rule, "
        "single gold contact row beneath, no subtitle line. Canonical repository "
        f"date ranges are University of Phoenix ({UNIVERSITY_OF_PHOENIX_DATES}) "
        f"and investigative service ({INVESTIGATIVE_DATE_RANGES[0]}, "
        f"{INVESTIGATIVE_DATE_RANGES[1]})."
    )

    add_section_heading(doc, "Teaching Experience")
    add_job_block(doc, "Adjunct Faculty, Criminal Justice",
                  "University of Phoenix",
                  UNIVERSITY_OF_PHOENIX_DATES)

    add_section_heading(doc, "Professional Experience")
    add_job_block(doc, "Investigative Service Sample",
                  "Reference chronology verification entry",
                  INVESTIGATIVE_DATE_RANGES[0])
    add_job_block(doc, "Detective / Digital Forensic Examiner",
                  "Lakeville Police Department  |  Dakota County Electronic Crimes Task Force",
                  INVESTIGATIVE_DATE_RANGES[1])
    add_bullet(doc, "Sample bullet to verify body styling stays consistent across builds.")
    add_bullet(doc, "Second sample bullet to confirm bullet alignment and line spacing.")

    out = Path(output_path) if output_path else Path(__file__).resolve().parent / "reference_header.docx"
    doc.save(out)
    print(out)


if __name__ == "__main__":
    build()

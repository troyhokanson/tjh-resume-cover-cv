"""
Build a reference DOCX showing the locked header.
Used as the visual ground truth and as a smoke test for docx_header.py.

Run: python3 templates/build_reference.py
Output: templates/reference_header.docx
"""

import os, sys

# Allow running directly from the repo root (`python build_reference.py`) as
# well as via the workspace/templates symlink (`python templates/build_reference.py`).
_here = os.path.dirname(os.path.abspath(__file__))
if _here not in sys.path:
    sys.path.insert(0, _here)

from docx_header import (
    new_document, build_navy_header,
    add_section_heading, add_bullet, add_job_block,
)


def build():
    doc = new_document()
    build_navy_header(doc)

    add_section_heading(doc, "Professional Summary")
    p = doc.add_paragraph(
        "This is a reference document used to verify the locked navy/gold header "
        "for Troy J. Hokanson's DOCX resumes, cover letters, and CVs. The header "
        "above must match the UHG reference exactly: full-bleed navy bar with zero "
        "whitespace above, white serif name centered, inset gold horizontal rule, "
        "single gold contact row beneath, no subtitle line."
    )

    add_section_heading(doc, "Professional Experience")

    # DCECTF and ECU are always two separate blocks -- never merged.
    # Dates from CAREER_CONSTANTS.md (locked June 2026).
    add_job_block(doc, "Detective / Digital Forensic Examiner",
                  "Dakota County Electronic Crimes Task Force (DCECTF)  |  Lakeville Police Department",
                  "June 2017 - December 2021")
    add_bullet(doc, "Sample bullet to verify body styling stays consistent across builds.")

    add_job_block(doc, "Detective / Electronic Crimes Unit (ECU)",
                  "Lakeville Police Department  |  Lakeville, MN",
                  "September 2016 - June 2017")
    add_bullet(doc, "Second sample bullet to confirm bullet alignment and line spacing.")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reference_header.docx")
    doc.save(out)
    print(out)


if __name__ == "__main__":
    build()

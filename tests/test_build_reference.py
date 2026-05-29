from pathlib import Path

from docx import Document

import build_reference


def test_reference_build_contains_canonical_date_ranges(tmp_path):
    output = tmp_path / "reference_header.docx"

    build_reference.build(output)

    assert output.exists()

    doc = Document(output)
    text = "\n".join(paragraph.text for paragraph in doc.paragraphs)

    assert f"University of Phoenix ({build_reference.UNIVERSITY_OF_PHOENIX_DATES})" in text
    assert build_reference.UNIVERSITY_OF_PHOENIX_DATES in text
    assert build_reference.INVESTIGATIVE_DATE_RANGES[0] in text
    assert build_reference.INVESTIGATIVE_DATE_RANGES[1] in text

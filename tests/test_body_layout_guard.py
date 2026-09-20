from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import fitz
from docx import Document
from body_typography_pagination_validator import validate_body


def fixture(tmp_path, bottoms):
    word = tmp_path / 'test.docx'
    d = Document()
    d.add_paragraph('Example body')
    d.save(word)
    pdf = fitz.open()
    for bottom in bottoms:
        p = pdf.new_page(width=612, height=792)
        p.insert_text((50, bottom), 'Example body', fontsize=11)
    pdf.save(tmp_path / 'test.pdf')
    pdf.close()
    return word, tmp_path / 'test.pdf'


def test_large_blank_space_fails(tmp_path):
    report = validate_body(*fixture(tmp_path, [580, 580]))
    assert any(c['name'] == 'body.bottom_blank.1' and not c['passed'] for c in report['checks'])


def test_balanced_pages_pass_geometry_but_reject_wrong_font(tmp_path):
    report = validate_body(*fixture(tmp_path, [680, 680]))
    assert all(c['passed'] for c in report['checks'] if 'bottom_blank' in c['name'] or 'page_balance' in c['name'])
    assert any(not c['passed'] for c in report['checks'] if 'rendered_fonts' in c['name'])


def test_missing_input_fails_closed(tmp_path):
    report = validate_body(tmp_path/'missing.docx', tmp_path/'missing.pdf')
    assert not report['passed']
    assert report['checks'][0]['name'] == 'body.inspection_available'


def test_blank_pdf_page_fails(tmp_path):
    word, pdf_path = fixture(tmp_path, [680])
    d = fitz.open();d.new_page();d.save(pdf_path);d.close()
    report = validate_body(word, pdf_path)
    assert any(c['name'] == 'body.content.1' and not c['passed'] for c in report['checks'])

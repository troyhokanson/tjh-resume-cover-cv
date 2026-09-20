"""Fail-closed checks supplementing the required per-page visual review."""
from pathlib import Path
import argparse
import hashlib
import json


def validate_body(docx_path, pdf_path, doc_type='resume'):
    from docx import Document
    import fitz
    docx_path, pdf_path = Path(docx_path), Path(pdf_path)
    checks = []
    def add(name, passed, detail):
        checks.append(dict(name=name, passed=bool(passed), severity='error', detail=detail))
    try:
        policy = json.loads((Path(__file__).parent / 'standards/document_design_standard.json').read_text())['pagination']
        document = Document(docx_path)
        for i, paragraph in enumerate(document.paragraphs):
            text = paragraph.text.strip()
            if not text:
                continue
            is_heading = paragraph.style.name.startswith('Heading') or (text.isupper() and any(c.isalpha() for c in text))
            if is_heading:
                keep = paragraph.paragraph_format.keep_with_next
                style = paragraph.style
                while keep is None and style is not None:
                    keep = style.paragraph_format.keep_with_next
                    style = style.base_style
                add(f'body.heading_keep.{i}', keep is True, text)
        blanks = []
        with fitz.open(pdf_path) as pdf:
            add('body.page_count', len(pdf) > 0 and (doc_type != 'resume' or len(pdf) <= 2) and (doc_type != 'cover' or len(pdf) == 1), f'{len(pdf)} pages')
            for number, page in enumerate(pdf, 1):
                # Exclude the full 1.28-inch header; inspect rendered body text.
                spans = [s for b in page.get_text('dict')['blocks'] if 'lines' in b for line in b['lines'] for s in line['spans'] if s['text'].strip() and s['bbox'][1] >= 92.16]
                add(f'body.content.{number}', bool(spans), 'Selectable body text required')
                if not spans:
                    continue
                fonts = sorted({s['font'] for s in spans if 'garamond' not in s['font'].lower() and s['text'].strip() not in ['•', '·', '\uf0b7']})
                add(f'body.rendered_fonts.{number}', not fonts, 'Non-Garamond text fonts: ' + repr(fonts))
                bounds_ok = all(s['bbox'][0] >= -0.5 and s['bbox'][2] <= page.rect.width + 0.5 and s['bbox'][3] <= page.rect.height + 0.5 for s in spans)
                add(f'body.page_bounds.{number}', bounds_ok, 'Rendered text must remain on the page')
                blank = (page.rect.height - max(s['bbox'][3] for s in spans)) / 72
                blanks.append(blank)
                limit = policy['max_bottom_blank_inches'].get(doc_type, 2.5)
                add(f'body.bottom_blank.{number}', blank <= limit, f'{blank:.3f} inches; maximum {limit}')
        if doc_type == 'resume' and len(blanks) > 1:
            delta = max(blanks) - min(blanks)
            limit = policy['max_resume_bottom_blank_difference_inches']
            add('body.page_balance', delta <= limit, f'Bottom-space difference {delta:.3f} inches; maximum {limit}')
    except Exception as exc:
        add('body.inspection_available', False, f'{type(exc).__name__}: {exc}')
    return {'passed': all(c['passed'] for c in checks), 'checks': checks,
            'artifact_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in [docx_path, pdf_path] if p.is_file()},
            'manual_visual_review_required': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--docx', required=True)
    parser.add_argument('--pdf', required=True)
    parser.add_argument('--doc-type', choices=['resume', 'cover', 'cv', 'bio'], default='resume')
    args = parser.parse_args()
    report = validate_body(args.docx, args.pdf, args.doc_type)
    print(json.dumps(report, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

# Troy Hokanson - Document Header Standard

**Locked May 19, 2026. Updated July 19, 2026. This is the single source of truth for every document Troy ships.**

Any resume, cover letter, CV, portfolio export, recruiter packet, professional bio, one-pager, or other artifact bearing Troy's name MUST use the locked header from this repo. No exceptions. No hand-rolled headers. No one-off deviations.

---

## Critical enforcement rule - read first

### The navy banner MUST live inside the Word document header section. NOT in the body.

- In a `.docx` file, the navy `#0D1B2A` full-bleed banner, including Troy's name, gold rule, and contact row, MUST be placed inside the document's **header section** using `doc.sections[0].header` in python-docx.
- NEVER render the navy banner as body content.
- The body of the document begins BELOW the header section, with the correct top margin applied so body text does not overlap the header.
- The `build_navy_header(doc)` function in `docx_header.py` handles this correctly. Calling it is mandatory.

Correct output:

- The header section contains the full-bleed navy banner, white name, gold rule, and gold contact row.
- The body starts cleanly below with white background and normal margins.
- No navy color appears anywhere in the body content.
- No footer is used unless Troy explicitly requests one for a specific document.

---

## Trigger keywords, auto-route to this standard

If the user request contains ANY of the following words or phrases, this header standard must be used.

**Document type triggers:** resume, résumé, cv, curriculum vitae, cover letter, application package, application docs, application materials, job package, application bundle, applicant materials, hiring packet, recruiter packet, intro letter, letter of interest, letter of intent, professional bio, biographical statement, statement of interest, candidate profile pdf, candidate profile doc, profile sheet, one-pager, leave-behind.

**File format triggers:** docx, Word doc, Word document, Microsoft Word, pdf, Adobe PDF, export PDF, save as PDF, save as Word, save as docx, page header, document header, header bar, header banner, navy header, navy bar, gold rule, gold underline, contact row, contact bar, name header.

**Action triggers:** tailor a resume, tailor a cover letter, build a resume, build a cover letter, build a cv, generate a resume, generate a cover letter, write me a resume, write me a cover letter, draft a resume, draft a cover letter, customize my resume, customize my cover letter, rebuild the resume, rebuild the cover letter, redo the header, fix the header, format the header, match the template, match the brand, apply the template, apply the brand, use the standard header, use my standard, use the locked header, navy and gold, navy/gold.

---

## Locked visual standard

| Element | Spec |
|---|---|
| Background | Full-bleed navy `#0D1B2A`, zero whitespace above, left, or right |
| Name | `Troy Hokanson`, white `#FFFFFF`, Garamond-family bold, 26 pt, centered |
| Rule | Thin gold `#C9A84C`, 0.90 pt, centered, about 55 percent page width, directly under the name |
| Contact row | Garamond, gold `#C9A84C`, centered, separator `   \|   ` |
| Contact items | Loaded from environment variables via `config.py`; `troyhokanson.com` is the final visible item |
| Subtitle | NONE. No role title between name and contact row. Ever. |
| Page 2+ PDF | Slim 0.42 inch navy bar with name only in white Garamond-family bold, 16 pt |
| Page 2+ DOCX | Same full banner repeats via section header part |
| Footer | NONE by default. Do not add a footer unless Troy explicitly requests one |
| Body top margin | 1.55 inch page 1 / 0.67 inch page 2+ for PDF. DOCX body margin is set by `build_navy_header` |

---

## Locked coordinate geometry

- The navy background is a page-relative shape measuring 612 points wide by 92.16 points high on US Letter pages.
- Name, gold rule, and contact row are centered in normal header paragraphs within symmetric section margins.
- Horizontal centering is measured against the physical page center, never against body margins, a table, a text box, or another document.
- Negative table indents and oversized tables are prohibited for header construction. They can make Word-compatible renderers center text against a shifted canvas.
- Vertical balance is measured using the complete name-rule-contact composition. Troy's name sits above the header midpoint because the rule and contact row follow it.
- `docx_header.py` is the only approved DOCX implementation. Its page-relative background is deliberately separate from its content alignment.
- Render the first page to PNG and run `header_render_validator.py`. The build fails if the top, left, or right background edge is missing or if the composition, name, or rule is more than two pixels from physical page center.
- Validate resume and cover letter independently before comparing them. Two equally shifted headers do not constitute a pass.
## ATS-first application standard

For every serious job application, build two resume tracks:

1. **ATS Resume - primary upload**
   - DOCX preferred unless the employer requires PDF.
   - No tables, text boxes, columns, floating shapes, or decorative section grids.
   - Standard headings, left-aligned body text, bullets, and plain parsing-friendly layout.
   - The locked navy header is allowed only when created by `build_navy_header(doc)`, not as a body table or text box.
   - Education must remain separate from Training and Certifications.

2. **Executive Presentation Resume - human-facing PDF**
   - May use the locked header and limited visual design.
   - Tables may be used only when they improve human readability.
   - Do not submit the table-heavy version as the primary ATS upload unless the application portal clearly preserves PDF formatting and parsing is not a concern.

3. **Cover letter**
   - Uses the locked header.
   - PDF is acceptable for human review.
   - DOCX may be used if an application portal requests editable upload.

4. **Portfolio / case examples**
   - Separate from the resume.
   - Use sanitized, role-relevant case summaries when they materially improve the application.

---

## How to use

### DOCX, resumes, cover letters, CVs in Word format

```python
import sys
sys.path.insert(0, "/home/user/workspace")
from templates.docx_header import (
    new_document, build_navy_header,
    add_section_heading, add_bullet, add_job_block,
)

doc = new_document()
build_navy_header(doc)   # writes into doc.sections[0].header, not into the body
add_section_heading(doc, "Professional Summary")
# body content below here
doc.save("output.docx")
```

After rendering page one to PNG:

```bash
python header_render_validator.py page-1.png --background "#0D1B2A" --accent "#C9A84C"
```

### PDF, resumes, cover letters, CVs in PDF format

```python
import sys
sys.path.insert(0, "/home/user/workspace")
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate
from templates.pdf_header import draw_page1_header, draw_pageN_header, MARGIN, clean_pdf_metadata

def on_first(c, d): draw_page1_header(c, LETTER)
def on_later(c, d): draw_pageN_header(c, LETTER)

doc = SimpleDocTemplate(
    out_path, pagesize=LETTER,
    leftMargin=MARGIN["left"], rightMargin=MARGIN["right"],
    topMargin=0, bottomMargin=MARGIN["bottom"],
)
doc.build(story, onFirstPage=on_first, onLaterPages=on_later)
clean_pdf_metadata(out_path, title="Resume - Troy Hokanson")
```

---

## Hard rules

1. Never hand-roll the header. Always import from `templates.docx_header` or `templates.pdf_header`.
2. The navy banner lives in the Word header section, never in the document body.
3. Never add a subtitle, role title, eyebrow, or tagline between the name and contact row.
4. The name is white Garamond-family bold, 26 pt on page 1.
5. Contact row and divider rule remain gold.
6. Never use tables, columns, or text boxes in the primary ATS resume.
7. Separate Education from Training and Certifications.
8. Never add a footer by default.
9. If the spec genuinely needs to change, edit both `docx_header.py` and `pdf_header.py`, rebuild the reference, run `header_render_validator.py` on each first-page PNG, visually check output, and commit.
10. Never approve a header merely because Word alignment properties say `center` or because the resume and cover letter match. Rendered physical-page centering controls.

---

## Repo

Public repo: https://github.com/troyhokanson/tjh-resume-cover-cv

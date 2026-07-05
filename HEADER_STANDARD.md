# Troy Hokanson - Document Header Standard

**Locked May 19, 2026. Last updated July 3, 2026. This is the single source of truth for every document Troy ships.**

Any resume, cover letter, CV, portfolio export, VA tracker print view, or other artifact bearing Troy's name MUST use the locked header from this repo. No exceptions. No hand-rolled headers. No "just this once" deviations.

---

## Critical enforcement rule - read first

### The navy banner MUST live inside the Word document header section. NOT in the body.

**This is the most commonly violated rule. Every AI session must read and enforce this before generating any DOCX.**

- In a `.docx` file, the navy `#0D1B2A` full-bleed banner, including Troy's name, gold rule, and contact row, MUST be placed inside the document's **header section** using `doc.sections[0].header` in python-docx.
- **NEVER render the navy banner as body content.** Placing it in the body makes it look like a solid navy block at the top of the page followed by a second chunk of color. That is visually broken and unprofessional.
- The body of the document begins BELOW the header section, with the correct top margin applied so body text does not overlap the header.
- The `build_navy_header(doc)` function in `docx_header.py` handles this correctly. Calling it is mandatory. Writing header HTML, table rows, or colored paragraphs into `doc.add_paragraph()` is forbidden.

**What a broken output looks like. Never do this:**
- A navy bar appears at the very top of the page.
- Then another navy or colored block immediately follows in the body with the name text inside it.
- This produces a double-banner, ugly stacked block effect.

**What the correct output looks like:**
- The header section contains the full-bleed navy banner, name, gold rule, and contact row. This repeats on every page automatically.
- The body starts cleanly below with white background and normal margins.
- No navy color appears anywhere in the body content.
- No footer is used unless Troy explicitly requests one for a specific document.

---

## Trigger keywords, auto-route to this standard

If the user request contains ANY of the following words or phrases, this header standard must be used. No matter which skill is active, no matter how the request is phrased.

**Document type triggers:**
resume, résumé, cv, curriculum vitae, cover letter, coverletter, application package, application docs, application materials, job package, application bundle, applicant materials, hiring packet, recruiter packet, intro letter, letter of interest, letter of intent, professional bio, biographical statement, statement of interest, candidate profile pdf, candidate profile doc, profile sheet, one-pager, leave-behind, attach my resume, send my resume, polish my resume, format my resume

**File format triggers:**
docx, .docx, word doc, word document, microsoft word, pdf, .pdf, adobe pdf, export pdf, save as pdf, save as word, print to pdf, save as docx, page header, document header, header bar, header banner, navy header, navy bar, gold rule, gold underline, contact row, contact bar, name header

**Action triggers:**
tailor a resume, tailor a cover letter, build a resume, build a cover letter, build a cv, generate a resume, generate a cover letter, generate a cv, write me a resume, write me a cover letter, draft a resume, draft a cover letter, draft a cv, customize my resume, customize my cover letter, rebuild the resume, rebuild the cover letter, redo the header, fix the header, format the header, fix the formatting, polish the formatting, match the template, match the brand, apply the template, apply the brand, use the standard header, use my standard, use my locked header, use the locked template, the standard one, the usual format, the same look, the brand look, navy and gold, navy + gold, navy/gold

**Format auto-routing:**

| Phrase the user says | Format to build | Module to import |
|---|---|---|
| "docx", "Word doc", "editable", "send to recruiter as Word" | DOCX | `templates.docx_header` |
| "pdf", "final", "polished", "locked version", "to upload", "for the application" | PDF | `templates.pdf_header` |
| "both", "package", "bundle", "application package", "resume + cover letter" | DOCX and PDF | both modules |
| Format not specified | DOCX by default; ask if PDF is also needed | `templates.docx_header` |

**If unsure which module to use, default to DOCX. Never hand-roll either format.**

---

## The Standard

| Element | Spec |
|---|---|
| Background | Full-bleed navy `#0D1B2A`, zero whitespace above, left, or right, entire header always navy, no exceptions |
| Name | "Troy Hokanson", Garamond-Bold 24pt, gold `#C9A84C`, centered |
| Rule | Thin gold `#C9A84C`, 0.90pt, centered, about 55% page width, directly under the name |
| Contact row | Garamond 10pt for PDF / Garamond 12pt for DOCX, gold `#C9A84C`, centered, separator `   \|   ` |
| Contact items | Loaded from environment variables via `config.py`. See `config.example.env`. Never hardcoded. |
| Subtitle | NONE. No role title between name and contact row. Ever. |
| Page 2+ PDF | Slim 0.42 inch navy bar with name only in gold Garamond-Bold 16pt |
| Page 2+ DOCX | Same full banner repeats via section header part |
| Footer | NONE by default. Do not add a footer unless Troy explicitly requests one for that document. |
| Body top margin | 1.55 inch page 1 / 0.67 inch page 2+ for PDF. DOCX body margin is set by `build_navy_header`. |

---

## How to Use

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

**Why this works:** `build_navy_header(doc)` writes the navy banner into `doc.sections[0].header`, the actual Word document header section. This means the banner is structurally separate from the body, prints on every page, and looks correct in Word, Google Docs, and PDF export. Writing banner content into `doc.add_paragraph()` is the failure mode. It will always look broken.

### PDF, resumes, cover letters, CVs in PDF format, ReportLab Platypus

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

### PDF, direct canvas for non-Platypus exports

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from templates.pdf_header import draw_page1_header

c = canvas.Canvas("out.pdf", pagesize=LETTER)
draw_page1_header(c, LETTER)
# draw body content below MARGIN["top_page1"]
c.save()
```

---

## Visual Ground Truth

`templates/reference_header.docx` should be opened side by side with any new DOCX. Page 1 must match. If it does not match, the build script is wrong, not the module.

Rebuild the reference after any module change:

```bash
cd /home/user/workspace && python3 templates/build_reference.py
```

---

## Hard Rules

1. **Never hand-roll the header.** Always import from `templates.docx_header` or `templates.pdf_header`.
2. **The navy banner lives in the Word header section, never in the document body.** If you are writing a colored paragraph, table, or any navy content via `doc.add_paragraph()` or `doc.add_table()` at the top of the body, you are doing it wrong. Stop. Use `build_navy_header(doc)`.
3. **Never add a subtitle, role title, eyebrow, or tagline between the name and contact row.** The contact row sits directly under the gold rule.
4. **The name is gold Garamond-Bold, not white.** This is now the locked default.
5. **Never use Inter for the name or Garamond for the body.** Garamond is reserved for the header name and contact row unless another spec explicitly says otherwise.
6. **Never use em dashes, en dashes, exclamation points, or VEVRAA language** anywhere in the document.
7. **Never add a footer by default.** Footer content is off unless Troy specifically asks for one.
8. **Never use `topMargin > 0` on a PDF.** The navy banner must sit flush at the top.
9. **If the spec genuinely needs to change**, edit both `docx_header.py` and `pdf_header.py`, rebuild the reference DOCX, bump the version, and commit.

---

## Repo

Public repo: https://github.com/troyhokanson/tjh-resume-cover-cv

Pull into a fresh sandbox:

```bash
git clone https://github.com/troyhokanson/tjh-resume-cover-cv
cd tjh-resume-cover-cv
cp config.example.env .env
# Edit .env and fill in real contact values
```

---

## Contact Info Setup, Multi-Device

Contact details are loaded from environment variables and never hardcoded in the public repo.

**Local machine, any device:**
1. Copy `config.example.env` to `.env` in the repo root.
2. Fill in real values.
3. The `.env` file is gitignored and will never be committed.

**GitHub Actions automated builds:**
Add these secrets under Settings, Secrets and variables, Actions:

- `TROY_PHONE`, e.g. `612.555.0000`
- `TROY_EMAIL`, e.g. `TroyHokanson@iCloud.com`
- `TROY_LOCATION`, e.g. `Lakeville, MN`
- `TROY_LINKEDIN`, e.g. `linkedin.com/in/troyhokanson`
- `TROY_PORTFOLIO`, e.g. `https://troy-hokanson.github.io/portfolio/`
- `TROY_NAME`, e.g. `Troy Hokanson`

Builds run on any device or via Actions will inject the real values into every document header automatically.

---

## Skill Enforcement

These skills enforce the standard at the top of their instructions and must never be bypassed:

- `linkedin-profile-optimizer`, resumes, cover letters, CVs, LinkedIn-adjacent docs
- `investigator-portfolio-website-optimizer`, printable case-study exports, portfolio PDFs
- `resume-file-router`, validation gate before OneDrive export
- `va-disability-tracker`, any printable claim-package artifact

If you are working in any of these skills and you are tempted to write header code from scratch, stop and import from this repo instead.

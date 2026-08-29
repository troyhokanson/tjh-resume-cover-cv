# Troy Hokanson — Document Templates for Investigative Job Search - Microsoft Word or PDF Format.

**SINGLE SOURCE OF TRUTH** for every Troy Hokanson resume, cover letter, CV, recruiter packet, professional bio, one-pager, or any DOCX/PDF document bearing his name. This repo MUST be cloned into `/home/user/workspace/templates/` (via symlink) at the start of every application build session — automatically, no exceptions.

This repo separates hard safeguards from role-specific authoring choices:

1. **Role adaptation and LLM autonomy** — ROLE_ADAPTATION_STANDARD.md requires posting-led wording, evidence, structure, and formatting for SIU, corporate security, customer success, technical account management, DFIR/cyber, intelligence, and solutions roles.
2. **Headline and scanability** — RESUME_HEADLINE_SCANABILITY_STANDARD.md requires a truthful role-aligned headline by default, a concise opening, verified metric placement, relevance-based compression of older work, and readable one- or two-page length.
3. **ATS and presentation formats** — HEADER_STANDARD.md supports a plain text-first ATS header or the navy/gold branded presentation header.
4. **Body typography and pagination** — standards/body_typography_pagination_standard.md and standards/document_design_standard.json require Garamond-family body styling, steel-blue section headings with restrained gold rules, and no orphaned headings or job blocks.
5. **Voice guardrails** — VOICE_STANDARD.md preserves Troy's direct, specific, human voice without forcing one career identity or opening formula.
6. **PTSD-safe scope and privacy hard blocks** — PRIVACY_STANDARD.md and anti_ai_scan.py prohibit POST / peace-officer licensing identifiers, badge numbers, case identifiers, and other unnecessary public-facing data.
7. **Case evidence and ECTF crosswalk control** — CASE_EVIDENCE_REVIEW_STANDARD.md requires exact source matching, role reconciliation, duplicate-view control, and an explicit unresolved status when an ECTF number cannot be verified.
8. **ATS keyword coverage and truth** — ats_injector.py audits against the job description, but terms may be used only when supported by Troy's verified record.
9. **Mandatory final validator** — validate_application_packet.py is the final delivery gate. A document is not ready unless this validator passes.

Seven primary lanes are defined: `vendor-solutions`, `siu-fraud`, `analyst-intelligence`, `corporate-security-investigations`, `customer-success`, `technical-account-management`, and `dfir-cyber`. The scanner uses `adaptive` if no lane is supplied, but each final application should log a selected primary lane.

If you are about to build a Hokanson document and this repo is not present in the workspace, STOP and clone it first.

---

## Automatic Trigger Rule

Any time Troy uploads, pastes, summarizes, or references a job description and asks to draft, build, tailor, revise, update, format, or prepare a resume, cover letter, CV, professional bio, candidate profile, recruiter packet, or application materials, that request is a **formal application build**.

A formal application build automatically requires:

1. Read the job posting completely.
2. Select one primary role lane and record the rationale.
3. Draft the ATS version and, when useful, the branded presentation version.
4. Separate Education from Training and Certifications.
5. Use the locked header when a branded copy is requested or appropriate.
6. Use Garamond-family body, heading, subheading, and job-block styling.
7. Prevent orphaned headings, subheadings, employer/title lines, and job blocks.
8. Render DOCX to PDF.
9. Render every PDF page to PNG.
10. Run `validate_application_packet.py` against every final document.
11. Save the JSON validation reports with the application files.
12. Do not deliver, share, upload, or mark the packet Ready unless the validator passes.

This rule is mandatory. The user should not have to separately ask for the anti-AI scan, privacy scan, header check, body typography check, pagination check, or Drive save.

---

## Starting a New Application

**You do not need to remember the workflow. Run one command:**

```bash
bash new_application.sh
```

It will ask for the job description file path, selected profile, employer name, and role name, then:
- Extract the high-signal ATS keywords from the job description automatically
- Save a dated ATS audit report to `build_logs/`
- Print the mandatory final validation commands
- Print the exact prompt to paste into an AI session to build the documents

The script starts the process. The build is not complete until `validate_application_packet.py` passes on the final files.

### Manual ATS audit

```bash
python ats_injector.py \
  --jd job_description.txt \
  --resume Hokanson_Resume_XYZ.docx \
  --cover Hokanson_Cover_XYZ.docx \
  --profile siu-fraud \
  --output build_logs/ats_audit.txt
```

Exit code `0` = 85%+ coverage. Exit code `1` = below floor, fix before sending.

### Mandatory final validator

Use this after the DOCX has been rendered to PDF and the PDF pages have been rendered to PNG.

```bash
python validate_application_packet.py \
  --docx output/Hokanson_Resume_Employer_Role_BRANDED.docx \
  --pdf output/Hokanson_Resume_Employer_Role_BRANDED.pdf \
  --header-png output/rendered_resume/page-1.png \
  --header-png output/rendered_resume/page-2.png \
  --doc-type resume \
  --profile analyst-intelligence \
  --json-out build_logs/validate_resume_Employer_Role.json

python validate_application_packet.py \
  --docx output/Hokanson_Cover_Employer_Role_BRANDED.docx \
  --pdf output/Hokanson_Cover_Employer_Role_BRANDED.pdf \
  --header-png output/rendered_cover/page-1.png \
  --doc-type cover \
  --profile analyst-intelligence \
  --json-out build_logs/validate_cover_Employer_Role.json
```

The validator checks anti-AI language, privacy patterns, POST/license suppression, blocked PTSD-scope terms, role-lane wrong-language, Garamond-family styling, Word header placement, navy/gold header markers, rendered header edges, and page-tail orphan headings.

---

## How the ATS injector works

- Extracts single-word and two-word phrase keywords from any raw JD text, weighted by frequency
- Checks which terms are already present in your built resume and cover letter
- Reports coverage percentage vs. the 85% floor target
- `inject_into_summary()` and `inject_into_skills()` helpers let build scripts auto-weave missing terms
- **Never overclaims:** profile-specific skip lists block terms Troy cannot legitimately claim, such as Salesforce, Tableau, or underwriting authority for SIU targets
- **Never violates VOICE_STANDARD:** Layer 1 banned phrases and PTSD-scope hard block are enforced at injection time
- See `ats_injector.py` for full documentation

---

## Repository Structure

```
tjh-resume-cover-cv/
├── config.py                                # Contact info loader, reads env vars, never hardcoded
├── config.example.env                       # Copy to .env and fill in real values
├── docx_header.py                           # Locked DOCX header builder + body helpers
├── pdf_header.py                            # Locked PDF page-1 header renderer
├── anti_ai_scan.py                          # Voice/anti-AI enforcement gate
├── validate_application_packet.py           # Mandatory final delivery validator
├── ats_injector.py                          # ATS keyword extraction, audit, and injection engine
├── new_application.sh                       # One-command new application starter
├── scan_and_report.py                       # Friendly anti-AI wrapper
├── build_reference.py                       # Rebuilds reference_header.docx after any header change
├── reference_header.docx                    # Visual ground truth, diff against every new build
├── requirements.txt                         # Python dependencies
├── build_logs/                              # ATS and validation audit reports, gitignored
├── fonts/
│   └── README.md                            # Font installation guide, EB Garamond, Inter
├── tests/
│   ├── test_anti_ai_scan.py                 # Unit tests for scan rules
│   └── test_config.py                       # Tests for env-var loading and safe fallbacks
├── standards/
│   ├── document_design_standard.json        # Machine-readable visual/body/pagination standard
│   └── body_typography_pagination_standard.md # Human-readable body typography standard
├── CASE_BANK.md                             # Source-of-truth case examples
├── CASE_EVIDENCE_REVIEW_STANDARD.md          # Mandatory case-source and ECTF crosswalk workflow
├── ROLE_ADAPTATION_STANDARD.md              # Posting-led authoring and formatting autonomy
├── RESUME_HEADLINE_SCANABILITY_STANDARD.md  # Headline, summary, length, recency, metrics, and ATS rules
├── HEADER_STANDARD.md                       # ATS and branded presentation layout options
├── VOICE_STANDARD.md                        # Voice, truth, and privacy guardrails
├── PRIVACY_STANDARD.md                      # Privacy suppression rules
├── PROFILES.md                              # Layer 2 profile definitions
├── PROFILE_SELECTOR.md                      # Decision tree, pick the right profile from a job posting
├── SYSTEM_PROMPT.md                         # Copy-paste system prompt for custom AI setups
├── PLATFORM_SETUP.md                        # Configure ChatGPT, Claude, Gemini, etc.
└── chatgpt_action_schema.json               # OpenAPI schema for ChatGPT Actions
```

---

## Quick Start

```bash
# 1. Clone and set up
git clone https://github.com/troyhokanson/tjh-resume-cover-cv
cd tjh-resume-cover-cv
pip install -r requirements.txt

# 2. Configure contact info, never hardcoded
cp config.example.env .env
# Edit .env and fill in real values

# 3. Verify imports work
python -c "from docx_header import build_navy_header, new_document; print('OK')"
python -c "from pdf_header import draw_page1_header; print('OK')"
python -c "from anti_ai_scan import scan_pdf; print('OK')"
python -c "from ats_injector import ATSInjector; print('OK')"
python -c "import validate_application_packet; print('OK')"

# 4. Run the test suite
python -m pytest tests/ -v

# 5. Build the visual reference DOCX
python build_reference.py
```

---

## Usage in a build script

```python
import sys
sys.path.insert(0, "/home/user/workspace")
from templates.docx_header import (
    new_document, build_navy_header,
    add_section_heading, add_bullet, add_job_block,
    set_run, set_paragraph_format,
    BODY_FONT, NAME_FONT, NAVY, GOLD, STEEL, BLACK, GRAY, WHITE,
)

doc = new_document()
build_navy_header(doc)
add_section_heading(doc, "Professional Summary")
# body content using add_bullet, add_job_block, etc.
doc.save("/home/user/workspace/output/Hokanson_Resume_Employer_Role.docx")
```

Every build script must finish by rendering the DOCX, rendering page PNGs, and running `validate_application_packet.py`. `scan_pdf` alone is no longer enough for final delivery because it does not check Garamond styling, rendered header edges, or orphaned job headings.

---

## Files

- `new_application.sh` — start here for every new application. One command. Handles the ATS audit and prints the mandatory final validator commands.
- `validate_application_packet.py` — final delivery checklist. Hard-blocks failed application packets.
- `ats_injector.py` — ATS keyword extraction, coverage audit, and injection engine.
- `docx_header.py` — branded navy/gold header builder + shared body helpers. Import it when a branded presentation copy is selected. Never hand-roll the branded header.
- `pdf_header.py` — locked PDF page-1 header renderer.
- `reference_header.docx` — visual ground truth. Diff against page 1 of every new build.
- `build_reference.py` — rebuilds the reference DOCX after any header change.
- `standards/document_design_standard.json` — machine-readable visual, typography, and pagination standard.
- `standards/body_typography_pagination_standard.md` — human-readable Garamond and pagination standard.
- `HEADER_STANDARD.md` — locked layout specification.
- `CASE_BANK.md` — quantified case examples with resume, cover-letter, and interview language. Pull from here, never rewrite from memory.
- `CASE_EVIDENCE_REVIEW_STANDARD.md` — mandatory source hierarchy, role verification, privacy controls, and exact ECTF crosswalk workflow for every relevant case review.
- `anti_ai_scan.py` — voice and anti-AI rules. Still required, but now called through the full validator.
- `ROLE_ADAPTATION_STANDARD.md` — posting-led identity, wording, structure, evidence, and format choices.
- `VOICE_STANDARD.md` — direct, precise, human voice rules.
- `PRIVACY_STANDARD.md` — privacy and identifier suppression rules.
- `requirements.txt` — Python dependencies.
- `fonts/README.md` — instructions for installing EB Garamond and Inter fonts locally.
- `tests/` — unit tests for scan engine and config loader.

---

## Locked spec

- Full-bleed navy `#0D1B2A` bar, zero whitespace above, left, or right.
- Navy header must live in the Word document header section, not the body.
- `Troy Hokanson` in white Garamond-family bold, centered.
- Inset gold `#C9A84C` horizontal rule.
- Single gold contact row beneath, pipe-separated.
- No subtitle or role title between name and contact row.
- Body, headings, subheadings, job headings, date lines, and bullets use Garamond-family styling.
- Section headings use steel blue `#2D6A9F` with restrained gold underline.
- No orphaned section headings, subheadings, employer/title lines, or job headings.
- No Adjunct Faculty or other job block may start at the bottom of a page without related content following on that same page.
- Education remains separate from Training and Certifications.

---

## Contact Info Setup, Multi-Device

Contact details are **never hardcoded** in this repo. They are loaded from environment variables at build time.

**Local machine:**
1. Copy `config.example.env` to `.env` in the repo root: `cp config.example.env .env`
2. Fill in real values. The `.env` file is gitignored and will never be committed.
3. Run any build script normally. `config.py` loads `.env` automatically.

**GitHub Actions:**
Add these secrets under Settings → Secrets and variables → Actions:
- `TROY_PHONE`
- `TROY_EMAIL`
- `TROY_LOCATION`
- `TROY_LINKEDIN`
- `TROY_PORTFOLIO`

---

## To pull into a fresh sandbox

```bash
cd /home/user/workspace
gh repo clone troyhokanson/tjh-resume-cover-cv
ln -sfn /home/user/workspace/tjh-resume-cover-cv /home/user/workspace/templates
pip install -r templates/requirements.txt
```

After clone, verify imports work and run the validator before delivery.
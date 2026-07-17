# Troy Hokanson — Document Templates for Investigative Job Search - Microsoft Word or PDF Format.

**SINGLE SOURCE OF TRUTH** for every Troy Hokanson resume, cover letter, CV, recruiter packet, professional bio, one-pager, or any DOCX/PDF document bearing his name. This repo MUST be cloned into `/home/user/workspace/templates/` (via symlink) at the start of every application build session — automatically, no exceptions.

This repo enforces five locked standards:

1. **Authoritative fact routing and writeback** — `SOURCE_OF_TRUTH_ROUTING.md` and `AGENTS.md` require every verified correction, clarification, credential, award, metric, or reusable language improvement to be committed to the correct source file before an application is finalized.
2. **Navy/gold header layout** — `HEADER_STANDARD.md`, `DOCX_NODE_STANDARD.md`, `docx_header.py`, and `pdf_header.py`.
3. **Anti-AI / voice rules** — two layers: Layer 1 hard rules in `VOICE_STANDARD.md` and Layer 2 audience profiles in `PROFILES.md`. Enforced by `anti_ai_scan.py`. Pick the right profile using `PROFILE_SELECTOR.md`.
4. **PTSD-safe scope and writing voice** — linked from `VOICE_STANDARD.md`.
5. **ATS keyword coverage** — `ats_injector.py` audits every build against the job description and flags missing terms before documents are sent.

Three profiles are defined: `vendor-solutions` (default — Solutions Consultant, Sales Engineer, Public Safety Manager), `siu-fraud` (SIU Investigator, Insurance Fraud Investigator), and `analyst-intelligence` (Investigations and Intelligence Analyst, Financial Crime Analyst). The scan defaults to `vendor-solutions` if no profile is specified.

If you are about to build a Hokanson document and this repo is not present in the workspace, STOP and clone it first.

---

## Starting a New Application

**You do not need to remember the workflow. Run one command:**

```bash
bash new_application.sh
```

It will ask you three questions (JD file path, profile, employer/role name) and then:
- Extract the high-signal ATS keywords from the job description automatically
- Check coverage against any existing resume/cover docs you point to
- Print the missing keywords you need to weave in
- Save a dated audit report to `build_logs/`
- Print the exact prompt to paste into your AI session to build the documents

**That's it.** The script handles the rest. You do not need to remember command flags.

### Mandatory source-of-truth writeback

Before any application package is treated as complete:

1. Read `SOURCE_OF_TRUTH_ROUTING.md`.
2. Identify every new, corrected, clarified, or improved reusable fact or description developed during the build.
3. Update the correct authoritative source on the same branch or pull request.
4. Update the application-specific Markdown and generated documents from that source.
5. Verify that the authoritative source and tailored application agree.
6. Report the authoritative file and commit or pull request.

Application folders are outputs, not permanent fact stores. Do not leave reusable information only in chat history, an application Markdown file, a DOCX/PDF, a pull-request description, or a correction sidecar.

### Manual ATS audit (if you prefer)

```bash
# Save the job description as a .txt file, then:
python ats_injector.py \
  --jd job_description.txt \
  --resume Hokanson_Resume_XYZ.docx \
  --cover Hokanson_Cover_XYZ.docx \
  --profile siu-fraud \
  --output build_logs/ats_audit.txt
```

Exit code `0` = 85%+ coverage (good to send). Exit code `1` = below floor (fix before sending).

### How the ATS injector works

- Extracts single-word and two-word phrase keywords from any raw JD text, weighted by frequency
- Checks which terms are already present in your built resume and cover letter
- Reports coverage percentage vs. the 85% floor target
- `inject_into_summary()` and `inject_into_skills()` helpers let build scripts auto-weave missing terms
- **Never overclaims:** profile-specific skip lists block terms Troy cannot legitimately claim (e.g. Salesforce, Tableau, underwriting authority for `siu-fraud` targets)
- **Never violates VOICE_STANDARD:** Layer 1 banned phrases and PTSD-scope hard block are enforced at injection time
- See `ats_injector.py` for full documentation

---

## Repository Structure

```text
tjh-resume-cover-cv/
├── AGENTS.md                         # Mandatory AI-agent read order and writeback rule
├── SOURCE_OF_TRUTH_ROUTING.md        # Routes every reusable fact to its authoritative file
├── CAREER_CONSTANTS.md               # Employment, dates, titles, role boundaries, and locked career facts
├── TEACHING_FACULTY_CONSTANTS.md     # Teaching history, degrees, GPAs, faculty credentials, and recognition
├── CASE_BANK.md                      # Source-of-truth investigative cases and outcomes
├── config.py                         # Contact info loader — reads env vars, never hardcoded
├── config.example.env                # Copy to .env and fill in real values
├── docx_header.py                    # Locked DOCX header builder + body helpers
├── pdf_header.py                     # Locked PDF page-1 header renderer
├── anti_ai_scan.py                   # Automatic voice/anti-AI enforcement gate
├── ats_injector.py                   # ATS keyword extraction, audit, and injection engine
├── new_application.sh                # One-command new application starter
├── scan_and_report.py                # Friendly wrapper — run at the share-file delivery gate
├── build_reference.py                # Rebuilds reference_header.docx after header changes
├── reference_header.docx             # Visual ground truth — diff against every new build
├── requirements.txt                  # Python dependencies
├── skills/
│   └── troy-credentials-library/
│       └── credentials_catalog.json  # Machine-readable professional training and credentials
├── standards/
│   └── document_design_standard.json # Machine-readable document design standard
├── build_logs/                       # ATS audit reports (auto-created, gitignored)
├── fonts/
│   └── README.md                     # Font installation guide
├── tests/
│   ├── test_anti_ai_scan.py          # Unit tests for scan rules
│   └── test_config.py                # Tests for env-var loading and safe fallbacks
├── HEADER_STANDARD.md                # Locked layout specification
├── DOCX_NODE_STANDARD.md             # Locked Node.js DOCX implementation standard
├── VOICE_STANDARD.md                 # Layer 1 hard rules
├── PROFILES.md                       # Layer 2 profile definitions
├── PROFILE_SELECTOR.md               # Decision tree — pick the right profile
├── SYSTEM_PROMPT.md                  # Copy-paste system prompt for custom AI setups
├── PLATFORM_SETUP.md                 # Configure ChatGPT, Claude, Gemini, etc.
└── chatgpt_action_schema.json         # OpenAPI schema for ChatGPT Actions
```

---

## Quick Start

```bash
# 1. Clone and set up
git clone https://github.com/troyhokanson/tjh-resume-cover-cv
cd tjh-resume-cover-cv
pip install -r requirements.txt

# 2. Configure contact info (never hardcoded — kept out of the repo)
cp config.example.env .env
# Edit .env and fill in real values

# 3. Verify imports work
python -c "from docx_header import build_navy_header, new_document; print('OK')"
python -c "from pdf_header import draw_page1_header; print('OK')"
python -c "from anti_ai_scan import scan_pdf; print('OK')"
python -c "from ats_injector import ATSInjector; print('OK')"

# 4. Run the delivery-gate scan on a built document
python scan_and_report.py /path/to/Hokanson_Cover_ThomsonReuters.pdf cover
python scan_and_report.py /path/to/Hokanson_Cover_GEICO_SIU.pdf cover --profile siu-fraud
python scan_and_report.py /path/to/Hokanson_Resume_Stripe_Analyst.pdf resume --profile analyst-intelligence

# 5. Run the test suite
python -m pytest tests/ -v

# 6. Build the visual reference DOCX
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
# ... body content using add_bullet, add_job_block, etc.
doc.save("/home/user/workspace/output/Hokanson_Resume_Employer_Role.docx")

# Convert to PDF, then run the MANDATORY anti-AI / voice scan
import subprocess
subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf",
                "--outdir", "/home/user/workspace/output",
                "/home/user/workspace/output/Hokanson_Resume_Employer_Role.docx"],
               check=True, capture_output=True)

from templates.anti_ai_scan import scan_pdf
scan_pdf("/home/user/workspace/output/Hokanson_Resume_Employer_Role.pdf",
         doc_type="resume")   # raises FailedScan if any violation
```

**Every `build_*.py` script must end with the `scan_pdf` call.** Skipping the scan is not allowed.

---

## Files

- `SOURCE_OF_TRUTH_ROUTING.md` — mandatory routing and writeback standard. Read first for every build.
- `AGENTS.md` — hard instructions for AI agents and automation operating in the repo.
- `CAREER_CONSTANTS.md` — authoritative employment, role, and date facts. Never improvise from memory.
- `TEACHING_FACULTY_CONSTANTS.md` — authoritative teaching history, degrees, GPAs, faculty development, and teaching recognition.
- `skills/troy-credentials-library/credentials_catalog.json` — machine-readable professional training and credential source.
- `new_application.sh` — **start here for every new application.** One command. Handles the ATS audit and prints the next steps.
- `ats_injector.py` — ATS keyword extraction, coverage audit, and injection engine. Called by `new_application.sh` automatically.
- `docx_header.py` — locked header builder + shared body helpers. Import this in every build script. Never hand-roll the header.
- `pdf_header.py` — locked PDF page-1 header renderer.
- `reference_header.docx` — visual ground truth. Diff against page 1 of every new build.
- `build_reference.py` — rebuilds the reference DOCX after any header change.
- `HEADER_STANDARD.md` — locked layout specification.
- `CASE_BANK.md` — quantified case examples with resume, cover-letter, and interview language. Pull from here, never rewrite from memory.
- `anti_ai_scan.py` — automatic enforcement of voice and anti-AI rules. Called at the bottom of every `build_*.py` script.
- `VOICE_STANDARD.md` — Troy's permanent voice standard.
- `requirements.txt` — Python dependencies.
- `fonts/README.md` — font installation instructions.
- `tests/` — unit tests for the scan engine and configuration loader.

---

## Locked spec

- Full-bleed navy `#0D1B2A` bar, ZERO whitespace above
- `Troy J. Hokanson` in white Garamond-Bold, 26 pt on page 1
- Inset gold `#C9A84C` horizontal rule
- Single gold contact row beneath, pipe-separated
- No subtitle or role title between name and contact row
- Section headings: steel-blue `#2D6A9F` with gold underline rule

---

## Contact Info Setup (Multi-Device)

Contact details are **never hardcoded** in this repo. They are loaded from environment variables at build time.

**Local machine:**
1. Copy `config.example.env` to `.env`.
2. Fill in the real values.
3. Run the build script normally; `.env` is gitignored.

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

After clone, verify imports work:

```python
from templates.docx_header import build_navy_header, new_document
from templates.pdf_header import draw_page1_header
from templates.anti_ai_scan import scan_pdf
from templates.ats_injector import ATSInjector
```

---

## Running Tests

```bash
python -m pytest tests/ -v
```

Tests cover:
- forbidden phrases and AI clichés
- punctuation rules
- cover-letter structural rules
- resume/CV contraction rules
- PTSD-scope guard
- VEVRAA language guard
- configuration loading and safe fallbacks

---

## Changing a locked standard

When a locked standard changes:

1. Update the authoritative standard file.
2. Update any machine-readable companion standard or implementation.
3. Rebuild or rerun the applicable validation artifact.
4. Run the test suite.
5. Commit the authoritative update and downstream changes on the same branch or pull request.
6. Identify the changed source-of-truth file in the handoff.
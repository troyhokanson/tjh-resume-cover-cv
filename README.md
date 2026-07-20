# Troy Hokanson — Document Templates for Investigative Job Search - Microsoft Word or PDF Format.

**SINGLE SOURCE OF TRUTH** for every Troy Hokanson resume, cover letter, CV, recruiter packet, professional bio, one-pager, or any DOCX/PDF document bearing his name. This repo MUST be cloned into `/home/user/workspace/templates/` (via symlink) at the start of every application build session — automatically, no exceptions.

This repo enforces four locked standards:

1. **Navy/gold header layout** (HEADER_STANDARD.md, docx_header.py, pdf_header.py)
2. **Anti-AI / voice rules** — two layers: Layer 1 hard rules in VOICE_STANDARD.md and Layer 2 audience profiles in PROFILES.md. Enforced by anti_ai_scan.py. Pick the right profile using PROFILE_SELECTOR.md.
3. **PTSD-safe scope and writing voice** (linked from VOICE_STANDARD.md)
4. **ATS keyword coverage** — ats_injector.py audits every build against the job description and flags missing terms before documents are sent.

Before choosing a writing profile or starting an application, use [`CAREER_STRATEGY.md`](./CAREER_STRATEGY.md) to decide whether the opportunity advances Troy's primary public-safety technology vendor goal, the parallel investigations lane, or a selective leadership lane. It also contains the job-scoring framework, weekly priorities, learning priorities, and the rule for deciding when CFE study supports or distracts from the primary goal.

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

```
tjh-resume-cover-cv/
├── config.py               # Contact info loader — reads env vars, never hardcoded
├── config.example.env      # Copy to .env and fill in real values
├── docx_header.py          # Locked DOCX header builder + body helpers
├── pdf_header.py           # Locked PDF page-1 header renderer
├── anti_ai_scan.py         # Automatic voice/anti-AI enforcement gate (Layer 1 + Layer 2)
├── ats_injector.py         # ATS keyword extraction, audit, and injection engine
├── new_application.sh      # One-command new application starter (run this first)
├── scan_and_report.py      # Friendly wrapper — run at the share-file delivery gate
├── build_reference.py      # Rebuilds reference_header.docx after any header change
├── reference_header.docx   # Visual ground truth — diff against every new build
├── requirements.txt        # Python dependencies
├── build_logs/             # ATS audit reports (auto-created, gitignored)
├── fonts/
│   └── README.md           # Font installation guide (EB Garamond, Inter)
├── tests/
│   ├── test_anti_ai_scan.py  # 80+ unit tests for every scan rule
│   └── test_config.py        # Tests for env-var loading and safe fallbacks
├── CASE_BANK.md            # Source-of-truth case examples (Condello Wall, Garwood, Lakeville, BEC, etc.)
├── CAREER_STRATEGY.md       # Job-search priorities, role-fit scorecard, learning plan, and CFE decision rule
├── HEADER_STANDARD.md      # Locked layout specification
├── VOICE_STANDARD.md       # Layer 1 hard rules (apply to every document, every profile)
├── PROFILES.md             # Layer 2 profile definitions (vendor-solutions, siu-fraud, analyst-intelligence)
├── PROFILE_SELECTOR.md     # Decision tree — pick the right profile from a job posting
├── SYSTEM_PROMPT.md        # Copy-paste system prompt for custom AI setups
├── PLATFORM_SETUP.md       # How to configure ChatGPT, Claude, Gemini, etc.
└── chatgpt_action_schema.json  # OpenAPI schema for ChatGPT Actions
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

- `new_application.sh` — **start here for every new application.** One command. Handles the ATS audit and prints the next steps.
- `ats_injector.py` — ATS keyword extraction, coverage audit, and injection engine. Called by new_application.sh automatically.
- `docx_header.py` — the locked header builder + shared body helpers. Import this in every build script. Never hand-roll the header.
- `pdf_header.py` — locked PDF page-1 header renderer.
- `reference_header.docx` — visual ground truth. Diff against page 1 of every new build.
- `build_reference.py` — rebuilds the reference DOCX after any header change.
- `HEADER_STANDARD.md` — locked layout specification.
- `CASE_BANK.md` — all quantified case examples with resume bullet, condensed bullet, cover letter paragraph, and interview talking points for each. Pull from here, never rewrite from memory.
- `anti_ai_scan.py` — **automatic enforcement** of the voice and anti-AI rules. Called at the bottom of every `build_*.py` script. Hard-blocks any document that fails.
- `VOICE_STANDARD.md` — Troy's permanent voice standard (54-year-old Gen-X retired detective, Master's-educated, empathetic / humanistic, investigations-experienced).
- `requirements.txt` — Python dependencies. Install with `pip install -r requirements.txt`.
- `fonts/README.md` — Instructions for installing EB Garamond and Inter fonts locally.
- `tests/` — Unit tests for the scan engine and config loader. Run with `python -m pytest tests/ -v`.

---

## Locked spec (matches UHG reference April 2026)

- Full-bleed navy `#0D1B2A` bar, ZERO whitespace above (sits in section page header part)
- `Troy J. Hokanson` in WHITE Garamond-Bold ~28pt, mixed case, centered
- INSET gold `#C9A84C` horizontal rule (not edge-to-edge)
- Single gold contact row beneath, pipe-separated
- NO subtitle / role title between name and contact row
- Section headings: steel-blue `#2D6A9F` with gold underline rule

---

## Contact Info Setup (Multi-Device)

Contact details (phone, email, location) are **never hardcoded** in this repo. They are loaded from environment variables at build time.

**Local machine (any device):**
1. Copy `config.example.env` to `.env` in the repo root: `cp config.example.env .env`
2. Fill in your real values — the `.env` file is gitignored and will never be committed
3. Run any build script normally; `config.py` loads `.env` automatically

**GitHub Actions (automated builds):**
Add these secrets under Settings → Secrets and variables → Actions:
- `TROY_PHONE` — e.g. `612.555.0000`
- `TROY_EMAIL` — e.g. `TroyHokanson@iCloud.com`
- `TROY_LOCATION` — e.g. `Lakeville, MN`
- `TROY_LINKEDIN` — e.g. `linkedin.com/in/troyhokanson`
- `TROY_PORTFOLIO` — e.g. `https://troy-hokanson.github.io/portfolio`

---

## To pull into a fresh sandbox (AUTOMATIC at session start)

```bash
cd /home/user/workspace
gh repo clone troyhokanson/troy-hokanson-resume-cover-cv
ln -sfn /home/user/workspace/troy-hokanson-resume-cover-cv /home/user/workspace/templates
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
# From the repo root (no symlink needed — tests import directly)
python -m pytest tests/ -v

# From the workspace root (templates/ symlink layout)
python -m pytest templates/tests/ -v
```

Tests cover:
- All 50+ forbidden phrases and extra-flagged AI clichés
- All punctuation rules (em dash, en dash, exclamation, ellipsis, curly quotes)
- Cover-letter structural rules (closing, contraction cap, semicolons)
- Resume/CV contraction rules
- PTSD-scope guard
- VEVRAA language guard
- Config env-var loading and safe fallbacks

---

## Changing the locked spec

If the header style genuinely needs to change:
1. Edit `docx_header.py`
2. Run `python3 build_reference.py` to rebuild the reference
3. Visually diff against the prior reference
4. Run the test suite: `python -m pytest tests/ -v`
5. Commit and push: `git add -A && git commit -m "Header change: <reason>" && git push`

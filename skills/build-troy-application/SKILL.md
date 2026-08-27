---
name: build-troy-application
description: Canonical end-to-end application builder for Troy Hokanson. Triggers on @build-troy-application, career-application-builder, build my application, draft or update my resume, cover letter, CV, candidate profile, expert-network profile, contractor one-pager, role-fit assessment, application packet, I am going to apply, let's give this role a shot, or any request to create or revise Troy's application materials. Orchestrates exact-job verification, GitHub standards, verified evidence, fit and gap analysis, ATS targeting, DOCX/PDF generation, anti-AI and privacy validation, visual inspection, authorized Google Drive filing, GitHub packaging, Notion tracking, and completion reporting. This is the controlling skill; supporting skills provide evidence or specialist checks but may not bypass its gates.
---

# Build Troy Application

## Purpose

This is the single controlling workflow for every Troy Hokanson job application. It combines the former career-application-builder concept with the `build-troy-application` trigger so there is one authoritative process, one completion gate, and one cross-system status.

The skill coordinates research, evidence selection, drafting, document production, validation, filing, tracking, and final reporting. It does not invent experience and does not mark an application submitted without confirmation.

## Candidate Boundary

This skill is only for Troy Hokanson.

Authoritative repository:

```text
troyhokanson/tjh-resume-cover-cv
```

Never use Melissa Hokanson's facts, documents, repository, metrics, application records, or role guidance. Melissa's workflow remains separate in `troy-hokanson/auditorsearchbot` and `build-melissa-application`.

## Trigger Behavior

Any request to draft, create, update, tailor, rebuild, or review Troy's resume, cover letter, CV, candidate profile, one-pager, role-fit assessment, or application packet automatically starts the applicable drafting and validation workflow. GitHub, Drive, and Notion writes occur only when the user authorizes those systems for the request.

Recognized entry points include:

- `@build-troy-application`
- `career-application-builder`
- `build the application packet`
- `draft my resume and cover letter`
- `I am going to apply`
- `let's give this role a shot`
- `update my resume for this posting`

## Governing Sources

Before drafting, read the current repository versions of all applicable standards. At minimum:

- `HEADER_STANDARD.md`
- `CONTACT_STANDARD.md`
- `VOICE_STANDARD.md`
- `ROLE_FAMILIES.md`
- `ROLE_ADAPTATION_STANDARD.md`
- `PROFILE_SELECTOR.md`
- `PROFILES.md`
- `PRIVACY_STANDARD.md`
- `EDUCATION_CONSTANTS.md`
- `CAREER_CONSTANTS.md`
- `SKILLS_CONSTANTS.md`
- `TRAINING_CONSTANTS.md`
- `DOCX_NODE_STANDARD.md`
- `CASE_BANK.md`
- `awards_comm_perf_reviews.md`
- `PUBLIC_SAFETY_TECHNOLOGY_INVENTORY.md` when relevant
- `anti_ai_scan.py`
- `validate_application_packet.py`
- `delivery_gate.py` when present on the active branch

Load relevant supporting skills when needed, including:

- `skills/troy-credentials-library/SKILL.md`
- `skills/cert-comm-extractor/SKILL.md`
- any current role-family, evidence, document, ATS, or routing skills found in the repository

Repository content controls over memory. When a conflict exists, pause the affected claim, identify the conflicting sources, and use the safest verified wording until resolved.

Use `references/standards-map.md` for precedence. Do not describe Troy's strategy as a single-role pivot; select from the canonical role families.

## Required Workflow

### Phase 1: Exact Opportunity Resolution

Resolve and record:

- candidate: Troy Hokanson
- employer
- exact job title
- requisition or job ID
- official job URL
- location
- work mode
- salary range
- posting date
- application deadline when stated
- travel requirement
- complete job description

Use the official employer posting whenever available. Do not substitute a similar role. Archive the complete description, not only a summary.

If the official posting cannot be confirmed, keep the application in `Researching` or `Drafting`. Never call it Ready to Submit.

### Phase 2: Application Workspace

Perform cross-system workspace creation only when the user has authorized Drive, GitHub, and Notion for the request. Otherwise keep the package local and mark those publication checks not authorized.

Create or confirm the dated Google Drive folder under `09_Applications` using:

```text
YYYY-MM-DD Company Role
```

Archive the official job description and source URL in that folder. Use Troy's application area, not Melissa's.

Create or locate the corresponding GitHub application package using a stable sanitized folder name.

Create or locate one matching Notion Applications record. Do not create duplicate records for the same requisition.

### Phase 3: Role Lane and Fit Analysis

Select the primary role family using `ROLE_FAMILIES.md`, `PROFILE_SELECTOR.md`, and `ROLE_ADAPTATION_STANDARD.md` when present. Record secondary families only when they materially improve evidence selection.

Evaluate:

- verified direct matches
- transferable strengths
- genuine gaps
- mandatory versus preferred qualifications
- ATS terminology
- likely recruiter screens
- hiring-manager concerns
- travel and location fit
- compensation fit
- realistic competitiveness
- recommended application priority

Use a defensible fit score. Do not inflate the score to justify applying.

### Phase 4: Evidence Retrieval

Pull facts only from verified sources in GitHub, Google Drive, SharePoint/OneDrive when available, and Notion.

Evidence priority:

1. Primary records and official documents
2. Current GitHub constants and approved career facts
3. Notion evidence records linked to primary sources
4. Google Drive or SharePoint source documents
5. User statements requiring confirmation

Use only the minimum evidence necessary for the role. Protect private, sensitive, sealed, or trauma-heavy material.


### Praise-to-Experience Crosswalk

When a job requirement could be strengthened by an award, commendation, stakeholder comment,
or annual-review excerpt:

1. Open `awards_comm_perf_reviews.md`.
2. Select the verified experience first.
3. Search the crosswalk for praise tied to that experience or competency.
4. Rank the eligible item for direct relevance, proof strength, specificity, distinctiveness,
   recency, duplication, and privacy risk.
5. Use direct quotation marks only when the entry is `verified_verbatim` or
   `verified_excerpt`.
6. Suppress reviewer names and protected identifiers. Attribute by role or source type only.
7. Use no direct praise quotes in resumes or CVs. A cover letter normally uses zero or one;
   never exceed the quote limits in the credentials library.
8. If a public citation materially improves credibility, link only to a sanitized
   TroyHokanson.com evidence card that has passed the publication gate in the praise file.
   Never link application materials to private source records.

Praise corroborates the experience; it does not replace the experience or prove a claim that
the underlying evidence does not support.

### Phase 5: Drafting

Draft an ATS-readable targeted resume and role-specific cover letter using verified facts only.

Resume requirements:

- match the selected role lane
- use job-relevant vocabulary naturally
- lead with the strongest transferable evidence
- preserve truthful titles and dates
- avoid keyword stuffing
- avoid unsupported metrics
- include TroyHokanson.com and the current approved contact information
- exclude prohibited identifiers and obsolete branding

Cover-letter requirements:

- explain why this role and company make sense
- connect two or three strongest evidence themes to the employer's needs
- acknowledge a material transition gap when doing so improves credibility
- use Troy's natural professional voice
- avoid generic praise, fake enthusiasm, and canned AI phrasing
- use typed-name-only signature unless the current repository standard says otherwise

Never invent:

- titles
- direct reports
- certifications
- software proficiency
- enterprise SaaS experience
- customer outcomes
- statistics
- budget ownership
- platform Trust & Safety experience
- responsibilities
- security clearances beyond verified history

### Phase 6: Document Production

Generate final DOCX and PDF files using the current repository design and typography standards.

Required deliverables unless the role explicitly does not call for one:

- targeted resume DOCX
- targeted resume PDF
- targeted cover letter DOCX
- targeted cover letter PDF
- resume Markdown
- cover-letter Markdown
- job description archive
- validation report
- application metadata

Use the repository naming convention and preserve ATS-readable document structure.

For candidate profiles, expert-network profiles, contractor profiles, and other one-pagers, use `profile_one_pager.py`. It delegates the locked header to `docx_header.py` and reads spacing minimums from `workflow_contract.json`. Center the document title and focus line below the header; edit content before compressing the minimum spacing.

### Phase 7: Validation

Run all applicable checks:

- anti-AI scan
- privacy scan
- prohibited-content scan
- factual consistency check
- contact-information check
- education and credential constants check
- ATS keyword and readability review
- filename and package completeness check
- paired delivery gate when available
- `validate_application_packet.py`

Failures must be fixed or recorded as exceptions. Do not waive a failed gate silently.

### Phase 8: Visual QA

Render and inspect every PDF page.

Check:

- no clipping, overflow, or blank pages
- correct headers and page-two continuation header
- consistent Garamond typography where required
- proper spacing and hierarchy
- readable line lengths
- balanced page density
- correct links and contact row
- no hidden case identifiers or private information
- no conversion artifacts

A script reporting success is not a substitute for visual inspection.

### Phase 9: Cross-System Publication

After validation and visual QA, and only for systems the user authorized:

- save final DOCX and PDF files to the dated Drive folder
- save the job description and validation report to Drive
- update the GitHub application package with sanitized Markdown, metadata, and validation status
- create or update the matching Notion Applications record
- link Drive and GitHub in Notion
- record status, fit score, priority, role lane, document completion, recruiter/contact, next action, and follow-up date when known

Never claim a write succeeded unless the connector confirms it and a read-back verifies the intended destination and content.

### Phase 10: Completion Gate

An application may be labeled `Ready to Submit` only when all applicable items are confirmed:

- exact job identified
- official job description archived
- current GitHub standards reviewed
- role lane selected
- verified evidence reviewed
- resume complete
- cover letter complete
- validation passed
- every PDF page visually inspected
- Drive folder confirmed or not authorized
- final files saved to Drive or not authorized
- Notion record confirmed or not authorized
- GitHub package confirmed or not authorized
- remaining user action is only review and submission

If any item fails, status remains `Researching`, `Drafting`, or `Exception`.

Never mark `Submitted` until Troy confirms submission or a submission confirmation is received.

## Rejection Cleanup Rule

When Troy confirms a rejection or no-thank-you decision:

- set the matching application record to `Rejected`;
- remove any pending next-action date that exists only for application-status follow-up;
- automatically delete related application-status follow-up reminders from Outlook Calendar; and
- preserve interviews, legal or benefits deadlines, and unrelated appointments unless Troy explicitly directs otherwise.

Record the rejection source and date when available. If the source message cannot be retrieved, state that the status is based on Troy's confirmation. Verify both the application record and calendar cleanup before reporting completion.

## Exception Handling

Routine, reversible work should continue without asking for separate approval. Pause only for:

- uncertainty about the exact candidate or job
- unresolved conflict between strong sources
- material privacy risk
- destructive action
- public publication
- actual application submission
- a choice that depends on Troy's personal preference
- connector or validation failure that could leave systems inconsistent

For each exception, record:

- blocked item
- reason
- sources checked
- safest provisional status
- next evidence target
- exact user action required

Continue independent work when possible.

## Privacy and Safety Rules

Never include Troy's POST number, badge number, personnel identifiers, Social Security number, protected case numbers, victim information, private addresses, or restricted investigative details.

Apply all current GitHub privacy and prohibited-content rules. Uploaded raw records may contain protected information and must be sanitized before any GitHub or public-facing use.

Use trauma-heavy evidence only when essential to the role and allowed by the current evidence-selection rules. Prefer accurate capability language over unnecessary case detail.

Do not weaken Windows Security or Application Control to run a document tool. Use an allowed renderer or validator and report blocked coverage honestly.

## Application Metadata Contract

Every GitHub application package should track, when known:

```json
{
  "candidate": "Troy J. Hokanson",
  "employer": "",
  "role": "",
  "job_id": "",
  "job_url": "",
  "location": "",
  "work_mode": "",
  "salary": "",
  "posted_date": "",
  "primary_lane": "",
  "secondary_lanes": [],
  "fit_score": 0,
  "priority": "",
  "status": "researching",
  "google_drive_folder": "",
  "notion_record": "",
  "documents": {},
  "qa": {},
  "exceptions": []
}
```

Use `workflow_contract.json` in this skill directory as the machine-readable checklist.

## Required Completion Report

After each build, report:

- candidate
- exact employer, role, and job ID
- selected role lane
- fit score and priority
- resume status
- cover-letter status
- validation status
- PDF visual-inspection status
- job-description archive status
- Drive folder status
- Notion record status
- GitHub package status
- application status
- remaining user action

State exactly what failed. Never imply a connector, validation, upload, or database update occurred without confirmation.

## Compatibility Rule

`career-application-builder` is an alias for this skill. It must delegate here and may not maintain a competing workflow. Supporting skills may add evidence, drafting, formatting, or validation capability, but this skill owns sequencing and the final completion state.

## Update This Skill When

- a repository standard changes
- a new required validation or delivery gate is added
- Drive or Notion schemas change
- a new evidence source becomes authoritative
- application naming or folder conventions change
- repeated failures reveal a missing control
- Troy approves a durable workflow improvement

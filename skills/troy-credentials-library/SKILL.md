---
name: troy-credentials-library
description: Structured catalog of Troy Hokanson's certifications, training hours, and commendation quotes used to populate every resume, cover letter, CV, recruiter packet, professional bio, one-pager, capabilities sheet, or any DOCX/PDF that bears his name. Triggers on cert lookup, certification picker, training hours, commendation quote, supervisor quote, citizen quote, attach my certificates, pull a quote, populate the cert section, build the credentials block, and any phrase asking which credentials or quotes to use for a specific role. Loads alongside linkedin-profile-optimizer, github-application-document-standard, and resume-file-router. PTSD-safe filter is enforced at lookup time, never at edit time.
---

# Troy Credentials Library

> **Public Version Notice.** This is the sanitized, cross-platform-portable copy of `troy-credentials-library` published to GitHub for use across ChatGPT, Claude, Cursor, and other AI tools that read skills from a repo. Third-party civilian names and one neighboring-agency case file number have been redacted. The `suppressed_email_quotes` block has been removed entirely. The unsanitized master copy lives in Troy's private Perplexity user skill library and is the authoritative source.

## Purpose

This skill is the single source of truth for which certifications and which commendation quotes are eligible for any given Troy Hokanson document. It exists so cover letters, resumes, and recruiter packets stop overclaiming, stop undershipping, and stop accidentally surfacing PTSD-flagged content.

The skill consumes one structured data file:

```
/home/user/workspace/skills/troy-credentials-library/credentials_catalog.json
```

Five top-level keys live in that file:

1. `certifications` — split into `digital_forensics`, `investigations`, `supervisory_management`. Every entry has a tier (`headline` / `supporting` / `suppressed`), a `ptsd_safe` boolean, and a `profiles` list naming which target archetypes the entry is appropriate for.
2. `commendation_quotes` — every formal written-commendation Troy can cite. Each has a `ptsd_safe` flag, a `themes` list, a `profiles` list, a one-paragraph `verbatim_short` direct quote, an `verbatim_attribution_notes` paragraph that captures the case context Troy can paraphrase, and a `nominator_role` (supervisor / citizen).
3. `email_quotes` — supervisor and citizen email atta-cops and thank-you notes (less formal than written commendations, but still citable). Same shape as `commendation_quotes`: `id` (prefix `EMAIL-YYYYMMDD-SHORTNAME`), `ptsd_safe`, `tier`, `profiles`, `themes`, `verbatim_short`, `verbatim_attribution_notes`, `nominator_role`. Selectors treat `email_quotes` as an EXTENSION of `commendation_quotes` — both pools are eligible, both honor the supervisor + citizen cap and the voice/PTSD rules.
4. `suppressed_email_quotes` — email entries excluded from selector output because they fail the PTSD-safe filter. Kept for personnel-file completeness only. NEVER pulled by any selector.
5. `training_hours_total` — the documented hours figure used in summaries and cover letters.

## Hard Rules

These are non-negotiable and apply to every consumer of this skill.

1. **PTSD-safe filter is mandatory.** Anything with `ptsd_safe: false` or `tier: "suppressed"` MUST NOT appear in any auto-built document. The catalog records them so Troy has a complete personnel-file snapshot, but the selector logic skips them.
2. **Profile match is mandatory.** Every selection passes a profile filter (`vendor-solutions`, `siu-fraud`, or `analyst-intelligence`). An entry without that profile in its `profiles` list is not eligible for that document.
3. **Quote cap.** Cover letters get up to two `commendation_quotes`: at most one supervisor and at most one citizen. Resumes and CVs get zero direct quotes (commendations are summarized as a count and theme, never quoted verbatim in resume bullets).
4. **Verbatim quote integrity.** The `verbatim_short` field is the only string that may be presented as a direct quotation. Anything from `verbatim_attribution_notes` must be paraphrased, never quoted.
5. **Tier ordering.** When listing certifications in a document, headline-tier entries appear first and are never demoted; supporting-tier entries fill out the section as space allows; suppressed-tier entries are excluded entirely.

## Selection Workflow

When another skill (linkedin-profile-optimizer, github-application-document-standard, resume-file-router, or a build script) needs credentials or a quote, it must follow this order:

1. **Decide the profile.** Default is `vendor-solutions`. Override only when the cover letter or resume is targeted at a fraud SIU role (`siu-fraud`) or a pure analyst / intelligence role (`analyst-intelligence`).
2. **Decide the document type.** `resume` / `cv` / `cover` / `bio` / `recruiter-packet`.
3. **Pull eligible certifications.** Filter by `ptsd_safe == true`, `tier in ("headline", "supporting")`, and the chosen profile in `profiles`. Sort by tier then by date descending. Respect document space:
   - Resume credentials block: 8 to 12 entries, headline-tier weighted toward the top.
   - Cover letter inline reference: never list certifications. Reference one or two by name in prose if directly relevant (for example, "Cellebrite CCPA" for a vendor with mobile-forensics adjacency).
   - CV: every eligible entry, grouped by domain.
   - One-pager / capabilities sheet: 6 to 8 headline-tier entries only.
4. **Pull eligible quotes.** Filter `commendation_quotes` AND `email_quotes` together the same way (union the two pools, apply identical filters). For a cover letter, attempt to select one entry with `nominator_role == "supervisor"` and one with `nominator_role == "citizen"`. If only one role is available for that profile, use one quote. Never use two from the same role. Headline-tier entries are preferred over supporting-tier. `suppressed_email_quotes` is NEVER read by the selector.
5. **Pull the training hours figure.** Always cite `training_hours_total.documented_hours` rather than rounding or inventing.

## Quote Insertion Standard

When a quote is inserted into a cover letter, follow this pattern (adjust voice to match VOICE_STANDARD):

> One supervisor put it this way: "[verbatim_short text]" — [paraphrase from verbatim_attribution_notes for context].

Do NOT use em-dashes per VOICE_STANDARD. Use a period and a new sentence:

> One supervisor described that work this way. "[verbatim_short text]." [Paraphrase the context from verbatim_attribution_notes in plain Gen-X cadence.]

Citizen quotes follow the same shape with attribution adjusted ("A business owner whose case I closed put it this way." or similar). Never identify a citizen by name in any external document.

## Anti-AI Scan Compatibility

Every quote in the catalog has been reviewed for anti-AI scan compliance under `anti_ai_scan.py`. The quote selector still re-runs the scan on the final document. If a quote insertion causes the document to fail the scan, the build fails per the resume-file-router and github-application-document-standard delivery gate.

## Adding New Items

When Troy provides new certificates or commendations:

1. OCR the PDF (use the `read` tool on PDFs in `/home/user/workspace/uploaded_attachments/...`).
2. Append a new object to the appropriate section of `credentials_catalog.json`. Use the next available `id` in that section's prefix series (`DF-###`, `INV-###`, `SUP-###`, `COM-YYYY-SHORTNAME`).
3. Set `ptsd_safe` honestly. If the case involves homicide, lethal force, sexual assault, criminal sexual conduct, human trafficking, child abuse, child exploitation, suicide / self-harm, or violent assault, mark `ptsd_safe: false` and add a `ptsd_reason` string. Set `tier: "suppressed"`.
4. Set the `profiles` list. Default is `["vendor-solutions"]` for supervisory and digital forensics items, `["siu-fraud", "analyst-intelligence"]` for fraud and intelligence items. Add `vendor-solutions` whenever the entry has clear teaching, demo, or customer-success adjacency (Cellebrite, Magnet, X-Ways, BCA Police Management, Public Safety Manager).
5. For commendations, fill `verbatim_short` with the exact quote text from the certificate. Fill `verbatim_attribution_notes` with the context paragraph (case file number, agencies, outcomes). Set `nominator_role` to `supervisor` or `citizen`.

## Files Currently Cataloged

Source PDFs OCR'd into the catalog:

- Digital-Forensic-Certificates.pdf (16 pages)
- Investigations-Certificates.pdf (22 pages)
- Supervisory-Certificates.pdf (8 pages)
- WRITTEN-COMMENDATION-02.pdf (4 pages)
- Written-Commendations-01.pdf (24 pages)
- 30 atta-cop email files (2002–2016) supplied 2026-05-29. 20 entries are in `email_quotes` (SAFE / citable). In the private master copy an additional 10 entries live under `suppressed_email_quotes` for personnel-file completeness only; that block is omitted from this public copy. Headline entries include the Chief Long thank-you on the joint US Postal Inspection Service federal mail-fraud case (Troy received a formal US Postal Inspection Service award on this case), the Sgt Polinski note on Troy's leadership of the probation liaison program, the Sgt Castonguay fraud follow-through note (prime SIU material), the Chief Martens 2002 performance-evaluation praise ("go-gettum attitude"), Troy's nomination of an off-duty civilian nurse for the Chief's Award of Merit (civilian-recognition leadership work), the 2009 Hvinden military send-off escort (multi-agency military-LE bridge), and a strong Lakeville-resident citizen letter (stolen-property recovery).

## Cross-References

- VOICE_STANDARD.md (in tjh-resume-cover-cv repo) — voice and anti-AI rules every consumer of this skill must respect.
- linkedin-profile-optimizer — primary consumer for cover letters, resumes, and bios.
- github-application-document-standard — preflight gate; verifies this skill is loaded before any Troy-bearing document is built.
- resume-file-router — post-build gate; verifies anti-AI scan passed before routing to OneDrive.

## Update This Skill When

- Troy adds a new certification PDF or commendation document.
- Troy provides the NotebookLM email PDFs.
- A new target archetype is introduced and a fourth profile is added.
- An existing entry changes status (a sealed case becomes citable, or a previously safe entry is reclassified).

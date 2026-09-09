# Career Evidence Archives

Reusable, source-backed evidence system for Troy Hokanson's resumes, cover letters, interviews, portfolios, and application tracking.

## Archive categories

| Archive | Primary scope |
|---|---|
| `scsu_public_safety` | Campus public-safety training, investigations, supervision, and commendations |
| `military_service` | Army components, MOS history, awards, and Honor Guard service |
| `lakeville_programs` | FTO, reserve liaison, park-ranger training, community engagement, crime-scene, and tactical assignments |
| `electronic_crimes` | ECU, DCECTF, digital forensics, legal process, tools, volume, and investigator enablement |
| `technology_implementation` | ALPR, technical acquisition, integration, adoption, and workflow implementation |
| `public_safety_vendors` | Vendor/product crosswalk linked to evidence in other archives |
| `university_of_phoenix` | Remote adjunct teaching, faculty credentials, awards, and customer-education evidence |
| `real_estate` | Residential sales, client outcomes, credentials, CRM use, and transition framing |
| `training_certifications` | Canonical training and certification records with profile routing |
| `investigations_casework` | Privacy-safe case outcomes and investigative methods linked to `CASE_BANK.md` |

## Standard files

Each category contains:

- `README.md` for human review, safe claims, and usage boundaries.
- `evidence_catalog.json` for automated filtering by profile, competency, source, and verification status.
- Source artifacts when the file is appropriate for a public repository.

## Source hierarchy

1. Original source artifact or connected Drive record.
2. `CAREER_CONSTANTS.md`, `TRAINING_CONSTANTS.md`, `CASE_BANK.md`, and the credentials library.
3. User-confirmed corrections recorded with confirmation date.
4. Derived application language, which must never override a higher-level source.

## Global rules

- Do not invent dates, titles, metrics, outcomes, tools, or authority.
- Preserve discrepancies and cautions in the catalog.
- Do not duplicate a source artifact across archives; use `related_archives` references.
- Separate tool operation from training-only exposure.
- Keep ECU and DCECTF as separate assignments.
- Keep sensitive case facts privacy-safe and follow `PRIVACY_STANDARD.md`.
- Treat scans as verification artifacts, not routine application attachments.

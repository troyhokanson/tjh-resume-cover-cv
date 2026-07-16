# Career System Architecture

## Operating model

- **Notion is the command center.** It is the authoritative database for opportunity status, fit, priority, next action, follow-up dates, contacts, and links.
- **Google Drive is the document vault.** It stores job descriptions, editable DOCX files, final PDFs, QA reports, correspondence, and interview preparation.
- **GitHub is the standards and automation engine.** It stores machine-readable JSON standards, reusable Markdown content, application metadata, builders, tests, and workflow logic.
- **Telegram is the alert channel.** It provides time-sensitive job, failure, and health notifications but is never the authoritative record.

## Required application lifecycle

1. A bot discovers a job and applies candidate-specific quality rules.
2. A qualifying opportunity is deduplicated and written to Notion.
3. Telegram receives an alert only when the configured threshold is met.
4. A human decides whether to pursue the role.
5. The application package is generated from verified facts and locked design standards.
6. DOCX and PDF files are saved under `01_Investigator Command Center/09_Applications/YYYY-MM-DD_Company_Role` in Google Drive.
7. The substantive resume and cover letter are archived as Markdown in GitHub.
8. Application metadata is validated against `standards/application_package.schema.json`.
9. Google Drive and GitHub links are written back to the Notion application record.
10. Package QA is completed before submission.
11. Submission date, follow-up date, recruiter, and next action are tracked in Notion.

## Required generated artifacts

- Job description archive
- Resume DOCX
- Resume PDF
- Cover letter DOCX
- Cover letter PDF
- Resume Markdown
- Cover letter Markdown
- Application metadata JSON
- QA report

## Automation boundary

Automation may create folders, records, files, links, reminders, validation reports, and alerts. Human approval remains required for submission, outbound communication, visible signature use, new factual claims, deletion, withdrawal, and publication of sensitive material.

## Privacy rule

Sensitive personal records, private health information, unsanitized case records, and signature image files must never be committed to a public repository. Only sanitized, role-relevant, verified career evidence may be archived in GitHub.

## Health standard

The system is healthy only when:

- scheduled workflows completed successfully within their expected window;
- Telegram failures are surfaced;
- Notion records contain required links and next actions;
- generated Drive packages contain the expected files;
- GitHub contains the matching Markdown and JSON records;
- no stale repository names, hardcoded owner paths, or expired integration assumptions remain.

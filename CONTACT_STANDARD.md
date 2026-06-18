# Troy Hokanson Contact Standard

**Permanent. Applies to every resume, cover letter, CV, recruiter packet, professional bio, one-pager, PDF, DOCX, and application document bearing Troy Hokanson's name.**

## Canonical Email Rule

Use this email address for every document header and every application document:

`TroyHokanson@iCloud.com`

Do not use `Troy.Hokanson@pm.me` for resumes, cover letters, CVs, application packets, or document headers.

## Build Rule

The document templates must continue loading contact fields from environment variables. Do not hardcode personal contact details in template code.

For local builds, set the local `.env` file:

```bash
TROY_EMAIL=TroyHokanson@iCloud.com
```

For GitHub Actions builds, set the repository secret:

```bash
TROY_EMAIL=TroyHokanson@iCloud.com
```

## AI Build Rule

Any AI-assisted build session must confirm the contact email before exporting documents. If there is a conflict between memory, a previous resume, or a generated draft, this file controls.

## Reason

Past builds used the wrong email address in the header. This file prevents that from happening again.
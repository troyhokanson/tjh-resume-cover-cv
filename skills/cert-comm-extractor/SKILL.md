---
name: cert-comm-extractor
description: Extract, reconcile, and structure Troy Hokanson certification, training, award, and written-commendation records from PDFs, images, spreadsheets, or document collections. Use when new certificates or commendations must be OCRed, source-linked, privacy-reviewed, added to the credential tracker, or prepared for evidence-safe use in resumes, cover letters, CVs, LinkedIn, or the public portfolio.
---

# Certification and Commendation Extractor

Create source-traceable credential records without turning OCR guesses into career claims.

## Workflow

1. Inventory every source file and retain its original filename, page number, and Drive or private-source link when available.
2. Use the PDF, image, or spreadsheet skill appropriate to the source format.
3. Extract exact visible fields: document title, course or award name, course/certificate number, date, hours or credits, issuing organization, sponsor, instructors or signatories, and the name on the document.
4. Record illegible or uncertain fields as `Needs Evidence`; do not infer them from nearby documents.
5. Classify relevance across the canonical role families in `ROLE_FAMILIES.md`, not only investigator roles.
6. Apply `PRIVACY_STANDARD.md`. Suppress personnel identifiers, badge/POST numbers, protected case numbers, victim information, private addresses, signatures, barcodes, and other unnecessary identifiers from public copies.
7. Reconcile against `skills/troy-credentials-library/credentials_catalog.json` and the current tracker before adding a new item. Preserve the verified source link.
8. Keep original evidence in Drive or another approved private store. Commit only sanitized structured facts and approved public-safe files to GitHub.
9. Read back every Drive, Notion, spreadsheet, or repository write. Report missing, unreadable, duplicate, or conflicting records explicitly.

## Record fields

Capture when present:

- source document and page;
- record type;
- exact document or course title;
- course, certificate, or credential number;
- completion or issue date;
- documented hours, credits, or CEUs;
- issuing and sponsoring organizations;
- instructor and signatory names;
- evidence-safe one-sentence summary;
- relevant role families;
- confidence and extraction notes;
- private source link and approved public link, when one exists;
- privacy status and redaction requirements.

## Output rules

- Use structured JSON or the repository's credential tracker as the machine-readable source.
- Preserve exact quotations only when the source is legible and the quotation is necessary.
- Never publish a raw commendation or certificate merely because it was extracted successfully.
- Do not claim a public link until it returns the intended sanitized document.
- Delegate document selection and application wording to `build-troy-application` and `troy-credentials-library`.

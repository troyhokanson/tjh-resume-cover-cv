# Body Typography and Pagination Standard

**Effective date:** July 24, 2026  
**Applies to:** resumes, cover letters, CVs, recruiter packets, professional bios, candidate profiles, and one-pagers.

This standard closes two failure modes from the Sibylline Intelligence Analyst packet build:

1. Garamond styling was not consistently enforced across headings, subheadings, and job blocks.
2. A job block heading, specifically Adjunct Faculty, appeared at the bottom of page 1 without related content following it.

## Governing rule

The branded navy/gold header is not enough. The body must also follow Troy Hokanson's visual standard.

Every serious application packet must pass both gates:

1. **Header gate:** zero-bleed navy header with the locked gold rule and contact row.
2. **Body gate:** Garamond-family headings, subheadings, job blocks, body text, balanced spacing, and no orphaned headings.

## Required body typography

| Element | Required styling |
|---|---|
| Body text | Garamond-family, 10.25 pt resume / 10.5 pt cover letter, body text color |
| Section heading | Garamond bold, 11 pt, steel blue `#2D6A9F`, restrained gold underline |
| Subsection heading | Garamond bold, 10.5 pt, body text color |
| Job heading | Garamond bold, 10.5 pt, body text color |
| Employer/date line | Garamond-family, 9.75-10 pt, secondary text color where appropriate |
| Bullets | Garamond-family, 10.25 pt, consistent spacing |
| Header name | Garamond-family bold, 26 pt, white |
| Header contact row | Garamond-family, 9.5 pt, gold |

A build fails if visible document text falls back to Calibri, Aptos, Arial, or another default Word font when Garamond-family styling was intended.

## Heading and subheading rules

1. Section headings must use Garamond bold with the approved steel-blue text and restrained gold underline.
2. Subheadings must use Garamond-family bold, not Word default heading styles.
3. Job titles must use Garamond-family bold and must be kept with the employer/date line and the first bullet or first descriptive line.
4. Section headings, subheadings, and job headings must use `keep_with_next` behavior.
5. No section heading, subheading, job title, or employer line may appear alone at the bottom of a page.

## Pagination and spacing rules

A build fails if any of the following appears in the rendered PDF or page images:

- A section heading is the last visible paragraph on a page.
- A subsection heading is the last visible paragraph on a page.
- A job heading is stranded at the bottom of a page.
- A job title appears on one page and its bullets start on the next page.
- The Adjunct Faculty block, or any other job block, starts at the end of a page without at least two lines of related content after it.

## Required remediation order

When a block is orphaned, fix it in this order:

1. Move the entire job block to the next page.
2. Reduce safe intra-section spacing by no more than 0.5 points at a time.
3. Condense bullets only if the factual meaning remains unchanged and the anti-AI scan still passes.
4. Do not solve the problem by changing body font away from Garamond.
5. Do not hide content, shrink below the minimum font size, or remove important context without a content decision.

## Validation requirements

Every generated resume, cover letter, and CV must be rendered before approval.

Required checks:

- Render DOCX to PDF.
- Render every PDF page to PNG.
- Inspect every page, not just page 1.
- Confirm headings and subheadings use Garamond-family styling.
- Confirm section headings use the approved steel-blue plus gold underline treatment.
- Confirm no job heading or section heading is isolated at the page bottom.
- Confirm the final page has balanced spacing and no unexpected blank page.

## Automation note

This Markdown standard is the human-readable companion to `standards/document_design_standard.json`. The JSON file remains the machine-readable source for build scripts and validators.

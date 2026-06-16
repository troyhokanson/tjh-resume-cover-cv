# Skills Constants — Locked Table Format

This file defines the canonical skills section for Troy Hokanson's resumes and CVs.
Skills are organized into six domains and rendered as a two-column table in all documents.
**Never free-list skills. Always render from this table.** Never add skill categories not listed here
without updating this file first.

---

## Canonical Skills Table (verbatim for resume/CV)

Render as a bordered two-column table with a navy header row matching the document header standard.
Left column: domain label (bold). Right column: comma-separated skills string.

| Domain | Skills |
|---|---|
| **Fraud Investigation** | Insurance fraud detection, SIU case management, financial crime analysis, workers compensation fraud, healthcare fraud, identity theft investigation, asset tracing |
| **Digital Forensics** | Cellebrite UFED (CCLO/CCPA), mobile device extraction, cell-site analysis, location data interpretation, social media OSINT, dark web investigation, NW3C cybercrime |
| **Interviewing and Interrogation** | Reid Technique, cognitive interviewing, recorded statement management, witness coordination, victim-sensitive interviewing |
| **Intelligence and Analysis** | Criminal intelligence analysis, link analysis, pattern recognition, threat assessment, i2 Analyst Notebook, geospatial mapping, OSINT tools |
| **Legal and Compliance** | Search warrant preparation, criminal case referral, subpoena management, chain of custody, court testimony, expert witness, Minnesota Rules of Criminal Procedure |
| **Technology and Platforms** | Axon Evidence, Microsoft 365, SharePoint, case management systems, SQL basics, Python basics, AI-assisted research tools |

---

## Document Rendering Rules

- The table header row must use navy fill (#1F3864) with white bold text, matching `HEADER_STANDARD.md`.
- Domain column width: fixed at 28% of text area width.
- Skills column width: 72%.
- Font: Calibri 10pt in the table body. Domain labels are bold. Skills text is regular weight.
- Do NOT reorder domains. Fraud Investigation is always first; Technology and Platforms is always last.
- If a specific role does not require a domain (e.g., a pure analyst role with no court testimony),
  that row may be omitted for that document only. The source table here remains unchanged.
- Do NOT add a "Core Competencies" prose block above the table. The table is the section.

---

## ATS Plain-Text Fallback

When generating a plain-text ATS version, render skills as a flat pipe-delimited list:

```
Insurance Fraud Detection | SIU Case Management | Financial Crime Analysis | Workers Compensation Fraud | Healthcare Fraud | Identity Theft Investigation | Asset Tracing | Cellebrite UFED (CCLO/CCPA) | Mobile Device Extraction | Cell-Site Analysis | Location Data Interpretation | Social Media OSINT | Dark Web Investigation | Reid Technique | Cognitive Interviewing | Recorded Statement Management | Criminal Intelligence Analysis | Link Analysis | i2 Analyst Notebook | Geospatial Mapping | Search Warrant Preparation | Criminal Case Referral | Court Testimony | Expert Witness | Axon Evidence | Microsoft 365 | SharePoint | AI-Assisted Research Tools
```

---

## Change Log

- 2026-06-15: Created. Six-domain table established. ATS plain-text fallback added.
  CCCI and Cellebrite CCLO/CCPA reflected under Digital Forensics domain.

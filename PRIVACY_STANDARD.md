# PRIVACY_STANDARD.md
## Troy J. Hokanson — Application Document Privacy Standard

This file governs the suppression of personally identifiable information (PII),
case-identifying data, and law enforcement record details in all application
documents bearing Troy Hokanson's name: resumes, cover letters, CVs, bios,
one-pagers, recruiter packets, and any derivative document.

This standard exists for two compounding reasons:

1. **Professional signal.** SIU investigators, fraud examiners, intelligence analysts,
   and ACA program integrity investigators are expected to demonstrate information
   handling discipline as a baseline competency. Appearing in application materials
   with suspect full names, case control numbers, and court case numbers signals the
   opposite of what these roles require.

2. **Legal and ethical obligation.** Even when case information is technically public
   record, selectively publishing it in employment documents without a law enforcement
   or judicial purpose creates unnecessary exposure for subjects who have served their
   sentences, for victims whose information may be embedded in the record, and for the
   agencies that generated the original case file.

This standard does not suppress the investigative outcomes. It suppresses the
identifiers. The value of the case to an employer is the investigative method,
the legal instrument used, the outcome, and the quantified impact — not the
subject's name or the court file number.

---

## Section 1 — Suppressed Elements (Hard Block)

The following elements must NEVER appear in any application document.
This is a hard block enforced by `anti_ai_scan.py`. No exceptions.

### 1A — Suspect / Subject Names
- Full names of any suspect, subject, defendant, or person of interest
- Partial names that are uniquely identifying (e.g., "Condello Wall," "Matt Garwood")
- Aliases used in the case record

**Permitted replacement:** Describe role only.
- BLOCKED: "Condello Wall, office manager at MCI Paint and Drywall"
- PERMITTED: "an office manager at a local construction company"
- BLOCKED: "Matthew Scott Garwood"
- PERMITTED: "the subject" or "the suspect"

### 1B — Case Control Numbers
- Internal department control numbers (e.g., "Control #10001056", "Control #16004659")
- Court case numbers (e.g., "19HA-CR-11-907", "19HA-CR-18-2512")
- Any alphanumeric string that functions as a unique case file identifier

**Permitted replacement:** Omit entirely. The year, case type, and outcome are sufficient.

### 1C — Subject Date of Birth
- Any DOB in the format MM/DD/YYYY, YYYY-MM-DD, or any derivative
- Age-as-identifier language tied to a named subject

**Permitted replacement:** Omit entirely.

### 1D — Subject Address or Residence Jurisdiction Used as Identifier
- Street address of a subject's residence used as part of identification
- City/neighborhood used in combination with name or DOB

**Permitted replacement:** Jurisdiction reference without address is acceptable when
it describes the investigative action (e.g., "coordinated with another city's SWAT
team to serve a search warrant").

### 1E — Victim Names
- Full or partial names of any victim, complainant, or reporting party
- Any descriptor that would identify a specific victim in combination with case details

**Permitted replacement:** "the victim," "the complainant," "the employer," as appropriate.

### 1F — Judge Names in Case Outcomes
- Names of presiding judges cited in application documents
- Judicial identifiers used to validate case outcomes

**Permitted replacement:** "the court," "a Dakota County District Court judge," or omit.

### 1G — Probation Officer Names
- Names of probation officers cited in commendation context

**Permitted replacement:** "a Dakota County probation officer," "department supervision staff."

---

## Section 2 — Permitted Elements (What Stays)

These elements are explicitly permitted and should be retained because they represent
the professional value of the case without creating identifiability risk.

| Permitted Element | Example |
|---|---|
| Case type / fraud category | Business Email Compromise, occupational fraud, burglary |
| Verified dollar loss or restitution amount | $360,000+ in verified victim losses |
| Conviction type and statute class | Felony conviction under Minnesota law |
| Sentence outcome | 30-month commitment stayed 10 years, 10-year supervised probation |
| Investigative methods | Search warrant, Google account preservation, APS query, Excel financial summary |
| Agency name (your own) | Lakeville Police Department, Dakota County Electronic Crimes Task Force |
| Commendation source by role title | An Assistant Dakota County Attorney, a supervising sergeant |
| Geographic reference for investigative action | Coordinated with casino security staff; served warrant in a neighboring city |
| Year or approximate year | Approximately 2019 to 2021, offense date 2016 |
| Criminal history reference (non-identifying) | A subject with a documented 36-year criminal history |
| Charge citation by statute | MN Statute 609.52.2(4), Theft by Swindle, Felony |
| Court-ordered conditions | Court-ordered gambling treatment, restitution, supervised probation |

---

## Section 3 — The Expungement Detail (Special Rule)

Case 2 (occupational fraud) contains an expungement denial that is highly valuable as a
proof point for documentation integrity and case package quality. It may be referenced,
but it must be framed in terms of what it demonstrates about the case record, not in
terms of identifying the subject.

**BLOCKED:** "Condello Wall's motion for expungement was denied by Judge Arlene Perkkio."
**PERMITTED:** "A subsequent motion for expungement filed by the subject was denied by the
court in February 2022, confirming the integrity and durability of the original case record."

The name of the judge is suppressed. The name of the subject is suppressed. The outcome
and its significance to documentation quality are fully retained.

---

## Section 4 — CASE_BANK.md Internal Records vs. Application Output

CASE_BANK.md is an **internal reference file only.** It intentionally contains full
names, case numbers, DOBs, and judicial identifiers because it is the source of truth
for interview preparation and legal accuracy. That level of detail is appropriate in
a private repository used to prepare for interviews where the record may be verified.

**The rule is:** CASE_BANK.md is the source. Application documents are the output.
The output must never reproduce the identifiers from the source.

When any AI agent or build script pulls content from CASE_BANK.md to generate a
resume bullet, cover letter paragraph, or any application-facing text, it must
run the output through the suppression rules in Section 1 before including it
in the final document. The resume bullet variants and cover letter paragraph
variants written directly in CASE_BANK.md are already written to this standard
and may be used as-is. Do not pull from the case header blocks (Case Reference,
Suspect Profile, etc.) and reproduce them verbatim in application documents.

---

## Section 5 — Interview Context Exception

Interview talking points in CASE_BANK.md are written for verbal preparation only.
They may include fuller operational detail because they are spoken, not distributed,
and they occur in a credentialed professional context where the record is being
verified by a prospective employer.

Even in interview settings, do not volunteer a subject's full name, DOB, or
current location. Reference the case by type and outcome. If the interviewer asks
for specifics to verify, those may be provided in that professional context.

---

## Section 6 — Enforcement in anti_ai_scan.py

The following patterns are added to the scanner's hard-block list and will
cause a `FailedScan` on any document that contains them:

```
CONTROL_NUMBER_PATTERN = r'Control\s*#\s*\d+'
COURT_CASE_PATTERN     = r'\d{2}[A-Z]{2}-[A-Z]{2}-\d{2}-\d{4}'
DOB_PATTERN            = r'DOB\s*[:\-]?\s*\d{2}/\d{2}/\d{4}'
```

Suspect name blocking is handled by maintaining a `SUPPRESSED_NAMES` list in
`anti_ai_scan.py`. When a new case is added to CASE_BANK.md, the subject's name
must also be added to `SUPPRESSED_NAMES` in the scanner.

Current suppressed names (maintained in scanner, not repeated here for privacy):
- Subject from Case 2 (occupational fraud)
- Subject from Case 4 (commercial burglary)
- Judicial names from Cases 2 and 4

---

## Section 7 — When to Update This File

Update this file when:
- A new case is added to CASE_BANK.md (add subject name to scanner's SUPPRESSED_NAMES)
- A new category of identifiable data is discovered in a document review
- A role-specific exception is needed (e.g., a role that requires case citation as a work sample)
- The legal or ethical landscape around case record publication changes

Update `anti_ai_scan.py` at the same time. The standard and the enforcement must stay synchronized.

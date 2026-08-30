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
- Partial names that are uniquely identifying
- Aliases used in the case record

**Permitted replacement:** Describe role only.
- BLOCKED: "[named subject], office manager at [named business]"
- PERMITTED: "an office manager at a local construction company"
- BLOCKED: "[full subject name]"
- PERMITTED: "the subject" or "the suspect"

### 1B — Case Control Numbers
- Internal department control numbers
- Court case numbers
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

### 1H — Law-Enforcement License and Internal Service Identifiers
- Minnesota POST or peace-officer license numbers
- Badge numbers and internal personnel or employee identifiers
- License effective dates, expiration dates, renewal details, or credential IDs
- A standalone POST or peace-officer licensing credential line, even without a number

Troy is not pursuing sworn law-enforcement positions. These identifiers provide no
material value for his current targets and create an unnecessary searchable link to
licensing records.

**Permitted replacement:** Omit the licensing credential entirely. Describe the
relevant experience as "25 years of sworn law-enforcement service" or "medically
retired Minnesota detective" when the target role benefits from that context.

**Private verification exception:** If an employer makes a legitimate, role-specific
written request for licensing verification, respond privately outside the resume,
cover letter, CV, portfolio, or public repository.

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

**BLOCKED:** "[named subject]'s motion for expungement was denied by [named judge]."
**PERMITTED:** "A subsequent motion for expungement filed by the subject was denied by the
court in February 2022, confirming the integrity and durability of the original case record."

The name of the judge is suppressed. The name of the subject is suppressed. The outcome
and its significance to documentation quality are fully retained.

---

## Section 4 — Public Case Patterns vs. Private Evidence

`CASE_BANK.md` is stored in this public repository and therefore contains sanitized
patterns only. Full names, case numbers, DOBs, judicial identifiers, provider account
data, exact crosswalks, and raw evidence belong in the approved private evidence system.

**The rule is:** private evidence supports the claim; `CASE_BANK.md` provides a sanitized
candidate pattern; the final document still must pass the current role, verification,
privacy, and PTSD-scope gates.

When any AI agent or build script pulls content from CASE_BANK.md to generate a
resume bullet, cover letter paragraph, or any application-facing text, it must recheck
the private evidence status and run the output through the suppression rules in Section 1.
No public case pattern is approved for automatic use merely because it exists in the file.

---

## Section 5 — Interview Context Exception

Interview talking points in `CASE_BANK.md` remain sanitized. Fuller operational detail
may be reviewed from private evidence during interview preparation, but it must not be
copied into this repository.

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

Known private names may be blocked at runtime through the local
`TROY_PRIVATE_CASE_DENYLIST` environment variable. Store the pipe-delimited values only
in the gitignored `.env` file or an approved secret store. Never place the values in
source code, tests, comments, logs, or public workflow output.

The scanner also blocks generic case-control, court-number, DOB, licensing-identifier,
and named-judge patterns without requiring a private denylist value.

---

## Section 7 — When to Update This File

Update this file when:
- A new private case is reviewed (update the local denylist only when needed)
- A new category of identifiable data is discovered in a document review
- A role-specific exception is needed (e.g., a role that requires case citation as a work sample)
- The legal or ethical landscape around case record publication changes

Update `anti_ai_scan.py` at the same time. The standard and the enforcement must stay synchronized.

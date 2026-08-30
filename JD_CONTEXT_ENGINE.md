# JD_CONTEXT_ENGINE.md
## Troy J. Hokanson — Job Description Context Engine

This file is the **content selection layer** that sits between the constants files and the final document.
It does not replace CAREER_CONSTANTS.md, CASE_BANK.md, PROFILES.md, or VOICE_STANDARD.md.
It tells any AI agent or build script **which** assets to surface, **which** stat to lead with, and
**which** summary sentence variant to use — based on the actual keywords and emphasis in the job description.

**Workflow:**
1. Read the full job description.
2. Run Signal Detection (Section 1) to identify active signals.
3. Use Stat Routing Rules (Section 2) to select the lead stat and suppressed stats.
4. Use Summary Sentence Variants (Section 3) to select the opening profile sentence.
5. Use the Case Selection Matrix (Section 4) to rank cases as LEAD, SUPPORT, or OMIT.
6. Use Bullet Emphasis Rules (Section 5) to order and trim bullets within each job block.
7. Assemble document from the resulting manifest. Do not deviate from VOICE_STANDARD.md.

---

## Section 1 — Signal Detection

Read the job description and mark each signal as PRESENT or ABSENT.
A signal is PRESENT if one or more of its trigger keywords appear in the JD.
Multiple signals can be active simultaneously; rank by frequency and prominence of keywords.

### Signal A — FWA / Insurance Fraud Investigation
**Trigger keywords:** fraud, waste, abuse, FWA, SIU, special investigations unit, insurance fraud,
claims investigation, fraudulent claims, workers compensation fraud, healthcare fraud, auto fraud,
property fraud, life insurance fraud, subrogation, ISO, NICB, fraud referral, civil referral,
IFPA, fraud examiner, CFE, fraud detection, claimant interview, recorded statement

### Signal B — ACA / Marketplace / Healthcare Program Integrity
**Trigger keywords:** ACA, Affordable Care Act, Marketplace, CMS, CPI, MPIC, FFM, program integrity,
enrollment data, agent/broker compliance, navigator, qualified health plan, Medicaid, Medicare,
FWA investigation, healthcare enrollment, health insurance exchange, consumer protection,
administrative action, PII, PHI, HIPAA, SOP compliance, case management system, IPOA

### Signal C — Intelligence Analysis / Data Analysis
**Trigger keywords:** intelligence analyst, crime analyst, crime intelligence, data analysis,
pattern analysis, trend analysis, link analysis, investigative analysis, OSINT, open source,
entity resolution, data visualization, reporting, structured analytic techniques, SAT,
i2, Palantir, Analyst's Notebook, Excel analysis, database query, enrollment data analysis,
lead development, analytical report, case summary, written findings

### Signal D — Digital Forensics / Electronic Evidence
**Trigger keywords:** digital forensics, computer forensics, mobile forensics, electronic evidence,
ESI, Cellebrite, AXIOM, FTK, EnCase, Magnet, UFED, image acquisition, hash value, chain of custody,
forensic analysis, forensic examination, forensic imaging, DCECTF, ICAC, cybercrime, dark web,
online exploitation, electronic device examination, digital evidence, search warrant for digital accounts

### Signal E — Corporate / Private Sector Investigation
**Trigger keywords:** corporate investigator, internal investigations, workplace investigation,
employee misconduct, HR investigation, loss prevention, asset protection, retail fraud,
organized retail crime, ORC, vendor fraud, background investigation, due diligence,
executive protection, corporate security, enterprise risk, third-party investigation,
civil investigation, EUO, examination under oath, SIU vendor, TPА, third party administrator

### Signal F — Law Enforcement / Government / Federal
**Trigger keywords:** law enforcement, LE, police, detective, criminal investigation, federal,
DOJ, FBI, HSI, USSS, IRS-CI, clearance, background check, government contract, contractor,
sworn, peace officer, POST, certification, public safety, task force, ICAC, HIDTA

---

## Section 2 — Stat Routing Rules

Each stat is tagged with the signals where it LEADS, SUPPORTS, or is SUPPRESSED.
**LEAD** = feature prominently in summary and first relevant bullet.
**SUPPORT** = available for use in bullets or interview prep, not the summary.
**SUPPRESSED** = do not use; it creates noise or implies misfit for this role.

### Stat: "$360,000+ BEC / verified victim losses / felony conviction / Dakota County Attorney commendation"
- Signal A (FWA/Insurance Fraud): **LEAD** — open the summary with this; use condensed bullet
- Signal B (ACA/Marketplace): **SUPPORT** — use in experience bullets, not the summary opener
- Signal C (Intelligence Analysis): **SUPPORT** — frame as complex financial case documentation and reporting
- Signal D (Digital Forensics): **SUPPORT** — frame in context of financial transaction tracing and subpoena work
- Signal E (Corporate Investigation): **LEAD** — use full bullet; this is the strongest private-sector credentialing stat
- Signal F (LE/Government): **LEAD** — use full bullet with federal coordination framing

### Stat: "~$80,000 occupational fraud / Theft by Swindle felony / expungement denied 2022"
- Signal A (FWA/Insurance Fraud): **SUPPORT** — good secondary case; use condensed bullet
- Signal B (ACA/Marketplace): **SUPPORT** — use to demonstrate documentation integrity and audit trail quality
- Signal C (Intelligence Analysis): **SUPPORT** — use the Excel financial summary and structured case package angle
- Signal D (Digital Forensics): **SUPPRESSED** — no digital component; does not add value for this signal
- Signal E (Corporate Investigation): **LEAD** — occupational fraud is the dominant case type for corporate investigators; use full bullet
- Signal F (LE/Government): **SUPPORT** — secondary case; use condensed

### Stat: "5,304 GB of digital evidence / DCECTF / Cellebrite / AXIOM / FTK / EnCase"
- Signal A (FWA/Insurance Fraud): **SUPPRESSED** — insurance SIU work is not digital forensics; this creates misfit signal
- Signal B (ACA/Marketplace): **SUPPRESSED** — no relevance to ACA enrollment or program integrity work
- Signal C (Intelligence Analysis): **SUPPORT** — mention as part of investigative breadth; do not lead with it
- Signal D (Digital Forensics): **LEAD** — this is the primary credential; open the summary with this
- Signal E (Corporate Investigation): **SUPPRESSED** — unless JD specifically mentions electronic evidence or BYOD investigations
- Signal F (LE/Government): **SUPPORT** — relevant as task force experience; use in career block, not summary

### Stat: "18 years adjunct instructor / crisis intervention training / 40+ sessions"
- Signal A (FWA/Insurance Fraud): **SUPPRESSED** — not relevant; creates noise
- Signal B (ACA/Marketplace): **SUPPRESSED** — not relevant to CMS/ACA context
- Signal C (Intelligence Analysis): **SUPPORT** — frame as analytical methodology instruction if the JD mentions training or knowledge transfer
- Signal D (Digital Forensics): **SUPPRESSED** — not relevant
- Signal E (Corporate Investigation): **SUPPRESSED** — unless the role is a training or supervisory role
- Signal F (LE/Government): **SUPPORT** — use in training block; demonstrates instructional credibility within LE context

### Stat: "25-year / medically retired / Minnesota detective / decorated"
**Routing notes:** This phrase leads only when seniority and credentialing are the primary differentiators.
For mid-level analyst and investigator roles at companies that typically hire from a 5-15 year experience pool,
leading with "25 years" can read as overqualified before fit is established. Route as follows:

- Signal A (FWA/Insurance Fraud, senior/lead level): **LEAD** — use "two decades of fraud investigation" framing
- Signal A (FWA/Insurance Fraud, individual contributor level): **SUPPORT** — let the BEC case lead; mention career length as context, not the headline
- Signal B (ACA/Marketplace): **SUPPORT** — frame experience in terms of FWA methodology, not career length
- Signal C (Intelligence Analysis): **SUPPORT** — let the analytical work lead; career length is secondary
- Signal D (Digital Forensics): **LEAD** — DCECTF context earns the seniority framing
- Signal E (Corporate Investigation): **LEAD** — private sector values experience depth; use full career framing
- Signal F (LE/Government): **LEAD** — LE and federal roles expect this framing

---

## Section 3 — Summary Sentence Variants

Select ONE variant based on the dominant active signal(s).
If two signals are co-equal (e.g., Signal A + Signal E for a corporate SIU role), use the first applicable variant.
Never combine variants. Never rewrite — use as written or update this file first.

### Variant A — SIU / Insurance Fraud (Signal A dominant)
"Medically retired Minnesota detective with investigative experience spanning financial crime, Business Email
Compromise, occupational fraud, and multi-victim scheme investigation, including a case that closed at felony
conviction with verified victim losses exceeding $360,000 and earned a written commendation from an Assistant
Dakota County Attorney. Certified Fraud Examiner candidate currently completing CFE examination requirements."

### Variant B — ACA / Marketplace / Healthcare Program Integrity (Signal B dominant)
"Medically retired Minnesota detective with investigative experience in fraud, waste, and abuse identification,
case documentation, and inter-agency coordination, developed across two investigative rotations and a five-year
pattern of self-initiated fraud case follow-up during patrol assignments. CFE candidate with direct experience
in SOP-governed casework, structured reporting, PII safeguarding, and interview technique across both telephonic
and in-person settings."

### Variant C — Intelligence / Crime Analysis (Signal C dominant)
"Medically retired Minnesota detective with investigative analysis experience spanning financial transaction
analysis, multi-system data convergence, link analysis, structured case documentation, and report writing for
county attorneys and federal investigators. CFE candidate with an 18-year adjunct instruction record in
investigative methodology and a consistent history of translating complex evidence into prosecutable case packages."

### Variant D — Digital Forensics (Signal D dominant)
"Medically retired Minnesota detective with digital forensics experience including 5,304 GB of digital
evidence processed across commercial forensic platforms (Cellebrite UFED, Magnet AXIOM, FTK, EnCase) as a
Dakota County Electronic Crimes Task Force investigator. CFE candidate with parallel experience in financial
crime investigation, search warrant authorship for digital accounts, and case documentation for federal referral."

### Variant E — Corporate / Private Sector Investigation (Signal E dominant)
"Medically retired Minnesota detective transitioning to corporate investigations with career experience in
occupational fraud, Business Email Compromise, financial crime, and inter-agency collaboration. Investigated
cases that collectively documented more than $440,000 in verified or alleged fraud losses with outcomes
including felony convictions, court-ordered restitution, and a written commendation from a county attorney.
CFE candidate."

### Variant F — LE / Government / Federal Contractor (Signal F dominant)
"Medically retired Minnesota detective with field experience across patrol, two investigative rotations,
digital forensics task force assignment, and a formal probation liaison program co-founded with Dakota County
Community Corrections. Fraud case history spans BEC, occupational fraud, and multi-victim financial crime;
one case drew a written commendation from an Assistant Dakota County Attorney. CFE candidate."

---

## Section 4 — Case Selection Matrix

For each case in CASE_BANK.md, role is LEAD, SUPPORT, or OMIT per signal.
**LEAD** = feature as the primary case reference; use the full bullet or cover letter paragraph.
**SUPPORT** = available as a secondary reference; use the condensed bullet.
**OMIT** = do not reference; the case type does not map to this role signal.

| Case | Signal A (FWA/SIU) | Signal B (ACA/Marketplace) | Signal C (Intelligence) | Signal D (Digital Forensics) | Signal E (Corporate) | Signal F (LE/Gov) |
|---|---|---|---|---|---|---|
| Case 1 — BEC / Shell Companies | LEAD | SUPPORT | SUPPORT | SUPPORT | LEAD | LEAD |
| Case 2 — Occupational Fraud | SUPPORT | SUPPORT | SUPPORT | OMIT | LEAD | SUPPORT |
| Case 3 — Park Theft / Multi-System ID | SUPPORT | OMIT | LEAD | SUPPORT | SUPPORT | SUPPORT |
| Case 4 — Commercial Burglary / Google Search Warrant | SUPPORT | OMIT | SUPPORT | LEAD | SUPPORT | LEAD |
| Probation Liaison Program | SUPPORT | LEAD | SUPPORT | OMIT | SUPPORT | SUPPORT |
| Self-Initiated Fraud Follow-Up (patrol) | LEAD | SUPPORT | SUPPORT | OMIT | LEAD | SUPPORT |

### Case Selection Rules
- Use at most TWO cases at LEAD level in any single resume or cover letter.
- A SUPPORT case may be referenced in bullets but not the cover letter opening paragraph.
- OMIT means do not mention the case in any section of the document.
- If Signal B (ACA/Marketplace) is dominant and no LEAD case has direct healthcare/enrollment framing,
  use the Probation Liaison Program as a proxy for inter-agency coordination and compliance documentation.

---

## Section 5 — Bullet Emphasis Rules

Within each job block, bullets should be ordered and trimmed to match active signals.
These rules govern WHICH bullets lead within a job block, not the text of the bullets themselves.
Bullet text is always drawn from CAREER_CONSTANTS.md or CASE_BANK.md as written.

### For Signal A (FWA/Insurance Fraud)
Lead with: fraud case outcomes (BEC, occupational fraud), interview experience, written reporting,
multi-agency coordination. De-emphasize: use-of-force, patrol stats, traffic enforcement.

### For Signal B (ACA/Marketplace)
Lead with: SOP-governed casework, structured written reporting, PII/PHI safeguarding, inter-agency
coordination (probation liaison, federal agents, county attorneys), self-initiated follow-up documentation.
De-emphasize: digital forensics volume stats, patrol narrative, SWAT coordination.

### For Signal C (Intelligence Analysis)
Lead with: financial transaction analysis (Excel, multi-source), multi-system data convergence (APS, pawn,
video, digital), report writing for prosecutorial audiences, crime alert issuance, lead development.
De-emphasize: use-of-force, tactical operations, physical evidence collection narrative.

### For Signal D (Digital Forensics)
Lead with: DCECTF assignment, platform enumeration (Cellebrite, AXIOM, FTK, EnCase), 5,304 GB stat,
Google search warrant authorship and return analysis, digital evidence preservation under time pressure.
De-emphasize: patrol blocks, probation liaison, adjunct teaching unless the JD specifically asks for it.

### For Signal E (Corporate Investigation)
Lead with: occupational fraud, BEC, financial crime outcomes, self-initiated case follow-up
demonstrating autonomy, end-user experience framing (claimants, witnesses, victims in non-law-enforcement
context). De-emphasize: SWAT coordination, tactical narrative, government contractor framing.

### For Signal F (LE/Government)
Lead with: investigative rotation history, task force assignment, probation liaison, federal coordination,
commendations from county attorney and supervisors. Full career length framing is appropriate here.
De-emphasize: private-sector reframing language.

---

## Section 6 — Suppression Rules (Hard Stops)

These rules override all other content selection decisions.

1. **Never surface the 5,304 GB / DCECTF stat in a document targeting Signal A, B, or E roles**
   unless the JD explicitly mentions digital forensics, electronic evidence, or ESI.

2. **Never use "25-year" or "decades" as the opening credential for Signal B or C roles.**
   Let the methodology and case outcomes lead; career length becomes context, not headline.

3. **Never include the adjunct instructor stat in Signal A, B, D, or E documents.**
   It is only relevant when the JD asks for training, knowledge transfer, or instructional experience.

4. **Never reference Case 4 (Commercial Burglary / Google Search Warrant) in Signal B documents.**
   The commercial burglary framing does not translate to ACA/healthcare program integrity context.

5. **Never reference Case 2 (Occupational Fraud) in Signal D documents.**
   The case has no digital component and creates a subject-matter mismatch for forensics roles.

6. **Never stack more than three quantified outcomes in the summary.**
   Select the top two or three most relevant to the dominant signal; do not list all of them.

7. **Always close cover letters with "Respectfully," followed only by "Troy J. Hokanson."**
   No repeated contact block. No "Thank you for your consideration" sentence before it.

8. **No em dashes, no semicolons in narrative prose, no exclamation points.**
   Governed by VOICE_STANDARD.md; this file enforces the same constraint.

---

## Section 7 — Role Family Quick Reference

Use this table as a fast lookup when a job title maps clearly to one of the four target families.

| Role Title Pattern | Primary Signal | Secondary Signal | Lead Stat | Lead Case | Summary Variant |
|---|---|---|---|---|---|
| SIU Investigator I / II / III | A | F | $360,000 BEC | Case 1 | Variant A |
| Insurance Fraud Investigator | A | E | $360,000 BEC | Case 1 | Variant A |
| Healthcare Fraud Investigator | A | B | Self-initiated pattern | Case 1 + Probation Liaison | Variant A |
| Marketplace Investigator | B | A | Self-initiated pattern | Probation Liaison + Case 1 condensed | Variant B |
| ACA Program Integrity Analyst | B | C | Structured reporting | Probation Liaison | Variant B |
| Crime Analyst | C | F | Multi-system convergence (Case 3) | Case 3 | Variant C |
| Intelligence Analyst | C | F | Case 3 + BEC financial analysis | Case 3 + Case 1 condensed | Variant C |
| Senior Crime Intelligence Analyst | C | A | BEC financial analysis | Case 1 full + Case 3 condensed | Variant C |
| Digital Forensic Analyst | D | F | 5,304 GB / DCECTF | Case 4 | Variant D |
| Corporate Investigator | E | A | $360,000 BEC + $80,000 occ fraud | Case 1 + Case 2 | Variant E |
| Senior Investigative Analyst | C | A | BEC financial analysis + Case 3 | Case 1 + Case 3 | Variant C |
| Senior SIU Investigator | A | E | $360,000 BEC | Case 1 full | Variant A |
| Fraud Examiner | A | E | $360,000 BEC + expungement denied | Case 1 + Case 2 | Variant A |

---

## Updating This File

**Trigger phrase:** "Update JD_CONTEXT_ENGINE" followed by the change needed.
Examples:
- "Update JD_CONTEXT_ENGINE — add Signal G for loss prevention / ORC roles"
- "Update JD_CONTEXT_ENGINE — add new case stat for [case label]"
- "Update JD_CONTEXT_ENGINE — add role family row for [job title]"

Do not modify Section 6 (Suppression Rules) without also updating VOICE_STANDARD.md if the
change affects tone or construction. All edits must remain consistent with VOICE_STANDARD.md,
CAREER_CONSTANTS.md, and CASE_BANK.md usage notes.

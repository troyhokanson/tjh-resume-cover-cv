# Troy Hokanson Profile Definitions

**Seven role lanes. One verified career record. Selected from the posting.**

This file defines the Layer 2 (audience-specific) voice rules referenced by [`VOICE_STANDARD.md`](./VOICE_STANDARD.md). Layer 1 hard rules apply to every profile and live in `VOICE_STANDARD.md`. The scanner reads this file conceptually but enforces the rules programmatically via the `PROFILE_RULES` dictionary in [`anti_ai_scan.py`](./anti_ai_scan.py).

If no profile is specified at scan time, the scanner uses **`adaptive`**. Application builds should still select and log a primary lane after reading the complete posting. [`ROLE_ADAPTATION_STANDARD.md`](./ROLE_ADAPTATION_STANDARD.md) controls authoring autonomy and hybrid-role decisions.

Each profile defines:

1. **Target roles** — what postings match this profile
2. **Voice emphasis** — what to lean into
3. **Required framing elements** — what must appear
4. **Preferred vocabulary** — words and phrases that read as Troy in this lane
5. **Banned vocabulary** — phrases that read as the wrong lane (in addition to Layer 1 bans)
6. **Empathy marker** — the canonical human-connection sentence pattern for this profile
7. **Worked example** — a short cover-letter opener and resume bullet rewritten in profile voice

---

## Profile 1: `vendor-solutions` (DEFAULT)

### Target roles

- Solutions Consultant (Thomson Reuters CLEAR, Magnet Forensics, Cellebrite, Flock Safety)
- Sales Engineer / Senior Sales Engineer (Axon, Veritone, Mark43, Flock Safety)
- Solutions Expert / Solutions Architect (Cellebrite, Magnet, Exterro)
- Customer Solutions Manager (Flock Safety, Axon, public-safety SaaS)
- Public Safety Manager / Public Safety Strategy Lead
- Technical Consultant (Public Safety, Government, Justice)
- Customer Success Engineer (public-safety SaaS)
- Field Application Specialist (forensics tooling)

### Voice emphasis

Lean into Troy's 5.5 years of hands-on Cellebrite / Magnet AXIOM / FTK / X-Ways / GrayKey operator experience as the END USER the vendor is selling to. Lean into his 18 years of adjunct teaching as proof he can train customers, run workshops, and present at conferences. Lean into the 10-agency Dakota County Electronic Crimes Task Force as proof he understands the multi-stakeholder buyer (chief, sheriff, county attorney, IT). Lean into the 25 years of credibility with sworn-officer audiences. Travel readiness 25%-60% is in-scope.

### Required framing elements (in addition to Layer 1)

- The phrase "from the end-user side of the workflow" or its equivalent must appear at least once in a cover letter or About section. Troy was the customer for these tools. That credibility is the whole pitch.
- At least one reference to teaching, training, or explaining to a non-technical audience. Examples: "I have spent 18 years explaining digital evidence to undergraduate Criminal Justice classes that had never seen a hash value." "I trained five sworn officers in Cellebrite UFED extraction over the course of three years."
- Comp / travel readiness: when the posting names travel above 25%, the cover letter must explicitly affirm travel readiness in one sentence. Plain, not performative.

### Preferred vocabulary

- field-tested, end-user experience, end-user workflow, operator perspective, daily driver, hands-on user, twelve years of Cellebrite UFED use (or current accurate figure), demonstrated to, walked through, trained sworn officers in, presented to chiefs and sheriffs, briefed county attorneys, explained to a jury, taught to undergraduates, ride-along with the analyst, in the lab, in court, at the prosecutor's table
- workflow integration, agency adoption, multi-jurisdictional rollout, ten-agency task force, partner-agency feedback, RFP response, after-action review, customer-readiness assessment

### Banned vocabulary for this profile (in addition to Layer 1)

- "evangelize" / "evangelist" — reads as Silicon Valley sales cliche
- "rockstar" / "ninja" / "guru" — disqualifying
- "drive revenue" / "drive top-line" — Troy is technical-side
- "thought leadership" — too marketing-department
- "passionate practitioner" — reads as performed enthusiasm
- "trusted advisor" — overused vendor cliche
- Heavy SIU adjuster vocabulary in resume bullets (recorded statement, EUO, claim file review). Save these for `siu-fraud`.

### Empathy marker

"The analysts and investigators on the receiving end of these tools." Variant: "the deputies, detectives, and analysts who have to make this software work on a Friday afternoon when a search warrant is on the clock."

### Worked example — cover-letter opener

> Twenty-five years in Minnesota law enforcement and prior U.S. Army service taught me what good investigative tooling looks like from the end-user side of the workflow. I conducted digital forensic examinations through the ten-agency Dakota County Electronic Crimes Task Force, personally processed 5,304 GB of digital evidence in 2020, and spent 18 years as an adjunct faculty member at the University of Phoenix explaining investigative concepts to undergraduate Criminal Justice students.

### Worked example — resume bullet

> Used Cellebrite UFED and Physical Analyzer while supporting examinations through the ten-agency Dakota County Electronic Crimes Task Force, connecting mobile-device findings with investigative records and explaining the results to investigators and prosecutors.

---

## Profile 2: `siu-fraud`

### Target roles

- Senior SIU Investigator / SIU Investigator (auto, home, life, property, workers' comp)
- Special Investigations Unit (Allstate, State Farm, GEICO, Travelers, Liberty Mutual, Progressive, USAA, Erie, AAA, Auto-Owners, Nationwide)
- Insurance Fraud Investigator
- Field Fraud Investigator (insurance carrier)
- Fraud Examiner (claims-side, carrier-side)
- Special Investigator (PBM, healthcare insurer)

### Voice emphasis

Lean into the verified investigative assignments, documented victim-loss figures, multi-victim case framing, work with prosecutors, and cooperation with partner agencies. Lean into the CFE in progress. Lean into the empathy. SIU hiring managers often include former investigators and adjusters. The voice should land plain, procedural, and outcome-focused.

### Required framing elements (in addition to Layer 1)

- Cover letter should use at least one privacy-safe, source-backed case outcome when it materially strengthens the application. Use only the verified loss amount, conviction, charge type, or commendation recorded in `CAREER_CONSTANTS.md` and `CASE_BANK.md`.
- Cover letter must reference fraud's effect on policyholders or premium-payers explicitly. Earned empathy, not slogan.
- Resume must include the CFE-in-progress status with honest framing (e.g., "Certified Fraud Examiner (CFE), credential in progress, exam scheduled [date]"). Never overclaim.
- At least one reference to working with the county attorney's office, federal prosecutor, or carrier counsel as the document hand-off audience.

### Preferred vocabulary

- recorded statement, examination under oath (EUO) familiarity, claim file review, indicator review, red flag, pattern of loss, suspicious loss, claim handler hand-off, SIU referral, NICB referral, insurance fraud bureau referral, restitution, charged out, complaint, plea, sentencing memorandum, victim impact statement, evidence chain of custody, written report for the county attorney
- multi-victim, multi-jurisdictional, organized fraud crew, Theft by Swindle, Aggravated Forgery, Identity Theft, Mail Fraud, Wire Fraud, Business Email Compromise, account takeover, romance scam, elder financial exploitation (cataloged elder-financial use is acceptable; "elder abuse" alone is not)

### Banned vocabulary for this profile (in addition to Layer 1)

- "demo," "demonstrated to the customer," "evangelize" — vendor lane
- "drive top-of-funnel" — wrong lane
- "sales cycle" / "deal cycle" — wrong lane
- "thought leadership" — wrong lane
- "intelligence cycle" / "F3EAD" / "i2 link analysis" as primary framing — save for `analyst-intelligence`
- "boots on the ground" — overused
- "white-collar crime" without specificity (always pair with case type)

### Empathy marker

"The trust between people and the systems designed to protect them." Variant: "the policyholders on the other end of those losses — the people whose premiums go up when fraud goes unanswered."

### Worked example — cover-letter opener

> Twenty-five years in Minnesota law enforcement shaped how I work a suspicious claim. I led a multi-victim Business Email Compromise investigation that documented more than $360,000 in victim losses and resulted in a felony conviction. The work also produced written recognition from a county prosecutor.

### Worked example — resume bullet

> Led a multi-victim Business Email Compromise investigation that documented more than $360,000 in victim losses, resulted in a felony conviction, and required coordination with local, state, and federal investigative partners.

---

## Profile 3: `analyst-intelligence`

### Target roles

- Investigations and Intelligence Analyst
- Senior Intelligence Analyst (financial crime, cybersecurity fraud)
- Financial Crime Analyst (BSA / AML / SAR-side)
- Cybersecurity Fraud Analyst
- Threat Intelligence Analyst (corporate)
- Corporate Security Analyst / Senior Corporate Security Analyst
- Insider Threat Analyst
- Trust & Safety Investigator (non-ICAC; ICAC-adjacent uses the `allow_icac` Layer 1 gate)
- Strategic Intelligence Analyst

### Voice emphasis

Lean into the writing. Lean into the 18 years of adjunct teaching as proof Troy writes for audiences who were not there. Lean into the Master's degree (M.A. Police Leadership, GPA 3.94) and the OSINT, link-analysis, and structured-analytic-technique exposure. Lean into the digital forensic underpinning (Cellebrite, FTK, X-Ways) as the source of the data the analyst would normally consume. Lean into pattern recognition across cases. Lean into the SAR/STR familiarity (cataloged training hours back this up).

### Required framing elements (in addition to Layer 1)

- Cover letter must reference written products explicitly. Example: "I wrote the search warrant affidavits, the after-action reports, and the case summaries that went to the county attorney."
- Cover letter must reference at least one example of explaining technical or investigative material to a non-technical audience.
- Resume must surface OSINT, link analysis, pattern recognition, or structured-analytic-technique exposure where supportable, with honest framing.
- Tooling must distinguish what is mastered, what is operator-familiar, and what is in progress. Same honest-positioning rule as the other profiles, but more visible here because analyst hiring managers screen on tooling lists.

### Preferred vocabulary

- written intelligence product, finished intelligence, raw to finished, all-source, link analysis, network analysis, pattern recognition, structured analytic technique, key intelligence question, key judgment, alternative hypothesis, indicators, warning, OSINT, SOCMINT (where supportable), tradecraft (used sparingly), analyst-to-investigator hand-off, written for the chief, written for the deputy director, briefed to a non-technical audience, distilled from
- typology, fraud typology, suspicious activity report (SAR), structuring, layering, smurfing, account takeover, synthetic identity, mule account, romance scam typology, BEC typology, AML red flag

### Banned vocabulary for this profile (in addition to Layer 1)

- "demo," "demonstrated to the customer," "evangelize" — vendor lane
- "drive revenue" — wrong lane
- "recorded statement," "EUO," "claim file" as primary framing — save for `siu-fraud`
- "boots on the ground" as the primary value prop — Troy is positioning as the analyst, not the field operator
- "deep dive" — banned at Layer 1, doubly inappropriate here
- "actionable intelligence" — used by everyone, signals nothing. Prefer "intelligence the customer could act on" or restructure.

### Empathy marker

"Writing for audiences who were not there for the investigation." Variant: "the chief, the prosecutor, or the board member reading a one-page summary of a six-month case at 11pm on a Sunday."

### Worked example — cover-letter opener

> Twenty-five years in Minnesota law enforcement taught me to write for audiences who were not there for the investigation. I converted multi-month digital forensic examinations into search-warrant affidavits, case summaries, and briefings for prosecutors, command staff, and partner agencies.

### Worked example — resume bullet

> Produced written intelligence products from 5,304 GB of digital evidence processed in 2020, including search warrant affidavits, after-action reports, and case summaries written for non-technical audiences in the county attorney's office and the Dakota County Electronic Crimes Task Force partner agencies.

---

## Profile 5: `customer-success`

### Target roles

- Customer Success Manager / Senior or Strategic CSM
- Customer Enablement Manager
- Agency Success Manager
- Customer Onboarding or Adoption Manager

### Voice emphasis

Lead with customer adoption, training, stakeholder relationships, issue resolution, change management, and the ability to translate complex tools into useful workflows. Use adjunct teaching, multi-agency coordination, end-user experience, and verified client work as transferable evidence. Do not claim renewals, ARR, churn, NRR, QBR ownership, CRM expertise, or a book of business unless verified.

### Format and framing

Use an outcome-oriented ATS resume with a concise customer-value summary, relevant transferable achievements, and a focused technology section. Translate experience honestly; do not rename prior jobs or disguise investigative work.

---

## Profile 6: `technical-account-management`

### Target roles

- Technical Account Manager
- Customer Success Engineer
- Technical Customer Success Manager
- Service Delivery Manager
- Implementation-oriented customer technical roles

### Voice emphasis

Lead with technical discovery, troubleshooting, escalation coordination, implementation support, workflow integration, training, documentation, and product feedback. Connect tools to operational or customer results. Do not claim formal SaaS account ownership, SLAs, cloud architecture, ticket volumes, or renewal quotas without evidence.

### Format and framing

Use a hybrid customer/technical ATS resume. Put relevant technical capabilities near the top and explain the transfer from operator, investigator, instructor, or cross-agency coordinator without overstating direct TAM experience.

---

## Profile 7: `dfir-cyber`

### Target roles

- Digital Forensic Examiner
- DFIR or Cyber Investigations role
- Cybercrime Investigator
- Incident Response Investigator
- Digital Forensics Consultant

### Voice emphasis

Lead with acquisition, preservation, examination, validation, chain of custody, mobile and computer forensics, evidence volume, forensic reporting, and communication with technical and non-technical audiences. Separate primary platforms from supplemental tools and label developing cyber or incident-response skills honestly.

### Format and framing

Use a technical ATS resume with an early tools and methods section, representative examinations or projects, quantified evidence work, and relevant training. Avoid generic customer-success, insurance, or leadership-heavy wording unless the posting is genuinely hybrid.

---

## Profile Selection at Scan Time

```bash
# Default (vendor-solutions):
python anti_ai_scan.py /path/to/cover.pdf cover

# Explicit profile:
python anti_ai_scan.py /path/to/cover.pdf cover --profile siu-fraud
python anti_ai_scan.py /path/to/cover.pdf cover --profile analyst-intelligence
python anti_ai_scan.py /path/to/cover.pdf cover --profile vendor-solutions

# Wrapper with friendly output:
python scan_and_report.py /path/to/cover.pdf cover --profile siu-fraud
```

See [`PROFILE_SELECTOR.md`](./PROFILE_SELECTOR.md) for the upstream logic that picks a profile from a job posting URL or title.

------

## Profile 4: `corporate-security-investigations`

### Target roles

- Global Special Investigator
- Corporate Global Investigator
- Corporate Security Investigator
- Senior Corporate Investigator
- Employee Relations Investigator with security scope
- Insider Threat Investigator
- Workplace Violence / Threat Assessment Investigator
- Global Security Investigations
- Enterprise Investigations
- Ethics and Compliance Investigator with investigative authority

### Voice emphasis

Lead with corporate risk, colleague safety, sensitive internal investigations, fact-finding, interviews, digital evidence, data loss, insider threat, workplace violence, and executive-ready reporting.

Do not lead with "retired police officer." Do not lead with "25-year law enforcement veteran." Use that as credibility after the corporate investigation frame is already set.

This profile should read like a serious corporate security investigator who has handled real cases, preserved evidence, interviewed people, coordinated with legal decision-makers, and written reports leaders could act on.

### Required framing elements

- Must include the phrase "corporate investigations" or "enterprise investigations" in the summary or opening.
- Must include "colleague safety," "employee misconduct," "insider threat," "data loss," or "workplace violence" when supported by the posting.
- Must include at least two specific investigation examples from the case bank, but sanitized for privacy.
- Must include one digital evidence example.
- Must include one threat, safety, harassment, or violence example.
- Must include one financial crime, fraud, or misconduct example when the posting mentions financial crimes.
- Must frame law enforcement as transferable investigative judgment, not as the main identity.

### Preferred vocabulary

corporate investigations, enterprise investigations, colleague safety, employee misconduct, insider threat, data loss, cyber activity, workplace violence, threat assessment, fact-finding, investigative findings, evidence preservation, executive-ready reporting, Legal, Human Resources, Internal Audit, Cyber Security, confidential investigation, reputational risk, business risk, risk mitigation, investigative judgment, misconduct review, internal inquiry, case intake, investigative plan, findings memo, leadership briefing

### Banned vocabulary

retired police officer as opener, 25-year law enforcement veteran as opener, street cop, patrol-heavy framing, criminal justice career, boots on the ground, passion for investigations, lifelong service, badge-forward framing, policyholder premium language, claim file review, recorded statement, EUO, demo, customer workflow, end-user side of the workflow

### Empathy marker

"The people inside the organization who need the process to be fair, careful, and defensible."

Variant: "the employee, manager, attorney, or business leader who needs a clear answer without turning the investigation into theater."

### Worked example — cover-letter opener

Aon’s Global Special Investigator role fits the part of my background that has always mattered most: careful fact-finding in sensitive, high-liability situations. My investigative work has included fraud, employee-style misconduct, threats, harassment, digital evidence, search warrants, interviews, and written findings prepared for prosecutors, command staff, and partner agencies.

### Worked example — resume bullet

Led complex investigations involving fraud, threats, harassment, digital evidence, vulnerable victims, and financial crimes, translating witness interviews, electronic evidence, records review, and case timelines into written findings for legal and command-level decision-makers.

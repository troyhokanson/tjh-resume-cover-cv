# Profile Selector Logic

**Pick the right profile from the job posting before building.**

This file is the upstream decision tree that maps a job posting to one of the four profiles defined in [`PROFILES.md`](./PROFILES.md). Run this before you scan and before you build. The wrong profile produces the wrong document and wastes a real submission slot.

For law-enforcement technology, SLED, public-safety SaaS, digital evidence, ALPR, RTCC, CAD/RMS, body-worn camera, DFR, investigative-data, or DFIR vendor roles, also read [`SLED_PUBLIC_SAFETY_VENDOR_STRATEGY.md`](./SLED_PUBLIC_SAFETY_VENDOR_STRATEGY.md).

If you cannot decide, **default to `vendor-solutions`** and note the uncertainty in the build log.

---

## Step 1: Read the posting title

| Title contains | Profile |
|---|---|
| Solutions Consultant, Senior Solutions Consultant, Technical Solutions Consultant | `vendor-solutions` |
| Solutions Expert, Solutions Architect, Technical Solutions Architect | `vendor-solutions` |
| Solutions Engineer, Senior Solutions Engineer, Public Safety Solutions Engineer | `vendor-solutions` |
| Sales Engineer, Senior Sales Engineer, Public Safety Sales Engineer | `vendor-solutions` |
| Customer Solutions Manager, Customer Solutions Lead, Customer Solutions Architect | `vendor-solutions` |
| Customer Success Manager, Senior Customer Success Manager, Strategic Customer Success Manager | `vendor-solutions` when the employer serves public safety, law enforcement, justice, DFIR, or SLED |
| Scaled Customer Success Manager, Growth Customer Success Manager, Customer Success Manager - Majors | `vendor-solutions` when the employer serves public safety, law enforcement, justice, DFIR, or SLED |
| Customer Success Engineer, Customer Success Advocate, Agency Success Manager | `vendor-solutions` |
| Technical Account Manager, Senior Technical Account Manager | `vendor-solutions` when the product serves public safety, investigations, evidence, or DFIR |
| Customer Engagement Manager, Engagement Manager, Customer Program Manager | `vendor-solutions` when customer implementation or adoption is the core duty |
| Account Manager - Law Enforcement, Strategic Account Manager - Public Safety | `vendor-solutions` |
| Public Safety Manager, Public Safety Strategy, Public Safety Strategist | `vendor-solutions` |
| Public Safety Advisor, Public Safety Technology Advisor, Public Safety Subject-Matter Expert | `vendor-solutions` |
| Law Enforcement Subject-Matter Expert, Industry Consultant - Public Safety | `vendor-solutions` |
| Technical Consultant - Public Safety / Government / Justice | `vendor-solutions` |
| Implementation Consultant, Senior Implementation Consultant, Implementation Specialist | `vendor-solutions` when the employer is a public-safety or investigative-technology vendor |
| Implementation Manager, Professional Services Consultant, Service Delivery Consultant | `vendor-solutions` when duties are individual-contributor, project, or customer-outcome focused |
| Public Safety Project Manager, Service Delivery Project Manager, Deployment Program Manager | `vendor-solutions` |
| Customer Onboarding Manager, Customer Onboarding Consultant, Adoption Consultant | `vendor-solutions` |
| Business Analyst - Public Safety, Business Analyst - Justice | `vendor-solutions` |
| Field Application Specialist, Product Specialist - Public Safety / Forensics | `vendor-solutions` |
| Investigative Trainer, Technical Trainer, Customer Training Consultant | `vendor-solutions` |
| Training Specialist - Public Safety, Law Enforcement Trainer, Customer Education Manager | `vendor-solutions` |
| Customer Enablement Manager, Product Trainer, Curriculum Developer - Public Safety | `vendor-solutions` |
| Instructor - Digital Investigations, Instructor - Geolocation Investigations | `vendor-solutions` |
| DFR Customer Success Manager, Customer Success Manager - DFR | `vendor-solutions` |
| DFR Program Manager, DFR Implementation Consultant, DFR Training Specialist | `vendor-solutions` |
| DFR Technical Account Manager, Public Safety Drone Solutions Consultant | `vendor-solutions` |
| Digital Evidence Consultant, Evidence Solutions Consultant, ALPR Solutions Consultant | `vendor-solutions` |
| Real-Time Crime Center Solutions Consultant, CAD/RMS Implementation Consultant | `vendor-solutions` |
| Digital Forensics Consultant, Mobile Forensics Consultant, Forensic Solutions Consultant | `vendor-solutions` when employed by a vendor or professional-services team |
| Investigative Analyst or Geolocation Analyst at a public-safety vendor | `analyst-intelligence` unless the role is mainly customer training, implementation, demos, or adoption, then `vendor-solutions` |
| SIU Investigator, Senior SIU Investigator, Special Investigations Unit | `siu-fraud` |
| Insurance Fraud Investigator, Field Fraud Investigator, Special Investigator - carrier | `siu-fraud` |
| Fraud Examiner - claims-side or carrier-side | `siu-fraud` |
| Investigations and Intelligence Analyst | `analyst-intelligence` |
| Senior Intelligence Analyst, Financial Crime Analyst, AML Analyst | `analyst-intelligence` |
| Threat Intelligence Analyst - corporate | `analyst-intelligence` |
| Corporate Security Analyst, Senior Corporate Security Analyst | `analyst-intelligence` |
| Trust & Safety Investigator - non-ICAC | `analyst-intelligence` |
| Global Special Investigator, Corporate Global Investigator, Corporate Security Investigator | `corporate-security-investigations` |
| Senior Corporate Investigator, Enterprise Investigator, Ethics Investigator | `corporate-security-investigations` |
| Insider Threat Investigator, Workplace Violence Investigator, Threat Assessment Investigator | `corporate-security-investigations` |

**Manager-title rule:** Do not assume a title containing `Manager` requires direct reports. Read the responsibilities. Customer Success Manager, Account Manager, Implementation Manager, Program Manager, Technical Account Manager, and Engagement Manager are often individual-contributor roles.

## Step 2: Read the company

| Company type | Tiebreaker |
|---|---|
| Public-safety / law-enforcement technology vendor | Strong pull toward `vendor-solutions` even if the title is generic. |
| Digital forensics / digital evidence vendor | Strong pull toward `vendor-solutions` for customer, training, solutions, implementation, and professional-services work. Use `analyst-intelligence` for internal examiner or analyst work. |
| DFR / public-safety drone vendor | Strong pull toward `vendor-solutions` for customer success, training, implementation, program, and solutions roles. |
| ALPR / RTCC / investigative-intelligence vendor | Strong pull toward `vendor-solutions`. |
| CAD / RMS / dispatch / justice software vendor | Strong pull toward `vendor-solutions` for implementation, professional services, business analyst, customer success, and training roles. |
| LexisNexis Risk Solutions Government / Public Safety | Strong pull toward `vendor-solutions` for Accurint, Accurint One, Accurint Virtual Crime Center, Accurint TraX / ZetX, training, product, account, implementation, and service-delivery roles. Use `analyst-intelligence` for analyst-only geolocation or investigative-analysis positions. |
| Flock Safety, Axon, Cellebrite, Magnet Forensics, Skydio, Motorola Solutions, Mark43, Tyler Technologies, Peregrine, SoundThinking, Genetec, RapidSOS, DroneSense, BRINC, Paladin, Rekor, CentralSquare, Hexagon, Veritone | Strong pull toward `vendor-solutions` when the job is customer-facing, implementation, training, solutions, technical account, program, or product-adoption focused. |
| Insurance carrier | Strong pull toward `siu-fraud`. |
| Bank / fintech / payments | Strong pull toward `analyst-intelligence`. |
| Tech platform corporate security | Strong pull toward `analyst-intelligence`, unless the title is investigator-led. |
| Healthcare insurer or PBM | `siu-fraud` for SIU titles, `analyst-intelligence` for analyst titles. |
| Corporate security or global investigations team | Strong pull toward `corporate-security-investigations`. |
| Consulting investigations firm | Default to `analyst-intelligence`; flip to `corporate-security-investigations` if title is investigator-led. |

## Step 3: Read the JD body for tooling and verbs

If the JD is heavy on:

- **demo, customer demos, RFP, RFI, proof of concept, discovery, partner agencies, workshops, customer training, implementation, onboarding, adoption, go-live, customer outcomes, account health, technical account, QBR, professional services, conference, territory, travel** -> `vendor-solutions`
- **public safety, SLED, law enforcement, CJIS, ALPR, body-worn camera, fleet video, digital evidence, RTCC, CAD, RMS, dispatch, DFR, UAS, customer agency, command staff, patrol workflow** -> strong `vendor-solutions` signal when paired with customer-facing duties
- **Accurint, Accurint One, Accurint Virtual Crime Center, Accurint TraX, ZetX, geolocation, cellular records, Google Earth, investigative trainer** -> `vendor-solutions` for training, customer, solutions, product, account, and service-delivery duties; `analyst-intelligence` for analyst-only duties
- **Cellebrite, UFED, Physical Analyzer, Magnet AXIOM, FTK, X-Ways, GrayKey, mobile forensics, forensic examiner** -> `vendor-solutions` when customer-facing; `analyst-intelligence` when examination or analysis is the primary output
- **recorded statement, EUO, claim file, indicator review, NICB, restitution, charged out, plea, victim, premium** -> `siu-fraud`
- **SAR / STR, AML, structured analytic, link analysis, finished intelligence, written products, briefing, OSINT, typology, key judgment** -> `analyst-intelligence`
- **employee misconduct, colleague safety, workplace violence, insider threat, data loss, cyber activity, Legal, HR, Internal Audit, enterprise risk, corporate security, business leaders, investigative findings** -> `corporate-security-investigations`

If two profiles tie, prefer the one supported by the company tiebreaker. If still tied, default to `vendor-solutions` and log the uncertainty.

## Step 4: Apply remote-first and travel filters

For `vendor-solutions` roles, use [`SLED_PUBLIC_SAFETY_VENDOR_STRATEGY.md`](./SLED_PUBLIC_SAFETY_VENDOR_STRATEGY.md) to score location and travel.

Priority order:

1. Fully remote United States
2. Home-based or territory-based with reasonable travel
3. Remote roles compatible with Minnesota now and southwest Washington after relocation
4. Minneapolis-area hybrid before relocation when unusually strong
5. Portland / Vancouver / southwest Washington hybrid after relocation

Travel guidance:

- 0-25%: preferred
- 26-40%: acceptable
- 41-50%: selective
- More than 50%: apply only when the role's compensation, fit, and long-term value justify it

A `remote` label does not mean low travel. Read the entire posting.

## Step 5: Confirm with the credentials catalog

Run a lookup against [`skills/troy-credentials-library/credentials_catalog.json`](./skills/troy-credentials-library/credentials_catalog.json). If the profile selection produces fewer than three usable certs or documented experience assets from the catalog, the profile may be wrong. Re-read the JD and reselect.

Profile-to-cert and experience coverage rough floor:

- `vendor-solutions` -> at least three of: Cellebrite UFED, Magnet AXIOM, FTK, X-Ways, GrayKey, LexisNexis Accurint, ZetX / Accurint TraX, cell-site analysis, Google Earth, NW3C CCCI, adjunct teaching, FTO, reserve academy development, ALPR project, BCA Law Enforcement Supervision & Management.
- `siu-fraud` -> at least three of: NW3C CCCI, Reid Technique, Financial Crimes Investigation, Show Me the Money / TCORCA Forensic Accounting, Business Email Compromise case, CFE in progress.
- `analyst-intelligence` -> at least three of: NW3C CCCI, OSINT training, Accurint, ZetX / Accurint TraX, cell-site / historical cellular analysis, investigative writing / report writing training, Master's in Police Leadership, adjunct teaching as writing-for-audiences proof.
- `corporate-security-investigations` -> at least three of: Reid Technique, search warrant training, threat / crisis response training, workplace violence / active shooter response, Cellebrite / FTK / X-Ways, NW3C cybercrime, forensic accounting, BCA supervision and management.

If the floor cannot be met for any profile, the posting probably is not a fit. Note the gap in the build log and discuss with Troy before applying.

## Corporate security document strategy

```yaml
document_strategy:
  profile: corporate-security-investigations
  lead_identity: corporate investigator
  supporting_identity: retired detective / digital forensics SME
  primary_examples:
    - digital evidence / data loss
    - workplace threat / harassment / safety
    - fraud / financial crime
  examples_to_suppress:
    - patrol-heavy material
    - generic 25-year veteran language
    - real estate transition unless relevant
  tone:
    - mature
    - corporate
    - precise
    - calm under pressure
    - not salesy

evidence_pack:
  required:
    - one fraud / financial crime example
    - one digital evidence / cyber-adjacent example
    - one threat / safety / sensitive-person matter
  max_examples: 3
  no_generic_claim_without_example: true
```

## Step 6: Edge cases

- **Hybrid Sales Engineer + Solutions Consultant** at a forensics vendor -> `vendor-solutions`. Do not split the cover letter.
- **Customer Success Manager or Account Manager with `Manager` in the title but no direct reports** -> treat as a senior individual-contributor `vendor-solutions` role.
- **SIU title at a vendor company** -> `siu-fraud` if the JD reads as investigation-side; `vendor-solutions` if it reads as customer-product, training, implementation, or carrier-product-side.
- **Financial Crime Investigator** at a bank -> usually `analyst-intelligence`. Confirm via Step 3 verbs.
- **Public Safety Sales Engineer** at Axon, Veritone, Mark43, Flock, Peregrine, Motorola, or LexisNexis Risk Solutions -> `vendor-solutions`.
- **Investigative Trainer at LexisNexis Risk Solutions** -> `vendor-solutions`; lead with Accurint, ZetX / Accurint TraX, cellular investigations, Google Earth, teaching, and curriculum development.
- **Geolocation Investigations Analyst at LexisNexis Risk Solutions** -> `analyst-intelligence` when case analysis is primary; use `vendor-solutions` if the role primarily trains or supports customers.
- **DFR role requiring Part 107 within a stated onboarding period** -> potentially viable; state willingness to earn it. Do not claim certification before completion.
- **DFR role requiring extensive logged flight time or advanced aviation credentials** -> likely gap; score cautiously.
- **Trust & Safety Investigator** roles explicitly involving ICAC / child safety -> still `analyst-intelligence`, but build with `allow_icac=True` on the Layer 1 scanner gate.

## Step 7: Log it

In the build log, cover-letter file header comment, or commit message, include:

```text
Profile: vendor-solutions
Posting: Investigative Trainer - LexisNexis Risk Solutions
URL: [posting URL if available]
Verified live: [date]
Remote status: [fully remote / home-based / territory / hybrid / onsite]
Travel: [percentage or unknown]
Direct reports: [yes / no / unclear]
allow_icac: False
```

The scanner will refuse to pass a document whose source comment names one profile while the body reads as another. Tone is not enforced, so read the document out loud before sharing.

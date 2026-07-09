# Profile Selector Logic

**Pick the right profile from the job posting before building.**

This file is the upstream decision tree that maps a job posting to one of the four profiles defined in [`PROFILES.md`](./PROFILES.md). Run this before you scan and before you build. The wrong profile produces the wrong document and wastes a real submission slot.

If you cannot decide, **default to `vendor-solutions`** and note the uncertainty in the build log.

---

## Step 1: Read the posting title

| Title contains | Profile |
|---|---|
| Solutions Consultant, Solutions Expert, Solutions Architect, Solutions Engineer | `vendor-solutions` |
| Customer Solutions Manager, Customer Solutions Lead, Customer Solutions Architect | `vendor-solutions` |
| Sales Engineer, Senior Sales Engineer, Public Safety Sales Engineer | `vendor-solutions` |
| Public Safety Manager, Public Safety Strategy, Customer Success Engineer (public safety) | `vendor-solutions` |
| Field Application Specialist, Technical Consultant (Public Safety / Justice) | `vendor-solutions` |
| SIU Investigator, Senior SIU Investigator, Special Investigations Unit | `siu-fraud` |
| Insurance Fraud Investigator, Field Fraud Investigator, Special Investigator (carrier) | `siu-fraud` |
| Fraud Examiner (claims-side, carrier-side) | `siu-fraud` |
| Investigations and Intelligence Analyst | `analyst-intelligence` |
| Senior Intelligence Analyst, Financial Crime Analyst, AML Analyst | `analyst-intelligence` |
| Threat Intelligence Analyst (corporate) | `analyst-intelligence` |
| Corporate Security Analyst, Senior Corporate Security Analyst | `analyst-intelligence` |
| Trust & Safety Investigator (non-ICAC) | `analyst-intelligence` |
| Global Special Investigator, Corporate Global Investigator, Corporate Security Investigator | `corporate-security-investigations` |
| Senior Corporate Investigator, Enterprise Investigator, Ethics Investigator | `corporate-security-investigations` |
| Insider Threat Investigator, Workplace Violence Investigator, Threat Assessment Investigator | `corporate-security-investigations` |

## Step 2: Read the company

| Company type | Tiebreaker |
|---|---|
| Public-safety / forensics vendor | Strong pull toward `vendor-solutions` even if title is generic. |
| Insurance carrier | Strong pull toward `siu-fraud`. |
| Bank / fintech / payments | Strong pull toward `analyst-intelligence`. |
| Tech platform corporate security | Strong pull toward `analyst-intelligence`, unless the title is investigator-led. |
| Healthcare insurer or PBM | `siu-fraud` for SIU titles, `analyst-intelligence` for analyst titles. |
| Corporate security or global investigations team | Strong pull toward `corporate-security-investigations`. |
| Consulting investigations firm | Default to `analyst-intelligence`; flip to `corporate-security-investigations` if title is investigator-led. |

## Step 3: Read the JD body for tooling and verbs

If the JD is heavy on:

- **demo, customer demos, RFP, proof of concept, partner agencies, workshops, training delivery, conference, travel 25%+** -> `vendor-solutions`
- **recorded statement, EUO, claim file, indicator review, NICB, restitution, charged out, plea, victim, premium** -> `siu-fraud`
- **SAR / STR, AML, structured analytic, link analysis, finished intelligence, written products, briefing, OSINT, typology, key judgment** -> `analyst-intelligence`
- **employee misconduct, colleague safety, workplace violence, insider threat, data loss, cyber activity, Legal, HR, Internal Audit, enterprise risk, corporate security, business leaders, investigative findings** -> `corporate-security-investigations`

If two profiles tie, prefer the one supported by the company tiebreaker. If still tied, default to `vendor-solutions` and log the uncertainty.

## Step 4: Confirm with the credentials catalog

Run a lookup against [`skills/troy-credentials-library/credentials_catalog.json`](./skills/troy-credentials-library/credentials_catalog.json). If the profile selection produces fewer than three usable certs from the catalog, the profile is probably wrong. Re-read the JD and reselect.

Profile-to-cert coverage rough floor:

- `vendor-solutions` -> at least three of: Cellebrite UFED, Magnet AXIOM, FTK, X-Ways, GrayKey, NW3C CCCI, Supervisor Survival for Public Safety Managers, BCA Law Enforcement Supervision & Management.
- `siu-fraud` -> at least three of: NW3C CCCI, Reid Technique, Financial Crimes Investigation, Show Me the Money (TCORCA Forensic Accounting), Business Email Compromise case, CFE in progress.
- `analyst-intelligence` -> at least three of: NW3C CCCI, OSINT training, cell-site / historical cellular analysis, investigative writing / report writing training, Master's in Police Leadership, adjunct teaching as writing-for-audiences proof.
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

## Step 5: Edge cases

- **Hybrid Sales Engineer + Solutions Consultant** at a forensics vendor -> `vendor-solutions`. Do not split the cover letter.
- **SIU title at a vendor company** -> `siu-fraud` if the JD reads as investigation-side; `vendor-solutions` if it reads as carrier-product-side.
- **Financial Crime Investigator** at a bank -> usually `analyst-intelligence`. Confirm via Step 3 verbs.
- **Public Safety Sales Engineer** at Axon, Veritone, Mark43, Flock, Peregrine -> `vendor-solutions`.
- **Trust & Safety Investigator** roles that are explicitly ICAC / child-safety -> still `analyst-intelligence`, but build with `allow_icac=True` on the Layer 1 scanner gate.

## Step 6: Log it

In the build log, cover-letter file header comment, or commit message, include:

```text
Profile: corporate-security-investigations
Posting: Global Special Investigator - Aon
URL: [posting URL if available]
Verified live: [date]
allow_icac: False
```

The scanner will refuse to pass a document whose source comment names one profile while the body reads as another. Tone is not enforced, so read the document out loud before sharing.

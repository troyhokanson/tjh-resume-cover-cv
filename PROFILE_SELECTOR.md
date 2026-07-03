# Profile Selector Logic

**Pick the right profile from the job posting before building.**

This file is the upstream decision tree that maps a job posting to one of the three profiles defined in [`PROFILES.md`](./PROFILES.md). Run this in your head (or programmatically) before you scan, before you build. The wrong profile produces the wrong document and wastes a real submission slot.

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
| Threat Intelligence Analyst (corporate), Insider Threat Analyst | `analyst-intelligence` |
| Corporate Security Analyst, Senior Corporate Security Analyst | `analyst-intelligence` |
| Trust & Safety Investigator (non-ICAC) | `analyst-intelligence` || Global Special Investigator, Corporate Global Investigator, Corporate Security Investigator | `corporate-security-investigations` |
| Senior Corporate Investigator, Enterprise Investigator, Ethics Investigator | `corporate-security-investigations` |
| Insider Threat Investigator, Workplace Violence Investigator, Threat Assessment Investigator | `corporate-security-investigations` |

## Step 2: Read the company

| Company type | Tiebreaker |
|---|---|
| Public-safety / forensics vendor (Thomson Reuters, Magnet, Cellebrite, Axon, Veritone, Mark43, Exterro, Grayshift, Susteen) | Strong pull toward `vendor-solutions` even if title is generic. |
| Insurance carrier (Allstate, State Farm, GEICO, Travelers, Liberty Mutual, Progressive, USAA, Erie, AAA, Auto-Owners, Nationwide, Farmers) | Strong pull toward `siu-fraud`. |
| Bank / fintech / payments (JPM, Citi, Wells, Capital One, Stripe, Block, PayPal, Plaid, Wise) | Strong pull toward `analyst-intelligence`. |
| Tech platform corporate security (Meta, Google, Microsoft, Amazon, Apple, Adobe, Salesforce) | Strong pull toward `analyst-intelligence`. |
| Healthcare insurer or PBM (UnitedHealth, Optum, CVS Health, Elevance, Humana, Cigna) | `siu-fraud` for SIU titles, `analyst-intelligence` for analyst titles. |
| Consulting (Big 4, K2 Integrity, Kroll, Control Risks, Nardello, Mintz Group) | Default to `analyst-intelligence`; flip to `siu-fraud` if title is investigator-flavored. |

## Step 3: Read the JD body for tooling and verbs

If the JD is heavy on:

- **demo, customer demos, RFP, proof of concept, partner agencies, workshops, training delivery, conference, travel 25%+** → `vendor-solutions`
- **recorded statement, EUO, claim file, indicator review, NICB, restitution, charged out, plea, victim, premium** → `siu-fraud`
- **SAR / STR, AML, structured analytic, link analysis, finished intelligence, written products, briefing, OSINT, typology, key judgment** → `analyst-intelligence`
If the JD is heavy on:

- employee misconduct, colleague safety, workplace violence, insider threat, data loss, cyber activity, Legal, HR, Internal Audit, enterprise risk, corporate security, business leaders, investigative findings → `corporate-security-investigations`

If two profiles tie, prefer the one supported by the company tiebreaker. If still tied, default to `vendor-solutions`.

## Step 4: Confirm with the credentials catalog

Run a lookup against [`skills/troy-credentials-library/credentials_catalog.json`](./skills/troy-credentials-library/credentials_catalog.json). If the profile selection produces fewer than three usable certs from the catalog, the profile is wrong. Re-read the JD and reselect.

Profile-to-cert coverage (rough floor):

- `vendor-solutions` → at least three of: Cellebrite UFED, Magnet AXIOM, FTK, X-Ways, GrayKey, NW3C CCCI, Supervisor Survival for Public Safety Managers, BCA Law Enforcement Supervision & Management.
- `siu-fraud` → at least three of: NW3C CCCI, Reid Technique, Financial Crimes Investigation, Show Me the Money (TCORCA Forensic Accounting), Business Email Compromise case, CFE (in progress).
- `analyst-intelligence` → at least three of: NW3C CCCI, OSINT training, Cell-site / Historical Cellular Analysis (FBI), Investigative writing / report writing training, Master's in Police Leadership, 19 years adjunct teaching as a writing-for-audiences proof.

If the floor cannot be met for any profile, the posting probably is not a fit. Note the gap in the build log and discuss with Troy before applying.

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

## Step 5: Edge cases

- **Hybrid Sales Engineer + Solutions Consultant** at a forensics vendor → `vendor-solutions`. Do not split the cover letter.
- **SIU title at a vendor company** (rare; sometimes consulting arms of carriers) → `siu-fraud` if the JD reads as investigation-side; `vendor-solutions` if it reads as carrier-product-side.
- **Financial Crime Investigator** at a bank → usually `analyst-intelligence`. Confirm via Step 3 verbs.
- **Public Safety Sales Engineer** at Axon, Veritone, Mark43, Flock, Peregrine → `vendor-solutions`. Always.
- **Trust & Safety Investigator** roles that are explicitly ICAC / child-safety → still `analyst-intelligence`, but build with `allow_icac=True` on the Layer 1 scanner gate.
evidence_pack:
  required:
    - one fraud / financial crime example
    - one digital evidence / cyber-adjacent example
    - one threat / safety / sensitive-person matter
  max_examples: 3
  no_generic_claim_without_example: true
## Step 6: Log it

In the build log (cover-letter file header comment or commit message), include:

```
Profile: vendor-solutions
Posting: Solution Consultant, Government Risk/Fraud/Compliance — Thomson Reuters
URL: https://careers.thomsonreuters.com/us/en/job/JREQ200166/...
Verified live: 2026-05-29
allow_icac: False
```

The scanner will refuse to pass a document whose source comment names one profile while the body reads as another. (Tone is not enforced, but the profile name in the comment is checked against `--profile` at scan time.)

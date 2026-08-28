# Application Self-Identification and Accommodation Standard

**Status:** Mandatory application-stage privacy and truth standard  
**Last validated:** August 28, 2026  
**Scope:** Optional EEO, disability, demographic, veteran, diversity, and accommodation questions in U.S. employment applications

## Controlling rule

Protected traits are not job qualifications and must never enter Troy's job-fit score, employer ranking, resume tailoring, interview-probability estimate, or outcome analytics. This includes disability status, race, ethnicity, sex, sexual orientation, gender identity, religion, and genetic information.

Veteran **experience** is different: verified Army service may be used as career evidence when its duties are relevant. A protected-veteran category, disability rating, diagnosis, race, or orientation may not be inferred from that experience.

## What the evidence does and does not establish

There is no defensible public statistic that isolates the interview effect of selecting `I don't wish to answer` or `decline to self-identify` on a separate EEO form. Do not present an anecdote, correlation, or rejection sequence as a causal probability.

The best available evidence supports two narrower conclusions:

1. Federal guidance says voluntary disability self-identification for affirmative-action purposes must be confidential, separate from the application, and refusal may not produce adverse treatment. Race, sex, and national-origin self-identification should likewise be kept separate from the hiring application and not used as a selection basis.
2. Overt disability disclosure in application materials is a different exposure. A U.S. field experiment involving 6,016 accounting applications found 26% less employer interest for otherwise qualified applicants whose cover letters disclosed a disability. That result does not measure a confidential EEO form and does not establish Troy's personal odds.

ATS implementation varies. Greenhouse states that its standard EEOC responses are anonymized and available only in a restricted report. Do not assume every employer or every custom diversity survey has the same controls.

## Default decision table

| Application item | Default for interview-risk minimization | Exceptions and boundaries |
|---|---|---|
| Standard optional disability self-ID | Select the explicit `I don't wish to answer` or decline option when Troy prefers privacy | Truthfully selecting yes is lawful. Never select no if that would be untrue. A separately approved disability-targeted or federal hiring path may use disclosure intentionally. |
| Race or ethnicity survey | Decline when Troy prefers privacy | Answering truthfully is also valid. Do not change the answer as an application-optimization tactic. |
| Sex, gender identity, or sexual orientation survey | Decline when optional and privacy is preferred | Sexual orientation is generally a custom diversity-survey item, not a reason to alter resume content. Participate only by choice and after reading the stated privacy purpose. |
| General veteran question | Answer truthfully and use verified Army service in the resume when relevant | Army experience is a direct credential. Keep the locked service total and MOS history exact. |
| Protected-veteran or VEVRAA category | Do not claim; use decline unless separate eligibility is verified | `CAREER_CONSTANTS.md` controls: never use protected-veteran or VEVRAA language without an approved evidence update. |
| Accommodation question | Request only when an accommodation is needed for the current stage | Describe the functional accommodation needed. Do not volunteer a diagnosis, VA rating, or complete medical history. |
| Federal Schedule A or veterans-preference route | Route to the federal-application workflow for evidence verification | This is not governed by the generic private-vendor default and requires the correct supporting documentation. |

## Application-material rule

Do not place disability status, diagnosis, disability percentage, race, sexual orientation, gender identity, or other protected demographic details in a resume or cover letter merely to improve selection odds.

Disability may appear only when Troy expressly chooses identity-based advocacy, uses a documented targeted hiring authority, or needs to explain an accommodation. Even then, disclose the minimum necessary information.

Veteran experience may appear because it is verified employment history. Translate it by role:

- 95B Military Police: public-safety mission familiarity, field operations, accountability, and agency credibility when relevant.
- 11B Infantry and 19K Armor: mission execution, safety, adaptability, equipment accountability, and field operations when the posting values them.
- 88M Motor Transport: deployment, fleet, logistics, and equipment workflows when relevant.

Do not use a generic veteran bonus to satisfy SaaS, CRM, quota, API, integration, engineering, platform-administration, or people-management requirements.

## Accommodation timing

Troy does not need to disclose a disability before an interview merely to preserve the right to request an accommodation. Use the following timing rule:

1. If the application itself is inaccessible, request the needed accommodation immediately.
2. If an interview format requires an accommodation, request it when scheduling.
3. If no accommodation is needed during hiring, defer any work-related accommodation discussion until it becomes necessary.
4. Always answer the separate essential-functions question truthfully: whether the essential duties can be performed with or without reasonable accommodation.

## Data-handling rule

- Do not save screenshots or copies of completed demographic responses.
- Do not write disability, race, orientation, or other protected answers into Notion application records, Drive trackers, GitHub, or conversion dashboards.
- It is acceptable to record that the application was completed and submitted. Do not record which protected-category options were selected.
- Measure interview conversion by role family, employer, source, referral status, resume version, geography, compensation, and hard-gap profile—not by protected traits.

## Application QA checklist

- [ ] The demographic section is clearly optional or includes an explicit decline option.
- [ ] If declining, the explicit decline option was used instead of a false answer.
- [ ] No protected trait appears in the resume, cover letter, or open-text application answer unless Troy expressly approved that use.
- [ ] Veteran service is accurate: U.S. Army, 8 years 3 months, honorably discharged; MOS history matches `CAREER_CONSTANTS.md`.
- [ ] No protected-veteran or VEVRAA claim was made.
- [ ] Any accommodation request states the functional need and avoids unnecessary medical detail.
- [ ] Job-fit scoring and recommendation were completed without protected-trait inputs.

## Primary sources

- [EEOC preemployment disability inquiry guidance](https://www.eeoc.gov/laws/guidance/enforcement-guidance-preemployment-disability-related-questions-and-medical)
- [EEOC preemployment race inquiry guidance](https://www.eeoc.gov/pre-employment-inquiries-and-race)
- [EEOC veterans and the ADA employer guide](https://www.eeoc.gov/laws/guidance/veterans-and-americans-disabilities-act-guide-employers)
- [U.S. Department of Labor voluntary disability self-identification form](https://www.dol.gov/sites/dolgov/files/OFCCP/regs/compliance/sec503/Self_ID_Forms/503Self-IDForm.pdf)
- [Greenhouse EEOC questionnaire and reporting controls](https://support.greenhouse.io/hc/en-us/articles/205278605-Equal-employment-opportunity-and-affirmative-action-overview)
- [Ameri et al., disability hiring field experiment](https://www.nber.org/papers/w21560)

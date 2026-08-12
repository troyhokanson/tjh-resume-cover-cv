# Troy Hokanson Voice Standard

**Permanent voice, truth, and privacy guardrails. Role-specific wording, structure, emphasis, and formatting remain adaptive under [`ROLE_ADAPTATION_STANDARD.md`](./ROLE_ADAPTATION_STANDARD.md).**

This file is the canonical source of truth for the voice and anti-AI rules. The local skill (`linkedin-profile-optimizer/SKILL.md`) mirrors it, and the automated scanner (`anti_ai_scan.py`) enforces it on every build. If a document fails the scan, fix the source text and rebuild. Never share a document that did not pass.

---

## Architecture: Two Layers

This standard is organized in two layers.

- **Layer 1 — Hard safeguards.** Truth, privacy, PTSD-scope, factual precision, and high-signal anti-AI checks apply to every target. These safeguards do not prescribe one career identity or one document template.
- **Layer 2 — Role adaptation.** The AI selects industry-native vocabulary, framing, evidence, structure, and visual presentation after reading the complete posting. The available lanes include SIU, corporate security, customer success, technical account management, DFIR/cyber, intelligence/analytics, and solutions consulting.

[`ROLE_ADAPTATION_STANDARD.md`](./ROLE_ADAPTATION_STANDARD.md) governs authoring autonomy. [`PROFILES.md`](./PROFILES.md) supplies lane-specific guidance, and [`PROFILE_SELECTOR.md`](./PROFILE_SELECTOR.md) supplies selection logic. No profile is a master resume.

---

# LAYER 1 — HARD RULES (apply to every document, every profile)

## The Narrator

Every word must read as if Troy wrote it himself. The narrator is:

- Generation X (born 1971). Do not hardcode a current age in reusable standards.
- Medically retired Minnesota law-enforcement officer with 25 years of sworn service
- Master of Arts, Police Leadership, Administration and Education, University of St. Thomas, GPA 3.94
- 18 years as a remote adjunct faculty member teaching undergraduate Criminal Justice at the University of Phoenix
- U.S. Army veteran, honorably discharged. Use the exact verified duration from `CAREER_CONSTANTS.md`; never round it.
- Trained in the Reid Technique of Interviewing and Interrogation, FBI cell-site analysis, NW3C cybercrime investigation
- Empathetic. 25 years of public service shaped how he writes about victims, fraud impact, and trust.

## Core Voice Traits

- **Empathetic and humanistic, not corporate or detached.** Fraud is described as something that erodes trust between people and the systems meant to protect them, not as a "loss event" or "risk vector."
- **Plain Gen-X cadence.** Short sentences carry weight. Long sentences carry detail. Mechanical uniformity is an AI tell.
- **Master's-educated precision.** Vocabulary is exact, not ornate. Reduced, distilled, identified, documented, examined, traced, established, recovered, obtained. Never elevated, leveraged, harnessed, transformed.
- **Investigations-experienced specificity.** Names verified tools, outcomes, and jurisdictions. Never vague ("handled cases"); use source-backed language such as "led a multi-victim Business Email Compromise investigation that documented more than $360,000 in victim losses and resulted in a felony conviction."
- **Adjunct-faculty clarity.** Complex things are made plain, the way Troy explains evidence to a jury or a concept to a 200-level Criminal Justice class. Not academic. Not stiff. Explanatory.
- **Honest framing of skills he is still building.** Working proficiency, building competency, in progress, currently developing through directed self-study. Never overclaim.
- **Closes with one earned, plain sentence.** The AI may choose a restrained professional salutation that fits the employer and industry. Avoid canned enthusiasm and generic promises.

## Role-Adaptive Content Requirements

A cover letter must not be built from a universal three-item formula. The AI should choose the most persuasive verified evidence for the role and explain any meaningful transition or gap. Law-enforcement service, military service, teaching, case outcomes, and metrics are optional assets, not mandatory first-sentence ingredients.

A resume summary must lead with the professional identity most useful to the target. It may lead with SIU investigation, corporate investigations, customer success, technical account management, digital forensics, cyber investigations, intelligence analysis, or solutions consulting. It does not need to begin with "medically retired Minnesota detective."

The AI may shorten or omit experience that distracts from the target. It must never disguise Troy's actual titles or invent direct experience. See [`ROLE_ADAPTATION_STANDARD.md`](./ROLE_ADAPTATION_STANDARD.md).
## Markers That Violate Troy's Voice (never use, any profile)

- **Corporate / SaaS verbs:** leveraged, harnessed, spearheaded, championed, optimized, streamlined, transformed, delivered value, drove outcomes, empowered, elevated, unlocked, seamlessly
- **AI throat-clearing:** in today's environment, at the end of the day, needless to say, fundamentally, ultimately, ramping on
- **Performed enthusiasm:** I am excited, I am thrilled, I am eager, I look forward to discussing
- **Overclaim language:** expert in [X], deep expertise in [X] when Troy is actually building competency
- **Marketing-department openers:** "As a [title]...", "I bring", "I offer", "With over 25 years of experience..."

## Punctuation Rules (highest-signal AI tells)

| Punctuation | Rule |
|---|---|
| Em dash (—) | **Never. Anywhere. Zero exceptions.** Replace with a comma, period, or restructure the sentence. |
| En dash (–) | Never in prose. Plain hyphen acceptable in date fields only (1998-2024). |
| Double hyphen ( -- ) | **Never. Anywhere.** This is a direct substitution for an em dash and is equally forbidden. Use a comma or restructure. |
| Space-hyphen-space ( - ) | **Never as a separator between clauses or list items.** This is a visual em dash substitute and is equally forbidden. Use a comma, period, or semicolon instead. |
| Semicolon (;) | Never in cover letters or About / bio sections. Acceptable in resume bullets between parallel items. |
| Ellipsis (...) | Never. Use a period or rewrite. |
| Exclamation point (!) | Never in any professional content. Zero exceptions. |
| Curly / smart quotes (" ' ' ') | Never. Use straight quotes only. |
| Oxford comma | Use naturally, not mechanically. Mechanical consistency is itself an AI signal. |

**Preferred separators when em dashes, en dashes, double hyphens, or space-hyphen-space would otherwise be used:**
- Between a label and its value: use a comma. Example: `Certified Fraud Examiner (CFE), actively pursuing through ACFE, 2026.`
- Between parallel certifications or credentials: use a period to end each item, or a comma within a series.
- Between a clause and its modifier: rewrite as two sentences or use a comma.

## Number Conventions

- One through nine: spell out (four cases, nine interviews)
- 10 and above: numerals (25 years, 14 cases, $47,000)
- Statistics, case counts, technical measurements: always numerals regardless of size

## Contractions

- Resume / CV bullets: zero contractions. Always.
- Cover letters: maximum two contractions in the entire document. Prefer the uncontracted form.
- Possessives like "Master's degree" or "Comcast's customers" are not contractions and are fine.

## Closing

Use a restrained, professional closing appropriate to the employer and lane. Acceptable examples include `Respectfully,`, `Sincerely,`, and `Thank you,`. Do not force one closing across every application, and do not use performed enthusiasm.
## PTSD-Scope Hard Block (always, every profile)

The following terms must NEVER appear in any document Troy's name is on, regardless of profile or job target:

- homicide
- death investigation
- lethal force
- sexual assault
- criminal sexual conduct
- human trafficking

Additionally, CSAM / child exploitation / ICAC training references are blocked by default and only opened via the `allow_icac=True` flag for child-safety platform roles (Roblox Trust & Safety, NCMEC, tech platform child-safety teams).

## Law-Enforcement Identifier Privacy Hard Block

POST or peace-officer license numbers, badge numbers, internal personnel identifiers,
license dates, and standalone POST licensing credential lines must never appear in a
resume, cover letter, CV, recruiter packet, professional bio, one-pager, portfolio
page, or generated application artifact. Troy is not pursuing sworn law-enforcement
roles. Use experience-based framing instead, such as "25 years of sworn service" or
"medically retired Minnesota law-enforcement officer."

---

# LAYER 2 — ROLE-ADAPTIVE VOICE

Layer 2 is guidance, not a fixed script. Read the complete posting, select the primary lane under [`ROLE_ADAPTATION_STANDARD.md`](./ROLE_ADAPTATION_STANDARD.md), and use industry-native vocabulary only when supported by Troy's verified record. The full profile definitions live in [`PROFILES.md`](./PROFILES.md), and selection logic lives in [`PROFILE_SELECTOR.md`](./PROFILE_SELECTOR.md).

## vendor-solutions (default)

Target: Solutions Consultant, Sales Engineer, Solutions Expert, Public Safety Manager, Technical Consultant.
Emphasis: end-user expertise on the vendor's product, ability to demo and teach, customer empathy, 18 years adjunct teaching, field-tested tooling, travel readiness.
Avoid: SIU adjuster vocabulary, intelligence-analyst tradecraft vocabulary.
Empathy marker: "the analysts and investigators on the receiving end of these tools."

## siu-fraud

Target: SIU Investigator, Insurance Fraud Investigator, Special Investigations Unit, Fraud Examiner (claims-side).
Emphasis: investigation procedure, recorded statements, claim file review, evidence preservation, restitution outcomes, victim impact, CFE in progress, fraud-pattern recognition.
Avoid: sales/vendor verbs (demo, evangelize, customer success), heavy intel-cycle vocabulary.
Empathy marker: "the trust between people and the systems designed to protect them."

## analyst-intelligence

Target: Investigations and Intelligence Analyst, Financial Crime Analyst, Cybersecurity Fraud Analyst, Threat Intelligence Analyst, Corporate Security Analyst.
Emphasis: link analysis, pattern recognition, structured analytic technique, SAR/STR familiarity, OSINT, digital forensic underpinning, written intelligence products, briefing to non-technical audiences.
Avoid: sales-side verbs, claim-adjuster vocabulary, "boots on the ground" framing as the primary value prop.
Empathy marker: "writing for audiences who were not there for the investigation."

See [`PROFILES.md`](./PROFILES.md) for the full per-profile vocabulary lists, banned terms, framing examples, and worked rewrites.

---

## Automatic Enforcement

This standard is enforced by [`anti_ai_scan.py`](./anti_ai_scan.py), called at the bottom of every `build_*.py` script and at every share gate:

```python
from anti_ai_scan import scan_pdf
scan_pdf(PDF, doc_type="cover", profile="vendor-solutions")
```

CLI:

```bash
python anti_ai_scan.py /path/to/file.pdf cover --profile vendor-solutions
python scan_and_report.py /path/to/file.pdf cover            # default vendor-solutions
python scan_and_report.py /path/to/file.pdf cover --profile siu-fraud
```

The scanner raises `FailedScan` and hard-blocks the build on any Layer 1 violation OR any Layer 2 violation for the selected profile. Manual self-review is still required after the scan passes. The scanner catches phrases, not tone. Read the document out loud once before sharing.

If `--profile` is omitted, the scanner uses `adaptive`. Application builds should still record a selected primary lane after analyzing the posting.

---

## When to Update This File

Update this file when:

1. A new AI-flagged phrase is caught by ZeroGPT / Copyleaks / Grammarly during real submission review
2. Troy provides feedback that a document did not sound like him
3. A new voice marker (empathetic phrase, narrative anchor) proves effective in a successful application
4. The narrator facts change (age, retirement status, certifications, education)
5. A new profile is added or an existing profile changes target audience

Always update the canonical phrase list in `anti_ai_scan.py` at the same time so the rule is enforced automatically. Layer 1 changes update `FORBIDDEN_PHRASES` / `EXTRA_FLAGGED`. Layer 2 changes update `PROFILE_RULES` in the same file. Profile content lives in [`PROFILES.md`](./PROFILES.md).

# Troy Hokanson Voice Standard

**Permanent. Non-negotiable. Applied to every resume, cover letter, CV, recruiter packet, professional bio, one-pager, or any DOCX/PDF that bears Troy Hokanson's name.**

This file is the canonical source of truth for the voice and anti-AI rules. The local skill (`linkedin-profile-optimizer/SKILL.md`) mirrors it, and the automated scanner (`anti_ai_scan.py`) enforces it on every build. If a document fails the scan, fix the source text and rebuild. Never share a document that did not pass.

---

## Architecture: Two Layers

This standard is organized in two layers. Both layers apply to every document. Profile selection only changes Layer 2.

- **Layer 1 — Hard Rules.** Permanent, non-negotiable, identical across every job target. Punctuation, banned phrases, structural requirements, PTSD-scope. Enforced by `anti_ai_scan.py` regardless of profile.
- **Layer 2 — Profile Voice.** Audience-specific vocabulary, framing, and emphasis. Selected by the `--profile` flag at scan time. Three profiles are defined in [`PROFILES.md`](./PROFILES.md):
  - `vendor-solutions` (default) — Solutions Consultant, Sales Engineer, Solutions Expert, Public Safety Manager
  - `siu-fraud` — SIU Investigator, fraud examiner, insurance investigator
  - `analyst-intelligence` — Investigations and Intelligence Analyst, financial crime analyst, cybersecurity fraud analyst

If no profile is specified, the scanner defaults to `vendor-solutions`. This matches Troy's primary target archetype as of May 2026.

---

# LAYER 1 — HARD RULES (apply to every document, every profile)

## The Narrator

Every word must read as if Troy wrote it himself. The narrator is:

- 54 years old, Generation X (born 1971)
- Medically retired Minnesota detective with 25 years of sworn service
- Master of Arts, Police Leadership, Administration and Education, University of St. Thomas, GPA 3.94
- 18 years as a remote adjunct faculty member teaching undergraduate Criminal Justice at the University of Phoenix
- Nine-year U.S. Army veteran, honorably discharged
- Trained in the Reid Technique of Interviewing and Interrogation, FBI cell-site analysis, NW3C cybercrime investigation
- Empathetic. 25 years of public service shaped how he writes about victims, fraud impact, and trust.

## Core Voice Traits

- **Empathetic and humanistic, not corporate or detached.** Fraud is described as something that erodes trust between people and the systems meant to protect them, not as a "loss event" or "risk vector."
- **Plain Gen-X cadence.** Short sentences carry weight. Long sentences carry detail. Mechanical uniformity is an AI tell.
- **Master's-educated precision.** Vocabulary is exact, not ornate. Reduced, distilled, identified, documented, examined, traced, established, recovered, obtained. Never elevated, leveraged, harnessed, transformed.
- **Investigations-experienced specificity.** Names tools, names dollar amounts, names outcomes, names jurisdictions. Never vague ("handled cases"); always concrete ("led a multi-victim Business Email Compromise investigation that closed with $295,704.11 in court-ordered restitution").
- **Adjunct-faculty clarity.** Complex things are made plain, the way Troy explains evidence to a jury or a concept to a 200-level Criminal Justice class. Not academic. Not stiff. Explanatory.
- **Honest framing of skills he is still building.** Working proficiency, building competency, in progress, currently developing through directed self-study. Never overclaim.
- **Closes with one earned, plain sentence.** Never "I look forward to discussing." Never "I'm excited about the opportunity." Closing salutation is always `Respectfully,`.

## Three Things Every Cover Letter Must Contain

1. Both law enforcement and military credentials in the first sentence.
2. At least one concrete number or named case outcome from Troy's actual record. Examples:
   - The BEC case: $360,000+ in documented victim losses, $295,704.11 in court-ordered restitution, 15-year federal sentence
   - 5,304 GB of digital evidence processed in 2020
   - Ten partner agencies on the Dakota County Electronic Crimes Task Force
   - 20+ written commendations
   - $3.2M in real estate sales
   - 512 documented hours of investigation-relevant training
3. One sentence of genuine human connection between Troy's public service background and the real-world impact of the work — fraud raises premiums, denies legitimate claims, takes from people who cannot afford it; intelligence gaps cost lives; vendor tools that fail in the field cost cases. Earned, not performed. The exact framing is profile-specific (see Layer 2).

## Three Things Every Resume Summary Must Contain

1. "Twenty-five-year medically retired Minnesota detective and digital forensic examiner" or a near-equivalent opener that anchors the reader in his identity.
2. Quantified outcomes from real cases — felony convictions, restitution amounts, federal sentences, partner-agency adoption, training-hours total.
3. Honest tooling positioning — what is mastered (Cellebrite UFED, Magnet AXIOM, FTK, X-Ways, GrayKey, Python, API automation), what is being built (SQL, Tableau, Alteryx), what is in progress (CFE).

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

Cover letters always close with exactly:

```
Respectfully,
[48pt blank space for digital signature]
Troy Hokanson
```

Never use Sincerely, Best regards, Best, Thank you, Kind regards, or any other closing.

## PTSD-Scope Hard Block (always, every profile)

The following terms must NEVER appear in any document Troy's name is on, regardless of profile or job target:

- homicide
- death investigation
- lethal force
- sexual assault
- criminal sexual conduct
- human trafficking

Additionally, CSAM / child exploitation / ICAC training references are blocked by default and only opened via the `allow_icac=True` flag for child-safety platform roles (Roblox Trust & Safety, NCMEC, tech platform child-safety teams).

---

# LAYER 2 — PROFILE VOICE (selected by --profile flag)

Layer 2 controls vocabulary emphasis and framing per target audience. The full profile definitions live in [`PROFILES.md`](./PROFILES.md). The selector logic lives in [`PROFILE_SELECTOR.md`](./PROFILE_SELECTOR.md). What follows is a short overview.

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

If `--profile` is omitted, the scanner defaults to `vendor-solutions`. This matches Troy's primary target archetype as of May 2026.

---

## When to Update This File

Update this file when:

1. A new AI-flagged phrase is caught by ZeroGPT / Copyleaks / Grammarly during real submission review
2. Troy provides feedback that a document did not sound like him
3. A new voice marker (empathetic phrase, narrative anchor) proves effective in a successful application
4. The narrator facts change (age, retirement status, certifications, education)
5. A new profile is added or an existing profile changes target audience

Always update the canonical phrase list in `anti_ai_scan.py` at the same time so the rule is enforced automatically. Layer 1 changes update `FORBIDDEN_PHRASES` / `EXTRA_FLAGGED`. Layer 2 changes update `PROFILE_RULES` in the same file. Profile content lives in [`PROFILES.md`](./PROFILES.md).

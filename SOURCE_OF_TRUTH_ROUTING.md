# Source-of-Truth Routing and Writeback Standard

**Locked repository rule. Applies to every resume, CV, cover letter, recruiter packet, professional bio, portfolio entry, and job-application build.**

## Core Rule

Whenever a conversation produces a verified correction, clarified fact, new credential, award, metric, date, role detail, case outcome, or improved reusable description, the information must be written to the correct authoritative GitHub source in the same working session and branch before the tailored application is considered complete.

Application folders are outputs. They must never be the only storage location for reusable facts or language.

## Required Sequence

1. Identify whether the information is new, corrected, clarified, or merely job-specific.
2. Route reusable information to the authoritative source listed below.
3. Update that source first, or in the same commit sequence, on the active branch or pull request.
4. Update the tailored application file from the authoritative source.
5. Verify that both versions agree.
6. Report the authoritative file and commit or pull request to Troy.

## Routing Map

| Information type | Authoritative source |
|---|---|
| Employment titles, employers, locations, dates, duration, and role boundaries | `CAREER_CONSTANTS.md` |
| Higher-education teaching history, academic qualifications, faculty development, and teaching recognition | `TEACHING_FACULTY_CONSTANTS.md` |
| Certifications, courses, training hours, credential IDs, issuers, and status | `skills/troy-credentials-library/credentials_catalog.json` |
| Investigative cases, outcomes, quantified accomplishments, and case-specific language | `CASE_BANK.md` |
| Audience positioning and role-family strategy | `PROFILES.md` |
| Writing voice, prohibited language, tone, and punctuation rules | `VOICE_STANDARD.md` |
| Header, typography, color, margins, and document design | `HEADER_STANDARD.md`, `DOCX_NODE_STANDARD.md`, and `standards/document_design_standard.json` |
| Contact information handling | `config.py`, `.env`, and related configuration standards |
| Repository workflow and persistence rules | `SOURCE_OF_TRUTH_ROUTING.md` |
| Job-specific tailoring with no reusable fact or language | `applications/<date>_<employer>_<role>/` |

## Reusable-Language Test

Language is reusable when it accurately describes Troy's background and could reasonably appear in another application, profile, interview brief, or portfolio entry.

Examples:

- A better description of the Investigative Digital File is reusable and belongs in the relevant career or training source.
- A clarified award date belongs in the authoritative teaching or credential source.
- A job-specific sentence naming one employer's product may remain only in that application folder.

When uncertain, preserve the reusable factual core in the authoritative source and keep only the employer-specific adaptation in the application file.

## Hard Prohibitions

- Do not leave a new fact only inside an application resume or cover letter.
- Do not rely on chat memory as the permanent record.
- Do not create `*_CORRECTIONS.md`, override, patch-note, or sidecar files as a substitute for updating the authoritative source.
- Do not allow a tailored document to contradict an authoritative source.
- Do not silently overwrite a verified fact with inferred or AI-generated language.
- Do not mark an application package complete until writeback has occurred.

## Conflict Rule

When sources conflict, stop the build and resolve the conflict in the authoritative file before finalizing the application. The narrower authoritative source controls its subject area. For example, `TEACHING_FACULTY_CONSTANTS.md` controls teaching and faculty facts even if an older duplicate remains in `CAREER_CONSTANTS.md` pending reconciliation.

## Branch and Pull-Request Rule

- Use the active application branch and pull request when one exists.
- If no application branch exists, create a maintenance branch and pull request for the source update.
- Keep the source update and related application update in the same pull request whenever practical.
- State clearly when the change has been committed but not yet merged.

## Completion Statement

Every completed build should identify:

- the tailored application files created or updated;
- the authoritative source file updated;
- the branch or pull request containing the changes; and
- any unresolved verification issue.

This rule is mandatory and may not be skipped for convenience.
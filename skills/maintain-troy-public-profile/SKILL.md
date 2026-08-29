---
name: maintain-troy-public-profile
description: Audit and synchronize Troy Hokanson's approved public professional profile across TroyHokanson.com, GitHub, LinkedIn, and Notion when a durable career fact, credential, chronology, privacy rule, or public evidence citation changes. Do not use for routine role-specific application tailoring.
---

# Maintain Troy Public Profile

Keep Troy's public professional identity accurate, privacy-safe, and consistent without turning public systems or this skill into competing fact stores.

## Governing Sources

Use the current `troyhokanson/tjh-resume-cover-cv` repository as the authoritative standards and career-data source. Read, at minimum:

- `PUBLIC_PROFILE_CONTRACT.json`
- `PRIVACY_STANDARD.md`
- `CAREER_CONSTANTS.md`
- `TRAINING_CONSTANTS.md` when credentials or training are involved
- `CONTACT_STANDARD.md` when public contact information is involved

Use primary records in Google Drive to verify disputed facts, but keep originals private. Use Notion for operating status, decisions, and next actions. Treat LinkedIn and the website as public derivatives, never as authorities.

The only production portfolio repository is:

```text
troyhokanson/troyhokanson.github.io
```

`troy-hokanson/portfolio` is an unused duplicate. Never route production work, evidence links, or public-profile automation to it. Verify that it remains private.

## When to Run

Run this skill when:

- a durable career fact, date, credential, metric, or public positioning statement changes;
- Troy requests a portfolio, LinkedIn, or public-profile audit or update;
- an application review reveals a correction that should apply beyond one application;
- a public credential or evidence link is added, removed, or questioned; or
- a source-system discrepancy could make public information inaccurate.

Do not run it for ordinary role-specific keyword tailoring that does not change Troy's underlying professional record.

## Operating Modes

1. **Audit:** compare sources and report discrepancies without writing.
2. **Prepare:** create proposed copy, validation output, branches, and draft pull requests.
3. **Apply:** make only the external changes the user explicitly authorized, then read back each changed surface.

Authorization to update one surface does not authorize publishing or changing another. Never merge a pull request, publish a site change, expose evidence, or edit LinkedIn without explicit approval for that action.

## Workflow

### 1. Establish Current State

Read the current contract and authoritative GitHub files. Then inspect the current production repository, deployed site, relevant Notion pages, public LinkedIn profile, and Drive evidence records needed for the affected claims.

Record each claim with:

- proposed public wording;
- source and source date;
- verification status;
- permitted public surfaces;
- sensitivity or publication restriction; and
- any conflicting value.

### 2. Resolve Conflicts Conservatively

Apply this precedence:

1. Primary official record or source document
2. Current privacy and publication standards
3. Approved claim in `PUBLIC_PROFILE_CONTRACT.json`
4. Current GitHub career or training constants
5. Notion and Drive working records
6. Existing website or LinkedIn wording

When strong sources conflict, block the disputed value. Use a safe date range or qualitative description only when the contract explicitly permits it. Do not silently choose the newest, largest, or most favorable number.

### 3. Apply the Public-Release Gate

Never publish:

- POST, badge, personnel, responder, license, or credential identifiers;
- license effective, renewal, or expiration details;
- SSNs, birth data, protected case numbers, victim information, private addresses, signatures, or QR codes;
- raw case, court, personnel, certificate, commendation, or investigative files;
- a Drive link that has not been verified as public-safe and approved for release; or
- a claim marked `blocked`, `pending`, `private_only`, or `not_reviewed`.

Use sanitized evidence summaries and approved excerpts. Publication approval attaches to the exact public artifact, not to the existence of a private source.

### 4. Prepare Surface-Specific Changes

- **Career repository:** update the contract or governing standard first when the approved fact changes.
- **Production portfolio:** use a branch and draft pull request. Preserve site health checks and add regression coverage for the corrected privacy or fact rule.
- **LinkedIn:** prepare the exact headline, About, experience, and credential edits. Apply them only when explicitly authorized and the connector supports verified writes.
- **Notion:** update the existing portfolio status or decision page; do not create a duplicate record when the current page can be corrected.
- **Drive:** keep primary evidence private. Add a sanitized public copy only after explicit approval and a privacy review.

Material public-profile changes discovered during `build-troy-application` should invoke this skill as a separate alignment step. Routine application tailoring should be recorded as not applicable.

### 5. Validate

From a checked-out career repository, run:

```bash
python skills/maintain-troy-public-profile/scripts/validate_public_profile.py \
  --contract PUBLIC_PROFILE_CONTRACT.json \
  --scan <public-site-file-or-directory>
```

The script checks the contract, canonical repository routing, prohibited public identifiers, blocked metrics, unresolved duration claims, and unreviewed Drive links. Network permissions and live visibility still require connector or browser verification.

Also run the production repository's existing health tests. A passing deployment check does not replace cross-system comparison.

### 6. Verify Writes

After every authorized write, read the changed record or file back from its destination. Confirm the exact repository, branch, page, or profile section. If any write cannot be verified, report it as incomplete.

## Completion Report

Report:

- surfaces audited;
- surfaces changed and read-back status;
- draft PR links and validation results;
- claims approved, blocked, or still disputed;
- privacy findings;
- evidence that remains private;
- any user-only LinkedIn or account-setting action; and
- whether the unused duplicate repository is verified private.

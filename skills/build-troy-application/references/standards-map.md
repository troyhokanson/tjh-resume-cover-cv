# Standards map and precedence

Use this order when instructions appear to conflict:

1. `HEADER_STANDARD.md` - locked header placement, current colors, contact row, margins, and ATS rules.
2. `PRIVACY_STANDARD.md` - public/private boundary and redaction requirements.
3. `PUBLIC_PROFILE_CONTRACT.json` - approved public claims, blocked conflicts, publication gates, and canonical public surfaces.
4. `CONTACT_STANDARD.md` - contact values, display text, and hyperlink behavior.
5. `ROLE_FAMILIES.md` - canonical private-sector career taxonomy.
6. `ROLE_ADAPTATION_STANDARD.md` - posting-led identity, evidence selection, structure, and lane vocabulary.
7. `RESUME_HEADLINE_SCANABILITY_STANDARD.md` - headline decision, summary density, length, recency, metrics, and ATS structure.
8. `VOICE_STANDARD.md` - tone, phrasing, and anti-AI review.
9. `docx_header.py` and `pdf_header.py` - executable implementations of the locked standards.
10. `DOCX_NODE_STANDARD.md` - implementation guidance for Node builders; it must conform to the files above.

## Document routing

| Deliverable | Required implementation |
|---|---|
| ATS resume DOCX | `new_document()` + `build_navy_header()` + shared body helpers |
| Cover letter DOCX | Same locked header plus shared paragraph formatting |
| Candidate or contractor one-pager | `profile_one_pager.py` plus shared header/body helpers |
| Human-facing PDF | Export the validated DOCX when practical; otherwise use `pdf_header.py` |
| Public portfolio | `troyhokanson/troyhokanson.github.io`, governed by `PUBLIC_PROFILE_CONTRACT.json` |
| Portfolio evidence | Link only to reviewed public-safe evidence; keep originals in Drive/Notion |

## Layout precedence and delivery

Use `standards/document_design_standard.json` for typography and margins and `workflow_contract.json` for minimum spacing. Use the greater spacing when values differ. The older 9-point compression and spacing-reduction guidance is withdrawn. Edit content before reducing approved font sizes or minimum spacing.

Follow `standards/formatting_delivery_contract.md`. Inspect the bottom of every page, not only one-pagers. The user's standing navy/gold/Garamond requirement overrides plain-ATS autonomy. A missing validator is an Exception, never permission to substitute an unbranded document.

For DOCX and DOCX-exported PDFs, the full banner repeats as `HEADER_STANDARD.md` specifies. Slim continuation bars belong to the direct-PDF route only. Do not mix routes after rendering.

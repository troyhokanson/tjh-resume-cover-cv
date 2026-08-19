# Standards map and precedence

Use this order when instructions appear to conflict:

1. `HEADER_STANDARD.md` - locked header placement, current colors, contact row, margins, and ATS rules.
2. `PRIVACY_STANDARD.md` - public/private boundary and redaction requirements.
3. `CONTACT_STANDARD.md` - contact values, display text, and hyperlink behavior.
4. `ROLE_FAMILIES.md` - canonical private-sector career taxonomy.
5. `VOICE_STANDARD.md` - tone, phrasing, and anti-AI review.
6. `docx_header.py` and `pdf_header.py` - executable implementations of the locked standards.
7. `DOCX_NODE_STANDARD.md` - implementation guidance for Node builders; it must conform to the files above.

## Document routing

| Deliverable | Required implementation |
|---|---|
| ATS resume DOCX | `new_document()` + `build_navy_header()` + shared body helpers |
| Cover letter DOCX | Same locked header plus shared paragraph formatting |
| Candidate or contractor one-pager | `profile_one_pager.py` plus shared header/body helpers |
| Human-facing PDF | Export the validated DOCX when practical; otherwise use `pdf_header.py` |
| Portfolio evidence | Link only to reviewed public-safe evidence; keep originals in Drive/Notion |

## One-page spacing sequence

1. Start with the locked 1.55-inch body top margin and 0.55-inch bottom margin.
2. Center the document title and focus line below the header.
3. Use 8 points before and 2 points after section headings.
4. Use 6 points before role titles, 0 after titles, and 2 after employer/date lines.
5. Use 2 points after bullets and approximately 1.15 line spacing.
6. If whitespace remains, add measured space to the opening block and between sections before enlarging body type.
7. If content overflows, tighten paragraph spacing before reducing body text below 9 points.

Always inspect the bottom quarter of the rendered page. A one-pager should look intentionally balanced, not compressed at the top or stranded above a large empty area.


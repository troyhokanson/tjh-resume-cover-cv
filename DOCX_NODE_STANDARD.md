# Troy Hokanson - DOCX Node.js Formatting Standard

**Companion implementation guide. `HEADER_STANDARD.md`, `CONTACT_STANDARD.md`, and `docx_header.py` control if any value conflicts.**

Node builders must produce the same rendered result as the locked Python implementation. Do not maintain a separate brand palette, header identity, or spacing system.

## Current tokens

| Token | Hex | Use |
|---|---|---|
| Navy | `0D1B2A` | Full-bleed header background |
| Gold | `C9A84C` | Rule, role accents, restrained dividers |
| Steel | `2D6A9F` | Body section headings and links |
| White | `FFFFFF` | Header name |
| Body text | `141414` | Main text |

- Name and contact row: Garamond-family.
- Body: Calibri-family.
- Body section headings and role titles: Garamond-family.
- Name: 26 pt, bold, centered.
- Do not add a subtitle or role title inside the header.

## Page geometry

```javascript
const PAGE_W = 12240;
const PAGE_H = 15840;
const BODY_MARGIN = 864; // 0.6 inch
const BODY_TOP = 2232;   // 1.55 inches
const BODY_BOTTOM = 792; // 0.55 inch
```

Use U.S. Letter explicitly. The full-bleed navy table belongs in the Word header part and spans the physical page width. Body text begins below it.

## Locked header

The header contains only:

1. `Troy Hokanson` in white Garamond-family bold, 26 pt.
2. One centered gold rule, approximately 55 percent page width.
3. The environment-backed contact row in gold Garamond-family type.

Use `TroyHokanson.com` as the visible portfolio text and `https://troyhokanson.com` as its destination. Do not hardcode phone, email, location, or LinkedIn values in a public builder.

## Shared spacing

General résumé and cover-letter builders should follow `docx_header.py`:

- Section heading: 8 pt before, 2 pt after, 1.1 line spacing.
- Role title: 6 pt before, 0 pt after.
- Employer/date line: 0 pt before, 2 pt after.
- Bullet: 0 pt before, 2 pt after, approximately 1.15 line spacing.

Candidate profiles and one-pagers must also read:

```text
skills/build-troy-application/workflow_contract.json
```

That contract sets larger minimum spacing for intentionally balanced one-page layouts. Edit content before compressing its minimums.

## ATS and structure

- Keep the primary ATS document body free of tables, columns, text boxes, and floating shapes.
- Use real Word numbering for bullets.
- Set `keepNext` or `keep_with_next` on section headings, role titles, and employer lines.
- Use fixed DXA widths for any approved presentation-only table.
- Keep Education separate from Training and Certifications in a résumé.
- Use no footer by default.

## Validation

After generation, confirm:

- full-bleed navy header with no white edge or internal seam;
- centered name, rule, and contact row;
- required header-to-body whitespace;
- no clipping, overflow, blank pages, or orphan headings;
- balanced vertical rhythm and bottom whitespace;
- functional links and matching DOCX/PDF rendering.

Rendered output controls. Passing code or XML checks alone is not sufficient.

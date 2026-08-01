# Troy Hokanson — DOCX Node.js Formatting Standard

**Locked May 2026. Single source of truth for Word documents built with the Node.js docx npm library.**

This companion to HEADER_STANDARD.md covers the Node.js / docx@8+ implementation specifically.
The Python (python-docx) standard remains in HEADER_STANDARD.md.

---

## Colors

| Token  | Hex     | Use                          |
|--------|---------|------------------------------|
| NAVY   | 1C2B4A  | Header background, section headers, subheads |
| GOLD   | C09A20  | Gold rule, bullet character, job titles, table borders |
| WHITE  | FFFFFF  | Header name and contact text |
| BLACK  | 000000  | Body text, employer names    |

Font: **Garamond** throughout all elements — no exceptions.

---

## Font Sizes (half-points)

```javascript
const SZ_NAME     = 84;   // 42pt  — header name
const SZ_CONTACT  = 28;   // 14pt  — contact line in header
const SZ_SUBTITLE = 20;   // 10pt  — cover letter subtitle only
const SZ_SECHEAD  = 36;   // 18pt  — section headers
const SZ_JOBTITLE = 30;   // 15pt  — job titles (gold italic bold)
const SZ_BODY     = 24;   // 12pt  — body text and bullets
const SZ_SKILLS   = 18;   //  9pt  — competency/skills table cells
const SZ_RUNHEAD  = 44;   // 22pt  — running header pages 2+
const SZ_SUBHEAD  = 28;   // 14pt  — CV sub-section labels
```

> **SZ_BODY must be 24 (12pt).** Values of 38 (19pt) or higher produce oversized body text.

---

## Page Geometry (DXA / twips)

```javascript
const PAGE_W    = 12240;
const LM        = 1440;               // left & right margin (1 inch)
const CONTENT_W = PAGE_W - 2 * LM;   // 9360 DXA
```

---

## Section Margins

```javascript
const SEC1_MARGIN = { top: 0,    right: LM, bottom: 1008, left: LM }; // page 1
const SEC2_MARGIN = { top: 1200, right: LM, bottom: 1008, left: LM }; // pages 2+
```

Page 1 `top: 0` is required — the navy header table must sit flush at the top of the page.

---

## Vertical Spacing and Breathing Room

Vertical rhythm is a hard readability requirement. A document may be compact, but it may not look compressed or crowded.

Use these minimum values in twentieths of a point (`twips`; 20 twips = 1 point):

```javascript
const SPACE_HEADER_TO_FIRST_HEADING = 360; // 18pt minimum
const SPACE_SECTION_BEFORE          = 280; // 14pt minimum before each major section heading
const SPACE_SECTION_AFTER           = 120; //  6pt minimum after each major section heading
const SPACE_JOB_BEFORE              = 160; //  8pt minimum before a new job, degree, or major entry
const SPACE_JOBTITLE_AFTER          = 40;  //  2pt minimum after job title
const SPACE_EMPLOYER_AFTER          = 80;  //  4pt minimum after employer/date line
const SPACE_BULLET_AFTER            = 40;  //  2pt preferred after bullets; may be 0 only within a tightly related bullet group
const SPACE_PARAGRAPH_AFTER         = 120; //  6pt minimum between cover-letter paragraphs
```

### Required hierarchy

1. **Header to first heading:** At least 18pt of visible white space must separate the bottom of the page-one navy header from the first body heading or salutation.
2. **Between major sections:** At least 14pt before the next section heading and 6pt after it.
3. **Between entries within a section:** At least 8pt before each new job, degree, certification group, or other major entry.
4. **Heading attachment:** Section headings must remain visually attached to the content they introduce. Do not create more space after a heading than before it.
5. **Cover-letter paragraphs:** At least 6pt after each paragraph. Do not simulate spacing with blank paragraph characters.
6. **Bullet groups:** Bullets within the same thought group may use 0–2pt after spacing. A new role or subsection must receive the full entry spacing.
7. **Page breaks:** Do not leave a section heading or job title at the bottom of a page without at least two lines of following content.

### Compression rule

When content does not fit within the intended page count, adjust in this order:

1. Remove repetition or weak bullets.
2. Tighten wording.
3. Reduce the number of supporting credentials or competencies.
4. Rebalance section placement or page breaks.
5. Reduce optional spacing only above the stated minimums.

Never solve overflow by reducing body text below 12pt, narrowing margins below the approved standard, or reducing the minimum header/section spacing. White space is part of the design, not unused capacity.

### Example implementation

```javascript
function firstSectionHead(text) {
  return new Paragraph({
    keepNext: true,
    spacing: {
      before: SPACE_HEADER_TO_FIRST_HEADING,
      after: SPACE_SECTION_AFTER,
    },
    // ...
  });
}

function secHead(text) {
  return new Paragraph({
    keepNext: true,
    spacing: {
      before: SPACE_SECTION_BEFORE,
      after: SPACE_SECTION_AFTER,
    },
    // ...
  });
}

function jobTitle(text) {
  return new Paragraph({
    keepNext: true,
    spacing: {
      before: SPACE_JOB_BEFORE,
      after: SPACE_JOBTITLE_AFTER,
    },
    // ...
  });
}
```

The first section must use the dedicated first-heading spacing rather than inheriting the ordinary section spacing.

---

## Full-Bleed Navy Header (Page 1)

Use a negative left indent equal to LM to extend the table beyond the page margin:

```javascript
return new Table({
  width:  { size: PAGE_W, type: WidthType.DXA },
  indent: { size: -LM,   type: WidthType.DXA },  // negative = full-bleed
  layout: TableLayoutType.FIXED,
  borders: NB,
  rows,
});
```

Running header (pages 2+) uses the same negative indent, placed in the Word header zone via `new Header({ children: [table] })`.

---

## Skills / Competency Table

**Full content width, no left indent.** A non-zero indent creates a blank gap on the left side.

```javascript
return new Table({
  width:  { size: CONTENT_W, type: WidthType.DXA },
  indent: { size: 0,         type: WidthType.DXA },  // must be 0
  layout: TableLayoutType.FIXED,
  borders: NB,
  rows,
});
```

---

## Orphan Prevention — keepNext

The following paragraph types MUST include `keepNext: true` to prevent section headers and job titles from appearing alone at the bottom of a page:

```javascript
function secHead(text) {
  return new Paragraph({
    keepNext: true,
    // ...
  });
}

function jobTitle(text) {
  return new Paragraph({
    keepNext: true,
    // ...
  });
}

function empLine(company, dates) {
  return new Paragraph({
    keepNext: true,
    // ...
  });
}
```

`keepNext: true` on `empLine` is also required — without it the employer line can orphan even when `jobTitle` is chained correctly.

---

## Gold Bullet Character

Defined via numbering config, not a text character:

```javascript
const numbering = {
  config: [{
    reference: 'bullets',
    levels: [{
      level: 0,
      format: LevelFormat.BULLET,
      text: '•',
      alignment: AlignmentType.LEFT,
      style: {
        paragraph: { indent: { left: 360, hanging: 180 } },
        run: { size: SZ_BODY, font: 'Garamond', color: 'C09A20' },
      },
    }],
  }],
};
```

---

## Education Lines

The `eduLine()` helper accepts an optional fifth honors parameter:

```javascript
function eduLine(degree, school, year, gpa, honors) {
  const schoolLine = school + '   |   ' + year + '   |   GPA ' + gpa
    + (honors ? '   |   ' + honors : '');
  return [
    new Paragraph({ children: [new TextRun({ text: degree, bold: true, ... })], keepNext: true }),
    new Paragraph({ children: [new TextRun({ text: schoolLine, ... })] }),
  ];
}
```

Always pass city/state in the school string: `St. Cloud State University, St. Cloud, MN`.

---

## Hard Rules

1. `SZ_BODY = 24` (12pt). Never 38 or higher.
2. Skills tables: `indent: { size: 0 }`. Never a positive indent.
3. `secHead`, `jobTitle`, and `empLine` must all include `keepNext: true`.
4. Page 1 section margin: `top: 0`. Required for full-bleed header.
5. Minimum header and section spacing must meet the Vertical Spacing and Breathing Room standard.
6. Content must be edited before any minimum spacing value is reduced.
7. Honors (Magna Cum Laude, etc.) go in the `eduLine` fifth parameter — never omitted.
8. City/state always included in school name string.
9. All dates written in full: `March 2010 – May 2011`, not `2010-2011`.

---

## Reference Implementation

`build_roblox.js` (Roblox CHIIOPS application, May 2026) is the canonical corrected Node.js build script demonstrating all of these standards.

---

## Repo

https://github.com/troyhokanson/tjh-resume-cover-cv

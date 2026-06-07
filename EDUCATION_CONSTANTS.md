# Education Constants — Locked, Verbatim, Non-Negotiable

These three entries must appear in every resume, CV, and any document that lists education.
**Master of Arts is always listed first.** Never reorder. Never paraphrase. Never abbreviate.

---

## Master of Arts (always first)

```
Master of Arts, Police Leadership, Administration and Education
University of St. Thomas, St. Paul, MN
GPA: 3.94
2005
```

## Bachelor of Arts (always second)

```
Bachelor of Arts, Criminal Justice, Magna Cum Laude
St. Cloud State University, St. Cloud, MN
GPA: 3.51
1998
```

## Associate of Arts (always third)

```
Associate of Arts, Criminal Justice, Magna Cum Laude
St. Cloud State University, St. Cloud, MN
1996
```

---

## Usage Rules

- All three degrees must appear on every resume and CV. None are optional.
- The Master of Arts block always precedes the Bachelor of Arts block.
- The Associate of Arts block always follows the Bachelor of Arts block.
- "Magna Cum Laude" appears on both the BA and AA lines. No equivalent honor exists for the MA and none should be fabricated.
- Education uses year-only format (not month-year). Employment dates use month-year. Do not mix.
- Do not add "Expected" or "Completed" qualifiers. These are conferred degrees.
- Do not list coursework, thesis titles, or concentrations unless explicitly requested by the user for a specific application.

---

## Enforcement

`anti_ai_scan.py` should verify that the MA and BA degree strings appear in any resume or CV output.
If either is missing, the scan should emit a `WARN: missing education constant` message.

---

## Change Log

- 2026-06-07: Added Associate of Arts entry (1996). Standardized all dates to year-only.
  Removed date-range format (was "August 2003 - December 2005" for MA -- corrected to 2005).
  Removed BA date range (was "August 1994 - February 1998" -- corrected to 1998).

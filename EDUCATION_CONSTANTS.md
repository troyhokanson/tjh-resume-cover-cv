# Education Constants — Locked, Verbatim, Non-Negotiable

These two entries must appear in every resume, CV, and any document that lists education.
**Master of Arts is always listed first.** Never reorder. Never paraphrase. Never abbreviate.
Never omit the GPA, the institution city/state, or the date range.

---

## Master of Arts (always first)

```
Master of Arts, Police Leadership, Administration and Education
University of St. Thomas, St. Paul, MN
GPA: 3.94
August 2003 – December 2005
```

## Bachelor of Arts (always second)

```
Bachelor of Arts, Criminal Justice Studies
St. Cloud State University, St. Cloud, MN
Magna Cum Laude | GPA: 3.51
August 1994 – February 1998
```

---

## Usage Rules

- Both degrees must appear on every resume and CV. Neither is optional.
- The Master of Arts block always precedes the Bachelor of Arts block.
- "Magna Cum Laude" appears on the BA line. No equivalent honor exists for the MA and none should be fabricated.
- Date ranges use an en dash in print (–) but a plain hyphen is acceptable in plain-text or Markdown contexts.
- Do not add "Expected" or "Completed" qualifiers. These are conferred degrees.
- Do not list coursework, thesis titles, or concentrations unless explicitly requested by the user for a specific application.
- These constants are imported by `build_resume.py`, `build_cv.py`, and any ad-hoc build scripts. Never hardcode them inline — always import from this source of truth.

---

## Enforcement

`anti_ai_scan.py` should verify that both degree strings appear in any resume or CV output.
If either is missing, the scan should emit a `WARN: missing education constant` message.
Adding a hard-block (`FailedScan`) for missing education is at the developer's discretion based on doc type.

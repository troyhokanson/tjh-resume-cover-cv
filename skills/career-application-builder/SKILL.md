---
name: career-application-builder
description: Compatibility alias for Troy Hokanson's unified application workflow. Triggers on career-application-builder and delegates every request to `skills/build-troy-application/SKILL.md`. It must not maintain separate drafting, validation, filing, or completion logic.
---

# Career Application Builder Alias

This skill exists only to preserve the earlier command name.

For every Troy Hokanson application request, load and follow:

```text
skills/build-troy-application/SKILL.md
```

That skill is the controlling workflow for:

- exact job verification
- role-fit and gap analysis
- evidence retrieval
- resume and cover-letter drafting
- DOCX and PDF generation
- ATS, anti-AI, privacy, and factual validation
- visual PDF inspection
- Google Drive filing
- GitHub application packaging
- Notion application tracking
- completion reporting

Do not duplicate or override its rules. If this alias and the controlling skill appear to conflict, `build-troy-application` controls.

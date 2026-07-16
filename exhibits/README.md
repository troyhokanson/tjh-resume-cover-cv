# Troy Hokanson Application Exhibits

This folder mirrors Melissa's GitHub exhibit system.

Each approved application packet should receive its own folder using:

`exhibits/<company>_<requisition-or-role-slug>/`

Every exhibit folder should contain:

- `resume.md` for searchable, version-controlled resume content.
- `cover_letter.md` for searchable, version-controlled cover-letter content.
- `exhibit_manifest.json` for application metadata, document names, status, and source-of-truth rules.
- `visual_spec.json` for machine-readable typography, color, spacing, and header requirements.
- `README.md` explaining why the packet was approved as an example.
- Native DOCX and PDF files when they can be uploaded through the available GitHub workflow.

Markdown and JSON support search, review, automation, and future tailoring. They do not replace the native DOCX and PDF files as the visual source of truth.

Use `exhibits/_template/` to begin a new exhibit.

# Formatting delivery contract

Effective September 20, 2026. Applies to new documents and corrections.

- Full-bleed navy, restrained gold accents and Garamond are Troy's standing default. Do not ask him to restate it. Only an explicit request for a named plain deliverable permits an exception.
- Use the current locked header helper unchanged. Set up Garamond before rendering; silently substituting another font is a failure.
- Run formatting preflight before building. Required validator files must exist, import and run. Missing tools or failures mean Exception, not approval.
- Run `body_typography_pagination_validator.py --docx FILE --pdf FILE --doc-type resume|cover|cv`. It checks rendered font use, page boundaries, blank space, page balance, and DOCX heading keep rules. It is integrated into `validate_application_packet.py`.
- A resume page with more than 2 inches beneath its last body line fails. Two resume pages whose bottom blank areas differ by more than 1 inch fail. These are review thresholds, not permission to pad content or force identical pages. The final page also requires visual review.
- Do not insert a manual page break merely to separate relevant and additional experience. A deliberate break must keep a meaningful block together and pass the page-balance gate. Prefer editing irrelevant or repetitive text over shrinking type or crowding spacing.
- Inspect every rendered page for full bleed, centering, rule placement, spacing, clipping, orphan headings, and lower-page balance. Save the inspection record and bind it to PDF/page-image hashes. Automated checks do not replace visual review.
- Run strict header validation on every branded page at unchanged thresholds. DOCX-exported PDFs use the full repeated DOCX banner; the direct-PDF builder uses its own slim continuation.
- Draft is a workflow status, not an exemption from formatting. A failed correction must be reported as incomplete; never describe it as properly formatted or ready merely because files exist or uploaded successfully.
- Revalidate downstream outputs after every edit. Save final source, DOCX, PDF and reports together. Verify Drive uploads. Do not delete predecessors until accepted replacements are saved, unless Troy explicitly directs otherwise.

## Scope of automated checks

The body validator checks selectable-text PDFs and DOCX keep properties. It does not prove factual accuracy, ATS compatibility, signature balance, or the visual quality of image-only pages. Empty or image-only pages fail for manual resolution. Cover-letter optical balance and special document types still require page-by-page inspection.

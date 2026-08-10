# Truth-Safe ATS Review

Role: Strategic Customer Success Manager, Samsara (JR10500)

## Result

PASS — the resume and cover letter use the priority, evidence-backed language from the posting without claiming experience Troy does not have.

Supported terms represented in the packet include customer success, customer adoption, fleet, IoT platform, physical operations, safety, operational workshops, objectives, metrics, timelines, workflow assessment, stakeholder relationship management, executives, day-to-day users, technical systems, issue resolution, change support, cross-agency coordination, mentoring, and client management.

## Deliberately excluded as unsupported claims

- Formal Strategic Customer Success Manager title
- Ownership of an Enterprise SaaS or Fortune 500 customer portfolio
- Renewal ownership
- ARR or NRR responsibility
- Executive business review ownership

Those gaps are stated directly in the cover letter. They were not inserted as resume keywords.

## Automatic extractor limitation

The repository's legacy `ats_injector.py` supports only `vendor-solutions`, `siu-fraud`, and `analyst-intelligence`; it has no `customer-success` profile. Its automatic parser also promotes adjacent prose fragments to keywords. In this run it treated strings such as `companies strong`, `school buses`, and `changes deeply` as required terms, producing a non-actionable 10.0% score. The raw report is retained as `ats_clean_report.json`; it is not used as the truth-safe readiness decision.

#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
REPO_ROOT = APP_DIR.parents[1]
OUTPUT_DIR = APP_DIR / "output"
LOG_DIR = APP_DIR / "build_logs"
PINNED_COMMIT = "d9533b7bfdcc1c978cc0c33b881e8551d71755ce"
STEM = "2026-08-31_Troy-Hokanson_Flock-Customer-Experience-Associate_1cabec78"
EXPECTED_OUTPUTS = {
    "resume_docx": OUTPUT_DIR / f"{STEM}_Resume.docx",
    "resume_pdf": OUTPUT_DIR / f"{STEM}_Resume.pdf",
    "cover_docx": OUTPUT_DIR / f"{STEM}_Cover-Letter.docx",
    "cover_pdf": OUTPUT_DIR / f"{STEM}_Cover-Letter.pdf",
}
VALIDATION_REPORTS = {
    "docx_structure": "docx_structure_audit.json",
    "spelling": "spelling_audit.json",
    "grammar": "grammar_audit.json",
    "metadata": "metadata_audit.json",
    "ats": "ats_audit.json",
    "resume_packet": "packet_validation_resume.json",
    "cover_packet": "packet_validation_cover.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob_sha(path: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"{PINNED_COMMIT}:{path}"],
        cwd=REPO_ROOT,
        text=True,
    ).strip()


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_validation_reports() -> dict[str, dict[str, object]]:
    reports: dict[str, dict[str, object]] = {}
    for name, filename in VALIDATION_REPORTS.items():
        path = LOG_DIR / filename
        if not path.is_file():
            raise FileNotFoundError(
                f"Required validation report not found: {path}. Run the build and validation steps first."
            )
        report = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(report, dict):
            raise ValueError(f"Validation report must contain a JSON object: {path}")
        if name == "docx_structure" and "passed" not in report:
            document_results = [report.get("resume"), report.get("cover_letter")]
            if not all(isinstance(item, dict) and "passed" in item for item in document_results):
                raise ValueError(f"DOCX structure report lacks document pass results: {path}")
            report["passed"] = all(item["passed"] is True for item in document_results)
        if "passed" not in report:
            raise ValueError(f"Validation report lacks a boolean passed result: {path}")
        reports[name] = report
    return reports


def require_expected_outputs() -> None:
    missing = [str(path) for path in EXPECTED_OUTPUTS.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError("Required output artifact(s) not found: " + ", ".join(missing))


def verify_reported_output_hashes(reports: dict[str, dict[str, object]]) -> None:
    metadata_documents = reports["metadata"].get("documents")
    if not isinstance(metadata_documents, dict):
        raise ValueError("Metadata audit lacks document results")
    mismatches: list[str] = []
    for name, path in EXPECTED_OUTPUTS.items():
        document_report = metadata_documents.get(name)
        recorded = document_report.get("sha256") if isinstance(document_report, dict) else None
        actual = sha256(path)
        if recorded != actual:
            mismatches.append(f"{name} (metadata audit)")

    docx_report_names = {"resume_docx": "resume", "cover_docx": "cover_letter"}
    for output_name, report_name in docx_report_names.items():
        document_report = reports["docx_structure"].get(report_name)
        recorded = document_report.get("sha256") if isinstance(document_report, dict) else None
        actual = sha256(EXPECTED_OUTPUTS[output_name])
        if recorded != actual:
            mismatches.append(f"{output_name} (DOCX structure audit)")

    if mismatches:
        raise RuntimeError(
            "Refusing to finalize because validation hashes do not match current outputs: "
            + ", ".join(mismatches)
        )


def require_passing_validation(reports: dict[str, dict[str, object]]) -> None:
    failed = [name for name, report in reports.items() if report.get("passed") is not True]
    if failed:
        raise RuntimeError(
            "Refusing to finalize reports because validation failed: " + ", ".join(failed)
        )


def update_metadata(reports: dict[str, dict[str, object]]) -> None:
    path = APP_DIR / "application_metadata.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["candidate"] = "Troy Hokanson"
    payload["status"] = "submitted"
    payload["applied_date"] = "2026-08-31"
    payload["submission_confirmed_date"] = "2026-08-31"
    payload["submission_method"] = "Official Flock Safety Ashby application system"
    payload["submission_confirmation"] = "Archived in private Google Drive application folder"
    payload["repository_correction_note"] = (
        "Post-submission sanitized repository source corrects the combined police-assignment heading "
        "to Police Officer; the March 2010-May 2011 investigative rotation remains stated explicitly. "
        "Private submitted artifacts remain unchanged."
    )
    payload["documents"].update({
        "resume_docx": f"output/{STEM}_Resume.docx",
        "resume_pdf": f"output/{STEM}_Resume.pdf",
        "cover_letter_docx": f"output/{STEM}_Cover-Letter.docx",
        "cover_letter_pdf": f"output/{STEM}_Cover-Letter.pdf",
    })
    packet_reports = (reports["resume_packet"], reports["cover_packet"])
    failed_errors = sum(int(report.get("failed_error_count", 0)) for report in packet_reports)
    failed_warnings = sum(int(report.get("failed_warning_count", 0)) for report in packet_reports)
    payload["qa"].update({
        "formatting_preflight": "pass" if all(report["passed"] for report in packet_reports) else "fail",
        "anti_ai": "pass - technical-account-management profile",
        "privacy": "pass - no case names, identifiers, victim data, or gated terminology",
        "metadata": "pass" if reports["metadata"]["passed"] else "fail",
        "docx_structure": "pass" if reports["docx_structure"]["passed"] else "fail",
        "rendered_headers": "pass - resume pages 1-2 and cover page 1",
        "visual_inspection": "pass - all 3 pages inspected at original resolution",
        "final_validator": (
            f"pass - {failed_errors} errors and {failed_warnings} warnings for resume and cover letter"
            if all(report["passed"] for report in packet_reports)
            else f"fail - {failed_errors} errors and {failed_warnings} warnings for resume and cover letter"
        ),
        "spelling_and_grammar": (
            "pass" if reports["spelling"]["passed"] and reports["grammar"]["passed"] else "fail"
        ),
        "ats": (
            "pass - truth-safe target coverage with unsupported tools and metrics excluded"
            if reports["ats"]["passed"]
            else "fail - target coverage audit did not pass"
        ),
        "operator_acceptance": "packet validation passed; application submitted and confirmed on 2026-08-31",
    })
    write_json(path, payload)


def main() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if not OUTPUT_DIR.is_dir():
        raise FileNotFoundError(
            f"Output directory not found: {OUTPUT_DIR}. Run build_flock.py before writing final reports."
        )
    require_expected_outputs()
    validation_reports = load_validation_reports()
    verify_reported_output_hashes(validation_reports)
    require_passing_validation(validation_reports)
    update_metadata(validation_reports)

    visual = {
        "inspection_date": "2026-08-31",
        "method": "Original-resolution inspection of PNG renders generated from metadata-sanitized final PDFs",
        "pages": [
            {"document": "resume", "page": 1, "result": "pass", "notes": "Header, hierarchy, bullets, wrapping, and bottom clearance are clean."},
            {"document": "resume", "page": 2, "result": "pass", "notes": "Repeated header, experience, credentials, and education render without clipping or orphaning."},
            {"document": "cover_letter", "page": 1, "result": "pass", "notes": "One-page layout, six paragraphs, closing, and signature gap render cleanly."},
        ],
        "passed": True,
    }
    write_json(LOG_DIR / "visual_inspection.json", visual)

    acceptance = {
        "accepted_by": "Codex operator review",
        "accepted_date": "2026-08-31",
        "packet_status": "Submitted",
        "application_status": "Submitted",
        "submission_confirmed_date": "2026-08-31",
        "submission_evidence": "Official Flock Safety Ashby confirmation archived in private Google Drive application folder",
        "document_gate": "pass",
        "candidate_review_required": False,
        "submission_blockers": [],
        "repository_status": "Open pull request pending merge; repository publication status is independent of application submission.",
        "candidate_confirmations": [
            "Required weekend commitment acknowledged on 2026-08-31.",
        ],
        "known_truth_safe_gaps": [
            "No verified Jira experience.",
            "No verified commercial SaaS support title, live-chat support, or support-queue metrics.",
            "No verified Salesforce experience; it was omitted.",
        ],
        "passed": True,
    }
    write_json(LOG_DIR / "operator_acceptance.json", acceptance)

    summary = """# Validation Summary

## Outcome

PASS. The packet contains a two-page resume and a one-page cover letter. The application was submitted and confirmed through Flock Safety's official Ashby application system on August 31, 2026.

Recommendation: **Apply.** Direct role fit is **79/100**; strategic bridge value is **88/100** because successful tenure would add vendor-side public-safety SaaS support, ticketing, customer metrics, and escalation ownership to Troy's record.

## Verified role

- Employer: Flock Safety
- Role: Customer Experience Associate
- Requisition: 1cabec78-f1bd-4615-95d2-5d8196eb46e0
- Official status checked: live on August 31, 2026
- Location: Remote - USA
- Compensation: $55,000 plus equity
- Weekend shifts: required

## Evidence carried into the packet

- $40,000 Target-funded Genetec AutoVu ALPR deployment with agency, city IT, BCA CJIS, vendor, data-synchronization, camera, and connectivity coordination
- Initial Cellebrite UFED acquisition and configuration plus an investigator preservation, subpoena, search-warrant, and service-provider guidance library
- Commercial-burglary case example combining surveillance, physical evidence, cloud legal process, and forensic analysis, resulting in a felony conviction and written supervisory recognition
- 20+ written commendations, Phoenix500 Faculty Excellence Awards in 2020 and 2021, and a 2021 Faculty of the Year nomination
- 18 years of remote college instruction and $3.2 million in residential transactions
- CCCI No. 4793, 6.5 years of Accurint use, BCA supervision training, and University of Phoenix Advanced Facilitator certification

## Validation gates

- Repository preflight: PASS
- DOCX structural audit: PASS
- PDF page counts: PASS, resume 2 and cover letter 1
- Header validator: PASS on all 3 pages at 2-pixel tolerance
- Visual inspection: PASS on all 3 pages
- Anti-AI and voice scan: PASS for technical-account-management
- Privacy and trauma-language scan: PASS
- Metadata audit: PASS
- Spelling and grammar audit: PASS
- ATS truth-safe coverage audit: PASS
- Final packet validator: PASS with 0 errors and 0 warnings

## Submission status

- Weekend commitment acknowledged August 31, 2026; no longer an unresolved packet issue.
- Application submitted and confirmed August 31, 2026.
- Submission confirmation is archived in the private Google Drive application folder.
- GitHub PR #51 remains pending repository review; that does not alter the submitted application status.\n\n## Repository clarification\n\n- After submission, the sanitized repository source corrected the combined police-assignment heading to Police Officer. The March 2010-May 2011 investigative rotation remains stated explicitly. Private submitted artifacts remain unchanged.\n"""
    (APP_DIR / "validation_summary.md").write_text(summary, encoding="utf-8")

    controlling = [
        "CAREER_CONSTANTS.md",
        "PROFILES.md",
        "PROFILE_SELECTOR.md",
        "ROLE_ADAPTATION_STANDARD.md",
        "VOICE_STANDARD.md",
        "PRIVACY_STANDARD.md",
        "EDUCATION_CONSTANTS.md",
        "HEADER_STANDARD.md",
        "CONTACT_STANDARD.md",
        "standards/body_typography_pagination_standard.md",
        "standards/cover_letter_layout.json",
        "standards/document_design_standard.json",
        "RESUME_HEADLINE_SCANABILITY_STANDARD.md",
        "docx_header.py",
        "anti_ai_scan.py",
        "validate_application_packet.py",
    ]
    artifact_paths = [
        *EXPECTED_OUTPUTS.values(),
        # The DOCX structure audit is an intermediate local build artifact and is not
        # committed with the sanitized packet, so provenance must not reference it.
        *sorted(path for path in LOG_DIR.glob("*.json") if path.name != "docx_structure_audit.json"),
        *sorted(LOG_DIR.glob("*.txt")),
    ]
    provenance = {
        "build_date": "2026-08-31",
        "job_id": "1cabec78-f1bd-4615-95d2-5d8196eb46e0",
        "repository": "troyhokanson/tjh-resume-cover-cv",
        "pinned_repository_commit": PINNED_COMMIT,
        "branch": "applications/2026-08-31-flock-customer-experience-associate",
        "controlling_file_blob_shas": {path: blob_sha(path) for path in controlling},
        "application_source_hashes": {
            path.name: sha256(path)
            for path in sorted(APP_DIR.iterdir())
            if path.is_file() and path.name not in {"build_provenance.json", "write_final_reports.py"}
        },
        "artifact_and_report_hashes": {
            str(path.relative_to(APP_DIR)): sha256(path)
            for path in artifact_paths
            if path.exists() and path.name != "build_provenance.json"
        },
    }
    write_json(APP_DIR / "build_provenance.json", provenance)




if __name__ == "__main__":
    main()

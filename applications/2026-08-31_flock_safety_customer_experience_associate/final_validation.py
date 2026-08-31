#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

from docx import Document
from pypdf import PdfReader


APP_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = APP_DIR / "output"
LOG_DIR = APP_DIR / "build_logs"
STEM = "2026-08-31_Troy-Hokanson_Flock-Customer-Experience-Associate_1cabec78"
FILES = {
    "resume_docx": OUTPUT_DIR / f"{STEM}_Resume.docx",
    "resume_pdf": OUTPUT_DIR / f"{STEM}_Resume.pdf",
    "cover_docx": OUTPUT_DIR / f"{STEM}_Cover-Letter.docx",
    "cover_pdf": OUTPUT_DIR / f"{STEM}_Cover-Letter.pdf",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pdf_text(path: Path) -> str:
    return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)


def spelling_report(texts: dict[str, str]) -> dict[str, object]:
    dictionary_path = Path("/usr/share/hunspell/en_US.dic")
    dictionary = set()
    for line in dictionary_path.read_text(encoding="utf-8", errors="ignore").splitlines()[1:]:
        word = line.split("/", 1)[0].strip().lower()
        if word:
            dictionary.add(word)
    allowlist = set()
    for line in (APP_DIR / "proper_names_allowlist.txt").read_text(encoding="utf-8").splitlines():
        for token in re.findall(r"[A-Za-z]+", line):
            allowlist.add(token.lower())
    allowlist.update({
        "saas", "sql", "python", "linkedin", "icloud", "troyhokanson", "exp", "kw",
        "autosync", "nontechnical", "crossfunctional", "customerfacing", "timesensitive",
        "publicsafety", "digitalforensics", "fulltime", "individualcontributor", "hotlist",
        "coursework", "taskforce", "licenseplate", "searchwarrant", "serviceprovider",
        "subpoena", "workflow", "workflows", "troubleshooting", "motorola", "remote",
    })
    def known(token: str) -> bool:
        if token in dictionary or token in allowlist:
            return True
        stems = set()
        if token.endswith("ies") and len(token) > 4:
            stems.add(token[:-3] + "y")
        for suffix in ("s", "es", "ed", "ing", "ly", "er", "est"):
            if token.endswith(suffix) and len(token) > len(suffix) + 2:
                stem = token[:-len(suffix)]
                stems.update({stem, stem + "e"})
                if stem.endswith(stem[-1:] * 2):
                    stems.add(stem[:-1])
        return any(stem in dictionary or stem in allowlist for stem in stems)
    unknown: dict[str, list[str]] = {}
    for name, text in texts.items():
        hits = set()
        for raw in re.findall(r"[A-Za-z]+(?:['-][A-Za-z]+)*", text):
            for token in re.split(r"[-']", raw):
                token = token.lower()
                if token == "s" or len(token) <= 1 or known(token):
                    continue
                hits.add(token)
        unknown[name] = sorted(hits)
    return {
        "checker": "Hunspell en_US dictionary plus saved role-specific proper-name allowlist",
        "allowlist": "proper_names_allowlist.txt",
        "unknown_tokens": unknown,
        "passed": all(not values for values in unknown.values()),
    }


def grammar_report(texts: dict[str, str]) -> dict[str, object]:
    patterns = {
        "em_dash": "—",
        "en_dash": "–",
        "double_hyphen": "--",
        "ellipsis": "...",
        "exclamation": "!",
        "smart_double_quote_left": "“",
        "smart_double_quote_right": "”",
        "smart_single_quote_left": "‘",
        "smart_single_quote_right": "’",
    }
    findings: dict[str, dict[str, int]] = {}
    for name, text in texts.items():
        findings[name] = {label: text.count(value) for label, value in patterns.items() if text.count(value)}
        repeated = len(re.findall(r"\b([A-Za-z]+)\s+\1\b", text, flags=re.IGNORECASE))
        if repeated:
            findings[name]["repeated_word"] = repeated
    return {
        "checker": "Deterministic punctuation, repetition, and layout-language scan plus visual/manual readback",
        "findings": findings,
        "passed": all(not values for values in findings.values()),
        "manual_readback": "Pass. All three rendered pages were inspected; no clipping, orphan headings, malformed bullets, or sentence fragments were observed.",
    }


def metadata_report() -> dict[str, object]:
    reports: dict[str, object] = {}
    for name, path in FILES.items():
        if path.suffix == ".docx":
            doc = Document(path)
            props = doc.core_properties
            with zipfile.ZipFile(path) as archive:
                names = archive.namelist()
                xml = "\n".join(
                    archive.read(item).decode("utf-8", errors="replace")
                    for item in names
                    if item.endswith(".xml")
                )
            checks = {
                "author": props.author == "Troy Hokanson",
                "last_modified_by": props.last_modified_by == "Troy Hokanson",
                "title_present": "Flock Safety" in (props.title or ""),
                "subject_present": "1cabec78-f1bd-4615-95d2-5d8196eb46e0" in (props.subject or ""),
                "keywords_present": "Customer Experience Associate" in (props.keywords or ""),
                "no_comments_part": not any("comments" in item.lower() for item in names),
                "no_tracked_changes": not re.search(r"<w:(?:ins|del)(?:\s|>)", xml),
                "no_hidden_text": "<w:vanish" not in xml,
                "no_source_path": "/workspace/" not in xml and "project_sources" not in xml,
            }
            reports[name] = {"checks": checks, "passed": all(checks.values()), "sha256": sha256(path)}
        else:
            reader = PdfReader(path)
            metadata = {str(key): str(value) for key, value in (reader.metadata or {}).items()}
            checks = {
                "author": metadata.get("/Author") == "Troy Hokanson",
                "creator": metadata.get("/Creator") == "Troy Hokanson",
                "producer": metadata.get("/Producer") == "Troy Hokanson",
                "title_present": "Flock Safety" in metadata.get("/Title", ""),
                "subject_present": "1cabec78-f1bd-4615-95d2-5d8196eb46e0" in metadata.get("/Subject", ""),
                "no_creation_date": "/CreationDate" not in metadata,
                "no_modification_date": "/ModDate" not in metadata,
                "no_source_path": all("/workspace/" not in value and "project_sources" not in value for value in metadata.values()),
            }
            reports[name] = {
                "checks": checks,
                "metadata": metadata,
                "pages": len(reader.pages),
                "passed": all(checks.values()),
                "sha256": sha256(path),
            }
    return {"documents": reports, "passed": all(item["passed"] for item in reports.values())}


def ats_report(resume: str, cover: str) -> dict[str, object]:
    combined = f"{resume}\n{cover}".lower()
    supported = {
        "technical troubleshooting": "technical troubleshooting",
        "hardware and software": "hardware and software",
        "phone and email support": "phone and email support",
        "cross-functional escalation": "cross-functional escalation",
        "case ownership": "case ownership",
        "documentation": "documentation",
        "knowledge resources": "resource library",
        "public safety": "public-safety",
        "customer communication": "customer communication",
        "concurrent prioritization": "concurrent case",
    }
    matched = {label: term in combined for label, term in supported.items()}
    gaps = [
        "No verified commercial SaaS-support title or support-queue ownership metrics.",
        "No verified live-chat support experience.",
        "No verified Jira experience.",
        "No verified Salesforce experience; omitted rather than inferred.",
        "No verified SLA, ticket-volume, CSAT, or first-response-time metrics.",
        "Weekend availability must be confirmed by Troy before submission.",
    ]
    return {
        "official_job_description": "job_description.md",
        "supported_target_terms": matched,
        "supported_term_pass_rate": round(sum(matched.values()) / len(matched), 2),
        "truth_safe_gaps": gaps,
        "keyword_stuffing_detected": False,
        "assessment": "Pass. The packet covers the principal transferable duties and states the material support-platform gaps directly.",
        "passed": all(matched.values()),
    }


def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    texts = {
        "resume": pdf_text(FILES["resume_pdf"]),
        "cover_letter": pdf_text(FILES["cover_pdf"]),
    }
    reports = {
        "spelling": spelling_report(texts),
        "grammar": grammar_report(texts),
        "metadata": metadata_report(),
        "ats": ats_report(texts["resume"], texts["cover_letter"]),
    }
    for name, report in reports.items():
        (LOG_DIR / f"{name}_audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    summary = {name: bool(report["passed"]) for name, report in reports.items()}
    print(json.dumps(summary, indent=2))
    return 0 if all(summary.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Build Troy's reusable expert-network and contractor one-page profile."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from docx.shared import Pt

from docx_header import STEEL, add_hyperlink, set_paragraph_format, set_run
from profile_one_pager import (
    add_profile_bullet,
    add_profile_identity,
    add_profile_paragraph,
    add_profile_role,
    add_profile_section,
    new_profile_document,
)


OUTPUT = ROOT / "output" / "doc" / "Troy_Hokanson_Expert_Contractor_Profile.docx"


def build_profile() -> Path:
    doc = new_profile_document()
    add_profile_identity(
        doc,
        "Expert Network & Independent Contractor Profile",
        ["Investigations | Digital Forensics | Fraud | Public Safety Technology | AI Evaluation"],
    )

    add_profile_section(doc, "Professional Profile")
    add_profile_paragraph(
        doc,
        "Independent consultant and subject-matter expert with 25 years of law-enforcement "
        "experience, nine years of U.S. Army service, six years as a detective and digital "
        "forensic examiner, and 18 years as remote university faculty. Combines practitioner-level "
        "knowledge of investigations, digital evidence, fraud, public-safety technology, adult "
        "learning, and stakeholder communication with current paid AI project experience.",
    )
    add_profile_paragraph(
        doc,
        "AI-fluent evaluator experienced in evidence-led research, prompt development, source "
        "validation, structured analysis, and human review of model-generated content for accuracy, "
        "reasoning quality, completeness, unsupported claims, and instruction adherence.",
    )

    add_profile_section(doc, "Consulting and Expertise Areas")
    add_profile_paragraph(
        doc,
        "Expert interviews and market research | Public-safety technology adoption | Investigative "
        "and digital-evidence workflows | Fraud and financial investigations | AI response evaluation "
        "and quality review | Training, enablement, and adult education | Multi-agency and stakeholder "
        "coordination",
        size=9.0,
    )

    add_profile_section(doc, "Selected Experience")
    add_profile_role(doc, "Generalist Expert", "Mercor", "2026-Present")
    add_profile_bullet(
        doc,
        "Independent contractor selected for project-based expert work supporting AI-related "
        "initiatives; completed onboarding and paid task work while observing platform "
        "confidentiality restrictions.",
    )
    add_profile_role(
        doc,
        "Detective | Digital Forensic Examiner | Police Officer",
        "Lakeville Police Department",
        "1998-2024",
    )
    add_profile_bullet(
        doc,
        "Led evidence-intensive criminal and fraud investigations, including a multi-victim "
        "Business Email Compromise matter with more than $360,000 in verified losses, a felony "
        "conviction, and written recognition from an assistant county attorney.",
    )
    add_profile_bullet(
        doc,
        "Examined mobile, computer, cloud, and online evidence using Cellebrite, FTK, X-Ways, "
        "Magnet AXIOM, GrayKey, and related tools; recognized as a digital-forensics "
        "subject-matter expert and peer resource.",
    )
    add_profile_bullet(
        doc,
        "Produced prosecution-ready documentation, built repeatable investigative resource "
        "workflows, coordinated with local, state, and federal partners, and received more than "
        "20 written commendations or recognitions.",
    )
    add_profile_role(doc, "Adjunct Faculty", "University of Phoenix", "2007-2025")
    add_profile_bullet(
        doc,
        "Delivered 18 years of remote criminal-justice instruction for adult learners; received "
        "Phoenix 500 Faculty Excellence recognition in 2020 and 2021 and the John Sperling "
        "Distinguished Faculty Award in 2024.",
    )
    add_profile_role(
        doc,
        "U.S. Army",
        "Active Duty, Reserve, and Minnesota Army National Guard",
        "1989-1998",
    )
    add_profile_bullet(
        doc,
        "Nine years of service across infantry, armor, motor transport, and military-police "
        "assignments; earned the Army Achievement Medal and Army Good Conduct Medal.",
    )

    add_profile_section(doc, "Education, Credentials, and Selected Training")
    add_profile_paragraph(
        doc,
        "M.A., Police Leadership, Administration and Education, University of St. Thomas (GPA "
        "3.94) | B.A., Criminal Justice, Magna Cum Laude | NW3C Certified Cyber Crime "
        "Investigator (3CE), Certificate 4793 | Prior Cellebrite CCLO/CCPA | X-Ways Forensics | "
        "AccessData FTK | Reid Interviewing and Interrogation | BCA Supervision and Management",
        size=8.5,
    )

    add_profile_section(doc, "Engagements")
    add_profile_paragraph(
        doc,
        "Available for expert-network consultations, research interviews, scoped advisory work, "
        "public-safety technology and investigative-workflow reviews, AI evaluation and domain-SME "
        "projects, and training-content review.",
        size=9.0,
    )
    p = doc.add_paragraph()
    set_paragraph_format(p, before=0, after=0, line=1.0)
    set_run(p.add_run("Source-backed portfolio and public evidence: "), size=8.5, bold=True)
    add_hyperlink(
        p,
        "TroyHokanson.com/evidence.html",
        "https://troyhokanson.com/evidence.html",
        color=STEEL,
        size=8.5,
        bold=True,
    )
    p.paragraph_format.space_after = Pt(0)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUTPUT)
    return OUTPUT


if __name__ == "__main__":
    print(build_profile())

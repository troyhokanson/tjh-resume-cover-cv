"""
specs/trm_all_source_investigator.py
TRM Labs – All‑Source Investigator, Scam Disruption (US‑remote)
Posted: 2026  |  Scam Disruption team – Blockchain Intelligence
Role: fully remote within the US. Mission‑aligned application – strong
investigative and legal process match, crypto experience ramping.

Usage:
    from build_doc import build_document
    from specs.trm_all_source_investigator import RESUME_SPEC, COVER_SPEC

    build_document("resume",       RESUME_SPEC,
                   "output/Hokanson_Resume_TRM_All_Source_Investigator_2026-06-15.docx")
    build_document("cover_letter", COVER_SPEC,
                   "output/Hokanson_Cover_TRM_All_Source_Investigator_2026-06-15.docx")
"""

from datetime import date

TODAY = date(2026, 6, 15).strftime("%B %d, %Y")

RESUME_SPEC = {
    "summary": (
        "All‑source financial crimes and digital forensics investigator with 25 years of law "
        "enforcement experience, six years on a 10‑agency electronic crimes task force covering "
        "the southern Twin Cities metro, and nine years of U.S. Army service. Led 68 documented "
        "financial crimes cases—including transaction card fraud, check forgery, identity theft, "
        "and vulnerable‑adult exploitation—built to withstand cross‑examination and resulting in "
        "$295,704.11 in court‑ordered restitution and a 15‑year federal sentence. Expert in "
        "end‑to‑end legal process: drafting and executing multi‑jurisdictional search warrants, "
        "operationalizing returns, and converting disparate digital, financial, and OSINT data into "
        "defensible targeting packages. Heavy AI operator who runs 10+ intelligence and analytics "
        "platforms daily (Perplexity, Claude, ChatGPT, Copilot, Gemini, NotebookLM, and others) to "
        "accelerate triage, pattern recognition, and memo‑grade outputs; now directing that workflow "
        "into crypto‑enabled scams and blockchain intelligence."
    ),
    "skills": (
        "Financial crimes and fraud investigations; end‑to‑end legal process (search warrants, "
        "subpoenas, returns analysis); multi‑source link and pattern analysis; digital forensics and "
        "evidence handling; OSINT and commercial‑data research; inter‑agency coordination; "
        "prosecution‑ready report writing and federal‑style leads; AI‑accelerated analysis and "
        "drafting; remote and async collaboration; victim‑centered scam disruption."
    ),
    "jobs": [
        {
            "title": "Detective / Electronic Crimes Task Force Investigator",
            "employer": "Dakota County Electronic Crimes Task Force (10‑agency consortium), Minnesota",
            "dates": "2015–2021",
            "bullets": [
                "Ran financial‑crime investigations end‑to‑end across a 10‑agency electronic crimes "
                "task force, documenting 68 cases including 14 transaction card fraud, 13 forgery and "
                "check fraud, 7 identity theft, multiple vulnerable‑adult exploitation matters, and "
                "multi‑subject schemes spanning jurisdictions.",
                "Drafted, served, and worked returns from multi‑jurisdictional search warrants "
                "(including email providers and device seizures), then fused surveillance video, "
                "digital artifacts, financial records, and interview notes into prosecution‑ready "
                "case files.",
                "Delivered disruption‑grade outcomes: task‑force financial crime cases produced "
                "$295,704.11 in court‑ordered restitution and a 15‑year federal sentence, with files "
                "structured to survive cross‑examination at both state and federal levels.",
                "Practiced link and pattern analysis by pivoting from single transactions or artifacts "
                "(e.g., one check image, one Gmail hit, one surveillance still) to full operating "
                "pictures that identified operators, accomplices, and movement patterns across "
                "jurisdictions.",
                "Processed 5,304 GB of digital evidence in a single calendar year using Cellebrite UFED, "
                "Magnet AXIOM, FTK, X‑Ways Forensics, and GrayKey, correlating device artifacts with "
                "banking records, OSINT, and victim statements to build defensible attribution chains.",
            ],
        },
        {
            "title": "Detective / Fraud and Financial Crimes Investigator",
            "employer": "Lakeville Police Department, Lakeville, Minnesota",
            "dates": "2010–2015",
            "bullets": [
                "Led multi‑victim fraud and financial‑crime investigations involving unauthorized credit "
                "card charges, occupational fraud, organized schemes, and thefts impacting businesses "
                "and individuals, often self‑initiated from patrol leads.",
                "Authored search warrants and affidavits, preserved digital accounts, and analyzed "
                "return data to connect subjects to offenses and build clear, concise case packages for "
                "prosecutors and command staff.",
                "Coordinated with probation officers, banks, and external agencies to align investigative "
                "findings with restitution, supervision conditions, and loss‑recovery priorities.",
            ],
        },
        {
            "title": "Adjunct Faculty, Criminal Justice (Remote)",
            "employer": "University of Phoenix (Online)",
            "dates": "2005–2023",
            "bullets": [
                "Designed and delivered undergraduate criminal justice curriculum entirely online for 18+ "
                "years, translating complex investigative and legal concepts into accessible written "
                "content for non‑specialist audiences.",
                "Maintained high standards of written feedback and documentation in a fully remote, "
                "async environment that mirrors TRM's Slack‑ and Notion‑driven operating model.",
            ],
        },
    ],
    "extra_sections": [
        {
            "heading": "Certifications, AI and Scam‑Disruption Focus",
            "paragraphs": [
                "Certified Fraud Examiner (CFE) — actively pursuing through ACFE, 2026. Minnesota Peace "
                "Cellebrite CCLO and CCPA — "
                "trained and proficient (2016, recertified 2020). Heavy AI operator using Perplexity, "
                "Claude, ChatGPT, Copilot, Gemini, NotebookLM, and GitHub‑based automation as core "
                "investigative tools for OSINT, document analysis, and pattern recognition. Personally "
                "invested in scam disruption after a close family member lost $20,000 to a crypto‑ATM "
                "scam; actively ramping on blockchain intelligence, pig‑butchering and romance‑fraud "
                "typologies, and victim‑to‑operator tracing heuristics."
            ],
        }
    ],
}

COVER_SPEC = {
    "date_str": TODAY,
    "recipient_name": "Hiring Manager",
    "recipient_org": "TRM Labs",
    "recipient_address": ["Remote — United States"],
    "salutation": "Hiring Manager",
    "body_paragraphs": [
        "I spent nine years in the U.S. Army and 25 years as a law enforcement officer investigating "
        "financial crimes. What I carry from that background into this role is not simply a list of "
        "credentials. It is a bone-deep understanding that fraud is not an abstract loss metric — it "
        "is money taken from people who trusted a system designed to protect them. I know that "
        "personally. My birth mother lost $20,000 to a crypto-ATM scam and never recovered a dollar. "
        "The operators who built that operation are still out there. TRM's Scam Disruption mission is "
        "not abstract to me. It is the work I want to be doing.",
        "During six years assigned to the Dakota County Electronic Crimes Task Force — a 10-agency "
        "consortium covering the southern Twin Cities metro — I ran financial crime investigations "
        "end-to-end: 68 documented cases including transaction card fraud, check forgery, identity "
        "theft, and multi-subject organized schemes spanning jurisdictions. Those cases produced "
        "$295,704.11 in court-ordered restitution and a 15-year federal sentence. Every file was "
        "built to withstand cross-examination because in that environment, it had to. I drafted and "
        "executed multi-jurisdictional search warrants, worked the returns, and fused digital "
        "artifacts, financial records, surveillance video, and OSINT into prosecution-ready targeting "
        "packages — the same intelligence flywheel TRM's All-Source Investigators run daily.",
        "The pivot from a single transaction to a full operator network is not a new concept for me. "
        "That is how financial crime investigations work. You start with one check image, one Gmail "
        "hit, one surveillance still — and you build until you have the operator, the network, and "
        "the movement pattern. I have done that work across state and federal venues, coordinating "
        "with partner agencies, prosecutors, and federal task forces. The targeting-package language "
        "is new; the tradecraft is not.",
        "I processed 5,304 GB of digital evidence in a single calendar year using Cellebrite UFED, "
        "Magnet AXIOM, FTK, X-Ways Forensics, and GrayKey. I currently run 12 AI intelligence and "
        "analytics platforms — Perplexity, Claude, ChatGPT, Copilot, Gemini, NotebookLM, and others "
        "— as core tools for OSINT research, document analysis, and fraud-pattern recognition. I "
        "have built a GitHub-based document automation pipeline with Python scripting and AI-driven "
        "workflows. TRM asks for top-decile AI fluency in investigative work. I am already there.",
        "For 18 years I designed and delivered criminal justice curriculum entirely online for the "
        "University of Phoenix, long before remote work was a standard expectation. I know how to "
        "operate with high autonomy and high output in an async environment, document everything "
        "clearly in writing, and communicate findings to non-specialist audiences without losing "
        "precision — exactly what TRM's Notion-driven, Slack-first team requires.",
        "I am a Protected Veteran under VEVRAA and an Individual with a Disability under Section 503 "
        "of the Rehabilitation Act. I welcome the opportunity to discuss how my financial crimes "
        "investigative background, legal process expertise, and applied AI fluency can contribute to "
        "TRM's mission of dismantling the scam networks that devastate real people.",
    ],
}

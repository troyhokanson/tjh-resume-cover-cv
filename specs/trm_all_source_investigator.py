"""Historical TRM Labs application source.

This role is no longer active and crypto roles are outside the current search scope.
The source remains only to preserve the application record. It was corrected after
the original build to remove unsupported metrics, private family information,
status-disclosure language, and career-date drift. Do not reuse it as a template.
"""

from datetime import date


ARCHIVED = True
TODAY = date(2026, 6, 15).strftime("%B %d, %Y")

RESUME_SPEC = {
    "summary": (
        "Financial-crimes investigator and digital forensic examiner with 25 years "
        "of Minnesota law-enforcement experience, including 4.5 years assigned to "
        "the ten-agency Dakota County Electronic Crimes Task Force. Conducted fraud "
        "and digital-evidence investigations, drafted legal process, analyzed returns, "
        "and wrote findings for investigators, prosecutors, and partner agencies. "
        "Personally processed 5,304 GB of digital evidence in 2020. U.S. Army veteran "
        "with 18 years of remote adjunct Criminal Justice teaching experience."
    ),
    "skills": (
        "Financial-crimes investigations; search warrants, subpoenas, and returns "
        "analysis; digital evidence preservation and examination; OSINT and "
        "commercial-data research; cross-agency coordination; prosecution-ready "
        "report writing; remote collaboration."
    ),
    "jobs": [
        {
            "title": "Detective / Digital Forensic Examiner",
            "employer": (
                "Dakota County Electronic Crimes Task Force, assigned from Lakeville "
                "Police Department"
            ),
            "dates": "June 2017 - December 2021",
            "bullets": [
                "Conducted digital forensic examinations for Lakeville and partner "
                "agencies within a ten-agency task-force structure.",
                "Drafted and executed search warrants, analyzed legal-process returns, "
                "and connected digital artifacts with financial records, surveillance "
                "video, and interview findings.",
                "Personally processed 5,304 GB of digital evidence in 2020 using "
                "Cellebrite UFED, Magnet AXIOM, Forensic Toolkit (FTK), X-Ways "
                "Forensics, and GrayKey.",
            ],
        },
        {
            "title": "Police Officer / Investigator",
            "employer": "Lakeville Police Department, Lakeville, Minnesota",
            "dates": "March 2010 - May 2011",
            "bullets": [
                "Investigated fraud, financial crimes, and property offenses and wrote "
                "case files for prosecutors and command staff.",
                "Authored search-warrant affidavits, preserved digital accounts, and "
                "analyzed records to identify subjects and document losses.",
            ],
        },
        {
            "title": "Adjunct Faculty / Criminal Justice",
            "employer": "University of Phoenix, Remote",
            "dates": "March 2007 - October 2025",
            "bullets": [
                "Taught undergraduate Criminal Justice courses online for 18 years, "
                "explaining investigative and legal concepts to non-specialist audiences.",
            ],
        },
    ],
    "extra_sections": [
        {
            "heading": "Professional Development",
            "paragraphs": [
                "Certified Fraud Examiner (CFE) credential in progress through ACFE. "
                "Cellebrite mobile-device forensics training completed in 2016, 2018, "
                "and 2020."
            ],
        }
    ],
}

COVER_SPEC = {
    "date_str": TODAY,
    "recipient_name": "Hiring Manager",
    "recipient_org": "TRM Labs",
    "recipient_address": ["Remote, United States"],
    "salutation": "Hiring Manager",
    "body_paragraphs": [
        "I spent 25 years in Minnesota law enforcement investigating fraud, financial "
        "crimes, and digital evidence. The work taught me that fraud is not an abstract "
        "loss metric. It is money taken from people who trusted a system designed to "
        "protect them.",
        "During 4.5 years assigned to the Dakota County Electronic Crimes Task Force, I "
        "conducted digital forensic examinations within a ten-agency structure. I "
        "drafted legal process, worked the returns, and connected digital artifacts with "
        "financial records, surveillance video, and investigative findings.",
        "I personally processed 5,304 GB of digital evidence in 2020 using Cellebrite "
        "UFED, Magnet AXIOM, Forensic Toolkit, X-Ways Forensics, and GrayKey. For 18 "
        "years, I also taught undergraduate Criminal Justice courses online, which "
        "required clear writing, careful documentation, and independent work.",
        "My background is strongest in investigations, legal process, digital evidence, "
        "and written analysis. Blockchain intelligence would be a new technical domain, "
        "and I would approach it with the same disciplined learning and verification "
        "used throughout my investigative career.",
    ],
}

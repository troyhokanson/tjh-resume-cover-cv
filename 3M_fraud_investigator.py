"""
specs/3m_fraud_investigator.py
3M Fraud Investigator — Maplewood, MN
Posted: May 2026  |  Compensation: $145,676–$178,049
"""

from datetime import date

TODAY = date(2026, 6, 15).strftime("%B %d, %Y")

RESUME_SPEC = {
    "summary": (
        "Senior fraud and financial crimes investigator with 25 years of law "
        "enforcement experience, a Master of Arts in Police Leadership, "
        "Administration and Education, and a documented portfolio of complex "
        "fraud, theft, and financial exploitation cases. Experienced leading "
        "sensitive investigations from intake through resolution, analyzing "
        "financial and documentary evidence, conducting interviews independently, "
        "and producing clear, concise reports for prosecutorial and senior "
        "leadership review. Actively pursuing the Certified Fraud Examiner (CFE) "
        "designation through ACFE."
    ),
    "skills": (
        "Fraud and financial crimes investigations; forensic review of financial "
        "and documentary records; investigative interviewing; digital forensics "
        "supporting fraud inquiries; case strategy and planning; search warrants "
        "and subpoenas; inter-agency coordination; evidence preservation and chain "
        "of custody; report writing and executive-level case summarization; OSINT "
        "and data-driven analysis; Microsoft Excel financial summaries."
    ),
    "jobs": [
        {
            "title": "Detective / Fraud and Financial Crimes Investigator",
            "employer": "Lakeville Police Department, Lakeville, Minnesota",
            "dates": "2010–2021",
            "bullets": [
                "Led multi-victim fraud and financial crime investigations involving "
                "unauthorized credit card charges, occupational fraud, organized schemes, "
                "and thefts impacting businesses and individuals. Performed financial "
                "transaction analysis, compiled structured Excel summaries, and developed "
                "case packages supporting felony convictions, restitution orders, and "
                "long-term supervision conditions.",
                "Directed investigations combining physical, digital, and video evidence "
                "to rapidly identify suspects using automated databases, photo "
                "identification, and coordinated warrant service with partner agencies. "
                "Authored search warrants and affidavits, preserved digital accounts, and "
                "analyzed return data to connect subjects to offenses.",
                "Self-initiated fraud case follow-up during patrol assignments, working "
                "cases through to resolution. Earned written commendations from supervisors "
                "and probation partners for documentation quality, initiative, and "
                "inter-agency collaboration.",
            ],
        },
    ],
    "extra_sections": [
        {
            "heading": "Certifications and Professional Development",
            "paragraphs": [
                "Certified Fraud Examiner (CFE) — actively pursuing through ACFE, 2026. "
                "Minnesota Peace Officer License No. 4849 — POST Board Certified, 1998–2023. "
                "BCA Certificate, Bureau of Criminal Apprehension. "
                "Cellebrite CCLO and CCPA — trained and proficient (2016, recertified 2020)."
            ],
        }
    ],
}

COVER_SPEC = {
    "date_str": TODAY,
    "recipient_name": "Hiring Manager",
    "recipient_org": "3M",
    "recipient_address": ["3M Center", "Maplewood, MN 55144"],
    "salutation": "Hiring Manager",
    "body_paragraphs": [
        "I am writing to express my interest in the Fraud Investigator position at 3M "
        "in Maplewood, Minnesota. With 25 years of law enforcement experience, a Master "
        "of Arts in Police Leadership, Administration and Education, and a documented "
        "portfolio of complex fraud and financial crime investigations, I am prepared to "
        "lead and support sensitive matters that require careful analysis, independent "
        "judgment, and clear communication with senior leadership.",
        "Throughout my investigative career I have led cases involving unauthorized "
        "credit card use, occupational fraud, organized fraud schemes, and theft from "
        "businesses and individuals. I have gathered and analyzed financial and "
        "documentary evidence, compiled structured summaries, and developed case packages "
        "that supported felony convictions, restitution orders, and long-term supervision "
        "conditions. I have managed multiple investigations simultaneously and consistently "
        "presented findings in a concise, factual manner to prosecutors and command staff.",
        "In addition to traditional field investigations I have applied digital forensics, "
        "call detail record analysis, and database queries to connect subjects to events "
        "and verify or refute statements. I understand the importance of accurate "
        "documentation and neutral, evidence-based reporting when dealing with sensitive "
        "allegations, and I would bring that discipline to 3M's fraud investigation function.",
        "I understand this position is based on-site in Maplewood and that the ideal "
        "candidate brings strong accounting or finance experience alongside investigative "
        "skills. My path has come through law enforcement and fraud investigation rather "
        "than public accounting, but my graduate education, my experience working complex "
        "financial and documentary evidence, and my active pursuit of the Certified Fraud "
        "Examiner designation demonstrate my commitment to the standards of the fraud "
        "examination profession.",
        "I would welcome the opportunity to discuss how my investigative background, case "
        "management experience, and ability to distill complex fact patterns into clear "
        "written findings can support 3M's fraud investigation efforts.",
    ],
}

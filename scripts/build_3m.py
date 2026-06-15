"""
scripts/build_3m.py
One-command builder for the 3M Fraud Investigator application package.
Builds both the resume and cover letter with the locked navy/gold header
and controlled-distribution footer via build_doc.py.

Usage (from repo root):
    python scripts/build_3m.py

Output:
    output/Hokanson_Resume_3M_Fraud_Investigator_2026-06-15.docx
    output/Hokanson_Cover_3M_Fraud_Investigator_2026-06-15.docx
"""

from build_doc import build_document
from specs.three_m_fraud_investigator import RESUME_SPEC, COVER_SPEC

build_document(
    "resume",
    RESUME_SPEC,
    "output/Hokanson_Resume_3M_Fraud_Investigator_2026-06-15.docx",
)

build_document(
    "cover_letter",
    COVER_SPEC,
    "output/Hokanson_Cover_3M_Fraud_Investigator_2026-06-15.docx",
)

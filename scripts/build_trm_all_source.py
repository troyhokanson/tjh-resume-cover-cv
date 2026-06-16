"""
scripts/build_trm_all_source.py
One-command builder for the TRM Labs All‑Source Investigator resume.
Builds a TRM‑targeted resume with the locked navy/gold header and
controlled‑distribution footer via build_doc.py.

Usage (from repo root):
    python scripts/build_trm_all_source.py

Output:
    output/Hokanson_Resume_TRM_All_Source_Investigator_2026-06-15.docx
"""

from build_doc import build_document
from specs.trm_all_source_investigator import RESUME_SPEC

build_document(
    "resume",
    RESUME_SPEC,
    "output/Hokanson_Resume_TRM_All_Source_Investigator_2026-06-15.docx",
)

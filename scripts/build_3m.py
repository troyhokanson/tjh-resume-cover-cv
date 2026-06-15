from build_doc import build_document
from specs.three_m_fraud_investigator import RESUME_SPEC, COVER_SPEC

build_document("resume",       RESUME_SPEC, "output/Hokanson_Resume_3M_Fraud_Investigator_2026-06-15.docx")
build_document("cover_letter", COVER_SPEC,  "output/Hokanson_Cover_3M_Fraud_Investigator_2026-06-15.docx")

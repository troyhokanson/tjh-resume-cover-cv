#!/usr/bin/env bash
# new_application.sh
# ==================
# One command to start any new Troy Hokanson job application.
# Prompts for the job description file, employer name, role, and profile,
# runs the ATS audit, and prints the mandatory final validation commands.
#
# Usage:
#   bash new_application.sh
#
# Requirements: pip install -r requirements.txt

set -e

echo ""
echo "================================================"
echo "  Troy Hokanson -- New Application Setup"
echo "================================================"
echo ""

# ---- 1. Job description file ------------------------------------------------
read -p "Path to job description .txt file: " JD_FILE
if [ ! -f "$JD_FILE" ]; then
  echo "ERROR: File not found: $JD_FILE"
  exit 1
fi

# ---- 2. Profile selection ---------------------------------------------------
echo ""
echo "Profile options:"
echo "  1) siu-fraud                      (SIU Investigator, Fraud Investigator)"
echo "  2) vendor-solutions               (Solutions Consultant, Sales Engineer, Public Safety)"
echo "  3) analyst-intelligence           (Intelligence Analyst, Financial Crime Analyst)"
echo "  4) corporate-security-investigations"
echo "  5) customer-success"
echo "  6) technical-account-management"
echo "  7) dfir-cyber"
read -p "Pick profile [1-7, default 3 for analyst-intelligence]: " PROFILE_CHOICE

case "$PROFILE_CHOICE" in
  1) PROFILE="siu-fraud" ;;
  2) PROFILE="vendor-solutions" ;;
  4) PROFILE="corporate-security-investigations" ;;
  5) PROFILE="customer-success" ;;
  6) PROFILE="technical-account-management" ;;
  7) PROFILE="dfir-cyber" ;;
  *) PROFILE="analyst-intelligence" ;;
esac

echo "Using profile: $PROFILE"

# ---- 3. Employer and role ---------------------------------------------------
echo ""
read -p "Employer short name (e.g. Sibylline): " EMPLOYER
read -p "Role short name (e.g. IntelligenceAnalyst): " ROLE

SAFE_EMPLOYER=$(echo "$EMPLOYER" | tr ' ' '_')
SAFE_ROLE=$(echo "$ROLE" | tr ' ' '_')
DATESTAMP=$(date +%Y-%m-%d)
AUDIT_OUT="build_logs/ats_audit_${SAFE_EMPLOYER}_${SAFE_ROLE}_${DATESTAMP}.txt"
VALIDATE_RESUME_OUT="build_logs/validate_resume_${SAFE_EMPLOYER}_${SAFE_ROLE}_${DATESTAMP}.json"
VALIDATE_COVER_OUT="build_logs/validate_cover_${SAFE_EMPLOYER}_${SAFE_ROLE}_${DATESTAMP}.json"

mkdir -p build_logs

# ---- 4. Run ATS audit -------------------------------------------------------
echo ""
echo "Running ATS keyword audit..."
echo ""

python ats_injector.py \
  --jd "$JD_FILE" \
  --profile "$PROFILE" \
  --floor 0.85 \
  --output "$AUDIT_OUT"

echo ""
echo "------------------------------------------------"
echo "ATS audit saved to: $AUDIT_OUT"
echo "------------------------------------------------"
echo ""

cat <<EOF
MANDATORY BUILD RULES
---------------------
This job description has triggered a formal application build.
Before any final resume, cover letter, CV, recruiter packet, professional bio,
or candidate profile is delivered, shared, uploaded, or marked Ready:

1. Build the ATS version and, when appropriate, the branded navy/gold version.
2. Render each DOCX to PDF.
3. Render every PDF page to PNG.
4. Run validate_application_packet.py on each final document.
5. Save the validator JSON output with the application materials.
6. Fix and rerun until the validator passes.

No final document is ready if the validator fails.

Example final validation commands:

python validate_application_packet.py \
  --docx output/Hokanson_Resume_${SAFE_EMPLOYER}_${SAFE_ROLE}_BRANDED.docx \
  --pdf output/Hokanson_Resume_${SAFE_EMPLOYER}_${SAFE_ROLE}_BRANDED.pdf \
  --header-png output/rendered_resume/page-1.png \
  --header-png output/rendered_resume/page-2.png \
  --doc-type resume \
  --profile $PROFILE \
  --json-out $VALIDATE_RESUME_OUT

python validate_application_packet.py \
  --docx output/Hokanson_Cover_${SAFE_EMPLOYER}_${SAFE_ROLE}_BRANDED.docx \
  --pdf output/Hokanson_Cover_${SAFE_EMPLOYER}_${SAFE_ROLE}_BRANDED.pdf \
  --header-png output/rendered_cover/page-1.png \
  --doc-type cover \
  --profile $PROFILE \
  --json-out $VALIDATE_COVER_OUT

Prompt to use in an AI session:
"Build the resume and cover letter for $EMPLOYER, $ROLE, using profile $PROFILE. Read the live GitHub standards, separate Education from Training and Certifications, use Garamond body/headings/subheadings, prevent orphaned headings and job blocks, render every page, run validate_application_packet.py, and do not deliver the packet until the validator passes. Use ATS keywords from $AUDIT_OUT."
EOF

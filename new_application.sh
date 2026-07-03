#!/usr/bin/env bash
# new_application.sh
# ==================
# One command to start any new Troy Hokanson job application.
# Prompts for job description, profile, employer, role, and draft files.
# Runs mandatory case/training preflight gates, ATS audit, and post-draft verification.
#
# Usage:
#   bash new_application.sh
#
# Requirements: python-docx installed (pip install -r requirements.txt)

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
echo "  1) siu-fraud            (SIU Investigator, Fraud Investigator)"
echo "  2) vendor-solutions     (Solutions Consultant, Sales Engineer, Public Safety)"
echo "  3) analyst-intelligence (Intelligence Analyst, Financial Crime Analyst)"
echo "  4) corporate-security-investigations (Corporate/Enterprise Investigator)"
read -p "Pick profile [1/2/3/4, default 1 for siu-fraud]: " PROFILE_CHOICE

case "$PROFILE_CHOICE" in
  2) PROFILE="vendor-solutions" ;;
  3) PROFILE="analyst-intelligence" ;;
  4) PROFILE="corporate-security-investigations" ;;
  *) PROFILE="siu-fraud" ;;
esac

echo "Using profile: $PROFILE"

# ---- 3. Employer and role (for output file naming) --------------------------
echo ""
read -p "Employer short name (e.g. VWFinancial): " EMPLOYER
read -p "Role short name (e.g. SeniorFraudInvestigator): " ROLE

SAFE_EMPLOYER=$(echo "$EMPLOYER" | tr ' ' '_')
SAFE_ROLE=$(echo "$ROLE" | tr ' ' '_')
DATESTAMP=$(date +%Y-%m-%d)
AUDIT_OUT="build_logs/ats_audit_${SAFE_EMPLOYER}_${SAFE_ROLE}_${DATESTAMP}.txt"
MANIFEST_OUT="build_logs/application_manifest_${SAFE_EMPLOYER}_${SAFE_ROLE}_${DATESTAMP}.json"
VERIFY_OUT="build_logs/verification_report_${SAFE_EMPLOYER}_${SAFE_ROLE}_${DATESTAMP}.json"

mkdir -p build_logs

# ---- 4. Run mandatory preflight gates ---------------------------------------
echo ""
echo "Running mandatory preflight gates..."
echo ""

python application_quality.py prepare \
  --jd "$JD_FILE" \
  --profile "$PROFILE" \
  --employer "$EMPLOYER" \
  --role "$ROLE" \
  --date-seed "$DATESTAMP" \
  --output "$MANIFEST_OUT"

# ---- 5. Run ATS audit -------------------------------------------------------
echo ""
echo "Running ATS keyword audit..."
echo ""

python ats_injector.py \
  --jd "$JD_FILE" \
  --profile "$PROFILE" \
  --floor 0.85 \
  --output "$AUDIT_OUT"

# ---- 6. Drafting + mandatory verification -----------------------------------
echo ""
echo "Drafting checkpoint:"
echo "Build your draft resume and cover letter, then provide file paths to verify."
echo ""
read -p "Path to drafted resume (.txt/.md/.docx): " RESUME_DRAFT
read -p "Path to drafted cover letter (.txt/.md/.docx): " COVER_DRAFT

if [ ! -f "$RESUME_DRAFT" ]; then
  echo "ERROR: Resume draft not found: $RESUME_DRAFT"
  exit 1
fi

if [ ! -f "$COVER_DRAFT" ]; then
  echo "ERROR: Cover draft not found: $COVER_DRAFT"
  exit 1
fi

echo ""
echo "Running mandatory post-draft verification..."
echo ""

python application_quality.py verify \
  --manifest "$MANIFEST_OUT" \
  --resume "$RESUME_DRAFT" \
  --cover "$COVER_DRAFT" \
  --output "$VERIFY_OUT"

echo ""
echo "------------------------------------------------"
echo "Preflight manifest saved to: $MANIFEST_OUT"
echo "Audit saved to: $AUDIT_OUT"
echo "Verification saved to: $VERIFY_OUT"
echo ""
echo "Next steps:"
echo "  1. Use the manifest for required cases/training and variation profile"
echo "  2. Use ATS audit output to close keyword gaps"
echo "  3. Only send after this verification and anti_ai_scan pass"
echo "------------------------------------------------"
echo ""

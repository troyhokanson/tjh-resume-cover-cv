#!/usr/bin/env bash
# new_application.sh
# ==================
# One command to start any new Troy Hokanson job application.
# Prompts for the job description file, employer name, role, and profile,
# then runs the ATS audit and prints exactly what keywords need to be added.
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
echo "  1) siu-fraud          (SIU Investigator, Fraud Investigator)"
echo "  2) vendor-solutions   (Solutions Consultant, Sales Engineer, Public Safety)"
echo "  3) analyst-intelligence (Intelligence Analyst, Financial Crime Analyst)"
read -p "Pick profile [1/2/3, default 1 for siu-fraud]: " PROFILE_CHOICE

case "$PROFILE_CHOICE" in
  2) PROFILE="vendor-solutions" ;;
  3) PROFILE="analyst-intelligence" ;;
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
echo "Audit saved to: $AUDIT_OUT"
echo ""
echo "Next steps:"
echo "  1. Paste the job description into your AI session (Perplexity Space)"
echo "  2. Tell the AI: 'Build resume and cover letter using CASE_BANK,"
echo "     profile $PROFILE, and inject these ATS keywords: [from audit above]'"
echo "  3. Run anti_ai_scan.py on the finished documents before sending"
echo "------------------------------------------------"
echo ""

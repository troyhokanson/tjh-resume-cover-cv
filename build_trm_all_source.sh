#!/usr/bin/env bash
# Quick launcher: pull latest and build the TRM All-Source Investigator package.
# Run from the repo root:
#   bash build_trm_all_source.sh
set -e
git pull
python scripts/build_trm_all_source.py

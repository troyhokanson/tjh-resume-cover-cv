#!/usr/bin/env python3
"""
sync_credentials_catalog.py

Sync Troy Hokanson's Credentials Catalog from Notion (source of truth)
to the GitHub credentials_catalog.json consumed by the linkedin-profile-optimizer,
github-application-document-standard, and resume-file-router skills.

USAGE
-----
    # Dry run (show what would change, don't write)
    python sync_credentials_catalog.py --dry-run

    # Write to local JSON file only
    python sync_credentials_catalog.py --out skills/troy-credentials-library/credentials_catalog.json

    # Write and commit/push to GitHub
    python sync_credentials_catalog.py --push

REQUIREMENTS
------------
    pip install requests
    Environment vars:
        NOTION_TOKEN          - Notion internal integration token with read access to the Catalog DB
        GITHUB_TOKEN          - (only if --push) Personal access token with repo write access

DEFAULTS
--------
    Notion data source: dcfcf803-5470-4240-8dda-46fcbb6ec6d5  (Credentials Catalog (Resume-Ready))
    GitHub repo:        troyhokanson/tjh-resume-cover-cv
    GitHub path:        skills/troy-credentials-library/credentials_catalog.json

The script PRESERVES anything that lives only in the GitHub JSON and is not
modelled in Notion:
    - commendation_quotes (full block)
    - training_hours_total (full block)
    - per-entry fields the Notion DB cannot represent:
        * full multi-value 'profiles' array (Notion catalog stores ONE primary profile;
          this script reads the existing JSON to keep the full eligible list and only
          replaces the entry if the Notion 'Primary Profile' differs from the existing
          first-position profile)
        * credential_id, source, location, status, ptsd_reason (read from Notes field
          and re-parsed; original JSON values are kept where Notes parsing is ambiguous)

If a Notion catalog entry exists that is NOT in the current JSON, it is added with
profiles = [primary_profile_from_notion] and a warning is printed so Troy can
hand-enrich the profiles array later.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

import requests

NOTION_DATA_SOURCE_ID = "dcfcf803-5470-4240-8dda-46fcbb6ec6d5"
NOTION_API_VERSION = "2025-09-03"
NOTION_BASE = "https://api.notion.com/v1"

GITHUB_REPO = "troyhokanson/tjh-resume-cover-cv"
GITHUB_PATH = "skills/troy-credentials-library/credentials_catalog.json"
GITHUB_BRANCH = "main"

DOMAIN_REVERSE = {
    "Digital Forensics": "digital_forensics",
    "Investigations": "investigations",
    "Supervisory / Management": "supervisory_management",
    "Community / Diversity": "community_diversity",
    "Teaching / Faculty": "teaching_faculty",
}

TIER_REVERSE = {
    "Tier 1 - Hero": "headline",
    "Tier 2 - Strong": "strong",
    "Tier 3 - Supporting": "supporting",
    "Suppressed": "suppressed",
}


def notion_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json",
    }


def fetch_all_catalog_rows(token: str, data_source_id: str) -> list[dict]:
    """Query the Notion data source and return every row (paginated)."""
    rows = []
    cursor = None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        url = f"{NOTION_BASE}/data_sources/{data_source_id}/query"
        r = requests.post(url, headers=notion_headers(token), json=body, timeout=30)
        r.raise_for_status()
        data = r.json()
        rows.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
        time.sleep(0.3)
    return rows


def get_prop(props: dict, name: str):
    """Return a plain Python value from a Notion property block."""
    p = props.get(name)
    if not p:
        return None
    t = p.get("type")
    v = p.get(t)
    if v is None:
        return None
    if t == "title":
        return "".join(x.get("plain_text", "") for x in v).strip() or None
    if t == "rich_text":
        return "".join(x.get("plain_text", "") for x in v).strip() or None
    if t == "select":
        return v.get("name") if v else None
    if t == "multi_select":
        return [x.get("name") for x in v] or None
    if t == "checkbox":
        return bool(v)
    if t == "number":
        return v
    if t == "date":
        return v.get("start") if v else None
    if t == "relation":
        return [x.get("id") for x in v] or None
    return v


def notion_row_to_entry(row: dict, existing_by_cat_id: dict) -> tuple[str, dict, list[str]]:
    """
    Convert one Notion catalog row to a JSON entry, merging with the existing
    JSON entry (keyed by Catalog ID) to preserve fields Notion doesn't model.
    Returns (domain_key, entry_dict, warnings).
    """
    props = row.get("properties", {})
    warnings = []

    cat_id = get_prop(props, "Catalog ID")
    name = get_prop(props, "Catalog Entry") or cat_id
    domain_label = get_prop(props, "Domain")
    tier_label = get_prop(props, "Tier")
    primary_profile = get_prop(props, "Profiles")  # single primary profile
    profiles_list = primary_profile if isinstance(primary_profile, list) else (
        [primary_profile] if primary_profile else []
    )
    ptsd_safe = get_prop(props, "PTSD Safe")
    icac_gated = get_prop(props, "ICAC Gated")
    hours = get_prop(props, "Hours")
    date_iso = get_prop(props, "Date")
    provider = get_prop(props, "Provider")
    source_type = get_prop(props, "Source Type")
    notes = get_prop(props, "Notes") or ""

    if not cat_id:
        warnings.append(f"Row missing Catalog ID, skipping: {name}")
        return None, None, warnings

    domain_key = DOMAIN_REVERSE.get(domain_label)
    if not domain_key:
        warnings.append(f"{cat_id}: unknown domain '{domain_label}', skipping")
        return None, None, warnings

    tier_key = TIER_REVERSE.get(tier_label, "supporting")

    # Start from the existing JSON entry so we keep multi-profile arrays,
    # ptsd_reason, location, credential_id, status, source, etc.
    existing = existing_by_cat_id.get(cat_id, {})
    entry = dict(existing)  # shallow copy

    # Overwrite Notion-controlled fields
    entry["id"] = cat_id
    entry["name"] = name
    entry["tier"] = tier_key
    entry["ptsd_safe"] = bool(ptsd_safe)

    if icac_gated:
        entry["allow_icac_required"] = True
    else:
        entry.pop("allow_icac_required", None)

    # Profiles: if Notion has a primary profile that's NOT in the existing list,
    # add it. Otherwise keep the existing multi-value list.
    existing_profiles = entry.get("profiles", [])
    if profiles_list:
        primary = profiles_list[0]
        if primary not in existing_profiles:
            new_profiles = [primary] + [p for p in existing_profiles if p != primary]
            entry["profiles"] = new_profiles
            warnings.append(
                f"{cat_id}: Notion primary profile '{primary}' was not in existing list; "
                f"prepended. Review profiles list: {new_profiles}"
            )
        elif not existing_profiles:
            entry["profiles"] = [primary]
    elif not existing_profiles:
        entry["profiles"] = []
        warnings.append(f"{cat_id}: no profile set in Notion or JSON")

    if hours is not None:
        entry["hours"] = hours
    if provider:
        entry["issuer"] = provider
    if source_type:
        entry["credential_type"] = source_type.lower().replace(" ", "_")

    # Date handling: write to whichever date key the existing entry uses
    if date_iso:
        if existing.get("date") or not any(k in existing for k in ("month_year", "year", "completion_year")):
            entry["date"] = date_iso
        elif "month_year" in existing:
            entry["month_year"] = f"{int(date_iso[5:7])}/{date_iso[:4]}"
        elif "year" in existing:
            entry["year"] = int(date_iso[:4])
        elif "completion_year" in existing:
            entry["completion_year"] = int(date_iso[:4])

    # Notes-derived fields (preserve existing if Notes is empty)
    if notes:
        parsed = parse_notes(notes)
        for k, v in parsed.items():
            if v:
                entry[k] = v

    return domain_key, entry, warnings


NOTES_FIELD_PATTERNS = {
    "credential_id": re.compile(r"Credential ID:\s*([^|]+)"),
    "source": re.compile(r"Source doc:\s*([^|]+)"),
    "location": re.compile(r"Location:\s*([^|]+)"),
    "status": re.compile(r"Status:\s*([^|]+)"),
    "ptsd_reason": re.compile(r"PTSD reason:\s*([^|]+)"),
}


def parse_notes(notes: str) -> dict:
    """Pull structured fields back out of the pipe-delimited Notes column."""
    out = {}
    for field, pat in NOTES_FIELD_PATTERNS.items():
        m = pat.search(notes)
        if m:
            out[field] = m.group(1).strip()
    return out


def build_new_json(rows: list[dict], existing_json: dict) -> tuple[dict, list[str]]:
    """Rebuild the certifications block from Notion rows, preserving the rest."""
    # Index existing entries by catalog id
    existing_by_cat_id = {}
    for domain_key, items in existing_json.get("certifications", {}).items():
        for e in items:
            if e.get("id"):
                existing_by_cat_id[e["id"]] = e

    new_certs = defaultdict(list)
    all_warnings = []
    seen_cat_ids = set()

    for row in rows:
        domain_key, entry, warnings = notion_row_to_entry(row, existing_by_cat_id)
        all_warnings.extend(warnings)
        if not domain_key or not entry:
            continue
        if entry["id"] in seen_cat_ids:
            all_warnings.append(f"Duplicate Catalog ID in Notion: {entry['id']}")
            continue
        seen_cat_ids.add(entry["id"])
        new_certs[domain_key].append(entry)

    # Sort each domain by id for stable diffs
    for k in new_certs:
        new_certs[k].sort(key=lambda e: e.get("id", ""))

    # Detect entries that exist in JSON but not in Notion
    json_cat_ids = set(existing_by_cat_id.keys())
    missing_in_notion = json_cat_ids - seen_cat_ids
    if missing_in_notion:
        all_warnings.append(
            f"{len(missing_in_notion)} entries exist in JSON but not in Notion catalog: "
            f"{sorted(missing_in_notion)}"
        )

    # Build the final dict, preserving non-certification keys
    new_json = dict(existing_json)
    new_json["certifications"] = dict(new_certs)
    return new_json, all_warnings


def write_local(path: Path, data: dict, dry_run: bool) -> bool:
    """Write JSON locally. Returns True if file actually changed."""
    pretty = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if path.exists():
        old = path.read_text()
        if old == pretty:
            print(f"No changes to {path}")
            return False
    if dry_run:
        print(f"[DRY RUN] Would write {len(pretty)} chars to {path}")
        return True
    path.write_text(pretty)
    print(f"Wrote {len(pretty)} chars to {path}")
    return True


def push_to_github(local_path: Path, gh_token: str, repo: str, gh_path: str, branch: str) -> None:
    """Commit the local JSON file to GitHub via the contents API."""
    import base64
    headers = {
        "Authorization": f"token {gh_token}",
        "Accept": "application/vnd.github+json",
    }
    # Get current SHA
    get_url = f"https://api.github.com/repos/{repo}/contents/{gh_path}?ref={branch}"
    r = requests.get(get_url, headers=headers, timeout=30)
    if r.status_code == 404:
        sha = None
    else:
        r.raise_for_status()
        sha = r.json().get("sha")

    content_b64 = base64.b64encode(local_path.read_bytes()).decode()
    payload = {
        "message": "Sync credentials_catalog.json from Notion catalog",
        "content": content_b64,
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha
    put_url = f"https://api.github.com/repos/{repo}/contents/{gh_path}"
    r = requests.put(put_url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    print(f"Pushed to https://github.com/{repo}/blob/{branch}/{gh_path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument(
        "--out",
        default="skills/troy-credentials-library/credentials_catalog.json",
        help="Local JSON output path",
    )
    ap.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    ap.add_argument("--push", action="store_true", help="Commit and push to GitHub after writing")
    ap.add_argument("--data-source-id", default=NOTION_DATA_SOURCE_ID)
    ap.add_argument("--repo", default=GITHUB_REPO)
    ap.add_argument("--gh-path", default=GITHUB_PATH)
    ap.add_argument("--branch", default=GITHUB_BRANCH)
    args = ap.parse_args()

    notion_token = os.environ.get("NOTION_TOKEN")
    if not notion_token:
        print("ERROR: set NOTION_TOKEN environment variable", file=sys.stderr)
        sys.exit(2)

    out_path = Path(args.out).resolve()
    if not out_path.exists():
        print(f"ERROR: existing JSON not found at {out_path}. Sync requires an existing file to preserve non-Notion fields.", file=sys.stderr)
        sys.exit(2)

    existing_json = json.loads(out_path.read_text())
    print(f"Loaded existing JSON: {sum(len(v) for v in existing_json.get('certifications', {}).values())} entries across {len(existing_json.get('certifications', {}))} domains")

    print(f"Fetching catalog rows from Notion data source {args.data_source_id}...")
    rows = fetch_all_catalog_rows(notion_token, args.data_source_id)
    print(f"Fetched {len(rows)} rows")

    new_json, warnings = build_new_json(rows, existing_json)
    new_count = sum(len(v) for v in new_json.get("certifications", {}).values())
    print(f"New JSON: {new_count} entries across {len(new_json['certifications'])} domains")

    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(f"  - {w}")
        print()

    changed = write_local(out_path, new_json, args.dry_run)

    if args.push and not args.dry_run and changed:
        gh_token = os.environ.get("GITHUB_TOKEN")
        if not gh_token:
            print("ERROR: --push requested but GITHUB_TOKEN is not set", file=sys.stderr)
            sys.exit(2)
        push_to_github(out_path, gh_token, args.repo, args.gh_path, args.branch)
    elif args.push and args.dry_run:
        print("[DRY RUN] Would push to GitHub")


if __name__ == "__main__":
    main()

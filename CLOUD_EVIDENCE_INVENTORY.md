# Cloud Evidence Inventory and Duplicate Review

## Purpose

This workflow inventories locally synchronized **OneDrive**, **iCloud Drive**, and **Dropbox** folders when direct ChatGPT connector access is incomplete. It is designed for the Investigator Command Center and the Career Evidence Master.

The scanner is **read-only**. It does not move, rename, delete, upload, or alter source files.

## Tool

`tools/cloud_evidence_inventory.py`

The tool:

- Recursively inventories files from one or more local cloud-sync folders.
- Calculates SHA-256 and MD5 hashes using chunked reads.
- Detects exact duplicates by SHA-256.
- Records file size, modification time, extension, source root, and relative path.
- Applies a preliminary evidence category and sensitivity hint based on the file name and path.
- Optionally compares files against an exported `Sources` tab from the Career Evidence Master.
- Creates a complete manifest, duplicate report, transfer-candidate report, and JSON summary.

## Privacy rule

The generated manifests contain absolute local paths and may reveal private case names, source-system structure, or personal identifiers. Treat all outputs as **private evidence-processing records**.

- Save output under `build_logs/cloud_inventory/` or another private folder.
- Do not commit generated CSV or JSON manifests to GitHub.
- Do not publish the manifest or duplicate report.
- Do not delete source files based only on the duplicate report.
- A hash match identifies identical bytes, but retention still requires source-provenance review.

## Windows quick start

From PowerShell in the repository folder:

```powershell
python .\tools\cloud_evidence_inventory.py
```

The scanner will automatically check common locations when they exist:

- `%OneDrive%`
- `%USERPROFILE%\OneDrive`
- `%USERPROFILE%\iCloudDrive`
- `%USERPROFILE%\iCloudDrive\Documents`
- `%USERPROFILE%\Dropbox`

## Explicit paths

Use explicit paths when the automatic locations differ:

```powershell
python .\tools\cloud_evidence_inventory.py `
  --root "OneDrive=C:\Users\Troy\OneDrive" `
  --root "iCloudDrive=C:\Users\Troy\iCloudDrive" `
  --root "Dropbox=C:\Users\Troy\Dropbox"
```

Repeat `--root` as many times as needed.

## Compare against the Career Evidence Master

Export the Google Sheets `Sources` tab as CSV, then run:

```powershell
python .\tools\cloud_evidence_inventory.py `
  --registry-csv "C:\Private\Career Evidence Sources.csv"
```

Comparison results:

- `Exact SHA-256 match` - byte-identical file already represented in the registry.
- `Filename + size candidate match` - possible duplicate requiring hash or content review.
- `New candidate` - no registry match identified.
- `Unreadable` - access or file-system error; review manually.

## Outputs

Default folder: `build_logs/cloud_inventory/`

- `cloud_inventory_manifest.csv` - every inventoried file.
- `cloud_inventory_duplicates.csv` - all files belonging to an exact hash-duplicate group.
- `cloud_inventory_transfer_candidates.csv` - files not matched to the registry.
- `cloud_inventory_summary.json` - counts, roots, errors, and output paths.

## Transfer review gate

A file may be transferred into Google Drive only after:

1. Exact SHA-256 and size comparison against the source registry.
2. Filename and content review for mislabeled files.
3. Evidence-category selection.
4. Sensitivity and public-use classification.
5. Canonical-folder selection.
6. Confirmation that the file adds unique evidence or materially better provenance.

Never delete the original from OneDrive, iCloud Drive, or Dropbox during the intake process.

## Recommended processing sequence

1. Run the full inventory.
2. Preserve the manifest and JSON summary privately.
3. Review `cloud_inventory_transfer_candidates.csv` first.
4. Separate case, court, training, certification, commendation, and application files.
5. Compare high-value files against the Career Evidence Master by hash.
6. Transfer approved files into the appropriate Google Drive evidence folders.
7. Register each transferred file in the `Sources` tab.
8. Update the matching Case, Court Outcome, Training, Certification, or Award record.
9. Document the intake batch and exceptions in Notion.
10. Retain unresolved duplicates until Troy explicitly approves deletion.

# Cloud Evidence Inventory and Duplicate Review

## Purpose

This workflow inventories locally synced cloud folders without moving, renaming, deleting, uploading, or publishing source files. It is designed for personal OneDrive, work OneDrive, iCloud Drive for Windows, Dropbox, and other local sync folders.

The inventory creates a private manifest with:

- source label and root path
- relative and absolute file paths
- filename, extension, size, and modified time
- SHA-256 and MD5 values
- preliminary evidence category
- sensitivity warning
- exact duplicate groups
- matches against an exported Career Evidence Master Sources tab
- new transfer candidates
- unreadable or online-only placeholder errors

## Privacy rule

The output is private working data. It can contain full local paths, case filenames, subject names, internal case numbers, and other protected information. Keep the generated CSV and JSON files inside `build_logs/`, which is gitignored. Never commit manifests or source files to GitHub.

## Prerequisites

1. Install Python 3 on the Windows computer where OneDrive and iCloud Drive are synced.
2. Clone or update `troyhokanson/tjh-resume-cover-cv`.
3. Make files that require hashing locally available. Online-only placeholders may be logged as unreadable until downloaded by the sync client.
4. Export the `Sources` tab from the private Career Evidence Master as CSV when registry matching is desired.

## Standard Windows run

From PowerShell in the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_cloud_evidence_inventory.ps1 `
  -RegistryCsv "C:\Path\To\career_evidence_sources_export.csv"
```

The launcher automatically checks these locations when present:

- `$env:OneDrive`
- `$env:OneDriveConsumer`
- `$env:OneDriveCommercial`
- `%USERPROFILE%\OneDrive`
- `%USERPROFILE%\iCloudDrive`
- `%USERPROFILE%\Dropbox`

## Explicit roots

Use explicit roots when the sync client uses a custom location:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_cloud_evidence_inventory.ps1 `
  -RegistryCsv "C:\Evidence\career_evidence_sources_export.csv" `
  -Roots @(
    "OneDrive=C:\Users\Troy\OneDrive",
    "iCloudDrive=C:\Users\Troy\iCloudDrive",
    "Dropbox=D:\Dropbox"
  )
```

The Python command can also be run directly:

```powershell
py -3 .\tools\cloud_evidence_inventory.py `
  --root "OneDrive=%USERPROFILE%\OneDrive" `
  --root "iCloudDrive=%USERPROFILE%\iCloudDrive" `
  --registry-csv "C:\Evidence\career_evidence_sources_export.csv"
```

## Outputs

The default output folder is:

```text
build_logs/cloud_inventory/
```

Files created:

- `cloud_inventory_manifest.csv` — all readable and unreadable entries
- `cloud_inventory_duplicates.csv` — files sharing an exact SHA-256 hash
- `cloud_inventory_transfer_candidates.csv` — readable files not matched to the registry
- `cloud_inventory_summary.json` — totals, roots, errors, duplicates, and registry matches

## Review and transfer procedure

1. Review `cloud_inventory_summary.json` for scan completeness and errors.
2. Review `cloud_inventory_duplicates.csv` before considering any deletion. The script never deletes files.
3. Review `cloud_inventory_transfer_candidates.csv` and remove non-career material, application drafts, temporary files, and low-value artifacts.
4. For each retained candidate, determine the proper Google Drive destination:
   - cases and investigative reports → `02 Cases`
   - official court outcomes → `02 Cases/Court Outcomes` or the structured case folder
   - training histories and course evidence → `03 Training`
   - certificates and credentials → `04 Certifications`
   - commendations and awards → `05 Commendations & Awards`
5. Upload only verified, nonduplicate candidates.
6. Download or otherwise retrieve the exact uploaded raw Drive file and calculate SHA-256 and MD5 from those canonical post-upload bytes. Do not reuse a pre-upload working-copy hash unless an exact-byte comparison proves the uploaded file is identical.
7. Register each uploaded source in the Career Evidence Master with Drive file ID, size, post-upload SHA-256, MD5, provenance, sensitivity, role, original/derivative status, verification method, and retention decision.
8. Link the source to the correct case, ECTF file, training record, certification, award, or Notion page.
9. Read back every spreadsheet and Notion write before calling the ingestion complete.

## Post-upload integrity gate

A newly uploaded source does not pass integrity review merely because the upload action succeeded or the reported byte size matches. The controlling checksum values must be derived from the exact canonical Drive bytes after upload.

When a connector does not return Drive checksum metadata:

1. Retrieve the exact uploaded Drive file as raw bytes.
2. Calculate SHA-256 as the primary integrity value.
3. Calculate MD5 only as a compatibility value.
4. Compare the downloaded size with the registered size.
5. Record the verification method and date in the source registry.
6. Independently read back the registry row.
7. If a prior checksum was wrong, correct it transparently, preserve a data-quality record, and mark the earlier value superseded rather than silently replacing history.

## Matching rules

- SHA-256 controls exact duplicate identification.
- MD5 is retained only as a compatibility value, not as the primary integrity control.
- Pre-upload and post-upload hashes may be treated as the same only after an exact-byte comparison.
- A filename-and-size match without a SHA-256 match is only a candidate match and requires review.
- Similar filenames are not proof of duplicate content.
- Metadata-modified PDFs may render identically while having different hashes; record them as content-duplicate candidates only after comparison.
- Lakeville agency case and ECTF task-force numbers remain separate linked identifiers.
- BCA application answers and other interview/application narratives are internal reference sources only and cannot serve as public proof.

## Current connector limitation

ChatGPT can open identified files from a connected personal OneDrive account, but Microsoft currently blocks normal full-library Graph search and folder enumeration for personal Microsoft accounts through the SharePoint connector. The local synced-folder inventory is the durable workaround because it can enumerate and hash the entire local OneDrive and iCloud Drive trees.

## Completion gate

A cross-cloud ingestion pass is complete only when:

- every requested cloud root was scanned or listed as an explicit exception
- unreadable and online-only files are documented
- duplicate groups are reviewed
- selected files are copied to the correct Google Drive folders
- new Drive file IDs and links are captured
- exact canonical post-upload Drive bytes are rehashed and registered
- the Career Evidence Master is updated and read back
- related Notion records are updated and read back
- GitHub contains only the reusable workflow, never private manifests or evidence
- no deletion occurs without Troy's separate explicit approval

# OneDrive and iCloud Drive to Google Drive safe copy

This Windows PowerShell workflow inventories and copies locally hydrated cloud
files to a private Google Drive intake folder while preserving source
hierarchy.

Safety defaults:

- dry run unless `-Execute` is explicitly supplied;
- copy only—never move or delete;
- existing files with different bytes are reported as conflicts and never
  overwritten;
- every copied file is verified with SHA-256;
- SHA-256 inventory and status summary are written locally before and during
  transfer;
- cloud-only placeholders are reported and skipped unless
  `-IncludeCloudOnly` is explicitly supplied;
- temporary and incomplete download files are excluded;
- credentials, logs, and detailed manifests are excluded from Git.

## Package contents

- `Cloud-Storage-To-GDrive-Local.ps1` — primary dry-run and safe-copy workflow.
- `.gitignore` — excludes private manifests, logs, CSV output, and local
  credential files.
- `README.md` — setup, execution, privacy, and review instructions.

## Prerequisites

1. Sign in to OneDrive for Windows.
2. Install and sign in to iCloud for Windows, then turn on iCloud Drive.
3. Install and sign in to Google Drive for desktop.
4. In OneDrive and iCloud Drive, pin the folders to keep/download them locally
   before the final run.
5. Confirm the Google Drive destination is owner-only.

The script uses the providers' official Windows sync clients. It does not need
cloud API tokens, a GitHub secret, or a third-party transfer service.

## Dry run

```powershell
Set-ExecutionPolicy -Scope Process Bypass

.\Cloud-Storage-To-GDrive-Local.ps1 `
  -GoogleDriveRoot "G:\My Drive" `
  -DestinationRoot "Career Evidence\00_Source Documents\Cloud Intake"
```

The script automatically looks for the usual local OneDrive and iCloud Drive
folders. If either provider uses a nonstandard location, pass the source roots
explicitly:

```powershell
$sources = @(
  "C:\Users\Troy\OneDrive",
  "C:\Users\Troy\iCloudDrive"
)

.\Cloud-Storage-To-GDrive-Local.ps1 `
  -SourceRoot $sources `
  -GoogleDriveRoot "G:\My Drive"
```

Review the generated CSV and text summary under `private-manifests`. Any
`needs-hydration`, `source-read-error`, or `conflict-different` row requires
review before the copy run.

## Copy

Run the copy only after the dry-run exceptions have been reviewed:

```powershell
.\Cloud-Storage-To-GDrive-Local.ps1 `
  -GoogleDriveRoot "G:\My Drive" `
  -DestinationRoot "Career Evidence\00_Source Documents\Cloud Intake" `
  -Execute
```

The destination contains separate source branches, preventing same-name files
from different providers from colliding. The script does not overwrite a
file whose bytes differ from the source.

## GitHub boundary

The generic script, README, and `.gitignore` may be published. GitHub is not a
document-transfer destination and must not receive private evidence.

Do not commit:

- inventory CSVs or transfer logs;
- source paths that reveal case, court, medical, or personnel information;
- any copied source document;
- Apple, Microsoft, or Google credentials, session cookies, recovery codes,
  OAuth tokens, or local sync configuration.

Dropbox is intentionally not part of the workflow. It should only be added
after a durable personal account and retention rules are confirmed.

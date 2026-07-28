# OneDrive and iCloud Drive to Google Drive safe copy

These Windows PowerShell workflows inventory and copy locally hydrated cloud
files to a private Google Drive intake folder while preserving source
hierarchy.

Safety defaults:

- dry run unless `-Execute` is explicitly supplied;
- copy only—never move or delete;
- existing files with different bytes are reported as conflicts and never
  overwritten;
- every copied file is verified with SHA-256;
- SHA-256 inventory and status summary are written locally before/while
  transfer;
- cloud-only placeholders are reported and skipped unless
  `-IncludeCloudOnly` is explicitly supplied;
- temporary and incomplete download files excluded;
- credentials, logs, and detailed manifests excluded from Git.

## Prerequisites

1. Sign in to OneDrive for Windows.
2. Install and sign in to iCloud for Windows, then turn on iCloud Drive.
3. Install and sign in to Google Drive for desktop.
4. In OneDrive and iCloud Drive, pin the folders to keep/download them locally
   before the final run.
5. Confirm the Google Drive destination is owner-only.

The recommended script is `Cloud-Storage-To-GDrive-Local.ps1`. It uses the
three providers' official Windows sync clients and does not need cloud API
tokens, a GitHub secret, or a third-party transfer service.

## Dry run

```powershell
Set-ExecutionPolicy -Scope Process Bypass

.\Cloud-Storage-To-GDrive-Local.ps1 `
  -GoogleDriveRoot "G:\My Drive" `
  -DestinationRoot "Career Evidence\00_Source Documents\Cloud Intake"
```

The script automatically looks for the usual local OneDrive and iCloud Drive
folders. If either provider uses a nonstandard location, pass both explicitly:

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

```powershell
.\Cloud-Storage-To-GDrive-Local.ps1 `
  -GoogleDriveRoot "G:\My Drive" `
  -DestinationRoot "Career Evidence\00_Source Documents\Cloud Intake" `
  -Execute
```

The destination contains separate `OneDrive` and `iCloud Drive` branches, which
prevents same-name files from the two providers from colliding.

## Optional rclone path

`OneDrive-To-GDrive-Copy.ps1` remains available for a locally hydrated
OneDrive tree when Google Drive for desktop is not installed. It requires an
rclone Google Drive remote named `gdrive`, is dry-run by default, and uses
`copy --immutable`.

```powershell
.\OneDrive-To-GDrive-Copy.ps1 `
  -SourceRoot "$env:OneDriveConsumer" `
  -GoogleDriveRemote "gdrive:" `
  -DestinationRoot "Career Evidence/00_Source Documents/OneDrive Intake"
```

## GitHub boundary

The generic scripts, README, and `.gitignore` may be published. GitHub is not a
document-transfer destination and must not receive private evidence.

Do not commit:

- rclone configuration or OAuth tokens;
- inventory CSVs or transfer logs;
- source paths that reveal case, court, medical, or personnel information;
- any copied source document;
- Apple, Microsoft, or Google credentials, session cookies, or recovery codes.

Dropbox is intentionally not part of the workflow. It should only be added
after a durable personal account and retention rules are confirmed.

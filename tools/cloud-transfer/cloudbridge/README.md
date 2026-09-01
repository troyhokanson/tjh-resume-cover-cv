# CloudBridge CLI

CloudBridge is a copy-only command-line guardrail for inventorying and copying
OneDrive and iCloud Drive files into a private Google Drive destination.

It has two operating paths:

1. **Local mode** reads the official OneDrive/iCloud sync folders and writes to
   Google Drive for desktop. Every readable source file is SHA-256 hashed;
   copied files are hashed again.
2. **Remote mode** controls `rclone` for direct OneDrive/iCloud Drive to Google
   Drive transfers. It permits `copy`, never `sync` or `move`, and forces
   immutable destination behavior.

Runtime dependencies are limited to Python 3.11+. Remote mode also requires
`rclone`.

## Non-negotiable safety behavior

- Dry run is the default.
- No source deletion or move operation exists.
- Existing different-content files are conflicts and are never overwritten.
- Detailed manifests and logs stay local under `private-manifests`.
- Credentials, tokens, evidence, manifests, logs, and source filenames do not
  belong in Git.
- Symlinks and incomplete-download files are skipped in local mode.
- A cloud destination must be below the remote root.

## Install on Troy's Windows computer

From this folder in PowerShell:

```powershell
py -m pip install .
cloudbridge doctor
```

For remote mode, install the current official `rclone` release, then configure
three named remotes:

```powershell
cloudbridge configure
```

Suggested remote names:

- `onedrive` — Microsoft OneDrive Personal
- `icloud` — iCloud Drive
- `gdrive` — the private Google Drive account

Authentication remains in the interactive provider/rclone flow. Do not put an
Apple, Microsoft, or Google password, 2FA code, recovery code, token, or
`rclone.conf` in ChatGPT, a script, a GitHub issue, or a repository.

For iCloud Drive, current rclone releases require the regular Apple Account
password and 2FA; app-specific passwords are not accepted. The trust token
expires periodically. Consider encrypting `rclone.conf` from `rclone config`
and keep the configuration readable only by the Windows user.

## Check what is reachable

```powershell
cloudbridge discover
```

The output contains only detected local roots and configured rclone remote
names. It does not enumerate private filenames.

## Inventory OneDrive and iCloud Drive

```powershell
cloudbridge remote-scan `
  --source "onedrive:" `
  --manifest-dir "$env:LOCALAPPDATA\CloudBridge\private-manifests"

cloudbridge remote-scan `
  --source "icloud:" `
  --manifest-dir "$env:LOCALAPPDATA\CloudBridge\private-manifests"
```

These are read-only commands. The inventories contain private filenames and
must remain outside GitHub.

## Direct remote dry run

```powershell
cloudbridge remote-copy `
  --source "onedrive:" `
  --destination "gdrive:Career Evidence/00_Source Documents/Cloud Intake/OneDrive" `
  --manifest-dir "$env:LOCALAPPDATA\CloudBridge\private-manifests"

cloudbridge remote-copy `
  --source "icloud:" `
  --destination "gdrive:Career Evidence/00_Source Documents/Cloud Intake/iCloud Drive" `
  --manifest-dir "$env:LOCALAPPDATA\CloudBridge\private-manifests"
```

Review both private logs. To perform the same immutable copy, repeat the command
with `--execute`.

```powershell
cloudbridge remote-copy `
  --source "onedrive:" `
  --destination "gdrive:Career Evidence/00_Source Documents/Cloud Intake/OneDrive" `
  --manifest-dir "$env:LOCALAPPDATA\CloudBridge\private-manifests" `
  --execute
```

Remote mode uses rclone's provider-supported integrity checks. Because cloud
providers do not all expose a common SHA-256 hash, it does not claim
end-to-end SHA-256 verification.

## Highest-assurance local copy

Pin OneDrive and iCloud Drive folders as available offline. Use Google Drive
for desktop with a private destination:

```powershell
cloudbridge local-copy `
  --source "OneDrive=$env:OneDriveConsumer" `
  --source "iCloud Drive=$env:USERPROFILE\iCloud Drive" `
  --destination "G:\My Drive\Career Evidence\00_Source Documents\Cloud Intake" `
  --manifest-dir "$env:LOCALAPPDATA\CloudBridge\private-manifests"
```

This is a dry run. Resolve every `needs-hydration`, `source-read-error`, and
`conflict-different` record. Then repeat with `--execute`.

Local mode copies each file with exclusive-create semantics and verifies the
destination bytes with SHA-256. It will not overwrite a file that appears
during the run.

## Exit codes

- `0`: completed without blocking conflicts or errors.
- `2`: configuration problem, conflict, unreadable file, copy failure, or
  rclone failure. Review the private summary and manifest.

## Provider facts

- Microsoft Graph and rclone support delegated access to OneDrive Personal.
- Apple exposes iCloud Drive through iCloud for Windows; current rclone also
  has an iCloud Drive backend with Apple Account + 2FA authentication.
- Google Drive for desktop supports streamed or mirrored files; local
  SHA-256 verification requires files to be readable locally.

Official references:

- <https://learn.microsoft.com/en-us/graph/api/driveitem-list-children>
- <https://support.apple.com/guide/icloud-windows/set-up-icloud-drive-icw0144825a5/icloud>
- <https://support.google.com/drive/answer/13401938>
- <https://rclone.org/iclouddrive/>
- <https://rclone.org/onedrive/>
- <https://rclone.org/drive/>

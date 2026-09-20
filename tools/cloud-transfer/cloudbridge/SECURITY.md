# Security

## Data boundary

CloudBridge source code may be public. Its runtime data must remain private.

Never commit or upload:

- source documents or copied evidence;
- file inventories, transfer logs, or manifests;
- `rclone.conf`, OAuth tokens, cookies, trust tokens, or recovery codes;
- Apple, Microsoft, Google, Proton, or 1Password credentials;
- screenshots or terminal captures containing private filenames.

## Authentication

CloudBridge does not collect, store, transmit, or log provider credentials. The
`configure` command only opens rclone's own interactive configuration. Enter
credentials and 2FA codes directly into that local flow.

Rclone configuration commonly contains tokens or login information. Restrict
its filesystem permissions and use rclone's configuration encryption option.
Do not assume an obscured value is encrypted.

## Transfer guarantees

Local mode:

- opens destination files with exclusive-create semantics;
- does not follow directory symlinks;
- never deletes or moves source files;
- never overwrites an existing destination;
- computes SHA-256 before and after each completed local copy.

Remote mode:

- invokes `rclone copy`, never `sync` or `move`;
- forces `--immutable`;
- defaults to `--dry-run`;
- relies on the strongest integrity checks shared by the selected providers;
- does not claim end-to-end SHA-256 when providers do not expose a common hash.

## Reporting a vulnerability

Do not open a public issue containing filenames, credentials, account
identifiers, logs, or evidence. Report only a minimal, redacted reproduction.

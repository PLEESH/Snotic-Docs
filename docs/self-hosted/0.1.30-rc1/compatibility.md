# Compatibility and Known Limitations

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

## Supported matrix

| Platform | Architecture | Clean install | Upgrade from 0.1.29 | Reinstall | Rollback and re-upgrade |
| --- | --- | --- | --- | --- | --- |
| Ubuntu 22.04 LTS | amd64 | Validated | Validated | Validated | Validated within schema v1 |
| Ubuntu 24.04 LTS | amd64 | Validated | Validated | Validated | Validated within schema v1 |

ARM64, other Linux distributions, shared hosting, container-only application
deployment, and an existing conflicting web/database stack are not supported by
this release.

## Preserved identifiers

The Snotic public name does not rename the installed compatibility surface.
This release preserves:

- package and CLI name `hipanel`;
- existing systemd units and installed paths;
- configuration keys and schema version 1;
- SQLite metadata and authentication state;
- sessions and scoped API keys;
- backup metadata, formats, registries, encryption keys, and restore behavior;
- API routes and scopes; and
- package ordering and release history.

Do not replace `hipanel` with `snotic` in commands or paths.

## Upgrade and rollback limits

The declared minimum source package is `0.1.29`. Same-version reinstall is
supported and preserves state. Package rollback to `0.1.29` is declared only
while configuration and application data remain readable and writable at
schema version 1.

A package rollback does not undo changes made to WordPress, MariaDB, Nginx,
DNS, certificates, or external storage. Take a verified encrypted backup and
independent host snapshot before package changes.

## Early Access limits

- The distribution is supplied privately to approved recipients and is not a
  public download.
- The core application is not represented as open source.
- There is no automatic update, public APT promotion, SLA, managed monitoring,
  customer portal, payment, or software expiry.
- S3 is optional and non-EC2 use may require customer-managed static AWS
  credentials.
- Snotic Site Exporter is a controlled-pilot build. Its PHP fallback does not
  claim live-write consistency.
- The customer remains responsible for server security, DNS, TLS, capacity,
  updates, backups, restore testing, and incidents.

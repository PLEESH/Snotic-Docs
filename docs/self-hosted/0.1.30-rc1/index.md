# Snotic Self-Hosted 0.1.30~rc1

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

Snotic Self-Hosted is a WordPress server-management panel supplied by Pleesh
for operation on infrastructure the customer owns or controls.

This release provides:

- a browser panel for one local administrator;
- WordPress site creation, inspection, TLS, isolation, and deletion workflows;
- Snotic Site Exporter migration and compatible archive import;
- encrypted local backup, preview, restore, and optional S3 sync;
- host capacity and operational status views;
- scoped API keys for automation;
- optional TOTP MFA and recovery codes; and
- signed Debian artifacts for Ubuntu 22.04 and 24.04 LTS on amd64.

## Compatibility names

Snotic is the public product name. Version `0.1.30~rc1` deliberately retains:

- Debian package `hipanel`;
- CLI `hipanel` at `/opt/hipanel/bin/hipanel`;
- `hipanel` systemd services and timers;
- configuration under `/etc/hipanel`;
- state under `/var/lib/hipanel`;
- backups under `/var/backups/hipanel`; and
- logs under `/var/log/hipanel`.

There is no `snotic` package or CLI alias in this release.

## Start here

1. Confirm the [server requirements and responsibilities](requirements.md).
2. [Obtain and verify](obtain-and-verify.md) the complete supplied distribution.
3. Run the read-only preflight, then follow the
   [installation procedure](install.md).
4. Configure [secure access, HTTPS, and optional MFA](access-and-security.md).
5. [Create or manage WordPress sites](sites.md).
6. Establish [encrypted backups and a tested recovery path](backups-and-recovery.md).

Read the [release notes](release-notes.md),
[known limitations](compatibility.md), [use terms](use-terms.md), and
[third-party notices](third-party-notices.md) before installation.

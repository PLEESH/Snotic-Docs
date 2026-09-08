# Release Notes

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

## Identity

| Field | Value |
| --- | --- |
| Source commit | `7a0e9104e3eaed6290e0f29d78d5c12384b14084` |
| Built at | `2026-09-08T00:49:51Z` |
| Debian package | `hipanel` |
| Channel | Candidate |
| Offering | Snotic Self-Hosted by Pleesh |

This is a privately distributed Early Access candidate for an approved
recipient's customer-controlled Ubuntu server. It is not Snotic Managed, a
public beta, or a stable-channel promotion. There is no Portal activation,
payment method, subscription, or seven-day software expiry.

## Included

- The existing `hipanel` package, CLI, services, paths, API, state, auth,
  backup, migration, and encryption-key compatibility.
- Browser-visible Snotic Self-Hosted product naming.
- Unique host secret and backup-encryption keys created during installation.
- Local encrypted backup and real restore without AWS or S3.
- Optional S3 operation through static credentials or an EC2 instance role.
- Snotic Site Exporter `0.2.0-pilot.2` with its GPL-2.0-or-later material.
- Read-only host preflight, installation/recovery guidance, SBOM, schemas,
  checksums, detached signatures, and public verification key.

## Verification identity

- Package SHA-256:
  `becfff27cae7e8c8bc9edb2eae629ec873e8a555d83d05d77cf8dee16658aa3e`
- Owner handoff SHA-256:
  `2ca1f61225d85d53ac969456deb181e5cb185b7a4d0cb63b6a16843102485456`
- Signing fingerprint:
  `26BAEB9BC68C2AB633FD6B822473AD1517C2A642`

Follow [Obtain and verify](obtain-and-verify.md) rather than relying on this
summary alone.

## Validation status

Final package install, reinstall, upgrade from `0.1.29`, rollback, re-upgrade,
health, and populated-state preservation passed in systemd-enabled Ubuntu
22.04 and 24.04 amd64 LXD system containers. The release remains Early Access,
and the actual recipient host must still pass the supplied preflight.

## Important limitations

- One local Snotic administrator.
- Ubuntu 22.04/24.04 LTS on amd64 only.
- Fresh/minimal host or supported existing `hipanel` upgrade.
- No Snotic Managed policy, Pleesh AWS dependency, billing, public package
  channel, SLA, ARM64 support, or automatic host/DNS/firewall management.
- PHP exporter fallback requires a quiesced source for first-client use.

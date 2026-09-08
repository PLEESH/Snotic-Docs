# Application Architecture

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

Snotic Self-Hosted is a single-server WordPress management application. It is
not dependent on Pleesh AWS access, Snotic Managed account vending, or a Pleesh
control plane.

```text
Administrator browser
        |
     HTTPS
        |
      Nginx
        |
  127.0.0.1:8080
        |
  hipanel.service
    |     |      |
 SQLite  local  privileged helper
 state   backups     |
                   Nginx, PHP-FPM, MariaDB, WordPress, Certbot
```

## Components

- `hipanel.service` runs the Go application as the unprivileged `hipanel`
  account and listens on loopback by default.
- Nginx terminates public HTTP/HTTPS and proxies the panel to loopback.
- A typed privileged-helper path performs bounded host mutations for site,
  database, web, certificate, and backup operations.
- SQLite in WAL mode stores application metadata and authentication state.
- MariaDB stores each managed WordPress database.
- Per-site PHP-FPM and Nginx configuration serves WordPress sites.
- `hipanel-backup.timer` starts scheduled encrypted backups.
- `hipanel-ops-alert.timer` evaluates health and optional notifications.
- Local encrypted archives are primary Self-Hosted backups; S3 is optional.

## Installed boundaries

| Purpose | Path |
| --- | --- |
| Executables | `/opt/hipanel/bin` |
| Configuration and encryption keys | `/etc/hipanel` |
| Metadata and runtime state | `/var/lib/hipanel` |
| Encrypted backups | `/var/backups/hipanel` |
| Logs and audit log | `/var/log/hipanel` |
| WordPress site roots | `/var/www/<domain>` |

The secret key encrypts stored application settings and site database
credentials. The separate backup key encrypts backup archives. Losing either
key can make retained encrypted data unrecoverable.

## Security boundary

The package does not alter SSH, firewall, cloud, or DNS policy. The customer
owns server hardening, network exposure, DNS, TLS, updates, monitoring,
off-server backup copies, and incident response. Keep port 8080 private, use
HTTPS for ordinary browser access, and do not grant the service general root or
cloud administration.

The browser uses signed server-side sessions and CSRF protection. Automation
uses revocable scoped API keys. Site Exporter tokens are one-time, short-lived
migration credentials and are not general API keys.

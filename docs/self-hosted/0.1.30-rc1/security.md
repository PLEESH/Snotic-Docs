# Security and Contact

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

## Security baseline

- Keep `hipanel.service` on `127.0.0.1:8080` behind reviewed Nginx HTTPS.
- Restrict SSH and `sudo` to authorized administrators.
- Enable MFA and preserve recovery codes in an approved password manager.
- Use short-lived, least-privilege API keys and revoke unused keys.
- Keep legacy bearer-token authentication and `open_dev_mode` disabled.
- Protect `/etc/hipanel`, `/var/lib/hipanel`, backups, database dumps, and
  WordPress exports.
- Keep Ubuntu, Snotic, Nginx, PHP, MariaDB, Certbot, and WordPress components
  patched through verified sources.
- Monitor logs, capacity, certificate expiry, backup freshness, and restore
  results.
- Preserve the secret and backup keys off server through an approved encrypted
  process.

The package does not configure the host firewall, SSH, cloud account, or DNS.
Those controls remain the customer's responsibility.

## Report a vulnerability

Do not open a public issue for a suspected vulnerability. Email
`github@pleesh.com` with:

- the affected Snotic/`hipanel` version;
- sanitized reproduction steps;
- expected security impact; and
- a safe contact method.

Do not include passwords, private keys, API keys, recovery codes, cookies,
database URLs, customer data, export archives, raw logs containing sensitive
data, or backup-encryption keys.

Test only systems you own or have explicit permission to assess. Pleesh will
acknowledge the report, investigate it, and coordinate remediation and
disclosure according to severity.

## Operational compromise

Preserve evidence and verified backups, restrict affected access where
practical, revoke credentials proven to be exposed, and follow the
[incident procedure](monitoring-and-incidents.md). Do not destroy the original
host or rotate encryption keys before confirming that required data and
recovery material remain available.

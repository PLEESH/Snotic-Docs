# Monitoring and Incident Response

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

The customer is responsible for monitoring and incident response. The package
provides local signals and an optional webhook; it does not provide a managed
24-hour response service.

## Daily operating checks

```shell
curl --fail --silent --show-error http://127.0.0.1:8080/healthz
curl --fail --silent --show-error http://127.0.0.1:8080/readyz
sudo /opt/hipanel/bin/hipanel ops check -summary
sudo systemctl --failed
sudo systemctl list-timers hipanel-backup.timer hipanel-ops-alert.timer
```

Monitor at least:

- process liveness and application readiness;
- root-disk capacity and inode capacity;
- memory and sustained load;
- backup freshness, encryption, and real restore results;
- S3 verification when optional S3 is enabled;
- TLS hostname, trust, expiry, and renewal;
- failed or unusually frequent audited mutations;
- systemd service/timer failures; and
- pending operations that do not reach a terminal state.

Test the chosen off-host notification destination. A configured timer without
a reachable recipient is not an alerting system.

## Relevant logs

```shell
sudo journalctl -u hipanel.service --since "30 minutes ago"
sudo journalctl -u hipanel-backup.service --since "24 hours ago"
sudo journalctl -u hipanel-ops-alert.service --since "24 hours ago"
sudo tail -n 100 /var/log/hipanel/audit.log
```

Sanitize evidence before sharing it. Do not publish configuration files,
cookies, API keys, database dumps, export archives, recovery codes, or key-file
contents.

## Incident procedure

1. Preserve timestamps, bounded logs, current state, and available backups.
2. If compromise is plausible, restrict external access without deleting the
   host or evidence.
3. Revoke exposed API keys and browser sessions; rotate credentials proven to
   be exposed.
4. Confirm the exact installed package and configuration state.
5. Verify encrypted backup integrity and key availability before destructive
   repair.
6. Restore on a replacement compatible host when the original host cannot be
   trusted.
7. Validate authentication, site content, TLS, backup, and monitoring after
   recovery.
8. Record the cause, scope, recovery, and follow-up without including secrets.

Do not run a real restore, key rotation, package rollback, or site deletion
merely to diagnose an alert. Use preview and read-only checks first.

Report a suspected product vulnerability according to the
[security guidance](security.md). Test only systems you own or are explicitly
authorized to assess.

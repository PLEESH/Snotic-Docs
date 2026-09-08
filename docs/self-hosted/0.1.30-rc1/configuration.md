# Configuration Reference

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

The package configuration is `/etc/hipanel/config.json`. The package and CLI
retain the `hipanel` name for compatibility. Back up the file and both key
files before changing configuration.

## Edit and validate safely

Use an authorized root session. Do not print the file into tickets or logs: it
can contain an alert URL and legacy credentials.

```shell
sudoedit /etc/hipanel/config.json
sudo python3 -m json.tool /etc/hipanel/config.json >/dev/null
sudo systemctl restart hipanel.service
curl --fail --silent --show-error http://127.0.0.1:8080/readyz
```

All supported settings in this release require a service restart. A changed
configuration is also reported in **Ops** until the service reloads it.

## Runtime and storage

| Key | Packaged value or default | Purpose |
| --- | --- | --- |
| `listen_addr` | `127.0.0.1:8080` | Local HTTP listener behind Nginx. Keep it on loopback. |
| `data_dir` | `/var/lib/hipanel` | Application state. |
| `metadata_store_path` | `/var/lib/hipanel/metadata.sqlite` | SQLite metadata and authentication store. |
| `auth_store_path` | `/var/lib/hipanel/auth.json` | Legacy authentication import path. |
| `backups_dir` | `/var/backups/hipanel` | Local backup root. |
| `isolation_rollback_dir` | `/var/backups/hipanel-release-state/isolation-migrations` | Protected site-isolation rollback bundles. |
| `backup_retention` | `7` | Retained backups per site. `0` disables pruning. |
| `command_timeout_seconds` | `1800` | Bound for external provisioning and backup commands. |

## Keys and sensitive settings

| Key | Packaged value | Handling |
| --- | --- | --- |
| `backup_encryption_key_file` | `/etc/hipanel/backup.key` | Required to decrypt local and S3 backup archives. |
| `secret_key_file` | `/etc/hipanel/secrets.key` | Required to decrypt stored settings and site database credentials. |
| `api_token` | empty | Deprecated legacy bearer secret. Do not enable for new automation. |
| `legacy_api_token_enabled` | `false` | Keep disabled; use scoped API keys. |
| `open_dev_mode` | `false` | Never enable on a non-loopback listener. |
| `ops_alert_webhook_url` | empty | Optional secret notification endpoint. |

Do not replace either key file when encrypted state must remain recoverable.
Key rotation is a separate, destructive operation with its own confirmation
and recovery requirements.

## Optional S3

| Key | Default | Purpose |
| --- | --- | --- |
| `s3_bucket` | empty | Destination bucket name. |
| `s3_prefix` | empty | Suffix below the fixed `HiPanel/` namespace. |
| `s3_credential_mode` | `static` | `static` or `instance-role`. |
| `s3_region` | empty | AWS Region containing the bucket. |

See [Optional S3 storage](s3.md) before setting these fields.

## Operations thresholds

| Key | Default |
| --- | ---: |
| `ops_alert_state_file` | `/var/lib/hipanel/ops-alert-state.json` |
| `ops_alert_repeat_seconds` | `21600` |
| `ops_alert_min_status` | `warn` |
| `ops_backup_max_age_hours` | `30` |
| `ops_backup_critical_age_hours` | `72` |
| `ops_certificate_warning_days` | `30` |
| `ops_certificate_critical_days` | `7` |
| `ops_disk_warning_used_percent` | `80` |
| `ops_disk_critical_used_percent` | `90` |
| `ops_disk_warning_free_mib` | `2048` |
| `ops_disk_critical_free_mib` | `1024` |
| `ops_audit_window_hours` | `24` |
| `ops_audit_burst_window_minutes` | `15` |
| `ops_audit_failure_warning` | `5` |
| `ops_audit_mutation_burst_warning` | `20` |

Review thresholds against the server's capacity and operating model. A default
is not a substitute for tested notification delivery and an incident owner.

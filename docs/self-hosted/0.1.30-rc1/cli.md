# CLI Reference

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

The installed entry point is `/opt/hipanel/bin/hipanel`. Commands that inspect
or mutate protected state normally require `sudo`.

## Command families

| Command | Purpose |
| --- | --- |
| `serve` | Run the local HTTP service. The package manages this with systemd. |
| `sites` | List, create, delete, isolate, back up, and restore sites. |
| `auth` | Initialize/reset the local admin and manage scoped API keys. |
| `ops` | Inspect operational status and optionally send an alert. |
| `token` | Rotate the deprecated service API token. |
| `backup-key` | Initialize the backup-encryption key. |
| `secret-key` | Rotate the local settings/database-credential encryption key. |
| `recovery` | Bootstrap an empty host from configured S3 state. |
| `version` | Print build identity as JSON. |

Use the built-in help from the exact installed release before an unfamiliar
operation:

```shell
sudo /opt/hipanel/bin/hipanel help
sudo /opt/hipanel/bin/hipanel sites -h
sudo /opt/hipanel/bin/hipanel auth api-key -h
```

## Read-only checks

```shell
sudo /opt/hipanel/bin/hipanel version
sudo /opt/hipanel/bin/hipanel sites list
sudo /opt/hipanel/bin/hipanel sites backups -domain example.com
sudo /opt/hipanel/bin/hipanel ops check -summary
```

Add `-require-s3-verified` to `sites backups` only when S3 is configured and a
failed live remote listing should make the command fail.

## Site operations

```shell
sudo /opt/hipanel/bin/hipanel sites backup -domain example.com
sudo /opt/hipanel/bin/hipanel sites backup-all
sudo /opt/hipanel/bin/hipanel sites restore -domain example.com -dry-run
sudo /opt/hipanel/bin/hipanel sites isolate
```

Site creation, real restore, isolation apply, and deletion can change the host.
Follow the preview, backup, and exact-confirmation procedures in
[Manage WordPress sites](sites.md) and
[Encrypted backups and recovery](backups-and-recovery.md).

## Scoped API keys

Create a short-lived key with only the required scopes:

```shell
sudo /opt/hipanel/bin/hipanel auth api-key create -name inventory-reader -scopes sites:read,system:read -expires-in 24h
```

The plaintext key appears only in the create or rotate result. Store it in an
approved secret manager and do not put command output in logs or tickets.

```shell
sudo /opt/hipanel/bin/hipanel auth api-key list
sudo /opt/hipanel/bin/hipanel auth api-key rotate -id <key-id>
sudo /opt/hipanel/bin/hipanel auth api-key revoke -id <key-id>
```

Available ordinary scopes are listed in the [API reference](api.md). The `*`
and `admin` meta-scopes grant every ordinary API scope and should not be used
when a narrower key works.

## Destructive recovery commands

!!! danger
    The following operations require a separate recovery plan, current backup,
    preserved keys, and exact confirmation. Do not use them as diagnostics.

```shell
sudo /opt/hipanel/bin/hipanel secret-key rotate -config /etc/hipanel/config.json -confirm rotate-secrets
sudo /opt/hipanel/bin/hipanel recovery bootstrap -config /etc/hipanel/config.json -confirm restore-from-s3
```

`recovery bootstrap` refuses non-empty or previously restored state unless
`-force` is supplied. Treat `-force` as a second destructive approval.

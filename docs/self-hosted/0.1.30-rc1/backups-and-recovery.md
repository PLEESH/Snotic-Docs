# Encrypted Backups and Recovery

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

The Self-Hosted package enables a unique local backup-encryption key. Local
encrypted backup and restore work without AWS or S3.

## Create and inspect backups

```shell
sudo /opt/hipanel/bin/hipanel sites backup -domain example.com
sudo /opt/hipanel/bin/hipanel sites backups -domain example.com
sudo /opt/hipanel/bin/hipanel sites backup-all
```

The daily `hipanel-backup.timer` runs the packaged backup service. Verify timer
health and the resulting artifacts rather than relying only on its schedule:

```shell
sudo systemctl status hipanel-backup.timer
sudo systemctl list-timers hipanel-backup.timer
```

In the browser, **Create Backup**, **Backup & Sync All**, and **Backup History**
show operation progress and local/S3 status. An S3 status of **unknown** means
the live remote listing failed; it is not proof that an object is present or
absent.

## Preserve recovery material off server

Store protected, encrypted copies of:

- `/etc/hipanel/config.json`;
- `/etc/hipanel/secrets.key`;
- `/etc/hipanel/backup.key`;
- `/var/lib/hipanel`;
- `/var/backups/hipanel`;
- site roots under `/var/www`;
- Nginx and PHP-FPM site configuration;
- MariaDB data or consistent dumps; and
- certificate state.

The backup key is required to decrypt encrypted backups. The secret key is
required to recover encrypted settings and site database credentials. Preserve
their original ownership and permissions and never paste their contents into
chat, tickets, email, or documentation.

## Preview before restore

Preview the latest local backup:

```shell
sudo /opt/hipanel/bin/hipanel sites restore -domain example.com -dry-run
```

Preview a named archive:

```shell
sudo /opt/hipanel/bin/hipanel sites restore -domain example.com -path example.com-20260908T010000Z.tar.gz.enc -dry-run
```

The preview checks archive safety and expected WordPress content without
changing the site.

## Perform a real restore

!!! danger
    A real restore replaces current site files and database state. Take a
    separate current backup, retain the matching keys, review the preview, and
    confirm the target domain before proceeding.

```shell
sudo /opt/hipanel/bin/hipanel sites restore -domain example.com -path example.com-20260908T010000Z.tar.gz.enc
```

In the browser, select **Preview** for the exact Backup History entry, then
select **Restore** and type the target domain. Uploaded `.tar.gz`, `.tgz`, and
`.tar.gz.enc` files also require **Preview File** before **Restore From File**.

After restoration, verify:

```shell
curl --fail --silent --show-error http://127.0.0.1:8080/healthz
curl --fail --silent --show-error http://127.0.0.1:8080/readyz
sudo /opt/hipanel/bin/hipanel sites list
sudo /opt/hipanel/bin/hipanel sites backups -domain example.com
```

Also verify browser login, WordPress login, representative content, TLS, and a
new post-restore backup.

## Recover onto a replacement host

1. Provision a compatible fresh Ubuntu 22.04 or 24.04 amd64 server.
2. Verify and install the same package version.
3. Stop `hipanel.service`.
4. Restore the preserved configuration, both keys, application state, site
   content, databases, backups, web configuration, and certificates with their
   original ownership and modes.
5. Start the service and run health, readiness, authentication, site, TLS, and
   real restore checks.

Do not generate replacement keys when encrypted data must remain recoverable.
Schedule recurring real restore drills; an archive that has never been restored
is not sufficient recovery evidence.

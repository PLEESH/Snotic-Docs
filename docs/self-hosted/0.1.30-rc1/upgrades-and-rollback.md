# Reinstall, Upgrade, and Rollback

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

Every package change requires a maintenance window, current encrypted backup,
independent host snapshot, sufficient disk/inode capacity, and verification of
the exact new distribution.

## Same-version reinstall

```shell
sudo apt-get install --yes --reinstall ./hipanel_0.1.30~rc1_amd64.deb
```

The release contract declares same-version reinstall with preserved state.
Verify the exact configuration, keys, authentication, sites, backups, services,
and health after reinstall.

## Upgrade

Version `0.1.30~rc1` supports in-place upgrade from package `0.1.29`. For a
later package supplied by Pleesh, verify that release's own signatures,
checksums, manifest, compatibility range, and rollback declaration before use.

```shell
sudo apt-get install --yes ./hipanel_0.1.31_amd64.deb
```

Do not infer an upgrade path from a filename alone. This Early Access handoff
does not configure a public APT repository or automatic stable promotion.

## Rollback boundary

The rc1 contract declares package rollback to `0.1.29` only while configuration
and application data remain readable and writable at schema version 1.

!!! danger
    A package downgrade does not reverse external WordPress, database, DNS, or
    certificate changes. Restore the pre-upgrade snapshot when a changed schema
    or incomplete operation makes package-only rollback unsafe.

```shell
sudo apt-get install --yes --allow-downgrades ./hipanel_0.1.29_amd64.deb
```

## Post-change verification

```shell
sudo systemctl status hipanel.service hipanel-backup.timer hipanel-ops-alert.timer
curl --fail --silent --show-error http://127.0.0.1:8080/healthz
curl --fail --silent --show-error http://127.0.0.1:8080/readyz
sudo /opt/hipanel/bin/hipanel version
sudo /opt/hipanel/bin/hipanel sites list
sudo /opt/hipanel/bin/hipanel ops check -summary
```

Also test browser authentication, MFA state, API keys, site access, TLS, backup
listing, one new encrypted backup, and a real restore in an approved drill.

Final-byte integration testing for rc1 used systemd-enabled LXD system
containers on Ubuntu 22.04 and 24.04 amd64. These were containers, not virtual
machines. The customer must still run the supplied preflight and this guide on
the actual target host.

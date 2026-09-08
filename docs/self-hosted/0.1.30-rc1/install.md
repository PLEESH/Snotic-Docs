# Preflight and Installation

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

Complete [distribution verification](obtain-and-verify.md) first. Run these
steps on the intended server through an authorized administrative session.

## Run the read-only preflight

From the verified release directory:

```shell
python3 ./snotic-self-hosted-preflight.py
```

The preflight checks the Ubuntu release, architecture, systemd, capacity,
package state, existing listeners, and conflicting software. It does not stop
services or change SSH, firewall, DNS, or virtual hosts.

!!! warning
    Stop when the result is `BLOCKED`. Resolve and review the reported host
    conflict before making package changes.

## Install the package

```shell
sudo apt-get update
sudo apt-get install --yes ./hipanel_0.1.30~rc1_amd64.deb
```

Dependencies come from the server's configured Ubuntu repositories. The package
generates unique local secret and backup-encryption keys. It contains no shared
administrator password, preinitialized database, reusable token, or private
signing key.

## Verify activation

```shell
sudo systemctl status hipanel.service hipanel-backup.timer hipanel-ops-alert.timer
curl --fail --silent --show-error http://127.0.0.1:8080/healthz
curl --fail --silent --show-error http://127.0.0.1:8080/readyz
sudo /opt/hipanel/bin/hipanel version
```

Expected health responses use service identity `hipanel`. `/healthz` proves the
process is alive; `/readyz` also checks the metadata and authentication stores.
A failed readiness check returns HTTP 503 without exposing paths or errors.

## Initialize the administrator

Create a temporary password file without placing the password in shell history
or process arguments:

```shell
sudo install -m 0600 -o root -g root /dev/null /root/snotic-admin-password
sudo sh -c 'umask 077; python3 -c "import secrets; print(secrets.token_urlsafe(32))" > /root/snotic-admin-password'
sudo /opt/hipanel/bin/hipanel auth init-admin -config /etc/hipanel/config.json -username admin -password-file /root/snotic-admin-password
```

Read it only in a private administrator terminal, store it in the customer's
approved password manager, then remove the temporary file:

```shell
sudo cat /root/snotic-admin-password
sudo rm -f /root/snotic-admin-password
```

MFA is disabled by default. Enable it later from the browser Security page so
the administrator can scan the QR code and record the recovery codes.

Continue with [secure panel access and HTTPS](access-and-security.md).

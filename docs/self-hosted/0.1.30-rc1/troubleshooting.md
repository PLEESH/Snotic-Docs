# Troubleshooting

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

## Service or readiness failure

```shell
sudo systemctl status hipanel.service
sudo journalctl -u hipanel.service --since "30 minutes ago"
curl --include http://127.0.0.1:8080/healthz
curl --include http://127.0.0.1:8080/readyz
```

- `/healthz` failing usually means the service is not listening.
- `/readyz` returning 503 means the metadata or authentication store is not
  ready.
- Keep error reports sanitized. Do not send configuration, key files, raw
  exports, database dumps, or credentials.

## Browser redirects to login

The session may have expired. Sign in again at `/login`. Do not append a token
to `/ui` or any browser URL.

## An action appears stuck

Record the operation ID and inspect **Ops** before retrying. A failed progress
poll does not prove that the server-side job stopped.

## Site is missing

Refresh the **Sites** view, then verify the CLI inventory:

```shell
sudo /opt/hipanel/bin/hipanel sites list
```

## TLS reports no while the browser is secure

Refresh Site Details and inspect certificate status under **Ops**. Validate and
reload Nginx if its configuration changed outside Snotic:

```shell
sudo nginx -t
sudo systemctl reload nginx
```

## Certificate issuance fails

Confirm that the exact domain resolves publicly to the server, ports 80 and 443
are reachable, and the intended Nginx server block is enabled. Inspect the
bounded Snotic operation result and Certbot service logs without publishing
private host data.

## Backup is not verified in S3

Check **Backup History**, **Storage**, and **Ops**. An S3 status of **unknown**
means the live listing failed. Test connection again after checking AWS CLI,
Region, credential mode, bucket policy, and the effective case-sensitive
`HiPanel/<suffix>/` prefix.

## MFA device is unavailable

Use one unused recovery code. If no code remains, an authorized server
administrator must reset access through the documented root recovery procedure.

## Ask for help safely

Report the affected version, sanitized reproduction steps, expected result, and
actual result through the agreed Pleesh channel or `github@pleesh.com`. Never
include passwords, API keys, private keys, MFA recovery codes, WordPress export
archives, customer content, or raw backup-encryption keys.

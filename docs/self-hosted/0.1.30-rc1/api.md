# HTTP API Reference

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

Version `0.1.30~rc1` exposes an unversioned, compatible v1 HTTP API. Keep the
service on loopback and access it through the reviewed HTTPS reverse proxy.

## Authentication

`GET /healthz` and `GET /readyz` are unauthenticated. Other API operations use
a signed browser session or a scoped API key. Send an API key as a bearer
credential:

```shell
curl --fail --silent --show-error \
  --header "Authorization: Bearer ${SNOTIC_API_KEY}" \
  https://panel.example.com/version
```

Never place a key in a URL. Legacy `api_token` bearer authentication is
disabled by default and deprecated for this release.

## Health contract

| Method and path | Authentication | Result |
| --- | --- | --- |
| `GET /healthz` | None | HTTP 200 with `status=ok` and `service=hipanel` when the process is alive. |
| `GET /readyz` | None | HTTP 200 when metadata and auth stores are ready; HTTP 503 otherwise. |
| `GET /version` | `system:read` | Build and package identity. |

Health responses do not expose errors, paths, state, or credentials.

## API routes and scopes

| Method and route | Required scope | Purpose |
| --- | --- | --- |
| `GET /system/capacity` | `system:read` | Current disk, memory, and load status. |
| `GET /system/ops` | `system:read` | Consolidated operational status. |
| `GET /system/operations` | `system:read` | Recent operations. |
| `GET /system/operations/<operation-id>` | `system:read` | One operation. |
| `POST /system/operations/<operation-id>/cancel` | `system:write` | Request cancellation. |
| `GET /sites` | `sites:read` | List sites. |
| `POST /sites` | `sites:write` | Create or register a site. |
| `GET /sites/<domain>` | `sites:read` | Read one site. |
| `DELETE /sites/<domain>` | `sites:delete` | Preview or confirm site deletion. |
| `GET /sites/<domain>/backups` | `backups:read` | List backup history. |
| `GET /sites/<domain>/backups/download/<backup-name>` | `backups:read` | Download an authorized backup. |
| `POST /sites/<domain>/backups` | `backups:create` | Create a backup. |
| `POST /sites/<domain>/backups/delete/<backup-name>` | `backups:delete` | Delete a selected backup. |
| `POST /sites/<domain>/restore` | `backups:restore` | Preview or perform a restore. |
| `POST /sites/<domain>/wp-password` | `wordpress:write` | Reset a WordPress admin password. |
| `POST /sites/<domain>/cert` | `certs:write` | Request a certificate. |
| `POST /backups/all` | `backups:create` | Back up all sites. |
| `GET /settings/aws` | `settings:read` | Read redacted S3 settings. |
| `POST /settings/aws` | `settings:write` | Save S3 settings. |
| `POST /settings/aws/probe` | `settings:write` | Test bounded S3 operations. |
| `GET /settings/info` | `settings:read` | Read configuration status. |
| `POST /migrations/wp-import` | `migrations:write` | Import through Snotic Site Exporter. |

Browser-only password and MFA routes require a browser session and are not API
key automation endpoints.

## Scope inventory

The ordinary scopes are:

```text
system:read
system:write
sites:read
sites:write
sites:delete
backups:read
backups:create
backups:restore
backups:delete
settings:read
settings:write
certs:write
wordpress:write
migrations:write
```

Namespace wildcards such as `sites:*` grant matching scopes. The `*` and
`admin` meta-scopes grant all ordinary scopes. Prefer exact ordinary scopes,
short expiry, separate keys per integration, and immediate revocation when a
key is no longer needed.

## Mutation safety

Many writes are asynchronous and return an operation ID. Follow the operation
to a terminal state before retrying. Site deletion and restore require their
documented preview and confirmation fields. Treat backup downloads, migration
archives, and one-time generated credentials as sensitive data.

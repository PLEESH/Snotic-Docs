# Migrate with Snotic Site Exporter

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

Snotic Site Exporter `0.2.0-pilot.2` is included in the verified distribution.
It is provided by Pleesh under `GPL-2.0-or-later` and remains compatible with
the `hipanel-migrator-v1` import format.

The plugin is an unpublished controlled-pilot build. Do not obtain it from an
unverified third party or submit it to WordPress.org.

## Understand the data boundary

An export contains the complete WordPress files and database. It can include
users, personal information, private content, uploads, and plugin-held
credentials.

- The plugin contains no telemetry.
- It does not initiate a transfer on its own.
- It creates data only in response to an administrator action and an
  authenticated export request.
- Temporary artifacts are protected and cleaned after use; scheduled cleanup
  removes stale artifacts.
- A one-time token expires after 15 minutes and is consumed by the first
  request, including a failed or interrupted request.

Treat the token and archive as secrets. Do not place the token in a URL, log,
ticket, chat, or command history.

## Install on the source site

1. In WordPress, open **Plugins > Add New > Upload Plugin**.
2. Upload `snotic-site-exporter_0.2.0-pilot.2.zip` from the verified release.
3. Activate **Snotic Site Exporter**.
4. Open **Tools > Snotic Site Exporter** as a WordPress administrator.
5. Read the displayed privacy and transfer warning.

## Prepare a consistent export

The exporter first attempts `mysqldump`. When process execution is unavailable,
it uses a bounded-memory PHP fallback.

For first-client use:

- use the consistent `mysqldump` path; or
- place the source site in maintenance/quiesced mode before using the PHP
  fallback.

Live-site consistency is not claimed for the PHP fallback. Prevent writes until
the receiving import and content checks are complete.

## Issue the one-time token

1. Make the receiving Snotic import form ready first.
2. Select **Issue One-Time Export Token**.
3. Record the displayed HTTPS Export URL and token in a protected temporary
   location.
4. Note the UTC expiry time.

The source URL must use HTTPS on port 443 and resolve entirely to public
internet addresses. The importer rejects URL credentials, plain HTTP, private
or reserved destinations, mixed public/private DNS answers, cross-host
redirects, and exports larger than 2 GiB.

## Import into Snotic

1. Open **Create Site > Import From WordPress Plugin**.
2. Enter the target domain and WordPress administrator details.
3. Enter the source Export URL and one-time token.
4. Start the import once and follow its operation ID to completion.
5. If the request fails, issue a new token before retrying.

The importer validates the complete archive digest, manifest, and
`SHA256SUMS`. The export contains `db.sql`,
`hipanel-export-manifest.json`, and the WordPress files.

## Validate and clean up

After import, compare the source and destination:

- table counts;
- users;
- posts and metadata;
- options and serialized values;
- uploads;
- active and installed plugins; and
- themes and front-end behavior.

Record whether `mysqldump` or PHP fallback was used. Keep a quiesced source
unchanged until validation succeeds. Then revoke access by removing the plugin
and deleting any operator-held token or export copy according to the approved
data-handling policy.

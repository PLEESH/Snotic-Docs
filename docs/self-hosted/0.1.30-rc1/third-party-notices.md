# Third-Party Notices

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

These notices apply to the Snotic Self-Hosted Debian distribution. The core
application [use terms](use-terms.md) are separate.

## Snotic Site Exporter

Snotic Site Exporter `0.2.0-pilot.2` is licensed under
`GPL-2.0-or-later`. Its versioned ZIP is the corresponding source form and
contains the PHP source, complete GNU GPL v2 text, licensing statement, README,
and plugin notice. The import format and route retain the
`hipanel-migrator-v1` compatibility identifiers.

## WP-CLI

The package includes official WP-CLI `2.12.0` at `/opt/hipanel/bin/wp`,
SHA-256:

```text
ce34ddd838f7351d6759068d09793f26755463b4a4610a5a5c0a97b68220d85c
```

The reviewed upstream `wp-cli/wp-cli-bundle` `v2.12.0` production dependency
set contains 54 packages: 53 declare MIT and one, `mck89/peast`, declares
BSD-3-Clause. The PHAR also contains the MIT-licensed bundle root. Exact
component versions, declarations, and available upstream notices are installed
under `/usr/share/doc/hipanel/third-party/wp-cli-2.12.0/`.

One component, `nb/oxymel`, declares MIT in its pinned `composer.json` but does
not publish a standalone licence file at that revision. The packaged audit
records that exception.

## htmx

The browser UI embeds htmx `1.9.12`, licensed under the Zero-Clause BSD licence
(`0BSD`). Its exact upstream licence is installed with the package notices.

## Go toolchain and modules

The `hipanel` binary statically links Go standard-library and module code. The
distribution includes an SPDX 2.3 JSON SBOM and collects licence/copying/notice
files from the checksum-verified module sources reported for the built binary.
The resulting inventory is installed under
`/usr/share/doc/hipanel/third-party/go/`.

## System packages and WordPress

Nginx, PHP, MariaDB, Certbot, Python, and other Debian dependencies come from
the customer's configured Ubuntu package sources and are not copied into the
Snotic Debian archive. AWS CLI is optional and not bundled.

WordPress core, themes, and plugins downloaded while provisioning a site are
not part of this distribution and remain governed by their respective terms.

Consult the signed `THIRD_PARTY_NOTICES.md`, package notice directories, and
SPDX SBOM supplied with the exact release for the authoritative full inventory.

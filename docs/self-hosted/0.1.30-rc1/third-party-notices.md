# Third-Party Notices

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

This notice applies to the Snotic Self-Hosted Debian distribution. Snotic is a
Pleesh product. The core application use grant is separate and is provided in
`SELF_HOSTED_USE_GRANT.md`.

## Snotic Site Exporter

The package and release bundle include Snotic Site Exporter
`0.2.0-pilot.2`, licensed under `GPL-2.0-or-later`. The versioned plugin ZIP is
the corresponding source form: it contains the PHP source, complete GNU GPL v2
text, licensing statement, README, and its own third-party notice. The import
format and route retain the `hipanel-migrator-v1` compatibility identifiers.

## WP-CLI

The package includes the official WP-CLI `2.12.0` PHAR at
`/opt/hipanel/bin/wp`, SHA-256
`ce34ddd838f7351d6759068d09793f26755463b4a4610a5a5c0a97b68220d85c`.

The reviewed upstream source is the `wp-cli/wp-cli-bundle` `v2.12.0` tag at
commit `d639a3dab65f4b935b21c61ea3662bf3258a03a5`. Its production Composer lock
contains 54 packages: 53 declare MIT and one (`mck89/peast`) declares
BSD-3-Clause. The supplied notice inventory also includes the MIT-licensed
bundle root, for 55 recorded components. This source-lock inventory is not
complete for the actual PHAR payload.

The PHAR additionally contains `psr/container` `1.0.0` (three PHP interface
files) and `wp-cli/wp-cli-tests` `v4.3.14` (eleven files). Neither is recorded in
the supplied inventory. The pinned upstream
[psr/container licence](https://github.com/php-fig/container/blob/b7ce3b176482dbbc1245ebf52b181af44c2cf55f/LICENSE)
has copyright notices absent from the supplied material. The pinned
[WP-CLI tests licence](https://github.com/wp-cli/wp-cli-tests/blob/b72c36dd0ebd70547c441f03c9257c3e857af4be/LICENSE)
has equivalent MIT notice text elsewhere in the package, but its component
inventory entry is missing. These links document the discrepancy; they do not
repair or replace the unchanged signed package notices.

Anonymous publication remains on hold until this notice coverage is resolved.
The package, bundle, embedded grant, and their signatures have not changed.

The exact component versions, source commits, declared licences, and copied
upstream notice files are installed under
`/usr/share/doc/hipanel/third-party/wp-cli-2.12.0/`. The same audited material
is maintained in `third_party/wp-cli-2.12.0/` in the source repository.

One upstream component, `nb/oxymel`, declares MIT in its pinned `composer.json`
but does not publish a standalone licence file at that commit. The audit retains
that exact declaration and records the exception explicitly. All other audited
components include their upstream root licence or notice files.

## htmx

The browser UI embeds htmx `1.9.12`, licensed under the Zero-Clause BSD
licence (`0BSD`). The exact upstream licence and source commit are included at
`/usr/share/doc/hipanel/third-party/htmx-1.9.12/`.

## Go Toolchain And Modules

The `hipanel` binary statically links Go standard-library code and the exact Go
modules recorded in the SPDX SBOM. During package construction, licence,
copying, and notice files are collected from the checksum-verified module
sources actually reported by `go version -m` for that binary. The resulting
`MODULES.json` and files are installed under
`/usr/share/doc/hipanel/third-party/go/`. Package validation fails if a linked
module has no top-level licence material.

## System Packages And Downloaded WordPress Code

Nginx, PHP, MariaDB, certbot, Python, and other Debian dependencies are installed
from the customer's configured Ubuntu package sources; they are not copied into
the Snotic Debian archive. AWS CLI is optional and is not bundled.

WordPress core, themes, and plugins downloaded while provisioning a site are not
part of this distribution. They remain governed by their respective licences.

The [public use grant](use-terms.md) reproduces the release's
`SELF_HOSTED_USE_GRANT.md`.

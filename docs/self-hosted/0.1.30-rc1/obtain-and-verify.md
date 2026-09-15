# Obtain and Verify the Distribution

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

The complete distribution is being prepared for the
[Snotic Self-Hosted download page](https://packages.snotic.com/).
The intended public route requires no login, email address, recipient allowlist
or expiring token. Once released, the page will list the exact size and SHA-256
of every required file. A prepared page is not a working download service.

!!! note "Approved eligibility; complete distribution required"
    The [public-use supplement v1](public-use-supplement-v1.md), effective
    15 September 2026, makes the downloader of this exact distribution from a
    Pleesh-provided or Pleesh-authorized public download an eligible recipient.
    The [embedded grant](use-terms.md) otherwise remains unchanged: one instance
    on one server per recipient, with no additional allowance through repeated
    downloads and no broader redistribution, modification or service rights.

!!! warning "Publication preparation is not a complete handoff"
    The signed notice addendum and offline public-use supplement are required,
    not optional links. Their signatures and final complete inventory are being
    prepared. The existing-file list below is not yet a complete distribution.
    Do not install or hand off this partial selection. Keep the software,
    required documents and all verification files together for offline use.

## Public file set

Keep these files together:

- [Signed product bundle](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel_0.1.30~rc1_amd64.tar.gz).
- [Bundle signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel_0.1.30~rc1_amd64.tar.gz.asc).
- [Bundle checksum](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel_0.1.30~rc1_amd64.tar.gz.sha256).
- [Checksum signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel_0.1.30~rc1_amd64.tar.gz.sha256.asc).
- [Armored public key](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel-archive-key.asc).
- [Armored public key signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel-archive-key.asc.asc).
- [Binary public keyring](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel-archive-keyring.gpg).
- [Public keyring signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel-archive-keyring.gpg.asc).
- [Installation and recovery guide](https://packages.snotic.com/self-hosted/0.1.30-rc1/INSTALL.txt).
- [Guide signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/INSTALL.txt.asc).
- [Read-only server preflight](https://packages.snotic.com/self-hosted/0.1.30-rc1/snotic-self-hosted-preflight.py).
- [Preflight signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/snotic-self-hosted-preflight.py.asc).

The public product bundle is `hipanel_0.1.30~rc1_amd64.tar.gz`, SHA-256:

```text
05bb2729f85cd3f377a4b3b3e0bff19d7905d0b07db21a536572bef6ffd92d08
```

It contains `hipanel_0.1.30~rc1_amd64.deb`, SHA-256:

```text
becfff27cae7e8c8bc9edb2eae629ec873e8a555d83d05d77cf8dee16658aa3e
```

Filenames and commands retain their released `hipanel` compatibility identifiers,
including the `~` in the bundle and package versions. Do not rename the files.
Historical source-repository identifiers in provenance are not public download
instructions and do not require repository access to install the binary release.
This is Early Access, not a stable release or a public APT repository.

## Confirm the signing identity

Verification requires `gpg`, `gpgv`, and `sha256sum`. Use a trusted machine
with these tools to verify the bundle before executing its contents. If the
destination server lacks verification tools, verify on a trusted Ubuntu
workstation first, then transfer the verified files securely. On that
workstation, missing tools can be installed from its trusted Ubuntu repositories:

```shell
sudo apt-get update
sudo apt-get install --yes gnupg gpgv ca-certificates
```

These commands install verification tools on the workstation, not Snotic on
the destination. Do not execute an unverified preflight or install the
application before verification. The destination's verified read-only preflight
must pass before package installation or changing its server stack.

Display the supplied public key fingerprint:

```shell
gpg --no-default-keyring --keyring ./hipanel-archive-keyring.gpg --fingerprint
```

Compare every character through a separate trusted Pleesh contact. The
authorized fingerprint is:

```text
26BAEB9BC68C2AB633FD6B822473AD1517C2A642
```

## Verify the bundle and companions

Run the checks from the directory containing the downloaded files:

```shell
BUNDLE=hipanel_0.1.30~rc1_amd64.tar.gz
gpgv --keyring ./hipanel-archive-keyring.gpg "${BUNDLE}.sha256.asc" "${BUNDLE}.sha256"
sha256sum --check "${BUNDLE}.sha256"
gpgv --keyring ./hipanel-archive-keyring.gpg "${BUNDLE}.asc" "${BUNDLE}"
gpgv --keyring ./hipanel-archive-keyring.gpg hipanel-archive-key.asc.asc hipanel-archive-key.asc
gpgv --keyring ./hipanel-archive-keyring.gpg hipanel-archive-keyring.gpg.asc hipanel-archive-keyring.gpg
gpgv --keyring ./hipanel-archive-keyring.gpg INSTALL.txt.asc INSTALL.txt
gpgv --keyring ./hipanel-archive-keyring.gpg snotic-self-hosted-preflight.py.asc snotic-self-hosted-preflight.py
```

!!! danger
    Stop if the fingerprint, a signature, or a checksum differs. Do not run the
    preflight, extract, or install a partially verified bundle. Do not replace
    a failed file from an untrusted source.

## Extract and verify the product files

Use a new empty extraction directory. The product files are directly at the
bundle root; no second wrapper archive needs to be extracted.

```shell
mkdir verified-release
tar -C verified-release -xzf "${BUNDLE}"
cd verified-release
gpgv --keyring ./hipanel-archive-keyring.gpg SHA256SUMS.asc SHA256SUMS
sha256sum --check SHA256SUMS
```

The signed inventory must pass for every listed artifact. Then follow the
[preflight and installation procedure](install.md). The package to install is
`hipanel_0.1.30~rc1_amd64.deb` in `verified-release`. No Pleesh AWS or GitHub
credentials are required, and local encrypted backup and restore do not require S3.

## Included material

The verified bundle includes the release manifest, schemas, SPDX SBOM,
installation guide, preflight, release notes, unchanged use grant, third-party
notices, public keys, checksums, and detached signatures.

It also includes `snotic-site-exporter_0.2.0-pilot.2.zip`, the complete plugin
PHP source form with its GPL-2.0-or-later declaration, full GPL v2 text,
README, and notices. The Debian package carries the bundled WP-CLI, htmx, and
Go dependency notice material described in [third-party notices](third-party-notices.md),
including the recorded WP-CLI notice-coverage limitation.
Ubuntu system dependencies and subsequently downloaded WordPress code are not
bundled in the application package.

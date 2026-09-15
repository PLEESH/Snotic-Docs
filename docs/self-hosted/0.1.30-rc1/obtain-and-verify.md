# Obtain and Verify the Distribution

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

Download the product bundle and its listed verification companions from the
[Snotic Self-Hosted download page](https://packages.snotic.com/). No login,
email address, recipient allowlist, or expiring download token is required.
The page lists the exact size and SHA-256 of every file.

!!! warning "Downloading and permission to use are different"
    The embedded [use grant](use-terms.md) still applies to individually
    authorized recipients. Downloading alone does not grant permission to
    install, redistribute, or modify the core application. A proposed public-use
    supplement is not effective unless separately approved by Pleesh. The
    signed archive and its terms have not been changed.

Obtain these files together:

- [Complete product bundle](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel_0.1.30~rc1_amd64.tar.gz).
- [Bundle signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel_0.1.30~rc1_amd64.tar.gz.asc).
- [Bundle checksum](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel_0.1.30~rc1_amd64.tar.gz.sha256).
- [Checksum signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel_0.1.30~rc1_amd64.tar.gz.sha256.asc).
- [Armored public key](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel-archive-key.asc).
- [Armored public key signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel-archive-key.asc.asc).
- [Binary public keyring](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel-archive-keyring.gpg).
- [Public keyring signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel-archive-keyring.gpg.asc).
- [Installation and recovery guide](https://packages.snotic.com/self-hosted/0.1.30-rc1/INSTALL.txt).
- [Guide signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/INSTALL.txt.asc).

The unchanged product bundle contains the Debian package, its signature,
read-only preflight, release notes, signed use grant and third-party notices,
public verification keys, schemas, SBOM and signed checksum inventory. It also
includes the Snotic Site Exporter ZIP with its PHP corresponding source, GPL
licence, README and notices. Dependency licences and notices are installed by
the package. See [third-party notices](third-party-notices.md).

Filenames retain the released `hipanel` compatibility names. Historical source
and schema provenance in signed metadata does not provide anonymous repository
access; use only the public download links above. This is Early Access, not a
stable release or a public APT repository. No application rebuild or new wrapper
was needed to provide this product distribution.

The expected product bundle SHA-256 is:

```text
05bb2729f85cd3f377a4b3b3e0bff19d7905d0b07db21a536572bef6ffd92d08
```

The expected Debian package SHA-256 inside the verified release is:

```text
becfff27cae7e8c8bc9edb2eae629ec873e8a555d83d05d77cf8dee16658aa3e
```

## Confirm the signing identity

Use a trusted machine with GnuPG to verify the bundle before executing its
contents. If the destination server does not already have verification tools,
perform these checks on a trusted Ubuntu workstation first, then transfer the
verified files securely. Do not skip the destination's read-only preflight
before package installation. On the verification workstation, missing tools
can be installed from its configured Ubuntu repositories:

```shell
sudo apt-get update
sudo apt-get install --yes gnupg gpgv ca-certificates
```

Display the supplied public key fingerprint:

```shell
gpg --no-default-keyring --keyring ./hipanel-archive-keyring.gpg --fingerprint
```

Compare every character through a separate trusted Pleesh contact. The
authorized fingerprint is:

```text
26BAEB9BC68C2AB633FD6B822473AD1517C2A642
```

## Verify the product bundle

Run all three checks from the directory containing the supplied files:

```shell
BUNDLE=hipanel_0.1.30~rc1_amd64.tar.gz
gpgv --keyring ./hipanel-archive-keyring.gpg "${BUNDLE}.sha256.asc" "${BUNDLE}.sha256"
sha256sum --check "${BUNDLE}.sha256"
gpgv --keyring ./hipanel-archive-keyring.gpg "${BUNDLE}.asc" "${BUNDLE}"
```

Also verify the public-key companions and supplied guide before following it:

```shell
gpgv --keyring ./hipanel-archive-keyring.gpg hipanel-archive-key.asc.asc hipanel-archive-key.asc
gpgv --keyring ./hipanel-archive-keyring.gpg hipanel-archive-keyring.gpg.asc hipanel-archive-keyring.gpg
gpgv --keyring ./hipanel-archive-keyring.gpg INSTALL.txt.asc INSTALL.txt
```

!!! danger
    Stop if the fingerprint, a signature, or a checksum differs. Do not install
    a partially verified distribution and do not replace a failed file from an
    untrusted source.

## Extract and verify the inner release

```shell
mkdir verified-release
tar -C verified-release -xzf "${BUNDLE}"
cd verified-release
gpgv --keyring ./hipanel-archive-keyring.gpg SHA256SUMS.asc SHA256SUMS
sha256sum --check SHA256SUMS
```

The signed inventory must pass for every listed artifact. The package to install
is `hipanel_0.1.30~rc1_amd64.deb` in `verified-release`.

Proceed to the [read-only preflight and installation steps](install.md). No
Pleesh AWS or GitHub credentials are required, and local encrypted backup and
restore do not require S3.

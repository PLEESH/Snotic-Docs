# Obtain and Verify the Distribution

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

Pleesh supplies this Early Access release through an authorized private
handoff. It is not a public download. Obtain these files together:

- `Snotic-Self-Hosted-0.1.30-rc1-owner-handoff.tar.gz`;
- `Snotic-Self-Hosted-0.1.30-rc1-owner-handoff.tar.gz.sha256`;
- both corresponding `.asc` detached signatures;
- `hipanel-archive-key.asc` and `hipanel-archive-keyring.gpg`;
- `INSTALL.txt` and `INSTALL.txt.asc`; and
- the supplied release notes, use terms, notices, inventories, and signatures.

The expected owner-handoff archive SHA-256 is:

```text
2ca1f61225d85d53ac969456deb181e5cb185b7a4d0cb63b6a16843102485456
```

The expected Debian package SHA-256 inside the verified release is:

```text
becfff27cae7e8c8bc9edb2eae629ec873e8a555d83d05d77cf8dee16658aa3e
```

## Confirm the signing identity

Install verification tools from the server's configured Ubuntu repositories if
they are not already present:

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

## Verify the owner handoff

Run all three checks from the directory containing the supplied files:

```shell
HANDOFF=Snotic-Self-Hosted-0.1.30-rc1-owner-handoff.tar.gz
gpgv --keyring ./hipanel-archive-keyring.gpg "${HANDOFF}.sha256.asc" "${HANDOFF}.sha256"
sha256sum --check "${HANDOFF}.sha256"
gpgv --keyring ./hipanel-archive-keyring.gpg "${HANDOFF}.asc" "${HANDOFF}"
```

Also verify the supplied guide before following it:

```shell
gpgv --keyring ./hipanel-archive-keyring.gpg INSTALL.txt.asc INSTALL.txt
```

!!! danger
    Stop if the fingerprint, a signature, or a checksum differs. Do not install
    a partially verified handoff and do not replace a failed file from an
    untrusted source.

## Extract and verify the inner release

```shell
mkdir Snotic-Self-Hosted-0.1.30-rc1-verified
tar -C Snotic-Self-Hosted-0.1.30-rc1-verified -xzf "${HANDOFF}"
cd Snotic-Self-Hosted-0.1.30-rc1-verified/Snotic-Self-Hosted-0.1.30-rc1/release-output
gpgv --keyring ./hipanel-archive-keyring.gpg hipanel_0.1.30~rc1_amd64.tar.gz.sha256.asc hipanel_0.1.30~rc1_amd64.tar.gz.sha256
sha256sum --check hipanel_0.1.30~rc1_amd64.tar.gz.sha256
gpgv --keyring ./hipanel-archive-keyring.gpg hipanel_0.1.30~rc1_amd64.tar.gz.asc hipanel_0.1.30~rc1_amd64.tar.gz
mkdir verified-release
tar -C verified-release -xzf hipanel_0.1.30~rc1_amd64.tar.gz
cd verified-release
gpgv --keyring ./hipanel-archive-keyring.gpg SHA256SUMS.asc SHA256SUMS
sha256sum --check SHA256SUMS
```

The signed inventory must pass for every listed artifact. The package to install
is `hipanel_0.1.30~rc1_amd64.deb` in `verified-release`.

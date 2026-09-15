# Obtain and Verify the Distribution

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

Obtain the complete distribution from the
[Snotic Self-Hosted download page](https://packages.snotic.com/).
No login, email address, recipient allowlist or expiring token is required.
The page lists the exact size and SHA-256 of every required file.

!!! note "Approved eligibility; complete distribution required"
    The [public-use supplement v1](public-use-supplement-v1.md), effective
    15 September 2026, makes the downloader of this exact distribution from a
    Pleesh-provided or Pleesh-authorized public download an eligible recipient.
    The [embedded grant](use-terms.md) otherwise remains unchanged: one instance
    on one server per recipient, with no additional allowance through repeated
    downloads and no broader redistribution, modification or service rights.

!!! warning "Keep the complete distribution together"
    The signed notice addendum and offline public-use supplement are required,
    not optional links. Do not install or hand off a partial selection. Keep the software,
    required documents and all verification files together for offline use.

## Public file set

Every file below is required. The download command and checksum inventory are
generated from the same reviewed inventory used by the download page.

<!-- BEGIN GENERATED DELIVERY LINKS -->
- [Signed product bundle](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel_0.1.30~rc1_amd64.tar.gz).
- [Bundle signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel_0.1.30~rc1_amd64.tar.gz.asc).
- [Bundle checksum](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel_0.1.30~rc1_amd64.tar.gz.sha256).
- [Checksum signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel_0.1.30~rc1_amd64.tar.gz.sha256.asc).
- [Armored public key](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel-archive-key.asc).
- [Armored public key signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel-archive-key.asc.asc).
- [Binary public keyring](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel-archive-keyring.gpg).
- [Public keyring signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/hipanel-archive-keyring.gpg.asc).
- [Signed installation and recovery guide](https://packages.snotic.com/self-hosted/0.1.30-rc1/INSTALL.txt).
- [Guide signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/INSTALL.txt.asc).
- [Read-only server preflight](https://packages.snotic.com/self-hosted/0.1.30-rc1/snotic-self-hosted-preflight.py).
- [Preflight signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/snotic-self-hosted-preflight.py.asc).
- [Required third-party notice addendum v1](https://packages.snotic.com/self-hosted/0.1.30-rc1/Snotic-Self-Hosted-0.1.30-rc1-THIRD-PARTY-NOTICE-ADDENDUM-v1.txt).
- [Required third-party notice addendum v1 signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/Snotic-Self-Hosted-0.1.30-rc1-THIRD-PARTY-NOTICE-ADDENDUM-v1.txt.asc).
- [Required third-party notice addendum v1 checksum](https://packages.snotic.com/self-hosted/0.1.30-rc1/Snotic-Self-Hosted-0.1.30-rc1-THIRD-PARTY-NOTICE-ADDENDUM-v1.txt.sha256).
- [Required third-party notice addendum v1 checksum signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/Snotic-Self-Hosted-0.1.30-rc1-THIRD-PARTY-NOTICE-ADDENDUM-v1.txt.sha256.asc).
- [Required approved public-use supplement v1](https://packages.snotic.com/self-hosted/0.1.30-rc1/Snotic-Self-Hosted-0.1.30-rc1-PUBLIC-USE-SUPPLEMENT-v1.txt).
- [Required approved public-use supplement v1 signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/Snotic-Self-Hosted-0.1.30-rc1-PUBLIC-USE-SUPPLEMENT-v1.txt.asc).
- [Required approved public-use supplement v1 checksum](https://packages.snotic.com/self-hosted/0.1.30-rc1/Snotic-Self-Hosted-0.1.30-rc1-PUBLIC-USE-SUPPLEMENT-v1.txt.sha256).
- [Required approved public-use supplement v1 checksum signature](https://packages.snotic.com/self-hosted/0.1.30-rc1/Snotic-Self-Hosted-0.1.30-rc1-PUBLIC-USE-SUPPLEMENT-v1.txt.sha256.asc).
<!-- END GENERATED DELIVERY LINKS -->

## Download all required files

Use a trusted workstation with `curl` and sufficient disk space. Run this block
in Bash. It creates a new directory and stops on any failed download; it never
executes downloaded software. If interrupted, remove only the incomplete new
download directory and start again. Do not merge old and new download sets.

<!-- BEGIN GENERATED DELIVERY COMMAND -->
```shell
(
set -eu
mkdir snotic-rc1-download || exit 1
cd snotic-rc1-download || exit 1
while IFS= read -r filename; do
  curl --fail --show-error --silent --location --proto "=https" --proto-redir "=https" \
    --output "$filename" "https://packages.snotic.com/self-hosted/0.1.30-rc1/$filename" || exit 1
done <<'REQUIRED_FILES'
hipanel_0.1.30~rc1_amd64.tar.gz
hipanel_0.1.30~rc1_amd64.tar.gz.asc
hipanel_0.1.30~rc1_amd64.tar.gz.sha256
hipanel_0.1.30~rc1_amd64.tar.gz.sha256.asc
hipanel-archive-key.asc
hipanel-archive-key.asc.asc
hipanel-archive-keyring.gpg
hipanel-archive-keyring.gpg.asc
INSTALL.txt
INSTALL.txt.asc
snotic-self-hosted-preflight.py
snotic-self-hosted-preflight.py.asc
Snotic-Self-Hosted-0.1.30-rc1-THIRD-PARTY-NOTICE-ADDENDUM-v1.txt
Snotic-Self-Hosted-0.1.30-rc1-THIRD-PARTY-NOTICE-ADDENDUM-v1.txt.asc
Snotic-Self-Hosted-0.1.30-rc1-THIRD-PARTY-NOTICE-ADDENDUM-v1.txt.sha256
Snotic-Self-Hosted-0.1.30-rc1-THIRD-PARTY-NOTICE-ADDENDUM-v1.txt.sha256.asc
Snotic-Self-Hosted-0.1.30-rc1-PUBLIC-USE-SUPPLEMENT-v1.txt
Snotic-Self-Hosted-0.1.30-rc1-PUBLIC-USE-SUPPLEMENT-v1.txt.asc
Snotic-Self-Hosted-0.1.30-rc1-PUBLIC-USE-SUPPLEMENT-v1.txt.sha256
Snotic-Self-Hosted-0.1.30-rc1-PUBLIC-USE-SUPPLEMENT-v1.txt.sha256.asc
REQUIRED_FILES
) && cd snotic-rc1-download
```
<!-- END GENERATED DELIVERY COMMAND -->

Remain in that directory for verification. For a manual handoff, transfer the
entire directory after verification, including every document and verification
file. The receiver must repeat verification before acknowledging receipt. Record
delivery separately from installation; sending files is not an installation test.

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

Run the checks from the directory containing all downloaded files. The complete
checksum inventory fails if any required document, signature or key export is
missing or changed. It does not replace independent signing-identity verification.

<!-- BEGIN GENERATED DELIVERY CHECKSUMS -->
```shell
sha256sum --check --strict <<'REQUIRED_SHA256'
05bb2729f85cd3f377a4b3b3e0bff19d7905d0b07db21a536572bef6ffd92d08  hipanel_0.1.30~rc1_amd64.tar.gz
e650a462dce2a8da78c94c8bf8649d15043e4d140c2cc1e2c102c44c627964c6  hipanel_0.1.30~rc1_amd64.tar.gz.asc
9c8d420cdca7e02d442efddcb35bf26f8b30553995ccbd335f4ff73d9c10745e  hipanel_0.1.30~rc1_amd64.tar.gz.sha256
576774350a2785dd86167af0d4d2e9a0cb97f7f0f039c4b92a6e0e9b18583362  hipanel_0.1.30~rc1_amd64.tar.gz.sha256.asc
a37cef936d17b73589f3737be4ae3f6f93e3c73132426b127e0bae5a36f08fe3  hipanel-archive-key.asc
7c36cfbf2c85acff72b9e02fd843e82506161852c0fa7f191ce7a3c920749344  hipanel-archive-key.asc.asc
f8a70a5c03bfad9a9471b04be4a55f1116d155c451316f8d952eb3d726236d32  hipanel-archive-keyring.gpg
be160de7d09217498ab837aeab2afcf8ccb5ad7076750e23203ab1eb9f44b137  hipanel-archive-keyring.gpg.asc
746b7ade29796697d7d426d90ebbc0155573b0a48d14ca9a5c1a0491a355abaa  INSTALL.txt
26aeca89302697e3687de13e5b0bab0eeb4c9efe92caa44b97bd933976068095  INSTALL.txt.asc
fc4fa0768e702adfcd58539255790aa7c1ceca616e262cd000c46a12e7be986b  snotic-self-hosted-preflight.py
f2c7505eabf01dc247b9e826fc11fd00d526b684cb8c05e1e12cd25997bbd660  snotic-self-hosted-preflight.py.asc
dbc4d5d4bea6c39b66035e4882e167c48f75cbd5eee518cbe1d037d9cced66fb  Snotic-Self-Hosted-0.1.30-rc1-THIRD-PARTY-NOTICE-ADDENDUM-v1.txt
f8e535e9932c840334fdbcd3c80e307b1412a7f50f032f2f335dc7fa69d4167e  Snotic-Self-Hosted-0.1.30-rc1-THIRD-PARTY-NOTICE-ADDENDUM-v1.txt.asc
05d7ce4a387e7e1d2885021fb1ae94120aea61b33d599bdca91c054f01b4df86  Snotic-Self-Hosted-0.1.30-rc1-THIRD-PARTY-NOTICE-ADDENDUM-v1.txt.sha256
8c493e068dd2c0085be521c40628428c35789243cd70614c4bf550665b20fbcb  Snotic-Self-Hosted-0.1.30-rc1-THIRD-PARTY-NOTICE-ADDENDUM-v1.txt.sha256.asc
cb755d684eb36bb1621e6e8031e512b75373d6f30424f569f85f2abd93ba6929  Snotic-Self-Hosted-0.1.30-rc1-PUBLIC-USE-SUPPLEMENT-v1.txt
3751e7d4b86fe0ec6dd439d05daa2005181b60f9e1460ef93ca454529b49171c  Snotic-Self-Hosted-0.1.30-rc1-PUBLIC-USE-SUPPLEMENT-v1.txt.asc
aaec58b897f790dc644284b3b08fb1b70f996c24a2f8d1bfe42ccb3521030807  Snotic-Self-Hosted-0.1.30-rc1-PUBLIC-USE-SUPPLEMENT-v1.txt.sha256
41f2b5536e66d1380c5213ffbf8fa3297294abe8022088966d5d4ca02b400910  Snotic-Self-Hosted-0.1.30-rc1-PUBLIC-USE-SUPPLEMENT-v1.txt.sha256.asc
REQUIRED_SHA256
```
<!-- END GENERATED DELIVERY CHECKSUMS -->

```shell
BUNDLE=hipanel_0.1.30~rc1_amd64.tar.gz
NOTICE=Snotic-Self-Hosted-0.1.30-rc1-THIRD-PARTY-NOTICE-ADDENDUM-v1.txt
SUPPLEMENT=Snotic-Self-Hosted-0.1.30-rc1-PUBLIC-USE-SUPPLEMENT-v1.txt
for document in "$NOTICE" "$SUPPLEMENT"; do
  gpgv --keyring ./hipanel-archive-keyring.gpg "${document}.sha256.asc" "${document}.sha256" || exit 1
  sha256sum --check --strict "${document}.sha256" || exit 1
  gpgv --keyring ./hipanel-archive-keyring.gpg "${document}.asc" "$document" || exit 1
done
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
    a failed file from an untrusted source. The approved key expires on
    8 September 2027 at 02:00 UTC. Stop and contact Pleesh if it is expired,
    revoked or no longer approved; do not override verification to install.

Read the notice addendum and public-use supplement before installation. Keep
their originals and verification files beside `verified-release`, including for
offline recovery. The original signed bundle and embedded terms are unchanged.

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
with the required separate addendum correcting the RC1 WP-CLI notice omissions.
Ubuntu system dependencies and subsequently downloaded WordPress code are not
bundled in the application package.

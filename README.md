# Snotic Documentation

This repository contains the reviewed public documentation for Snotic, a
product developed and operated by Pleesh. The published site is
<https://docs.snotic.com/>.

The first versioned documentation set covers Snotic Self-Hosted
`0.1.30~rc1` at `/self-hosted/0.1.30-rc1/`. This is an Early Access release,
not a stable release. Public download availability does not broaden the
embedded installation/use licence.

## Authority boundary

- This repository is authoritative for published public documentation.
- The private application repository is authoritative for released behavior,
  packages, commands, schemas, and compatibility.
- The private product repository is authoritative for brand and approved
  product requirements.
- Private infrastructure repositories remain authoritative for deployment,
  access, incident, and customer-specific evidence.

No application source, customer record, private infrastructure evidence, or
release secret belongs here.

## Local validation

```shell
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --require-hashes --requirement requirements.txt
python -m compileall -q scripts
python -m unittest discover -s tests -p 'test_*.py'
python scripts/check_commands.py docs
python scripts/check_links.py docs
python scripts/check_public_safety.py docs
python scripts/check_public_safety.py .
mkdocs build --strict --site-dir site
python scripts/check_links.py site
python scripts/check_public_safety.py site
python scripts/build_downloads.py --output /tmp/snotic-download-page
python scripts/check_public_safety.py /tmp/snotic-download-page
```

GitHub Actions runs the same checks for pull requests. Only reviewed `main`
builds are eligible for GitHub Pages deployment.

## Separate download page

`downloads/rc1.json` is the canonical reviewed public artifact inventory. It pins
filenames, sizes, SHA-256 values, content types, and the bundle/package identity.
Both this page and the infrastructure object scope consume that inventory;
DevOps pins an identical copy to a reviewed source commit and verifies its digest.
Do not maintain a separately authored infrastructure inventory.
The builder produces only `index.html` and `styles.css` in a new or empty output
directory. `--verify-assets ASSET_DIRECTORY` additionally checks the selected local
release files without copying or changing them. Never commit those files here.

DevOps deploys the reviewed page through the separately approved distribution
execution plan. The origin maps `/public` to the viewer root; release file
URLs include `/self-hosted/0.1.30-rc1/`. Only `/` uses a default-root object;
no S3 website-style version-directory indexing is assumed. No page JavaScript,
forms, authentication, analytics, external fonts, or viewer tokens are used.

Keep this change in draft until the selected public set passes its public-content
gate, the infrastructure execution plan is approved, and independent anonymous
GET/checksum/signature and browser verification succeeds. Only then merge the
documentation download-link change and verify Pages again. Page output is
separate from the `site` directory and never expands the Pages allowlist.

The public set reuses the existing signed product bundle. The private owner
archive and custody records are never deployment inputs; they remain unchanged.
File counts and download-size totals are derived from the reviewed inventory.

The selected product bundle passed focused private-content and signature
screening, but its WP-CLI notice coverage is incomplete. The versioned
third-party-notices page records the two omitted components. Do not interpret
passing page tests as release-completeness or publication approval. Resolve
that coverage separately without altering frozen RC1 assets before exposure.

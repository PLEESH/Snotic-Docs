# Snotic Documentation

This repository contains the reviewed public documentation for Snotic, a
product developed and operated by Pleesh. The published site is
<https://docs.snotic.com/>.

The first versioned documentation set covers Snotic Self-Hosted
`0.1.30~rc1` at `/self-hosted/0.1.30-rc1/`. This is an Early Access release,
not a stable or publicly downloadable distribution.

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
```

GitHub Actions runs the same checks for pull requests. Only reviewed `main`
builds are eligible for GitHub Pages deployment.

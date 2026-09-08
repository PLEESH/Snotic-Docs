# Snotic Documentation Agent Guide

## Purpose

This repository is the canonical public documentation source for Snotic. Every
agent working on application, product, or operations changes owns the affected
documentation and must not leave it as an unassigned future task.

## Authority and evidence

- Pleesh is the company and legal owner. Snotic is the product.
- The private Snotic application repository is authoritative for actual
  behavior, package contents, commands, paths, schemas, and release evidence.
- The private Snotic Product repository and its `BRAND.md` are authoritative
  for approved names and product requirements.
- This repository is authoritative only for reviewed public documentation.
- Private infrastructure repositories remain authoritative for deployment,
  access, customer, incident, and operational evidence.

Verify a claim against the exact released artifact or implementation commit.
Do not infer current behavior from product planning alone. Never copy private
application, product, or infrastructure documents wholesale.

## Standing responsibilities

Development maintains:

- public product behavior and supported platforms;
- Self-Hosted installation and configuration;
- administrator workflows;
- CLI and API reference;
- Snotic Site Exporter guidance;
- release notes, compatibility, limitations, and security guidance; and
- application architecture and integration guidance.

DevOps maintains public deployment and upgrade runbooks and verifies
installation, security, backup, and recovery instructions against released
behavior. DevOps also owns GitHub Pages, DNS, HTTPS, and the publishing path.
Private runbooks and evidence stay outside this repository.

Use paired pull requests when a code change and its public documentation live
in different repositories. A code PR with no documentation impact must explain
why.

## Public boundary

Use synthetic examples such as `example.com` and `admin@example.com`.

Never commit or publish:

- customer identities, recipient records, domains, or data;
- production or private hosts, addresses, account inventories, or account IDs;
- passwords, API keys, recovery codes, private keys, secret values, or export
  archives;
- private signing operations or key-custody locations;
- private filesystem or evidence paths;
- internal handovers, incidents, logs, rollback evidence, or access procedures;
- local-only links, absolute workstation paths, or local filesystem URIs; or
- links that require access to a private repository.

Public keys, approved signing fingerprints, package paths, and product key-file
paths may be documented when required for customer verification or recovery.
Never include their secret contents.

## Product and compatibility language

Use **Snotic** in headings and prose. Use **Pleesh** as provider. Use
**Snotic Self-Hosted**, **Snotic Managed**, and **Snotic Site Exporter** exactly.

For released commands and machine identifiers, use the actual compatibility
names: package and CLI `hipanel`, current systemd units, and current installed
paths. Explain this once per versioned guide. Do not invent a `snotic` command.

## Versioning and publication

- Keep immutable release documentation below its versioned path.
- Label Early Access, candidate, beta, and stable status accurately.
- Do not rewrite commands for an older release after a future alias appears.
- Build only the allowlisted `docs/` directory.
- Scan source and generated output, including the search index.
- Require navigation, local search, link and anchor checks, command checks,
  strict builds, and independent review.
- Publish only from reviewed `main` through the Pages workflow.

## Change workflow

1. Identify the affected release and authoritative evidence.
2. Preserve unrelated changes and use a focused branch.
3. Write task-oriented steps with prerequisites, expected results, failure
   guidance, and warnings for destructive operations.
4. Run all commands in `README.md`.
5. Inspect the generated site at desktop and mobile widths for overflow,
   unreadable text, broken navigation, and inaccessible controls.
6. Request independent Development or DevOps review as appropriate.
7. Merge normally after required checks and review pass.

Escalate only unresolved legal or commercial commitments, credentials/access,
or materially risky publishing and DNS mutations.

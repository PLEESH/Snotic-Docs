# Requirements and Responsibilities

> **Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access**

## Supported server

- Fresh, or explicitly supported minimal, Ubuntu 22.04 LTS or Ubuntu 24.04
  LTS.
- amd64 architecture.
- systemd as the init system.
- At least 2 GiB RAM.
- At least 10 GiB free on `/`, plus capacity for WordPress content, databases,
  logs, and backups.
- No existing hosting panel, web/database stack, or listener on ports 80, 443,
  3306, or 8080. An existing `hipanel` installation is handled as an upgrade,
  not a fresh install.

The supplied preflight is the authoritative host check. Stop when it reports
`BLOCKED`.

## Customer responsibilities

For Snotic Self-Hosted, the customer operates and protects:

- the Ubuntu server and administrative access;
- SSH, firewall, DNS, and network policy;
- panel and site HTTPS certificates;
- operating-system and Snotic updates;
- monitoring, capacity, logs, and incident response;
- backup retention, off-server copies, and restore drills; and
- credentials, MFA recovery codes, encryption keys, and exported WordPress
  data.

Pleesh does not operate this server or its backups unless a separate written
arrangement says otherwise. Early Access includes no SLA or automatic managed
support.

## Before installation

Have these ready:

- the complete private distribution handoff from Pleesh;
- the authorized signing fingerprint confirmed through a separate trusted
  Pleesh contact;
- root or passwordless authorized `sudo` access;
- a current server snapshot when upgrading an existing installation;
- a customer-controlled panel hostname for normal HTTPS browser access; and
- a secure password manager for administrator credentials and recovery codes.

Do not send the recipient private-repository credentials. The supplied handoff
contains everything required to verify and install the release.

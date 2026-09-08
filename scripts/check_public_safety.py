#!/usr/bin/env python3
"""Reject private or sensitive material from public documentation trees."""

from __future__ import annotations

import re
import sys
from ipaddress import ip_address
from pathlib import Path


TEXT_SUFFIXES = {
    "",
    ".css",
    ".html",
    ".in",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".toml",
    ".xml",
    ".yml",
    ".yaml",
}

FORBIDDEN = {
    "local workstation path": re.compile(r"(?:^|[\s\"'(])/(?:home|Users)/", re.MULTILINE),
    "local-only URI": re.compile(r"\b(?:file|vscode)://", re.IGNORECASE),
    "recipient record identifier": re.compile(r"\bSNOTIC-SH-EA-[A-Z0-9-]+\b", re.IGNORECASE),
    "AWS account ID": re.compile(r"(?<![0-9A-Fa-f])\d{12}(?![0-9A-Fa-f])"),
    "private repository URL": re.compile(
        r"https?://github\.com/PLEESH/(?!Snotic-Docs(?:[/?#]|$))[^\s)]+",
        re.IGNORECASE,
    ),
    "private key material": re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "release-secret namespace": re.compile(r"/snotic/(?:pilot|production)/release/", re.IGNORECASE),
    "private handover reference": re.compile(r"\b(?:Handover\.md|private-custody|private-delivery-record)\b", re.IGNORECASE),
}

VERSION_ROOT = Path("self-hosted/0.1.30-rc1")
VERSION_MARKER = "Version: Snotic Self-Hosted 0.1.30~rc1 | Status: Early Access"
IPV4 = re.compile(r"(?<![0-9])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9])")
SKIP_PARTS = {".git", ".venv", "site", "__pycache__"}


def text_files(root: Path):
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in SKIP_PARTS for part in rel.parts):
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_public_safety.py <tree>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    failures: list[str] = []
    for path in text_files(root):
        content = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(root)
        for label, pattern in FORBIDDEN.items():
            match = pattern.search(content)
            if match:
                line = content.count("\n", 0, match.start()) + 1
                failures.append(f"{rel}:{line}: {label}")

        for match in IPV4.finditer(content):
            try:
                address = ip_address(match.group(0))
            except ValueError:
                continue
            if not address.is_loopback:
                line = content.count("\n", 0, match.start()) + 1
                failures.append(f"{rel}:{line}: non-loopback IPv4 address")

        if root.name == "docs" and path.suffix.lower() == ".md":
            try:
                rel.relative_to(VERSION_ROOT)
            except ValueError:
                continue
            if VERSION_MARKER not in content:
                failures.append(f"{rel}: missing version/status marker")

    if failures:
        print("public-safety validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"public-safety validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

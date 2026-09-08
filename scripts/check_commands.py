#!/usr/bin/env python3
"""Syntax-check shell examples and enforce released command identifiers."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


FENCE = re.compile(r"^```(?:bash|console|shell)\s*$\n(.*?)^```\s*$", re.MULTILINE | re.DOTALL)
PLACEHOLDER = re.compile(r"<[A-Za-z0-9._-]+>")
INVENTED_CLI = re.compile(
    r"(?:^|[;&|]\s*|\bsudo\s+)(?:/\S+/)?snotic\s+(?:auth|backup-key|ops|recovery|secret-key|serve|sites|token|version)\b",
    re.MULTILINE,
)
INVENTED_SERVICE = re.compile(r"\bsnotic(?:-[a-z0-9-]+)?\.(?:service|timer)\b")
HIPANEL_UNIT = re.compile(r"\bhipanel(?:-[a-z0-9-]+)?\.(?:service|timer)\b")
RC1_UNITS = {
    "hipanel.service",
    "hipanel-backup.service",
    "hipanel-backup.timer",
    "hipanel-ops-alert.service",
    "hipanel-ops-alert.timer",
}


def normalize_shell(block: str) -> str:
    lines = []
    for line in block.splitlines():
        if line.startswith("$ "):
            line = line[2:]
        if line.startswith("# ") and not line.startswith("#!"):
            lines.append(line)
            continue
        lines.append(PLACEHOLDER.sub("example", line))
    return "\n".join(lines) + "\n"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_commands.py <docs-tree>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1])
    failures: list[str] = []
    blocks = 0
    all_content = ""

    for path in sorted(root.rglob("*.md")):
        content = path.read_text(encoding="utf-8")
        all_content += "\n" + content
        for index, match in enumerate(FENCE.finditer(content), start=1):
            blocks += 1
            shell = normalize_shell(match.group(1))
            result = subprocess.run(
                ["bash", "-n"],
                input=shell,
                text=True,
                capture_output=True,
                check=False,
            )
            if result.returncode:
                failures.append(f"{path}: shell block {index}: {result.stderr.strip()}")

    if INVENTED_CLI.search(all_content):
        failures.append("documentation invents a snotic CLI command; rc1 uses hipanel")
    if INVENTED_SERVICE.search(all_content):
        failures.append("documentation invents a snotic systemd unit; rc1 uses hipanel units")
    invalid_units = sorted(set(HIPANEL_UNIT.findall(all_content)) - RC1_UNITS)
    if invalid_units:
        failures.append("documentation uses units absent from rc1: " + ", ".join(invalid_units))
    if "apt-key" in all_content:
        failures.append("documentation uses deprecated apt-key")
    if "/opt/hipanel/bin/hipanel" not in all_content:
        failures.append("released hipanel CLI path is not documented")
    if "hipanel.service" not in all_content:
        failures.append("released hipanel.service is not documented")

    if failures:
        print("command validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"command validation passed: {blocks} shell blocks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

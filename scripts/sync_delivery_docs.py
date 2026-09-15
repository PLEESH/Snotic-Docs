#!/usr/bin/env python3
"""Render delivery instructions from the one canonical publication inventory."""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def generated_blocks(data):
    base = "https://packages.snotic.com" + data["path"]
    links = "\n".join(f'- [{f["label"]}]({base}{f["name"]}).' for f in data["files"])
    names = "\n".join(f["name"] for f in data["files"])
    command = (
        "```shell\n(\nset -eu\nmkdir snotic-rc1-download || exit 1\ncd snotic-rc1-download || exit 1\n"
        "while IFS= read -r filename; do\n"
        '  curl --fail --show-error --silent --location --proto "=https" --proto-redir "=https" \\\n'
        f'    --output "$filename" "{base}$filename" || exit 1\n'
        "done <<'REQUIRED_FILES'\n" + names + "\nREQUIRED_FILES\n) && cd snotic-rc1-download\n```"
    )
    checksums = (
        "```shell\nsha256sum --check --strict <<'REQUIRED_SHA256'\n"
        + "\n".join(f'{f["sha256"]}  {f["name"]}' for f in data["files"])
        + "\nREQUIRED_SHA256\n```"
    )
    return {"LINKS": links, "COMMAND": command, "CHECKSUMS": checksums}


def render(content, data):
    for kind, block in generated_blocks(data).items():
        start = f"<!-- BEGIN GENERATED DELIVERY {kind} -->"
        end = f"<!-- END GENERATED DELIVERY {kind} -->"
        if content.count(start) != 1 or content.count(end) != 1:
            raise ValueError("missing or duplicate generated delivery markers")
        before, rest = content.split(start)
        _, after = rest.split(end)
        content = before + start + "\n" + block + "\n" + end + after
    return content


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.loads((ROOT / "downloads/rc1.json").read_text())
    path = ROOT / "docs/self-hosted/0.1.30-rc1/obtain-and-verify.md"
    original = path.read_text()
    result = render(original, data)
    if args.check:
        if result != original:
            raise SystemExit("delivery documentation differs from canonical inventory")
    else:
        path.write_text(result, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render the two allowlisted download-page assets without copying release files."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from html import escape
from pathlib import Path
from string import Template


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = "Snotic-Self-Hosted-0.1.30-rc1-owner-handoff.tar.gz"
EXPECTED = {
    ARCHIVE, f"{ARCHIVE}.asc", f"{ARCHIVE}.sha256", f"{ARCHIVE}.sha256.asc",
    "hipanel-archive-key.asc", "hipanel-archive-key.asc.asc",
    "hipanel-archive-keyring.gpg", "hipanel-archive-keyring.gpg.asc",
    "INSTALL.txt", "INSTALL.txt.asc",
}
FINGERPRINT = "26BAEB9BC68C2AB633FD6B822473AD1517C2A642"
ARCHIVE_DIGEST = "2ca1f61225d85d53ac969456deb181e5cb185b7a4d0cb63b6a16843102485456"
# Pins all ten approved (filename, size, SHA-256) tuples without a second table.
INVENTORY_DIGEST = "ea3904c24d709e0c6e4fe555b44733e52864d335ccd576c9cb57373ad9e254c8"


def load_inventory(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if (data["version"], data["status"], data["path"], data["fingerprint"]) != (
        "0.1.30~rc1", "Early Access", "/self-hosted/0.1.30-rc1/", FINGERPRINT
    ):
        raise ValueError("unexpected release identity")
    files = data["files"]
    if len(files) != 10 or {f["name"] for f in files} != EXPECTED:
        raise ValueError("expected the exact ten-file inventory")
    for item in files:
        if type(item["size"]) is not int or item["size"] <= 0:
            raise ValueError("invalid file size")
        if not re.fullmatch(r"[a-f0-9]{64}", item["sha256"]):
            raise ValueError("invalid SHA-256")
        if not isinstance(item["label"], str) or not item["label"].strip():
            raise ValueError("missing file label")
        if item["name"] == ARCHIVE and (item["size"], item["sha256"]) != (
            49230129, ARCHIVE_DIGEST
        ):
            raise ValueError("immutable archive identity differs")
    identities = sorted((f["name"], f["size"], f["sha256"]) for f in files)
    encoded = json.dumps(identities, separators=(",", ":")).encode("ascii")
    if hashlib.sha256(encoded).hexdigest() != INVENTORY_DIGEST:
        raise ValueError("immutable ten-file inventory differs")
    return data


def verify_assets(data: dict, source: Path) -> None:
    """Read only the explicit ten-file allowlist from a local verified asset set."""
    for item in data["files"]:
        path = source / item["name"]
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"missing or non-regular asset: {item['name']}")
        if path.stat().st_size != item["size"]:
            raise ValueError(f"size differs: {item['name']}")
        with path.open("rb") as handle:
            digest = hashlib.file_digest(handle, "sha256").hexdigest()
        if digest != item["sha256"]:
            raise ValueError(f"SHA-256 differs: {item['name']}")


def render(data: dict) -> str:
    rows = []
    for item in data["files"]:
        name = escape(item["name"], quote=True)
        rows.append(
            '        <li class="file">'
            f'<div class="file-title"><strong>{escape(item["label"])}</strong>'
            f'<span>{item["size"]:,} bytes</span></div>'
            f'<a class="filename" href="{data["path"]}{name}" download="{name}">{name}</a>'
            '<div class="digest"><span>SHA-256</span>'
            f'<code>{item["sha256"]}</code></div></li>'
        )
    template = Template((ROOT / "downloads/page.html").read_text(encoding="utf-8"))
    return template.substitute(
        archive_url=data["path"] + ARCHIVE, archive_name=ARCHIVE,
        archive_size=f"{49230129:,}", file_rows="\n".join(rows),
        fingerprint=data["fingerprint"],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verify-assets", type=Path)
    args = parser.parse_args()
    data = load_inventory(ROOT / "downloads/rc1.json")
    if args.verify_assets is not None:
        verify_assets(data, args.verify_assets)
    # An empty output prevents stale files from joining the deployment allowlist.
    if args.output.exists() and any(args.output.iterdir()):
        parser.error("output must be empty")
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "index.html").write_text(render(data), encoding="utf-8", newline="\n")
    (args.output / "styles.css").write_bytes((ROOT / "downloads/styles.css").read_bytes())
    print("Built index.html and styles.css; no release assets copied or changed")


if __name__ == "__main__":
    main()

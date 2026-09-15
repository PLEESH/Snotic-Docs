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
ARCHIVE = "hipanel_0.1.30~rc1_amd64.tar.gz"
FINGERPRINT = "26BAEB9BC68C2AB633FD6B822473AD1517C2A642"
ARCHIVE_DIGEST = "05bb2729f85cd3f377a4b3b3e0bff19d7905d0b07db21a536572bef6ffd92d08"
PACKAGE = {"name": "hipanel_0.1.30~rc1_amd64.deb", "size": 12257444,
           "sha256": "becfff27cae7e8c8bc9edb2eae629ec873e8a555d83d05d77cf8dee16658aa3e"}
# Pins download and page identities from the single reviewed inventory.
INVENTORY_DIGEST = "d02ebe4eeda068dc6a5854b823e027adbd7a7a0a8e8d5f94cb077a6f3059780b"
PRIVATE_NAME = re.compile(r"owner[-_]handoff|custody|recipient|authorization|immutable-release-assets", re.I)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def load_inventory(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    if (data["version"], data["status"], data["path"], data["fingerprint"]) != (
        "0.1.30~rc1", "Early Access", "/self-hosted/0.1.30-rc1/", FINGERPRINT
    ):
        raise ValueError("unexpected release identity")
    if data["archive"] != ARCHIVE or data["package"] != PACKAGE:
        raise ValueError("immutable bundle/package identity differs")
    files = data["files"]
    if not files or len({f["name"] for f in files}) != len(files):
        raise ValueError("empty or duplicate publication inventory")
    for item in files:
        if PRIVATE_NAME.search(item["name"]):
            raise ValueError("private custody artifacts cannot be published")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._~+-]*", item["name"]):
            raise ValueError("invalid publication filename")
        if type(item["size"]) is not int or item["size"] <= 0:
            raise ValueError("invalid file size")
        if not re.fullmatch(r"[a-f0-9]{64}", item["sha256"]):
            raise ValueError("invalid SHA-256")
        if not isinstance(item["label"], str) or not item["label"].strip():
            raise ValueError("missing file label")
        if item["object_key"] != "public" + data["path"] + item["name"]:
            raise ValueError("unexpected download object key")
        if item["content_type"] not in {
            "application/gzip", "application/pgp-signature", "application/pgp-keys",
            "text/plain; charset=utf-8", "text/x-python; charset=utf-8",
        }:
            raise ValueError("invalid content type")
        if item["name"] == ARCHIVE and (item["size"], item["sha256"]) != (
            12344056, ARCHIVE_DIGEST
        ):
            raise ValueError("immutable archive identity differs")
    pages = data["page_assets"]
    if len(pages) != 2 or {p["name"] for p in pages} != {"index.html", "styles.css"}:
        raise ValueError("unexpected page inventory")
    for item in pages:
        expected_type = {"index.html": "text/html; charset=utf-8", "styles.css": "text/css; charset=utf-8"}[item["name"]]
        if item["object_key"] != "public/" + item["name"] or item["content_type"] != expected_type:
            raise ValueError("unexpected page object key or content type")
        if type(item["size"]) is not int or item["size"] <= 0 or not re.fullmatch(r"[a-f0-9]{64}", item["sha256"]):
            raise ValueError("invalid page identity")
    if len({f["object_key"] for f in files + pages}) != len(files + pages):
        raise ValueError("duplicate object key")
    identities = identity_tuples(data)
    encoded = json.dumps(identities, separators=(",", ":")).encode("ascii")
    if hashlib.sha256(encoded).hexdigest() != INVENTORY_DIGEST:
        raise ValueError("immutable publication inventory differs")
    return data


def identity_tuples(data: dict) -> list:
    return sorted((f["name"], f["size"], f["sha256"], f["content_type"], f["object_key"])
                  for f in data["files"] + data["page_assets"])


def verify_assets(data: dict, source: Path) -> None:
    """Require the complete delivery set, with no stale or unreviewed files."""
    if {p.name for p in source.iterdir()} != {f["name"] for f in data["files"]}:
        raise ValueError("missing or extra delivery asset")
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
    archive = next(item for item in data["files"] if item["name"] == data["archive"])
    return template.substitute(
        archive_url=data["path"] + archive["name"], archive_name=archive["name"],
        archive_size=f'{archive["size"]:,}', file_rows="\n".join(rows),
        fingerprint=data["fingerprint"], file_count=len(data["files"]),
        package_name=data["package"]["name"], package_digest=data["package"]["sha256"],
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
    verify_assets({"files": data["page_assets"]}, args.output)
    print("Built index.html and styles.css; no release assets copied or changed")


if __name__ == "__main__":
    main()

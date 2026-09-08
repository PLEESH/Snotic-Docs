#!/usr/bin/env python3
"""Validate local Markdown links and generated HTML links and anchors."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel"}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        if "id" in values:
            self.ids.add(values["id"])
        if tag == "a" and "href" in values:
            self.links.append(values["href"])


def markdown_checks(root: Path) -> list[str]:
    failures: list[str] = []
    for path in sorted(root.rglob("*.md")):
        content = path.read_text(encoding="utf-8")
        for raw in MARKDOWN_LINK.findall(content):
            target = raw.strip().split(maxsplit=1)[0].strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme in EXTERNAL_SCHEMES or target.startswith("#"):
                continue
            if parsed.scheme or target.startswith("/"):
                failures.append(f"{path.relative_to(root)}: non-relative link {target}")
                continue
            candidate = (path.parent / unquote(parsed.path)).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError:
                failures.append(f"{path.relative_to(root)}: link escapes docs tree: {target}")
                continue
            if not candidate.exists():
                failures.append(f"{path.relative_to(root)}: missing target: {target}")
    return failures


def parse_html(path: Path) -> LinkParser:
    parser = LinkParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser


def html_target(site_root: Path, source: Path, href: str) -> tuple[Path, str] | None:
    parsed = urlsplit(href)
    if parsed.scheme in EXTERNAL_SCHEMES or href.startswith("//"):
        return None
    raw_path = unquote(parsed.path)
    if raw_path.startswith("/"):
        candidate = site_root / raw_path.lstrip("/")
    elif raw_path:
        candidate = source.parent / raw_path
    else:
        candidate = source
    candidate = candidate.resolve()
    if candidate.is_dir():
        candidate = candidate / "index.html"
    return candidate, unquote(parsed.fragment)


def html_checks(root: Path) -> list[str]:
    failures: list[str] = []
    parsers = {path.resolve(): parse_html(path) for path in sorted(root.rglob("*.html"))}
    for source, parser in parsers.items():
        for href in parser.links:
            resolved = html_target(root.resolve(), source, href)
            if resolved is None:
                continue
            target, anchor = resolved
            try:
                target.relative_to(root.resolve())
            except ValueError:
                failures.append(f"{source.relative_to(root)}: link escapes site: {href}")
                continue
            if not target.exists():
                failures.append(f"{source.relative_to(root)}: missing target: {href}")
                continue
            if anchor and target.suffix.lower() == ".html":
                target_parser = parsers.get(target.resolve())
                if target_parser is None:
                    target_parser = parse_html(target)
                    parsers[target.resolve()] = target_parser
                if anchor not in target_parser.ids:
                    failures.append(f"{source.relative_to(root)}: missing anchor: {href}")
    return failures


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_links.py <tree>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    failures = html_checks(root) if any(root.rglob("*.html")) else markdown_checks(root)
    if failures:
        print("link validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"link validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

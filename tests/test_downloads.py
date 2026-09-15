import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_downloads", ROOT / "scripts/build_downloads.py")
build = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build)


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.downloads = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            self.links.append(attrs.get("href", ""))
            if "download" in attrs:
                self.downloads.append((attrs["href"], attrs["download"]))


class DownloadTests(unittest.TestCase):
    def setUp(self):
        self.data = build.load_inventory(ROOT / "downloads/rc1.json")

    def load(self, data):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.json"
            path.write_text(json.dumps(data))
            return build.load_inventory(path)

    def test_exact_inventory_and_archive_identity(self):
        self.assertEqual(sum(f["size"] for f in self.data["files"]), 12377229)
        for mutation in ("missing", "duplicate", "extra", "path", "size", "hash", "archive", "package", "mime", "signer"):
            with self.subTest(mutation=mutation):
                data = copy.deepcopy(self.data)
                if mutation == "missing":
                    data["files"].pop()
                elif mutation == "duplicate":
                    data["files"][-1] = data["files"][0]
                elif mutation == "extra":
                    data["files"].append(data["files"][0])
                elif mutation == "path":
                    data["files"][0]["name"] = "../unexpected"
                elif mutation == "size":
                    data["files"][1]["size"] = -1
                elif mutation == "hash":
                    data["files"][1]["sha256"] = "not-a-digest"
                elif mutation == "archive":
                    data["files"][0]["sha256"] = "0" * 64
                elif mutation == "package":
                    data["package"]["sha256"] = "0" * 64
                elif mutation == "mime":
                    data["files"][1]["content_type"] = "text/html"
                else:
                    data["fingerprint"] = "0" * 40
                with self.assertRaises(ValueError):
                    self.load(data)

    def test_page_exact_untokened_downloads_and_metadata(self):
        html = build.render(self.data)
        links = Links(html)
        self.assertEqual(len(links.downloads), len(self.data["files"]) + 1)
        self.assertEqual(set(links.downloads), {
            (self.data["path"] + f["name"], f["name"]) for f in self.data["files"]
        })
        for item in self.data["files"]:
            self.assertIn(item["sha256"], html)
            self.assertIn(f'{item["size"]:,} bytes', html)
        for href in links.links:
            self.assertNotIn("?", href)
            self.assertNotIn("github.com", href)
            self.assertNotIn("amazonaws.com", href)
        self.assertIn(build.FINGERPRINT, html)
        self.assertIn(self.data["package"]["sha256"], html)
        self.assertIn(f'{len(self.data["files"])} files', html)
        self.assertIn("Approved public-use eligibility", html)
        self.assertIn("one instance on one server per recipient", html)
        self.assertIn("Publication preparation only", html)
        self.assertNotIn("individually authorized recipients", html)
        self.assertIn("not a stable release", html)
        self.assertNotIn("$", html)
        self.assertEqual(build.render(self.data), html)

    def test_all_immutable_size_and_digest_pairs(self):
        for index, item in enumerate(self.data["files"]):
            for field in ("size", "sha256", "content_type"):
                with self.subTest(file=item["name"], field=field):
                    data = copy.deepcopy(self.data)
                    data["files"][index][field] = {
                        "size": item["size"] + 1,
                        "sha256": "0" * 64,
                        "content_type": "application/gzip" if item["content_type"] != "application/gzip" else "application/pgp-keys",
                    }[field]
                    with self.assertRaisesRegex(ValueError, "immutable"):
                        self.load(data)

    def test_cli_only_builds_two_assets_and_rejects_stale_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "page"
            cmd = [sys.executable, str(ROOT / "scripts/build_downloads.py"), "--output", str(output)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual({p.name for p in output.iterdir()}, {"index.html", "styles.css"})
            self.assertEqual((output / "index.html").read_text(), build.render(self.data))
            self.assertEqual((output / "styles.css").read_bytes(), (ROOT / "downloads/styles.css").read_bytes())
            self.assertIn('href="/styles.css"', (output / "index.html").read_text())
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("output must be empty", result.stderr)

    def test_documentation_direct_downloads_match_inventory(self):
        import re
        text = (ROOT / "docs/self-hosted/0.1.30-rc1/obtain-and-verify.md").read_text()
        urls = re.findall(r"\]\((https://packages\.snotic\.com/self-hosted/[^)]+)\)", text)
        self.assertEqual(len(urls), len(self.data["files"]))
        self.assertEqual(set(urls), {
            "https://packages.snotic.com" + self.data["path"] + item["name"]
            for item in self.data["files"]
        })

    def test_label_is_escaped(self):
        self.data["files"][0]["label"] = '<img src="x" onerror="alert(1)">'
        html = build.render(self.data)
        self.assertNotIn('<img src="x"', html)
        self.assertIn("&lt;img", html)

    def test_private_artifacts_rejected_before_digest_comparison(self):
        bundle = "Snotic-Self-Hosted-0.1.30-rc1-owner-handoff.tar.gz"
        for name in (bundle, bundle + ".asc", bundle + ".sha256", bundle + ".sha256.asc",
                     "producer-custody.json", "producer-custody.json.asc",
                     "recipient-record.json", "private-authorization.json", "immutable-release-assets.json"):
            with self.subTest(name=name):
                data = copy.deepcopy(self.data)
                data["files"][0]["name"] = name
                with self.assertRaisesRegex(ValueError, "private custody"):
                    self.load(data)

    def test_page_and_public_guide_exclude_private_archive(self):
        guide = (ROOT / "docs/self-hosted/0.1.30-rc1/obtain-and-verify.md").read_text()
        for text in (build.render(self.data), guide):
            self.assertNotIn("owner-handoff", text)
            self.assertNotIn("producer-custody", text)
            self.assertNotIn("2ca1f612", text)
        self.assertIn("$file_count", (ROOT / "downloads/page.html").read_text())

    def test_wrong_nested_package_identity_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["package"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "bundle/package identity"):
            self.load(data)

    def test_byte_verification_rejects_changed_missing_and_symlink(self):
        import hashlib
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            asset = root / "synthetic.txt"
            asset.write_bytes(b"synthetic")
            data = {"files": [{"name": asset.name, "size": 9, "sha256": hashlib.sha256(b"synthetic").hexdigest()}]}
            build.verify_assets(data, root)
            asset.write_bytes(b"modified!")
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                build.verify_assets(data, root)
            asset.unlink()
            with self.assertRaisesRegex(ValueError, "missing"):
                build.verify_assets(data, root)
            asset.symlink_to(ROOT / "downloads/rc1.json")
            with self.assertRaisesRegex(ValueError, "non-regular"):
                build.verify_assets(data, root)

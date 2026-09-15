import copy
import importlib.util
import json
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
        self.assertEqual(sum(f["size"] for f in self.data["files"]), 49246632)
        for mutation in ("missing", "duplicate", "extra", "path", "size", "hash", "archive", "signer"):
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
                else:
                    data["fingerprint"] = "0" * 40
                with self.assertRaises(ValueError):
                    self.load(data)

    def test_page_exact_untokened_downloads_and_metadata(self):
        html = build.render(self.data)
        links = Links(html)
        self.assertEqual(len(links.downloads), 11)  # Main action repeats the archive.
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
        self.assertIn("individually authorized recipients", html)
        self.assertIn("not a stable release", html)
        self.assertNotIn("$", html)
        self.assertEqual(build.render(self.data), html)

    def test_label_is_escaped(self):
        self.data["files"][0]["label"] = '<img src="x" onerror="alert(1)">'
        html = build.render(self.data)
        self.assertNotIn('<img src="x"', html)
        self.assertIn("&lt;img", html)

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

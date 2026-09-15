import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
COMPANIONS = ROOT / "downloads/companions"
NOTICE = "Snotic-Self-Hosted-0.1.30-rc1-THIRD-PARTY-NOTICE-ADDENDUM-v1.txt"
SUPPLEMENT = "Snotic-Self-Hosted-0.1.30-rc1-PUBLIC-USE-SUPPLEMENT-v1.txt"
LICENCES = [
    "0688ee39285c33067ad77d82349cdacb5569756bea4398b34bb223af9e57f1c0",
    "7b1e7b898618c53feba37b239e6d1c7de1882f0a6228c92c4800bfe9e58149e6",
    "c08c66f8037c23f20614b58c0cbab6bbacef833dfa9c6a3a00ad3dc3344c2040",
    "3f3d9e0024b1921b067d6f7f88deb4a60cbe7a78e76c64e3f1d7fc3b779b9d04",
    "ec23fc793e0472d7b34129069b71acb3efbfa3700c2317c7819657b30ba52e29",
]


class CompanionTests(unittest.TestCase):
    def setUp(self):
        self.inventory = json.loads((ROOT / "downloads/rc1.json").read_text())

    def test_source_documents_match_signed_inventory(self):
        files = {f["name"]: f for f in self.inventory["files"]}
        self.assertEqual({p.name for p in COMPANIONS.iterdir()}, {NOTICE, SUPPLEMENT})
        for name in (NOTICE, SUPPLEMENT):
            raw = (COMPANIONS / name).read_bytes()
            self.assertEqual(len(raw), files[name]["size"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), files[name]["sha256"])
            for suffix in (".asc", ".sha256", ".sha256.asc"):
                self.assertIn(name + suffix, files)

    def test_exact_upstream_notices_are_complete(self):
        raw = (COMPANIONS / NOTICE).read_text(encoding="ascii")
        blocks = re.findall(r"BEGIN EXACT UPSTREAM LICENCE\n(.*?)END EXACT UPSTREAM LICENCE", raw, re.S)
        self.assertEqual([hashlib.sha256(b.encode("ascii")).hexdigest() for b in blocks], LICENCES)
        self.assertIn("Copyright (c) 2013-2016 container-interop", blocks[0])
        self.assertIn("Copyright (c) 2016 PHP Framework Interoperability Group", blocks[0])

    def test_coverage_accounts_for_actual_payload_not_lock_entries(self):
        raw = (COMPANIONS / NOTICE).read_text()
        coverage = json.loads(raw.split("BEGIN CORRECTED COVERAGE JSON\n")[1].split("\nEND CORRECTED COVERAGE JSON")[0])
        self.assertEqual(coverage["phar_sha256"], "ce34ddd838f7351d6759068d09793f26755463b4a4610a5a5c0a97b68220d85c")
        components = {c["name"]: c for c in coverage["components"]}
        self.assertEqual(len(components), len(coverage["components"]))
        self.assertEqual(len(components), coverage["vendor_component_count"])
        self.assertEqual(sum(c["member_count"] for c in components.values()), coverage["vendor_member_count"])
        self.assertEqual(coverage["vendor_member_count"] + len(coverage["non_vendor_members"]), 1162)
        self.assertEqual(coverage["phar_member_count"], 1162)
        for name, version, members in (("psr/container", "1.0.0", 3), ("wp-cli/wp-cli-tests", "v4.3.14", 11)):
            self.assertEqual(components[name]["version"], version)
            self.assertEqual(components[name]["member_count"], members)
            self.assertEqual(components[name]["notice_status"], "exact-upstream-licence-in-required-addendum")
        self.assertNotIn("symfony/debug", components)
        self.assertNotIn("wp-cli/wp-cli-bundle", components)
        nested = {c["name"]: c for c in coverage["nested_components"]}
        self.assertEqual(set(nested), {"rmccue/requests", "ComplexPie IRI Parser", "Mozilla CA certificate data"})
        self.assertEqual(nested["rmccue/requests"]["version"], "2.0.12")
        self.assertEqual(nested["rmccue/requests"]["member_count"], 66)
        self.assertEqual(nested["Mozilla CA certificate data"]["licence"], "MPL-2.0")
        self.assertEqual(nested["Mozilla CA certificate data"]["member_count"], 1)
        self.assertEqual(nested["ComplexPie IRI Parser"]["member_count"], 1)
        bootstrap = next(m for m in coverage["non_vendor_members"] if m["name"] == "php/boot-phar.php")
        self.assertEqual(bootstrap["notice_component"], "wp-cli/wp-cli-bundle")
        zend = coverage["scoped_adaptations"][0]
        self.assertEqual(zend["original_copied_revision"], "unspecified in shipped source")
        self.assertIn("not the entire utils.php", zend["scope"])
        self.assertEqual(zend["upstream_licence_sha256"], LICENCES[-1])
        self.assertTrue(coverage["retained_source_attributions"])
        for component in components.values():
            self.assertTrue(component["notice_location"])
            self.assertRegex(component["source_commit"], r"^[a-f0-9]{40}$")

    def test_approved_supplement_operative_text_and_exact_binding(self):
        offline = (COMPANIONS / SUPPLEMENT).read_bytes()
        self.assertEqual(hashlib.sha256(offline).hexdigest(), "cb755d684eb36bb1621e6e8031e512b75373d6f30424f569f85f2abd93ba6929")
        page = (ROOT / "docs/self-hosted/0.1.30-rc1/public-use-supplement-v1.md").read_text()
        for part in (offline.decode().split("> This grant applies", 1)[1],):
            self.assertIn(part.rstrip(), page)
        for digest in (self.inventory["package"]["sha256"], next(f["sha256"] for f in self.inventory["files"] if f["name"] == self.inventory["archive"])):
            self.assertIn(digest.encode(), offline)

    def test_generated_delivery_instructions_are_current(self):
        subprocess.run([sys.executable, str(ROOT / "scripts/sync_delivery_docs.py"), "--check"], check=True)

    def test_missing_or_changed_required_file_fails_documented_checksum_command(self):
        spec = importlib.util.spec_from_file_location("delivery", ROOT / "scripts/sync_delivery_docs.py")
        delivery = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(delivery)
        synthetic = b"synthetic document\n"
        data = {"path": self.inventory["path"], "files": [{"name": NOTICE, "label": "Required notice", "sha256": hashlib.sha256(synthetic).hexdigest()}]}
        block = delivery.generated_blocks(data)["CHECKSUMS"].removeprefix("```shell\n").removesuffix("\n```")
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / NOTICE
            for payload, expected in ((synthetic, 0), (b"modified", 1), (None, 1)):
                if payload is None:
                    file.unlink()
                else:
                    file.write_bytes(payload)
                result = subprocess.run(["bash", "-c", block], cwd=tmp, capture_output=True)
                self.assertEqual(result.returncode, expected)

    def run_download_example(self, root, mode):
        spec = importlib.util.spec_from_file_location("delivery", ROOT / "scripts/sync_delivery_docs.py")
        delivery = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(delivery)
        command = delivery.generated_blocks(self.inventory)["COMMAND"].removeprefix("```shell\n").removesuffix("\n```")
        bin_dir = root / "bin"
        bin_dir.mkdir()
        fake_curl = bin_dir / "curl"
        fake_curl.write_text(
            '#!/bin/sh\nprintf "call\\n" >> "$CALL_LOG"\n'
            '[ "$FAIL_CURL" != yes ] || exit 22\n'
            'while [ "$#" -gt 0 ]; do\n'
            '  if [ "$1" = --output ]; then shift; : > "$1"; fi\n'
            '  shift\ndone\n'
        )
        fake_curl.chmod(0o700)
        if mode == "existing-directory":
            (root / "snotic-rc1-download").mkdir()
            (root / "snotic-rc1-download/sentinel").write_text("preserve")
        if mode == "failed-cd":
            fake_mkdir = bin_dir / "mkdir"
            fake_mkdir.write_text("#!/bin/sh\nexit 0\n")
            fake_mkdir.chmod(0o700)
        env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ["PATH"],
                   CALL_LOG=str(root / "calls"), FAIL_CURL="yes" if mode == "failed-download" else "no")
        result = subprocess.run(["bash", "-c", command], cwd=root, env=env, capture_output=True, text=True)
        calls = (root / "calls").read_text().splitlines() if (root / "calls").exists() else []
        return result, calls

    def test_download_example_stops_on_failed_directory_or_first_download(self):
        for mode, expected_calls in (("existing-directory", 0), ("failed-cd", 0), ("failed-download", 1)):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                result, calls = self.run_download_example(root, mode)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertEqual(len(calls), expected_calls)
                if mode == "existing-directory":
                    self.assertEqual((root / "snotic-rc1-download/sentinel").read_text(), "preserve")
                    self.assertEqual(len(list((root / "snotic-rc1-download").iterdir())), 1)

    def test_download_example_requests_every_required_file_on_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result, calls = self.run_download_example(root, "success")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(calls), len(self.inventory["files"]))
            self.assertEqual({p.name for p in (root / "snotic-rc1-download").iterdir()},
                             {f["name"] for f in self.inventory["files"]})

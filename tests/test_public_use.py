import hashlib
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs/self-hosted/0.1.30-rc1"


def normalized_digest(text):
    text = re.sub(r"^> ?", "", text, flags=re.MULTILINE)
    return hashlib.sha256(" ".join(text.split()).encode("utf-8")).hexdigest()


class ApprovedPublicUseTests(unittest.TestCase):
    def test_operative_meaning_matches_owner_approved_revision(self):
        text = (DOCS / "public-use-supplement-v1.md").read_text()
        operative = text.split("> This grant applies", 1)[1].split("## Offline Distribution", 1)[0]
        self.assertEqual(
            normalized_digest("This grant applies" + operative),
            "a909ce25c136f2421908dce7c3979be842692a36e0d55260acac5b19f6e36cb5",
        )
        self.assertIn("Approved and effective: 15 September 2026", text)
        self.assertIn("Snotic-Self-Hosted-0.1.30-rc1-PUBLIC-USE-v1", text)
        for digest in (
            "05bb2729f85cd3f377a4b3b3e0bff19d7905d0b07db21a536572bef6ffd92d08",
            "becfff27cae7e8c8bc9edb2eae629ec873e8a555d83d05d77cf8dee16658aa3e",
            "a266c82caf775f1e7aad41aa26c305efeb06f1c8a9351f2c2879a86674c5e11c",
        ):
            self.assertIn(digest, text)

    def test_original_embedded_grant_body_remains_unchanged(self):
        text = (DOCS / "use-terms.md").read_text()
        original = "Copyright" + text.split("Copyright", 1)[1].split(
            "See the [public third-party notices]", 1
        )[0]
        self.assertEqual(
            normalized_digest(original),
            "6c2bb9c83a6136f280b02c4ad8c1ba3429e7471974a22ba0dd1f591e49fd4acb",
        )

    def test_complete_offline_document_delivery_is_required(self):
        text = (DOCS / "obtain-and-verify.md").read_text()
        self.assertIn("required,", text)
        self.assertIn("not optional links", text)
        self.assertIn("together for offline use", text)
        self.assertIn("Do not install or hand off this partial selection", text)


if __name__ == "__main__":
    unittest.main()

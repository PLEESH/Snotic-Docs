#!/usr/bin/env python3
"""Regression tests for released command and service validation."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_commands.py"


def run_checker(markdown: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as temp_dir:
        docs = Path(temp_dir)
        (docs / "test.md").write_text(markdown, encoding="utf-8")
        return subprocess.run(
            ["python3", str(CHECKER), str(docs)],
            check=False,
            capture_output=True,
            text=True,
        )


class CommandChecksTest(unittest.TestCase):
    def test_released_units_are_accepted(self) -> None:
        result = run_checker(
            "`/opt/hipanel/bin/hipanel` uses `hipanel.service`, "
            "`hipanel-backup.service`, `hipanel-backup.timer`, "
            "`hipanel-ops-alert.service`, and `hipanel-ops-alert.timer`.\n"
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unknown_hipanel_unit_is_rejected(self) -> None:
        result = run_checker(
            "`/opt/hipanel/bin/hipanel` uses `hipanel.service` and "
            "`hipanel-web.service`.\n"
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("units absent from rc1: hipanel-web.service", result.stderr)


if __name__ == "__main__":
    unittest.main()

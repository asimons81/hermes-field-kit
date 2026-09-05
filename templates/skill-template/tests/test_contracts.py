from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
CASES = json.loads((ROOT / "tests" / "cases.json").read_text(encoding="utf-8"))


class SkillContractTests(unittest.TestCase):
    """TEMPLATE ONLY: replace or extend these with skill-specific behavior contracts."""

    def test_workflow_has_checkable_completion_criterion(self):
        self.assertIn("Completion criterion:", SKILL)

    def test_behavior_cases_are_present(self):
        self.assertGreaterEqual(len(CASES["cases"]), 1)
        self.assertTrue(all(case.get("expect") for case in CASES["cases"]))


if __name__ == "__main__":
    unittest.main()

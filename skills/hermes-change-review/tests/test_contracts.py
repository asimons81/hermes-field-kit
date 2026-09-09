from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
CASES = json.loads((ROOT / "tests" / "cases.json").read_text(encoding="utf-8"))


class HermesChangeReviewContractTests(unittest.TestCase):
    def test_three_review_axes_are_independent(self):
        self.assertIn("Intent", SKILL)
        self.assertIn("Repository", SKILL)
        self.assertIn("Verification", SKILL)
        self.assertIn("Keep the axes separate", SKILL)

    def test_missing_intent_is_not_invented(self):
        self.assertIn("Do not invent missing requirements", SKILL)
        self.assertIn("mark the Intent axis `UNVERIFIED`", SKILL)

    def test_review_is_read_only_by_default(self):
        self.assertIn("The review is read-only by default", SKILL)
        self.assertIn("Any repair requires a separate explicit instruction", SKILL)

    def test_green_tests_cannot_override_intent(self):
        self.assertIn("Green-test laundering", SKILL)
        self.assertIn("Passing tests prove only what they exercise", SKILL)

    def test_disposition_rules_are_published(self):
        for disposition in {"ACCEPT", "ACCEPT WITH FINDINGS", "CHANGES REQUIRED", "UNVERIFIED"}:
            with self.subTest(disposition=disposition):
                self.assertIn(disposition, SKILL)
        self.assertIn("any `BLOCKER` -> `CHANGES REQUIRED`", SKILL)

    def test_behavior_cases_cover_trigger_behavior_and_safety(self):
        case_types = {case["type"] for case in CASES["cases"]}
        self.assertTrue({"positive-trigger", "negative-trigger", "behavior", "safety"}.issubset(case_types))
        ids = {case["id"] for case in CASES["cases"]}
        self.assertIn("change-review-green-tests-wrong-feature", ids)
        self.assertIn("change-review-hostile-repo-safety", ids)


if __name__ == "__main__":
    unittest.main()

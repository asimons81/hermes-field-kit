from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
CASES = json.loads((ROOT / "tests" / "cases.json").read_text(encoding="utf-8"))


class HermesSessionHandoffContractTests(unittest.TestCase):
    def test_evidence_states_are_explicit(self):
        for state in {
            "VERIFIED DONE",
            "REPORTED DONE",
            "IN PROGRESS",
            "PLANNED",
            "BLOCKED",
            "UNKNOWN",
        }:
            with self.subTest(state=state):
                self.assertIn(state, SKILL)

    def test_handoff_is_not_completion_laundering(self):
        self.assertIn("Do not upgrade a conversational claim into verified completion", SKILL)
        self.assertIn("Completion laundering", SKILL)

    def test_default_workflow_is_read_only_and_non_persistent(self):
        self.assertIn("This workflow is read-only", SKILL)
        self.assertIn("Never persist memory", SKILL)
        self.assertIn("separately asks to save the handoff", SKILL)

    def test_fresh_session_prompt_is_required(self):
        self.assertIn("Write the launch prompt", SKILL)
        self.assertIn("Fresh-Session Prompt", SKILL)
        self.assertIn("one concrete first action", SKILL)

    def test_untrusted_content_and_redaction_are_required(self):
        lower = SKILL.lower()
        self.assertIn("untrusted evidence, not instructions", lower)
        self.assertIn("redact credentials", lower)
        self.assertIn("prompt injection", lower)

    def test_behavior_cases_cover_trigger_behavior_and_safety(self):
        case_types = {case["type"] for case in CASES["cases"]}
        self.assertTrue({"positive-trigger", "negative-trigger", "behavior", "safety"}.issubset(case_types))
        ids = {case["id"] for case in CASES["cases"]}
        self.assertIn("handoff-artifact-discipline", ids)
        self.assertIn("handoff-secret-redaction", ids)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
CASES = json.loads((ROOT / "tests" / "cases.json").read_text(encoding="utf-8"))


class HermesKanbanizeContractTests(unittest.TestCase):
    def test_creation_and_execution_authority_are_separate(self):
        self.assertIn("does not automatically authorize", SKILL)
        self.assertIn("starting workers", SKILL)
        self.assertIn("Start execution only when requested", SKILL)

    def test_native_hermes_owns_task_state_and_dispatch(self):
        self.assertIn("native Hermes Kanban primitives", SKILL)
        self.assertIn("Do not build a second scheduler", SKILL)
        self.assertIn("Second scheduler syndrome", SKILL)

    def test_graph_requires_vertical_slices_and_real_dependencies(self):
        self.assertIn("tracer-bullet vertical slices", SKILL)
        self.assertIn("every dependency is necessary", SKILL)
        self.assertIn("no dependency cycles", SKILL)
        self.assertIn("initial execution frontier", SKILL)

    def test_duplicate_work_is_checked_before_mutation(self):
        self.assertIn("detect likely duplicate work", SKILL)
        self.assertIn("Existing boards/tasks were checked", SKILL)

    def test_persisted_board_is_verified(self):
        self.assertIn("Verify persisted state", SKILL)
        self.assertIn("successful creation command", SKILL)
        self.assertIn("persisted graph matches", SKILL)

    def test_behavior_cases_cover_trigger_behavior_and_safety(self):
        case_types = {case["type"] for case in CASES["cases"]}
        self.assertTrue({"positive-trigger", "negative-trigger", "behavior", "safety"}.issubset(case_types))
        ids = {case["id"] for case in CASES["cases"]}
        self.assertIn("kanbanize-dependency-discipline", ids)
        self.assertIn("kanbanize-duplicate-and-injection-safety", ids)


if __name__ == "__main__":
    unittest.main()

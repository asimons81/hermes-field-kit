from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
SCRIPT = (ROOT / "scripts" / "today_sessions.py").read_text(encoding="utf-8")
CASES = json.loads((ROOT / "tests" / "cases.json").read_text(encoding="utf-8"))


class WhatHaveWeDoneTodayContractTests(unittest.TestCase):
    def test_required_sections_published(self):
        for section in (
            "## Overview",
            "## When to Use",
            "## Workflow",
            "## Common Pitfalls",
            "## Verification Checklist",
        ):
            with self.subTest(section=section):
                self.assertIn(section, SKILL)

    def test_three_surfaces_published(self):
        lower = SKILL.lower()
        self.assertIn("sessions", lower)
        self.assertIn("kanban", lower)
        self.assertIn("cron", lower)

    def test_read_only_contract_published(self):
        self.assertIn("mode=ro", SKILL)
        self.assertIn("read-only", SKILL.lower())

    def test_append_only_log_contract_published(self):
        self.assertIn("append", SKILL.lower())
        self.assertIn("never overwrite", SKILL.lower())

    def test_manual_trigger_no_cron_contract_published(self):
        self.assertIn("intentionally NOT a cron job", SKILL)
        self.assertIn("Don't install this as a cron", SKILL)

    def test_scanner_implementation_is_read_only(self):
        self.assertIn("mode=ro", SCRIPT)
        self.assertIn("kanban", SCRIPT)
        self.assertIn("boards", SCRIPT)
        self.assertIn("jobs.json", SCRIPT)
        self.assertIn("executions", SCRIPT)
        self.assertNotIn("/home/", SCRIPT)

    def test_behavior_cases_published(self):
        ids = {case["id"] for case in CASES["cases"]}
        for case_id in {
            "positive-trigger-what-done",
            "positive-trigger-closeout",
            "negative-trigger-past-session",
            "negative-trigger-schedule",
            "behavior-append-not-overwrite",
            "safety-read-only-stores",
        }:
            with self.subTest(case_id=case_id):
                self.assertIn(case_id, ids)


if __name__ == "__main__":
    unittest.main()

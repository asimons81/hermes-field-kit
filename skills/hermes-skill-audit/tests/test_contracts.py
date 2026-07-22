from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = (ROOT / "SKILL.md").read_text(encoding="utf-8")
CASES = json.loads((ROOT / "tests" / "contract-cases.json").read_text(encoding="utf-8"))

class ContractTests(unittest.TestCase):
    def test_frontmatter(self):
        self.assertTrue(TEXT.startswith("---\n"))
        for key in ["name:", "description:", "version:", "author:", "license:", "platforms:", "metadata:"]:
            self.assertIn(key, TEXT)

    def test_required_sections(self):
        for heading in ["## Overview", "## When to Use", "## Counter-Triggers", "## Safety Contract", "## Required Procedure", "## Classification", "## Report Contract", "## Common Pitfalls"]:
            self.assertIn(heading, TEXT)

    def test_triggers_are_represented(self):
        lower = TEXT.lower()
        for phrase in CASES["positive_triggers"]:
            words=[w for w in re.findall(r"[a-z0-9]+", phrase.lower()) if len(w) > 3]
            self.assertTrue(any(w in lower for w in words), phrase)

    def test_counter_triggers_are_represented(self):
        lower = TEXT.lower()
        for phrase in CASES["negative_triggers"]:
            words=[w for w in re.findall(r"[a-z0-9]+", phrase.lower()) if len(w) > 3]
            self.assertTrue(any(w in lower for w in words), phrase)

    def test_safety_and_approval(self):
        lower=TEXT.lower()
        self.assertIn("explicit approval", lower)
        self.assertRegex(lower, r"read-only|session-only|do not|never")

    def test_report_headings(self):
        for heading in CASES["report_headings"]:
            self.assertIn(heading, TEXT)

    def test_verdicts(self):
        for verdict in CASES["verdicts"]:
            self.assertIn(verdict, TEXT)

    def test_no_private_paths_or_secrets(self):
        markers = [
            "C:" + "\\Users\\" + "example-user",
            "/home/" + "example-user",
            "internal" + "." + "example",
            "private-" + "knowledge-base",
            "SECRET_" + "TOKEN=",
        ]
        for marker in markers:
            self.assertNotIn(marker, TEXT)

if __name__ == "__main__":
    unittest.main()

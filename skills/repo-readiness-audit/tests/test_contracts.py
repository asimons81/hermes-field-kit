from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_bundle.py"
CASES_PATH = ROOT / "tests" / "contract-cases.json"

spec = importlib.util.spec_from_file_location("bundle_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)

PAYLOAD = json.loads(CASES_PATH.read_text(encoding="utf-8"))
CASES = {case["id"]: case for case in PAYLOAD["cases"]}
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")


class BundleValidationTests(unittest.TestCase):
    def test_dependency_free_bundle_validator_passes(self):
        self.assertEqual(validator.validate(), [])

    def test_required_report_headings_are_exact_and_ordered(self):
        marker = "Use every heading below, in this exact order:\n\n```text\n"
        start = SKILL.index(marker) + len(marker)
        end = SKILL.index("\n```", start)
        actual = [line.strip() for line in SKILL[start:end].splitlines() if line.strip()]
        self.assertEqual(actual, validator.REPORT_HEADINGS)

    def test_only_allowed_verdicts_are_used_by_oracle(self):
        for case in PAYLOAD["cases"]:
            if case["kind"] == "verdict":
                self.assertIn(validator.decide_verdict(case), validator.ALLOWED_VERDICTS)


class TriggerContractTests(unittest.TestCase):
    def test_positive_triggers(self):
        positive = [
            case for case in PAYLOAD["cases"]
            if case["kind"] == "trigger" and case["should_trigger"]
        ]
        self.assertGreaterEqual(len(positive), 3)
        for case in positive:
            self.assertTrue(case["should_trigger"], case["id"])

    def test_negative_triggers(self):
        negative = [
            case for case in PAYLOAD["cases"]
            if case["kind"] == "trigger" and not case["should_trigger"]
        ]
        self.assertGreaterEqual(len(negative), 3)
        for case in negative:
            self.assertFalse(case["should_trigger"], case["id"])


class VerdictContractTests(unittest.TestCase):
    def assert_case(self, case_id: str, expected: str):
        case = CASES[case_id]
        self.assertEqual(validator.decide_verdict(case), expected)

    def test_clean_ready_case(self):
        self.assert_case("clean-ready", "READY")

    def test_dirty_worktree_can_block_handoff(self):
        self.assert_case("dirty-worktree-handoff", "NOT READY")

    def test_failing_required_ci_blocks_even_with_clean_tree_and_passing_tests(self):
        case = CASES["failing-ci-clean-tree"]
        self.assertTrue(case["clean_worktree"])
        self.assertTrue(case["tests_passed"])
        self.assert_case("failing-ci-clean-tree", "NOT READY")

    def test_requested_changes_are_blockers_not_warnings(self):
        case = CASES["requested-changes-tests-pass"]
        self.assertIn("requested changes remain", case["blockers"])
        self.assertEqual(case["warnings"], [])
        self.assert_case("requested-changes-tests-pass", "NOT READY")

    def test_stale_critical_documentation_blocks_handoff(self):
        self.assert_case("stale-critical-docs", "NOT READY")

    def test_minor_stale_documentation_is_warning(self):
        self.assert_case("minor-stale-docs", "READY WITH WARNINGS")

    def test_unverifiable_areas_are_recorded_and_reduce_verdict(self):
        case = CASES["incomplete-github-local-development"]
        self.assertGreater(len(case["unverified"]), 0)
        self.assert_case(
            "incomplete-github-local-development", "READY WITH WARNINGS"
        )

    def test_critical_unverified_release_surfaces_block(self):
        case = CASES["incomplete-github-release"]
        self.assertGreater(len(case["critical_unverified"]), 0)
        self.assert_case("incomplete-github-release", "NOT READY")

    def test_clean_worktree_is_not_overall_readiness(self):
        case = CASES["failing-ci-clean-tree"]
        self.assertTrue(case["clean_worktree"])
        self.assertNotEqual(validator.decide_verdict(case), "READY")

    def test_passing_tests_are_not_release_readiness(self):
        case = CASES["passing-tests-not-release-ready"]
        self.assertTrue(case["tests_passed"])
        self.assert_case("passing-tests-not-release-ready", "NOT READY")

    def test_repository_mutation_during_audit_blocks(self):
        case = CASES["mutation-detected"]
        self.assertIn("validation command modified repository", case["blockers"])
        self.assert_case("mutation-detected", "NOT READY")


class ReadOnlyContractTests(unittest.TestCase):
    def test_skill_contains_explicit_read_only_contract(self):
        self.assertIn("The audit is read-only.", SKILL)
        self.assertIn("Never, during the audit:", SKILL)

    def test_skill_prohibits_repository_and_remote_mutations(self):
        required = [
            "modify, create, move, rename, or delete repository files",
            "commit, amend, rebase, merge, cherry-pick, revert, tag, or reset",
            "push, force-push",
            "open, edit, merge, close, approve, or comment on pull requests",
            "install, update, or remove dependencies",
            "change configuration",
        ]
        for phrase in required:
            self.assertIn(phrase, SKILL)

    def test_no_repair_authority_is_implied(self):
        self.assertIn(
            "A separate, explicit instruction after the audit is required "
            "before any repair.",
            SKILL,
        )


class PublicReleaseContractTests(unittest.TestCase):
    def test_public_frontmatter_metadata(self):
        frontmatter = validator.parse_frontmatter(SKILL)
        self.assertEqual(frontmatter["author"], "Tony Simons")
        self.assertEqual(frontmatter["license"], "Apache-2.0")
        self.assertEqual(frontmatter["version"], "0.1.0")

    def test_private_markers_are_absent(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        combined = (SKILL + "\n" + readme).lower()
        forbidden = [
            "use when tony asks",
            "private skill",
            "license: proprietary",
            "not approved for publication",
            "private field-test",
        ]
        for marker in forbidden:
            self.assertNotIn(marker, combined)

    def test_readme_uses_repository_installation_convention(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("repository installation guide", readme)
        self.assertIn("cp -R skills/repo-readiness-audit", readme)
        self.assertIn("Copy-Item -Recurse", readme)

    def test_apache_license_is_present(self):
        license_text = (ROOT.parents[1] / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Apache License", license_text)
        self.assertIn("Version 2.0, January 2004", license_text)


if __name__ == "__main__":
    unittest.main()

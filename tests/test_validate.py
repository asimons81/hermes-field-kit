from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate.py"
SPEC = importlib.util.spec_from_file_location("field_kit_validate", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


SKILL_BODY = """---
name: example-skill
description: Use when a repeatable example workflow needs disciplined execution.
version: 0.1.0
author: Test Author
license: Apache-2.0
platforms: [platform-agnostic]
metadata:
  hermes:
    category: testing
    tags: [example, testing]
    related_skills: []
---

# Example Skill

## Overview
A minimal test skill.

## When to Use
Use it for tests. Do not use it outside tests.

## Workflow
1. Perform the test and verify an observable result.

## Common Pitfalls
1. Skipping validation.

## Verification Checklist
- [ ] The result is observable.
"""

TEST_CASES = {
    "schema_version": "1.0",
    "cases": [
        {
            "id": "positive-trigger",
            "type": "positive-trigger",
            "prompt": "Run the example workflow.",
            "expect": ["Uses the documented workflow"],
        }
    ],
}


class RepositoryFactory:
    def __init__(self, root: Path) -> None:
        self.root = root
        required = validator.REQUIRED_ROOT_FILES
        for relative in required:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            if relative == "catalog.json":
                path.write_text(
                    json.dumps({"schema_version": "1.0", "skills": []}),
                    encoding="utf-8",
                )
            elif relative.endswith(".json"):
                path.write_text("{}", encoding="utf-8")
            else:
                path.write_text(f"fixture for {relative}\n", encoding="utf-8")
        (root / "skills").mkdir(exist_ok=True)

    def add_skill(self, *, nested: bool = False, catalog: bool = True) -> Path:
        directory = self.root / "skills" / (
            "testing/example-skill" if nested else "example-skill"
        )
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "SKILL.md").write_text(SKILL_BODY, encoding="utf-8")
        (directory / "README.md").write_text("# Example\n", encoding="utf-8")
        (directory / "examples").mkdir()
        (directory / "examples" / "README.md").write_text(
            "# Examples\n", encoding="utf-8"
        )
        (directory / "tests").mkdir()
        (directory / "tests" / "cases.json").write_text(
            json.dumps(TEST_CASES), encoding="utf-8"
        )
        if catalog:
            self.set_catalog(
                [
                    {
                        "name": "example-skill",
                        "category": "testing",
                        "path": "skills/example-skill",
                        "version": "0.1.0",
                        "description": "Use when a repeatable example workflow needs disciplined execution.",
                        "platforms": ["platform-agnostic"],
                        "status": "experimental",
                    }
                ]
            )
        return directory

    def set_catalog(self, skills: list[dict]) -> None:
        (self.root / "catalog.json").write_text(
            json.dumps({"schema_version": "1.0", "skills": skills}),
            encoding="utf-8",
        )


class ValidatorTests(unittest.TestCase):
    def make_repo(
        self,
    ) -> tuple[tempfile.TemporaryDirectory[str], RepositoryFactory]:
        temp = tempfile.TemporaryDirectory()
        return temp, RepositoryFactory(Path(temp.name))

    def assert_error_contains(self, errors: list[str], text: str) -> None:
        self.assertTrue(
            any(text in error for error in errors),
            f"Expected {text!r} in {errors}",
        )

    def test_valid_minimal_tap_skill(self) -> None:
        temp, repo = self.make_repo()
        with temp:
            repo.add_skill()
            self.assertEqual([], validator.validate_repository(repo.root))

    def test_nested_category_layout_is_rejected(self) -> None:
        temp, repo = self.make_repo()
        with temp:
            repo.add_skill(nested=True)
            errors = validator.validate_repository(repo.root)
            self.assert_error_contains(errors, "immediate children of skills/")

    def test_missing_skill_md_is_rejected(self) -> None:
        temp, repo = self.make_repo()
        with temp:
            directory = repo.add_skill()
            (directory / "SKILL.md").unlink()
            errors = validator.validate_repository(repo.root)
            self.assert_error_contains(errors, "SKILL.md is required")

    def test_catalog_only_entry_is_rejected(self) -> None:
        temp, repo = self.make_repo()
        with temp:
            repo.set_catalog(
                [
                    {
                        "name": "ghost-skill",
                        "category": "testing",
                        "path": "skills/ghost-skill",
                        "version": "0.1.0",
                        "description": "Use when a ghost fixture is needed.",
                        "platforms": ["platform-agnostic"],
                        "status": "experimental",
                    }
                ]
            )
            errors = validator.validate_repository(repo.root)
            self.assert_error_contains(errors, "points to missing skill directory")

    def test_skill_without_catalog_entry_is_rejected(self) -> None:
        temp, repo = self.make_repo()
        with temp:
            repo.add_skill(catalog=False)
            errors = validator.validate_repository(repo.root)
            self.assert_error_contains(errors, "missing catalog.json entry")

    def test_mismatched_metadata_path_and_version_are_rejected(self) -> None:
        temp, repo = self.make_repo()
        with temp:
            repo.add_skill()
            base = {
                "name": "example-skill",
                "category": "testing",
                "path": "skills/example-skill",
                "version": "0.1.0",
                "description": "Use when a repeatable example workflow needs disciplined execution.",
                "platforms": ["platform-agnostic"],
                "status": "experimental",
            }

            wrong_path = dict(base, path="skills/wrong-path")
            repo.set_catalog([wrong_path])
            self.assert_error_contains(
                validator.validate_repository(repo.root),
                ".path must be skills/example-skill",
            )

            wrong_category = dict(base, category="wrong-category")
            repo.set_catalog([wrong_category])
            self.assert_error_contains(
                validator.validate_repository(repo.root),
                "catalog category does not match SKILL.md",
            )

            wrong_version = dict(base, version="9.9.9")
            repo.set_catalog([wrong_version])
            self.assert_error_contains(
                validator.validate_repository(repo.root),
                "catalog version does not match SKILL.md",
            )

    def test_invalid_frontmatter_is_rejected(self) -> None:
        temp, repo = self.make_repo()
        with temp:
            directory = repo.add_skill()
            (directory / "SKILL.md").write_text("name: broken\n", encoding="utf-8")
            errors = validator.validate_repository(repo.root)
            self.assert_error_contains(errors, "must start with '---' at byte zero")

    def test_missing_test_cases_are_rejected(self) -> None:
        temp, repo = self.make_repo()
        with temp:
            directory = repo.add_skill()
            (directory / "tests" / "cases.json").unlink()
            errors = validator.validate_repository(repo.root)
            self.assert_error_contains(errors, "cases.json is required")

    def test_duplicate_catalog_names_are_rejected(self) -> None:
        temp, repo = self.make_repo()
        with temp:
            repo.add_skill()
            catalog = json.loads(
                (repo.root / "catalog.json").read_text(encoding="utf-8")
            )
            catalog["skills"].append(dict(catalog["skills"][0]))
            repo.set_catalog(catalog["skills"])
            errors = validator.validate_repository(repo.root)
            self.assert_error_contains(errors, "Duplicate skill name in catalog")

    def test_secret_like_content_is_rejected(self) -> None:
        temp, repo = self.make_repo()
        with temp:
            directory = repo.add_skill()
            marker = "gh" + "p_" + "A" * 36
            (directory / "examples" / "bad.txt").write_text(
                marker, encoding="utf-8"
            )
            errors = validator.validate_repository(repo.root)
            self.assert_error_contains(errors, "possible GitHub token")

    def test_unsafe_support_path_is_rejected(self) -> None:
        temp, repo = self.make_repo()
        with temp:
            directory = repo.add_skill()
            (directory / "hooks").mkdir()
            (directory / "hooks" / "post-install.sh").write_text(
                "echo nope\n", encoding="utf-8"
            )
            errors = validator.validate_repository(repo.root)
            self.assert_error_contains(errors, "unsupported skill path")


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Validate the Hermes Field Kit repository without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
ALLOWED_PLATFORMS = {"linux", "macos", "windows", "platform-agnostic"}
REQUIRED_ROOT_FILES = {
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "LICENSE",
    "README.md",
    "ROADMAP.md",
    "SECURITY.md",
    "SUPPORT.md",
    "catalog.json",
    "schemas/catalog.schema.json",
    "schemas/test-cases.schema.json",
    "skills/README.md",
}
REQUIRED_SKILL_SECTIONS = {
    "## Overview",
    "## When to Use",
    "## Workflow",
    "## Common Pitfalls",
    "## Verification Checklist",
}


class ValidationError(Exception):
    """Raised for a repository validation failure."""


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(errors, f"Missing JSON file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(
            errors,
            f"Invalid JSON in {path.relative_to(ROOT)}:"
            f"{exc.lineno}:{exc.colno}: {exc.msg}",
        )
    return None


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("\"'") for item in inner.split(",")]
    return value.strip("\"'")


def parse_frontmatter(content: str, path: Path, errors: list[str]) -> dict[str, Any]:
    if not content.startswith("---\n"):
        fail(errors, f"{path}: SKILL.md must start with '---' at byte zero")
        return {}
    closing = content.find("\n---\n", 4)
    if closing == -1:
        fail(errors, f"{path}: missing closing frontmatter delimiter")
        return {}

    frontmatter_text = content[4:closing]
    data: dict[str, Any] = {}
    current_top: str | None = None
    current_nested: str | None = None

    for line_number, line in enumerate(frontmatter_text.splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if ":" not in stripped:
            fail(errors, f"{path}:{line_number}: invalid frontmatter line")
            continue
        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        value = parse_scalar(raw_value)

        if indent == 0:
            current_top = key
            current_nested = None
            if raw_value.strip():
                data[key] = value
            else:
                data[key] = {}
        elif indent == 2 and current_top:
            parent = data.setdefault(current_top, {})
            if not isinstance(parent, dict):
                fail(errors, f"{path}:{line_number}: invalid nested mapping")
                continue
            current_nested = key
            if raw_value.strip():
                parent[key] = value
            else:
                parent[key] = {}
        elif indent == 4 and current_top and current_nested:
            parent = data.get(current_top, {})
            nested = parent.get(current_nested, {}) if isinstance(parent, dict) else {}
            if not isinstance(nested, dict):
                fail(errors, f"{path}:{line_number}: invalid nested mapping")
                continue
            nested[key] = value
            parent[current_nested] = nested
        else:
            fail(errors, f"{path}:{line_number}: unsupported frontmatter indentation")

    body = content[closing + len("\n---\n") :].strip()
    if not body:
        fail(errors, f"{path}: SKILL.md body must not be empty")
    data["_body"] = body
    return data


def validate_catalog(catalog: Any, errors: list[str]) -> dict[str, dict[str, Any]]:
    if not isinstance(catalog, dict):
        fail(errors, "catalog.json must contain an object")
        return {}
    if set(catalog) != {"schema_version", "skills"}:
        fail(errors, "catalog.json must contain only schema_version and skills")
    if catalog.get("schema_version") != "1.0":
        fail(errors, "catalog.json schema_version must be 1.0")
    skills = catalog.get("skills")
    if not isinstance(skills, list):
        fail(errors, "catalog.json skills must be an array")
        return {}

    by_path: dict[str, dict[str, Any]] = {}
    names: set[str] = set()
    for index, entry in enumerate(skills):
        prefix = f"catalog.json skills[{index}]"
        if not isinstance(entry, dict):
            fail(errors, f"{prefix} must be an object")
            continue
        required = {
            "name", "category", "path", "version",
            "description", "platforms", "status",
        }
        missing = required - set(entry)
        if missing:
            fail(errors, f"{prefix} missing: {', '.join(sorted(missing))}")
            continue
        name = entry.get("name")
        category = entry.get("category")
        path = entry.get("path")
        if not isinstance(name, str) or not KEBAB.fullmatch(name):
            fail(errors, f"{prefix}.name must be lowercase kebab-case")
        if not isinstance(category, str) or not KEBAB.fullmatch(category):
            fail(errors, f"{prefix}.category must be lowercase kebab-case")
        expected_path = f"skills/{category}/{name}"
        if path != expected_path:
            fail(errors, f"{prefix}.path must be {expected_path}")
        if name in names:
            fail(errors, f"Duplicate skill name in catalog: {name}")
        names.add(name)
        if path in by_path:
            fail(errors, f"Duplicate skill path in catalog: {path}")
        if isinstance(path, str):
            by_path[path] = entry
        if not isinstance(entry.get("version"), str) or not SEMVER.fullmatch(
            entry["version"]
        ):
            fail(errors, f"{prefix}.version must be valid SemVer")
        description = entry.get("description")
        if not isinstance(description, str) or not (1 <= len(description) <= 1024):
            fail(errors, f"{prefix}.description must be 1-1024 characters")
        platforms = entry.get("platforms")
        if (
            not isinstance(platforms, list)
            or not platforms
            or len(platforms) != len(set(platforms))
            or any(platform not in ALLOWED_PLATFORMS for platform in platforms)
        ):
            fail(errors, f"{prefix}.platforms contains invalid values")
        if entry.get("status") not in {"experimental", "stable", "deprecated"}:
            fail(errors, f"{prefix}.status is invalid")
    return by_path


def validate_test_cases(path: Path, errors: list[str]) -> None:
    data = load_json(path, errors)
    if not isinstance(data, dict):
        return
    if set(data) != {"schema_version", "cases"}:
        fail(errors, f"{path.relative_to(ROOT)} must contain schema_version and cases")
    if data.get("schema_version") != "1.0":
        fail(errors, f"{path.relative_to(ROOT)} schema_version must be 1.0")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        fail(errors, f"{path.relative_to(ROOT)} cases must be a nonempty array")
        return
    ids: set[str] = set()
    for index, case in enumerate(cases):
        prefix = f"{path.relative_to(ROOT)} cases[{index}]"
        if not isinstance(case, dict):
            fail(errors, f"{prefix} must be an object")
            continue
        for field in ("id", "type", "prompt", "expect"):
            if field not in case:
                fail(errors, f"{prefix} missing {field}")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not KEBAB.fullmatch(case_id):
            fail(errors, f"{prefix}.id must be lowercase kebab-case")
        elif case_id in ids:
            fail(errors, f"{prefix}.id duplicates {case_id}")
        ids.add(case_id) if isinstance(case_id, str) else None
        if case.get("type") not in {
            "positive-trigger",
            "negative-trigger",
            "behavior",
            "safety",
            "regression",
        }:
            fail(errors, f"{prefix}.type is invalid")
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            fail(errors, f"{prefix}.prompt must be nonempty")
        expect = case.get("expect")
        if (
            not isinstance(expect, list)
            or not expect
            or any(not isinstance(item, str) or not item.strip() for item in expect)
        ):
            fail(errors, f"{prefix}.expect must be a nonempty string array")


def validate_skill(
    directory: Path,
    catalog_entry: dict[str, Any] | None,
    errors: list[str],
) -> None:
    relative_dir = directory.relative_to(ROOT).as_posix()
    category = directory.parent.name
    name = directory.name

    if not KEBAB.fullmatch(category):
        fail(errors, f"{relative_dir}: category must be lowercase kebab-case")
    if not KEBAB.fullmatch(name):
        fail(errors, f"{relative_dir}: skill name must be lowercase kebab-case")
    if len(name) > 64:
        fail(errors, f"{relative_dir}: skill name exceeds 64 characters")

    skill_path = directory / "SKILL.md"
    content = skill_path.read_text(encoding="utf-8")
    if len(content) > 100_000:
        fail(errors, f"{relative_dir}/SKILL.md exceeds 100,000 characters")

    frontmatter = parse_frontmatter(content, skill_path.relative_to(ROOT), errors)
    if not frontmatter:
        return

    required = {
        "name", "description", "version", "author",
        "license", "platforms", "metadata",
    }
    missing = required - set(frontmatter)
    if missing:
        fail(errors, f"{relative_dir}/SKILL.md missing: {', '.join(sorted(missing))}")

    if frontmatter.get("name") != name:
        fail(errors, f"{relative_dir}: frontmatter name must match directory name")
    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.startswith("Use when "):
        fail(errors, f"{relative_dir}: description must begin with 'Use when '")
    if isinstance(description, str) and len(description) > 1024:
        fail(errors, f"{relative_dir}: description exceeds 1024 characters")
    version = frontmatter.get("version")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        fail(errors, f"{relative_dir}: version must be valid SemVer")
    if not str(frontmatter.get("author", "")).strip():
        fail(errors, f"{relative_dir}: author must be nonempty")
    if frontmatter.get("license") != "Apache-2.0":
        fail(errors, f"{relative_dir}: license must be Apache-2.0")
    platforms = frontmatter.get("platforms")
    if (
        not isinstance(platforms, list)
        or not platforms
        or any(platform not in ALLOWED_PLATFORMS for platform in platforms)
    ):
        fail(errors, f"{relative_dir}: platforms contains invalid values")

    metadata = frontmatter.get("metadata")
    hermes = metadata.get("hermes") if isinstance(metadata, dict) else None
    if not isinstance(hermes, dict):
        fail(errors, f"{relative_dir}: metadata.hermes must be a mapping")
    else:
        tags = hermes.get("tags")
        related = hermes.get("related_skills")
        if not isinstance(tags, list) or not tags:
            fail(errors, f"{relative_dir}: metadata.hermes.tags must be nonempty")
        if not isinstance(related, list):
            fail(errors, f"{relative_dir}: metadata.hermes.related_skills must be an array")

    body = frontmatter.get("_body", "")
    for section in REQUIRED_SKILL_SECTIONS:
        if section not in body:
            fail(errors, f"{relative_dir}/SKILL.md missing section: {section}")

    for required_path in (
        directory / "README.md",
        directory / "examples",
        directory / "tests" / "cases.json",
    ):
        if not required_path.exists():
            fail(errors, f"{required_path.relative_to(ROOT)} is required")

    cases_path = directory / "tests" / "cases.json"
    if cases_path.exists():
        validate_test_cases(cases_path, errors)

    if catalog_entry is None:
        fail(errors, f"{relative_dir}: missing catalog.json entry")
    else:
        comparisons = {
            "name": name,
            "category": category,
            "path": relative_dir,
            "version": version,
            "description": description,
            "platforms": platforms,
        }
        for field, expected in comparisons.items():
            if catalog_entry.get(field) != expected:
                fail(
                    errors,
                    f"{relative_dir}: catalog {field} does not match SKILL.md",
                )


def validate_secrets(errors: list[str]) -> None:
    fragments = [
        ("private key", "-----BEGIN " + "PRIVATE KEY-----"),
        ("OpenAI-style key", "sk-" + "proj-"),
        ("GitHub token", "gh" + "p_"),
        ("GitHub fine-grained token", "github_" + "pat_"),
        ("Slack token", "xox" + "b-"),
    ]
    aws_pattern = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
    ignored_parts = {".git", "__pycache__", ".venv", "node_modules"}

    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in ignored_parts for part in path.parts):
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        relative = path.relative_to(ROOT)
        for label, marker in fragments:
            if marker in content:
                fail(errors, f"{relative}: possible {label}")
        if aws_pattern.search(content):
            fail(errors, f"{relative}: possible AWS access key")
        if re.search(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9+/=_-]{20,}", content):
            fail(errors, f"{relative}: possible assigned secret")


def main() -> int:
    errors: list[str] = []

    for required in sorted(REQUIRED_ROOT_FILES):
        if not (ROOT / required).exists():
            fail(errors, f"Missing required repository file: {required}")

    for path in sorted(ROOT.rglob("*.json")):
        load_json(path, errors)

    catalog = load_json(ROOT / "catalog.json", errors)
    catalog_by_path = validate_catalog(catalog, errors)

    skill_files = sorted((ROOT / "skills").glob("*/*/SKILL.md"))
    discovered_paths = {
        skill_file.parent.relative_to(ROOT).as_posix()
        for skill_file in skill_files
    }

    for skill_file in skill_files:
        directory = skill_file.parent
        relative = directory.relative_to(ROOT).as_posix()
        validate_skill(directory, catalog_by_path.get(relative), errors)

    for catalog_path in catalog_by_path:
        if catalog_path not in discovered_paths:
            fail(errors, f"catalog.json points to missing skill directory: {catalog_path}")

    validate_secrets(errors)

    if errors:
        print(f"Validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        "Validation passed: "
        f"{len(discovered_paths)} published skill(s), "
        f"{len(list(ROOT.rglob('*.json')))} JSON file(s), "
        "no common secret patterns detected."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

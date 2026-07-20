#!/usr/bin/env python3
"""Validate Hermes Field Kit repositories with no third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
ALLOWED_PLATFORMS = {"linux", "macos", "windows", "platform-agnostic"}
ALLOWED_SKILL_ENTRIES = {
    "SKILL.md",
    "README.md",
    "examples",
    "tests",
    "references",
    "scripts",
    "templates",
    "assets",
}
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


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(root: Path, path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        add_error(errors, f"Missing JSON file: {path.relative_to(root)}")
    except json.JSONDecodeError as exc:
        add_error(
            errors,
            f"Invalid JSON in {path.relative_to(root)}:"
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


def parse_frontmatter(
    root: Path, content: str, path: Path, errors: list[str]
) -> dict[str, Any]:
    relative = path.relative_to(root)
    if not content.startswith("---\n"):
        add_error(errors, f"{relative}: SKILL.md must start with '---' at byte zero")
        return {}
    closing = content.find("\n---\n", 4)
    if closing == -1:
        add_error(errors, f"{relative}: missing closing frontmatter delimiter")
        return {}

    data: dict[str, Any] = {}
    current_top: str | None = None
    current_nested: str | None = None
    for line_number, line in enumerate(content[4:closing].splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if ":" not in stripped:
            add_error(errors, f"{relative}:{line_number}: invalid frontmatter line")
            continue
        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        value = parse_scalar(raw_value)
        if indent == 0:
            current_top = key
            current_nested = None
            data[key] = value if raw_value.strip() else {}
        elif indent == 2 and current_top:
            parent = data.setdefault(current_top, {})
            if not isinstance(parent, dict):
                add_error(errors, f"{relative}:{line_number}: invalid nested mapping")
                continue
            current_nested = key
            parent[key] = value if raw_value.strip() else {}
        elif indent == 4 and current_top and current_nested:
            parent = data.get(current_top, {})
            nested = parent.get(current_nested, {}) if isinstance(parent, dict) else {}
            if not isinstance(nested, dict):
                add_error(errors, f"{relative}:{line_number}: invalid nested mapping")
                continue
            nested[key] = value
            parent[current_nested] = nested
        else:
            add_error(errors, f"{relative}:{line_number}: unsupported frontmatter indentation")

    body = content[closing + len("\n---\n") :].strip()
    if not body:
        add_error(errors, f"{relative}: SKILL.md body must not be empty")
    data["_body"] = body
    return data


def validate_catalog(
    catalog: Any, errors: list[str]
) -> tuple[dict[str, dict[str, Any]], set[str]]:
    if not isinstance(catalog, dict):
        add_error(errors, "catalog.json must contain an object")
        return {}, set()
    if set(catalog) != {"schema_version", "skills"}:
        add_error(errors, "catalog.json must contain only schema_version and skills")
    if catalog.get("schema_version") != "1.0":
        add_error(errors, "catalog.json schema_version must be 1.0")
    skills = catalog.get("skills")
    if not isinstance(skills, list):
        add_error(errors, "catalog.json skills must be an array")
        return {}, set()

    by_path: dict[str, dict[str, Any]] = {}
    names: set[str] = set()
    for index, entry in enumerate(skills):
        prefix = f"catalog.json skills[{index}]"
        if not isinstance(entry, dict):
            add_error(errors, f"{prefix} must be an object")
            continue
        required = {
            "name",
            "category",
            "path",
            "version",
            "description",
            "platforms",
            "status",
        }
        missing = required - set(entry)
        if missing:
            add_error(errors, f"{prefix} missing: {', '.join(sorted(missing))}")
            continue
        name = entry.get("name")
        category = entry.get("category")
        path = entry.get("path")
        if not isinstance(name, str) or not KEBAB.fullmatch(name):
            add_error(errors, f"{prefix}.name must be lowercase kebab-case")
        if isinstance(name, str) and len(name) > 64:
            add_error(errors, f"{prefix}.name exceeds 64 characters")
        if not isinstance(category, str) or not KEBAB.fullmatch(category):
            add_error(errors, f"{prefix}.category must be lowercase kebab-case")
        expected_path = f"skills/{name}"
        if path != expected_path:
            add_error(errors, f"{prefix}.path must be {expected_path}")
        if isinstance(name, str):
            if name in names:
                add_error(errors, f"Duplicate skill name in catalog: {name}")
            names.add(name)
        if isinstance(path, str):
            if path in by_path:
                add_error(errors, f"Duplicate skill path in catalog: {path}")
            by_path[path] = entry
        version = entry.get("version")
        if not isinstance(version, str) or not SEMVER.fullmatch(version):
            add_error(errors, f"{prefix}.version must be valid SemVer")
        description = entry.get("description")
        if not isinstance(description, str) or not (1 <= len(description) <= 1024):
            add_error(errors, f"{prefix}.description must be 1-1024 characters")
        platforms = entry.get("platforms")
        if (
            not isinstance(platforms, list)
            or not platforms
            or len(platforms) != len(set(platforms))
            or any(platform not in ALLOWED_PLATFORMS for platform in platforms)
        ):
            add_error(errors, f"{prefix}.platforms contains invalid values")
        if entry.get("status") not in {"experimental", "stable", "deprecated"}:
            add_error(errors, f"{prefix}.status is invalid")
    return by_path, names


def validate_test_cases(root: Path, path: Path, errors: list[str]) -> None:
    data = load_json(root, path, errors)
    if not isinstance(data, dict):
        return
    if set(data) != {"schema_version", "cases"}:
        add_error(errors, f"{path.relative_to(root)} must contain schema_version and cases")
    if data.get("schema_version") != "1.0":
        add_error(errors, f"{path.relative_to(root)} schema_version must be 1.0")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        add_error(errors, f"{path.relative_to(root)} cases must be a nonempty array")
        return
    ids: set[str] = set()
    for index, case in enumerate(cases):
        prefix = f"{path.relative_to(root)} cases[{index}]"
        if not isinstance(case, dict):
            add_error(errors, f"{prefix} must be an object")
            continue
        for field in ("id", "type", "prompt", "expect"):
            if field not in case:
                add_error(errors, f"{prefix} missing {field}")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not KEBAB.fullmatch(case_id):
            add_error(errors, f"{prefix}.id must be lowercase kebab-case")
        elif case_id in ids:
            add_error(errors, f"{prefix}.id duplicates {case_id}")
        else:
            ids.add(case_id)
        if case.get("type") not in {
            "positive-trigger",
            "negative-trigger",
            "behavior",
            "safety",
            "regression",
        }:
            add_error(errors, f"{prefix}.type is invalid")
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            add_error(errors, f"{prefix}.prompt must be nonempty")
        expect = case.get("expect")
        if (
            not isinstance(expect, list)
            or not expect
            or any(not isinstance(item, str) or not item.strip() for item in expect)
        ):
            add_error(errors, f"{prefix}.expect must be a nonempty string array")


def validate_skill_support_paths(root: Path, directory: Path, errors: list[str]) -> None:
    for entry in directory.iterdir():
        relative = entry.relative_to(root)
        if entry.name not in ALLOWED_SKILL_ENTRIES:
            add_error(errors, f"{relative}: unsupported skill path")
        if entry.is_symlink():
            add_error(errors, f"{relative}: symlinks are not allowed in published skills")
    for path in directory.rglob("*"):
        if path.is_symlink():
            add_error(errors, f"{path.relative_to(root)}: symlinks are not allowed in published skills")


def validate_skill(
    root: Path,
    directory: Path,
    catalog_entry: dict[str, Any] | None,
    errors: list[str],
) -> None:
    relative_dir = directory.relative_to(root).as_posix()
    name = directory.name
    if not KEBAB.fullmatch(name):
        add_error(errors, f"{relative_dir}: skill name must be lowercase kebab-case")
    if len(name) > 64:
        add_error(errors, f"{relative_dir}: skill name exceeds 64 characters")

    validate_skill_support_paths(root, directory, errors)
    skill_path = directory / "SKILL.md"
    if not skill_path.is_file():
        add_error(errors, f"{relative_dir}/SKILL.md is required")
        return
    content = skill_path.read_text(encoding="utf-8")
    if len(content) > 100_000:
        add_error(errors, f"{relative_dir}/SKILL.md exceeds 100,000 characters")
    frontmatter = parse_frontmatter(root, content, skill_path, errors)
    if not frontmatter:
        return

    required = {
        "name",
        "description",
        "version",
        "author",
        "license",
        "platforms",
        "metadata",
    }
    missing = required - set(frontmatter)
    if missing:
        add_error(errors, f"{relative_dir}/SKILL.md missing: {', '.join(sorted(missing))}")

    if frontmatter.get("name") != name:
        add_error(errors, f"{relative_dir}: frontmatter name must match directory name")
    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.startswith("Use when "):
        add_error(errors, f"{relative_dir}: description must begin with 'Use when '")
    if isinstance(description, str) and len(description) > 1024:
        add_error(errors, f"{relative_dir}: description exceeds 1024 characters")
    version = frontmatter.get("version")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        add_error(errors, f"{relative_dir}: version must be valid SemVer")
    if not str(frontmatter.get("author", "")).strip():
        add_error(errors, f"{relative_dir}: author must be nonempty")
    if frontmatter.get("license") != "Apache-2.0":
        add_error(errors, f"{relative_dir}: license must be Apache-2.0")
    platforms = frontmatter.get("platforms")
    if (
        not isinstance(platforms, list)
        or not platforms
        or len(platforms) != len(set(platforms))
        or any(platform not in ALLOWED_PLATFORMS for platform in platforms)
    ):
        add_error(errors, f"{relative_dir}: platforms contains invalid values")

    metadata = frontmatter.get("metadata")
    hermes = metadata.get("hermes") if isinstance(metadata, dict) else None
    category = None
    if not isinstance(hermes, dict):
        add_error(errors, f"{relative_dir}: metadata.hermes must be a mapping")
    else:
        category = hermes.get("category")
        if not isinstance(category, str) or not KEBAB.fullmatch(category):
            add_error(errors, f"{relative_dir}: metadata.hermes.category must be lowercase kebab-case")
        tags = hermes.get("tags")
        related = hermes.get("related_skills")
        if not isinstance(tags, list) or not tags:
            add_error(errors, f"{relative_dir}: metadata.hermes.tags must be nonempty")
        if not isinstance(related, list):
            add_error(errors, f"{relative_dir}: metadata.hermes.related_skills must be an array")

    body = frontmatter.get("_body", "")
    for section in REQUIRED_SKILL_SECTIONS:
        if section not in body:
            add_error(errors, f"{relative_dir}/SKILL.md missing section: {section}")

    for required_path in (
        directory / "README.md",
        directory / "examples",
        directory / "tests" / "cases.json",
    ):
        if not required_path.exists():
            add_error(errors, f"{required_path.relative_to(root)} is required")
    cases_path = directory / "tests" / "cases.json"
    if cases_path.exists():
        validate_test_cases(root, cases_path, errors)

    if catalog_entry is None:
        add_error(errors, f"{relative_dir}: missing catalog.json entry")
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
                add_error(errors, f"{relative_dir}: catalog {field} does not match SKILL.md")


def validate_tap_layout(root: Path, errors: list[str]) -> list[Path]:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        add_error(errors, "skills/ directory is required")
        return []
    nested = sorted(skills_root.glob("*/*/SKILL.md"))
    for path in nested:
        add_error(
            errors,
            f"{path.relative_to(root)}: Hermes tap skills must be immediate children of skills/",
        )
    immediate_dirs = sorted(
        path for path in skills_root.iterdir() if path.is_dir() and not path.name.startswith(".")
    )
    return immediate_dirs


def validate_secrets(root: Path, errors: list[str]) -> None:
    fragments = [
        ("private key", "-----BEGIN " + "PRIVATE KEY-----"),
        ("OpenAI-style key", "sk-" + "proj-"),
        ("GitHub token", "gh" + "p_"),
        ("GitHub fine-grained token", "github_" + "pat_"),
        ("Slack token", "xox" + "b-"),
    ]
    aws_pattern = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
    assigned_pattern = re.compile(
        r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9+/=_-]{20,}"
    )
    ignored_parts = {".git", "__pycache__", ".venv", "node_modules"}
    for path in root.rglob("*"):
        if not path.is_file() or any(part in ignored_parts for part in path.parts):
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        relative = path.relative_to(root)
        for label, marker in fragments:
            if marker in content:
                add_error(errors, f"{relative}: possible {label}")
        if aws_pattern.search(content):
            add_error(errors, f"{relative}: possible AWS access key")
        if assigned_pattern.search(content):
            add_error(errors, f"{relative}: possible assigned secret")


def validate_repository(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    for required in sorted(REQUIRED_ROOT_FILES):
        if not (root / required).exists():
            add_error(errors, f"Missing required repository file: {required}")
    for path in sorted(root.rglob("*.json")):
        load_json(root, path, errors)

    catalog = load_json(root, root / "catalog.json", errors)
    catalog_by_path, _ = validate_catalog(catalog, errors)
    immediate_dirs = validate_tap_layout(root, errors)
    discovered_paths: set[str] = set()
    for directory in immediate_dirs:
        relative = directory.relative_to(root).as_posix()
        discovered_paths.add(relative)
        validate_skill(root, directory, catalog_by_path.get(relative), errors)
    for catalog_path in catalog_by_path:
        if catalog_path not in discovered_paths:
            add_error(errors, f"catalog.json points to missing skill directory: {catalog_path}")
    validate_secrets(root, errors)
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root to validate (defaults to this checkout).",
    )
    args = parser.parse_args(argv)
    errors = validate_repository(args.root)
    if errors:
        print(f"Validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        return 1
    published = len(
        [
            directory
            for directory in (args.root / "skills").iterdir()
            if directory.is_dir() and (directory / "SKILL.md").is_file()
        ]
    )
    print(
        "Validation passed: "
        f"{published} published skill(s), "
        f"{len(list(args.root.rglob('*.json')))} JSON file(s), "
        "tap layout compatible, no common secret patterns detected."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

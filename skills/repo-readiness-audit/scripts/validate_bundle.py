#!/usr/bin/env python3
"""Dependency-free validator and deterministic contract oracle."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "references/audit-protocol.md",
    "references/evidence-and-access.md",
    "references/report-contract.md",
    "references/verdict-rules.md",
    "examples/clean-ready.md",
    "examples/incomplete-access.md",
    "examples/not-ready-failing-ci.md",
    "scripts/validate_bundle.py",
    "tests/cases.json",
    "tests/contract-cases.json",
    "tests/test_contracts.py",
]

REPORT_HEADINGS = [
    "Repository Readiness Audit",
    "Verdict",
    "Repository State",
    "Recent Work",
    "Pull Requests and Reviews",
    "Issues and Blockers",
    "CI and Tests",
    "Documentation and Plan Alignment",
    "Risks and Warnings",
    "Not Verified",
    "Recommended Next Actions",
    "Evidence Summary",
]

ALLOWED_VERDICTS = {"READY", "READY WITH WARNINGS", "NOT READY"}

PROHIBITED_AUDIT_ACTIONS = [
    "commit, amend, rebase, merge",
    "push, force-push",
    "comment on pull requests",
    "comment on issues",
    "delete branches",
    "install, update, or remove dependencies",
    "change configuration",
    "modify, create, move, rename, or delete repository files",
]


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with frontmatter at byte 0")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter is not closed")
    block = text[4:end]
    result: dict[str, str] = {}
    current_key: str | None = None
    folded: list[str] = []
    for raw in block.splitlines():
        if raw.startswith((" ", "\t")):
            if current_key == "description":
                stripped = raw.strip()
                if stripped:
                    folded.append(stripped)
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", raw)
        if not match:
            continue
        if current_key == "description" and folded:
            result["description"] = " ".join(folded)
            folded = []
        current_key, value = match.groups()
        value = value.strip().strip('"').strip("'")
        if value not in {">-", ">", "|", "|-"}:
            result[current_key] = value
    if current_key == "description" and folded:
        result["description"] = " ".join(folded)
    return result


def decide_verdict(case: dict[str, Any]) -> str:
    blockers = case.get("blockers", [])
    critical_unverified = case.get("critical_unverified", [])
    warnings = case.get("warnings", [])
    unverified = case.get("unverified", [])
    if blockers or critical_unverified:
        return "NOT READY"
    if warnings or unverified:
        return "READY WITH WARNINGS"
    return "READY"


def validate() -> list[str]:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    skill_path = ROOT / "SKILL.md"
    if not skill_path.is_file():
        return errors

    skill = skill_path.read_text(encoding="utf-8")
    try:
        frontmatter = parse_frontmatter(skill)
    except ValueError as exc:
        errors.append(str(exc))
        frontmatter = {}

    expected = {
        "name": "repo-readiness-audit",
        "version": "0.1.0",
        "author": "Tony Simons",
        "license": "Apache-2.0",
    }
    for key, value in expected.items():
        if frontmatter.get(key) != value:
            errors.append(f"frontmatter {key!r} must equal {value!r}")

    description = frontmatter.get("description", "")
    if not description:
        errors.append("frontmatter description is required")
    elif len(description) > 1024:
        errors.append("frontmatter description exceeds 1024 characters")

    if len(skill) > 100_000:
        errors.append("SKILL.md exceeds 100,000 characters")

    forbidden_public_markers = [
        "use when tony asks",
        "private skill",
        "license: proprietary",
        "not approved for publication",
        "private field-test",
    ]
    combined_public_text = skill.lower()
    readme_path = ROOT / "README.md"
    if readme_path.is_file():
        combined_public_text += "\n" + readme_path.read_text(encoding="utf-8").lower()
    for marker in forbidden_public_markers:
        if marker in combined_public_text:
            errors.append(f"public bundle contains private marker: {marker}")

    license_path = ROOT.parents[1] / "LICENSE"
    if license_path.is_file():
        license_text = license_path.read_text(encoding="utf-8")
        if "Apache License" not in license_text or "Version 2.0, January 2004" not in license_text:
            errors.append("LICENSE must contain the Apache License 2.0 text")

    if readme_path.is_file():
        readme = readme_path.read_text(encoding="utf-8")
        required_install_markers = [
            "repository installation guide",
            "cp -R skills/repo-readiness-audit",
            "Copy-Item -Recurse",
        ]
        for marker in required_install_markers:
            if marker not in readme:
                errors.append(f"README is missing install guidance: {marker}")

    for verdict in ALLOWED_VERDICTS:
        if verdict not in skill:
            errors.append(f"missing verdict token in SKILL.md: {verdict}")

    marker = "Use every heading below, in this exact order:\n\n```text\n"
    start = skill.find(marker)
    if start < 0:
        errors.append("required report-heading contract block is missing")
    else:
        start += len(marker)
        end = skill.find("\n```", start)
        if end < 0:
            errors.append("required report-heading contract block is not closed")
        else:
            actual_headings = [
                line.strip()
                for line in skill[start:end].splitlines()
                if line.strip()
            ]
            if actual_headings != REPORT_HEADINGS:
                errors.append(
                    "report headings do not exactly match the required order"
                )

    lower_skill = skill.lower()
    for action in PROHIBITED_AUDIT_ACTIONS:
        if action not in lower_skill:
            errors.append(f"read-only boundary does not mention: {action}")

    cases_path = ROOT / "tests" / "contract-cases.json"
    if cases_path.is_file():
        try:
            payload = json.loads(cases_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"tests/cases.json is invalid JSON: {exc}")
        else:
            if payload.get("skill") != "repo-readiness-audit":
                errors.append("cases.json skill name mismatch")
            ids = [case.get("id") for case in payload.get("cases", [])]
            if len(ids) != len(set(ids)):
                errors.append("cases.json contains duplicate case IDs")
            required_ids = {
                "clean-ready",
                "dirty-worktree-handoff",
                "failing-ci-clean-tree",
                "stale-critical-docs",
                "incomplete-github-local-development",
                "passing-tests-not-release-ready",
                "mutation-detected",
            }
            missing = sorted(required_ids - set(ids))
            if missing:
                errors.append(f"missing required contract cases: {missing}")
            for case in payload.get("cases", []):
                if case.get("kind") == "verdict":
                    actual = decide_verdict(case)
                    expected_verdict = case.get("expected_verdict")
                    if expected_verdict not in ALLOWED_VERDICTS:
                        errors.append(
                            f"{case.get('id')}: invalid expected verdict {expected_verdict!r}"
                        )
                    elif actual != expected_verdict:
                        errors.append(
                            f"{case.get('id')}: oracle returned {actual}, "
                            f"expected {expected_verdict}"
                        )

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: repo-readiness-audit bundle is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
IGNORED_DIRS = {".git", ".venv", "node_modules"}
GENERATED_NAMES = {"__pycache__", ".DS_Store", "Thumbs.db", ".pytest_cache", ".mypy_cache"}
GENERATED_SUFFIXES = {".pyc", ".pyo", ".tmp", ".swp", ".bak"}
PRIVATE_MARKERS = [
    "C:" + "\\Users\\" + "example-user",
    "/home/" + "example-user",
    "internal" + "." + "example",
    "private-" + "knowledge-base",
]
SECRET_FRAGMENTS = [
    ("private key", "-----BEGIN " + "PRIVATE KEY-----"),
    ("OpenAI-style key", "sk-" + "proj-"),
    ("GitHub token", "gh" + "p_"),
    ("GitHub fine-grained token", "github_" + "pat_"),
    ("Slack token", "xox" + "b-"),
]
ASSIGNED_SECRET = re.compile(
    r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\\\"][A-Za-z0-9+/=_-]{20,}"
)
AWS_KEY = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def published_skills() -> list[Path]:
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    return [ROOT / entry["path"] for entry in catalog["skills"]]


def run(command: list[str], cwd: Path) -> tuple[int, str]:
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    return completed.returncode, completed.stdout + completed.stderr


def validate_python(errors: list[str]) -> int:
    count = 0
    for path in ROOT.rglob("*.py"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        count += 1
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, UnicodeDecodeError) as exc:
            errors.append(f"Python syntax failure in {path.relative_to(ROOT)}: {exc}")
    return count


def validate_public_tree(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        relative = path.relative_to(ROOT)
        if path.name in GENERATED_NAMES or path.suffix.lower() in GENERATED_SUFFIXES:
            errors.append(f"generated or temporary artifact present: {relative}")
        if path.is_symlink():
            errors.append(f"symlink present in public tree: {relative}")
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for marker in PRIVATE_MARKERS:
            if marker in content:
                errors.append(f"private marker in {relative}: {marker}")
        for label, marker in SECRET_FRAGMENTS:
            if marker in content:
                errors.append(f"possible {label} in {relative}")
        if AWS_KEY.search(content):
            errors.append(f"possible AWS access key in {relative}")
        if ASSIGNED_SECRET.search(content):
            errors.append(f"possible assigned secret in {relative}")


def validate_markdown_links(errors: list[str]) -> int:
    checked = 0
    for path in ROOT.rglob("*.md"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        content = path.read_text(encoding="utf-8")
        for raw in MARKDOWN_LINK.findall(content):
            target = raw.strip().split()[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue
            checked += 1
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"Markdown link escapes repository in {path.relative_to(ROOT)}: {raw}")
                continue
            if not resolved.exists():
                errors.append(f"broken relative Markdown link in {path.relative_to(ROOT)}: {raw}")
    return checked


def main() -> int:
    failures: list[str] = []
    validators_passed = 0
    tests_passed = 0
    skills = published_skills()

    for skill in skills:
        name = skill.name
        validator = skill / "scripts" / "validate_bundle.py"
        if validator.is_file():
            code, output = run([sys.executable, "-B", str(validator)], skill)
            if code:
                failures.append(f"{name} validator failed:\n{output}")
            else:
                validators_passed += 1

        tests = skill / "tests"
        if not tests.is_dir():
            failures.append(f"{name} has no tests directory")
            continue
        code, output = run(
            [sys.executable, "-B", "-m", "unittest", "discover", "-s", str(tests), "-v"],
            skill,
        )
        match = re.search(r"Ran (\d+) tests?", output)
        if code or not match:
            failures.append(f"{name} contract tests failed:\n{output}")
        else:
            count = int(match.group(1))
            tests_passed += count
            print(f"PASS: {name}: {count} contract tests" + (" + validator" if validator.is_file() else ""))

    python_files = validate_python(failures)
    validate_public_tree(failures)
    links = validate_markdown_links(failures)

    if failures:
        print("\n\n".join(failures))
        return 1

    print(
        "PASS: "
        f"{len(skills)} published skills; "
        f"{validators_passed} bundle validators; "
        f"{tests_passed} contract tests; "
        f"{python_files} Python files parsed; "
        f"{links} relative Markdown links checked; "
        "public-tree hygiene passed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

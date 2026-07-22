#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
skill = root / "SKILL.md"
required = [root / "README.md", root / "references" / "protocol.md", root / "references" / "safety.md", root / "references" / "report-contract.md", root / "examples" / "example-report.md", root / "tests" / "cases.json", root / "tests" / "contract-cases.json", root / "tests" / "test_contracts.py"]
errors=[]
for path in [skill, *required]:
    if not path.is_file():
        errors.append(f"missing: {path.relative_to(root)}")
if skill.is_file():
    text=skill.read_text(encoding="utf-8")
    if not text.startswith("---\n") or text.count("---\n") < 2:
        errors.append("invalid YAML frontmatter boundary")
    for key in ("name:", "description:", "version:", "author:", "license:", "platforms:", "metadata:"):
        if key not in text:
            errors.append(f"missing frontmatter key: {key}")
    banned=[
        "C:" + "\\Users\\" + "example-user",
        "/home/" + "example-user",
        "internal" + "." + "example",
        "private-" + "knowledge-base",
        "SECRET_" + "TOKEN=",
        "api_" + "key:",
    ]
    for marker in banned:
        if marker in text:
            errors.append(f"private or secret-bearing marker present: {marker}")
    if "explicit approval" not in text.lower():
        errors.append("missing explicit-approval boundary")
if errors:
    print("FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)
print(f"PASS: {root.name} bundle is valid")

#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE_SKILLS = (
    'repo-readiness-audit',
    'interview-me',
    'hermes-skill-audit',
    'hermes-update-doctor',
    'pre-build-feature-audit',
    'hermes-environment-migration',
    'hermes-gateway-doctor',
    'oss-tool-trust-audit',
    'hermes-profile-audit',
    'hermes-token-audit',
    'hermes-stack-doctor',
)

failures: list[str] = []
validators_passed = 0
tests_passed = 0

for name in RELEASE_SKILLS:
    skill = ROOT / 'skills' / name
    validator = subprocess.run(
        [sys.executable, str(skill / 'scripts' / 'validate_bundle.py')],
        cwd=skill,
        text=True,
        capture_output=True,
    )
    if validator.returncode:
        failures.append(
            f'{name} validator failed:\n{validator.stdout}{validator.stderr}'
        )
    else:
        validators_passed += 1

    tests = subprocess.run(
        [
            sys.executable,
            '-m',
            'unittest',
            'discover',
            '-s',
            str(skill / 'tests'),
            '-v',
        ],
        cwd=skill,
        text=True,
        capture_output=True,
    )
    output = tests.stdout + tests.stderr
    match = re.search(r'Ran (\d+) tests?', output)
    if tests.returncode or not match:
        failures.append(f'{name} contract tests failed:\n{output}')
        count = 0
    else:
        count = int(match.group(1))
        tests_passed += count

    if validator.returncode == 0 and tests.returncode == 0 and match:
        print(f'PASS: {name}: validator + {count} contract tests')

if failures:
    print('\n\n'.join(failures))
    raise SystemExit(f'FAIL: {len(failures)} release validation checks failed')

print(
    'PASS: '
    f'{len(RELEASE_SKILLS)} Field Kit skill bundles; '
    f'{validators_passed} validators; '
    f'{tests_passed} contract tests'
)

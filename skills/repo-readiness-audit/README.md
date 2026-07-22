# repo-readiness-audit

Open-source Hermes Agent skill, version **0.1.0**.

`repo-readiness-audit` determines whether an identified Git repository is ready
for further development, a new feature, handoff, contributor onboarding, or
release work. It performs a disciplined read-only audit and issues exactly one
verdict:

- `READY`
- `READY WITH WARNINGS`
- `NOT READY`

A clean working tree or passing test suite is never treated as proof of overall
readiness. Git state, remote collaboration, CI, documentation, dependencies,
unfinished work, and unavailable evidence are evaluated separately.

## Install

Install from Hermes Field Kit as a tap using the command supported by your installed Hermes version, or copy this skill directory into your local Hermes skills tree. See the [repository installation guide](../../docs/installation.md).

Linux or macOS:

```bash
mkdir -p ~/.hermes/skills
cp -R skills/repo-readiness-audit ~/.hermes/skills/
```

PowerShell:

```powershell
$destination = Join-Path $env:LOCALAPPDATA "hermes\skills"
New-Item -ItemType Directory -Force $destination | Out-Null
Copy-Item -Recurse "skills\repo-readiness-audit" $destination
```

Start a fresh Hermes session after installation because skill discovery may be cached.
## Bundle

```text
repo-readiness-audit/
├── SKILL.md
├── README.md
├── LICENSE
├── references/
│   ├── audit-protocol.md
│   ├── evidence-and-access.md
│   ├── report-contract.md
│   └── verdict-rules.md
├── examples/
│   ├── clean-ready.md
│   ├── incomplete-access.md
│   └── not-ready-failing-ci.md
├── scripts/
│   └── validate_bundle.py
└── tests/
    ├── cases.json
    └── test_contracts.py
```

## Safety

The skill is read-only. During an audit it does not modify repositories, install
dependencies, run migrations, repair findings, commit, push, merge, edit pull
requests, or perform other repository or GitHub write actions. Repairs require a
separate explicit instruction after the audit report.

## Validation

The validator and deterministic contract tests use only the Python standard
library.

```bash
python scripts/validate_bundle.py
python -m unittest discover -s tests -v
```

The contracts verify trigger boundaries, exact report headings, verdict rules,
read-only behavior, incomplete-access handling, dirty-worktree and failing-CI
cases, stale documentation, clean-ready behavior, and the distinction between
local cleanliness, passing tests, and overall repository readiness.

## License

Apache License 2.0. See the repository [`LICENSE`](../../LICENSE).

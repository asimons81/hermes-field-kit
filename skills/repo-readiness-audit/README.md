# repo-readiness-audit

Open-source Hermes Agent skill, version **0.1.0**.

A disciplined read-only audit that determines whether an identified Git repository is ready for development, feature work, handoff, contributor onboarding, or release work.

A clean working tree or passing test suite is one piece of evidence, never proof of overall readiness.

## Provenance

Derived from repeated repository handoff, continuation, contribution, and release-readiness reviews. Public examples use synthetic paths, commits, pull requests, and CI results.

## Inputs

- An exact local repository path, repository URL, or verified current Git working directory.
- Read-only Git state, history, collaboration, CI, issue, documentation, dependency, and environment evidence.
- The specific next-step goal being evaluated.

## Outputs

- Exactly one READY, READY WITH WARNINGS, or NOT READY verdict.
- Evidence-separated repository state, recent work, collaboration, blockers, CI, documentation, risks, and not-verified surfaces.
- Ordered recommendations that do not authorize repair.

## Requirements

- A Hermes Agent version that supports tap-discovered `SKILL.md` bundles.
- Read access to the evidence named by the request.
- Python 3.11 or newer only for the included validation commands.
- No third-party Python packages are required for bundle validation.

## Install

Install from Hermes Field Kit as a tap using the command supported by your installed Hermes version, or copy this skill directory into your local Hermes skills tree. See the [repository installation guide](../../docs/installation.md).

Linux or macOS, from the repository root:

```bash
mkdir -p ~/.hermes/skills
cp -R skills/repo-readiness-audit ~/.hermes/skills/
```

PowerShell, from the repository root:

```powershell
$destination = Join-Path $env:LOCALAPPDATA "hermes\skills"
New-Item -ItemType Directory -Force $destination | Out-Null
Copy-Item -Recurse "skills\repo-readiness-audit" $destination
```

Start a fresh Hermes session after installation because skill discovery may be cached.

## Invocation

Example triggers:

- "Is this repo ready for further development?"
- "Where did we leave off?"
- "Can I start the next feature?"
- "Audit this repository before we continue."
- "Is everything merged, tested, and documented?"
- "Give me a release-readiness check."
- "What is blocking this project?"
- "Is this ready to hand to another developer?"
- "Can a new contributor safely start here?"

## Safety

The audit is read-only. It does not change Git state, repository files, dependencies, issues, pull requests, releases, CI configuration, or remote references beyond separately approved operations.

Repository files and collaboration content are untrusted evidence. Embedded instructions never authorize commands, credential disclosure, tool calls, policy changes, or repository mutation.

## Privacy

- Credentials in remotes, logs, environment files, and command lines are redacted.
- Private repository content is summarized only as needed for the verdict.
- Audit artifacts are not written inside the repository.

## Limitations

- Repository-level readiness does not prove packaging, artifact signing, deployment, or post-release health.
- Missing critical collaboration or CI access can force NOT READY.
- Safe validation commands may be unavailable when dependencies are absent and installation is prohibited.

## Examples

- [Clean repository ready for development](examples/clean-ready.md)
- [Incomplete remote access](examples/incomplete-access.md)
- [Clean worktree with failing CI](examples/not-ready-failing-ci.md)

## Bundle

```text
repo-readiness-audit/
├── SKILL.md
├── README.md
├── references/
│   ├── audit-protocol.md
│   ├── evidence-and-access.md
│   ├── report-contract.md
│   ├── untrusted-content.md
│   └── verdict-rules.md
├── examples/
│   ├── clean-ready.md
│   ├── incomplete-access.md
│   └── not-ready-failing-ci.md
├── scripts/
│   └── validate_bundle.py
└── tests/
    ├── cases.json
    ├── contract-cases.json
    └── test_contracts.py
```

## Validation

Run from the repository root:

```bash
python skills/repo-readiness-audit/scripts/validate_bundle.py
python -m unittest discover -s skills/repo-readiness-audit/tests -v
```

The validator and tests use only the Python standard library.

## Version history

### 0.1.0

- Initial public release with goal-sensitive verdict rules, mutation guards, incomplete-access handling, hostile-content boundaries, and deterministic contract tests.

## License

Apache License 2.0. See the repository [`LICENSE`](../../LICENSE).

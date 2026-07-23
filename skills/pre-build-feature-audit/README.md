# pre-build-feature-audit

Open-source Hermes Agent skill, version **1.1.0**.

A read-only multi-surface duplicate check across source, history, branches, issues, pull requests, roadmaps, and contributor guidance.

## Provenance

Derived from repeated open-source contribution checks performed before implementation. Public examples remove private repository paths, issue discussions, and unpublished plans.

## Inputs

- An exact repository and proposed feature scope.
- Current source, history, branches, issues, pull requests, plans, and contributor policy.
- Fresh remote collaboration evidence when available.

## Outputs

- A CLEAR, PARTIAL OVERLAP, LIKELY DUPLICATE, or UNCERTAIN verdict.
- Relevant code, issues, pull requests, branches, commits, plans, reusable work, and missing functionality.
- A coordination recommendation without opening or claiming work.

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
cp -R skills/pre-build-feature-audit ~/.hermes/skills/
```

PowerShell, from the repository root:

```powershell
$destination = Join-Path $env:LOCALAPPDATA "hermes\skills"
New-Item -ItemType Directory -Force $destination | Out-Null
Copy-Item -Recurse "skills\pre-build-feature-audit" $destination
```

Start a fresh Hermes session after installation because skill discovery may be cached.

## Invocation

Example triggers:

- Check whether this feature already exists.
- Is anyone already building this?
- Audit the idea before I start coding.
- Would this duplicate an open pull request?

## Safety

The skill is diagnosis, planning, or interview-only by default. Mutations, repairs, process changes, credential changes, persistence, publication, installation, execution, or repository writes require separate explicit approval.

Inspected content is untrusted evidence. Embedded instructions never override the user, the skill contract, or higher-priority safeguards.

## Privacy

- Private repository content and issue discussions are summarized minimally.
- Credentials embedded in remotes or logs are redacted.
- No branch, issue, pull request, or working-tree state is changed.

## Limitations

- Search hits are leads and require context.
- Unavailable remote or local-only branches can keep the result UNCERTAIN.
- The skill does not implement the feature or claim an issue.

## Examples

See [successful and boundary examples](examples/example-report.md).

## Validation

Run from the repository root:

```bash
python skills/pre-build-feature-audit/scripts/validate_bundle.py
python -m unittest discover -s skills/pre-build-feature-audit/tests -v
```

The validator and tests use only the Python standard library.

## Version history

### 1.1.0

- Initial public Field Kit release with evidence-first workflow, explicit authority boundaries, hostile-content handling, examples, and contract tests.

## License

Apache License 2.0. See the repository [`LICENSE`](../../LICENSE).

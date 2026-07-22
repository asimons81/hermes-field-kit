# pre-build-feature-audit

Open-source Hermes Agent skill, version **1.1.0**.

A read-only multi-surface duplicate check across source, history, branches, issues, pull requests, roadmaps, and contributor guidance.

## Install

Install from Hermes Field Kit as a tap using the command supported by your installed Hermes version, or copy this skill directory into your local Hermes skills tree. See the [repository installation guide](../../docs/installation.md).

Linux or macOS:

```bash
mkdir -p ~/.hermes/skills
cp -R skills/pre-build-feature-audit ~/.hermes/skills/
```

PowerShell:

```powershell
$destination = Join-Path $env:LOCALAPPDATA "hermes\skills"
New-Item -ItemType Directory -Force $destination | Out-Null
Copy-Item -Recurse "skills\pre-build-feature-audit" $destination
```

Start a fresh Hermes session after installation because skill discovery may be cached.
## Example triggers

- Check whether this feature already exists.
- Is anyone already building this?
- Audit the idea before I start coding.
- Would this duplicate an open pull request?

## Safety

This bundle preserves a diagnosis, planning, or interview boundary. Any external mutation or durable write requires separate explicit approval.

## Validation

```bash
python scripts/validate_bundle.py
python -m unittest discover -s tests -v
```

The validator and tests use only the Python standard library.

## License

Apache License 2.0. See the repository [`LICENSE`](../../LICENSE).

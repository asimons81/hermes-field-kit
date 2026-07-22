# hermes-environment-migration

Open-source Hermes Agent skill, version **1.0.0**.

A platform-aware migration protocol that refuses blind copies of machine-bound state and separates ordinary configuration from credentials and encrypted vault material.

## Install

Install from Hermes Field Kit as a tap using the command supported by your installed Hermes version, or copy this skill directory into your local Hermes skills tree. See the [repository installation guide](../../docs/installation.md).

Linux or macOS:

```bash
mkdir -p ~/.hermes/skills
cp -R skills/hermes-environment-migration ~/.hermes/skills/
```

PowerShell:

```powershell
$destination = Join-Path $env:LOCALAPPDATA "hermes\skills"
New-Item -ItemType Directory -Force $destination | Out-Null
Copy-Item -Recurse "skills\hermes-environment-migration" $destination
```

Start a fresh Hermes session after installation because skill discovery may be cached.
## Example triggers

- Move my Hermes setup to a new machine.
- Prepare a Hermes migration export.
- Verify and import this Hermes archive.
- Migrate profiles, skills, memory, and cron safely.

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

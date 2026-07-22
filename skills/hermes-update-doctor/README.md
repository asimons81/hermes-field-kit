# hermes-update-doctor

Open-source Hermes Agent skill, version **1.0.0**.

A diagnosis-first update investigator that separates remote drift, repository divergence, process locks, stale caches, partial installs, and runtime-version mismatches.

## Install

Install from Hermes Field Kit as a tap using the command supported by your installed Hermes version, or copy this skill directory into your local Hermes skills tree. See the [repository installation guide](../../docs/installation.md).

Linux or macOS:

```bash
mkdir -p ~/.hermes/skills
cp -R skills/hermes-update-doctor ~/.hermes/skills/
```

PowerShell:

```powershell
$destination = Join-Path $env:LOCALAPPDATA "hermes\skills"
New-Item -ItemType Directory -Force $destination | Out-Null
Copy-Item -Recurse "skills\hermes-update-doctor" $destination
```

Start a fresh Hermes session after installation because skill discovery may be cached.
## Example triggers

- Hermes says it is behind but will not update.
- Update says already current but the version is stale.
- Another Hermes process is blocking the update.
- Diagnose a failed Hermes update.

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

# hermes-skill-audit

Open-source Hermes Agent skill, version **1.0.0**.

A read-only health audit for global and profile-local Hermes skills, including dependency references, frontmatter, usage metadata, cron dependencies, duplicates, and upstream drift.

## Install

Install from Hermes Field Kit as a tap using the command supported by your installed Hermes version, or copy this skill directory into your local Hermes skills tree. See the [repository installation guide](../../docs/installation.md).

Linux or macOS:

```bash
mkdir -p ~/.hermes/skills
cp -R skills/hermes-skill-audit ~/.hermes/skills/
```

PowerShell:

```powershell
$destination = Join-Path $env:LOCALAPPDATA "hermes\skills"
New-Item -ItemType Directory -Force $destination | Out-Null
Copy-Item -Recurse "skills\hermes-skill-audit" $destination
```

Start a fresh Hermes session after installation because skill discovery may be cached.
## Example triggers

- Audit my installed Hermes skills.
- Find duplicate or broken skills.
- Which skills are stale or unused?
- Check skill references before cleanup.

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

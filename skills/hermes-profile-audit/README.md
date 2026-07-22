# hermes-profile-audit

Open-source Hermes Agent skill, version **1.0.0**.

A read-only profile assessment that compares declared responsibilities to actual tools, skills, persistence, access, and observed behavior without rewriting the profile automatically.

## Install

Install from Hermes Field Kit as a tap using the command supported by your installed Hermes version, or copy this skill directory into your local Hermes skills tree. See the [repository installation guide](../../docs/installation.md).

Linux or macOS:

```bash
mkdir -p ~/.hermes/skills
cp -R skills/hermes-profile-audit ~/.hermes/skills/
```

PowerShell:

```powershell
$destination = Join-Path $env:LOCALAPPDATA "hermes\skills"
New-Item -ItemType Directory -Force $destination | Out-Null
Copy-Item -Recurse "skills\hermes-profile-audit" $destination
```

Start a fresh Hermes session after installation because skill discovery may be cached.
## Example triggers

- Audit this Hermes profile.
- Why does this profile keep making the same mistake?
- Check whether the profile has too much access.
- Review the profile before we rely on it.

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

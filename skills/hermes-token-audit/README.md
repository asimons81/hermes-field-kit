# hermes-token-audit

Open-source Hermes Agent skill, version **1.0.0**.

A read-only, schema-discovering token and cost audit that defaults to aggregate metadata and clearly separates local estimates from provider billing.

## Install

Install from Hermes Field Kit as a tap using the command supported by your installed Hermes version, or copy this skill directory into your local Hermes skills tree. See the [repository installation guide](../../docs/installation.md).

Linux or macOS:

```bash
mkdir -p ~/.hermes/skills
cp -R skills/hermes-token-audit ~/.hermes/skills/
```

PowerShell:

```powershell
$destination = Join-Path $env:LOCALAPPDATA "hermes\skills"
New-Item -ItemType Directory -Force $destination | Out-Null
Copy-Item -Recurse "skills\hermes-token-audit" $destination
```

Start a fresh Hermes session after installation because skill discovery may be cached.
## Example triggers

- Where did my Hermes tokens go?
- Which sessions cost the most?
- Did a cron job burn the budget?
- Why does provider billing not match local usage?

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

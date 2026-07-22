# hermes-gateway-doctor

Open-source Hermes Agent skill, version **1.0.0**.

A read-only gateway doctor that verifies the actual process instead of trusting stale state files and keeps credential handling out of command history and reports.

## Install

Install from Hermes Field Kit as a tap using the command supported by your installed Hermes version, or copy this skill directory into your local Hermes skills tree. See the [repository installation guide](../../docs/installation.md).

Linux or macOS:

```bash
mkdir -p ~/.hermes/skills
cp -R skills/hermes-gateway-doctor ~/.hermes/skills/
```

PowerShell:

```powershell
$destination = Join-Path $env:LOCALAPPDATA "hermes\skills"
New-Item -ItemType Directory -Force $destination | Out-Null
Copy-Item -Recurse "skills\hermes-gateway-doctor" $destination
```

Start a fresh Hermes session after installation because skill discovery may be cached.
## Example triggers

- Telegram stopped responding through Hermes.
- Is my Hermes gateway actually running?
- Diagnose a gateway polling conflict.
- Why are scheduled messages not delivering?

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

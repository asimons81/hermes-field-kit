# oss-tool-trust-audit

Open-source Hermes Agent skill, version **1.0.0**.

An evidence-driven trust audit that reads source and release machinery, treats popularity as context rather than proof, and separates technical legitimacy from adoption fit.

## Install

Install from Hermes Field Kit as a tap using the command supported by your installed Hermes version, or copy this skill directory into your local Hermes skills tree. See the [repository installation guide](../../docs/installation.md).

Linux or macOS:

```bash
mkdir -p ~/.hermes/skills
cp -R skills/oss-tool-trust-audit ~/.hermes/skills/
```

PowerShell:

```powershell
$destination = Join-Path $env:LOCALAPPDATA "hermes\skills"
New-Item -ItemType Directory -Force $destination | Out-Null
Copy-Item -Recurse "skills\oss-tool-trust-audit" $destination
```

Start a fresh Hermes session after installation because skill discovery may be cached.
## Example triggers

- Is this viral GitHub tool safe?
- Audit this npm package before I install it.
- Does this CLI phone home?
- Should we use, fork, build, or skip this tool?

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

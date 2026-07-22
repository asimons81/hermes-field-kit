# hermes-stack-doctor

Open-source Hermes Agent skill, version **1.0.0**.

A capstone health check that discovers the installation architecture, delegates to focused evidence contracts, and reports one GREEN, YELLOW, or RED verdict without repairing the stack.

## Install

Install from Hermes Field Kit as a tap using the command supported by your installed Hermes version, or copy this skill directory into your local Hermes skills tree. See the [repository installation guide](../../docs/installation.md).

Linux or macOS:

```bash
mkdir -p ~/.hermes/skills
cp -R skills/hermes-stack-doctor ~/.hermes/skills/
```

PowerShell:

```powershell
$destination = Join-Path $env:LOCALAPPDATA "hermes\skills"
New-Item -ItemType Directory -Force $destination | Out-Null
Copy-Item -Recurse "skills\hermes-stack-doctor" $destination
```

Start a fresh Hermes session after installation because skill discovery may be cached.
## Example triggers

- Is my Hermes stack healthy?
- Run a complete Hermes doctor.
- Can I trust scheduled automation right now?
- Audit the installation after migration or update.

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

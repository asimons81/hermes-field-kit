# interview-me

Open-source Hermes Agent skill, version **0.2.0**.

An adaptive interview protocol that asks one high-value question at a time, inspects available sources before questioning the user, and stops when more questions would not change the next action.

## Install

Install from Hermes Field Kit as a tap using the command supported by your installed Hermes version, or copy this skill directory into your local Hermes skills tree. See the [repository installation guide](../../docs/installation.md).

Linux or macOS:

```bash
mkdir -p ~/.hermes/skills
cp -R skills/interview-me ~/.hermes/skills/
```

PowerShell:

```powershell
$destination = Join-Path $env:LOCALAPPDATA "hermes\skills"
New-Item -ItemType Directory -Force $destination | Out-Null
Copy-Item -Recurse "skills\interview-me" $destination
```

Start a fresh Hermes session after installation because skill discovery may be cached.
## Example triggers

- Interview me before you start.
- Ask me questions so you understand what I want.
- Help me turn this rough idea into a decision brief.
- Learn my preferences before drafting the plan.

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

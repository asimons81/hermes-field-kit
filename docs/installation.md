# Installation

Published skills can be installed through a Hermes tap or copied manually from this repository. Review each skill before installation.

## Requirements

- Hermes Agent with the `hermes skills tap` and `hermes skills install` commands.
- Network access to GitHub for tap discovery and installation.
- A new Hermes session after installation or removal because skill discovery may be cached per session.

The v1.0.0 release gate used Hermes Agent v0.19.0 (2026.7.20), Python 3.11.15, on Windows 11. See [Compatibility](compatibility.md).

## Install as a Hermes tap

Add the repository once:

```bash
hermes skills tap add asimons81/hermes-field-kit
```

Search for a skill:

```bash
hermes skills search hermes-stack-doctor
```

Inspect a skill before installing:

```bash
hermes skills inspect asimons81/hermes-field-kit/hermes-stack-doctor
```

Install it:

```bash
hermes skills install asimons81/hermes-field-kit/hermes-stack-doctor --yes
```

Replace `hermes-stack-doctor` with any published skill name. Hermes records the source repository and exact commit in its hub metadata.

## Verify installation

```bash
hermes skills list
hermes skills audit
```

Start a new Hermes session and use a documented positive trigger from the selected skill's `SKILL.md`. Also verify a documented counter-trigger does not load it.

## Update a tap-installed skill

Check for available updates, then update the selected skill:

```bash
hermes skills check
hermes skills update hermes-stack-doctor
```

Review upstream changes before updating consequential or write-capable skills.

## Remove a tap-installed skill

```bash
hermes skills uninstall hermes-stack-doctor
```

Start a new Hermes session after removal.

## Install one skill manually

Hermes discovers user-local skills under:

```text
~/.hermes/skills/<optional-category>/<skill-name>/SKILL.md
```

From a clone, copy a selected skill directory into your local tree.

Linux or macOS:

```bash
mkdir -p ~/.hermes/skills
cp -R skills/<skill-name> ~/.hermes/skills/
```

PowerShell:

```powershell
$destination = Join-Path $env:LOCALAPPDATA "hermes\skills"
New-Item -ItemType Directory -Force $destination | Out-Null
Copy-Item -Recurse "skills\<skill-name>" $destination
```

## Manual and pinned-review lifecycle

Use the lifecycle that matches the installation method:

- **Tap-installed skill:** use Hermes `skills update` and `skills uninstall`.
- **Manually copied skill:** replace or remove the complete installed skill directory.
- **Pinned raw-URL review install:** treat it as a one-commit verification artifact. Reinstall from the newly selected commit rather than assuming in-place update support.

Do not mix lifecycle methods. A raw URL pinned to one commit is not evidence that the repository's normal tap-update path is broken.

## Safety

Installation does not grant authorization for consequential actions. Review tool requirements, scripts, approval boundaries, and untrusted-content handling before use.

# Installation

Published skills can be installed through Hermes' community registry resolution or copied manually from this repository. Review each skill before installation.

## Requirements

- Hermes Agent with `hermes skills inspect`, `install`, `check`, `update`, and `uninstall`.
- Network access to GitHub and the configured skill registries.
- A new Hermes session after installation or removal because skill discovery may be cached per session.

The v1.0.1 corrective release was validated with Hermes Agent v0.19.0 (2026.7.20), Python 3.11.15, on Windows 11. See [Compatibility](compatibility.md).

## Inspect and install

Inspect a skill before installation:

```bash
hermes skills inspect asimons81/hermes-field-kit/hermes-stack-doctor
```

Install it:

```bash
hermes skills install asimons81/hermes-field-kit/hermes-stack-doctor --yes
```

Replace `hermes-stack-doctor` with any published skill name. In the tested Hermes v0.19.0 environment, this repository-qualified identifier resolved through the skills.sh community registry and Hermes recorded the exact GitHub source revision in hub metadata.

## Custom tap status

Hermes accepts the repository as a custom tap:

```bash
hermes skills tap add asimons81/hermes-field-kit
hermes skills tap list
```

However, in the v1.0.1 validation environment, adding the tap did not make `hermes skills search hermes-stack-doctor` return the skill, including with `--source github`. Because the successful inspect and install operations resolved through skills.sh, this release does not claim working tap-backed search or installation.

Treat custom tap registration as experimental until a future Hermes version exposes that path reliably and the complete lifecycle is retested.

## Verify installation

```bash
hermes skills list
hermes skills audit
```

Start a new Hermes session and use a documented positive trigger from the selected skill's `SKILL.md`. Also verify that a documented counter-trigger does not load it.

## Check and update

```bash
hermes skills check
hermes skills update hermes-stack-doctor
```

A Hermes v0.19.0 quirk was reproduced during the release gate: an unchanged skills.sh-backed installation can report `update_available`, reinstall the same source revision, and continue reporting `update_available` afterward. Confirm the recorded `source_revision` and content hash rather than treating the status label alone as proof that new content exists.

Review upstream changes before updating consequential or write-capable skills.

## Remove an installed skill

Interactive use:

```bash
hermes skills uninstall hermes-stack-doctor
```

Confirm the prompt when asked. For automation, provide confirmation through the shell or use a Hermes version that supports an explicit noninteractive uninstall flag. Start a new Hermes session after removal.

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

- **Registry-installed skill:** use Hermes `skills check`, `skills update`, and `skills uninstall`, while verifying the recorded source revision when status reporting is ambiguous.
- **Manually copied skill:** replace or remove the complete installed skill directory.
- **Pinned raw-URL review install:** treat it as a one-commit verification artifact. Reinstall from the newly selected commit rather than assuming in-place update support.

Do not mix lifecycle methods. A raw URL pinned to one commit is not evidence that registry or future tap update paths are broken.

## Safety

Installation does not grant authorization for consequential actions. Review tool requirements, scripts, approval boundaries, and untrusted-content handling before use.

# Installation

Published skills can be installed through a Hermes tap or copied manually from this repository. Review each skill before installation.

## Install as a Hermes tap

The repository is structured so every published skill is an immediate child of `skills/`:

```text
skills/<skill-name>/SKILL.md
```

Add the repository using the Hermes tap command supported by your installed Hermes version, then install the selected skill through Hermes. Review the repository and each skill before installation.

## Install one skill manually

Hermes discovers user-local skills under:

```text
~/.hermes/skills/<optional-category>/<skill-name>/SKILL.md
```

From a clone, copy a selected tap skill into your local tree.

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

## Activate

Start a new Hermes session after installation. Skill discovery may be cached for the lifetime of an existing session.

## Update and remove

Use the lifecycle that matches the installation method:

- **Tap-installed skill:** use the update or uninstall command supported by the installed Hermes version.
- **Manually copied skill:** review the new version, replace the complete installed skill directory with the reviewed directory from the selected commit, and start a new Hermes session.
- **Pinned raw-URL review install:** treat it as a one-commit verification artifact. Do not assume Hermes can update it in place. Reinstall from the newly selected commit or remove its installed directory.

Do not mix lifecycle methods. In particular, a raw URL pinned to one commit is not evidence that the repository's normal tap-update path is broken.

To remove a manually copied or pinned review skill, delete its complete installed directory and start a new Hermes session.

## Safety

Installation does not grant authorization for consequential actions. Review tool requirements, scripts, and approval boundaries before use.

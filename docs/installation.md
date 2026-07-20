# Installation

There are no published skills yet. This document defines the installation workflow that will apply when the catalog is populated.

## User-local skill location

Hermes Agent discovers user-local skills under:

```text
~/.hermes/skills/<optional-category>/<skill-name>/SKILL.md
```

On Windows, `~` resolves to the current user's home directory.

## Install one skill

From a clone of this repository, copy or link the selected skill directory into the Hermes user-local skills tree.

Example on Linux or macOS:

```bash
mkdir -p ~/.hermes/skills/<category>
cp -R skills/<category>/<skill-name> ~/.hermes/skills/<category>/
```

Example on PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.hermes\skills\<category>" | Out-Null
Copy-Item -Recurse "skills\<category>\<skill-name>" "$HOME\.hermes\skills\<category>\"
```

Review every file before installation, especially scripts, templates, and tool requirements.

## Activate

Start a new Hermes session after installation. Skill discovery may be cached for the lifetime of an existing session.

## Update

Pull the repository, review the skill's version and changes, then replace the installed directory. Do not overwrite private overlays without reviewing the diff.

## Remove

Delete the installed skill directory and start a new Hermes session.

## Safety

Installation does not grant authorization for consequential actions. Review each skill's requirements, tool boundaries, and safety notes before use.

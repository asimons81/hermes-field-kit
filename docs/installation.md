# Installation

There are no published skills yet. This document defines the workflow that applies when the catalog is populated.

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
New-Item -ItemType Directory -Force "$HOME\.hermes\skills" | Out-Null
Copy-Item -Recurse "skills\<skill-name>" "$HOME\.hermes\skills\"
```

## Activate

Start a new Hermes session after installation. Skill discovery may be cached for the lifetime of an existing session.

## Update and remove

Review version changes before replacing an installed directory. To remove a skill, delete its installed directory and start a new Hermes session.

## Safety

Installation does not grant authorization for consequential actions. Review tool requirements, scripts, and approval boundaries before use.

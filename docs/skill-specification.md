# Skill Specification

This document defines the repository contract for published skills. It follows Hermes Agent `SKILL.md` conventions and the immediate-child layout used by Hermes tap discovery.

## Directory layout

```text
skills/<name>/
├── SKILL.md
├── README.md
├── examples/
├── tests/
│   └── cases.json
├── references/      # optional
├── scripts/         # optional
├── templates/       # optional
└── assets/          # optional
```

The skill directory must be an immediate child of `skills/`. Do not insert a category directory between `skills/` and the skill. Category organization belongs in metadata and `catalog.json`.

Skill names use lowercase kebab-case.

## Required `SKILL.md` frontmatter

The file begins with `---` at byte zero and contains a nonempty body.

```yaml
---
name: example-skill
description: Use when a specific trigger applies. Describe the behavior in one focused sentence.
version: 0.1.0
author: Contributor Name
license: Apache-2.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: productivity
    tags: [example, workflow]
    related_skills: []
---
```

Repository requirements:

- `name`: lowercase kebab-case, at most 64 characters, identical to the directory name
- `description`: starts with `Use when `, describes the trigger class, at most 1024 characters
- `version`: valid Semantic Versioning
- `author`: nonempty attribution
- `license`: `Apache-2.0` unless an approved exception is documented
- `platforms`: one or more of `linux`, `macos`, `windows`, or `platform-agnostic`
- `metadata.hermes.category`: lowercase kebab-case category used for catalog organization
- `metadata.hermes.tags`: focused discovery tags
- `metadata.hermes.related_skills`: repository-resolvable names unless explicitly documented

The full `SKILL.md` must not exceed 100,000 characters.

## Required body

At minimum:

```text
# Title
## Overview
## When to Use
## Workflow
## Common Pitfalls
## Verification Checklist
```

`When to Use` includes positive triggers and counter-triggers. Ordered workflow steps end in checkable completion criteria.

## Supporting paths

Only these top-level entries are permitted within a published skill:

- `SKILL.md`
- `README.md`
- `examples/`
- `tests/`
- `references/`
- `scripts/`
- `templates/`
- `assets/`

Symlinks are not allowed. This keeps tap installs self-contained and reviewable.

## Skill README

The skill README documents the problem, real-workflow provenance, inputs, outputs, installation, invocation, requirements, limitations, safety, privacy, and version history.

## Examples

Examples are sanitized but realistic. Include one successful use and one boundary, counter-trigger, or failure-mode example.

## Behavior tests

Each skill requires `tests/cases.json` conforming to `schemas/test-cases.schema.json`, including a positive trigger, negative trigger, workflow behavior, and safety boundary when applicable.

## Catalog entry

Every published skill has exactly one entry in `catalog.json`. The entry path is always `skills/<name>`. Its category agrees with `metadata.hermes.category`; name, version, description, and platforms agree with `SKILL.md`.

## Admission evidence

The pull request states the recurring task, practical use, behavior change, public/private boundary, limitations, and validation performed.

## Versioning

Each skill uses Semantic Versioning independently:

- Patch: correction without intended behavior change
- Minor: backward-compatible workflow expansion
- Major: breaking trigger, input, output, or safety-boundary change

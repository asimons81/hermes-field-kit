# Skill Specification

This document defines the repository contract for published skills. It follows the Hermes Agent `SKILL.md` conventions while adding evidence, testing, and catalog requirements for Hermes Field Kit.

## Directory layout

```text
skills/<category>/<name>/
├── SKILL.md
├── README.md
├── examples/
│   └── ...
├── tests/
│   └── cases.json
├── references/      # optional
├── scripts/         # optional
├── templates/       # optional
└── assets/          # optional
```

Category and skill directory names must use lowercase kebab-case.

## Required `SKILL.md` frontmatter

The file must begin with `---` at byte zero and contain a nonempty body after the closing delimiter.

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
    tags: [example, workflow]
    related_skills: []
---
```

Repository requirements:

- `name`: lowercase kebab-case, at most 64 characters, and identical to the directory name
- `description`: begins with `Use when `, describes the trigger class, and is at most 1024 characters
- `version`: valid Semantic Versioning
- `author`: nonempty attribution
- `license`: `Apache-2.0` unless an approved exception is documented
- `platforms`: one or more of `linux`, `macos`, `windows`, or `platform-agnostic`
- `metadata.hermes.tags`: focused discovery tags
- `metadata.hermes.related_skills`: only repository-resolvable names unless explicitly documented

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

`When to Use` must include both positive triggers and explicit counter-triggers. Ordered workflow steps must end in checkable completion criteria. The verification checklist must test the result, not merely state that work was attempted.

## Skill README

The skill's `README.md` is written for humans and must include:

- Problem solved
- Real-workflow provenance, described without private data
- Inputs and outputs
- Installation
- Example invocation
- Requirements
- Limitations
- Safety and privacy notes
- Version history or changelog link

## Examples

Examples must be sanitized but realistic. They must not contain live credentials, private analytics, unpublished content, customer data, or identifying environment details.

At least one example must show a successful use. At least one must demonstrate a boundary, counter-trigger, or failure mode.

## Behavior tests

Each skill requires `tests/cases.json` conforming to `schemas/test-cases.schema.json`.

The initial test suite must include:

- One positive trigger
- One negative trigger
- One expected workflow behavior
- One safety or privacy boundary when the skill touches tools, files, accounts, publishing, or consequential actions

Tests describe observable agent behavior. They do not need to assert exact prose.

## Catalog entry

Every published skill must have exactly one entry in `catalog.json`. The entry's `name`, `path`, `version`, description, and platforms must agree with the skill source.

A skill directory without a catalog entry, or a catalog entry without a directory, fails validation.

## Admission evidence

The pull request must state:

- The recurring task
- How the skill was used in practice
- What changed compared with default agent behavior
- What was removed or generalized for public release
- Known limitations
- Validation performed

Screenshots, private exports, and confidential logs are not required and should not be included merely to prove use.

## Versioning

Each skill uses Semantic Versioning independently:

- Patch: clarification or correction without intended behavior change
- Minor: backward-compatible behavior or workflow expansion
- Major: changed triggers, required inputs, output contract, or safety boundary that can break existing use

The repository release process may bundle multiple independently versioned skills.

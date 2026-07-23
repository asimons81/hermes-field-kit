# Hermes Field Kit

[![Validate repository](https://github.com/asimons81/hermes-field-kit/actions/workflows/validate.yml/badge.svg)](https://github.com/asimons81/hermes-field-kit/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**Field-tested, open-source skills for Hermes Agent.**

Hermes Field Kit is a curated collection of reusable workflows that have earned their place through real, repeated use. It is intentionally not a bulk skill dump.

## Current status

**Thirteen field-tested skills are now available.**

The catalog includes private-by-default analytics, source-locked writing, and an operational Field Kit organized around:

```text
inspect -> diagnose -> recover -> migrate -> verify
```

The repository applies the same admission rule to every future skill.

## The admission rule

A skill belongs here only when all three statements are true:

1. It solves a real task.
2. It has been used in an actual workflow.
3. Another person can reproduce the intended behavior from the repository.

Generated filler, speculative prompts, thin wrappers, and untested skill bundles do not qualify.

## What every published skill must provide

- A Hermes-compatible `SKILL.md`
- Direct tap discovery under `skills/<skill-name>/`
- Clear triggers and counter-triggers
- Sanitized examples from realistic workflows
- Behavior-oriented test cases
- Known limitations and failure modes
- Platform and tool requirements
- Independent versioning
- No embedded credentials, private data, or personal configuration

See the [skill specification](docs/skill-specification.md) for the complete contract.

## Repository map

```text
skills/<skill-name>/       Published tap-discoverable skills
catalog.json               Machine-readable index and category metadata
templates/skill-template/  Nonfunctional authoring scaffold
schemas/                   Machine-readable catalog and test schemas
scripts/validate.py         Dependency-free repository validator
scripts/validate_release_wave.py  Published-skill and public-tree hardening validator
tests/                     Validator contract tests
docs/                      Installation, design, testing, and release policy
.github/                   Contribution forms, dependency updates, and CI
```

The `skills/` directory contains tap-discoverable published skills and its explanatory README.

## Published skills

- [`hermes-environment-migration`](skills/hermes-environment-migration/README.md): Safely migrate Hermes environments with staged archives, integrity manifests, secret separation, selective imports, verification, and rollback.
- [`hermes-gateway-doctor`](skills/hermes-gateway-doctor/README.md): Diagnose gateway failures from real process, adapter, credential-posture, log, delivery, and persistence evidence without automatic repair.
- [`hermes-profile-audit`](skills/hermes-profile-audit/README.md): Compare a profile’s declared responsibilities with its actual tools, skills, persistence, access, and observed behavior without rewriting it.
- [`hermes-skill-audit`](skills/hermes-skill-audit/README.md): Audit global and profile-local skills for dependencies, frontmatter, usage integrity, cron references, duplicates, and upstream drift.
- [`hermes-stack-doctor`](skills/hermes-stack-doctor/README.md): Discover the installation architecture, delegate to focused evidence contracts, and report a GREEN, YELLOW, or RED stack verdict without repairs.
- [`hermes-token-audit`](skills/hermes-token-audit/README.md): Audit token usage and cost with live schema discovery, aggregate-first privacy, and clear separation between estimates and provider billing.
- [`hermes-update-doctor`](skills/hermes-update-doctor/README.md): Investigate update failures by separating remote drift, repository divergence, process locks, stale caches, partial installs, and runtime mismatches.
- [`interview-me`](skills/interview-me/README.md): Ask one high-value question at a time, inspect available sources before questioning, and stop when more questions would not change the next action.
- [`oss-tool-trust-audit`](skills/oss-tool-trust-audit/README.md): Read source and release machinery, treat popularity as context rather than proof, and separate technical legitimacy from adoption fit.
- [`pre-build-feature-audit`](skills/pre-build-feature-audit/README.md): Run a read-only duplicate check across source, history, branches, issues, pull requests, roadmaps, and contributor guidance.
- [`repo-readiness-audit`](skills/repo-readiness-audit/README.md): Determine whether a Git repository is ready for development, release, handoff, or contribution using independent evidence from repository and collaboration surfaces.
- [`x-analytics-import`](skills/x-analytics-import/README.md): Validate, normalize, import, and compare X Analytics CSV exports through a repeatable private-by-default workflow.
- [`x-post-writer`](skills/x-post-writer/README.md): Draft, rewrite, and repurpose short-form X content with source fidelity, format routing, and claim verification.

## Design principles

- **Field-tested over fashionable.**
- **Trust over volume.**
- **Process predictability over ornamental prose.**
- **Progressive disclosure over giant always-loaded instructions.**
- **Reproducible behavior over promises of guaranteed outcomes.**
- **Safe defaults over environment-specific shortcuts.**
- **Tap compatibility over aesthetically tidy but undiscoverable nesting.**

Read [Design Principles](docs/design-principles.md) for the reasoning behind these rules.

## Installing skills

The repository can be added as a Hermes tap, or any `skills/<skill-name>/` directory can be copied into the user's Hermes skills directory. Review each skill README and scripts before installation.

See [Installation](docs/installation.md) for the installation workflow and platform paths.

## Validation

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/validate_release_wave.py
```

The repository validator checks tap layout, catalog agreement, frontmatter, behavior cases, supporting paths, JSON validity, and common secret patterns. The hardening validator runs contract tests for every published skill, runs bundle validators where supplied, parses every Python file, checks relative Markdown links, rejects generated artifacts, and scans the public tree for private or credential-bearing material.

## Contributing

Start with [CONTRIBUTING.md](CONTRIBUTING.md). New skill proposals use the dedicated GitHub issue form and must include evidence of real use without exposing private information.

## Versioning and releases

The repository and catalog use Semantic Versioning. Individual skills carry their own SemVer version in `SKILL.md`. No release tag will be created solely for the scaffold.

See [Release Process](docs/release-process.md).

## Security

Never submit API keys, session tokens, private analytics exports, customer data, unpublished credentials, or personal configuration. Report suspected exposure privately as described in [SECURITY.md](SECURITY.md).

## Relationship to Hermes Agent

This is an independent community repository for skills compatible with [Hermes Agent](https://github.com/NousResearch/hermes-agent). It is not an official Nous Research repository and does not imply endorsement.

## License

Apache License 2.0. See [LICENSE](LICENSE).

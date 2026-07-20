# Hermes Field Kit

[![Validate repository](https://github.com/asimons81/hermes-field-kit/actions/workflows/validate.yml/badge.svg)](https://github.com/asimons81/hermes-field-kit/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**Field-tested, open-source skills for Hermes Agent.**

Hermes Field Kit is a curated collection of reusable workflows that have earned their place through real, repeated use. It is intentionally not a bulk skill dump.

## Current status

**Foundation phase. There are no published skills yet.**

The repository currently contains the specification, contribution process, validation tooling, governance, and a nonfunctional authoring template. The first skill will be added only after it has been sanitized, documented, tested, and reviewed as a real daily-driver workflow.

## The admission rule

A skill belongs here only when all three statements are true:

1. It solves a real task.
2. It has been used in an actual workflow.
3. Another person can reproduce the intended behavior from the repository.

Generated filler, speculative prompts, thin wrappers, and untested skill bundles do not qualify.

## What every published skill must provide

- A Hermes-compatible `SKILL.md`
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
skills/                    Published skills, grouped by category
templates/skill-template/  Nonfunctional authoring scaffold
schemas/                   Machine-readable catalog and test schemas
scripts/validate.py         Dependency-free repository validator
docs/                      Installation, design, testing, and release policy
.github/                   Contribution forms, pull-request policy, and CI
catalog.json               Machine-readable index of published skills
```

The `skills/` directory is intentionally empty except for its explanatory README.

## Design principles

- **Field-tested over fashionable.**
- **Trust over volume.**
- **Process predictability over ornamental prose.**
- **Progressive disclosure over giant always-loaded instructions.**
- **Reproducible behavior over promises of virality or guaranteed outcomes.**
- **Safe defaults over environment-specific shortcuts.**

Read [Design Principles](docs/design-principles.md) for the reasoning behind these rules.

## Installing skills

There is nothing to install yet. When the first skill ships, each catalog entry will point to a self-contained directory that can be copied or linked into the user's Hermes skills directory.

See [Installation](docs/installation.md) for the planned workflow and platform paths.

## Contributing

Start with [CONTRIBUTING.md](CONTRIBUTING.md). New skill proposals use the dedicated GitHub issue form and must include evidence of real use without exposing private information.

Repository policy and specification changes are welcome before the first skill lands.

## Versioning and releases

The repository and catalog use Semantic Versioning. Individual skills also carry their own SemVer version in `SKILL.md`. No release tag will be created solely for this scaffold.

See [Release Process](docs/release-process.md).

## Security

Never submit API keys, session tokens, private analytics exports, customer data, unpublished credentials, or personal configuration. Report suspected exposure privately as described in [SECURITY.md](SECURITY.md).

## Relationship to Hermes Agent

This is an independent community repository for skills compatible with [Hermes Agent](https://github.com/NousResearch/hermes-agent). It is not an official Nous Research repository and does not imply endorsement.

## License

Apache License 2.0. See [LICENSE](LICENSE).

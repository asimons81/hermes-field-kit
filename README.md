# Hermes Field Kit

[![Validate repository](https://github.com/asimons81/hermes-field-kit/actions/workflows/validate.yml/badge.svg)](https://github.com/asimons81/hermes-field-kit/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**Field-tested, open-source skills for Hermes Agent.**

Hermes Field Kit is a curated collection of reusable workflows that have earned their place through real, repeated use. It is intentionally not a bulk skill dump.

## Current status

**Foundation phase. There are no published skills yet.**

The repository contains the specification, contribution process, validation tooling, validator self-tests, governance, and a nonfunctional authoring template. The first skill will be added only after it has been sanitized, documented, tested, and reviewed as a real daily-driver workflow.

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
tests/                     Validator contract tests
docs/                      Installation, design, testing, and release policy
.github/                   Contribution forms, dependency updates, and CI
```

The `skills/` directory is intentionally empty except for its explanatory README.

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

There is nothing to install yet. When the first skill ships, the repository can be added as a Hermes tap, or an individual `skills/<skill-name>/` directory can be copied into the user's Hermes skills directory.

See [Installation](docs/installation.md) for the planned workflow and platform paths.

## Validation

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
```

The validator checks tap layout, catalog agreement, frontmatter, behavior tests, supporting paths, JSON validity, and common secret patterns. Its own tests prove both acceptance and rejection behavior.

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

# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and the project uses Semantic Versioning.

## [Unreleased]

### Added

- Repository mission and admission rule
- Contribution, governance, conduct, support, and security policies
- Hermes-compatible skill specification
- Installation, testing, design, and release documentation
- Empty machine-readable catalog and JSON schemas
- Nonfunctional skill authoring template
- Dependency-free validation script
- Validator contract tests covering valid and invalid repositories
- GitHub issue forms, pull-request template, CODEOWNERS, Dependabot, and CI
- `x-analytics-import` 1.0.0, the first published field-tested skill
- Deterministic X Analytics importer, synthetic tests, examples, and privacy guidance

### Changed

- Published skills now live directly under `skills/<skill-name>/` for Hermes tap discovery
- Category organization is metadata rather than a physical directory layer
- CI actions are pinned to immutable commit SHAs with read-only permissions and bounded execution

### Skills

- `x-analytics-import` 1.0.0: first baseline, recurring incremental imports, matched snapshot comparison, robust statistics, and privacy-safe reporting.

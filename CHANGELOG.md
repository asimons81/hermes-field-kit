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
- `x-post-writer` 1.0.0, a source-locked short-form X writing workflow
- Generic format routing, claim verification, voice customization, and anti-fabrication tests
- Eleven-skill Hermes Field Kit operational release wave
- Dependency-free hardening validator for all published skill tests, supplied bundle validators, Python syntax, relative links, generated artifacts, and public-tree hygiene

### Changed

- Published skills now live directly under `skills/<skill-name>/` for Hermes tap discovery
- Category organization is metadata rather than a physical directory layer
- CI actions are pinned to immutable commit SHAs with read-only permissions and bounded execution
- Release-wave bundles follow the repository's Apache-2.0 policy and standard behavior-case schema while retaining their richer contract oracles
- Hostile-content boundaries now treat inspected repositories, packages, logs, archives, databases, issues, pull requests, and skills as untrusted evidence

### Skills

- `x-analytics-import` 1.0.0: first baseline, recurring incremental imports, matched snapshot comparison, robust statistics, and privacy-safe reporting.
- `x-post-writer` 1.0.0: single-post default, quote posts, replies, explicit threads, source locking, unsupported-claim blocking, and configurable voice guidance.
- `hermes-environment-migration` 1.0.0: Safely migrate Hermes environments with staged archives, integrity manifests, secret separation, selective imports, verification, and rollback.
- `hermes-gateway-doctor` 1.0.0: Diagnose gateway failures from real process, adapter, credential-posture, log, delivery, and persistence evidence without automatic repair.
- `hermes-profile-audit` 1.0.0: Compare a profile’s declared responsibilities with its actual tools, skills, persistence, access, and observed behavior without rewriting it.
- `hermes-skill-audit` 1.0.0: Audit global and profile-local skills for dependencies, frontmatter, usage integrity, cron references, duplicates, and upstream drift.
- `hermes-stack-doctor` 1.0.0: Discover the installation architecture, delegate to focused evidence contracts, and report a GREEN, YELLOW, or RED stack verdict without repairs.
- `hermes-token-audit` 1.0.0: Audit token usage and cost with live schema discovery, aggregate-first privacy, and clear separation between estimates and provider billing.
- `hermes-update-doctor` 1.0.0: Investigate update failures by separating remote drift, repository divergence, process locks, stale caches, partial installs, and runtime mismatches.
- `interview-me` 0.2.0: Ask one high-value question at a time, inspect available sources before questioning, and stop when more questions would not change the next action.
- `oss-tool-trust-audit` 1.0.0: Read source and release machinery, treat popularity as context rather than proof, and separate technical legitimacy from adoption fit.
- `pre-build-feature-audit` 1.1.0: Run a read-only duplicate check across source, history, branches, issues, pull requests, roadmaps, and contributor guidance.
- `repo-readiness-audit` 0.1.0: Determine whether a Git repository is ready for development, release, handoff, or contribution using independent evidence from repository and collaboration surfaces.

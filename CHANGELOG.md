# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and the project uses Semantic Versioning.

## [Unreleased]

## [1.1.0] - 2026-09-05

### Added

- Experimental `hermes-session-handoff` 0.1.0 for evidence-aware continuation packets across sessions, profiles, machines, and compatible agents, including exact fresh-session prompts and explicit re-verification requirements.
- Experimental `hermes-kanbanize` 0.1.0 for translating settled conversations, plans, and specs into Hermes-native Kanban graphs with vertical work slices, acceptance criteria, blocking edges, verified frontiers, and separate execution authorization.
- Experimental `hermes-change-review` 0.1.0 for separate Intent, Repository, and Verification review axes before implementation work is accepted or merged.
- Experimental `what-have-we-done-today` 0.2.0, a manual on-demand daily recap that scans today's sessions across all profile stores, today's kanban activity across all boards, and today's cron runs (including no_agent jobs with no session trace), then writes an append-friendly daily markdown log.
- Experimental `dont-lie-to-me` 0.1.0 with evidence states and proof obligations for strong factual and completion claims.
- Experimental `hermes-skill-consolidate` 0.1.0, a safety-gated write-side companion to `hermes-skill-audit` for consolidating, restructuring, deprecating, splitting, or extracting shared references from installed skills.
- Relationship classification covering confirmed duplicates, likely redundancy, partial overlap, complementary skills, parent/orchestrator designs, shared-reference candidates, intentionally separate safety domains, and insufficient evidence.
- Standard-library rollback snapshot support for skill consolidation with SHA-256 manifest verification, path containment checks, symlink rejection, and tamper detection.
- Skill authoring guidance for routing-pointer precision, single-source-of-truth discipline, environment-backed facts, progressive disclosure, and checkable completion criteria.

### Changed

- The working catalog now contains thirteen stable skills and six experimental skills.
- Field Kit's operating loop now explicitly covers planning, execution verification, and continuation handoff in addition to inspection, diagnosis, recovery, and migration.
- The authoring template now emphasizes observable completion criteria, executable contract tests, and optional progressive references without turning the template into an always-loaded wall of prose.
- Pull-request CI now runs `git diff --check` as an explicit release-quality gate.

### Fixed

- Hardened release-wave validation so a published skill with zero executable contract tests fails consistently on every supported Python version. Python 3.13 exposed that `unittest` can fail an empty discovery while Python 3.11 had previously allowed the hardening script to count zero tests as a pass.

### Design lineage

- The handoff, spec-to-ticket, and multi-axis review concepts in this wave were inspired in part by Matt Pocock's MIT-licensed `skills` repository. The Field Kit implementations were independently written around Hermes-native capabilities, Field Kit safety boundaries, behavior tests, hostile-content handling, and evidence discipline.

## [1.0.1] - 2026-07-24

### Fixed

- Corrected installation documentation to describe the reproducible skills.sh-backed repository identifier flow.
- Removed the unsupported claim that custom tap registration populates search in Hermes Agent v0.19.0.
- Documented the current update-check quirk where an unchanged skills.sh installation may continue to report `update_available` after update.
- Committed compatibility and release-note documentation that was omitted from v1.0.0.
- Corrected the CI compatibility claim to Python 3.11 and 3.13.

## [1.0.0] - 2026-07-23

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
- `hermes-profile-audit` 1.0.0: Compare a profile's declared responsibilities with its actual tools, skills, persistence, access, and observed behavior without rewriting it.
- `hermes-skill-audit` 1.0.0: Audit global and profile-local skills for dependencies, frontmatter, usage integrity, cron references, duplicates, and upstream drift.
- `hermes-stack-doctor` 1.0.0: Discover the installation architecture, delegate to focused evidence contracts, and report a GREEN, YELLOW, or RED stack verdict without repairs.
- `hermes-token-audit` 1.0.0: Audit token usage and cost with live schema discovery, aggregate-first privacy, and clear separation between estimates and provider billing.
- `hermes-update-doctor` 1.0.0: Investigate update failures by separating remote drift, repository divergence, process locks, stale caches, partial installs, and runtime mismatches.
- `interview-me` 0.2.0: Ask one high-value question at a time, inspect available sources before questioning, and stop when more questions would not change the next action.
- `oss-tool-trust-audit` 1.0.0: Read source and release machinery, treat popularity as context rather than proof, and separate technical legitimacy from adoption fit.
- `pre-build-feature-audit` 1.1.0: Run a read-only duplicate check across source, history, branches, issues, pull requests, roadmaps, and contributor guidance.
- `repo-readiness-audit` 0.1.0: Determine whether a Git repository is ready for development, release, handoff, or contribution using independent evidence from repository and collaboration surfaces.

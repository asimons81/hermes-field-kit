# Hermes Field Kit v1.0.0

Hermes Field Kit is a curated, open-source collection of thirteen field-tested skills for Hermes Agent. Each published bundle includes explicit triggers and counter-triggers, realistic sanitized examples, behavior tests, safety boundaries, platform declarations, and independent versioning.

## Included skills

- Seven Hermes operations and diagnostics skills covering environment migration, gateways, profiles, installed skills, full-stack health, token usage, and updates.
- `interview-me` for adaptive, consent-based discovery before ambiguous work.
- `oss-tool-trust-audit`, `pre-build-feature-audit`, and `repo-readiness-audit` for evidence-first software decisions.
- `x-analytics-import` for private-by-default analytics ingestion and comparison.
- `x-post-writer` for source-locked short-form writing and claim verification.

## Installation

```bash
hermes skills tap add asimons81/hermes-field-kit
hermes skills install asimons81/hermes-field-kit/hermes-stack-doctor --yes
```

Replace `hermes-stack-doctor` with any published skill name.

## Validation

The release gate passed:

- 13 published skills
- 12 supplied bundle validators
- 158 contract tests
- 29 Python files parsed
- 62 relative Markdown links checked
- 11/11 positive routing cases
- 11/11 counter-trigger exclusions
- 11/11 hostile-content boundary exercises
- 11/11 safe-runtime exercises
- Fresh-profile tap registration and repository-qualified installation
- Exact-commit manual install, update, uninstall, and rollback verification
- Public-tree hygiene and common secret-pattern scans

Validated with Hermes Agent v0.19.0 (2026.7.20), Python 3.11.15, on Windows 11. GitHub Actions validates Python 3.11, 3.12, and 3.13.

## Safety

Field Kit skills do not grant authorization for consequential actions. Diagnostic and audit skills default to read-only behavior, inspected content is treated as untrusted evidence, and mutations require separate explicit approval where documented.

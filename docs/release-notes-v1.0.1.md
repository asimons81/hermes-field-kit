# Hermes Field Kit v1.0.1

Hermes Field Kit v1.0.1 is a corrective documentation and release-integrity update. The thirteen published skill bundles are unchanged from v1.0.0.

## What this fixes

- Commits the compatibility and release documentation that was omitted from the v1.0.0 tag.
- Replaces unsupported custom-tap claims with the repository-qualified skills.sh installation path reproduced in a fresh Hermes profile.
- Documents that custom tap registration succeeded in Hermes v0.19.0, but tap-backed search did not return the tested skill.
- Documents the Hermes v0.19.0 update-check quirk where unchanged content can continue to report `update_available` after update.
- Corrects CI compatibility to Python 3.11 and 3.13 on Ubuntu and Windows.
- Aligns the README, roadmap, changelog, installation guide, compatibility policy, and release process with tested behavior.

## Installation

```bash
hermes skills inspect asimons81/hermes-field-kit/hermes-stack-doctor
hermes skills install asimons81/hermes-field-kit/hermes-stack-doctor --yes
```

Replace `hermes-stack-doctor` with any published skill name.

## Validation

The corrective release gate includes:

- 13 published skills
- 12 supplied bundle validators
- 158 skill contract tests
- 11 repository-validator tests
- 29 Python files parsed
- Relative Markdown link validation
- Public-tree hygiene and common secret-pattern scans
- Positive routing, counter-trigger exclusion, hostile-content boundary, and safe-runtime exercises
- Fresh-profile repository-qualified inspect, install, check, update, and uninstall testing
- Fresh-clone validation on the merged release commit

## Compatibility note

Validated with Hermes Agent v0.19.0 (2026.7.20), Python 3.11.15, on Windows 11. GitHub Actions validates Python 3.11 and 3.13 on Ubuntu and Windows.

Custom tap-backed search is not claimed as supported in this release. See [Compatibility](compatibility.md) and [Installation](installation.md) for the exact tested behavior.

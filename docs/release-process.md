# Release Process

## Version model

Hermes Field Kit uses repository release versions and independent skill versions.

## Release status

Version 1.0.0 is the first tagged repository release. It includes thirteen admitted, tested, cataloged, tap-discoverable skills.

## Release checklist

1. Confirm `main` is green and review branch-protection or ruleset status.
2. Run `python scripts/validate.py` from a clean checkout.
3. Run `python -m unittest discover -s tests -v`.
4. Run `python scripts/validate_release_wave.py`.
5. Verify changed skill versions.
6. Verify catalog metadata matches source.
7. Review examples and fixtures for private data and hostile-content regression coverage.
8. Confirm the repository tap indexes the skill from `skills/<name>/SKILL.md`.
9. Install and evaluate the skill in a fresh Hermes environment. Record the exact Hermes Agent version, installation method, discovery result, trigger result, counter-trigger result, and uninstall or rollback result.
10. Update `CHANGELOG.md`.
11. Create and verify an annotated SemVer tag and GitHub release notes.
12. Confirm the release tag resolves to the tested commit and GitHub Actions succeeds on the release-preparation commit.

## Compatibility

Release notes identify the Hermes Agent version used for tap indexing and runtime validation. Compatibility claims must be tested.

## Deprecation

A deprecated skill remains cataloged with `status: deprecated` for at least one repository release when practical.

## Emergency fixes

Credential exposure or unsafe behavior may be fixed outside the normal cadence. Revoke exposed credentials before repository cleanup.

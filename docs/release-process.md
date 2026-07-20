# Release Process

## Version model

Hermes Field Kit uses repository release versions and independent skill versions.

## Before the first release

The foundation is not a tagged release. The first release requires at least one admitted, tested, cataloged, tap-discoverable skill.

## Release checklist

1. Confirm `main` is protected and green.
2. Run `python scripts/validate.py` from a clean checkout.
3. Run `python -m unittest discover -s tests -v`.
4. Verify changed skill versions.
5. Verify catalog metadata matches source.
6. Review examples and fixtures for private data.
7. Confirm the repository tap indexes the skill from `skills/<name>/SKILL.md`.
8. Install and evaluate the skill in a fresh Hermes environment.
9. Update `CHANGELOG.md`.
10. Create and verify an annotated SemVer tag and release notes.

## Compatibility

Release notes identify the Hermes Agent version used for tap indexing and runtime validation. Compatibility claims must be tested.

## Deprecation

A deprecated skill remains cataloged with `status: deprecated` for at least one repository release when practical.

## Emergency fixes

Credential exposure or unsafe behavior may be fixed outside the normal cadence. Revoke exposed credentials before repository cleanup.

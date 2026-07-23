# Release Process

## Version model

Hermes Field Kit uses repository release versions and independent skill versions.

## Release checklist

1. Confirm `main` is protected and green.
2. Create a release branch from the current remote `main`.
3. Run `python -B -m unittest discover -s tests -v` from a clean checkout.
4. Run `python -B scripts/validate.py`.
5. Run `python -B scripts/validate_release_wave.py`.
6. Run `git diff --check`.
7. Verify changed skill versions and catalog metadata.
8. Review examples and fixtures for private data and hostile-content regression coverage.
9. Validate the documented installation path in a fresh disposable Hermes profile. Record the exact Hermes version, identifier, resolved source, source revision, security verdict, update behavior, and uninstall result.
10. Do not describe a registry-resolved installation as a custom-tap installation unless Hermes metadata proves the tap was the source.
11. Update `CHANGELOG.md`, compatibility documentation, and release notes.
12. Open a pull request and wait for every required status check.
13. Merge normally without bypassing branch protection.
14. Repeat static and fresh-profile validation against the actual merged commit.
15. Create and verify an annotated SemVer tag on the merged commit.
16. Publish a non-draft GitHub release from the committed release-note file.
17. Confirm the tag target, release target, latest `main` CI, and cleanup of temporary profiles and worktrees.

## Compatibility

Release notes identify the Hermes Agent version and environment used for runtime validation. Compatibility claims must be tested and must distinguish repository behavior from Hermes CLI or registry behavior.

## Corrections

Do not move or replace a published tag. Correct release metadata or documentation through a new patch release, preserving the historical tag and explaining the correction.

## Deprecation

A deprecated skill remains cataloged with `status: deprecated` for at least one repository release when practical.

## Emergency fixes

Credential exposure or unsafe behavior may be fixed outside the normal cadence. Revoke exposed credentials before repository cleanup.

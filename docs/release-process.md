# Release Process

## Version model

Hermes Field Kit uses two version layers:

- **Repository release version:** the catalog, schemas, documentation, and bundled set of skills
- **Skill version:** the independent SemVer value in each skill's `SKILL.md`

A repository release may contain unchanged skills, and a skill version may advance as part of a repository release.

## Before the first release

The foundation scaffold is not itself a tagged release. The first release requires at least one admitted, tested, cataloged skill.

## Release checklist

1. Confirm `main` is green and releasable.
2. Run `python scripts/validate.py` from a clean checkout.
3. Verify every changed skill's frontmatter version increased correctly.
4. Verify catalog metadata matches source.
5. Review examples and fixtures for private data.
6. Update `CHANGELOG.md`.
7. Confirm installation in a fresh Hermes environment.
8. Create an annotated SemVer tag.
9. Publish release notes describing repository and per-skill changes.
10. Verify the tag and release point to the intended commit.

## Compatibility

Release notes must identify the Hermes Agent version used for validation. Compatibility claims must be based on testing, not assumption.

## Deprecation

A deprecated skill remains cataloged with `status: deprecated` for at least one repository release when practical. Its README must identify the replacement or explain why no replacement exists.

## Emergency fixes

Credential exposure or unsafe behavior may be fixed outside the normal cadence. Revoke exposed credentials before repository cleanup and describe security-sensitive details privately.

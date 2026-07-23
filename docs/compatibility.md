# Compatibility

## v1.0.0 validation environment

Hermes Field Kit v1.0.0 was validated on July 23, 2026 with:

- Hermes Agent v0.19.0 (2026.7.20)
- Hermes upstream revision `91546b83`
- Python 3.11.15
- Windows 11
- Repository commit `ca8d4812c2e46648744252c8ee463f0aaea1d92a` before release-preparation documentation

The release gate verified:

- Tap registration for `asimons81/hermes-field-kit`
- Repository-qualified installation using `asimons81/hermes-field-kit/<skill-name>`
- Exact source commit recording and community-source security scanning
- Positive routing, counter-trigger exclusion, hostile-content boundaries, and safe-runtime behavior
- Manual exact-commit installation, complete-directory update, removal, and rollback
- Static validation on Python 3.11, 3.12, and 3.13 through GitHub Actions

## Supported platforms

Every published skill declares its own platform list in `SKILL.md` and `catalog.json`. Repository validation ensures those declarations match. A platform declaration means the workflow and paths are documented for that platform; it does not guarantee every optional external tool is installed.

## Compatibility policy

- Compatibility claims are evidence-based and tied to a tested Hermes Agent version.
- Newer Hermes versions are expected to work when the tap and skill-management interfaces remain compatible, but untested versions are not guaranteed.
- Report regressions with the Hermes version, operating system, skill version, installation method, and exact failing command.
- Skills are independently versioned. A repository release can include skills at different semantic versions.

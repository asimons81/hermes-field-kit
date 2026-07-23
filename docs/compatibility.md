# Compatibility

## v1.0.1 validation environment

Hermes Field Kit v1.0.1 was validated on July 23, 2026 with:

- Hermes Agent v0.19.0 (2026.7.20)
- Python 3.11.15
- Windows 11
- Repository base commit `ca8d4812c2e46648744252c8ee463f0aaea1d92a`

The corrective release gate verified:

- Repository-qualified inspection and installation through Hermes' skills.sh community-registry resolution
- Exact GitHub source revision recording in Hermes hub metadata
- Positive routing, counter-trigger exclusion, hostile-content boundaries, and safe-runtime behavior
- Manual exact-commit installation, complete-directory replacement, removal, and rollback
- Static validation on Python 3.11 and 3.13 through GitHub Actions on Ubuntu and Windows

## Known Hermes v0.19.0 behaviors

- Custom tap registration for `asimons81/hermes-field-kit` succeeds and appears in `skills tap list`, but tap-backed search did not return `hermes-stack-doctor` in the tested environment.
- The successful repository-qualified inspect and install path resolved through skills.sh rather than the newly registered tap.
- `skills check` can report `update_available` immediately after installation and continue reporting it after reinstalling the identical source revision.
- `skills uninstall` prompts for confirmation; noninteractive callers must provide confirmation explicitly.

These behaviors are documented rather than treated as Field Kit guarantees.

## Supported platforms

Every published skill declares its own platform list in `SKILL.md` and `catalog.json`. Repository validation ensures those declarations match. A platform declaration means the workflow and paths are documented for that platform; it does not guarantee every optional external tool is installed.

## Compatibility policy

- Compatibility claims are evidence-based and tied to a tested Hermes Agent version.
- Newer Hermes versions are expected to work when the relevant skill-management interfaces remain compatible, but untested versions are not guaranteed.
- Report regressions with the Hermes version, operating system, skill version, installation method, exact identifier, and failing command.
- Skills are independently versioned. A repository release can include skills at different semantic versions.

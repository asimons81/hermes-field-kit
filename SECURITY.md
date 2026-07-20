# Security Policy

## Supported versions

Before the first tagged release, only the default branch is supported. After releases begin, supported versions will be listed here.

## Reporting a vulnerability or exposure

Do not open a public issue for:

- Committed credentials or tokens
- Private data included in examples or fixtures
- Instructions that enable unsafe credential handling
- Supply-chain compromise
- A validation bypass that could expose users
- A skill that performs consequential actions without adequate boundaries

Use GitHub's private vulnerability reporting feature when available. If it is not available, contact the maintainer privately through the contact method on the maintainer's GitHub profile.

Include:

- Affected file, skill, or version
- Reproduction steps
- Expected and actual behavior
- Potential impact
- Suggested mitigation, when known

## Response

The maintainer will acknowledge a credible report, investigate it, and coordinate a fix and disclosure appropriate to the risk. Exact timing depends on severity and reproducibility.

## Secret handling

This repository must never contain live secrets. Examples and templates must use unmistakably fake placeholders. If a secret is committed:

1. Revoke or rotate it immediately.
2. Treat deletion from Git history as cleanup, not revocation.
3. Open a private report describing the exposure.
4. Add a regression check when practical.

## Scope boundary

Security reports should concern this repository and its distributed contents. Vulnerabilities in Hermes Agent itself should be reported to the Hermes Agent project.

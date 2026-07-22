# Safety and Authority

- Open databases read-only and run integrity checks before analysis.
- Discover tables and columns instead of assuming a fixed schema.
- Default to aggregate metadata and do not inspect message bodies without explicit authorization.
- Never print prompts, private messages, credentials, account identifiers, or raw personal data.
- Label local cost fields as estimates unless reconciled with provider billing.
- Do not pause jobs or change models during the audit.

## Approval boundary

The skill may recommend a mutation, but it must not perform one until the user separately and explicitly approves the exact action after reviewing the report.

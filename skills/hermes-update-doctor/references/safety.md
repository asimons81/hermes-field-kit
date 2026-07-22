# Safety and Authority

- Diagnosis is read-only by default.
- Do not kill processes, change remotes, reset branches, delete caches, reinstall packages, or force updates without explicit approval.
- Preserve dirty worktrees and record them as blockers.
- Verify the actual running code path, not only the checkout path.
- Distinguish local update success from personal-fork synchronization.
- Never use a force flag as a substitute for identifying the lock or divergence.

## Approval boundary

The skill may recommend a mutation, but it must not perform one until the user separately and explicitly approves the exact action after reviewing the report.

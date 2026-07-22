# Safety and Authority

- Never print, echo, log, or paste tokens.
- Prefer credential checks that expose set or not set only.
- Treat webhook changes, polling calls, restarts, state deletion, process termination, and service changes as mutations requiring approval.
- Do not run a competing long-poll request while the gateway may be active.
- Verify process liveness independently from state and PID files.
- Do not infer delivery success from process state alone.

## Approval boundary

The skill may recommend a mutation, but it must not perform one until the user separately and explicitly approves the exact action after reviewing the report.

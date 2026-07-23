# Evidence and Access

## Access Matrix

Record each surface as one of:

- `verified`
- `partially verified`
- `not verified`
- `not applicable`

For `not verified`, include the exact reason:

- tool unavailable
- authentication failed
- permission denied
- network unavailable
- repository lacks the surface
- command safety uncertain
- dependencies absent and installation prohibited
- command exceeded the permitted runtime
- platform unsupported
- data returned was incomplete

## Confidence Calibration

Do not use a single confidence percentage. The verdict is determined by
evidence and blockers. Use **Not Verified** to preserve uncertainty precisely.

Examples:

- "Unresolved GitHub review threads were not verified because the available PR
  summary did not expose thread resolution state."
- "Branch protection rules were not verified because the token lacks
  administration read permission."
- "The full test suite was not run because required dependencies are absent and
  installation is prohibited during the audit."
- "Ignored build output was not inspected because it may contain secrets; only
  filenames were checked."

## Direct Evidence

Good evidence contains:

- command or tool name
- relevant path, branch, PR, issue, workflow, or commit
- observed status
- timestamp when volatile
- exact failure or limitation

Weak evidence to avoid:

- "looks clean"
- "seems merged"
- "probably passing"
- "should be current"
- "the previous session said"
- "no obvious issues"

## Remote Freshness

A local remote-tracking ref may be stale. State whether remote references were
refreshed during the audit. When fetch is not permitted or not performed,
report synchronization findings as local-ref observations, not current remote
truth.

## Missing GitHub or CI Access

Do not silently omit collaboration surfaces. Record:

- which repository and branch were queried
- which tool or command failed
- whether local workflow definitions were still inspected
- whether the missing surface is critical to the user's stated goal
- how the missing access affected the verdict

## Repository Mutation Detection

The audit itself must not modify the repository. Pre/post Git state is evidence.
If a command produces files or changes tracked content:

- identify the command and paths
- stop
- do not remove the changes
- classify the repository as `NOT READY`
- recommend a separately authorized cleanup and safer validation path

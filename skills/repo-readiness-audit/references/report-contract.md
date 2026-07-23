# Report Contract

Use the headings exactly once and in this exact order.

```markdown
# Repository Readiness Audit

## Verdict

READY | READY WITH WARNINGS | NOT READY

Goal: <further development | new feature | handoff | new contributor | release work>
Audited repository: <name and exact path>
Audited commit: <branch and SHA>
Audit timestamp: <timestamp and timezone>

## Repository State

Confirmed facts about identity, remotes, branches, worktree, synchronization,
unfinished Git operations, ignored/untracked state, and submodules.

## Recent Work

Evidence-backed summary of the latest completed work and current branch
relationship.

## Pull Requests and Reviews

Open/draft/recently merged PRs, review decisions, unresolved threads, requested
changes, conflicts, and stale branches. State access gaps here and again under
Not Verified when material.

## Issues and Blockers

Confirmed open issues, milestones, unfinished markers, and blockers. Explicitly
write "No blockers confirmed" only when that statement was actually verified.

## CI and Tests

Workflow definitions, latest relevant runs, required checks, exact commands
executed, exit results, failures, skips, and pre/post mutation checks.

## Documentation and Plan Alignment

README, changelog, release notes, ADRs, roadmap, implementation plans, and
environment/setup alignment with current code.

## Risks and Warnings

Only non-blocking concerns. Do not bury blockers here.

## Not Verified

Every unavailable or incomplete surface and the exact reason.

## Recommended Next Actions

Ordered actions. Recommendations do not authorize modifications.

## Evidence Summary

Compact mapping of each material conclusion to its command, file, commit, PR,
issue, workflow, or tool result.
```

The verdict line must be exactly one allowed verdict. Do not write `GO`,
`NO-GO`, `Mostly Ready`, a percentage, or a custom label.

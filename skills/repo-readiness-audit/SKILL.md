---
name: repo-readiness-audit
description: Use when a user asks whether an identified repository is ready for further development, release work, a new feature, handoff, or a new contributor, requiring a disciplined read-only audit before an evidence-backed verdict.
version: 0.1.0
author: Tony Simons
license: Apache-2.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: software-development
    tags: [repository, readiness, audit, git, github, ci, tests, handoff]
    related_skills: []
---
# Repository Readiness Audit

## Overview

Use this skill to answer a broad repository-state question before new work
begins. It determines whether the repository is ready for further
development, release work, a new feature, a handoff, or a new contributor.

This is a **read-only evidence audit**. It does not repair findings. It does not
equate a clean working tree, passing tests, or a green local build with overall
repository readiness. It verifies each relevant surface independently and
records any surface that could not be checked.

This skill covers repository-level readiness. Packaging integrity, upgrade
rehearsal, registry publication, signed artifacts, deployment verification, and
post-release checks require additional release-specific evidence. When those
surfaces matter but cannot be inspected, record them under **Not Verified** and
reduce the verdict accordingly.

## When to Use

Load this skill for requests such as:

- "Is this repo ready for further development?"
- "Where did we leave off?"
- "Can I start the next feature?"
- "Audit this repository before we continue."
- "Is everything merged, tested, and documented?"
- "Give me a release-readiness check."
- "What is blocking this project?"
- "Is this ready to hand to another developer?"
- "Can a new contributor safely start here?"

A repository must be identified by an exact local path, a repository URL, or a
current working directory that can be verified as a Git repository.

## Counter-Triggers

Do not load this skill for:

- A simple code review of one file or one diff.
- Implementing a feature, bug fix, migration, or refactor.
- Automatically fixing every issue found.
- Generic Git or GitHub explanations.
- A feature-duplication investigation focused only on whether one proposed feature already exists.
- An incoming prototype assessment focused only on real versus simulated code.
- A packaging-only, artifact-signing, publication, or post-release verification audit.
- Any request where no repository has been identified.

If the repository is not identified, ask for or resolve the exact repository
before auditing. Do not guess from stale conversation context.

## Non-Negotiable Safety Contract

The audit is read-only.

Never, during the audit:

- modify, create, move, rename, or delete repository files
- stage or unstage files
- commit, amend, rebase, merge, cherry-pick, revert, tag, or reset
- push, force-push, fetch with side effects beyond remote-reference refresh,
  publish, or create releases
- open, edit, merge, close, approve, or comment on pull requests
- open, edit, close, label, assign, or comment on issues
- create, switch, rename, or delete branches
- install, update, or remove dependencies
- run formatters, auto-fixers, generators, migrations, or commands documented as
  mutating
- change configuration, environment files, hooks, permissions, or secrets
- clean ignored or untracked files
- write audit artifacts inside the repository

A command is not safe merely because it is familiar. Prefer commands known to
be read-only. Before running an unfamiliar validation command, inspect its
definition and scripts for mutation behavior. If safety cannot be established,
record it under **Not Verified**.

A separate, explicit instruction after the audit is required before any repair.

## Evidence Priority

Prefer evidence in this order:

1. Direct repository state and command output from the identified working copy.
2. Current remote and GitHub/CI state retrieved during this audit.
3. Repository-owned configuration, tests, docs, ADRs, plans, and lockfiles.
4. Current issue, pull-request, milestone, and review records.
5. Conversation context, memory, or prior reports only as leads to verify.

Never use prior conversation state as proof that the repository is clean,
tested, synchronized, merged, documented, or ready.

## Workflow

Follow the required audit sequence below.

## Required Audit Sequence

Follow all steps in order. A step may be marked unavailable, but it may not be
silently skipped. Use `references/audit-protocol.md` for command guidance and
completion criteria.

### 1. Confirm Repository Identity

Verify:

- exact local path
- Git worktree root
- repository name
- remote names and URLs
- default branch, from local config or remote metadata
- current branch
- current HEAD commit
- upstream tracking branch, when configured

Stop and return `NOT READY` if repository identity is contradictory or the
target is not a Git repository. Record inaccessible remote metadata under
**Not Verified**.

Completion criterion: every reported identity field is backed by current
command output or explicitly marked not verified.

### 2. Inspect Working-Tree and Synchronization State

Inspect:

- modified tracked files
- staged changes
- untracked files
- ignored files when build output, secrets, generated files, or environment
  state could affect readiness
- ahead/behind counts against the tracked branch
- local commits not pushed
- detached HEAD, unfinished merge/rebase/cherry-pick/revert, or bisect state
- submodule state when present
- worktrees when relevant

Do not clean, stash, reset, stage, or switch branches.

A clean worktree proves only that the current checkout has no visible local
changes. It does not prove tests, CI, documentation, synchronization, reviews,
or release readiness.

Completion criterion: every category is either checked or listed under
**Not Verified**.

### 3. Determine Recent Work

Inspect recent commits, merge commits, branch history, changed-file summaries,
and relevant changelog or plan updates. Determine:

- what work was completed most recently
- what commit or merge established the current state
- whether the current branch contains work absent from the default branch
- whether recent commits suggest incomplete follow-up work

Do not summarize commit subjects alone when changed files or commit bodies are
needed to understand the work.

Completion criterion: recent-work claims cite commits, dates, branches, or
changed paths.

### 4. Inspect Pull Requests and Reviews

When GitHub or equivalent access permits, inspect:

- open and draft pull requests
- source and target branches
- mergeability and merge conflicts
- review decisions
- unresolved review threads
- requested changes
- required reviewers or approvals
- check status attached to each relevant pull request
- stale branches and abandoned pull requests
- recently merged pull requests that explain current state

Do not infer "all merged" from an empty local branch list. Do not infer review
completion from a mergeable state.

Completion criterion: relevant pull requests are enumerated or access is
explicitly recorded as unavailable.

### 5. Inspect Issues, Blockers, and Unfinished Markers

Inspect:

- open issues and project blockers
- milestones and due dates
- issue links from recent commits or pull requests
- TODO, FIXME, XXX, HACK, NOT IMPLEMENTED, placeholder, stub, mock, temporary,
  follow-up, and deferred-work markers
- roadmap notes, implementation plans, checklists, and open loops
- known bugs or security advisories when accessible

Search results are leads, not automatic blockers. Read context and distinguish
intentional test fixtures, historical notes, and genuine unfinished work.

Completion criterion: material blockers and unfinished areas are separated
from harmless markers.

### 6. Inspect CI and Branch Expectations

Inspect:

- workflow definitions
- latest workflow runs for the current/default branch and relevant pull requests
- failing, cancelled, timed-out, skipped, and neutral jobs
- required checks and branch-protection or ruleset expectations
- platform matrix coverage
- release or deployment workflows when relevant
- discrepancies between local validation and CI

A skipped job is not a passing job. A green unrelated workflow is not proof
that required checks passed.

Completion criterion: each required or expected check is passed, failed,
skipped, not applicable, or not verified.

### 7. Inspect Test Configuration and Run Safe Validation

Discover validation commands from repository-owned evidence:

- contributor docs
- package scripts
- task runners
- CI workflow definitions
- test configuration
- Makefiles or equivalent

Run the safest relevant commands available without installing dependencies or
changing files. Prefer:

1. collection, syntax, or dry-run checks
2. targeted tests for recent work
3. primary documented test suite
4. lint/type/build checks only when confirmed read-only

Before and after each command, compare repository state. If a supposedly
read-only command changes files, stop, report the mutation as a blocker, and do
not clean it up without authorization.

Do not claim "tested" unless the exact command, exit status, and relevant
results were observed in this audit.

Completion criterion: commands, results, duration if available, failures,
skips, and file-state comparison are recorded.

### 8. Check Documentation and Plan Alignment

Inspect:

- README and contributor instructions
- changelog and release notes
- ADRs and architecture docs
- roadmap and implementation plans
- environment/setup documentation
- generated API or schema docs when relevant
- version references and feature-status claims

Compare documentation claims against code, configuration, tests, and recent
commits. Classify drift as a warning or blocker using
`references/verdict-rules.md`.

Completion criterion: material claims are either aligned, contradicted, stale,
or not verified.

### 9. Inspect Dependencies and Operational State

When relevant, inspect:

- manifest and lockfile agreement
- multiple or missing lockfiles
- dependency update bots and open dependency pull requests
- security warnings and advisories
- generated files and whether their sources are newer
- migrations and schema state
- environment-variable examples and runtime requirements
- supported language/runtime versions
- submodules, vendored code, package metadata, and build artifacts

Do not install dependencies, regenerate lockfiles, run migrations, or update
advisories during the audit.

Completion criterion: dependency and environment state is verified from
available evidence or recorded as not verified.

### 10. Reconcile Findings

Identify incomplete, contradictory, stale, risky, or unverifiable areas.
Deduplicate related findings and separate:

- confirmed facts
- warnings
- blockers
- recommended next actions
- items not verified

A warning is a real concern that does not currently prevent the stated next
step. A blocker prevents the stated next step or makes a confident ready
verdict unsafe.

### 11. Apply the Verdict Rules

Use exactly one verdict:

- `READY`
- `READY WITH WARNINGS`
- `NOT READY`

Apply `references/verdict-rules.md` mechanically.

Never return `READY` when:

- any blocker exists
- a required check failed
- requested changes or merge conflicts remain
- required CI is failing or absent without an accepted exception
- the audit caused or detected unexplained repository mutation
- a material readiness surface required by the user's goal was not verified
- evidence is contradictory on a material point

`READY WITH WARNINGS` requires zero blockers. It is appropriate when the stated
next step can proceed but non-blocking risks or unverifiable secondary areas
remain.

`NOT READY` is required when one or more blockers exist, or when missing
critical access prevents establishing readiness for the stated goal.

### 12. Produce the Required Report

Use every heading below, in this exact order:

```text
Repository Readiness Audit

Verdict

Repository State

Recent Work

Pull Requests and Reviews

Issues and Blockers

CI and Tests

Documentation and Plan Alignment

Risks and Warnings

Not Verified

Recommended Next Actions

Evidence Summary
```

Under **Verdict**, print exactly one of the three allowed verdicts as the first
line.

The report must explain the verdict with direct evidence. Do not use vague
confidence language as a substitute for proof.

## Finding Classification

### Confirmed Facts

Current observations backed by command output, repository files, or current
remote records. Facts are not automatically good or bad.

### Warnings

Non-blocking risks, drift, cleanup debt, stale secondary documentation,
optional checks not run, or uncertainties that do not prevent the stated next
step.

### Blockers

Conditions that prevent the stated next step, invalidate readiness, or make a
ready verdict unsafe. Examples include:

- unresolved merge conflict or requested changes
- failing required test or CI check
- unfinished merge/rebase/cherry-pick
- critical documentation contradicting implementation for a handoff
- missing migration or generated artifact required by the code
- unreviewed or unmerged required work
- unexplained dirty state for release, handoff, or contributor onboarding
- material security warning
- inability to verify a critical surface required by the user's request

### Not Verified

Any surface not checked because of missing access, unavailable tools,
authentication failure, command safety uncertainty, excessive runtime, absent
dependencies, unsupported platform, or ambiguous repository evidence.

State exactly what was not checked and why. Never hide unavailable access in a
generic caveat.

## Goal-Sensitive Readiness

Evaluate readiness against the requested next step:

- **Further development:** local identity, branch state, unfinished work,
  test baseline, and known blockers matter most.
- **New feature:** also verify branch freshness, open competing work, plans, and
  unresolved foundational issues.
- **Handoff or new contributor:** setup docs, environment requirements,
  reproducibility, current plans, and clean explainable state become critical.
- **Release work:** extend the audit to packaging, version, artifact, security,
  upgrade, deployment, and publication gates. Any unavailable release surface
  is material and must be listed under **Not Verified**.

The same repository state can therefore receive different verdicts for
different goals. State the goal near the top of the report.

## Tool and Command Discipline

Use direct repository tools when available. For terminal commands:

- prefer `git status --short --branch`, `git diff --check`, `git diff --stat`,
  `git log`, `git show`, `git branch`, `git remote -v`, `git rev-list`, and
  read-only `gh ... --json` queries
- avoid `git fetch` unless remote freshness is important and the tool policy
  treats remote-reference updates as permitted; disclose when not fetched
- never use commands with `--fix`, `--write`, `--update`, `--upgrade`,
  `--install`, `--force`, `--delete`, `--prune` with destructive scope,
  `reset`, `clean`, `checkout`, `switch`, `stash`, `commit`, `push`, or `merge`
- inspect package scripts before running them
- capture pre-command and post-command Git state around validation commands

See `references/audit-protocol.md` and
`references/evidence-and-access.md`.

## Common Pitfalls

The following failure modes are the primary pitfalls for this audit.

## Common Failure Modes

1. **Clean-tree tunnel vision.** A clean tree is one fact, not a verdict.
2. **Passing-test tunnel vision.** Tests can pass while CI, reviews, docs,
   migrations, packaging, or branch state remain unready.
3. **Green-workflow substitution.** One green workflow does not prove all
   required checks passed.
4. **Silent access gaps.** Unavailable GitHub or CI access must appear under
   **Not Verified** and affect the verdict.
5. **Mutating validation.** Some test, lint, build, and docs commands rewrite
   files. Inspect first and compare Git state afterward.
6. **Commit-message storytelling.** Read changed paths and relevant diffs before
   describing recent work.
7. **Marker overcounting.** TODO text in fixtures or historical docs may not
   represent unfinished implementation.
8. **Stale-context confidence.** Previous sessions are clues, never proof.
9. **Release-scope creep.** Do not let repository-level evidence masquerade as
   full packaging, artifact, deployment, or publication verification.
10. **Repair during diagnosis.** Stop after the report. Ask for separate
    authorization before changing anything.

## Verification Checklist

Before delivering the report, confirm:

- [ ] Repository identity, path, remotes, default branch, current branch, and
      HEAD were checked or explicitly marked not verified.
- [ ] Working tree, staged, untracked, relevant ignored files, synchronization,
      and unfinished Git operations were checked.
- [ ] Recent completed work is supported by commit and changed-path evidence.
- [ ] Pull requests, reviews, conflicts, issues, blockers, and stale branches
      were checked when access permitted.
- [ ] CI definitions, latest runs, required checks, failures, and skips were
      distinguished.
- [ ] Safe relevant tests or validations were run, or exact reasons for not
      running them were recorded.
- [ ] Documentation, plans, dependencies, lockfiles, generated files,
      migrations, and environment requirements were considered when relevant.
- [ ] Confirmed facts, warnings, blockers, next actions, and not-verified items
      are separated.
- [ ] No repository mutation was authorized or performed.
- [ ] A clean worktree was not treated as overall readiness.
- [ ] Passing tests were not treated as release readiness.
- [ ] The verdict is exactly READY, READY WITH WARNINGS, or NOT READY.
- [ ] Every required report heading appears once and in order.

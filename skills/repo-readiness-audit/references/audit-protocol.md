# Audit Protocol

## Read-Only Baseline

Capture repository state before any validation command:

```bash
git rev-parse --show-toplevel
git remote -v
git branch --show-current
git status --short --branch
git rev-parse HEAD
git rev-parse --abbrev-ref --symbolic-full-name @{upstream}
git rev-list --left-right --count HEAD...@{upstream}
git log --date=iso-strict --decorate --oneline -10
```

Commands may vary by shell and repository. Failure to resolve an upstream branch
is evidence to record, not permission to invent synchronization state.

Inspect unfinished operations without changing them:

```bash
git rev-parse -q --verify MERGE_HEAD
git rev-parse -q --verify REBASE_HEAD
git rev-parse -q --verify CHERRY_PICK_HEAD
git rev-parse -q --verify REVERT_HEAD
git bisect log
```

Use file existence checks for `.git/rebase-merge`, `.git/rebase-apply`, and
other state only after resolving the actual Git directory with
`git rev-parse --git-dir`.

## Working Tree

Use separate evidence for each category:

```bash
git diff --name-status
git diff --cached --name-status
git ls-files --others --exclude-standard
git status --ignored --short
git diff --check
```

Do not call the tree clean unless modified, staged, and untracked state were
checked. Ignored files are relevant when they may contain generated output,
local databases, environment state, or secrets that affect reproducibility.

## Recent Work

Use:

```bash
git log --date=iso-strict --format=fuller -10
git show --stat --summary <commit>
git diff --stat <base>...HEAD
git log --merges --oneline -10
```

Read commit bodies and changed paths when subjects are insufficient.

## GitHub Collaboration State

Prefer structured output:

```bash
gh repo view --json nameWithOwner,defaultBranchRef,url
gh pr list --state open --json number,title,isDraft,headRefName,baseRefName,reviewDecision,mergeStateStatus,statusCheckRollup,updatedAt,url
gh issue list --state open --json number,title,labels,milestone,updatedAt,url
gh run list --branch <branch> --limit 20 --json databaseId,workflowName,status,conclusion,headSha,createdAt,updatedAt,url
```

For relevant pull requests, inspect reviews, comments, files, and checks. A PR
summary may not expose unresolved threads; record that limitation when the
available tool cannot retrieve them.

## Unfinished Markers

Search tracked source and planning surfaces with context. Exclude generated
files, vendor directories, lockfiles, and fixtures when appropriate.

Suggested terms:

```text
TODO
FIXME
XXX
HACK
NOT IMPLEMENTED
NotImplemented
placeholder
stub
temporary
follow-up
deferred
blocked
```

Each hit must be read in context before classification.

## CI

Read workflow definitions before interpreting run results. Identify:

- trigger branches and paths
- required matrices
- allowed failures
- conditional and skipped jobs
- release-only workflows
- generated-file or formatting checks
- branch-protection expectations

A skipped required job is not passing. A green run for a different commit is
not evidence for current HEAD.

## Safe Validation Discovery

Determine commands from, in order:

1. CI workflow commands
2. CONTRIBUTING or AGENTS instructions
3. package/task scripts
4. test configuration
5. README instructions

Inspect scripts before execution. Reject commands that install, update,
generate, format, migrate, clean, publish, or write state unless a documented
dry-run or check-only mode exists.

Examples that are often read-only but still require inspection:

```text
pytest
python -m unittest
npm test
npm run lint
npm run typecheck
cargo test
go test ./...
dotnet test
ruff check .
mypy .
```

Build commands may write output. Do not run them unless output is outside the
repository, already ignored and harmless, or the command's behavior is verified
and pre/post state will be compared.

## Pre/Post Mutation Guard

Before each validation command:

```bash
git status --porcelain=v1 -uall
```

After it:

```bash
git status --porcelain=v1 -uall
```

If state differs:

1. stop further validation
2. record the command and changed paths
3. classify unexpected mutation as a blocker
4. do not revert or clean the changes without authorization

## Documentation and Plan Alignment

Compare current code and tests against:

- README and setup steps
- CONTRIBUTING and AGENTS guidance
- CHANGELOG and release notes
- ADRs and architecture docs
- roadmap and implementation plans
- environment examples
- migration documentation

A historical note is not stale merely because it describes old behavior.
Current-state claims must match current code.

## Dependencies and Environment

Inspect manifests and lockfiles without updating them. Check:

- lockfile corresponding to each manifest
- multiple competing lockfiles
- runtime version constraints
- environment examples
- generated files and source timestamps or checksums
- migration files and ordering
- open dependency/security pull requests
- current advisories when access permits

Do not install packages or run package-manager audit commands that mutate
lockfiles, caches inside the repository, or dependency state.

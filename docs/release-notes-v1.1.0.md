# Hermes Field Kit v1.1.0

Release date target: September 5, 2026

## Status

Release candidate. Static repository validation and fresh-profile Hermes runtime validation must complete before publication.

## Headline

Field Kit 1.1.0 expands the kit from operational diagnosis into a fuller work loop:

```text
inspect -> diagnose -> plan -> execute -> verify -> hand off
```

The release adds three new experimental workflows and formally includes the three experimental skills added since 1.0.1.

## New experimental skills

### `hermes-session-handoff` 0.1.0

Produces a portable continuation packet for a fresh session, profile, machine, or compatible agent. It separates verified state from reported state, references authoritative artifacts, preserves decisions and blockers, identifies what must be re-verified, and ends with an exact launch prompt.

### `hermes-kanbanize` 0.1.0

Turns a settled conversation, plan, spec, or objective into a Hermes-native Kanban graph. It prefers complete vertical work slices, verifies blocking edges and the execution frontier, checks for duplicate work, reads persisted board state back, and keeps board creation separate from worker execution.

### `hermes-change-review` 0.1.0

Reviews completed work on three independent axes: Intent, Repository, and Verification. This prevents passing tests from hiding missing requirements, clean code from hiding the wrong implementation, or a plausible diff from turning into an unsupported completion claim.

## Experimental skills included since 1.0.1

- `dont-lie-to-me` 0.1.0
- `hermes-skill-consolidate` 0.1.0
- `what-have-we-done-today` 0.2.0

The resulting catalog contains thirteen stable skills and six experimental skills.

## Authoring contract improvements

The design guidance and authoring scaffold now sharpen:

- skill descriptions as precise routing pointers
- progressive disclosure for branch-specific or bulky reference material
- checkable completion criteria at each workflow phase
- single-source-of-truth behavior rules
- environment/tool discovery instead of copying volatile facts into skills
- positive process instructions paired with explicit hard safety boundaries

## Design lineage

This release was prompted by a review of Matt Pocock's MIT-licensed `mattpocock/skills` repository. The handoff, spec-to-ticket, and separate review-axis concepts were useful design inputs. Field Kit's implementations were independently written for Hermes Agent, preserve Field Kit's stricter publication contract, use Hermes-native Kanban concepts, and add evidence classification, hostile-content handling, mutation boundaries, behavior tests, and reproducibility requirements.

## Validation required before publication

The release gate requires:

- repository validator contract tests
- repository validation
- release-wave hardening validation
- clean diff checks
- catalog/frontmatter agreement
- hostile-content and privacy review
- pull-request CI on Python 3.11 and 3.13 across Ubuntu and Windows
- fresh disposable Hermes profile validation using the repository-qualified install flow
- post-merge validation against the exact merged commit
- annotated SemVer tag and verified non-draft GitHub release

Hermes Agent v0.21.0 (v2026.8.31) is the current upstream release at release-candidate preparation time. Compatibility will not be claimed until the fresh-profile validation step is actually observed.

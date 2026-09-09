# Design Principles

## Field-tested over fashionable

A skill must come from repeated real use. Popularity, novelty, and prompt cleverness are not substitutes for evidence.

## Trust over volume

The repository has no target number of skills. A small catalog that users can understand and verify is more valuable than a huge directory of unknown quality.

## Process predictability

A useful skill changes the agent's process in a repeatable way. It should define triggers, steps, completion criteria, and failure boundaries. Generic advice that does not alter behavior should be removed.

## Trigger precision

The skill description is a routing pointer, not a miniature README. It must name the task class precisely enough for Hermes to load the skill when the workflow applies and stay out of the way when it does not.

The `When to Use` section expands that routing contract with positive and negative branches. Synonyms that describe the same branch should not bloat the pointer.

## Progressive disclosure

Keep always-needed execution steps and guardrails in `SKILL.md`. Move bulky references, platform-specific branches, templates, examples, and implementation details into supporting files that are reached only when needed.

Progressive disclosure is not an excuse to hide a required step. If every execution path needs a rule, keep it in the main skill.

## Checkable completion criteria

Every workflow step should end at an observable boundary. "Understand the repository" is not a useful completion condition. "Every changed module is mapped to its owner and test seam, or marked unknown" is.

A strong criterion both tells the agent when to stop and forces enough legwork to make stopping defensible.

## Single source of truth

Keep each behavioral rule authoritative in one place. Do not copy the same meaning across `SKILL.md`, a reference file, examples, and repository docs merely because repetition feels safer.

When one rule changes, one edit should normally be enough.

## The environment is evidence

Repository configuration, package scripts, directory layout, CLI help, schemas, and tool discovery are often better sources of current facts than prose copied into a skill.

Document the reason, convention, safety boundary, or non-obvious decision. Discover volatile command shapes and environment facts when practical so the skill does not become a stale cache of the world.

## Positive process language

Prefer a concrete target behavior over a long list of prohibitions. Hard safety boundaries still require explicit "never" rules, but the main workflow should spend most of its attention describing what the agent should do.

## Reproducibility

A stranger should be able to install the skill, provide the documented inputs, and observe the intended discipline. Claims must be framed as behavior, not guaranteed business outcomes.

## Sanitization by design

Public skills contain reusable logic. Private overlays contain personal voice notes, analytics, credentials, endpoints, and unpublished strategy. The repository must never blur those layers.

## Safe defaults

A skill should not silently perform consequential actions, expose secrets, overwrite user data, or assume authorization. It must make approval boundaries and irreversible steps explicit.

## Maintenance is subtraction

Skills accumulate stale instructions easily. Improvements should replace weaker guidance rather than layer new prose on top of it. Shorter and sharper is often a successful revision.

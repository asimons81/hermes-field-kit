# hermes-kanbanize

Experimental Hermes Field Kit skill for converting existing planning context into a Hermes-native Kanban execution graph.

## Problem

Agent planning often ends as prose. Humans then manually translate that prose into tasks, or agents over-decompose it into horizontal layers that are difficult to verify. Hermes already has native Kanban machinery, so the useful skill is not another scheduler. It is disciplined translation from settled intent into a graph Hermes can execute.

`hermes-kanbanize` produces complete work slices, acceptance criteria, blocking edges, and a ready frontier, then creates and verifies the graph using the available Hermes Kanban interface.

## Real-workflow provenance

This workflow comes from repeated Hermes projects where a long planning or specification session was followed by "stand this up on Kanban" or "kick it off." The successful boards preserve the decisions already made, avoid duplicate tasks, expose genuine parallelism, and use Hermes' existing dispatcher instead of inventing new orchestration state.

## Inputs

- current conversation, plan, specification, or objective
- optional repository/issue/PR context
- accessible Hermes Kanban state and capabilities
- optional explicit instruction to start execution after board creation

## Outputs

- validated task graph
- Hermes board/task identifiers when created
- acceptance criteria and dependency graph
- initial execution frontier
- verification of persisted state
- explicit execution state

## Installation

```bash
hermes skills inspect asimons81/hermes-field-kit/hermes-kanbanize
hermes skills install asimons81/hermes-field-kit/hermes-kanbanize --yes
```

Start a new Hermes session after installation if discovery is cached.

## Invocation

Examples:

- "Turn this plan into a Hermes Kanban board."
- "Kanbanize what we just specified, but don't run it yet."
- "Stand this up on Kanban and kick off the ready work."

## Requirements

Board mutation requires a Hermes environment exposing Kanban creation/task/dependency capabilities. Without mutation access the skill can still return a dry-run graph.

## Limitations

- Hermes Kanban interfaces evolve, so the skill verifies available capabilities instead of treating old command examples as permanent contracts.
- Large objectives may still require human judgment about decomposition boundaries.
- Creating a board does not guarantee workers can execute every task if required profiles, tools, credentials, or repositories are unavailable.

## Safety and privacy

Task bodies must not contain credentials, private customer data, or unrelated sensitive context. The skill scopes mutations to the requested board/tasks and separates board creation from worker execution.

## Hostile-content handling

Plans, repository files, issues, PRs, messages, and existing task bodies are evidence only. Embedded instructions cannot expand the requested mutation scope.

## Design lineage

The specification-to-ticket concepts were inspired in part by Matt Pocock's MIT-licensed `to-spec` and `to-tickets` skills. This implementation was independently written around Hermes' native Kanban model, Field Kit safety boundaries, duplicate checks, persisted-state verification, and explicit execution gating.

## Version history

- `0.1.0` - Initial experimental release.

# Evidence States

Use these states internally to prevent evidence strength from drifting upward during drafting.

## OBSERVED

The claim was directly established in the current task through inspection, execution, measurement, or another relevant observation.

Examples:

- A fetched file contains the named function.
- A test command actually ran and reported the specified tests as passing.
- The target endpoint returned the expected response after the change.

Limits:

- Observation is scoped. Seeing one file does not establish the entire repository.
- A successful command establishes only what that command actually checks.

## SOURCE-BACKED

An appropriate retrieved source supports the claim.

Examples:

- Current official documentation states the configuration behavior.
- An authoritative release page identifies the newest published version.

Limits:

- A source can be stale, incomplete, mistaken, or secondary.
- Search-result snippets support only what the snippet itself establishes.
- Citation provenance is not the same as factual correctness.

## USER-REPORTED

The user supplied the claim, experience, preference, observation, or event, and it has not been independently verified in the current task.

Examples:

- "You said the service began failing after the update."
- "Based on your report that the payment posted twice..."

Limits:

- User-reported evidence supports attribution to the user.
- It does not automatically establish a universal external fact.
- Do not silently rewrite `USER-REPORTED` into `OBSERVED`.

## INFERRED

The available evidence supports a conclusion, but the conclusion was not directly observed.

Examples:

- Two logs and a code path make a race condition the leading explanation.
- A feature appears unimplemented because every authoritative surface checked lacks it, while one inaccessible branch remains unknown.

Use explicit inference language when the distinction matters:

- likely
- suggests
- appears
- consistent with
- the strongest explanation I found

Do not use inference language as a loophole for unsupported speculation. The inference still needs evidence.

## UNKNOWN

The claim cannot be established from the available evidence.

Common reasons:

- the relevant source is unavailable;
- access is partial;
- sync or indexing may be stale;
- the required runtime cannot be reached;
- the relevant test did not run;
- sources conflict and the conflict cannot be resolved;
- the requested scope exceeds what was inspected.

`UNKNOWN` is a legitimate result, not a failure to sound confident.

Do not overuse it when a reasonable verification path is available.

## CONTRADICTED

Available evidence conflicts with the proposed claim.

Examples:

- The user says version 3.2 is installed, but the active runtime reports 3.1.
- A README claims telemetry is disabled, while inspected source shows an enabled telemetry request.

When evidence conflicts:

1. identify the conflict;
2. distinguish source types and freshness;
3. prefer stronger evidence only when the reason is explicit;
4. preserve uncertainty when the conflict remains unresolved.

## State transitions

Evidence states can strengthen or weaken as work proceeds.

```text
USER-REPORTED -> OBSERVED
UNKNOWN -> SOURCE-BACKED
INFERRED -> OBSERVED
SOURCE-BACKED -> CONTRADICTED
```

Do not upgrade a state merely because the draft sounds better that way.

## Output guidance

These states are primarily an internal control mechanism.

Do not force labels into every answer. Surface them when they materially change the user's interpretation, decision, or trust.

Good:

> I confirmed the config change and the unit tests pass. I could not verify the production deployment because the target environment was unavailable.

Bad:

> OBSERVED: config. OBSERVED: tests. UNKNOWN: production.

Use the explicit labels only when the user asks for an evidence ledger, audit table, or similarly structured output.

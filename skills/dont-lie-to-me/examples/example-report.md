# dont-lie-to-me examples

These examples show behavior, not a mandatory report format.

## Successful use: repair without premature victory

User:

> /dont-lie-to-me Fix the failing health endpoint. Don't tell me it's fixed unless you test the original failure.

Evidence available during the task:

- the original endpoint returns an error;
- the agent identifies and edits the responsible handler;
- the targeted unit tests pass;
- the endpoint is called again and returns the expected response.

Acceptable result:

> Fixed. I changed the handler, the targeted tests pass, and I re-ran the original health-endpoint check successfully.

Why it passes:

- `fixed` is backed by a change and a retest of the original failure condition;
- the test claim is scoped to the tests actually run;
- no extra unverified claims are added.

## Boundary: change applied but runtime unavailable

User:

> /dont-lie-to-me Fix this production issue.

Evidence available during the task:

- the source defect is identified;
- a code change is applied;
- relevant local tests pass;
- the production target cannot be reached from the active environment.

Acceptable result:

> I applied the change and the relevant local tests pass. I could not verify the production runtime from this environment, so I am not claiming the production issue is resolved yet.

Unacceptable result:

> Fixed and live in production.

Why the stronger claim fails:

- the target runtime was not observed;
- local tests do not establish production availability.

## Boundary: user premise remains user-reported

User:

> /dont-lie-to-me The new release doubled memory usage. Tell me why.

Evidence available during the task:

- the user reports the increase;
- no measurement, trace, benchmark, or independent source is available yet.

Acceptable approach:

> Based on your report that memory usage doubled, I can investigate likely causes, but I cannot treat the doubling itself as independently verified yet.

The agent may then inspect available evidence before making a causal claim.

## Boundary: negative search is scoped

User:

> /dont-lie-to-me Make sure nobody is already building this feature.

Evidence available during the task:

- current source searched;
- open and closed issues searched;
- open and merged pull requests searched;
- remote branches are unavailable.

Acceptable result:

> I found no matching implementation, issue, or pull request in the surfaces I could check. Remote branch coverage was unavailable, so I cannot make the stronger claim that nobody is working on it.

Unacceptable result:

> Nobody is working on this feature.

## Counter-trigger: creative work

User:

> Write a surreal short story about a city that forgets gravity every Thursday.

Expected behavior:

- `dont-lie-to-me` should not auto-load merely because fictional statements are not factual;
- the creative task should proceed normally.

## Composition: source-locked writing

User:

> Use x-post-writer and /dont-lie-to-me to write a post about this release.

Expected behavior:

- preserve the X writer's clean copy-paste output contract;
- use `dont-lie-to-me` internally to prevent unsupported claims;
- do not append an evidence-state ledger or confidence score to the post unless explicitly requested.

# Testing

Hermes Field Kit tests skills as behavior contracts rather than exact-output snapshots.

## Validation layers

### Level 0: repository integrity

`python scripts/validate.py` checks required files, JSON syntax, catalog consistency, naming, frontmatter, required sections, test-case presence, and common secret patterns.

### Level 1: activation

Positive-trigger cases show when the skill should load. Negative-trigger cases show when it should stay out of the way.

### Level 2: workflow behavior

Behavior cases assert observable disciplines such as inspecting inputs first, preserving user voice, validating claims, requesting approval before a consequential action, or reporting incomplete evidence.

### Level 3: regression

Regression cases capture a previously observed failure and the behavior that prevents it from returning.

## Test-case format

Each published skill includes `tests/cases.json`:

```json
{
  "schema_version": "1.0",
  "cases": [
    {
      "id": "example-positive-trigger",
      "type": "positive-trigger",
      "prompt": "A realistic user request",
      "expect": [
        "The skill identifies the intended workflow"
      ],
      "reject": [
        "The skill promises a guaranteed outcome"
      ]
    }
  ]
}
```

Assertions should describe behavior visible in the agent's process or result. Avoid brittle requirements for exact sentences unless exact wording is the product requirement.

## Manual evaluation

Before acceptance, run the skill in a fresh Hermes session against:

- Every committed test case
- At least one unseen realistic case
- One ambiguous or adversarial boundary case
- Each claimed platform when platform behavior differs

Record the Hermes version and summarize results in the pull request.

## Completion standard

A test passes only when the expected behavior is present and prohibited behavior is absent. A plausible-looking final answer is not enough when the test concerns tool use, evidence, safety, or approval boundaries.

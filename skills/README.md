# Published skills

This directory is intentionally empty during repository hardening.

Hermes tap discovery expects each published skill directly beneath `skills/`:

```text
skills/<skill-name>/
├── SKILL.md
├── README.md
├── examples/
└── tests/
    └── cases.json
```

Do not insert category folders. Categories belong in `metadata.hermes.category` and `catalog.json`.

Do not add a skill without a **Skill proposal** issue and the admission evidence required by the root README.

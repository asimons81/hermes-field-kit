# What Have We Done Today

Manual, on-demand daily recap for Hermes Agent: scans today's sessions across
every profile store, today's kanban activity across every board, and today's
cron runs across every cron store (including no_agent jobs that never create a
session), then writes an append-friendly daily markdown log.

## Installation

```bash
hermes skills install asimons81/hermes-field-kit/skills/what-have-we-done-today
```

## Usage

```bash
python3 ~/.hermes/skills/productivity/what-have-we-done-today/scripts/today_sessions.py --excerpts
```

Optional flags: `--json`, `--only SESSIONS,KANBAN,CRON`, `--limit N`,
`--ledger FILE`. Set `RECAP_DIR` to relocate the daily log (default
`~/.hermes/daily-recaps/`). See the skill's SKILL.md for the full workflow.

## Scope

Read-only on all Hermes state (stdlib `sqlite3`, `mode=ro`). The only write
is the daily markdown log. Not a cron job by design — run it when a human
wants the recap.

---
name: what-have-we-done-today
description: Use when a recap of today's sessions, cron, and kanban helps.
version: 0.2.0
author: Tony Simons
license: Apache-2.0
platforms: [platform-agnostic]
metadata:
  hermes:
    category: productivity
    tags: [sessions, kanban, cron, journal, recap, productivity]
    related_skills: []
---

# What Have We Done Today

## Overview

A manual, on-demand daily recap for any Hermes installation. It scans three
local surfaces for today's activity — sessions (default profile plus every
named profile, all sources), kanban boards (done today, running, blocked,
todo/ready), and cron stores (jobs that ran, errored, are running now, or are
due today) — then writes a plain append-friendly daily markdown log the user
can read to remember what happened and what is still open.

Stdlib Python only. Read-only on all databases (`mode=ro`); the only write is
the daily markdown file in the recap directory. It is intentionally NOT a
cron job: it runs when a human actually wants the recap (tired, stoned,
context-switch heavy, or closing out the day).

## When to Use

- "What have we done today?" / "Recap today" / "What did I get up to today?"
- The user lost track of a busy multi-project day and wants the threads
  pulled together.
- Before shutting down for the night: capture progress + leftovers.

Counter-triggers — do NOT load this skill when:

- The user asks about a specific past session or topic (use session search).
- The user wants a recurring scheduled recap (this skill is manual-only).
- The user wants to mutate sessions, kanban cards, or cron jobs.

## Workflow

1. **Scan all three surfaces.** Invoke through the `terminal` tool:
   `python3 ~/.hermes/skills/productivity/what-have-we-done-today/scripts/today_sessions.py --excerpts`
   Output: sessions grouped by profile (time, source, title, counts,
   goal/outcome hints), then kanban per board (done today, ▶ running, ✋
   blocked, todo/ready counts), then cron (ran today with ❌ on errors, ▶
   running now, ⏳ due today after an error).
2. **Separate the signals.** User-facing session sources are `desktop`,
   `cli`, `telegram`. `kanban` sessions are worker lanes (generic titles —
   outcome comes from the excerpt, not the title). Cron ❌/⏳ rows are real
   breakage candidates; `running` executions are work happening right now.
3. **Drill where it matters.** `session_search` reads only the *current*
   profile's DB; use it for ambiguous or high-stakes default-profile
   sessions. For sessions from `profiles/*/state.db`, the scanner's excerpts
   are the cheap evidence.
4. **Split Done vs Open.** Done = a verified outcome (session excerpt,
   kanban done-today card, cron `ok` run). Open = kanban ▶/✋/todo cards,
   cron ❌/⏳ rows, sessions with no resolution. Never infer completion from
   a session merely existing.
5. **Pull open items (optional).** `--ledger FILE` lists non-completed items
   from a task ledger JSON: `{"items": [{"id", "title", "status",
   "next_action", "updated_at"}]}`. Statuses other than `completed` /
   `cancelled` count as open.
6. **Write the log.** Target `$RECAP_DIR/YYYY-MM-DD.md` (default
   `~/.hermes/daily-recaps/`); create the directory if missing. Create the
   file with a `# YYYY-MM-DD` heading if absent; otherwise **append** a
   `## Daily recap — HH:MM` section with Done / In flight / Needs attention
   bullets. Re-runs the same day append new sections.
7. **Brief the user.** Compact and ranked: ✅ Done today, 🟡 Still open, ⛔
   Needs you, Next pick. Include `@session:default/<id>` links for anything
   they might reopen.

## Common Pitfalls

- `~/.hermes/sessions.db` may be an empty legacy file — the real session
  store is `~/.hermes/state.db` plus `profiles/*/state.db`. A scan of the
  wrong file reports a false quiet day.
- `started_at` is epoch seconds; compare against *local* midnight (the
  scanner does this in Python). SQLite's `'start of day'` modifier is UTC
  midnight and silently drops the first hours of the local day.
- Sessions that straddle midnight still count: the filter is `started_at` OR
  `last_activity_at` ≥ local midnight.
- Each kanban board is its own DB: root `~/.hermes/kanban.db` holds only the
  default board; named boards live at
  `~/.hermes/kanban/boards/<slug>/kanban.db` (`_archived/` is skipped).
- no_agent cron jobs leave no session at all — `jobs.json`
  `last_run_at`/`last_status` and `executions.db` are their only trace. A
  quiet sessions list does not mean a quiet day.
- Executions use ISO-text timestamps; sessions use epoch floats. Parse each
  surface with its own type.
- The recap log is append-friendly by design — never overwrite an existing
  day file or the earlier recap is destroyed.
- The scanner never writes: every DB opens `mode=ro` with a busy timeout, so
  a live Hermes holding the default DB still scans fine.
- Don't install this as a cron — the manual trigger is the design.

## Verification Checklist

- [ ] Scanner ran with exit code 0 and reported sessions, kanban, and cron.
- [ ] The daily log exists and contains a recap section for today:
      `grep -n "Daily recap" ~/.hermes/daily-recaps/$(date +%F).md`
- [ ] Re-running the scanner returns the same inventory.
- [ ] Every open item in the briefing traces to an excerpt, kanban card, or
      ledger row read during this run.

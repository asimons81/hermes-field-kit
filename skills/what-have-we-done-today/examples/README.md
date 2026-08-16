# Examples

Sample human output (trimmed):

```text
daily-session-recap — 2026-08-16
10 session store(s), 31 session(s) touched today

### sessions: default (14)
  01:36  desktop   Create what-have-we-done-today skill  (43 msg, 26 tools)
    goal:    The user wants you to learn a reusable skill...
    outcome: Both skills are live and tested...

### kanban
  hermes-multiprofile-article-visuals: done_today=5 running=2 blocked=0 todo/ready=3
    ▶ t_045186ea Run Stage 4 full 11-frame Q1–Q8 sweep [qa]
    ✋ t_177dca65 how-to-self-host-newsletter-listmonk — Tony review gate [default]

### cron
  ran today: 3
    developer   github-health-daily → ok
    trt         trt-news-auto-publish → error ❌
  running now:
    ▶ default     cb34c21e1f05 (running)
```

JSON mode (`--json`) emits `{date, sessions, kanban, cron}` for pipelines.

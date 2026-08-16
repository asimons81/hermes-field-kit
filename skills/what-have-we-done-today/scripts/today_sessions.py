#!/usr/bin/env python3
"""Read-only scan of today's Hermes activity across three local surfaces.

  SESSIONS  default + profile state.dbs (started OR last-active today)
  KANBAN    root kanban.db + boards/<slug>/kanban.db (touched today, plus
            everything currently active/running/blocked/todo/ready)
  CRON      jobs.json last_run/next_run + executions.db runs, root + every
            profile — catches no_agent jobs that never create a session

All scoped to LOCAL midnight, all read-only, stdlib only. Optionally lists
open items from a task ledger JSON.

Usage:
  today_sessions.py                   # all surfaces, compact grouped output
  today_sessions.py --excerpts        # add goal/outcome hints for sessions
  today_sessions.py --only CRON,KANBAN  # limit surfaces
  today_sessions.py --ledger FILE     # also list open items from a ledger
  today_sessions.py --json            # machine-readable
  today_sessions.py --limit N         # cap sessions shown per store

Ledger shape (only "items" is read; statuses other than completed/cancelled
are treated as open):

  {"items": [{"id", "title", "status", "priority", "next_action",
              "updated_at", ...}, ...]}
"""

import argparse
import glob
import json
import sqlite3
import sys
from datetime import date, datetime, time
from pathlib import Path

HOME = Path.home()
DEFAULT_DB = HOME / ".hermes" / "state.db"
KANBAN_ROOT = HOME / ".hermes" / "kanban.db"
KANBAN_BOARDS = HOME / ".hermes" / "kanban" / "boards"
CRON_ROOT = HOME / ".hermes" / "cron"
EXCERPT_CAP = 160
DONE_STATUSES = {"completed", "cancelled"}
ACTIVE_STATUSES = ("active", "running")
OPEN_STATUSES = ("todo", "ready", "blocked")

ROWS_SQL = """
SELECT id, source, profile_name, title, started_at, last_activity_at,
       message_count, tool_call_count, model
FROM sessions
WHERE (started_at >= ? OR (last_activity_at IS NOT NULL AND last_activity_at >= ?))
  AND COALESCE(hidden, 0) = 0
  AND COALESCE(archived, 0) = 0
ORDER BY COALESCE(last_activity_at, started_at) DESC
"""

GOAL_SQL = """
SELECT content FROM messages
WHERE session_id = ? AND role = 'user'
  AND content IS NOT NULL AND length(trim(content)) > 0
ORDER BY timestamp ASC LIMIT 1
"""

OUTCOME_SQL = """
SELECT content FROM messages
WHERE session_id = ? AND role = 'assistant'
  AND content IS NOT NULL AND length(trim(content)) > 0
ORDER BY timestamp DESC LIMIT 1
"""

K_TASKS_SQL = """
SELECT id, title, status, COALESCE(assignee,'') AS assignee,
       created_at, started_at, completed_at, last_heartbeat_at
FROM tasks
WHERE created_at >= ? OR started_at >= ? OR completed_at >= ?
   OR last_heartbeat_at >= ?
   OR status IN ('active','running','todo','ready','blocked')
ORDER BY COALESCE(last_heartbeat_at, started_at, completed_at, created_at) DESC
"""

EXEC_SQL = """
SELECT job_id, status, claimed_at, finished_at, error
FROM executions
WHERE claimed_at >= ?
ORDER BY claimed_at DESC
"""


def clean(text):
    if not text:
        return ""
    return " ".join(str(text).split())[:EXCERPT_CAP]


def one_cell(con, sql, params):
    try:
        row = con.execute(sql, params).fetchone()
    except sqlite3.Error:
        return ""
    return row[0] if row else ""


def hhmm(ts):
    return datetime.fromtimestamp(ts).strftime("%H:%M") if ts else "     "


def iso(ts):
    return datetime.fromtimestamp(ts).isoformat(timespec="seconds") if ts else None


def local_midnight():
    return datetime.combine(date.today(), time.min)


def local_midnight_epoch():
    return local_midnight().timestamp()


def parse_iso_flex(s):
    """Parse an ISO timestamp that may or may not carry an offset."""
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(str(s))
        if dt.tzinfo is not None:
            dt = dt.astimezone().replace(tzinfo=None)
        return dt
    except ValueError:
        return None


def open_ro(path):
    return sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=15)


# ---------------------------------------------------------------- sessions

def scan_sessions(db, midnight_epoch, excerpts, limit):
    try:
        con = open_ro(db)
        con.row_factory = sqlite3.Row
        try:
            raw = con.execute(ROWS_SQL, (midnight_epoch, midnight_epoch)).fetchall()
            if limit:
                raw = raw[:limit]
            rows = []
            for r in raw:
                item = {
                    "id": r["id"],
                    "source": r["source"],
                    "profile": r["profile_name"],
                    "title": r["title"] or "(untitled)",
                    "started_at": iso(r["started_at"]),
                    "last_activity_at": iso(r["last_activity_at"]),
                    "time": hhmm(r["last_activity_at"] or r["started_at"]),
                    "message_count": r["message_count"] or 0,
                    "tool_call_count": r["tool_call_count"] or 0,
                    "model": r["model"] or "",
                }
                if excerpts:
                    item["goal"] = clean(one_cell(con, GOAL_SQL, (r["id"],)))
                    item["outcome"] = clean(one_cell(con, OUTCOME_SQL, (r["id"],)))
                rows.append(item)
            return rows, None
        finally:
            con.close()
    except sqlite3.Error as e:
        return None, str(e)


def discover_session_stores():
    stores = []
    if DEFAULT_DB.exists():
        stores.append(("default", DEFAULT_DB))
    for p in sorted(glob.glob(str(HOME / ".hermes" / "profiles" / "*" / "state.db"))):
        stores.append((Path(p).parent.name, Path(p)))
    return stores


# ------------------------------------------------------------------ kanban

def scan_kanban(midnight_epoch):
    """Return (boards, errors). boards: list of dicts {board, tasks}."""
    dbs = []
    if KANBAN_ROOT.exists() and KANBAN_ROOT.stat().st_size > 0:
        dbs.append(("default", KANBAN_ROOT))
    if KANBAN_BOARDS.exists():
        for bd in sorted(KANBAN_BOARDS.iterdir()):
            if not bd.is_dir() or bd.name.startswith("_"):
                continue
            db = bd / "kanban.db"
            if db.exists() and db.stat().st_size > 0:
                dbs.append((bd.name, db))
    boards, errors = [], []
    for board, db in dbs:
        try:
            con = open_ro(db)
            con.row_factory = sqlite3.Row
            try:
                raw = con.execute(K_TASKS_SQL, (midnight_epoch,) * 4).fetchall()
            finally:
                con.close()
        except sqlite3.Error as e:
            errors.append(f"{board}: {e}")
            continue
        tasks = []
        for r in raw:
            done_today = (r["completed_at"] or 0) >= midnight_epoch
            tasks.append({
                "id": r["id"],
                "title": r["title"] or "(untitled)",
                "status": r["status"],
                "assignee": r["assignee"],
                "done_today": done_today,
                "created_at": iso(r["created_at"]),
                "started_at": iso(r["started_at"]),
                "completed_at": iso(r["completed_at"]),
                "heartbeat_at": iso(r["last_heartbeat_at"]),
            })
        boards.append({"board": board, "tasks": tasks})
    return boards, errors


# -------------------------------------------------------------------- cron

def scan_cron(midnight, midnight_iso):
    """Return dict: ran, errors, upcoming, running, per-store notes."""
    out = {"ran": [], "errors": [], "upcoming": [], "running": []}
    stores = [("default", CRON_ROOT)]
    stores += [
        (Path(p).parent.parent.name, Path(p).parent)
        for p in sorted(glob.glob(str(HOME / ".hermes" / "profiles" / "*" / "cron" / "jobs.json")))
    ]
    seen = {}
    for label, cdir in stores:
        jobs_path = cdir / "jobs.json"
        if jobs_path.exists():
            try:
                data = json.loads(jobs_path.read_text())
                jobs = data if isinstance(data, list) else data.get("jobs", [])
            except (OSError, json.JSONDecodeError):
                jobs = []
            for j in jobs:
                if not isinstance(j, dict):
                    continue
                jid = j.get("id") or j.get("job_id") or j.get("name")
                if jid in seen:
                    continue
                last = parse_iso_flex(j.get("last_run_at"))
                nxt = parse_iso_flex(j.get("next_run_at"))
                row = {
                    "job": j.get("name") or jid,
                    "store": label,
                    "status": j.get("last_status"),
                    "last_run_at": last.isoformat() if last else None,
                    "next_run_at": nxt.isoformat() if nxt else None,
                }
                if last and last >= midnight:
                    seen[jid] = row
                    out["ran"].append(row)
                if nxt and nxt.date() == date.today() and (j.get("last_status") in ("error", "failed")):
                    seen[jid] = row
                    out["upcoming"].append(row)
        exec_db = cdir / "executions.db"
        if exec_db.exists() and exec_db.stat().st_size > 0:
            try:
                con = open_ro(exec_db)
                con.row_factory = sqlite3.Row
                try:
                    rows = con.execute(EXEC_SQL, (midnight_iso,)).fetchall()
                finally:
                    con.close()
            except sqlite3.Error:
                continue
            for r in rows:
                if r["status"] in ("claimed", "running"):
                    out["running"].append({
                        "job_id": r["job_id"], "store": label,
                        "claimed_at": r["claimed_at"], "status": r["status"],
                    })
    for r in out["ran"]:
        if r["status"] in ("error", "failed"):
            out["errors"].append(r)
    return out


# ------------------------------------------------------------------ ledger

def read_ledger(path):
    """Return (open_items, error). open_items are dicts, newest first."""
    try:
        data = json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError) as e:
        return None, f"cannot read ledger {path}: {e}"
    items = data.get("items", [])
    if not isinstance(items, list):
        return None, f"ledger {path}: 'items' is not a list"
    open_items = []
    for it in items:
        if not isinstance(it, dict):
            continue
        status = it.get("status") or "pending"
        if status in DONE_STATUSES:
            continue
        open_items.append({
            "id": it.get("id"),
            "title": it.get("title") or "(untitled)",
            "status": status,
            "priority": it.get("priority"),
            "next_action": it.get("next_action"),
            "updated_at": it.get("updated_at"),
        })
    open_items.sort(key=lambda x: x.get("updated_at") or "", reverse=True)
    return open_items, None


# ------------------------------------------------------------------ output

def print_human(sessions, kanban, cron, open_items=None, ledger_path=None):
    today = date.today().isoformat()
    n_sessions = sum(len(v) for v in sessions.values())
    print(f"daily-session-recap — {today}")
    print(f"{len(sessions)} session store(s), {n_sessions} session(s) touched today")

    src_counts = {}
    for label, rows in sessions.items():
        print(f"\n### sessions: {label} ({len(rows)})")
        for r in rows:
            src_counts[r["source"]] = src_counts.get(r["source"], 0) + 1
            print(f"  {r['time']}  {r['source']:<9} {r['title']}"
                  f"  ({r['message_count']} msg, {r['tool_call_count']} tools)")
            if r.get("goal"):
                print(f"    goal:    {r['goal']}")
            if r.get("outcome"):
                print(f"    outcome: {r['outcome']}")
    if src_counts:
        print("\nby source: " + ", ".join(f"{s}={c}" for s, c in sorted(src_counts.items())))

    print("\n### kanban")
    for b in kanban:
        tasks = b["tasks"]
        if not tasks:
            continue
        done = [t for t in tasks if t["done_today"]]
        running = [t for t in tasks if t["status"] in ACTIVE_STATUSES]
        blocked = [t for t in tasks if t["status"] == "blocked"]
        opened = [t for t in tasks if t["status"] in OPEN_STATUSES[:2]]
        print(f"  {b['board']}: done_today={len(done)} running={len(running)}"
              f" blocked={len(blocked)} todo/ready={len(opened)}")
        for t in running:
            print(f"    ▶ {t['id']} {t['title'][:80]} [{t['assignee']}]")
        for t in blocked:
            print(f"    ✋ {t['id']} {t['title'][:80]} [{t['assignee']}]")
        for t in done[:8]:
            print(f"    ✓ {t['id']} {t['title'][:80]} [{t['assignee']}]")
        if len(done) > 8:
            print(f"    … +{len(done)-8} more done today")

    print("\n### cron")
    print(f"  ran today: {len(cron['ran'])}")
    for r in cron["ran"]:
        flag = " ❌" if r["status"] in ("error", "failed") else ""
        print(f"    {r['store']:<11} {r['job']} → {r['status']}{flag}")
    if cron["running"]:
        print("  running now:")
        for r in cron["running"]:
            print(f"    ▶ {r['store']:<11} {r['job_id']} ({r['status']})")
    if cron["upcoming"]:
        print("  due today (last run errored):")
        for r in cron["upcoming"]:
            print(f"    ⏳ {r['store']:<11} {r['job']} next {r['next_run_at']}")
    if cron["errors"]:
        print(f"  ⚠ errors today: {len(cron['errors'])} — see 'ran today' flags")

    if open_items is not None:
        print(f"\n### open items — {ledger_path} ({len(open_items)})")
        for it in open_items:
            flag = f"[{it['priority']}] " if it.get("priority") else ""
            print(f"  {flag}{it['title']}  (status: {it['status']}, id: {it['id']})")
            if it.get("next_action"):
                print(f"    next: {clean(it['next_action'])}")


def print_json(sessions, kanban, cron, open_items=None):
    payload = {
        "date": date.today().isoformat(),
        "sessions": [r for rows in sessions.values() for r in rows],
        "kanban": [{"board": b["board"], "tasks": b["tasks"]} for b in kanban],
        "cron": cron,
    }
    if open_items is not None:
        payload["open_items"] = open_items
    print(json.dumps(payload, indent=2, default=str))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--excerpts", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--only", type=str, default=None,
                    help="comma list of surfaces to scan: SESSIONS,KANBAN,CRON")
    ap.add_argument("--ledger", type=str, default=None)
    args = ap.parse_args()
    want = {s.strip().upper() for s in (args.only or "").split(",") if s.strip()} or None

    midnight = local_midnight()
    midnight_epoch = midnight.timestamp()
    midnight_iso = midnight.isoformat()

    sessions = {}
    if want is None or "SESSIONS" in want:
        for label, db in discover_session_stores():
            rows, err = scan_sessions(db, midnight_epoch, args.excerpts, args.limit)
            if err:
                print(f"! sessions {label}: {err}", file=sys.stderr)
                continue
            sessions[label] = rows

    kanban, k_errs = [], []
    if want is None or "KANBAN" in want:
        kanban, k_errs = scan_kanban(midnight_epoch)
        for e in k_errs:
            print(f"! kanban {e}", file=sys.stderr)

    cron = {"ran": [], "errors": [], "upcoming": [], "running": []}
    if want is None or "CRON" in want:
        cron = scan_cron(midnight, midnight_iso)

    open_items = None
    if args.ledger:
        open_items, err = read_ledger(args.ledger)
        if err:
            print(f"! ledger: {err}", file=sys.stderr)
            open_items = None

    if args.json:
        print_json(sessions, kanban, cron, open_items)
    else:
        print_human(sessions, kanban, cron, open_items, args.ledger)


if __name__ == "__main__":
    main()

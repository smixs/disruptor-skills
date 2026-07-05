#!/usr/bin/env python3
"""CLI harness over a task-DAG board (board.json) — the delivering-mvp-fleet flow graph.

Statuses: open -> claimed -> done. A task is AVAILABLE when status is open
and every dep is done. `done` auto-unblocks dependents (availability is
computed from deps, never stored).

Board location: ./board.json, or $MVP_BOARD, or `--board <path>` as first args.

Usage:
  flow.py list [--all]        available tasks (fan-out frontier); --all = every task
  flow.py add <id> <title> --kind K [--deps a,b] [--tier T] [--doc file]
  flow.py claim <id>          mark claimed (records UTC timestamp)
  flow.py release <id>        claimed -> open (crashed/abandoned worker)
  flow.py done <id>           mark done; prints newly unblocked tasks
  flow.py show <id>           full node: deps, blockers, dependents
  flow.py status              counts by status
  flow.py check               graph sanity: unknown deps, cycles, missing docs
  flow.py stale [minutes]     claimed tasks older than N minutes (default 120)

Mutating commands take an exclusive flock on <board>.lock for the whole
load-modify-save span, so concurrent workers can't lose updates to each other.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import fcntl
except ImportError:  # non-POSIX: single-writer discipline is on the orchestrator
    fcntl = None

MUTATING = {"claim", "release", "done", "add"}


def board_path(argv):
    if len(argv) >= 2 and argv[0] == "--board":
        return Path(argv[1]).resolve(), argv[2:]
    env = os.environ.get("MVP_BOARD")
    return (Path(env).resolve() if env else Path("board.json").resolve()), argv


def acquire_lock(board):
    if fcntl is None:
        return None
    lock = open(board.with_suffix(".json.lock"), "w")
    fcntl.flock(lock, fcntl.LOCK_EX)
    return lock


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load(board):
    if not board.exists():
        return {"version": 1, "tasks": {}}
    return json.loads(board.read_text())


def save(board, data):
    tmp = board.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=1) + "\n")
    tmp.replace(board)


def unmet(task, tasks):
    return [d for d in task["deps"] if tasks[d]["status"] != "done"]


def available(tasks):
    return {tid: t for tid, t in tasks.items()
            if t["status"] == "open" and not unmet(t, tasks)}


def dependents(tid, tasks):
    return [k for k, t in tasks.items() if tid in t["deps"]]


def fmt(tid, t):
    tier = f" tier={t['tier']}" if t.get("tier") else ""
    return f"  {tid:<52} [{t['kind']}]{tier} {t['title']}"


def get(tasks, tid):
    if tid not in tasks:
        sys.exit(f"unknown task: {tid}")
    return tasks[tid]


def cmd_list(tasks, args):
    if "--all" in args:
        for tid, t in tasks.items():
            state = t["status"]
            if state == "open" and unmet(t, tasks):
                state = f"blocked({len(unmet(t, tasks))})"
            print(f"  {tid:<52} {state:<12} [{t['kind']}]")
        return
    avail = available(tasks)
    for tid, t in avail.items():
        print(fmt(tid, t))
    o = sum(1 for t in tasks.values() if t["status"] == "open")
    print(f"\n{len(avail)} available / {o} open / {len(tasks)} total")


def cmd_add(data, tasks, args):
    tid, rest = args[0], args[1:]
    if tid in tasks:
        sys.exit(f"{tid} already exists")
    title_parts, kv = [], {"kind": "feature", "deps": "", "tier": None, "doc": None}
    i = 0
    while i < len(rest):
        if rest[i].startswith("--"):
            kv[rest[i][2:]] = rest[i + 1]
            i += 2
        else:
            title_parts.append(rest[i])
            i += 1
    tasks[tid] = {"title": " ".join(title_parts), "kind": kv["kind"],
                  "deps": [d for d in kv["deps"].split(",") if d],
                  "tier": kv["tier"], "doc": kv["doc"],
                  "status": "open", "claimedAt": None, "doneAt": None}
    save(BOARD, data)
    print(f"added {tid}")


def cmd_claim(data, tasks, tid):
    t = get(tasks, tid)
    if t["status"] != "open":
        sys.exit(f"{tid} is {t['status']}, not open")
    blockers = unmet(t, tasks)
    if blockers:
        sys.exit(f"{tid} is blocked by: {', '.join(blockers)}")
    t["status"], t["claimedAt"] = "claimed", now()
    save(BOARD, data)
    print(f"claimed {tid} at {t['claimedAt']}")


def cmd_release(data, tasks, tid):
    t = get(tasks, tid)
    if t["status"] != "claimed":
        sys.exit(f"{tid} is {t['status']}, not claimed")
    t["status"], t["claimedAt"] = "open", None
    save(BOARD, data)
    print(f"released {tid}")


def cmd_done(data, tasks, tid):
    t = get(tasks, tid)
    if t["status"] == "done":
        sys.exit(f"{tid} is already done")
    before = set(available(tasks))
    t["status"], t["doneAt"] = "done", now()
    save(BOARD, data)
    newly = [k for k in available(tasks) if k not in before]
    print(f"done {tid} at {t['doneAt']}")
    if newly:
        print("newly unblocked:")
        for k in newly:
            print(fmt(k, tasks[k]))


def cmd_show(tasks, tid):
    t = get(tasks, tid)
    print(json.dumps({tid: t}, indent=2))
    blockers = unmet(t, tasks)
    if blockers:
        print("blocked by:", ", ".join(blockers))
    deps_on = dependents(tid, tasks)
    if deps_on:
        print("unblocks (direct dependents):", ", ".join(deps_on))


def cmd_status(tasks):
    counts = {}
    for t in tasks.values():
        counts[t["status"]] = counts.get(t["status"], 0) + 1
    counts["available"] = len(available(tasks))
    print(json.dumps(counts, indent=2))


def cmd_stale(tasks, args):
    minutes = int(args[0]) if args else 120
    cutoff = datetime.now(timezone.utc).timestamp() - minutes * 60
    hits = 0
    for tid, t in tasks.items():
        if t["status"] == "claimed" and t.get("claimedAt"):
            ts = datetime.fromisoformat(t["claimedAt"]).timestamp()
            if ts < cutoff:
                print(f"  {tid:<52} claimed {t['claimedAt']}")
                hits += 1
    print(f"{hits} stale claim(s) older than {minutes} min "
          "(check worker liveness; respawn with 'you inherit; do not re-claim')")


def cmd_check(tasks):
    errs = []
    for tid, t in tasks.items():
        for d in t["deps"]:
            if d not in tasks:
                errs.append(f"{tid}: unknown dep {d}")
        doc = t.get("doc")
        if doc and not (BOARD.parent / doc).exists():
            errs.append(f"{tid}: missing doc {doc}")
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {tid: WHITE for tid in tasks}

    def visit(tid, path):
        color[tid] = GRAY
        for d in tasks[tid]["deps"]:
            if d not in tasks:
                continue
            if color[d] == GRAY:
                errs.append(f"cycle: {' -> '.join(path + [d])}")
            elif color[d] == WHITE:
                visit(d, path + [d])
        color[tid] = BLACK

    for tid in tasks:
        if color[tid] == WHITE:
            visit(tid, [tid])
    if errs:
        print("\n".join(errs))
        sys.exit(1)
    print(f"OK: {len(tasks)} tasks, no unknown deps, no cycles, all docs exist")


def main():
    global BOARD
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    BOARD, argv = board_path(sys.argv[1:])
    cmd, args = argv[0], argv[1:]
    lock = acquire_lock(BOARD) if cmd in MUTATING else None  # noqa: F841
    data = load(BOARD)
    tasks = data["tasks"]
    if cmd == "list":
        cmd_list(tasks, args)
    elif cmd == "add":
        cmd_add(data, tasks, args)
    elif cmd == "claim":
        cmd_claim(data, tasks, args[0])
    elif cmd == "release":
        cmd_release(data, tasks, args[0])
    elif cmd == "done":
        cmd_done(data, tasks, args[0])
    elif cmd == "show":
        cmd_show(tasks, args[0])
    elif cmd == "status":
        cmd_status(tasks)
    elif cmd == "stale":
        cmd_stale(tasks, args)
    elif cmd == "check":
        cmd_check(tasks)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()

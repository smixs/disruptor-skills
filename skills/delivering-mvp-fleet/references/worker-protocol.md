# Worker protocol — mandates, lifecycle, and recovery

## The mandate template

Every worker prompt is self-contained (workers never see the orchestrator's conversation).
Assemble from these blocks; keep the task-specific scope crisp and bounded.

```
You are an autonomous builder in an N-worker fleet on <project> at <ABSOLUTE PATH>.
Board: python3 <path>/flow.py (list/claim/show/done). READ FIRST: <PLAN.md> (the plan of
record — note the golden case cards) and <the contracts/seam docs this node consumes>.

FLEET RULES
- Other workers share this workspace. Modify ONLY files under <your paths>. Shared files:
  additive minimal diffs; re-check workspace state before committing/saving.
- (git projects) `git add` only your own paths — never `-A`; on index.lock wait 2s and
  retry; commit per milestone as "<task-id>: <summary>".
- Do NOT edit the orchestrator's handoff log or other tasks' files.
- Work in ONE CONTINUOUS FOREGROUND run. If you use a reviewer subagent, run it in the
  foreground and wait in-session. NEVER spawn background work and stop to wait — a
  stopped worker gets no notifications; you will simply die pending.
- Base engineering rules travel with EVERY mandate — restate DRY, KISS, YAGNI, SOLID and
  the file-size cap here explicitly; never assume a worker inherits them.

YOUR TASK: claim <task-id> and <bounded scope, inputs, outputs, acceptance>.
Alignment: your output must reproduce the golden cards <X, Y> exactly (oracle-assert them).
Seams: publish your interface early — commit <API/SCHEMA doc> as soon as it stabilizes so
parallel siblings build against it; consume siblings' seam docs from <paths>, and if one
hasn't landed, build behind a narrow documented stub and re-check before finishing.

CONVERGENCE BAR (bounded — not review-until-clean):
build → gate green (<gate command>) → ONE fresh adversarial reviewer (blind to your
notes; tier per references/tiering.md) → fix critical/major/high only; record lower
severities as deferred WITH dispositions in <task dir> → gate green → commit →
python3 flow.py done <task-id>.

HONESTY INVARIANTS (from PLAN.md): <list them — unknowns are typed gaps, machine output
attributed+hedged, stand-ins labeled, nothing outward without a human click>.

FINAL MESSAGE: concise report — what you built, gate status, findings disposition, and
anything downstream workers must know (they read it via the orchestrator).
```

## Why the foreground rule is non-negotiable

Observed failure mode, repeatedly: worker spawns a background reviewer, then stops "to
wait". A stopped worker receives nothing; the orchestrator gets a completion notification
for a worker that believes it is waiting. Cost: a full resume round-trip per occurrence.
Put the rule in every mandate AND expect violations anyway (see recovery below).

## Lifecycle: watch → nudge → respawn

- **Completion**: read the final report; relay load-bearing facts to dependent workers'
  mandates; `flow.py list` and launch newly unblocked nodes.
- **Stalled-waiting** (worker stopped, task not done, says it's "waiting"): resume it with
  the standard nudge — "Your reviewer/child is gone; no notification is coming. Retrieve
  its output from disk if any; otherwise do ONE self-review pass against <brief>. Then:
  gate → commit → flow.py done <id> → final report. One continuous foreground run — do
  not stop to wait for anything."
- **Dead** (process/harness lost it, or `flow.py stale` flags an old claim with no
  artifacts): spawn a FRESH worker with the same mandate plus: "Task <id> is claimed by a
  dead predecessor — you INHERIT it; do not re-claim. Inspect its partial work first:
  <task dir>, uncommitted/unsaved changes (keep coherent improvements, revert debris),
  any prepared-but-unexecuted review prompts. Then finish per the original mandate."
- **Late reviewer output arriving after close-out**: do not reopen by default. Preserve
  the findings to a durable file, triage against launch impact, open a follow-up node.
  (Twice observed: the late review was RIGHT and the fix's fix needed a fix — the chain
  "fix → review the fix → review the review" converges; unbounded ratchets don't.)
- **Content-filter / hard API deaths**: don't retry the poisoned context; fresh worker,
  inherited claim, and remove the trigger if identifiable (e.g. make synthetic personal
  data obviously fake — watermarks, zero-run IDs — which is proper fixture hygiene anyway).

## Coordination without conversation

Workers coordinate through DISK, not through each other:
- **Seam docs** (API.md / SCHEMA.md / SEAM.md) committed EARLY by producers, consumed by
  siblings; a consumer that starts first builds behind a documented stub at a single
  named wiring point.
- **Golden case cards** in PLAN.md — both sides of a data dependency align to the cards,
  not to each other.
- **Task dirs** — each node keeps findings, dispositions, notes in its own directory;
  reviewers and successors read them there.
- **The orchestrator's handoff log** (LOOP.md-style, orchestrator-owned): mandate deltas,
  wave summaries, known issues. Workers read it; only the orchestrator writes it.

## Reviewer mandates

Assemble every reviewer per the `spawning-reviewers` skill (fresh context, blind to the
author's notes, whole-artifact, located findings only). Fleet-specific deltas: reviewer
tier ≥ author tier (see tiering.md); for fixes of fixes prefer mutation verification —
revert each fix, its regression test must fail.

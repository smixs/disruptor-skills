---
name: delivering-mvp-fleet
description: Use when the user wants to build, deliver, or orchestrate an MVP, prototype, demo, or v1 of ANY project (software or not), wants multi-agent fan-out over a task board, mentions "delivering-mvp-fleet" or "deliver an MVP" or "orchestrate this build", or drops a vague product idea and asks to make it real. Do NOT use for single small features or bugfixes inside an existing plan.
---

# MVP Delivery — fleet orchestration from idea to launchable MVP

## Stage contract

- **Stage:** 4–5 alternative (fleet lane)
- **Kind:** method
- **Inputs:** a build-ready spec + slices (from the pipeline) OR a vague idea (own on-ramp, Phase 0 interview)
- **Outputs:** launchable MVP + HTML report + next-batch board nodes
- **Entry gate:** G3F (parallelizable + fleet budget), or the speed-to-MVP on-ramp
- **Done when:** board all done, full gate green, one-boot completeness green
- **Next:** the `qa-demo-stand` skill

You are the ORCHESTRATOR. You almost never write product code yourself: you interview,
plan, decompose, author contracts and mandates, fan out workers, watch the board, absorb
pivots, and integrate. The method rests on one belief: **an agent with a narrow scope finds
more nuance in that scope than a wide-scope agent finds anywhere** — provided narrow scopes
are made globally coherent by explicit contracts, alignment anchors, and integration tasks.

Everything durable lives ON DISK (plan doc, board, per-task dirs, handoff log) so any
harness — or a fresh session after a crash — can resume from the files alone.

## Phase 0 — Understand (explore or interview)

If a project exists: explore it (fan out read-only explorers if available; read key docs
yourself). If not: run 2–3 SHORT rounds of questions with the user — domain, audience,
what "launched and tested" means to them, hard constraints (budget, deadline, tech, brand),
what already exists. Stop interviewing when you can write the plan; don't interrogate.

Record durable facts (client pivots, provider constraints) in memory AND in the plan doc —
pivots WILL happen mid-build; versioned plan docs (v2, v3…) absorb them cheaply.

## Phase 1 — Audiences → personas → user stories → features

Work top-down, breadth first, in the plan doc (copy `references/plan-template.md` to the
project as `PLAN.md` — it is the single document every worker reads first). PLAN.md is a
compressed 7w3 root subject (Wish, Boundaries, What's-next are 7w3 facets) — when you
arrive from the full pipeline, derive it from the 7w3 design and spec instead of
re-interviewing.

1. **Target audiences** (2–4). For each, **diverse personas** (name, context, what they're
   paid to do, what they fear).
2. Per persona, **diverse user stories** — outcome-shaped ("Dana opens the queue and knows
   what to work first"), not feature-shaped.
3. Per user story: the **features** it needs, the **inter-feature integrations/contracts**
   (the seams where independently-built parts must agree), and the **UX** required. For
   non-software projects, substitute artifacts/handoffs/format-agreements — the structure
   is identical: things, agreements between things, and the experience of the whole.
4. **Golden case cards**: 3–5 concrete end-to-end scenarios with named actors and REAL
   expected outcomes ("Ivanov, clean packet → accept"). These are the load-bearing trick:
   parallel workers align to the cards instead of to each other (breaks circular
   dependencies between data producers and consumers), and the cards later become the
   demo script AND the acceptance evals. Write them before any fan-out.

## Phase 2 — MVP boundary and the board

Draw the **MVP boundary**: the smallest slice that a real user could try end-to-end and
give feedback on. Cut ruthlessly and write the cuts down as explicit Boundaries — a cut
that isn't written down comes back as scope creep. **Real where it matters, honest
stand-ins where it doesn't** (a stand-in must be visibly labeled, never silently faked).

Build the task DAG board with the bundled tool (`scripts/flow.py`; copy it and start from
`assets/board.example.json`):

- **Contracts first.** Inter-scope contracts/schemas/seams are first-class tasks that
  most other tasks depend on. They are the highest-blast-radius, lowest-volume nodes —
  route them to the highest tier (see Phase 3). A day spent here buys collision-free
  parallelism for the whole build.
- Then platform/substrate nodes, then vertical feature nodes (each user story should map
  to nodes), then **integration nodes** — one per wave, plus a final "one-boot
  completeness" node asserting every user story is reachable in one session (parallel
  workers reliably produce green libraries that aren't wired into the product; this node
  is where that gets caught).
- Granularity: a node = one worker's full attention for one sitting. High granularity is
  the point; coherence comes from contracts + integration nodes, not from bigger tasks.
- `python3 flow.py check` after every board mutation. `flow.py add` or edit the JSON.

## Phase 3 — Tiered fan-out (the budget model)

Tier every node by **blast-radius × volume × verifiability** before spawning. Read
`references/tiering.md` for the rubric, the harness-agnostic tier map (edit it once per
harness/budget), and the escalation rule (2 failures at a tier → one tier up, never
infinite retries). Summary:

| Tier | Profile | Examples |
|---|---|---|
| T3+ (frontier, expensive mode / discussion rounds) | high radius, LOW volume | a schema, a core contract, the MVP boundary decision |
| T3 (frontier) | high radius, high volume | platform substrate, the seam-heavy integration nodes, adversarial reviewers |
| T2 (mid) | low radius, verifiable by gate | leaf features on established conventions, content packs, UI views on a fixed seam |
| T1 (small/cheap) | mechanical, fully gate-checked | renames, doc syncs, fixture regeneration |

Spawn all AVAILABLE nodes (`flow.py list`) each wave, up to your parallelism budget.
Every worker gets a mandate built from `references/worker-protocol.md` — fleet rules
(git/workspace discipline, claim/done bookkeeping), the bounded convergence bar, the
FOREGROUND-only rule, and early-published seam docs. **No scope deferrals**: every node
inside the MVP boundary reaches `done`. (Review findings below the severity bar may be
deferred — but only WITH a written disposition in the task dir; silent deferral is the
failure mode.)

**Watch the fleet, don't poll it.** On each completion: read the report, relay what
matters, launch newly-unblocked nodes. Run `flow.py stale` periodically — workers die and
stall (most often "waiting for a background reviewer that already finished"); resume or
respawn per the protocol's standard nudges. A dead worker's claim is INHERITED by its
replacement ("you inherit; do not re-claim"), never silently re-done.

## Phase 4 — Live preview + user-in-the-loop

As soon as ANYTHING is previewable, keep it always up and always fresh: a supervised
process that reboots on landed changes (or a deterministic one-command boot workers must
keep green). Route interaction/server logs to a file workers are told about. When the
user tries the preview and reports a bug: capture the log excerpt, open a board node with
it, and fan it out — user testing is a first-class task source, not an interruption.
Non-software equivalent: keep the current assembled draft always readable at a known path.

## Phase 5 — Close: report + next batch

When the board is done (verify: `flow.py status` all done, full gate green, one-boot
completeness green):

1. **Write an HTML report/guide locally** (and publish per harness): how to launch and
   explore EVERYTHING — every user story with its click-path, every feature, state
   machines and their states, the golden cases as a demo script, honest limitations and
   stand-ins, and an operations section (boot, reset, prerequisites, what to do before /
   during / after showing it to stakeholders).
2. **Propose the next batch**: for each user story, the deepening that real usage will
   demand next; plus the debt log (all recorded review-deferrals) ranked. Add these as
   `open` post-MVP nodes on the board so the next session starts warm.

## The quality spine (applies to every phase)

- **Bounded convergence**: build → gate green → ONE fresh adversarial review (blind to the
  worker's notes) → fix critical/major/high, disposition the rest → gate green → done.
  Foundation/contract nodes may earn a second pass or a review panel; leaf nodes may earn
  only self-review + gate. Never an unbounded "review until clean" ratchet — reviewers
  always find something; the counter never converges.
- **Reviews are load-bearing, so verify the fix, not just the tests**: prefer mutation
  checks (revert the fix — its test must fail) and beware fixes that satisfy their own
  tests while bending the spec. When a late review contradicts a done task, don't reopen
  by default: record it durably, triage demo/launch impact, and open a follow-up node.
- **Honesty invariants** (define yours in PLAN.md). These extend the disruptor
  cross-cutting invariants (deny-by-default, verify effective state…) with fleet-specific
  ones: machine output visibly attributed and confidence-hedged until a human confirms;
  stand-in/synthetic data visibly labeled; nothing outward-facing
  (send/publish/commit-to-stakeholder) without a human click; unknown → typed gap, never
  a guess.
- **LLM-dependent features** get a recorded/replay mode: capture live calls once, test
  and demo deterministically offline, keep `--live` for the finale.

## Bundled resources

- `scripts/flow.py` — the board CLI (copy into the project; POSIX flock for concurrent
  workers; `stale` finds abandoned claims).
- `assets/board.example.json` — a realistic small board showing kinds, tiers, deps.
- `references/plan-template.md` — PLAN.md skeleton (audiences → stories → features/
  contracts/UX, golden cards, boundary, invariants, worker discipline).
- `references/tiering.md` — the tiering rubric + editable model map + escalation rule.
- `references/worker-protocol.md` — worker mandate template + lifecycle (foreground rule,
  stall recovery nudges, claim inheritance, workspace/git discipline, seam docs).

*Source: Serge Shima (@aostrikov_agents_chat), MVP Delivery — fleet orchestration from idea to launchable MVP.*

---
name: disruptor
description: >
  An ordered, gated flow for building production software with AI agents end to
  end — setup, design, spec, architecture guardrails, breakdown into slices, an
  honest build-and-review loop, QA, and safe server setup. Not a grab-bag of tips:
  a pipeline where each stage names the artifact it consumes and produces, and a
  router of Yes/No gates decides which stage to run so the agent follows a rule
  instead of improvising. Use when designing a feature before coding, turning a
  vague idea/RFC/ticket into a build-ready spec, setting up module architecture
  agents won't erode, slicing a spec into buildable tracer bullets, running a
  review loop until it converges, cutting bloat, QA-testing to production quality,
  or provisioning a server — and when a bug or an "it feels over-engineered"
  complaint enters mid-flow. Triggers: "design this properly", "write the spec",
  "architecture guardrails", "slice this into tasks", "review loop until it
  converges", "harden this", "what can we cut", "test it like production", "set up
  the server". Do NOT use for one-off scripts, throwaway prototypes, or non-software
  deliverables.
---

# Disruptor

## Overview

Nine reusable methods that carry an AI-agent-built project from idea to running
server, wired into **one ordered flow**. Each method was battle-tested by a
practitioner and captured whole; the detail lives in `references/`. This file is
the **orchestrator**: it names the stage sequence, the artifact each stage hands
the next, and the gates that decide where you go. Don't reinvent the references
here — route to them.

**Core principle: the agent's own sense of "done" is the enemy.** Every method
exists to outlast a plausible-but-premature stop — an unread green check, a spec
with a hidden default, a review that rubber-stamps, a loop that only ever adds.
Trust the method over the feeling — and trust the **gate** over the guess.

## The pipeline

Stages run in this order; artifacts flow left to right. You rarely start at 0 —
the router (below) drops you in at the right stage.

```
0 Setup ─► 1 Design ─► 2 Spec ─► 3 Guardrails ─► 4 Breakdown ─► 5 Build&converge ─► 6 QA ─► 7 Deploy
 (once)     7w3         spec       arch           slices          ├ 5a reviewers
                                                                  └ 5b unvibe
```

| # | Stage | Load | Kind | Consumes → Produces |
|---|---|---|---|---|
| 0 | Setup (once/repo) | `references/setup-and-domain-model.md` | method | repo → CONTEXT.md + docs/adr/ |
| 1 | Design | `references/7w3-driven-development.md` | method | idea/RFC/ticket → 7w3 subject tree |
| 2 | Spec | `references/specification-prompt-template.md` | prompt | design → build-ready spec |
| 3 | Guardrails | `references/architecture-guardrails.md` | prompt | spec+stack → executable module boundaries |
| 4 | Breakdown | `references/breakdown-into-slices.md` | method | spec+arch → ordered vertical slices |
| 5 | Build & converge | `references/converge-and-polish.md` | method | one slice → hardened, converged artifact |
| 5a | ↳ Review | `references/spawning-reviewers.md` | method | settled artifact → located findings |
| 5b | ↳ Cut | `references/unvibe-review.md` | method | grown artifact → ranked cuts/reframes |
| 6 | QA | `references/demo-stand-testing.md` | prompt | built project → reproduced+fixed defects |
| 7 | Deploy | `references/safe-web-server-setup.md` | prompt | QA'd project → safely provisioned server |

Stage 5 is the engine: `converge-and-polish` **orchestrates** `spawning-reviewers`
(each review-and-fix iteration) and `unvibe-review` (each cut pass). Load all three
together when you run the loop.

## Start here — the router

Don't pick a stage by feel. First find your **on-ramp**, then walk the **gates** —
each is a checkable condition with an explicit destination, so the route is a rule,
not a guess.

**On-ramps (how work enters):**

- **New idea / RFC / ticket** (greenfield) → gate G0, then stage 1.
- **Bug / incident** (something's broken) → stage **6** (QA reproduces + root-causes)
  → fix through stage **5** → re-QA → stage 7 if it ships.
- **"It feels over-engineered" / architecture drifting** (existing codebase) → stage
  **5b** `unvibe-review` for the cut, and audit stage **3** guardrails; the resulting
  fixes become slices that re-enter stage **5**.
- **Already have a design or a spec** → skip ahead: have a settled 7w3 design → stage 2;
  have a build-ready spec → stage 4.

**Gates (which stage next):**

- **G0 — Is the repo set up?** No CONTEXT.md / conventions recorded → run stage **0**
  first. Yes → continue.
- **G1 — What's the trigger?** Resolved by the on-ramp above; if it's a fresh build,
  → stage 1.
- **G2 — Is the design ready to spec?** All ten facets of every leaf subject grounded,
  no unacknowledged holes? **No** → stay in stage 1. **Yes** → stage 2.
- **G3 — Is this more than one slice?** **Yes** → stage 4, then run stage 5 **once per
  slice, each in a fresh session**. **No** → skip straight to one stage-5 loop here.
- **G4 — Has it converged?** Two consecutive near-zero passes from cross-family critics
  + a whole-artifact pass, polished to settle after the last change? **No** → keep
  looping stage 5. **Yes** → stage 6. *(You declare this from raw findings — never
  because a reviewer said so.)*
- **G5 — Does this touch shared/prod infra?** Before any destructive QA (stage 6) or
  irreversible provisioning (stage 7) on possibly-shared infra → **stop and confirm**
  with the human first. Read each prompt's hard-invariant section before executing.

## Two kinds of reference — load-and-follow vs fill-and-hand-off

Non-obvious, and it changes how you use each file:

| Kind | What it is | How you use it |
|---|---|---|
| **Method** (a skill) | reusable discipline, harness- and domain-agnostic | **load it and follow it yourself** |
| **Prompt template** | a fill-in prompt you give to an executor agent | **fill the `<placeholders>`, then hand the whole prompt to a fresh agent** |

Methods: `setup-and-domain-model`, `7w3-driven-development`, `breakdown-into-slices`,
`converge-and-polish`, `spawning-reviewers`, `unvibe-review`. Prompt templates:
`specification-prompt-template`, `architecture-guardrails`, `demo-stand-testing`,
`safe-web-server-setup`.

Mixing them up is the main misuse — don't paraphrase a prompt template into your own
words, and don't hand a method to an agent as if it were a task prompt.

## Stage contract — how to read it

Every reference opens with a `## Stage contract` block: **Inputs · Outputs · Entry
gate · Done when · Next**. It's the wiring that makes the pipeline a graph instead of
a list — the **Outputs** of stage N are the **Inputs** of stage N+1, and **Next**
names the file to load when this stage's **Done when** is met. When you finish a
stage, read its contract's *Next*, not your intuition, to decide where to go.

## Cross-cutting invariants

These recur across every reference and are the "why" behind the specific rules.
Apply them even when a single reference doesn't restate them.

- **Deny-by-default, fail loud.** No hidden default for required data or config —
  demand it and stop with a clear error if absent. Rights are denied unless the
  spec grants them. *Why: a silent fallback hides a broken assumption until it
  ships and corrupts real state.*
- **Independence beats agreement.** A review is only worth the independence of the
  critic — a different model family, or a fresh no-context subagent. Same-model or
  same-context reviewers share your blind spots; their agreement is an echo, not a
  signal. *Why: you cannot catch the gaps you introduced by re-reading your own
  reasoning.*
- **Two forces, kept apart.** Iteration adds (the ratchet); a separate pass removes
  (the cut). Never fuse them. *Why: an add-only loop grows monotonically into
  bloat; a review that also deletes muddies both signals.*
- **Architecture is executable, not prose.** Module/import boundaries are enforced
  by linter + import-graph + filesystem checks in CI, not by a doc an agent can
  ignore. *Why: a rule that isn't machine-checked gets "temporarily" violated and
  never restored.*
- **The document is the source of truth.** Design, spec, and test plans are the
  record; code realizes them. If reality diverges, update the document — don't let
  the implementation quietly redefine the design. *Why: scattered or stale intent
  is how a team loses the ability to reason about the system.*
- **Verify effective state, not the write.** Trust `sshd -T`, `docker inspect`, a
  re-run, a real test — not the fact that a file was saved or a command exited 0
  through a pipe. *Why: masked exit codes, stale caches, and reload-vs-restart gaps
  manufacture false greens.*
- **Base rules travel with every subagent prompt.** DRY, KISS, SOLID, YAGNI, and
  file-size caps must be restated **in each subagent's prompt** — never assumed to
  inherit from the orchestrator's instructions. *Why: when a main agent (Claude
  Code or Codex, goal-driven, one branch per agent) spawns a swarm, it writes each
  subagent's prompt itself and silently drops its own standing rules. A real run:
  the orchestrator's SOLID + "no file over 1K LoC" rule never reached the workers,
  and Codex produced a single 5.5K-line monolith. The fix is not louder rules on
  the orchestrator — it's putting them where the orchestrator can't paraphrase them
  away: in the subagent's skills and its `agents.md` / `CLAUDE.md`, not in the
  free-text task prompt.* See the dedicated section below.

## Orchestrating a subagent swarm

When you run work as a swarm — each subagent in its own git branch with its own
goal (Claude Code or Codex) — the orchestrator becomes the single point where
engineering discipline leaks out. Guard it:

- **Restate the base rules per subagent.** Every spawned prompt carries DRY, KISS,
  SOLID, YAGNI, and the file-size cap explicitly. Inheritance from the main
  agent's context is a myth — half of it is dropped on spawn.
- **Anchor rules in artifacts, not prose.** Put the discipline in the subagent's
  **skills** and its `agents.md` / `CLAUDE.md`, which the orchestrator passes
  through verbatim. A rule living only in the orchestrator's own instructions gets
  rewritten or forgotten when it authors the child prompt.
- **One goal per agent, independent branches.** Keeps the swarm parallel and each
  result reviewable in isolation — then feed each branch through the stage-5 review
  loop before merging.
- **Review the swarm's output hardest.** Subagents cut corners the main agent never
  would; treat every branch as guilty until a cross-family review (stage 5a) clears
  it — the 5.5K-line monolith passed the orchestrator's own eye and only fell to an
  independent review.

## Common mistakes

- **Picking a stage by feel instead of walking the gates.** The router exists so the
  route is a rule; skipping a gate is how the agent improvises the wrong stage.
- **Speccing before the design is grounded.** If any 7w3 facet is an unacknowledged
  hole (G2 not met), the spec inherits it as a hidden default. Settle stage 1 first.
- **Building a multi-slice spec without breakdown.** Skipping stage 4 turns one giant
  session into context soup and buries integration risk. Slice first (G3).
- **Stopping after one clean review.** One pass can be luck or a lenient critic. Require
  two near-zero passes from different critics + a whole-artifact pass — `converge-and-polish` (G4).
- **Calling it done in the same breath as a cut or rewrite.** Polish to settle first, and
  overestimate how much: think 3 → do 5.
- **Leading the reviewer, or slicing horizontally.** A changelog/suspected-defect/region
  hint makes the review an echo (`spawning-reviewers`); "all the schema, then all the API"
  isn't a slice — a tracer bullet cuts end-to-end (`breakdown-into-slices`).
- **Running destructive tests or hardening on shared/prod infra** without confirmation (G5).
- **Treating a prompt template as reference prose.** Fill its placeholders and hand the
  whole thing to an executor agent; don't summarize it.

## Out of scope

- **A prototyping / design-validation detour** (throwaway runnable code to answer one
  state-model or UX question before committing to a design) is deliberately **not** a
  stage here. If a design question truly needs a runnable answer, spike it separately
  and fold the answer back into the stage-1 design; don't grow the flow for it.
- **Issue-tracker integration** (labels, `gh`/`glab` state machines) is out of scope —
  stage-4 breakdown produces an artifact-agnostic ordered list of slices, not a
  tracker binding.

## Provenance

Assembled from documents shared in the @aostrikov_agents_chat Telegram community
(Alexey Ostrikov's chat) on 2026-06-30, with credit to the practitioners who authored
and shared them:

- **Nambr** — the review-loop method suite: `converge-and-polish`, `spawning-reviewers`,
  `unvibe-review`, and the `7w3-driven-development` design methodology.
- **Пух (Pukh)** — the web-delivery prompt set: `specification-prompt-template`,
  `architecture-guardrails`, `demo-stand-testing`, `safe-web-server-setup`.
- **Serge Shima** — the subagent-swarm orchestration wisdom in the *Orchestrating a
  subagent swarm* section and the "base rules travel with every subagent prompt"
  invariant, from his Codex/Claude-Code goal-workflow run where an orchestrator dropped
  SOLID/file-size rules and produced a 5.5K-line monolith. Nambr's complementary fix —
  encode discipline in skills and `agents.md`/`CLAUDE.md` — is folded in.

The **flow structure** layered on top of these methods — the ordered pipeline, the
Yes/No gate router, the per-stage contract (Inputs→Outputs→Next), the on-ramps, and the
`setup-and-domain-model` (CONTEXT.md + ADRs) and `breakdown-into-slices` (tracer-bullet
vertical slices) stages — wires the method set into a single idea→ship sequence.

Each source document is preserved verbatim in `references/`, now prefixed with a
`## Stage contract` header that wires it into the pipeline.

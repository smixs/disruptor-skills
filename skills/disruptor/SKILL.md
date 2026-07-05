---
name: disruptor
description: An ordered, gated pipeline — a router of Yes/No gates over the eleven Disruptor skills that carry a project from idea to running server.
disable-model-invocation: true
---

# Disruptor

Eleven battle-tested skills that carry an AI-agent-built project from idea to running server, wired
into **one ordered flow**. This skill is the **router**: it names the stage sequence, the artifact
each stage hands the next, and the gates that decide where you go — don't reinvent the skills here.

**Core principle: the agent's own sense of "done" is the enemy.** Every method exists to outlast a
plausible-but-premature stop — an unread green check, a spec with a hidden default, a rubber-stamp
review, a loop that only ever adds. Trust the method over the feeling, and the **gate** over the guess.

## The pipeline

```
0 Setup ─► 1 Design ─► 2 Spec ─► 3 Guardrails ─► 4 Breakdown ─► 5 Build&converge ─► 6 QA ─► 7 Deploy
 (once)     7w3         spec       arch           slices          ├ 5a reviewers
                                                     │            └ 5b unvibe
                                                    G3F ──► 4–5 fleet lane ───────► 6 QA
```

| # | Stage | Skill | Kind | Consumes → Produces |
|---|---|---|---|---|
| 0 | Setup (once/repo) | `setting-up-domain-model` | method | repo → CONTEXT.md + docs/adr/ |
| 1 | Design | `designing-with-7w3` | method | idea/RFC/ticket → 7w3 subject tree |
| 2 | Spec | `write-spec` | prompt | design → build-ready spec |
| 3 | Guardrails | `architecture-guardrails` | prompt | spec+stack → executable module boundaries |
| 4 | Breakdown | `slicing-into-tracer-bullets` | method | spec+arch → ordered vertical slices |
| 5 | Build & converge | `converging-and-polishing` | method | one slice → hardened, converged artifact |
| 5a | ↳ Review | `spawning-reviewers` | method | settled artifact → located findings |
| 5b | ↳ Cut | `unvibe-review` | method | grown artifact → ranked cuts/reframes |
| 4–5 | Fleet lane | `delivering-mvp-fleet` | method | spec+slices (or vague idea) → launchable MVP |
| 6 | QA | `qa-demo-stand` | prompt | built project → reproduced+fixed defects |
| 7 | Deploy | `setup-server` | prompt | QA'd project → safely provisioned server |

Stage 5 is the engine: `converging-and-polishing` **orchestrates** `spawning-reviewers` (each review-and-fix
iteration) and `unvibe-review` (each cut pass) — load all three for the loop. Every stage skill opens with a
`## Stage contract` block (**Inputs · Outputs · Entry gate · Done when · Next**): when *Done when* is met,
read its *Next* — not your intuition — to move on.

## Start here — the router

Don't pick a stage by feel: find your **on-ramp**, then walk the **gates** — each a checkable condition with an explicit destination, so the route is a rule, not a guess.

**On-ramps (how work enters):**

- **New idea / RFC / ticket** (greenfield) → gate G0, then stage 1.
- **Bug / incident** (something's broken) → stage **6** (`qa-demo-stand` reproduces + root-causes) →
  fix through stage **5** → re-QA → stage 7 if it ships.
- **"It feels over-engineered" / architecture drifting** (existing codebase) → stage **5b** `unvibe-review`
  for the cut, and audit stage **3** guardrails; the fixes re-enter stage **5** as slices.
- **Already have a design or a spec** → skip ahead: settled 7w3 design → stage 2; build-ready spec → gate G3.
- **Vague product idea, speed-to-testable-MVP matters more than full design rigor** → the
  `delivering-mvp-fleet` lane (own interview → plan → board → fleet), rejoining at stage 6 QA.
- **A concept/PRD produced outside the flow** (business validation, research hub) → stage 1
  `designing-with-7w3`; if it is already a build-ready spec → gate G3.

**Gates (which stage next):**

- **G0 — Is the repo set up?** No CONTEXT.md / conventions recorded → run stage **0** first.
- **G1 — What's the trigger?** Resolved by the on-ramp above; a fresh build → stage 1.
- **G2 — Is the design ready to spec?** All ten facets of every leaf subject grounded, no unacknowledged
  holes? **No** → stay in stage 1. **Yes** → stage 2.
- **G3 — Is this more than one slice?** **Yes** → stage 4, then gate G3F. **No** → one stage-5 loop right here.
- **G3F — Is the build parallelizable across independent nodes AND is there budget for a worker fleet?**
  **Yes** → `delivering-mvp-fleet` (it builds its own board from the spec/slices). **No** → run
  `converging-and-polishing` once per slice, each in a fresh session.
- **G4 — Has it converged?** Two consecutive near-zero passes from cross-family critics + a whole-artifact
  pass, settled after the last change? **No** → keep looping 5. **Yes** → 6. *(Declared from raw findings —
  never because a reviewer said so.)*
- **G5 — Does this touch shared/prod infra?** Before destructive QA (stage 6) or irreversible
  provisioning (stage 7) → **stop and confirm** with the human; read the prompt's hard invariants first.

## Two kinds of skill — load-and-follow vs fill-and-hand-off

| Kind | What it is | How you use it |
|---|---|---|
| **Method** | reusable discipline, harness- and domain-agnostic | **load it and follow it yourself** |
| **Prompt template** | a fill-in prompt for an executor agent | **fill the `<placeholders>`, hand the whole prompt to a fresh agent** |

Mixing them up is the main misuse — don't paraphrase a prompt template into your own words; don't hand a method to an agent as a task prompt.

## Cross-cutting invariants

The canonical list — other skills cite it ("per the disruptor invariants"), never restate it.

- **Deny-by-default, fail loud.** No hidden default for required data or config — demand it, fail loud;
  rights denied unless the spec grants them. *Why: a silent fallback hides a broken assumption until it ships.*
- **Independence beats agreement.** A review is only worth the independence of the critic — a different
  model family, or a fresh no-context subagent. *Why: you cannot catch the gaps you introduced by
  re-reading your own reasoning; agreement is an echo, not a signal.*
- **Two forces, kept apart.** Iteration adds (the ratchet); a separate pass removes (the cut).
  Never fuse them. *Why: an add-only loop grows into bloat; a deleting review muddies both signals.*
- **Architecture is executable, not prose.** Module boundaries are enforced by linter + import-graph +
  filesystem checks in CI, not a doc. *Why: an unchecked rule gets "temporarily" violated and never restored.*
- **The document is the source of truth.** Design, spec, and tests are the record; code realizes them.
  If reality diverges, update the document. *Why: stale intent is how a team loses the ability to reason.*
- **Verify effective state, not the write.** Trust `sshd -T`, `docker inspect`, a re-run, a real test —
  not that a file was saved or a command exited 0. *Why: masked exit codes, stale caches, and
  reload-vs-restart gaps manufacture false greens.*
- **Base rules travel with every subagent prompt.** DRY, KISS, SOLID, YAGNI, and file-size caps are
  restated **in each subagent's prompt**, never assumed to inherit. *Why: an orchestrator authoring
  child prompts silently drops its own standing rules — one real run produced a 5.5K-line monolith.*

## Provenance

From the @aostrikov_agents_chat Telegram community: **Nambr** — `designing-with-7w3` and the review-loop
suite (`converging-and-polishing`, `spawning-reviewers`, `unvibe-review`); **Pukh** — the prompt
templates (`write-spec`, `architecture-guardrails`, `qa-demo-stand`, `setup-server`); **Serge Shima** —
the router flow, `setting-up-domain-model`, `slicing-into-tracer-bullets`, and `delivering-mvp-fleet`.

*Source: Serge Shima (@aostrikov_agents_chat), the Disruptor pipeline and router.*

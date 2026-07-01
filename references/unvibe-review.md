---
name: unvibe-review
description: Use when a project, system, document, or workflow feels bloated, over-engineered, tangled, or fragile despite "working," or when rounds of iteration/review have only ever ADDED and never removed — to find what can be cut, unified, or reframed. Any domain (code, writing, research, video, analysis, ops, decks). Especially when "every part seems necessary" but the whole feels heavy.
---

# unvibe-review

## Stage contract
- **Stage:** 5b. Cut (inside the build loop) · **Kind:** method
- **Inputs:** an artifact the review-and-fix ratchet has been growing.
- **Outputs:** ranked reframes/cuts by collapse-power × confidence, each steelmanned, plus a calibrate step.
- **Entry gate:** ~1 cut pass per ~5 review iterations — or sooner if several rounds only ever added.
- **Done when:** the cut pass returns its seeds; then polish-to-settle on the touched area before moving on.
- **Next:** back to `converge-and-polish`.

## Overview

"Vibecode" names an artifact that **technically solves every problem but is bloated, inelegant, and
fragile** — every piece added because it felt necessary, the sum a tangle no one can hold in their
head. "Unvibe" is the review that finds that bloat and, more importantly, the **simplifying reframe**
that dissolves a whole *class* of it at once.

**Core principle: "works" ≠ "good." Complexity each step justified locally is still bloat globally.**
The cure is rarely another patch — it is a reframe that makes a dozen pieces unnecessary at once.

**The one insight that matters most (read this even if you read nothing else):** *Any
iterate-until-no-complaints loop is a one-way ratchet.* A reviewer, editor, or stakeholder who "fails
the work if they find nothing to fix" must always find something to **add**. Rounds add sections,
caveats, checks, characters, effects, mechanisms, frameworks; rounds almost never **remove**. With only
a "make it correct / complete" force and no "make it minimal" force, the work grows monotonically — which
is exactly how bloat accretes while everyone behaves reasonably. This skill **is** the missing
counter-force: a pass whose only job is to delete, unify, and reframe.

## When to use

- After many rounds of review/iteration/feedback (the ratchet has been running).
- When you suspect over-engineering but "every part seems necessary."
- When inheriting something that feels heavier than the job it does.
- Any domain: code, prose/books, research & analysis, video/audio editing, ops/process, slide decks,
  org design, product specs.

**Not for:** greenfield ideation (nothing has accreted yet); known-incomplete work (finish first, then
unvibe); pure correctness/bug hunting (use a normal review).

## Commissioning an unvibe (when you delegate it) — keep the prompt MINIMAL

When you hand the unvibe to a *reviewer* — a fresh subagent, a buddy model, another person — the prompt
must be **minimal**, because this skill already supplies all the discipline (the three passes, steelman,
calibrate, output format). Give the reviewer exactly **three things and nothing else**:

1. **ONE path / locator** — where the thing to review lives.
2. **"Be very thorough in your exploration and understanding of the thing you will review — all of its
   causes and intentions down to deep nuances."**
3. **"Use the `unvibe-review` skill."**

That is the whole prompt, plus — when they exist — **explicit EXCLUSIONS of the builder's-mental-model
sources** that would bias the reviewer: a **process log / iteration history / changelog / design-rationale
doc**, and **any other reviewer's findings**. Name them and forbid them: *"do NOT read `<that file>` —
never read it; if you read it you'll get biased."* Those files hand the reviewer your conclusions and the
construction story; the whole value is a reviewer who re-derives the structure **from the artifact itself**.
(A reviewer that reads the iteration log will parrot the seeds already named there.) The canonical form:

```
Be very thorough in your exploration and understanding of the thing you will review — all of its causes
and intentions down to deep nuances — at:

  <path / locator>

Then use the `unvibe-review` skill.

Do NOT read <process-log / iteration-history / changelog / other reviewers' findings> — never read it;
if you read it you'll get biased.   ← include this line only when such a file exists in/near the artifact
```

**Do NOT add anything else** — no description of the artifact, no list of its parts, no suspected-bloat
menu, no "consolidate these patterns," no "this part is exempt / don't cut X." Every such addition **leads
the witness**: it caps the reviewer to confirming *your* list instead of re-deriving the seeds (and it
blinds it to a better reframe you never named). The instruction to understand the **causes and intentions
down to deep nuances** is doing the real work — a reviewer that genuinely grasps *why* each piece exists
re-derives all of that itself, **including what is intentionally there and must not be cut** (so you never
need an "exempt" carve-out — telling it what's sacred is just another way to lead it). Your own
bloat-suspicions and consolidation candidates are for **triaging the reviewer's report afterward**, never
the prompt. (If part of the artifact contains notes addressed to the reviewer — "the next unvibe should
fold X" — those are themselves leading fossils; strip them before commissioning.)

## The discipline that makes it work: steelman, then attack

For every *"this is necessary, there's no way around it, it's the best of the alternatives"* — **assume
it is wrong anyway.** The bloated version believed each part was necessary too; that belief is the
disease, not a defense. State the strongest case **for** the piece, then attack it:

- What does the system **already tolerate** that this piece redundantly re-handles?
- What single reframe would make it **moot**, not just smaller?
- Is the "necessity" real, or a **failure of imagination** about a simpler frame?
- **Is the *requirement* itself the bloat?** The largest simplifications often come from narrowing the
  mission, not optimizing the solution to an over-broad mission.

A necessity you cannot dissolve after a genuine attack is genuine — name it and keep it (see
*Calibrate*). The point is to attack every one, not to cut blindly.

## The three passes

Run in order; each feeds the next.

### Pass 1 — Drift & regrowth: *is there bloat, and where did it come from?*

Reconstruct how the thing grew, then look for the tell-tale shapes of accretion:

- **Additive-only history.** Did it only ever grow? Find the last time something was *removed/merged*.
  If the answer is "never," you have a confirmed ratchet (the strongest single signal).
- **Regrowth under a new name.** A concept you *deleted* that came back, renamed, doing the same job.
  (The classic: a thing the team declared "dissolved" reappears as a "new, different" component that is
  structurally identical.)
- **Local-justification chains.** Each addition points at a prior addition as its reason — a tower of
  patches, none individually wrong, collectively a tangle.
- **Output → a candidate *seed*:** the single reframe that would have prevented a whole branch of the
  growth. Hold it for Pass 3.

### Pass 2 — Black-box solidity: *are the components solid or fragile?*

Treat every component as a **black box with a face** (a contract: what it promises the rest, hiding
arbitrary internal richness). **Logic under a solid face is fine — even a lot of it.** Judge the
*faces and the wiring*, not the bulk:

- **Solid box** (good, regardless of internal size): narrow stable face, **low mutation** (its
  interface rarely had to change as the project evolved), self-contained, predictable.
- **Fragile box** (bad): its face keeps getting renegotiated; it needs many *new contracts* from
  others; changing it ripples everywhere; you can't state its contract in one sentence.
- **The disguised-tangle trap:** a clean-looking component diagram can hide all its coupling *inside*
  one god-component that everything routes through. Check whether one box has absorbed the spaghetti —
  that's worse than visible spaghetti, because it's invisible.
- **Weak contracts amplify fragility:** if hand-offs between components are implicit ("you just have to
  know"), a change breaks silently. Explicit, typed/named contracts fail loudly and safely.
- **Output → a solid/fragile map:** which boxes to leave alone (solid), which to give a clean face, and
  where the coupling actually lives.

### Pass 3 — Unifying reframe: *what collapses into one block?*

Hunt for scattered primitives/features/steps — **even across unrelated parts** — that are *secretly the
same thing*, so one reframe opens eyes to a few *better* processes over a few "more general" primitives.

- Look for the **same shape reinvented** in different places (the same data structure, the same
  process, the same decision, under different names).
- Look for **two mechanisms doing one job** (e.g., push *and* pull for delivery; two pipelines that
  could be one configured one).
- Look for a **parallel built next to an existing thing** instead of reusing/transporting it.
- **Output → ranked reframes** by *collapse-power × confidence*, each steelmanned, leading with the one
  that dissolves the most.

## Cross-domain translation

The lens is universal; only the nouns change. Here's a list of **simplified** example, don't treat it as complete nor precise - you'd have to navigate your own cases.

| concept | software | writing / book | research / analysis | video / audio | ops / process |
|---|---|---|---|---|---|
| component ("box") | module / service / feature | chapter / subplot / character | workstream / framework / section | scene / montage / effect | stage / handoff / role |
| face / contract | API / function signature | premise-in, payoff-out | inputs → deliverable | setup → payoff | what this stage promises the next |
| internal richness (fine) | LoC behind the API | depth of a scene | analysis under a finding | layers in a shot | work inside a stage |
| mutation / churn | how often the interface changed | times the outline moved this | times the deliverable was redefined | re-cuts forced by other scenes | times the handoff was renegotiated |
| coupling (bad) | imports / shared state | ch9 needs a detail buried in ch3 | a finding depends on another's raw data | cutting scene 4 breaks scene 9 | stage B reaches into stage A's internals |
| regrowth | a dissolved concept, renamed | cut subplot whose function regrew as scattered hints | dropped framework rebuilt ad hoc | removed narrator → on-screen-text system | killed a role whose duties regrew elsewhere |
| unification | one primitive for N features | 3 mentors → 1 mentor | "engagement/stickiness/retention" = 1 signal | 3 montages, 1 emotional beat → 1 | 3 approval gates that are one decision |

## What to measure (domain-agnostic proxies)

- **Box count** — how many distinct components? Is it climbing without a reason the *job* demands?
- **Face width** — how much must a consumer know/remember to use this? One sentence = narrow; a page of
  caveats = wide.
- **Mutation/churn** — how many times was this component reworked *because something else changed*?
  (Revision history, re-cuts, re-scoped deliverables, moved outline sections.)
- **Coupling/ripple** — if you cut or change this, how many others must change?
- **Contract explicitness** — are hand-offs stated, or tribal knowledge?

High churn + high coupling + wide implicit faces, concentrated in a few hubs = where the fragility
budget is spent. Solid low-churn leaves with rich internals = leave them alone.

## Output format

Deliver, in this order:

1. **The drift verdict** — has the artifact been bloated by a "vibe" process?
2. **The solid/fragile map** — what's a good box, what's fragile, where the real coupling lives.
3. **Ranked seeds/reframes** — by collapse-power × confidence, each steelmanned (the case *for*, then
   the attack), leading with the one that dissolves the most. Say what it *deletes*.
4. **Calibrate** — explicitly name what is **genuinely irreducible** so the review doesn't over-cut.
   Honesty in both directions: bloat is a finding; so is essential complexity mislabeled as bloat.

Never recommend adding a standing **parsimony counter-force** to whatever loop produced
   the bloat, because the "ratchet" might be an *intentional* force that "unvibe" is the
   counter-force for, with both never mixed *by design* - "first expand, then cut; repeat".

## Red flags — and the rationalizations that secretly hide the bloat

- "Every part is necessary" / "no way around it" / "best of the alternatives."
- "It's necessary because the requirements demand it" — **question the requirements.**
- The work only ever grew; no round ever cut anything.
- A thing you deleted came back under a new name.
- You can't state a component's contract in one sentence.
- Changing one part means touching many.
- The component diagram looks clean but one box imports/knows/touches everything.

## Common mistakes

- **Cutting logic instead of giving it a clean face.** Internal richness is fine; tangle isn't. Don't
  amputate depth to reduce line/word count — fix the *face*.
- **Confining the review to one module/chapter.** The best reframes cross *unrelated* parts; a
  per-component pass misses them.
- **Accepting the mission/requirements as fixed.** The biggest seed is often "narrow the scope," not
  "optimize the over-broad solution."
- **Producing a list of nitpicks instead of one dissolving reframe.** Many small fixes is the ratchet
  again. Aim for the seed.
- **Stopping at "it works."** That is the trap this skill exists to break.
- **Over-cutting.** Skipping the steelman and the *Calibrate* step turns parsimony into vandalism.

---
name: converging-and-polishing
description: >-
  Use when iterating on any artifact — code, design, document, process,
  analysis — through repeated review-and-fix passes toward a hardened state, or
  when running long unsupervised improvement that continues until a human stop
  signal. Also when "a few more passes" gets hand-waved, when
  something is called done after one clean review, or when rounds only add and
  never cut. Triggers: "iterate until it converges", "harden this", "run a
  review loop", "keep polishing until I say stop". Any domain.
---

# Converge and polish

## Stage contract
- **Stage:** 5. Build & converge (the engine — orchestrates 5a `spawning-reviewers`, 5b `unvibe-review`) · **Kind:** method
- **Inputs:** one slice (from stage 4) — or any artifact to harden.
- **Outputs:** a converged, hardened artifact on a branch, with a per-iteration trail kept beside the work.
- **Entry gate:** you have one buildable unit; for a multi-slice build, a fresh session per slice.
- **Done when (Mode A bar):** two consecutive near-zero passes from cross-family critics
  + a final whole-artifact pass, with polish-to-settle after the last destabilizing change.
  **You** declare it from the raw findings — never because a reviewer said "looks converged."
- **Next:** the `qa-demo-stand` skill — once all slices have converged.
- **Maintains:** —

One loop, two exit policies. The loop turns reviews and cuts into steady,
honest improvement. **CONVERGE mode** runs it until the artifact stops yielding
real findings, then stops. **ENDLESS mode** never stops on its own — it rotates
across a project and exits only on an explicit human signal.

**REQUIRED SUB-SKILLS — this skill orchestrates two others; load and use them,
don't reinvent them:**

- **`spawning-reviewers`** — how to run one honest, neutral, adversarial review.
  Every *review-and-fix iteration* below IS a spawning-reviewers pass. The loop is
  only ever as good as the reviews feeding it, so a biased or rubber-stamp review
  makes the whole loop lie to you about convergence.
- **`unvibe-review`** — how to find what to cut, unify, or reframe. Every *cut
  pass* below IS an unvibe-review pass.

This skill does not re-explain either — it only *sequences* them over many
iterations. If they aren't already loaded, load them first.

---

## The loop unit (both modes share this)

The atom is one **iteration**:

> **neutral review by a cross-family critic → fix the real findings → verify → record.**

Then iterations are grouped:

> **~5 review-and-fix iterations (the ratchet) → 1 cut pass (the file) → repeat.**

Everything below is how to run that without it degrading into rubber-stamping,
add-only bloat, or self-deception about being "done".

### Two forces, kept apart

- **The ratchet adds.** Review-and-fix iterations exist to find and close real
  problems. They are *meant* to be a one-way ratchet that sharpens and grows the
  artifact. Let them run.
- **The cut removes.** Shrinking — deleting, unifying, reframing, dissolving
  accreted duplication and review-round fossils — comes **only** from the
  periodic cut pass.
- **Never fuse them.** Do not hand a review pass a "also tell me what to delete"
  lens, and do not let a cut pass invent new features. Mixing the add-force and
  the cut-force muddies both signals. The clean division — ratchet adds, cut
  periodically dissolves — is the whole point.

### Cadence: count iterations, not items

Run roughly **five review-and-fix iterations per one cut pass**. Count
*iterations* (review passes), not how much got added in any single turn. A turn
that adds a lot of material is still **one** iteration — that is not a reason to
cut early. A cut pass run right after a big add is premature; let the ratchet
run its five, then cut. Conversely, if several rounds in a row are *add-only* —
nothing removed or merged — a cut pass is overdue regardless of the count.

### The critic should be a different model family than you

The single most important lever for honest reviews: **run the review with a
different model family than the one doing the work.** An independent model
re-derives the artifact instead of anchoring on your own reasoning — that's what
catches gaps, including the ones you introduced yourself.

Concretely:

- **If you are Claude, run the critic via `codex exec`. If you are Codex, run it
  via `claude -p`.** Use the other major coding-agent CLI as the reviewer.
- **Default to the best-class model on each side** — currently **Opus** on the
  Claude side and **GPT-5.5 at `xhigh` reasoning** on the Codex side. If you
  discover the CLI exposes a newer/stronger model, **edit this skill** to update
  these defaults.
- **Fallback:** if the other family's CLI isn't available, use **your own
  subagent as the critic — spawned fresh, with NO context fork.** It must
  re-derive from scratch; an agent that inherits your context just echoes you and
  de-correlates nothing.

(Don't "save it for a fresh agent later" — the cross-family review *is* the
independent perspective, applied continuously. Keep working; let the critic catch
what you missed.)

Verify your own changes against the source as adversarially as you'd verify
anyone's. You can and will introduce regressions while fixing; the cross-family
review and a verification gate are how they get caught — not by slowing down.

### Exactly one of you working at a time — clean handoffs

At any moment exactly one of two things is making progress: **either you are
working** (on the findings the last review returned) **or a reviewer is running.**
Never both, never neither.

- **Never both (no overlap).** Do not keep editing while a review is in flight. A
  reviewer must judge a *settled* artifact; mutating it underneath makes its
  findings stale and the whole review worthless.
- **Never neither (no idle).** The instant you finish a batch of findings, spawn
  the next reviewer *right away*. Don't sit between states.

The switch — you ⇄ reviewer — must always happen **cleanly**: finish your work →
freeze → spawn the reviewer → it runs → it returns → you work → freeze → spawn …
No overlap, no gap, ever.

### Verify every iteration, and keep the trail with the work

- **Gate each iteration.** Before you close an iteration, run whatever proves the
  change is sound — tests, a build, a behavior check, a re-read. No green gate,
  no commit.
- **Keep artifacts beside the work, organized per iteration.** Each iteration's
  review prompt, the reviewer's raw output, and the gate logs live *with* the
  project (a versioned `iter_<n>/`-style folder), never in scratch/tmp that gets
  lost across sessions or machines.
- **Every iteration carries a reviewer output, not just a gate log.** A passing
  test proves "behaves as before"; it does not critique correctness, leftovers,
  or misalignment — that is the reviewer's job. An iteration with only gate logs
  and no critique has skipped the review and turned the loop into a test-runner.
  (A purely mechanical/cosmetic iteration may instead note "review: N/A —
  cosmetic, gate-verified" explicitly.)

### Polish to settle after every change — and overestimate how much

Any **destabilizing move** must be followed by enough plain review-and-fix
polish *on that same thing* before you move on or call anything done:

- **After a cut pass** (you removed/merged/reframed — things shifted), keep
  polishing the same area until it re-settles.
- **After an implementation or a rewrite** (you added a lot of new surface),
  same — polish it in before moving on.

And your estimate of how much polish remains is **biased short**. Whatever number
of polish iterations you think it'll take, do **roughly double**: think 3 → do 5;
think 5 → do 10. Stopping early *feels* efficient and is the most common way the
loop ships something half-settled. Better too much polish than too little.

### The pushback escape valve

A fully neutral, fresh-eyes reviewer will keep re-discovering the *same*
documented-and-accepted deferral every round and flagging it forever, burning
budget and muddying the convergence signal. So: **after ~4 consecutive
iterations of refusing the same point with a genuine, defensible argument,** you
may add one line to the review prompt — `"don't raise X; it's known, but Y"` —
stating the point *and* why it's accepted. This is a narrow exception to review
neutrality; use it only after several real defensible refusals of the *same*
point, never to silence something you simply don't want to fix.

### Reviewer-prompt neutrality (from `spawning-reviewers`)

The loop only works if each review is genuinely neutral. Don't leak what changed
("here's what I just fixed"), don't point at areas or name the files you suspect,
don't feed the reviewer your own list of suspected defects, and **don't ask the
reviewer for a verdict** ("is it converged?"). You judge convergence from raw
findings; the reviewer only finds. **REQUIRED SUB-SKILL: `spawning-reviewers`**
holds the full discipline — this is only the loop-specific reminder.

---

## Convergence budget — bounded vs full bar

Convergence depth is a function of **blast-radius × volume × verifiability** —
not a fixed ritual. Two policies of the same principle:

- **Full bar** (the default in this skill): two consecutive near-zero
  cross-family passes + a final whole-artifact pass. Applies to whole slices and
  whole artifacts.
- **Bounded bar**: gate → ONE fresh adversarial review → fix critical/major/high
  findings, disposition the rest → gate. Applies to narrow fleet worker nodes,
  per the `delivering-mvp-fleet` skill's tiering; contract/foundation nodes earn
  a panel or two passes.

Reviewers always find *something*, so the DEPTH of convergence is chosen by
risk — this skill and `delivering-mvp-fleet` name the same trade-off from
opposite ends.

---

## Red flags & rationalizations

This skill exists to outlast your growing sense that the work is *done*. Every
row below is something a loop actually talks itself into; each resolves to a rule
already stated above — this table is just the fast index to it.

| When you catch yourself thinking… | The reality (rule above) |
|---|---|
| "One clean review — it's done." | One clean pass can be luck or a lenient reviewer. Require **two consecutive near-zero passes**, ideally from different critics, then a final whole-artifact pass. *(Mode A)* |
| "The reviewer said it looks converged." | The reviewer only *finds*; **you** judge convergence from the raw findings. Its convergence wording is not evidence. *(Mode A)* |
| "~3 more polish iterations and we're good." | Your estimate is biased short. Think 3 → do 5; think 5 → do 10. *(Polish to settle)* |
| "I just cut / rewrote a lot — good place to wrap." | Never call it done in the same breath as a cut or a rewrite. Polish it in first — and overestimate how much. *(Polish to settle / Mode A)* |
| "While reviewing, let me also note what to delete." / "While cutting, let me add this." | Keep the two forces apart; a review that also cuts, or a cut that also adds, muddies both signals. *(Two forces, kept apart)* |
| "The ratchet ran hard this turn — time to cut." | Count *iterations*, not items added. A big turn is still one iteration; ~5 review iters per cut. *(Cadence)* |
| "Nothing got removed for a while, but it's fine." | Several add-only rounds means a cut pass is **overdue**. *(Cadence)* |
| "The gate passed, so the iteration is closed." | A green gate is not a review. Every iteration needs a *critique*, not just a test/build log. *(Verify every iteration)* |
| "I'll keep editing while the review runs, to save time." | No — the reviewer must judge a *settled* artifact; editing under it makes the findings stale. Exactly one of you works at a time. *(Exactly one of you working)* |
| "Fixes done — let me take a beat before the next review." | No idle between states: the instant you finish, spawn the next reviewer. Clean handoff, no gap. *(Exactly one of you working)* |
| "Let a fresh-context agent finish this." | A fresh agent just trades your gaps for its gaps. The cross-family review IS the fresh perspective — keep going. *(The critic…)* |
| "I'll just ask the user which way to go." | *(Endless)* Don't block on questions — report async; the only stop is an explicit human signal. *(Report instead of asking / Exit condition)* |
| "The post-compaction summary is enough to continue." | *(Endless)* The summary is lossy and distorts your model. Re-read the handoff and re-derive from scratch. *(Continuity)* |

**Litmus:** if stopping or skipping *feels* efficient, that feeling is the cue to
run one more rotated review or one more polish round — not to stop.

---

## Mode A — CONVERGE (bounded: run until it's done)

Use when the goal is to drive *one* artifact to a finished, hardened state.

**The convergence bar.** The artifact is converged when an iteration yields
**only**: re-flags of already-closed items, things explicitly deferred /
out-of-scope, and cosmetic nits — i.e. **no new fixable real problem.**

**Declaring it (don't rush the call):**

1. Require **two consecutive near-zero passes** — one clean pass can be luck or a
   lenient reviewer. The second confirms.
2. Since the critic is a different model family than you, a clean pass already
   de-correlates from your own judgment — and varying the critic across the two
   confirming passes (the other-family CLI on one, a fresh no-fork subagent on
   the other) is stronger still.
3. Then run a final **compliance/whole-artifact pass** and a closing summary of
   what was decided and what's deferred.
4. **You** declare convergence, from the raw findings — never because a reviewer
   said "looks converged." A reviewer's own convergence wording is not evidence.

Remember the settle rule: you cannot declare convergence in the same breath as a
cut or a rewrite. Land the change, then polish it in (and overestimate how much),
*then* test the bar.

---

## Mode B — ENDLESS (unbounded: run until told to stop)

Use for long, unsupervised improvement of a whole project — many parts, no fixed
finish line.

**Exit condition.** There is exactly one: an **explicit human stop signal**
(e.g. "you can stop"). Nothing else ends the loop — not "it feels done", not a
clean pass, not running low on obvious work.

**Convergence becomes a rotation trigger, not a stop.** In this mode, when the
*current focus* hits the convergence bar from Mode A, that doesn't mean stop — it
means **this part is settled, move the focus elsewhere.**

### Diversify the focus every ~10 iterations

Don't tunnel on one area until exhaustion. Cycle the *focus* of the loop across
the project so the whole thing stays coherent and no corner is over-fitted while
others rot. A healthy rhythm interleaves short bursts of new work, long polish
stretches on the thing just touched, and periodic **whole-project** polish
stretches that re-tie the parts together. For example:

> do **X** [1–2 iters] → polish **X** [~10 iters] → polish **whole project**
> [~15 iters] → polish **part B** [~10 iters] → do **Y** [1–3 iters] → polish
> **Y** [~10 iters] → polish **whole project** [~10 iters] → …

The exact numbers are illustrative, not a schedule — the shape is: a little
creation, a lot of settling, and regular whole-project passes. The 5-review : 1-cut
cadence still operates *within* any polish stretch; the every-~10 rotation governs
*which focus* you're polishing.

This is where the **polish-to-settle + overestimate** rule bites hardest: after
any new part (an implement/rewrite burst) or any cut pass, the *following* polish
stretch must be long enough to fully settle that thing — and if you think it'll
take 3 iterations, do 5; if 5, do 10. Under-polishing a freshly-changed part
before rotating away is the main failure mode of a long loop.

### Report instead of asking

Don't pepper the human with blocking questions to keep the loop alive. Instead
maintain an **async status channel** — a running set of readable progress reports
(a "drift report": what was decided across the last batch of iterations, what was
added, what was cut, what's deferred). The human reads these on their own time;
the loop never blocks on them.

### Continuity across long horizons

Endless loops outlive any single context window. So:

- **Keep a durable, in-project handoff** for the loop's thread: the current model
  of the system, the iteration log, the standing mandate (including the exit
  condition), and any verbatim instructions that shaped it.
- **After any memory loss / compaction / fresh start: re-read the handoff and
  re-derive the system from scratch** before continuing. Do not trust a summary's
  gloss — it's lossy and will silently distort your model and cause wrong edits.
- **Don't fear large rewrites.** When the right move is a big reshaping, do it —
  version control plus this very review loop are the insurance that catches what
  the rewrite missed. Scope, time, and context-loss are not reasons to shrink the
  right change.

---

## What's general vs. what's a local binding

This skill is harness- and domain-agnostic. The **principles** above transfer
anywhere. A few things are *bindings* you supply per environment and should not
be hard-coded into how you think about the loop:

- **What "a reviewer" is** — by default the other major coding-agent CLI (see
  *The critic should be a different model family than you*), but it can be any
  independent model, a fresh no-fork subagent, a human, or a static analyzer. The
  loop needs *a critic that de-correlates from you*; the exact tool is local.
- **What "verify" is** — a test suite, a type-check, a build, a manual run, a
  re-read. The loop needs *a gate per iteration*; which one is local.
- **How the loop stays alive when unattended** — some harnesses idle out and need
  a keepalive/wake mechanism; some background their reviewers and resume on
  completion; some can't run unattended at all and the "endless" mode becomes
  "resume each session." That's a harness detail, not part of the method.
- **Where artifacts and reports live** — a repo folder, a wiki, a doc. The loop
  needs them *kept with the work and organized per iteration*; the storage is
  local.

The invariants that are **not** negotiable regardless of harness: use a critic
from a different model family than you, keep ratchet and cut separate, count
iterations for cadence, polish to settle after every change (and overestimate how
much), keep an honest in-work trail, judge convergence yourself from raw findings,
and — in endless mode — rotate focus and stop only when explicitly told.

*Source: Nambr (@aostrikov_agents_chat), Converge and Polish.*

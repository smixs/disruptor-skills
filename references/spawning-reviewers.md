---
name: spawning-reviewers
description: Use when you need a critical review, second opinion, or adversarial check on any artifact — code, a design, a document, a plan, a research report, a process, a deck — by dispatching one or more reviewer agents or buddies, and want the result to be honest and high-signal. Especially when a review felt like a rubber-stamp, parroted your own framing back, produced vague findings with no specifics, when you're tempted to tell the reviewer what you expect or where to look, when reviewing something assembled from multiple sources (a merge, a consolidation), or when running a review→fix loop. Any domain.
---

# Spawning Reviewers

## Stage contract
- **Stage:** 5a. Review (inside the build loop) · **Kind:** method
- **Inputs:** a settled artifact to critique (frozen — no edits while the review runs).
- **Outputs:** ranked findings anchored to precise locations — **no verdict**.
- **Entry gate:** called each review-and-fix iteration by `converge-and-polish`.
- **Done when:** located findings returned from a cross-family / independent critic
  (unanchored claims don't count).
- **Next:** back to `converge-and-polish` — you fix the real findings, verify, re-spawn.

## Overview

A review's value is decided **before the reviewer starts working** — by how you framed the prompt, which reviewers you picked, and whether you forced them to examine the real thing. Get those wrong and even a strong model returns confident noise.

**Core principle: a reviewer is an instrument you can bias or starve without noticing.** Tell it what you expect — or even where to look — and it confirms your priors. Don't make it look at the artifact and it reviews your *description* of the artifact. Pick reviewers that share a brain and their agreement means nothing. This skill is the discipline that prevents all three.

## When to use

- You want a genuine critique, not reassurance, on anything that "works but might be wrong/bloated/fragile."
- A high-stakes or hard-to-reverse decision deserves an independent perspective.
- A previous review felt thin, agreeable, or suspiciously aligned with what you already believed.

**When NOT to use:** trivial or throwaway artifacts; when you need help *producing* rather than *critiquing*; when a 30-second self-check settles it.

## The two failure modes (the heart of the skill)

### 1. Leading the witness — biased framing

Anything in the prompt that signals **what you expect** or **where to look** gets echoed back. Poison includes:
- a **changelog / history** ("here's what changed", "after N rounds of fixes")
- a **list of suspected problems** or "I think X is the issue"
- **pointing at a region — *or* assigning a sub-area to "focus on / go deepest on".** Even a neutral-sounding "go deep on the auth module" partitions the artifact and caps what the reviewer hunts for. Coverage is not a reason to pinpoint (see Principle 3 for the real fix).
- **enumerating the artifact's parts.** A feature/module list in the prompt reads as an *exhaustive set* — the model treats it as the whole and stops thinking past it. **Point at the artifact; do not list it.**
- **calibrating the outcome** ("should be clean", "few findings expected")
- asking for a **pass/fail verdict** instead of findings

A reviewer steered this way parrots your framing and finds what you primed it to find — or nothing, if you primed "nothing." **Cure:** a *self-sufficient* question with **no history, no suspicions, no part-list, no expected findings**. Scope by **what to evaluate**, never by **what to conclude** or **where to look**. Point at the whole artifact ("here is X — understand it from the source") and let the reviewer build its own model and choose its own targets. The test of a clean prompt: a reviewer that independently surfaces a concern you never named is strong evidence it's real; one that only echoes your framing told you nothing.

### 2. The armchair review — no real examination

A reviewer that reasons from your prompt instead of inspecting the actual artifact returns plausible, generic, ungrounded findings — often in one step with zero citations. **Cure:** require it to examine the real thing **down to detail before judging**, trace real behavior (run it where possible), and cite **specific locations** (file:line, page/section, timestamp, cell). Make examination the bulk of the work and say so. **Reject any review whose findings aren't anchored to specific evidence** — it didn't look.

## Principles for a high-signal review

1. **Describe, don't lead — and don't pinpoint.** Self-contained question; no history, no suspicions, no verdict request; no part-list; no "focus on X". Point at the whole; let the reviewer find its own targets.
2. **Force examination; demand located evidence.** "Dig down to the deepest details before concluding; cite exact locations; expect many steps." Unanchored findings = armchair review.
3. **Triangulate across model *families*, not reviewer *count*.** Independence comes from **different models**, not from **more of the same one**. Five reviewers of one model share its blind spots — their agreement is *correlated*, not corroborating, and it burns budget for false confidence. A small cross-family set (e.g. one of each model you can reach) beats a pile of one. **Convergence between *different-family* reviewers = strong signal; divergence = investigate.** For a large artifact, run several *whole-artifact* reviewers across models — never carve it into per-reviewer focus-areas (carving is pinpointing, Failure Mode 1).
4. **Steelman both directions.** For each finding: state the strongest case *for the current form*, then attack it. For each proposed change: the strongest case *for keeping things*, then attack. Honesty both ways prevents rubber-stamping **and** "fix everything" vandalism.
5. **You judge, not the reviewer — and distrust your own green light.** Decide from the **raw findings**; **verify the load-bearing ones yourself**, including the apparent false positives. A reviewer's "looks good / converged" is an input, not the answer. **And the inverse: when a finding contradicts your own "it works / it passes" signal, suspect your *signal* first.** A green you didn't actually read — an exit code masked by a pipe, a stale cache, a test importing the wrong copy — is a *false green*; the reviewer that read the real output is usually right. Re-derive the signal before dismissing the finding.
6. **Use fresh context for big-picture findings.** Whoever (or whatever) built the artifact defends its own additions (fix-fatigue). A reviewer with no stake and no memory of the construction sees structure the builder can't.
7. **Counter the ratchet.** Any iterate-until-no-complaints loop only ever *adds* — a reviewer that "fails if it finds nothing" must invent something to add. Periodically spawn a reviewer whose **only** job is to cut, unify, or simplify, or the artifact grows monotonically. (See the related `unvibe-review` skill.)
8. **Tune the lenses to the task — a lens is a general CATEGORY of flaw, pitched between two opposite errors.** A review runs through a checklist of *what kinds of problem to hunt* — the lenses. The whole skill is getting the **abstraction level** right, and it fails in BOTH directions:
   - **Too LOW — an area/feature/file/module** ("the pool ledger", "sensor triage", "the KB pipeline", "the daemon lifecycle"), or a **method of finding** ("by running the e2e", "trace the startup path"). This is pinpointing in disguise (Failure Mode 1): it re-partitions the artifact, caps coverage to that slice, and tells the reviewer *where* to look. → answers "WHERE" — wrong.
   - **Too SPECIFIC — a named hypothesis** ("a privilege gate that a sibling path bypasses", "a desync between store A and store B"). This primes ONE finding and walks the reviewer to it — leading the witness. → answers "WHAT you'll find" — wrong.
   - **RIGHT — a general flaw/analysis category**, adapted to the task but un-prescriptive: e.g. "internal inconsistencies & bugs", "inter-part contract mismatch", "design misalignment", "dead/unreachable/duplicated fragments", "weak spots / optimization", "**security audit** (privilege/role bypass, secret handling, injection)", "leftover wiring to removed concepts". → answers "what KIND of flaw to hunt, everywhere" — and lets the reviewer discover which specific instances exist, and where. **This is the level of the default six below — treat them as a template to ADAPT to the task, not a fixed rule, and stay at their altitude.**
   - **A lens often needs a PREREQUISITE — state it.** "Design misalignment" is meaningless unless the reviewer knows *where the design lives*: naming a **high-level path** (a directory like `_designs/`, an artifact location — NEVER a module/feature/file to "focus on") is required context, not pinpointing. Same for "the spec is at \<path\>", "the prior art is in \<dir\>". Withholding the path doesn't make the review more neutral — it makes the lens unusable.
   - The list is **not fixed**: match it to the goal. Drop premature lenses (e.g. spec/design-conformance early in a build, before the design is even settled) and add ones the task demands. A stale lens set finds stale things. Useful task-shaped lenses beyond the defaults (inconsistencies, contract mismatches, weak spots, dead/duplicated/under-specified):
   - **Unintended leftovers** — orphaned, half-removed, or stranded fragments (code, config, tests, docs, wiring) that no longer connect to anything; two implementations where one was meant to replace the other.
   - **Cause-based precedence** — for anything assembled from multiple sources: where two parts overlap or conflict, *which should stand and which is now dead weight?* Resolve by the sources' intent, not by chance (see the merge review type).

## Pick the review type deliberately — and state which (incl. the lens set)

| Type | Question it answers | Caveat to put in the prompt |
|---|---|---|
| **Defect** | What is wrong / weak / risky *as it stands*? | whole-artifact, adversarial, no region focus, no verdict |
| **Forward / reframe** | If we adopted *this change/hypothesis*, what holds and breaks? | "this is not a defect review; evaluate adopting the idea below" |
| **Parsimony / cut** | What can be removed, merged, or reframed away? | "find what to delete; the loop has only ever added" |
| **Consolidation / merge** | Where parts from different sources overlap or conflict, which stands and what's a leftover? | point the reviewer at each source's **cause/intent record** (why each part exists) to judge precedence — but **exclude your own prior conclusions** (the plan, earlier findings) so it re-derives instead of parroting |

Blurring these produces mush. The lens checklist is part of the prompt — set it per type (Principle 8).

## Prompt template (adapt the lenses per type)

```
Be an adversarial, fully-neutral reviewer. Re-derive the artifact from scratch,
build your OWN model, verify every claim against it, trust no self-description
(or comment), and ATTACK it. A review that surfaces only minor nits has FAILED.

THE ARTIFACT: at [WHERE]. Dig into it down to the deepest details until you
understand it end to end — examine the real thing (run it / read it / trace it)
and build your understanding from the source, not from this prompt.
(Do NOT enumerate its parts here — a list reads as a complete set and caps the
reviewer's thinking. Do NOT tell it which part to focus on.)

AUDIT THROUGH THESE LENSES: [the tuned checklist for this task — each a KIND OF
FLAW swept over the WHOLE artifact, NEVER an area/feature/file/method (Principle 8) — e.g.
inconsistencies/bugs · inter-part contract mismatch · weak spots/optimization ·
dead/unreachable/under-specified/duplicated · unintended leftovers · which of two
overlapping parts should stand].

OUTPUT: findings only — no verdict, no "looks good." Per finding: SEVERITY ·
precise location · PROBLEM (what + why) · concrete FIX. Rank by severity.
An unanchored claim is not a finding. Your message is read directly — make it complete.
```

Notes: scale to stakes (a sanity check = one reviewer; an architectural/irreversible call = a cross-family pair + a cut pass + your own verification). Prefer **model-family diversity over reviewer count**. Use an **exclusion** ("don't raise X — known and accepted because Y") *only* for genuinely settled constraints, never to suppress an inconvenient truth — and only after it's been raised independently enough that you're sure it's settled.

## Red flags — your review is compromised

- You pasted a changelog, wrote "I think the problem is…", or "should be clean" → **you're leading.**
- You assigned each reviewer a sub-area to "go deep on," or listed the artifact's parts in the prompt → **you pinpointed / capped the scope.** Point at the whole.
- A "lens" answers "WHERE to look" (names an area/feature/file/subsystem, or a method like "by running X") → **region in disguise; too low.** Or it answers "WHAT you'll find" (a named flaw hypothesis like "a sibling path bypasses the gate") → **leading the witness; too specific.** A lens names a general flaw CATEGORY hunted everywhere (Principle 8) — pitch it between the two.
- You withheld the path to the design/spec/prior-art because "paths are pinpointing" → **a high-level path (a directory, an artifact location) is a PREREQUISITE, not pinpointing** (only a module/feature to "focus on" is). Without it, lenses like "design misalignment" are unusable.
- Your prompt says "read commit <sha> (it does X), read files A and B, run C" → **that's triple pinpointing** (where to look + what you think it does + the method). Let the reviewer find the commits, files, and checks itself.
- All your reviewers are the **same model** → correlated blind spots; that's not triangulation, it's an echo.
- A finding **contradicts your "tests pass / it works"** and you trust the green → **re-check the green**; it may be masked or stale.
- The findings have no locations, or arrived in one step → **armchair review.**
- The reviewer's findings match your prompt's emphasis exactly → **it parroted you.**
- You're acting on a "verdict" without re-checking the load-bearing claim → **stop and verify.**
- Round after round only adds; nothing gets cut → **spawn a parsimony reviewer.**
- Same lens list every task → **you're hunting last task's problems.**

## Common mistakes

- **Enumerating or summarizing the artifact instead of pointing at it.** A list reads as exhaustive; a summary carries your blind spots. Point; let it read the source.
- **Confusing many same-model reviewers with independence.** Independence is cross-family, not count.
- **Trusting a green signal you didn't actually read.** Masked exit codes, stale caches, and wrong-copy imports manufacture false greens.
- **A fixed lens list regardless of phase.** Match the lenses to the goal.
- **Treating agreement as confirmation.** Agreement you induced (by leading) or that's correlated (same model) confirms nothing.
- **Acting on the conclusion, not the evidence.** Verify the few load-bearing findings yourself — both directions.

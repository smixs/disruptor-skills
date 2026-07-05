# PLAN.md template — the single document every worker reads first

Copy to the project root as PLAN.md. Version the header on every pivot (v2, v3…) and
state WHAT changed and what it invalidates — workers re-read on mandate.

```markdown
# <Project> — MVP plan (v1, <date>)

## Wish
One paragraph: what a successful MVP demonstrably does, for whom, testable how.

## Audiences & personas
Per audience (2–4): personas with name, context, job-to-be-done, fears.

## User stories
Per persona, outcome-shaped stories (US-1…). Each story lists:
- Features it needs
- Integrations/contracts (the seams where independently built parts must agree)
- UX required
(Non-software: artifacts / handoff agreements / experience of the whole.)

## Golden case cards  ← the alignment anchor; write BEFORE any fan-out
3–5 concrete end-to-end scenarios, named actors, exact expected outcomes.
Every producer AND consumer task aligns to these cards (never to each other);
they double as the demo script and the acceptance evals.
When the spec came from the `write-spec` stage it already contains these cards —
copy them, don't reinvent.
- Card A "<name>": inputs … → expected outcome …
- Card B "<name>": the contradiction/edge case … → expected …

## MVP boundary — deliberate cuts
What is OUT, explicitly, with the honest stand-in for each cut (visibly labeled).

## Honesty invariants (non-negotiable, repeated in every worker mandate)
e.g.: unknown → typed gap, never a guess · machine output attributed + hedged until a
human confirms · stand-ins/synthetic data visibly labeled · nothing outward-facing
without a human click. Adapt to the domain; do not delete the section.

## Board map
Nodes by kind: contract/* (first, highest tier) → platform/* → feature/* (per story) →
integration/* (per wave + final one-boot completeness). Tier annotations per
references/tiering.md.

## Method — worker discipline
Convergence bar, gate command, workspace/git rules, seam-doc convention, preview boot
command. (Lift from references/worker-protocol.md, specialized to this project.)

## Demo script
The golden cards as presenter beats. Grows as features land; ends as the report's core.

## What's-next (post-MVP)
Deepenings per story + the ranked debt log (all recorded review-deferrals).
```

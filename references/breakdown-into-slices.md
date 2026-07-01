---
name: breakdown-into-slices
description: >-
  Use to turn a build-ready spec + a settled module architecture into an ordered
  list of independently-buildable VERTICAL SLICES (tracer bullets) — each cutting
  end-to-end through every layer (schema → API → UI → tests), demoable on its own,
  with explicit dependencies — so each slice is one small, focused build-loop run
  in its own fresh session. Reach for it whenever you're about to start building
  from a spec that is more than a single slice, or you catch yourself planning by
  horizontal layer ("first all the schema, then all the API"). Triggers: "break
  this into issues/tasks", "what do we build first", "slice this spec", "plan the
  build order".
---

# Breakdown into slices

## Stage contract
- **Stage:** 4. Breakdown · **Kind:** method
- **Inputs:** the canonical spec (stage 2) + the module boundaries (stage 3).
- **Outputs:** an ordered list of **vertical slices**, each with acceptance criteria,
  scope boundaries, and `Blocked by:` links — one slice = one build-loop run.
- **Entry gate:** the spec is build-ready **and** it is bigger than one slice. A
  single-slice job skips this stage — build it directly.
- **Done when:** every slice is end-to-end (touches all layers it needs),
  demoable/verifiable alone, and its dependencies are stated. No horizontal-only
  ("schema-only", "API-only") items remain.
- **Next:** `converge-and-polish.md` — run the build loop **once per slice**, each
  in its own fresh session seeded from the spec + that one slice.
- **Maintains:** —

## Why vertical, not horizontal

A **tracer bullet** is a thin slice that cuts through *all* the layers it touches —
schema, backend, adapter, UI, tests — and delivers one small end-to-end behavior
that you can actually run and see. It is the opposite of a **horizontal layer**
("build the whole DB schema", then "build the whole API"), which produces nothing
demoable until the last layer lands and hides integration risk until the end.

**Why it matters for an agent build:** each vertical slice is small enough to build,
review, and converge in **one focused session** without the context filling up. The
integration seams — the places things actually break — get exercised on slice #1,
not discovered at the end. And each slice merges independently.

## What makes a good slice

- **End-to-end.** It reaches every layer its behavior needs. If a slice can't be
  demoed or verified without a *future* slice, it isn't a slice yet — it's a layer.
- **Demoable / verifiable alone.** There's a concrete way to see it work: a request
  that returns the right thing, a screen that renders, a test that passes.
- **Small.** Sized to one build-loop run. If it won't converge in one session, split it.
- **Scoped.** State what it explicitly does NOT cover (goes to a later slice), so the
  builder doesn't gold-plate.
- **Behavioral, not procedural.** Describe *what* the slice must do (interfaces,
  contracts, acceptance criteria) — not *how* to code it, and not by pointing at file
  paths/line numbers that will have drifted by the time it's built.

## Ordering

- **Dependency-first.** A slice that another needs comes earlier; record it as
  `Blocked by: <slice>`. The first slice should be the thinnest complete path through
  the system (the "walking skeleton") — it proves the seams end to end.
- **Value-and-risk next.** After the skeleton, order by what de-risks or delivers most.
- **One slice per build session.** Each `converge-and-polish` run starts fresh, seeded
  with the spec + exactly one slice — not the whole conversation. Keeping the
  design→spec→breakdown work *unbroken in one context window*, then handing each slice
  to a clean session, is the context hygiene that keeps every build sharp.

## Slice template

```markdown
### Slice <n>: <short behavioral title>
- **Delivers:** <the one end-to-end behavior, in user/behavior terms>
- **Layers touched:** <schema · API · adapter · UI · tests — only what it needs>
- **Acceptance criteria:** <concrete, testable, independently verifiable>
- **Out of scope:** <what a later slice covers — do not build here>
- **Blocked by:** <earlier slice(s), or "none">
```

## Smells — you sliced it wrong if…

- A slice is named after a layer (`schema.md`, "the API work") → horizontal; re-slice
  by behavior.
- A slice can't be demoed until a later slice lands → it's a layer, not a tracer bullet.
- Slice #1 doesn't touch the UI or the outermost adapter → the walking skeleton doesn't
  actually walk; the integration seams stay unproven.
- The list has no `Blocked by:` anywhere on a multi-slice build → dependencies are hidden
  and the build order is guesswork.
- A single slice clearly won't converge in one session → split it before building.

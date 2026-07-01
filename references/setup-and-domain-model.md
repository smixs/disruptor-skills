---
name: setup-and-domain-model
description: >-
  Use once per repository before the flow begins — and then continuously — to
  stand up the two durable artifacts every later stage reads and writes: a
  CONTEXT.md glossary (the project's canonical vocabulary) and docs/adr/
  (architecture decision records). Reach for it when starting the flow in a repo
  that has no CONTEXT.md / conventions yet, when a term keeps getting used two
  ways, or when a hard-to-reverse decision was just made and needs recording.
  Triggers: "set up the repo", "what's our vocabulary", "record this decision",
  "write an ADR", "the glossary".
---

# Setup and domain model

## Stage contract
- **Stage:** 0. Setup (once per repo) + cross-cutting upkeep · **Kind:** method
- **Inputs:** the repo; whatever domain terms and decisions surface as the flow runs.
- **Outputs:** `CONTEXT.md` (glossary) and `docs/adr/` (decision records), created
  lazily and kept live.
- **Entry gate:** first time through the flow in this repo (no CONTEXT.md /
  conventions recorded), or a term/decision needs pinning down mid-flow.
- **Done when:** conventions are recorded; every term the flow relies on has one
  canonical definition; every hard-to-reverse decision is an ADR.
- **Next:** the stage you were routed to — usually `7w3-driven-development.md`.
- **Maintains:** it *owns* CONTEXT.md and docs/adr/; every other stage keeps them live.

## Why this exists

The whole flow rests on the invariant **the document is the source of truth** — design,
spec, and decisions are the record; code realizes them. That invariant needs a concrete
home, or it stays a slogan. These two artifacts are that home:

- **CONTEXT.md** keeps the vocabulary from drifting. When "user", "account", and
  "member" mean the same thing in three files, the design has already started to rot.
  One canonical term per concept keeps every later stage — spec, breakdown, reviews —
  talking about the same things.
- **docs/adr/** keeps the *why* of hard-to-reverse choices from evaporating. A decision
  that isn't recorded gets silently re-litigated or quietly reversed by an agent that
  never saw the trade-off.

Create both **lazily** — only when the first term or the first real decision appears.
An empty CONTEXT.md on day one is ceremony; a stale one is worse than none.

## Once-per-repo setup

Do this the first time the flow touches a repo. Keep it to what the flow actually needs:

1. **Decide where the artifacts live.**
   - Single domain: `CONTEXT.md` + `docs/adr/` at the repo root.
   - Multiple bounded contexts: a root `CONTEXT-MAP.md` pointing to
     `src/<context>/CONTEXT.md` + per-context `docs/adr/`.
2. **Record the conventions the flow assumes** (a short block in `CLAUDE.md` /
   `AGENTS.md`, or a `docs/agents/` note): where CONTEXT.md and ADRs live, and any
   project-specific rule the base invariants don't already cover.
3. **Don't scaffold empty files.** Note the locations; create the files when the first
   term/decision actually lands (see below).

## CONTEXT.md — the glossary

One entry per project-specific concept. Not a dictionary of general programming terms —
only the words that mean something particular *here*.

```markdown
## <Canonical term>
<What it IS, in 1–2 sentences — "is", not "does". State the thing, not its behavior.>
_Avoid:_ <synonyms/near-terms that must not be used for this concept>
```

Rules:
- **Is, not does.** Define what the term *is*, not what it does.
- **One opinionated choice.** Pick the canonical word; list the synonyms to avoid so they
  don't creep back.
- **Project-specific only.** If it's a general programming concept, it doesn't belong.
- **Sharpen on contact.** When a stage uses a fuzzy word, or a term two ways, resolve it
  here immediately — a concrete edge-case scenario is the fastest way to force precision.
- **Grow it lazily.** Add a term the moment it's resolved; don't pre-populate.

## docs/adr/ — decision records

Number sequentially: `0001-slug.md`, `0002-slug.md`.

```markdown
# <NNNN>. <Decision title>
<The decision and the WHY, in 1–3 sentences.>
<!-- optional, only if they carry weight: Status · Considered options · Consequences -->
```

**Offer an ADR sparingly** — only when a decision is **hard-to-reverse AND surprising AND
the result of a real trade-off**. Qualifies: architectural shape, integration pattern,
technology lock-in, a boundary decision, a deliberate deviation, a rejected alternative
with subtle reasoning. Does *not* qualify: routine choices, anything obvious, anything a
reader would guess. An ADR for every decision is noise that buries the few that matter.

## Keeping them live (every stage's job)

- **7w3 design** and **spec** cite CONTEXT.md terms and propose ADRs as decisions land.
- Any stage that discovers a term drifting fixes it in CONTEXT.md **then**, not later.
- When reality diverges from an ADR, update the ADR — don't let the code quietly redefine
  the decision. Same rule as the design of record: the document leads, code follows.

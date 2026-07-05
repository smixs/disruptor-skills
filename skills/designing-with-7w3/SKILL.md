---
name: designing-with-7w3
description: >-
  Use when designing a feature, system, refactor, process, protocol, or
  decision before implementing it; when expanding a vague spec, RFC, or ticket
  into an implementable design; when writing or reorganizing design docs; when
  the user mentions "7w3", the seven Ws, "wishes / functions / decision
  flows", or wants a design "like BDD or user-story-driven development but
  fuller"; or when the user says "design X" or "write this up properly" —
  prefer this over ad-hoc design notes or a phase/Gantt plan.
---

# 7w3 Driven Development

## Stage contract
- **Stage:** 1. Design · **Kind:** method
- **Inputs:** an idea / RFC / ticket / feature request (from a router on-ramp).
- **Outputs:** a 7w3 subject tree — each subject's ten facets, grounded in real things.
- **Entry gate:** you're moving from "what we want" to "how it works"; the repo's
  conventions/CONTEXT.md exist (else invoke the `setting-up-domain-model` skill first).
- **Done when:** every leaf subject answers all ten facets (or an explicit `n/a — because…`),
  Where/Who/When cite real files/names/events, no unacknowledged holes remain.
- **Next:** the `write-spec` skill — turn the settled design into a canonical spec.
- **Maintains:** CONTEXT.md (cite/sharpen terms) · ADRs (record hard-to-reverse design decisions).

7w3 is a way to design *anything* by describing each **subject** completely along
**ten facets**, and keeping all ten together in one place. It is similar in spirit to
user-story-driven development and BDD — but where a user story captures only the *wish*
and BDD captures only the *when/how* of a scenario, 7w3 insists you capture the whole
subject: who owns it, where it lives, when it fires, why it exists, what it is *not*,
what it can't do, and what happens next — all at once, so the subject can be reasoned
about, reviewed, and implemented as a single coherent unit.

The name: **7 Ws + 3** = ten facets.

## When to use this

Use 7w3 the moment you move from "what do we want" to "how will this actually work":
designing a feature or subsystem, an API, a protocol, a refactor, a migration, an org
process, a decision record. Use it to turn a vague spec/RFC/ticket into something
implementable. Use it instead of jumping straight to a phased to-do list — phases flatten
the decision structure that 7w3 preserves.

It is **general-purpose**: nothing about it is tied to code. A hiring process, a kitchen
remodel, and a rate limiter can all be 7w3 subjects.

## The ten facets

### The Seven Ws

| facet | the question it answers | a good answer | the hole it exposes when empty |
|---|---|---|---|
| **Wish** | What outcome do we want? What is success? | a desired *end state*, not a mechanism | you're building without knowing what "done" means |
| **Why** | Why does this matter? Why this way? | motivation + reason + **causes** + **intentions** | you can't tell which constraints are real |
| **What** | What *is* this, exactly? | a precise definition of the one thing | if there are two "whats", it's two subjects |
| **Who** | Who is responsible / who acts / who's affected? | named actors + their roles | nobody owns it, or everybody does |
| **Where** | Where does it live? (file, system, place, context) | concrete locations — grounded, not "somewhere" | it can't be found or built |
| **When** | When does it fire? In what order? **What is the lifecycle?** | triggers, sequencing, timing, state transitions | races, missed triggers, undefined ordering |
| **What's-next** | What does this cause downstream? What follows? | implications, ripple effects, dependencies, next steps | surprises land on whoever ships it |

### The three others

| facet | the question it answers | a good answer | the hole it exposes when empty |
|---|---|---|---|
| **Boundaries** | What is explicitly NOT this / not theirs / out of scope? | the edges — the things deliberately excluded | scope creep; two subjects bleed together |
| **Limitations** | What can't this do? What's deferred? What are the risks? | known constraints, trade-offs, deferrals, failure modes | false confidence; hidden landmines |
| **Method** | *How?* The mechanism: functions, decision flows, the decisions made | the actual branches/steps/contracts that realize the Wish | it's a wish, not a design |

**Every facet must be answered.** An empty facet is a signal, not a formatting gap: either
the facet genuinely doesn't apply (write "n/a — because …") or you haven't finished
thinking. Don't delete a facet to hide a hole.

## The cardinal rule

> **All ten facets of one subject live TOGETHER in one file. You decompose by *subject*
> into a tree — never by facet.**

This is the rule that makes 7w3 work, and the easiest one to get wrong.

**Why together.** A subject's value is in seeing it *whole*. You cannot judge a decision
when its Who is in one file, its When in another, and its Boundaries in a third — you'd
reassemble the subject in your head every time, and the facets silently drift out of sync.
One subject, one file, ten facets means each file is a self-contained, reviewable,
implementable unit. Reviewing it is reviewing the whole subject.

**The anti-pattern (do not do this).** Splitting the design into `who.md`, `where.md`,
`boundaries.md`, `methods.md` — a file *per facet* spanning all subjects. This looks tidy
and is exactly backwards: it scatters every subject across ten files. If you ever name a
file after a facet, stop.

**Decompose by subject instead.** When a subject gets too big — its facets sprawl, it has
two distinct "Whats", its Method has many independent branches — split it into **child
subjects**, each its own 7w3 file with its own complete ten. The parent keeps a short
version of each facet and points to the children. Recurse as deep as the work needs — a
tree of 5 or 500 nodes is fine. The tree of subjects should mirror the real structure of
the thing you're designing.

## The document template

One file per subject. Name it after the subject: `<subject>.7w3.md`. Fill all ten.

```markdown
# <Subject> — 7w3

**Parent:** [<parent-subject>](parent.7w3.md) · **Children:** [<a>](a.7w3.md), [<b>](b.7w3.md)
<!-- the tree edges; omit a side that doesn't exist -->

## Wish
<the desired outcome / definition of done>

## Why
<motivation; why this shape>

### Causes
<...>

### Intentions
<...>

## What
<precise definition of the one thing this subject is>

## Who
<actors + responsibilities — who does, owns, is affected>

## Where
<concrete locations: files, systems, places, contexts — grounded>

## When
<triggers · ordering · lifecycle · state transitions>

## Method
<HOW: the mechanism — functions, contracts, decision flows (guard → action → result),
the decisions made. This is the design proper.>

## Boundaries
<what is explicitly NOT this / not in scope / not this actor's job>

## Limitations
<constraints, trade-offs, deferrals, known risks & their mitigations>

## What's-next
<downstream implications, ripple effects, dependencies, follow-on subjects>
```

Order is a recommendation, not a law — lead with Wish/Why (intent) and end with
What's-next (consequences) because it reads well. The non-negotiable part is that **all ten
are present, in the one file.**

## Decomposing into a tree

- **The tree is a NESTABLE DIRECTORY, not a flat folder of cross-referencing files.** A
  subject is a file `<subject>.7w3.md`. When it earns children (gate below), it is
  **PROMOTED into a directory** `<subject>/` holding its own framing file
  `<subject>/<subject>.7w3.md` (the parent, whose facets now *summarize* and point) plus
  its child subject files — and each child can itself promote into a directory, recursively,
  as deep as the real structure goes. Promotion-into-a-directory is the growth mechanism.
  (A small design may sit in one flat folder; that's fine — but you grow it by promoting a
  subject, not by sprinkling sibling files.)
- **THE PARSIMONY GATE — a subject earns its own file/directory ONLY when it is a genuinely
  DISTINCT subject; otherwise it stays DATA inside its parent.** Concretely, promote a
  candidate to its own child subject only if it introduces a **new actor or owner**, a **new
  responsibility / authority boundary**, a **distinct contract or interface**, a **state
  machine**, or an **independently-realizable unit** (a sub-system, a state machine, a separately
  buildable/deliverable/testable piece). If it does none of these — it's a detail, a
  variant, a field, an example, another step of the same process — it must **EXTEND the
  existing subject as DATA**: another row, bullet, field, table entry, or cross-reference —
  **never a new file.** (Cross-domain: a *character* earns a subject; that character's
  *eyebrow-raise* does not — it's a line in their scene. An *auth service* earns one; its
  37th config flag does not — it's a row in a table.)
- **Why the gate is load-bearing (the counter-force).** Without it, every nuance gets
  "promoted so it can grow freely" — which keeps each leaf *locally* clean while the tree
  grows *globally* heavier: more files, more cross-links, more places the same thing is
  half-described, more navigation cost. A child that, after promotion, only **photocopies
  its parent's framing**, or holds a detail that **could have been a field**, is a
  mis-promotion — fold it back. (This is the structural twin of the over-decompose smell:
  splitting by facet scatters one subject; over-promoting by nuance multiplies subjects.)
- **Split (promote) when** the gate is met *and* one of: a facet won't fit cleanly, the
  subject has more than one coherent "What", or its Method has independent sub-mechanisms
  each worth its own ten. The gate is the *necessary* condition; these are the *triggers*.
- **A root/parent subject** describes the whole at a high level (its facets summarize) and
  links to children. A leaf subject is small enough that its ten facets are each a few lines.
- **Link both ways** (Parent / Children) so the tree is navigable from any node.
- **Cross-reference shared vocabulary** instead of restating it: define a term, a contract,
  or a state machine **once** in the subject that owns it, and link to it from siblings.
  (This keeps child docs tight without violating ten-together — each child still answers all
  ten *for itself*, it just doesn't re-explain shared concepts. A recurring concrete thing
  that ≥3 subjects re-describe is itself a candidate to factor into one owning subject + N
  references — the same gate applied to *shared data*, not just to *promotion*.)

## How to drive a 7w3 design

1. **Name the root subject** — the one thing being designed. Resist starting with structure.
2. **Fill its ten facets.** Where you can't, you've found a hole — research it or mark it
   `n/a — because …`.
3. **Notice strain.** If a facet sprawls or you're writing two "Whats", split off a child
   subject and give it its own ten. Recurse.
4. **Ground the facts.** Where/Who/When should cite real things (files, names, events), not
   placeholders — that's what makes the design implementable rather than aspirational.
5. **Implement against the Method + When** of each leaf subject — the decision flows are the
   build instructions. 7w3 deliberately has no separate "phase plan"; if you need build
   order, express it as a dependency note inside What's-next, not as a timeline that
   re-flattens the design.
6. **Keep it live.** When reality diverges, update the subject's ten — the file is the
   design of record, not a historical snapshot.

## Relationship to BDD and user-story-driven development

- A **user story** ("As an X I want Y so that Z") is roughly 7w3's **Wish + Who + Why** — three of ten.
- A **BDD scenario** (Given/When/Then) is roughly 7w3's **When + Method** for one path.
- 7w3 keeps both and adds **Where, What, Boundaries, Limitations, What's-next**, and binds
  them to one subject. So: stories and scenarios are *inputs*; a 7w3 subject is the *whole*.

## Smells — you're doing it wrong if…

- A file is named after a **facet** (`boundaries.md`, `methods.md`) → you split by facet. Re-split by subject.
- A facet is **empty** with no "n/a — because" → an unacknowledged hole.
- **Method reads like a Wish** ("it should be fast and clean") → you described the goal, not the mechanism.
- One subject has **two unrelated Whats** → it's two subjects.
- The same concept is **re-explained** in five files → define once, cross-link.
- A **child subject introduces no new actor/owner/authority/contract/unit** — it just holds a detail, a
  variant, or photocopies its parent → it failed the parsimony gate; fold it back into the parent as a
  field/row/reference. (And: the tree only ever GREW — no subject was ever folded back or merged → the
  promote-by-nuance ratchet is running; the tree is heavier than the thing it designs.)
- The design is a **list of phases** → you flattened the decision structure 7w3 exists to keep.

## A worked example (general — emailed password reset)

A small tree: a root subject with a child. Each file has all ten; shown compressed.

**`password-reset.7w3.md`** (root)
- **Wish:** a user who forgot their password can regain access within ~5 minutes, safely.
- **Why:** account lockout is the #1 support cost; self-serve recovery removes it.
- **What:** an emailed, single-use, time-boxed reset link that lets the holder set a new password.
- **Who:** the user (requests + completes); auth service (issues/validates); email provider (delivers); support (n/a — explicitly hands-off, see Boundaries).
- **Where:** `auth/reset` endpoints; the token store (→ child `reset-token.7w3.md`); the email template service.
- **When:** user submits "forgot password" → token issued + email sent → user clicks within TTL → new-password form → token consumed. Expired/used link → restart.
- **Method:** `POST /reset/request{email}` → always 200 (don't leak existence) → if account exists, mint token (→ child) + send link. `POST /reset/complete{token,newpw}` → validate token (exists ∧ unexpired ∧ unused) → set password → consume token → invalidate sessions.
- **Boundaries:** NOT account *creation*, NOT email *change*, NOT MFA reset (separate subject). Support never resets passwords by hand.
- **Limitations:** depends on email deliverability (out of our control); a leaked inbox = account takeover (mitigated by short TTL + session invalidation); no SMS fallback yet (deferred).
- **What's-next:** invalidating sessions on reset ripples to "remember me" tokens (must also clear); rate-limiting the request endpoint becomes its own subject; metrics: reset-completion rate.

**`reset-token.7w3.md`** (child) — its own complete ten:
- **Wish:** a token that is unguessable, single-use, and self-expiring … **Method:** 256-bit random, stored hashed, `expires_at = now + 15m`, `used_at` nullable; validate = lookup-by-hash ∧ `used_at IS NULL` ∧ `expires_at > now` … **Boundaries:** not a session token, not a JWT … **Limitations:** clock-skew on `expires_at`; no rotation … *(and Why/What/Who/Where/When/What's-next)*.

The root's **Where** and **Method** point at the child; the child answers all ten *for the
token*. That's the tree: decomposed by subject, ten-together at every node.

*Source: Nambr (@aostrikov_agents_chat), 7w3 Driven Development.*

# Tiering — routing every board node to the cheapest model that can't hurt you

## The three axes

Score each node LOW/HIGH on:

1. **Blast radius** — how much downstream work consumes this node's output? A schema
   everything validates against is HIGH; a leaf plugin consuming settled conventions is LOW.
   (Deps fan-out on the board is a good proxy: `flow.py show <id>` → dependents.)
2. **Volume** — how much material must be produced? A one-page contract is LOW; a
   full subsystem is HIGH.
3. **Verifiability** — can a gate (tests, lint, schema check, checklist) catch a bad
   result cheaply? HIGH verifiability lets you drop a tier safely: importance alone does
   NOT force an expensive model if failures are caught mechanically.

## Routing table

| Radius | Volume | Verifiability | Tier |
|---|---|---|---|
| HIGH | LOW | any | **T3+** — frontier in expensive mode (e.g. extended thinking / converge mode / 2 discussion rounds with a second frontier model). Schemas, core contracts, boundary decisions, architecture calls. Cheap in absolute terms because volume is low — this is the best money you spend. |
| HIGH | HIGH | any | **T3** — frontier, standard mode. Platform substrate, seam-heavy integrations, adversarial reviewers of T3+/T3 work. |
| LOW | any | HIGH | **T2** — mid-tier (e.g. Sonnet-class, gpt-5.4-medium-class, strong open-source like GLM/Minimax-class). Leaf features on established contracts, content packs, UI views over a fixed seam. The gate is the safety net. |
| LOW | LOW | HIGH, mechanical | **T1** — small/cheap model or a script. Renames, regeneration, doc syncs. |
| LOW | any | LOW | bump to T2/T3 — unverifiable output is where cheap models silently hurt you. |

Record the tier on the node (`"tier": "T2"`); it doubles as documentation of the risk call.

## Model map (EDIT PER HARNESS — this is config, not doctrine)

```
T3+: <frontier model, max reasoning / converge mode; optionally + 1-2 critique rounds
      from a second frontier model>
T3:  <frontier model, standard>       e.g. Opus-class / gpt-5.5-high-class
T2:  <mid model>                      e.g. Sonnet-class / gpt-5.4-medium / GLM / Minimax
T1:  <cheap model or none (script)>   e.g. Haiku-class / gpt-5.4-mini-high / Qwen / Gemma
Reviewers: one tier >= the author's tier, always a FRESH context (blind to author notes).
```

In Claude Code, tiers map to the Agent tool's `model` parameter. In other harnesses, map
to whatever worker-spawn mechanism exists; if only one model is available, tiers degrade
to effort/reasoning settings and review depth.

## Budget governor

- Cap concurrent workers (parallelism budget) and total T3+/T3 spawns per wave; T2 is the
  default tier when in doubt AND the gate is real.
- **Escalation rule**: a node that fails its convergence bar twice at its tier is
  re-mandated ONE tier up with the failure history attached — never retried indefinitely
  at the same tier, never jumped straight to T3+.
- Convergence budget by node kind: contract/foundation = review panel or 2 passes;
  standard feature = 1 adversarial pass; T1/T2 leaf = self-review + gate. Reviews find
  something ~always; the bar is "no unfixed critical/major/high", not "clean".

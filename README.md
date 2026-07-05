<div align="center">

<img src="assets/banner.webp" alt="Disruptor: Claude Code skills for agentic software development — idea to ship, no vibecode" width="100%">

# 🧨 Disruptor — agentic software development with Claude Code skills, from idea to ship

**A gated pipeline of 12 Claude Code skills that turns an idea into deployed, production-grade software — design, spec, executable architecture, honest review loops, QA, safe deploy. No vibecode.**

[![version](https://img.shields.io/badge/version-2.0.0-orange)](CHANGELOG.md)
[![skills](https://img.shields.io/badge/skills-12-blue)](#the-pipeline)
[![license: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skills-8A2BE2?logo=anthropic&logoColor=white)](https://code.claude.com/docs/en/skills)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)
[![Telegram](https://img.shields.io/badge/chat-@aostrikov__agents__chat-26A5E4?logo=telegram&logoColor=white)](https://t.me/aostrikov_agents_chat)
[![GitHub stars](https://img.shields.io/github/stars/smixs/disruptor-skills?style=social)](https://github.com/smixs/disruptor-skills/stargazers)

</div>

---

## What is it

**Disruptor** is a set of 12 [Claude Code](https://claude.com/claude-code) skills for agentic software development, stitched into **one idea-to-ship pipeline**. Each stage consumes the artifact of the previous one and hands a new artifact to the next, while a **router with Yes/No gates** decides what happens next. The agent acts **by rule**, not by vibe: it doesn't improvise the process and doesn't declare "done" early.

The core premise: an agent's own feeling of "done" cannot be trusted — it is the main enemy. Every method here exists to survive a premature stop: the unread green test, the spec with a hidden default, the rubber-stamp review, the loop that only adds and never cuts. Each skill was extracted from real production runs by practitioners, not invented for a README.

## The pipeline

```
Input → [ROUTER: on-ramps + gates G0–G5]
  0 Setup ─► 1 Design ─► 2 Spec ─► 3 Guardrails ─► 4 Slices ─► 5 Build & converge ─► 6 QA ─► 7 Deploy
  (once)      7w3         spec      executable       tracer      ├ 5a reviewers
                                    architecture     bullets     └ 5b unvibe
                                          └────────► G3F: fleet lane (delivering-mvp-fleet) ─► 6 QA
```

Two kinds of skills. **Methods** trigger automatically when the situation matches (model-invoked). **Prompt templates** are `/commands` you invoke yourself (user-invoked).

| Stage | Skill | Kind | What it does |
|---|---|---|---|
| — | [`disruptor`](skills/disruptor/SKILL.md) | `/command` | The router: on-ramps + gates G0–G5, routes any input to the right stage |
| 0 | [`setting-up-domain-model`](skills/setting-up-domain-model/SKILL.md) | auto | Repo conventions, shared glossary, ADRs → `CONTEXT.md` (once per project) |
| 1 | [`designing-with-7w3`](skills/designing-with-7w3/SKILL.md) | auto | 7w3 design interview: 10 facets per subject, a design tree per subject |
| 2 | [`write-spec`](skills/write-spec/SKILL.md) | `/command` | Canonical build-ready specification, incl. golden case cards |
| 3 | [`architecture-guardrails`](skills/architecture-guardrails/SKILL.md) | `/command` | Module boundaries as **executable** rules: linter + import graph + CI |
| 4 | [`slicing-into-tracer-bullets`](skills/slicing-into-tracer-bullets/SKILL.md) | auto | Breakdown into vertical slices (tracer bullets), each independently shippable |
| 5 | [`converging-and-polishing`](skills/converging-and-polishing/SKILL.md) | auto | The engine: review loop until findings converge to near zero |
| 5a | [`spawning-reviewers`](skills/spawning-reviewers/SKILL.md) | auto | Independent cross-family reviewers — fresh context, no rubber-stamping |
| 5b | [`unvibe-review`](skills/unvibe-review/SKILL.md) | auto | The counter-force: cut, unify, rethink bloat instead of adding more |
| 4–5 | [`delivering-mvp-fleet`](skills/delivering-mvp-fleet/SKILL.md) | auto | Fleet lane: parallel subagent workers build an MVP from a board of nodes |
| 6 | [`qa-demo-stand`](skills/qa-demo-stand/SKILL.md) | `/command` | Demo-stand testing to production quality; also the bug/incident on-ramp |
| 7 | [`setup-server`](skills/setup-server/SKILL.md) | `/command` | Safe Ubuntu/Debian web server setup and deploy |

**On-ramps** besides an idea from scratch: **bug/incident** → straight to QA, fix through the engine · **"bloated / architecture drifting"** → unvibe + guardrails audit · **existing design or spec** → jump to the matching stage · **vague idea, speed to testable MVP matters most** → the fleet lane.

## Install

**With the [skills.sh](https://skills.sh) installer** (interactive, works across agents):

```bash
npx skills@latest add smixs/disruptor-skills
```

**With install.sh** (copies all 12 skills, no `.git`):

```bash
curl -fsSL https://raw.githubusercontent.com/smixs/disruptor-skills/main/install.sh | bash
# current project only:
curl -fsSL https://raw.githubusercontent.com/smixs/disruptor-skills/main/install.sh | bash -s -- --project
```

**With git clone:**

```bash
git clone --depth 1 https://github.com/smixs/disruptor-skills /tmp/disruptor-skills \
  && cp -R /tmp/disruptor-skills/skills/* ~/.claude/skills/
```

Done — Claude Code discovers skills by the presence of folders in `~/.claude/skills/` (or `./.claude/skills/` for a single project); no extra registration command.

<details>
<summary>As a plugin (optional)</summary>

The repo ships `.claude-plugin/plugin.json`, so it can also be installed through the Claude Code <code>/plugin</code> flow. For most users the installs above are enough.
</details>

## Usage

You don't drive the pipeline by hand — the **router** does. Two ways in:

1. **Just describe the task.** The model-invoked methods trigger on matching situations, and the router places you at the right stage via its gates. Example phrasings:

   > "design this properly" · "slice this into tasks" · "review loop until it converges" · "what can we cut" · "this codebase feels bloated" · "build me an MVP of X fast"

2. **Invoke a `/command` directly** when you know what you need: `/disruptor` to run the full gated flow from any input, `/write-spec`, `/architecture-guardrails`, `/qa-demo-stand`, `/setup-server`.

The router asks Yes/No gate questions (G0–G5: is setup done? is the design build-ready? is the build parallelizable?…) and refuses to skip ahead — that refusal is the point.

## FAQ

### What is vibecode?

Code that "technically works" but is bloated, fragile, and impossible to hold in your head — the default output of an agent left to trust its own sense of "done". Disruptor exists to prevent it: every stage gates on an artifact, not a feeling.

### How is this different from spec-kit, BMAD, or superpowers?

Spec-kit and BMAD own your whole process end-to-end with heavy scaffolding. Disruptor is 12 small composable skills tied by a lightweight router — you can enter at any stage, use one skill standalone, or run the full flow. Compared to obra/superpowers (a broad general-purpose library), Disruptor is one opinionated pipeline for shipping web-facing software, including a parallel worker-fleet lane.

### Can I use it with Codex or other agents?

Partially. The skills are plain Markdown: the four prompt templates (`write-spec`, `architecture-guardrails`, `qa-demo-stand`, `setup-server`) work as prompts in any capable agent. Auto-triggering and the router rely on Claude Code's skill discovery; `npx skills@latest add` can install into other agents that support the skills format.

### Do I need all 12 skills?

No. Each skill is standalone. But the router and the stage contracts assume the set is present — the full pipeline is where the compounding value is.

### Which skills trigger automatically and which are commands?

Seven methods are model-invoked (they fire when the situation matches). Five are user-invoked `/commands`: the router and the four prompt templates. See the table above.

### Where are the Russian originals?

v2 translated all prompts to English. The original Russian sources live in the git history (v1, tag `v1.0.0` / the `references/` directory) with full attribution.

## Contributing

The goal: a battle-tested discipline machine for agentic development, grown from real runs. If you have your own discipline, a fix born from a real failure, a new on-ramp or gate — **send a PR**. See [CONTRIBUTING.md](CONTRIBUTING.md); discussion happens in **[t.me/aostrikov_agents_chat](https://t.me/aostrikov_agents_chat)**.

## Credits

Assembled from the working methods of practitioners of **[@aostrikov_agents_chat](https://t.me/aostrikov_agents_chat)** (Alexey Ostrikov's chat), with per-skill attribution inside each `SKILL.md`:

- **Nambr** — the review-loop method set (`converging-and-polishing`, `spawning-reviewers`, `unvibe-review`) and the `designing-with-7w3` design methodology.
- **Pukh** — the web-delivery prompt set (`write-spec`, `architecture-guardrails`, `qa-demo-stand`, `setup-server`).
- **Serge Shima** — subagent-fleet orchestration (`delivering-mvp-fleet`, base-rules-travel-with-every-prompt invariant) and the assembly into a single gated flow.

v2 translated all prompts from Russian to English; the RU originals remain in the git history.

*Русская версия и обсуждение — в чате [t.me/aostrikov_agents_chat](https://t.me/aostrikov_agents_chat).*

## License

[MIT](LICENSE) © **@aostrikov_agents_chat**.

---

<div align="center">
<sub>idea → ship, no vibecode · <a href="https://t.me/aostrikov_agents_chat">t.me/aostrikov_agents_chat</a></sub>
</div>

# Contributing to Disruptor

The goal: an **agentic-development disruptor machine built from real practice**. No
theory — every method here was earned on live projects. Bring yours.

## What we want most

- **A new skill** — a hard-won discipline the flow is missing. Add it as
  `skills/<name>/SKILL.md` and wire it into the router pipeline.
- **An edit to an existing skill** — from a real run where it broke or fell short.
- **A new on-ramp or gate** — a class of tasks that enters the flow differently.
- **Cross-domain examples** — where a method worked outside web development.

## Rules that keep this a flow, not a pile of practices

1. **Every skill keeps its `## Stage contract`** right after the H1
   (`Stage · Kind · Inputs · Outputs · Entry gate · Done when · Next`). Without it the
   stage doesn't weave into the pipeline.
2. **Outputs of stage N = Inputs of stage N+1.** Check that the seams fit.
3. **Method vs prompt template.** A method is a discipline the agent follows itself.
   A prompt template is filled in and handed to an executor. Don't mix them.
4. **Description rules.** Model-invoked skills start with "Use when…" and list ONLY
   trigger conditions — situations, symptoms, user phrasings. Never summarize the
   workflow: if the description tells the story, the agent skips the body.
5. **Sources stay as-is.** Bringing someone else's work from the chat — keep it whole,
   with attribution to the author.
6. **KISS/YAGNI.** A new skill must earn its place. A detail is a table field, not a
   new file.

## Flow

1. Fork, branch `feat/<what>`.
2. Make the change; keep the Stage contract header intact.
3. Open a PR with one logical change. Describe the real run that motivated it.

Discussion and proposals — in the chat:
**[t.me/aostrikov_agents_chat](https://t.me/aostrikov_agents_chat)**.

# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
versioning: [SemVer](https://semver.org/). (v1 entries kept in their original Russian.)

## [2.0.0] — 2026-07-05

**Breaking**: the monolith (root `SKILL.md` + 10 references) is split into **12 composable
skills** under `skills/<name>/`, each with its own frontmatter and Stage contract.

### Added
- **`delivering-mvp-fleet`** skill: fleet orchestration over a task DAG — tiered model
  routing, golden case cards, bounded convergence for worker nodes.
- **Gate G3F** in the router: parallelizable build + fleet budget → the fleet lane,
  otherwise `converging-and-polishing` per slice.
- **Two new on-ramps**: vague idea with speed-to-MVP priority → fleet lane; external
  concept/PRD → stage 1 (`designing-with-7w3`) or straight to gate G3.
- **Golden case cards** as a required section in `write-spec`: 3–5 end-to-end scenarios
  that anchor parallel builders, the demo script, and the acceptance evals.
- **Convergence-budget policy** in `converging-and-polishing`: one principle, two bars —
  full (whole slices/artifacts) vs bounded (narrow fleet worker nodes).

### Changed
- **User/model-invoked axis**: the router and the four prompt templates are user-invoked
  (`disable-model-invocation: true`); the seven methods are model-invoked with
  trigger-only descriptions.
- **Full English translation** of the four RU prompt templates (`write-spec`,
  `architecture-guardrails`, `qa-demo-stand`, `setup-server`); originals preserved in
  git history.
- **Router diet**: swarm-orchestration and "common mistakes" sections folded into
  `delivering-mvp-fleet` and the gates; invariants keep a single canonical home.
- **`install.sh`** installs all skills; compatible with `npx skills`.

## [1.0.0] — 2026-07-01

Первый публичный релиз. Скилл пересобран из «карты практик» в **упорядоченный флоу**.

### Added
- **Упорядоченный конвейер idea→ship**: `0 setup → 1 design (7w3) → 2 spec →
  3 guardrails → 4 breakdown → 5 build&converge → 6 QA → 7 deploy`.
- **Роутер с Yes/No-гейтами** (G0–G5) и **on-ramps**: вход из бага/инцидента и из
  ревизии архитектуры, не только из greenfield-идеи.
- **Контракт стадии** (`Inputs → Outputs → Entry gate → Done when → Next`) в каждом
  из 9 референсов — стрелки конвейера держатся с обоих концов.
- **Движок ревью-цикла**: `converge-and-polish` оркеструет `spawning-reviewers`
  (независимый cross-family критик) и `unvibe-review` (контр-сила «резать блоат»).
- **Prompt-шаблоны**: каноническая спека, executable-архитектура (guardrails),
  QA-демостенд до production-качества, безопасный setup сервера.
- **Новые стадии**: `setup-and-domain-model` (CONTEXT.md + ADR) и
  `breakdown-into-slices` (tracer-bullet вертикальные срезы).
- **Инварианты оркестрации subagent-swarm** (base-rules travel with every prompt).

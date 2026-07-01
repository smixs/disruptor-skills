# Changelog

Формат — [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/),
версионирование — [SemVer](https://semver.org/lang/ru/).

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

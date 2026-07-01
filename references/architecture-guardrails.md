# Промпт архитектурных guardrails для веб-проекта

## Stage contract
- **Stage:** 3. Architecture guardrails · **Kind:** prompt
- **Inputs:** the spec (stage 2) + the chosen stack.
- **Outputs:** module/import boundaries made **executable** — enforced by linter +
  import-graph + filesystem checks in CI, not by prose an agent can ignore.
- **Entry gate:** the spec exists; you're about to stand up structure agents will erode.
- **Done when:** the boundaries are machine-checked in CI (a violation fails the build).
- **Next:** `breakdown-into-slices.md`.
- **Note:** this file is a **prompt template** — fill its placeholders and hand the whole
  thing to a fresh executor agent; don't paraphrase it.

## Назначение

Этот документ - нейтральный шаблон для будущих веб-проектов, которые разрабатываются с AI-агентом. Его задача: заранее зафиксировать архитектуру, границы модулей, правила контрактов и автоматические проверки, чтобы агент не размывал структуру проекта по мере разработки.

Архитектура ниже - один из удачных вариантов для production-grade веб-проектов: DDD-модули, vertical slices, ports/adapters, контрактные границы и executable architecture через линтеры, импорт-граф и CI checks.

## Архитектурная модель

- Проект делится на bounded contexts: крупные доменные модули с собственной ответственностью.
- Внутри каждого модуля сценарии раскладываются как vertical slices: один use case хранит свою orchestration-логику, тесты и публичный вход.
- Приложения остаются тонкими composition roots: они поднимают runtime, конфиг, зависимости и подключают модули, но не содержат бизнес-логику.
- Общая техническая платформа содержит только cross-cutting capabilities: конфиг, БД, auth primitives, HTTP baseline, очереди, storage, observability, testing.
- Между модулями нельзя импортировать внутренности напрямую. Общение идёт только через явно опубликованные контракты.
- Архитектура считается частью кода: её соблюдение проверяется линтером, импорт-графом, filesystem-проверками, тестами и CI.

## Слои

- `app layer`: composition root, bootstrap, routing/runtime registration, dependency injection.
- `module contract`: публичный язык модуля для других модулей.
- `domain`: инварианты, state transitions, value objects, domain errors, чистые политики.
- `feature/use case`: orchestration конкретного сценария, side effects через ports, тесты рядом.
- `feature public boundary`: узкий публичный вход в feature для adapters и соседних features.
- `infra`: реализации ports, repository adapters, provider adapters, persistence mapping.
- `adapters`: HTTP/API routes, workers, UI entrypoints, CLI, webhooks.
- `platform`: общие технические возможности без продуктовой бизнес-логики.

## Контракты между модулями

У каждого bounded context должен быть один публичный contract boundary.

Через contract можно экспортировать:

- DTO/read models;
- command/query input types;
- service boundary interfaces;
- domain event envelopes;
- публичные enum/value object types;
- чистые policy-функции, если они являются частью общего языка модуля.

Через contract нельзя экспортировать:

- repository implementations;
- SQL/query builders;
- HTTP handlers;
- UI components;
- worker/job implementations;
- приватные helpers конкретной feature;
- compatibility aliases без явно подтверждённой необходимости.

Правило: если другой модуль хочет использовать данные или поведение модуля, сначала согласуется contract. Нельзя «временно» импортировать внутренний файл.

## Контракты feature

Каждая feature/use case должна иметь маленький public boundary.

Через него можно раскрывать:

- factory use case/service;
- service interface;
- command/result types;
- узкие selectors/policies, если они нужны другим feature или adapter-слоям.

Нельзя импортировать соседнюю feature через её внутренние файлы. Только через её public boundary.

## Поток зависимостей

Разрешено:

- apps -> adapters/modules public boundaries/platform;
- adapters -> feature public boundaries/contract/infra/platform;
- features -> domain/contract/platform/own infra/other feature public boundary;
- domain -> domain primitives/own public language;
- platform -> platform/external packages.

Запрещено:

- module A -> module B internals;
- feature A -> feature B internals;
- domain -> adapters/features;
- features -> adapters;
- platform -> product modules/apps;
- app A -> app B;
- runtime cycles.

## Проверки архитектуры

Нужно настроить 3 слоя проверок.

1. Линтер быстрых правил.

Проверяет локальные запреты импортов: app не лезет во внутренности модулей, domain не импортирует adapters/features, feature не импортирует adapters, platform не импортирует product code.

2. Проверка импорт-графа.

Проверяет весь dependency graph: runtime cycles, cross-module access only through contracts, feature-to-feature only through public boundaries, adapters-to-feature only through public boundaries.

3. Filesystem verifier.

Проверяет форму модулей: обязательные contract/domain/features/infra/adapters зоны, public boundary у feature, тесты рядом с feature, запрет generic `helpers/utils/common/misc`, запрет локальных docs как ложного source of truth.

## Что настроить в линтере

Для TypeScript/JavaScript проекта:

- ESLint flat config;
- `typescript-eslint` recommended rules;
- `no-unused-vars`/unused imports как error;
- `no-restricted-imports` для быстрых архитектурных запретов;
- dependency graph tool, например dependency-cruiser;
- отдельный filesystem verifier script;
- тесты на сами architecture rules.

Для другого стека выбрать аналоги:

- Java/Kotlin: ArchUnit + Checkstyle/Detekt/Ktlint;
- Python: Ruff + import-linter + pytest checks;
- Go: golangci-lint + depguard + custom graph checks;
- C#: Roslyn analyzers + NetArchTest;
- Rust: cargo-deny/cargo-machete + custom crate graph checks.

## Команды качества

В проекте должны быть единые команды:

- `lint`: обычный lint + архитектурные проверки.
- `lint:architecture`: импорт-граф + filesystem verifier.
- `typecheck`: полная проверка типов всех приложений и модулей.
- `test`: unit/integration tests.
- `verify:release`: secrets/artifacts/runtime checks + lint + architecture + typecheck + tests + build.
- `db:verify`: schema/migration checks, если есть БД.

CI должен запускать те же команды. Если `lint:architecture` падает, merge/release запрещён.

## Правила работы с контрактами

- Новый cross-module сценарий начинается с согласования contract.
- Contract должен быть маленьким и стабильным.
- Если данные нужны только внутри feature, они не попадают в module contract.
- Если feature нужна adapter-слою или другой feature, она публикует узкий public boundary.
- Любое расширение contract сопровождается тестом потребителя или contract-level тестом.
- Нельзя добавлять fallback/alias/backward compatibility без конкретной причины.
- Удаление или изменение contract требует поиска всех потребителей и обновления тестов.

## Что добавить в правила агента

Скопируй этот блок в agent rules будущего проекта.

```text
- Соблюдай модульную DDD + vertical slice архитектуру: bounded contexts, domain, features, adapters, platform.
- Между модулями импортируй только через публичный contract boundary.
- Между features импортируй только через public boundary feature.
- Не импортируй внутренние файлы чужого модуля или чужой feature, даже временно.
- Domain не зависит от adapters, UI, HTTP, workers или feature orchestration.
- Platform не импортирует product modules/apps и не содержит бизнес-логику продукта.
- Apps остаются тонкими composition roots: bootstrap, config, dependency wiring, module registration.
- Не создавай generic helpers/utils/common/misc; размещай общий код в конкретном domain/feature/platform capability.
- Перед добавлением cross-module поведения сначала обнови contract и тесты потребителя.
- `lint:architecture` проверяет соответствие импортов и файловой структуры архитектуре.
- `lint` запускает обычный lint и architecture checks.
- `verify:release` запускает полный набор проверок перед merge/release.
- Не считай задачу завершённой, пока relevant lint/typecheck/tests/architecture checks не проходят.
```

## Готовый промт агенту

```text
Нужно настроить архитектурный каркас и автоматические guardrails для нового веб-проекта.

Сначала изучи согласованный стек, продуктовую спецификацию, приложения, bounded contexts, auth/tenant модель, БД, очереди, внешние интеграции и deployment target.

Настрой архитектуру как модульную DDD + vertical slices + ports/adapters:
- apps являются тонкими composition roots;
- modules являются bounded contexts;
- каждый module имеет public contract boundary;
- каждый use case живёт как feature/vertical slice;
- каждая feature имеет public boundary и тесты;
- infra содержит реализации ports/adapters;
- platform содержит только общие технические capabilities.

Настрой автоматические проверки:
- обычный lint;
- архитектурные запреты импортов;
- dependency graph check без runtime cycles;
- filesystem verifier формы модулей/features;
- typecheck;
- tests;
- release verification command;
- DB schema/migration verification, если есть БД.

Зафиксируй правила:
- module-to-module только через contract;
- feature-to-feature только через public boundary;
- adapters-to-feature только через public boundary;
- domain не импортирует adapters/features;
- features не импортируют adapters;
- platform не импортирует apps/modules;
- apps не содержат бизнес-логику.

Добавь tests для architecture guardrails, чтобы правила нельзя было удалить или ослабить молча.

Добавь краткий architecture doc с описанием слоёв, контрактов, запретов импортов, команд проверки и definition of done.

В финале запусти relevant checks и перечисли результат каждой команды.
```

## Definition of done

- Архитектурные слои определены и описаны.
- Контракты между модулями зафиксированы.
- Линтер запрещает очевидные нарушения слоёв.
- Импорт-граф запрещает обход contract/public boundaries.
- Filesystem verifier проверяет форму модулей и features.
- Guardrails покрыты тестами.
- CI запускает lint, architecture checks, typecheck и tests.
- Правила агента добавлены в проектные инструкции.

---
name: architecture-guardrails
description: A prompt template that turns module boundaries into executable architecture — linter, import-graph, and filesystem checks enforced in CI.
disable-model-invocation: true
---

# Architecture guardrails prompt for a web project

## Stage contract
- **Stage:** 3. Architecture guardrails · **Kind:** prompt
- **Inputs:** the spec (stage 2) + the chosen stack.
- **Outputs:** module/import boundaries made **executable** — enforced by linter +
  import-graph + filesystem checks in CI, not by prose an agent can ignore.
- **Entry gate:** the spec exists; you're about to stand up structure agents will erode.
- **Done when:** the boundaries are machine-checked in CI (a violation fails the build).
- **Next:** the `slicing-into-tracer-bullets` skill.
- **Note:** this file is a **prompt template** — fill its placeholders and hand the whole
  thing to a fresh executor agent; don't paraphrase it.

## Purpose

This document is a neutral template for future web projects developed with an AI agent. Its job: fix the architecture, module boundaries, contract rules, and automatic checks up front, so the agent does not erode the project's structure as development proceeds.

The architecture below is one proven option for production-grade web projects: DDD modules, vertical slices, ports/adapters, contract boundaries, and executable architecture via linters, an import graph, and CI checks.

## Architectural model

- The project is divided into bounded contexts: large domain modules, each with its own responsibility.
- Inside each module, scenarios are laid out as vertical slices: one use case holds its orchestration logic, tests, and public entry point.
- Applications stay thin composition roots: they bring up the runtime, config, and dependencies and wire in the modules, but contain no business logic.
- The shared technical platform contains only cross-cutting capabilities: config, database, auth primitives, HTTP baseline, queues, storage, observability, testing.
- Modules must not import each other's internals directly. Communication goes only through explicitly published contracts.
- Architecture counts as part of the code: compliance is verified by a linter, an import graph, filesystem checks, tests, and CI.

## Layers

- `app layer`: composition root, bootstrap, routing/runtime registration, dependency injection.
- `module contract`: the module's public language for other modules.
- `domain`: invariants, state transitions, value objects, domain errors, pure policies.
- `feature/use case`: orchestration of a specific scenario, side effects through ports, tests alongside.
- `feature public boundary`: a narrow public entry into the feature for adapters and neighboring features.
- `infra`: port implementations, repository adapters, provider adapters, persistence mapping.
- `adapters`: HTTP/API routes, workers, UI entrypoints, CLI, webhooks.
- `platform`: shared technical capabilities with no product business logic.

## Contracts between modules

Every bounded context must have exactly one public contract boundary.

Allowed exports through the contract:

- DTO/read models;
- command/query input types;
- service boundary interfaces;
- domain event envelopes;
- public enum/value object types;
- pure policy functions, if they are part of the module's shared language.

Forbidden exports through the contract:

- repository implementations;
- SQL/query builders;
- HTTP handlers;
- UI components;
- worker/job implementations;
- private helpers of a specific feature;
- compatibility aliases without an explicitly confirmed need.

Rule: if another module wants to use a module's data or behavior, the contract is agreed first. You may not import an internal file "temporarily".

## Feature contracts

Every feature/use case must have a small public boundary.

It may expose:

- a use case/service factory;
- a service interface;
- command/result types;
- narrow selectors/policies, if other features or adapter layers need them.

You may not import a neighboring feature through its internal files. Only through its public boundary.

## Dependency flow

Allowed:

- apps -> adapters/modules public boundaries/platform;
- adapters -> feature public boundaries/contract/infra/platform;
- features -> domain/contract/platform/own infra/other feature public boundary;
- domain -> domain primitives/own public language;
- platform -> platform/external packages.

Forbidden:

- module A -> module B internals;
- feature A -> feature B internals;
- domain -> adapters/features;
- features -> adapters;
- platform -> product modules/apps;
- app A -> app B;
- runtime cycles.

## Architecture checks

Set up 3 layers of checks.

1. A fast-rules linter.

Checks local import bans: app does not reach into module internals, domain does not import adapters/features, a feature does not import adapters, platform does not import product code.

2. An import-graph check.

Checks the whole dependency graph: runtime cycles, cross-module access only through contracts, feature-to-feature only through public boundaries, adapters-to-feature only through public boundaries.

3. A filesystem verifier.

Checks module shape: mandatory contract/domain/features/infra/adapters zones, a public boundary in every feature, tests next to the feature, a ban on generic `helpers/utils/common/misc`, a ban on local docs as a false source of truth.

## What to configure in the linter

For a TypeScript/JavaScript project:

- ESLint flat config;
- `typescript-eslint` recommended rules;
- `no-unused-vars`/unused imports as error;
- `no-restricted-imports` for fast architectural bans;
- a dependency graph tool, e.g. dependency-cruiser;
- a separate filesystem verifier script;
- tests on the architecture rules themselves.

For another stack pick the equivalents:

- Java/Kotlin: ArchUnit + Checkstyle/Detekt/Ktlint;
- Python: Ruff + import-linter + pytest checks;
- Go: golangci-lint + depguard + custom graph checks;
- C#: Roslyn analyzers + NetArchTest;
- Rust: cargo-deny/cargo-machete + custom crate graph checks.

## Quality commands

The project must have unified commands:

- `lint`: regular lint + architecture checks.
- `lint:architecture`: import graph + filesystem verifier.
- `typecheck`: full type checking of all applications and modules.
- `test`: unit/integration tests.
- `verify:release`: secrets/artifacts/runtime checks + lint + architecture + typecheck + tests + build.
- `db:verify`: schema/migration checks, if there is a database.

CI must run the same commands. If `lint:architecture` fails, merge/release is forbidden.

## Rules for working with contracts

- A new cross-module scenario starts with agreeing the contract.
- A contract must be small and stable.
- If data is needed only inside a feature, it does not go into the module contract.
- If a feature is needed by the adapter layer or another feature, it publishes a narrow public boundary.
- Any contract extension is accompanied by a consumer test or a contract-level test.
- No fallback/alias/backward compatibility may be added without a concrete reason.
- Removing or changing a contract requires finding all consumers and updating the tests.

## What to add to the agent rules

Copy this block into the agent rules of the future project.

```text
- Follow the modular DDD + vertical slice architecture: bounded contexts, domain, features, adapters, platform.
- Between modules, import only through the public contract boundary.
- Between features, import only through the feature's public boundary.
- Do not import internal files of another module or another feature, even temporarily.
- Domain does not depend on adapters, UI, HTTP, workers, or feature orchestration.
- Platform does not import product modules/apps and contains no product business logic.
- Apps stay thin composition roots: bootstrap, config, dependency wiring, module registration.
- Do not create generic helpers/utils/common/misc; place shared code in a concrete domain/feature/platform capability.
- Before adding cross-module behavior, first update the contract and the consumer tests.
- `lint:architecture` checks that imports and file structure match the architecture.
- `lint` runs the regular lint plus architecture checks.
- `verify:release` runs the full set of checks before merge/release.
- Do not consider a task done until the relevant lint/typecheck/tests/architecture checks pass.
```

## Ready-to-use agent prompt

```text
Set up the architectural skeleton and automatic guardrails for a new web project.

First study the agreed stack, the product specification, the applications, bounded contexts, auth/tenant model, database, queues, external integrations, and the deployment target.

Set up the architecture as modular DDD + vertical slices + ports/adapters:
- apps are thin composition roots;
- modules are bounded contexts;
- every module has a public contract boundary;
- every use case lives as a feature/vertical slice;
- every feature has a public boundary and tests;
- infra contains ports/adapters implementations;
- platform contains only shared technical capabilities.

Set up automatic checks:
- regular lint;
- architectural import bans;
- a dependency graph check with no runtime cycles;
- a filesystem verifier of module/feature shape;
- typecheck;
- tests;
- a release verification command;
- DB schema/migration verification, if there is a database.

Fix the rules:
- module-to-module only through the contract;
- feature-to-feature only through the public boundary;
- adapters-to-feature only through the public boundary;
- domain does not import adapters/features;
- features do not import adapters;
- platform does not import apps/modules;
- apps contain no business logic.

Add tests for the architecture guardrails so the rules cannot be removed or weakened silently.

Add a short architecture doc describing the layers, contracts, import bans, verification commands, and definition of done.

At the end, run the relevant checks and list the result of every command.
```

## Definition of done

- The architectural layers are defined and documented.
- The contracts between modules are fixed.
- The linter forbids obvious layer violations.
- The import graph forbids bypassing contract/public boundaries.
- The filesystem verifier checks the shape of modules and features.
- The guardrails are covered by tests.
- CI runs lint, architecture checks, typecheck, and tests.
- The agent rules are added to the project instructions.

*Source: Pukh (@aostrikov_agents_chat), Architecture guardrails prompt for a web project. Translated from Russian.*

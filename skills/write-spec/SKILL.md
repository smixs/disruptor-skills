---
name: write-spec
description: A prompt template that turns a settled 7w3 design into a canonical, build-ready implementation specification covering data, API, security, testing, and deployment.
disable-model-invocation: true
---

# Write spec

## Stage contract
- **Stage:** 2. Spec · **Kind:** prompt
- **Inputs:** the 7w3 design (stage 1) + known stack/constraints.
- **Outputs:** a canonical, build-ready specification — every behavior stated; anything
  unspecified must not be silently invented at build time.
- **Entry gate:** the design is settled (7w3's done-gate met).
- **Done when:** DB, backend, UI, integrations, tests, and security can all be built from
  it without verbal clarification.
- **Next:** the `architecture-guardrails` skill.
- **Maintains:** uses CONTEXT.md vocabulary; surface new decisions as ADRs.
- **Note:** this file is a **prompt template** — everything below the line is the prompt.
  Fill its `<placeholders>` with the design's facts and hand the whole thing to a fresh
  executor agent; don't paraphrase it.

---

You act as the product's chief architect, systems analyst, and technical lead. Your task is to prepare not an overview and not a marketing description, but a canonical implementation specification from which the team and AI agents can build the product without constant verbal clarifications.

Write the specification in the language the user works in (`<language>` placeholder, default: the language of the input design), in plain understandable language, but with sufficient technical precision. If you use a technical term, explain it immediately in simple words. Do not write generic phrases like "security needs to be thought through". Instead, pin down concrete rules, tables, states, constraints, checks, and readiness criteria.

## Input Data

Product: `<product name>`

Short description: `<what the product does and for whom>`

Target audience: `<who the users, customers, administrators, external participants are>`

Specification language: `<language; default: the language of the input design>`

Current implementation stage: `<e.g.: Phase 1 / MVP / first production release / pilot>`

What is definitely in scope for the current stage:

- `<item>`
- `<item>`
- `<item>`

What is definitely out of scope for the current stage:

- `<item>`
- `<item>`
- `<item>`

Future stages that need architectural groundwork, but no implementation now:

- `<stage or direction>`
- `<stage or direction>`

Preferred technology stack, if already chosen:

- Frontend: `<stack or "propose one">`
- Backend: `<stack or "propose one">`
- Database: `<stack or "propose one">`
- Queues and background jobs: `<stack or "propose one">`
- Files: `<stack or "propose one">`
- Observability: `<stack or "propose one">`
- AI/LLM: `<stack or "propose one">`

Business, legal, security, or operational constraints:

- `<constraint>`
- `<constraint>`

Important integrations:

- `<integration>`
- `<integration>`

Expected product surfaces:

- `<e.g.: admin panel>`
- `<e.g.: customer account area>`
- `<e.g.: public widget>`
- `<e.g.: mobile app>`

## Main Goal

Create a specification of such a level that, from it, one can:

- design the database;
- build the server side;
- build the user interfaces;
- write the integrations;
- write the tests;
- verify security;
- deploy the product;
- delegate tasks to AI agents without loss of context.

The document must be strict: if a behavior is not described, the implementation must not silently invent it.

## Mandatory Principles Of The Document

- First fix the product's boundaries: what is in scope now, what is out of scope now, what is left for the future.
- Separate user scenarios, business entities, technical channels, notifications, analytics, and external integrations.
- For every important operation, state the acting party, the launch conditions, the successful outcome, and the side effects.
- For entities with statuses, describe the finite state machine: from where to where transitions are allowed, who may perform them, which invariants must not be violated.
- For data, state what is the source of truth, what is a derived read model, what is stored immutably, and what may be changed.
- For access rights, use the "deny by default" rule.
- Do not invent hidden default values for mandatory data and settings. If a value is needed for correct operation, the system must explicitly require it and fail with a clear error when it is missing.
- AI must be an advisor, not an invisible owner of business state: all AI results pass schema validation, a confidence threshold, and deterministic rules.
- All external side effects must be explicit: events, background jobs, action log, retries, duplicate suppression.
- Errors must have a stable code, a human-readable message, and a next-step hint where useful.
- Architectural rules must be verifiable by automation wherever possible.

## Required Specification Structure

Produce a document with the following sections.

### 1. Product Scope

Describe:

- the product's purpose;
- the current implementation stage;
- what is in scope for the stage;
- what is out of scope;
- which future stages are accounted for only as extension points;
- a rule forbidding turning the current stage into a throwaway prototype if the product must live long.

Add a `Scope Rules` subsection with hard rules for changing the boundaries.

### Golden case cards

3–5 concrete end-to-end scenarios with named actors, real inputs, and exact expected
outcomes. They anchor parallel builders (align to the cards, not to each other), become
the demo script, and become the acceptance evals. Write them before any breakdown.

### 2. Glossary

Make a table of terms.

For each term, state:

- name;
- a simple definition;
- important notes;
- what this term is not, if there is a risk of confusing it with another.

After the table, add `Glossary Rules`: a list of prohibitions against mixing similar concepts.

### 3. Universal Core And Product Templates

If the product may be used across different industries, roles, countries, customer types, or business models, describe:

- what is the universal core;
- what is defined by settings or templates;
- which differences must not spawn separate parallel implementations;
- which starter templates are needed now;
- which next template or scenario must be possible without rewriting the core.

If universality is not needed, explicitly explain why and which boundaries must still not be mixed.

### 4. Use-Case Catalog

Compose a catalog of key scenarios.

Break it down by product areas.

Each row must contain:

- `ID`;
- scenario name;
- primary acting party;
- preconditions;
- successful outcome;
- main side effects.

Be sure to cover:

- sign-in and user management;
- the product's main working scenarios;
- creation, modification, and closing of key business objects;
- external integrations;
- background jobs;
- notifications;
- analytics;
- customer or administrator settings;
- public surfaces, if any.

Add `Use-Case Rules`:

- every command, handler, screen, background job, and AI scenario must reference one or more use case IDs;
- hidden side effects are forbidden;
- if a new feature does not map onto the catalog, the specification is updated first.

### 5. Canonical State Machines

For each entity with statuses, describe a table:

- `From`;
- `To`;
- `Trigger`;
- `Allowed actors`;
- `Notes`.

After each table, add invariants:

- which states are terminal;
- which transitions are forbidden;
- which transitions require a reason;
- what is written to the history;
- which direct status changes are forbidden.

At minimum, cover:

- the product's main working entity;
- assignment or task ownership, if present;
- the user session;
- import or a bulk operation, if present;
- a notification or delivery, if present;
- content publication, if present.

### 6. Canonical Event Catalog

Describe events as facts that have already happened, not as commands.

First fix the rules:

- where events are created;
- how redelivery is ensured;
- how consumers must be resilient to reprocessing;
- how events are versioned;
- why events do not replace the primary database, unless this is event sourcing.

Describe the event envelope:

- event id;
- name;
- version;
- time;
- tenant/client/account id, if the product is multi-tenant;
- aggregate type;
- aggregate id;
- actor;
- correlation id;
- causation id;
- payload.

Make event tables by product area:

- event;
- who publishes;
- when it is published;
- mandatory fields;
- typical consumers.

### 7. Data Model Level 2

Describe the logical data model at the level of tables or collections.

For each table, state:

- name;
- purpose;
- mandatory fields;
- key constraints.

Be sure to describe:

- identifiers;
- dates and times;
- soft archiving or deletion;
- immutable records;
- action history;
- relationships between entities;
- rules for JSON/flexible fields;
- rules for personal and sensitive data.

If there is multi-tenancy, state:

- where `tenant/account/org id` is stored;
- how data cross-contamination is forbidden;
- which tables may be global;
- how unique keys are built.

### 8. API Contract Baseline

Describe the chosen API style.

State:

- the base prefix;
- the data format;
- the source of truth for schemas;
- how documentation is generated;
- where business logic must not live.

Make a catalog of endpoints in tables:

- method;
- path;
- who has access;
- linked use case IDs;
- whether protection against request re-submission is needed;
- notes.

Add a unified error format:

```json
{
  "error": {
    "code": "STABLE_ERROR_CODE",
    "message": "A human-readable explanation of what went wrong.",
    "hint": "What to do next, if applicable.",
    "requestId": "...",
    "details": {}
  }
}
```

Describe the rules:

- when an idempotency key against re-submission is mandatory;
- how pagination works;
- how filters are specified;
- how breaking changes are handled;
- how external webhooks/callbacks are verified;
- why DTOs must not leak straight from the database without an explicit schema.

### 9. Canonical Architecture

Describe the architectural baseline:

- repository type;
- modularity style;
- application boundaries;
- where business logic lives;
- where integrations live;
- where background jobs live;
- where the user interface lives;
- where the shared technical platform lives.

Make a list of the chosen technologies and a list of explicitly forbidden baseline solutions, if they create a risk of complexity or hidden logic.

### 10. Source-Of-Truth Rules

Describe what is the primary source of truth for:

- product rules;
- business logic;
- API schemas;
- the database schema;
- migrations;
- runtime settings;
- event routing;
- user interfaces.

Separately list where critical business logic is forbidden to live: for example, only in AI prompts, only in SQL read models, only in the interface, only in CI scripts, or in an external process builder.

### 11. Repo Layout

Propose a repository structure.

Describe:

- applications;
- modules by business area;
- the contracts layer;
- the domain layer;
- functional vertical slices;
- infrastructure adapters;
- tests;
- platform capabilities;
- documentation;
- architecture-checking tools.

After the folder tree, add rules:

- which imports are allowed;
- which imports are forbidden;
- where tests must live;
- where a module's public boundary must be;
- which folders are forbidden, so that shapeless `utils/common/helpers` do not appear;
- which architectural rules must be checked automatically.

### 12. AI-Agent Delivery Rules

Describe the rules so that AI agents can safely evolve the codebase:

- read the specification and local contracts before changing anything;
- always determine the bounded context and use case;
- tests before logic for behavior changes;
- the minimal correct change;
- no hidden default values for mandatory data;
- clear errors;
- file size limits;
- comments on non-obvious logic blocks;
- external side effects only via explicit adapters, events, or background jobs;
- automatic architecture checking as a mandatory barrier.

### 13. Bounded Contexts

Make a table of business areas:

- context;
- what it owns;
- what it does not own.

Important: explicitly separate similar areas that are easy to mix. For example: communications and notifications, user and session, payment and invoice, order and message, file and attachment, event and command.

### 14. Canonical Domain Model

Make a table of aggregates and key entities:

- entity;
- purpose;
- invariants.

After the table, add modeling rules:

- which entities are not equal to each other;
- which relationships are allowed;
- where history is needed;
- where physical deletion is forbidden;
- which AI results are not state until validated;
- which analytical data is derived.

### 15. Multitenancy Or Ownership Model

If the product is multi-tenant, describe the tenant isolation model.

If the product is not multi-tenant, describe the model of data ownership by users, organizations, teams, or projects.

State:

- how the data owner is determined;
- which data is global;
- how access is checked;
- how keys are built;
- how background jobs preserve the owner context;
- how files and analytics preserve access boundaries.

### 16. Data Rules And Import Rules

Describe the general data rules:

- identifier format;
- time and time zones;
- archiving;
- change history;
- personal data;
- JSON fields;
- foreign keys;
- table naming rules.

If there is import, bulk update, or synchronization, describe:

- the two-step process `preview/validation` -> `execute`;
- per-row errors;
- explicit confirmation of dangerous changes;
- prohibition of implicit deletions;
- the merge policy;
- error codes;
- the preview response contract.

### 17. Auth, Sessions And CSRF

Describe:

- who is the source of authorization;
- login types;
- sessions;
- lifetimes;
- rotation/revocation;
- protection of browser requests;
- throttling/rate limit;
- access recovery;
- why the user interface is not a security boundary.

### 18. RBAC Matrix

Make a role matrix:

- role;
- scope;
- main rights.

Then make a permissions table:

- permission code;
- meaning;
- allowed roles;
- scope restrictions.

Rules:

- deny-by-default;
- all permissions are checked on the server;
- privileged actions are logged;
- if a permission is not in the specification, it is forbidden.

### 19. Channel And Integration Model

If the product receives data from external channels or sends data outward, describe:

- the channels;
- the authorization model of each channel;
- how a channel is linked to a client/user/organization;
- what counts as a trustworthy identity;
- how attachments are handled;
- how retries are handled;
- how the original external data is stored;
- which actions a channel has no right to perform directly.

For each channel, make a contract:

- direction;
- binding;
- identity source;
- dialog or operation identifier;
- message or event identifier;
- attachments;
- replies;
- delivery confirmations;
- fault tolerance;
- special rules.

### 20. Frontend Runtime And UI Flow Specs

Describe all user surfaces.

For each surface, make a table of flows:

- `Flow ID`;
- screen or entry point;
- primary acting party;
- happy path;
- mandatory states for error, empty result, loading, access denied, and conflict.

Add interface rules:

- the interface does not compute permissions as a source of truth;
- stale state is not silently overwritten;
- dangerous actions require confirmation;
- errors must be understandable to the user;
- important statuses, history, and decision reasons must be visible.

### 21. Main Business Lifecycle

Describe the lifecycle of the product's main business entity in plain language and with a table.

State:

- internal statuses;
- user-facing statuses, if they differ;
- who may change the status;
- what happens to the history;
- how reopening, cancellation, rejection, duplicates, and archiving work;
- which actions require a reason.

### 22. Assignment, Routing, SLA Or Workload Rules

If the product has work assignment, routing, queues, deadlines, or workload, describe:

- how the performer or queue is chosen;
- which data is used;
- what is forbidden to choose;
- how deadlines are calculated;
- what pauses a deadline;
- what counts as a violation;
- how races and concurrent changes are handled;
- which changes must be visible in the history.

### 23. Dedupe, Merge And Conflict Rules

If duplicates or data merging are possible, describe:

- duplicate criteria;
- what AI may propose;
- what a rule or a human must confirm;
- which merges are forbidden;
- how the link to the original objects is stored;
- how an erroneous decision is rolled back;
- which conflicts block the operation.

### 24. AI Operating Model

Describe all AI scenarios.

For each, state:

- the use case;
- input data;
- the output schema;
- the confidence threshold;
- what the system does at low confidence;
- which fields AI has no right to change;
- which checks run after the response;
- how requests are logged;
- how quality evaluations are set up;
- what counts as an unacceptable response.

Rules:

- AI does not extend access rights;
- AI does not bypass consents, deadlines, settings, and policies;
- AI does not create mandatory data out of thin air;
- an AI response does not become business state without validation.

### 25. Files And Media

If the product works with files, describe:

- where the bytes are stored;
- where the metadata is stored;
- how links to business objects are created;
- how access is checked;
- how scanning is performed;
- how temporary links are issued;
- what is logged;
- which file types are allowed;
- what happens when a file is blocked.

### 26. Notifications And Campaigns

If the product sends notifications, describe:

- how a notification differs from an ordinary message or comment;
- notification types;
- the audience;
- consents and preferences;
- channel selection;
- quiet hours;
- duplicate suppression;
- retries;
- reasons for final failure;
- the two-step process for mass sends: preview -> publish/schedule;
- the preview contract;
- suppression codes.

### 27. Analytics And Read Models

Describe analytics as a separate layer, not as heavy queries straight against the working tables.

State:

- data sources;
- read models or marts;
- refresh frequency;
- metrics;
- formulas;
- what the user sees when data is stale;
- which widgets may fail independently;
- how drill-down transitions are built;
- which exports are allowed.

### 28. Observability

Describe the mandatory log fields:

- request id;
- trace id;
- owner/tenant/account id;
- actor id;
- module;
- use case;
- entity type;
- entity id;
- provider, if applicable.

List what must be logged.

Describe the baseline alert signals:

- error spikes;
- queue lag;
- external provider failure;
- AI errors;
- file errors;
- database problems;
- notification delivery problems.

### 29. Security, Privacy And Compliance

Describe:

- encryption;
- secrets;
- least privilege;
- audit;
- personal data;
- backups;
- legal or industry requirements;
- prohibition of secrets in the repository;
- prohibition of tokens in logs;
- support access;
- confirmation of destructive actions;
- data retention periods.

### 30. Runtime, Staging And Deploy

Describe:

- the service composition;
- environments;
- reverse proxy or entry point;
- build;
- registry;
- migrations;
- deploy order;
- readiness/liveness/startup checks;
- smoke checks;
- rollback;
- prohibition of manual hotfixes inside running containers or servers, if this matters for the project.

### 31. Environment And Config Contract

Describe the setting classes:

- database;
- cache;
- files;
- authorization;
- integrations;
- AI;
- observability;
- public interface settings.

For each class, state:

- examples;
- what happens when it is missing;
- whether the service may start in a degraded mode;
- where schema validation happens.

The main rule: a mandatory setting does not get an invented default value.

### 32. Backup And Disaster Recovery

Describe:

- what is backed up;
- the schedule;
- how restoration is verified;
- the restoration order;
- what counts as an incomplete restoration;
- how often restoration drills are conducted.

### 33. Testing Strategy

Describe risk-based testing: test critical risks first, not cosmetics.

Produce:

- a list of test types;
- a list of critical end-to-end scenarios;
- a minimal coverage matrix by module;
- a matrix of mandatory tests by change type;
- a release gate matrix.

Be sure to include:

- domain rule tests;
- integration tests of the database and background jobs;
- API contract tests;
- access rights tests;
- migration tests;
- redelivery tests for background handlers;
- an AI eval suite, if there is AI;
- regression tests for non-trivial fixes.

### 34. Non-Functional Requirements

Describe:

- availability;
- p95 read latency;
- p95 write latency;
- background job latency;
- limits on heavy operations;
- scaling;
- degradation when external providers fail.

Do not use abstract promises. Give numeric targets or explicitly state that they need to be confirmed by a load test.

### 35. Feature Delivery Gates

Describe the `Definition of Ready`:

- there is an area owner;
- there is a use case;
- the acting party, trigger, happy path, and errors are described;
- inputs and outputs are described;
- data changes are described;
- permissions and audit are described;
- tests and acceptance criteria are described.

Describe the `Definition of Done`:

- tests pass;
- type and quality checks pass;
- observability is added;
- the specification is updated when boundaries change;
- no hidden fallbacks;
- errors are understandable;
- permissions and data boundaries are verified;
- rollout and rollback are understood.

### 36. Canonical Implementation Decisions

A list of decisions that are no longer open questions.

For each decision, state:

- what was chosen;
- what was rejected;
- why;
- what consequence it has for the implementation.

### 37. Deferred Alignment Items

A list of questions that may be postponed but must not be forgotten.

For each, state:

- what is not yet decided;
- when it must be decided;
- which boundaries are already fixed;
- what is forbidden to do until it is decided.

### 38. Final Rule

Close the document with the rule:

If a quick implementation violates this specification, the implementation must be fixed, not the specification watered down for convenience.

## Quality Check Before Answering

Before producing the final specification, check yourself against the checklist:

- There are explicit boundaries of the current stage and future stages.
- There is a glossary of terms and prohibitions against mixing similar concepts.
- There is a use-case catalog with IDs.
- There are finite state machines for entities with statuses.
- There are events and reprocessing rules.
- There is a data model with mandatory fields and constraints.
- There is an API catalog and a unified error format.
- There are access rights and the deny-by-default rule.
- There are AI rules, if AI is used.
- There are integration and channel rules, if any.
- There are UI flows with error and empty states.
- There is analytics as a separate layer, if analytics is needed.
- There is observability, security, data retention, deploy, backups, and recovery.
- There is a testing strategy and readiness criteria.
- There are no hidden default values for mandatory data.
- There are no placeholder phrases without a concrete decision.

If the input data is insufficient for a precise decision, do not invent critical details. Make two blocks:

1. `Assumptions` — explicitly marked working assumptions.
2. `Open Questions` — questions without which a final architectural decision cannot be made.

But even with open questions, prepare the fullest possible draft specification, explicitly separating firm decisions from assumptions.

*Source: Pukh (@aostrikov_agents_chat), specification prompt template. Translated from Russian.*

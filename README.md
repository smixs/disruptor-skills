<div align="center">

<img src="assets/banner.webp" alt="Disruptor: Claude Code скилл для агентной разработки, idea → ship, no vibecode" width="100%">

# 🧨 Disruptor

**Дисциплина сборки production-софта с AI-агентами: от идеи до работающего сервера, без vibecode.**
Девять методов, собранных в один флоу для [Claude Code](https://claude.com/claude-code).

[![version](https://img.shields.io/badge/version-1.0.0-orange)](CHANGELOG.md)
[![license: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-8A2BE2?logo=anthropic&logoColor=white)](https://code.claude.com/docs/en/skills)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)
[![Telegram](https://img.shields.io/badge/чат-@aostrikov__agents__chat-26A5E4?logo=telegram&logoColor=white)](https://t.me/aostrikov_agents_chat)
[![GitHub stars](https://img.shields.io/github/stars/smixs/disruptor?style=social)](https://github.com/smixs/disruptor/stargazers)

</div>

---

## Что это

**Disruptor**: **Claude Code Skill** из девяти выстраданных на реальных проектах методов,
сшитых в **один конвейер**. Каждая стадия принимает артефакт предыдущей и отдаёт следующей, а
**роутер с Yes/No-гейтами** решает, что делать дальше. Так агент действует **по правилу**:
не импровизирует и не выдумывает «готово» раньше времени.

> **Ключевой принцип:** агенту нельзя доверять собственному ощущению «готово», это главный враг. Каждый метод существует,
> чтобы пережить преждевременную остановку: непрочитанный зелёный тест, спеку со скрытым
> дефолтом, ревью-штамповку, цикл, который только добавляет и никогда не режет.

**Для кого:** те, кто собирает софт агентами (Claude Code / Codex) и устал от vibecode: кода, который «технически работает», но раздут, хрупок и не держится в голове.

## Флоу: idea → ship

```
Вход → [РОУТЕР: on-ramp + гейты G0–G5]
  0 Setup ─► 1 Design ─► 2 Spec ─► 3 Guardrails ─► 4 Breakdown ─► 5 Build&converge ─► 6 QA ─► 7 Deploy
  (once)      7w3         spec       arch           срезы           ├ 5a reviewers
                                                                    └ 5b unvibe
```

| # | Стадия | Что делает | Артефакт |
|---|--------|-----------|----------|
| 0 | **Setup** | конвенции репо, глоссарий, ADR | `CONTEXT.md` + `docs/adr/` |
| 1 | **Design** | 7w3, 10 граней на субъект, дерево по субъектам | дизайн-дерево |
| 2 | **Spec** | каноническая build-ready спека | спека |
| 3 | **Guardrails** | границы модулей как **executable** (линтер + import-graph + CI) | архитектура |
| 4 | **Breakdown** | нарезка на **вертикальные срезы** (tracer bullets) | список срезов |
| 5 | **Build & converge** | движок: ревью-цикл до сходимости | сошедшийся артефакт |
| 5a | ↳ **Reviewers** | независимый **cross-family** критик, без поддавков | найденные дефекты |
| 5b | ↳ **Unvibe** | контр-сила: резать, унифицировать, переосмыслять блоат | сокращения |
| 6 | **QA** | демостенд до production-качества | воспроизведённые + чинёные баги |
| 7 | **Deploy** | безопасный setup Ubuntu/Debian-сервера | развёрнутый сервер |

**On-ramps** (входы, кроме идеи с нуля): **баг/инцидент** → сразу QA → фикс через движок ·
**«раздуто / архитектура плывёт»** → unvibe + аудит guardrails · **уже есть дизайн/спека** →
прыжок на нужную стадию.

## Быстрая установка

**Персонально (во всех проектах)**, самый простой путь, клонируем прямо в каталог скиллов:

```bash
git clone https://github.com/smixs/disruptor ~/.claude/skills/disruptor
```

**Через установщик** (кладёт только `SKILL.md` + `references/`, без `.git`):

```bash
curl -fsSL https://raw.githubusercontent.com/smixs/disruptor/main/install.sh | bash
# только для текущего репо:
curl -fsSL https://raw.githubusercontent.com/smixs/disruptor/main/install.sh | bash -s -- --project
```

**Только для одного проекта:**

```bash
git clone https://github.com/smixs/disruptor .claude/skills/disruptor
```

Готово: Claude Code подхватывает скилл автоматически (правки `SKILL.md` применяются даже
без перезапуска сессии). Отдельной команды для установки нет, скиллы обнаруживаются по
факту наличия папки в `~/.claude/skills/`.

<details>
<summary>Как плагин (опционально)</summary>

Репозиторий содержит `.claude-plugin/plugin.json`, так что скилл можно подключить и как плагин
через <code>/plugin</code>-флоу Claude Code. Для большинства достаточно установки выше.
</details>

## Как пользоваться

Просто опиши задачу: агент сам зайдёт в нужную стадию по роутеру. Триггеры:

> «design this properly» · «write the spec» · «architecture guardrails» · «slice this into tasks» ·
> «review loop until it converges» · «harden this» · «what can we cut» · «test it like production» ·
> «set up the server»

Или укажи прямо: *«прогони по disruptor»*.

## Приглашаем допиливать 🛠️

Цель: собрать **ультрамашину-дизраптор агентной разработки на реальной практике**. Это живой
проект, каждый метод здесь выстрадан на живых прогонах. Если у тебя есть своя
дисциплина, правка из реального фейла, новый on-ramp или гейт, **присылай PR**.

Как контрибьютить: смотри [CONTRIBUTING.md](CONTRIBUTING.md). Обсуждение, заявки и споры идут
в чате **[t.me/aostrikov_agents_chat](https://t.me/aostrikov_agents_chat)**.

## Кредсы

Собрано из наработок практиков чата **[@aostrikov_agents_chat](https://t.me/aostrikov_agents_chat)**
(чат Алексея Острикова). Каждый источник лежит внутри `references/` **as is**, целиком, с
атрибуцией автору:

- **Nambr**: набор методов ревью-цикла (`converge-and-polish`, `spawning-reviewers`,
  `unvibe-review`) и методология дизайна `7w3-driven-development`.
- **Пух (Pukh)**: набор промптов web-доставки (`specification-prompt-template`,
  `architecture-guardrails`, `demo-stand-testing`, `safe-web-server-setup`).
- **Serge Shima**: инварианты оркестрации subagent-swarm (base-rules travel with every prompt)
  и сборка методов в единый gated-флоу.

## Лицензия

[MIT](LICENSE) © **@aostrikov_agents_chat**.

---

<div align="center">
<sub>idea → ship, no vibecode · <a href="https://t.me/aostrikov_agents_chat">t.me/aostrikov_agents_chat</a></sub>
</div>

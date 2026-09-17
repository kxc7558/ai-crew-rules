# AI Crew Rules

**Discipline for AI coding crews.** One install puts three things into a project: a layered structure the AI has to respect, a gate that makes it search open source before writing anything new, and a shared task ledger so two AI tools never overwrite each other's work.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-blueviolet)](https://claude.com/claude-code)
[![Cursor](https://img.shields.io/badge/Cursor-supported-black)](.cursor/rules/ai-crew.mdc)
[![Codex](https://img.shields.io/badge/Codex-supported-black)](AGENTS.md)

---

## The problem

You run more than one AI coding tool. Maybe Claude Code for daily work, Codex for the hard problems, Cursor in the editor. Each one is capable on its own. Together they are a hazard:

| Failure | What it looks like |
| --- | --- |
| 🗂️ **Code lands wherever** | The function is correct, the layer is wrong. You fix one thing and break three. |
| 🔁 **The wheel gets reinvented** | Your AI quietly rebuilds what the open-source community already maintains — and never mentions it. |
| 🤼 **Agents overwrite each other** | Claude Code and Codex both edit `export.js` for different reasons. Last save wins. Nobody notices until it breaks. |

Asking more politely does not fix this. The rules have to live in the repository, where every tool reads them.

## What gets installed

| Piece | Lives in | What it does |
| --- | --- | --- |
| **Layered scaffold** | project root | `api/` `service/` `db/` `shared/`, each with its own README of responsibilities. Bug localization becomes a table lookup: wrong output → service, wrong data → db. |
| **Startup gate** | `UserPromptSubmit` hook | Detects "new project" / "new feature" requests and forces a real open-source search before any code is written. Fail-open: a broken hook can never block your session. |
| **Task ledger** | `data/ai-tasks/` | One Markdown file per task. Claim before you code, heartbeat on every step, two hours of silence and another AI may take over. |

## Install

### As a Claude Code plugin (recommended)

```text
/plugin marketplace add kxc7558/ai-crew-rules
/plugin install ai-crew@ai-crew
```

The hook ships with the plugin, so there is no `settings.json` to edit. Then, in any project:

> set up ai-crew rules for this project

The skill inspects the project, asks two questions, and installs what fits. Each write is explained before it happens.

### Manually, or for another tool

```bash
git clone https://github.com/kxc7558/ai-crew-rules
```

Then copy what you need:

| You want | Copy this | To here |
| --- | --- | --- |
| Layered scaffold | `skills/ai-crew/templates/layered-project/` | your project root |
| Architecture rule | `skills/ai-crew/templates/rules/layered-architecture.md` | `~/.claude/rules/common/` |
| Task ledger rule | `skills/ai-crew/templates/rules/ai-task-ledger.md` | `~/.claude/rules/common/` |

Cursor and Codex users can skip the plugin entirely — see [Works with](#works-with).

## The startup gate, in full

This is the text the hook injects when it detects a kickoff request:

> **[Project Startup Gate]** A project/feature kickoff request was detected. Before writing ANY code, complete these two steps:
>
> 1. **Open-source first (hard gate):** search the open-source community (GitHub, npm/PyPI, HuggingFace, etc.) for existing solutions. Adoption priority: use as-is > port & adapt > wrap > build from scratch. You may only write original code after a real search confirms nothing suitable exists, and you must tell the user what you searched and why nothing fit.
>
> 2. **Layered architecture evaluation:** decide whether the four-layer layout (`api -> service -> db -> shared`) is warranted. Long-lived project → use the scaffold, then `git init` and commit the scaffold as the first node. One-off script → skipping layers is fine, state the reason in one line.
>
> Finally, report both conclusions to the user in plain non-technical language.

The gate is a nudge, not a cage. It fires on kickoff keywords — edit `KEYWORDS` at the top of `hooks/project-startup-gate.py` to match how you actually phrase things.

## The task ledger

The ledger is the part that solves multi-AI collisions, and it does so without anyone agreeing on a fixed division of labor:

```markdown
---
task: switch exports to month grouping
state: in-progress
owner: claude-code
claimed_at: 2026-09-13 10:00
heartbeat: 2026-09-13 10:40
---
## Goal
What "done" means, in one or two sentences.

## Progress
- 10:00 claimed, reading the export module
- 10:40 decided: group by month at the service layer, db untouched

## Handoff notes
(left empty until done or blocked)
```

```text
open ──claim──▶ in-progress ──finish──▶ done
                   │
                   └──stuck──▶ blocked ──unblock──▶ open
```

Five rules, and only the first one is really iron:

1. **Claim before code.** No ledger entry, no edits. (Read-only review never needs to claim.)
2. **One task, one owner.** Two AIs never share an in-progress task.
3. **Heartbeat or let go.** Two hours without a heartbeat means the owner walked away and another AI may take over.
4. **Commit at every done step**, so even a collision is recoverable.
5. **Hand off through the ledger**, not through verbal summaries.

### Why a ledger and not a role table?

Role tables ("Claude Code does implementation, Codex does review") are personal. They depend on which subscriptions you pay for and how strong each model is that month, and they go stale the moment a quota changes. The ledger is impersonal and self-correcting: whoever claims a task does it, and quality gates belong in the task's own checklist rather than in someone's identity.

## How to know it's working

- The AI asks a clarifying question **before** writing code, not after breaking something.
- New features arrive with a one-line "I searched X and Y, here's why they didn't fit."
- Diffs touch the layer the task belongs to, and nothing else.
- Two AI tools working on the same repo stop producing conflicting edits.
- `git log` shows ledger updates committed alongside the code they describe.

## When not to use this

- **Throwaway scripts and one-off experiments.** The layering is overhead, not a benefit. The startup gate will tell you so and move on.
- **Projects with an existing strict architecture.** Merge the rules with your current conventions rather than replacing them — see [docs/CUSTOMIZE.md](docs/CUSTOMIZE.md).
- **Single AI tool, single short-lived project.** You probably only want the startup gate.

## Works with

| Tool | How |
| --- | --- |
| **Claude Code** | Plugin (above), or the skill at `skills/ai-crew/` |
| **Cursor** | [.cursor/rules/ai-crew.mdc](.cursor/rules/ai-crew.mdc) — a committed project rule |
| **Codex** | [AGENTS.md](AGENTS.md) — Codex reads this at the repo root |
| **Anything else** | Point it at `skills/ai-crew/templates/rules/`; the rules are plain Markdown |

## Repository layout

```text
ai-crew-rules/
├── .claude-plugin/          # Claude Code plugin + marketplace manifests
├── hooks/hooks.json         # registers the startup gate (ships with the plugin)
├── skills/ai-crew/
│   ├── SKILL.md             # the installer the AI follows
│   ├── hooks/               # the gate script
│   └── templates/
│       ├── layered-project/ # scaffold: constitution + per-layer READMEs
│       └── rules/           # layered-architecture.md, ai-task-ledger.md
├── .cursor/rules/           # Cursor adapter
├── AGENTS.md                # Codex and other agents
├── docs/                    # FAQ + customisation guide (EN / 中文)
└── tests/                   # startup gate regression suite
```

## Tests

```bash
python tests/test_startup_gate.py
```

Feeds 33 real prompts through the hook — 19 that should trigger it, 14 that should not — and fails if either group drifts. Run it after editing `KEYWORDS`.

## Docs

- [FAQ](docs/FAQ.md) ([中文](docs/FAQ.zh-CN.md)) — why four layers and not seven, coexisting with existing conventions, hook false positives
- [Customize](docs/CUSTOMIZE.md) ([中文](docs/CUSTOMIZE.zh-CN.md)) — change the keywords, remap layer names for frontend projects, adapt to other tools

## Credits

Inspired by [Anthropic's Claude Code hooks documentation](https://docs.claude.com/en/docs/claude-code/hooks), [disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery), and the OSI model — the origin of the layered idea.

## License

MIT

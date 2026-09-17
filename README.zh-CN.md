# AI Crew Rules

**给 AI 施工队立的规矩。** 装一次，往项目里放三样东西：一套 AI 必须遵守的分层结构、一道逼它先搜开源的启动关卡、一本让两个 AI 工具不会互相覆盖的任务台账。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-%E6%8F%92%E4%BB%B6-blueviolet)](https://claude.com/claude-code)
[![Cursor](https://img.shields.io/badge/Cursor-%E6%94%AF%E6%8C%81-black)](.cursor/rules/ai-crew.mdc)
[![Codex](https://img.shields.io/badge/Codex-%E6%94%AF%E6%8C%81-black)](AGENTS.md)

[English](README.md) | 简体中文

---

## 解决什么问题

你手上不止一个 AI 编程工具。可能 Claude Code 干日常，Codex 啃硬骨头，编辑器里还开着 Cursor。单独看哪个都聪明，凑在一起就是事故现场：

| 失控现场 | 具体长什么样 |
| --- | --- |
| 🗂️ **代码乱放** | 函数写得没错，放错了层。改一处崩三处。 |
| 🔁 **重复造轮子** | AI 闷头重写了社区早就在维护的东西——而且一个字都不提。 |
| 🤼 **互相覆盖** | Claude Code 和 Codex 因为不同的原因改了同一个 `export.js`。谁后保存谁赢，出事之前没人发现。 |

好声好气地多嘱咐两句没用。规矩得写进仓库里，让每个工具都读得到。

## 装了什么

| 东西 | 位置 | 作用 |
| --- | --- | --- |
| **分层骨架** | 项目根目录 | `api/` `service/` `db/` `shared/`，每层带一份职责说明。Bug 定位变成查表：结果算错 → service，数据存取错 → db。 |
| **启动关卡** | `UserPromptSubmit` 钩子 | 检测到「新建项目 / 新功能」时，强制先做一次真实的开源检索再动手。设计为 fail-open：钩子坏了也绝不会卡住你的对话。 |
| **任务台账** | `data/ai-tasks/` | 一个任务一个 Markdown 文件。动代码前先占坑，每走一步报心跳，两小时没动静其他 AI 可以接管。 |

## 安装

### 作为 Claude Code 插件（推荐）

```text
/plugin marketplace add kxc7558/ai-crew-rules
/plugin install ai-crew@ai-crew
```

钩子随插件一起装上，**不需要手动改 `settings.json`**。然后在任意项目里说：

> 给我的项目装 AI 施工队规矩

skill 会先看项目情况，问你两个问题，然后装合适的那部分。每次写入前都会先说明。

### 手动安装，或用在别的工具上

```bash
git clone https://github.com/kxc7558/ai-crew-rules
```

按需复制：

| 你要什么 | 复制这个 | 到哪里 |
| --- | --- | --- |
| 分层骨架 | `skills/ai-crew/templates/layered-project/` | 项目根目录 |
| 分层规则 | `skills/ai-crew/templates/rules/layered-architecture.md` | `~/.claude/rules/common/` |
| 台账规则 | `skills/ai-crew/templates/rules/ai-task-ledger.md` | `~/.claude/rules/common/` |

Cursor 和 Codex 用户完全不需要装插件——见下面的[适用工具](#适用工具)。

## 启动关卡全文

这是钩子检测到开工请求时注入的内容：

> **[Project Startup Gate]** A project/feature kickoff request was detected. Before writing ANY code, complete these two steps:
>
> 1. **Open-source first (hard gate):** search the open-source community (GitHub, npm/PyPI, HuggingFace, etc.) for existing solutions. Adoption priority: use as-is > port & adapt > wrap > build from scratch. You may only write original code after a real search confirms nothing suitable exists, and you must tell the user what you searched and why nothing fit.
>
> 2. **Layered architecture evaluation:** decide whether the four-layer layout (`api -> service -> db -> shared`) is warranted. Long-lived project → use the scaffold, then `git init` and commit the scaffold as the first node. One-off script → skipping layers is fine, state the reason in one line.
>
> Finally, report both conclusions to the user in plain non-technical language.

关卡是提醒，不是牢笼。它按关键词触发，改 `hooks/project-startup-gate.py` 顶部的 `KEYWORDS` 就能匹配你自己习惯的说法。

## 任务台账

台账是解决多 AI 打架的那一环，而且它不需要任何人先商量好分工：

```markdown
---
task: 把导出改成按月份分组
state: in-progress
owner: claude-code
claimed_at: 2026-09-13 10:00
heartbeat: 2026-09-13 10:40
---
## Goal
什么算「做完了」，一两句话说清。

## Progress
- 10:00 领活，在读导出模块
- 10:40 决定：在 service 层按月份分组，db 不动

## Handoff notes
（未完成或被卡住之前留空）
```

```text
open ──领活──▶ in-progress ──干完──▶ done
                   │
                   └──卡壳──▶ blocked ──解除──▶ open
```

五条规矩，真正硬的只有第一条：

1. **先占坑再动代码。** 台账里没登记就不改代码。（只读审查不用占坑。）
2. **一个任务一个主人。** 两个 AI 绝不共享一个 in-progress 任务。
3. **心跳或者让位。** 两小时没心跳，说明主人走了，别的 AI 可以接管。
4. **每完成一步就提交**，这样即使撞车也能恢复。
5. **交接走台账**，不靠口头转述。

### 为什么是台账，不是工种表？

工种表（「Claude Code 负责实现，Codex 负责审查」）是私人的：它取决于你付了哪些订阅、那个月哪个模型强，而且额度一变就作废。台账不认人，自我纠错：谁领的谁干，质量关卡写在任务自己的检查单里，而不是写在谁的身份上。

## 怎么知道它在起作用

- AI 在**写代码之前**先问澄清问题，而不是搞坏了之后才问。
- 新功能附带一句「我搜了 X 和 Y，它们不合适，原因是……」。
- diff 只动任务该动的那个层，不碰别处。
- 两个 AI 工具在同一个仓库里不再产出互相冲突的改动。
- `git log` 里能看到台账更新和它描述的代码一起提交。

## 什么时候别用

- **一次性脚本和临时实验。** 分层是开销不是收益。启动关卡会自己判断并跳过。
- **已有严格架构约束的项目。** 和你现有的规范合并，而不是替换——见 [docs/CUSTOMIZE.md](docs/CUSTOMIZE.md)。
- **只用一个 AI 工具、只做短期项目。** 那你大概只需要启动关卡那一半。

## 适用工具

| 工具 | 怎么用 |
| --- | --- |
| **Claude Code** | 上面的插件，或直接用 `skills/ai-crew/` 里的 skill |
| **Cursor** | [.cursor/rules/ai-crew.mdc](.cursor/rules/ai-crew.mdc) —— 提交进仓库的项目规则 |
| **Codex** | [AGENTS.md](AGENTS.md) —— Codex 会在仓库根目录读它 |
| **其他任何工具** | 直接指向 `skills/ai-crew/templates/rules/`，规矩就是纯 Markdown |

## 仓库结构

```text
ai-crew-rules/
├── .claude-plugin/          # Claude Code 插件与 marketplace 清单
├── hooks/hooks.json         # 注册启动关卡（随插件一起装）
├── skills/ai-crew/
│   ├── SKILL.md             # AI 照着走的安装流程
│   ├── hooks/               # 关卡脚本
│   └── templates/
│       ├── layered-project/ # 骨架：宪法 + 各层 README
│       └── rules/           # layered-architecture.md、ai-task-ledger.md
├── .cursor/rules/           # Cursor 适配
├── AGENTS.md                # Codex 及其他 agent 读它
├── docs/                    # FAQ + 定制指南（中 / EN）
└── tests/                   # 启动关卡回归测试
```

## 测试

```bash
python tests/test_startup_gate.py
```

把 33 条真实说法喂给钩子——19 条该触发、14 条不该触发——任何一边跑偏都会失败。改完 `KEYWORDS` 记得跑一次。

## 文档

- [FAQ](docs/FAQ.zh-CN.md)（[English](docs/FAQ.md)）—— 为什么是四层不是七层、怎么和现有规范共存、钩子误触发怎么办
- [定制指南](docs/CUSTOMIZE.zh-CN.md)（[English](docs/CUSTOMIZE.md)）—— 改关键词、给前端项目换分层命名、适配其他 AI 工具

## 致谢

灵感来自 [Anthropic Claude Code hooks 文档](https://docs.claude.com/en/docs/claude-code/hooks)、[disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery)，以及 OSI 七层模型——分层思想的源头。

## License

MIT

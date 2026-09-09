# AI Crew Rules 🤖🛠️

**给 AI 编程工具装上"施工队规矩"：一个 Claude Code skill，让 AI 写代码分层有序、先查开源、多 AI 不打架。**

你说一句"给我的项目装 AI 施工队规矩"，skill 自动完成：分层骨架铺设 → 项目启动关卡安装 → 多 AI 派工单配置。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/for-Claude%20Code-blueviolet)](https://claude.com/claude-code)

## 解决什么问题

用 AI 写代码最常见的三个失控现场：

| 痛点 | 没装规矩时 | 装了之后 |
|------|-----------|---------|
| 🗂️ 代码乱放 | 函数写得对但放错层，改一处崩三处 | 四层架构(api→service→db→shared)，bug 定位变查表 |
| 🔁 重复造轮子 | AI 闷头自研一个社区早已有的东西 | 启动关卡强制先搜开源，搜过才许动手 |
| 🤼 多 AI 打架 | Claude Code 和 Codex 互相覆盖代码 | 派工单分工 + A/B 角 + 接口清单交接 |

## 快速开始

```bash
# 1. 把 skills/ai-crew 复制到你的 Claude Code 技能目录
mkdir -p ~/.claude/skills
cp -r skills/ai-crew ~/.claude/skills/

# 2. 重启 Claude Code，然后对它说：
#    「给我的项目装 AI 施工队规矩」
```

skill 会引导 AI 完成三件事（每件都会先征求你确认）：

1. **分层骨架** — 把 `templates/layered-project/` 铺进项目（含各层 README 守则与接口清单）
2. **启动关卡** — 安装 UserPromptSubmit 钩子，检测到"新建项目/新功能"类消息时自动注入两步指令：先搜开源、再评估分层
3. **多 AI 派工单** — 生成 AI 分工规则文件（支持 Claude Code / Codex / 其他，按你实际的额度格局定制）

## 内容一览

```
skills/ai-crew/
├── SKILL.md                        # skill 本体：触发条件与执行流程
├── templates/
│   ├── layered-project/            # 分层项目骨架
│   │   ├── CLAUDE.md               # 项目宪法：分层地图 + bug 定位速查
│   │   └── {api,service,db,shared}/README.md  # 各层上岗守则 + 对外接口清单
│   └── rules/                      # 全局规则文件模板
│       ├── layered-architecture.md # 分层架构规则
│       └── ai-dispatch.md          # 多 AI 派工单模板
└── hooks/
    └── project-startup-gate.py     # 启动关卡钩子（关键词触发，fail-open）
```

## 核心理念

### 四层架构（借 OSI 的思想，不用它的七层）

```
api（接口层）        只接客：收请求、验参数、返结果
 └→ service（业务层） 只动脑：业务规则、流程编排
        └→ db（数据层） 只管仓：数据的存取改查
shared（公共层）      只做工具：人人可用，不依赖任何人
```

唯一铁律：**上层可调下层，下层禁调上层，跨层必经接口**。这一条就实现了"哪里报错 → 定位到层 → 只改那层"。

### 启动关卡（框架级强制，不靠 AI 自觉）

每条消息经过钩子检查，命中启动关键词时 AI 会被注入：

> 1. 先搜开源社区（GitHub / npm / PyPI / HuggingFace），下载即用 > 移植改造 > 包一层用 > 全新自研
> 2. 评估是否需要分层：要长期维护 → 用骨架；一次性脚本 → 说明原因即可

### 多 AI 派工单（按额度格局分工）

```
杂活工   MiMo/其他免费模型   简单独立单轮任务
施工队   Claude Code        日常主力（量大管饱）
主攻手   Codex/最强模型      卡壳难题 + 关键产出终审（额度稀缺花在刀刃上）
```

配套防打架三原则：同一项目同时只一个 AI 动手 / 干完一块立刻 commit / AI 交接只认接口清单。

## 适用与不适用

- ✅ 用 AI 维护多个长期项目、多套 AI 工具混用的人
- ✅ 非技术背景、靠 AI 全程实现的项目（skill 输出面向人的大白话）
- ❌ 玩具脚本、一次性实验（分层是开销不是收益）
- ❌ 已有严格架构约束的团队项目（和现有规范合并时先读 `docs/FAQ.md`）

## 文档

- [FAQ](docs/FAQ.md) — 常见问题：层数为什么是 4 不是 7、和现有项目怎么共存、钩子误触发怎么办
- [定制指南](docs/CUSTOMIZE.md) — 改关键词、换分层命名（前端 pages/store 映射）、适配其他 AI 工具

## 致谢与灵感

- [Anthropic Claude Code hooks 文档](https://docs.claude.com/en/docs/claude-code/hooks)
- [disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) — hooks 学习资料
- OSI 七层模型 — 分层思想的源头

## License

MIT

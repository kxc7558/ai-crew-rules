# 定制指南

## 改启动关键词

编辑 `hooks/project-startup-gate.py` 顶部的 `KEYWORDS` 正则：

```python
KEYWORDS = re.compile(
    r"新建项目|新项目|做项目|做个|做一个|搭一个|搭建|开发|新功能|加功能|加一个功能|"
    r"新需求|新应用|新网站|新工具|从零开始|从0开始|new project|new app|build me",
    re.IGNORECASE,
)
```

- 觉得太灵敏 → 删宽泛词（"做个""开发"）
- 觉得太迟钝 → 加你的常用说法
- 纯英文环境 → 只留 `new project|new app|build me|new feature|implement` 等

## 改注入的关卡指令

同一文件里的 `GATE` 常量就是注入给 AI 的完整指令文本，可按团队规范改写。
注意保持两条核心：①开源优先硬门槛 ②分层评估。

## 换分层目录名

前端项目常把目录映射为：

| 标准层 | 前端映射 |
|--------|---------|
| api/ | pages/ 或 views/（对外展示） |
| service/ | store/ 或 composables/（状态与逻辑） |
| db/ | api-client/ 或 services-data/（数据获取封装） |
| shared/ | utils/ 或 components/（通用件） |

方向规则不变：展示层 → 逻辑层 → 数据层，只准向下调。
改完记得同步更新各层 README 和 CLAUDE.md 里的层名。

## 适配其他 AI 工具

| 工具 | 全局规则文件 | 骨架宪法 |
|------|-------------|---------|
| Claude Code | `~/.claude/rules/common/*.md` + `~/.claude/CLAUDE.md` | 项目根 `CLAUDE.md` |
| Codex | `~/.codex/AGENTS.md` | 项目根 `AGENTS.md` |
| Cursor | `.cursor/rules/*.mdc` 或 `.cursorrules` | 同左 |
| 其他 | 该工具的自定义指令入口 | 项目根对应文件 |

宪法内容（分层地图、职责表、接口清单）和台账机制都是纯 Markdown，任何工具通用；
差异只在文件放的位置。

## 任务台账定制

`templates/rules/ai-task-ledger.md` 通常是开箱即用（它不按人定制），可调的只有两处：

1. **台账位置**：单项目 → 各仓库 `data/ai-tasks/`（随 git 走）；多项目 → 共享目录（如知识库 `ai-tasks/`），文件里注明项目名
2. **心跳时限**：默认 2 小时无更新视为离岗可接管。AI 工具响应快、协作紧密的团队可以缩到 1 小时；长任务（跑数据/训练）的建议放宽到半天，并在任务档案里注明预期时长

改完同步更新台账目录里的 `_README.md`。

## 贡献

欢迎 PR：更多语言的关键词表、更多项目类型的层名映射、其他工具的适配
说明。保持每个文件单一职责、总量精简。

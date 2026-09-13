---
name: ai-crew
description: 给项目装上 AI 施工队规矩：四层分层架构骨架、项目启动关卡（先搜开源+分层评估钩子）、多 AI 任务台账（防打架）。当用户说"装 AI 施工队规矩""给项目装规矩""ai-crew"或要求建立分层架构/开源优先/多 AI 协作制度时使用。
---

# AI Crew Rules 安装器

你要为用户的项目安装一套"AI 施工队规矩"。按以下流程执行，**每一步完成后用一句非技术语言向用户汇报**，涉及写入用户配置的操作必须先说明再执行。

## 第 0 步：了解环境

1. 确认目标项目目录（当前工作目录，或用户指定的目录）
2. 检查项目是否已有 git 仓库、已有的 CLAUDE.md / AGENTS.md / 规则文件（避免覆盖，已有内容要走合并）
3. 询问用户（一次问完）：
   - 项目是长期维护还是一次性脚本？（决定要不要分层）
   - 有没有多个 AI 工具共用项目？台账放哪（仓库内 / 共享知识库）？

## 第 1 步：铺设分层骨架

仅当项目需要长期维护时执行；一次性脚本跳过并说明原因。

1. 把 `templates/layered-project/` 下的内容复制到项目根目录：
   - `CLAUDE.md` — 项目宪法
   - `api/README.md`、`service/README.md`、`db/README.md`、`shared/README.md` — 各层守则
2. 若项目已有 CLAUDE.md，把宪法的"分层地图与调用方向"一节合并进去，不整体覆盖
3. 若项目类型使目录名不合适（如纯前端项目），参照宪法中的映射说明改名（如 pages/store），方向规则不变
4. **复制完成后立即 `git init`（若无 git）并提交首个节点**，commit message: `feat: ai-crew layered scaffold`

## 第 2 步：安装启动关卡钩子

1. 把 `hooks/project-startup-gate.py` 复制到用户全局钩子目录：
   - Claude Code：`~/.claude/hooks/project-startup-gate.py`
2. 编辑 `~/.claude/settings.json`，在 `hooks` 下合并加入（**保留已有配置，禁止覆盖整个文件**）：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python \"<用户主目录>/.claude/hooks/project-startup-gate.py\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

   - Windows 下用绝对路径的 python.exe 和脚本路径
   - 改完用 JSON 解析验证合法性，再向用户确认已安装
3. 若用户主要工具不是 Claude Code（如 Codex 为主），跳过钩子，改为在 `~/.codex/AGENTS.md`（或对应工具的全局规则文件）中写入"开源优先 + 分层评估"两条硬规则（内容见第 4 步模板）

## 第 3 步：配置规则文件

1. 把 `templates/rules/layered-architecture.md` 复制到 `~/.claude/rules/common/`（Claude Code 全局规则，目录不存在则创建）
2. 该文件末尾引用的骨架路径若与第 1 步实际路径不同，改成实际路径

## 第 4 步：配置多 AI 任务台账

1. 把 `templates/rules/ai-task-ledger.md` 复制到 `~/.claude/rules/common/`（Claude Code 全局规则，目录不存在则创建）
2. 和用户确认台账放哪（问一次）：
   - 单项目为主 → 台账就放各项目仓库内 `data/ai-tasks/`（随 git 走，交接可追溯）
   - 多项目常切换 → 共享目录（如知识库 `<vault>/ai-tasks/`），文件 frontmatter 里注明项目名
3. 建台账目录并放一个 `_README.md` 说明用法（复制 `ai-task-ledger.md` 的 Lifecycle 一节即可）
4. 若用户使用 Codex 等其他 AI 工具：把同一份 `ai-task-ledger.md` 写入其全局规则入口（如 `~/.codex/AGENTS.md`，已有内容走合并）——**台账机制对每个工具都是同一套，不按工具定制**
5. 向用户说明：防打架不靠"谁是谁的工种"，靠台账本身——领任务先占坑、心跳报平安、2 小时没动静可接管、办完写交接

## 第 5 步：收尾验证与汇报

1. 验证清单：
   - [ ] 骨架四目录 + 各层 README 存在（若适用）
   - [ ] settings.json JSON 合法且原有配置未丢失
   - [ ] 钩子脚本存在且管道测试通过：`echo '{"prompt":"开发一个新功能"}' | python <钩子路径>` 应输出含 additionalContext 的 JSON
   - [ ] 规则文件就位（分层 + 任务台账）
   - [ ] 台账目录存在且含 `_README.md`
2. git 提交所有变更（若适用）
3. 用大白话向用户汇报装了什么、每件东西干什么，并提示：**新会话开始生效；当前已打开的其他会话需重启或打开一次 /hooks 菜单**

## 注意事项

- 全程 fail-open：钩子安装失败不阻塞对话，向用户说明后继续
- 不覆盖用户已有配置，只做合并；合并前先展示 diff 要点
- 用户是非技术背景时，汇报禁止出现 JSON/钩子/路径等技术细节堆砌，用类比和结果说话

# AI Crew Rules · 发布文案

配套图文：`cards/` 目录下 9 张 1080×1440 PNG（01 是封面，按序号发布）。

---

## 小红书

**标题**

你的几个 AI 正在互相拆台

**正文**

同时用 Claude Code 和 Codex 的人，大概都遇到过这种事——

你分别让它们改功能，结果俩工具改了同一个文件。谁后保存谁赢，出事之前你根本不知道。

还有一种是：AI 把函数写对了，但放错了层。改一处崩三处，你还得先花时间搞清楚它把代码写到哪去了。

我做了个插件叫 AI Crew Rules，往项目里装三条规矩：

**一、四层架构。** api 接请求、service 管业务、db 管数据、shared 放工具。只准上层调下层，不许跳过。好处是 bug 定位变成查表——结果算错找 service，数据存取错找 db，定位到哪层就只改哪层。

**二、动手前先搜开源。** 你说"做个新功能"的时候，它先拦住 AI，逼它去 GitHub、npm 搜一遍有没有现成的，搜完还得告诉你为什么不用。

**三、先占坑再写代码。** 一个任务一个文件，领了任务才准改代码，每完成一步报个心跳。两小时没动静，别人可以接管。防打架靠这份公共记录，不靠谁比谁强。

装起来就两条命令，钩子随插件自动装好，不用改配置文件。
MIT 开源，中英双语，Cursor 和 Codex 也能用。

GitHub 搜 ai-crew-rules

**话题标签**

#AI编程 #ClaudeCode #开源项目 #程序员日常 #效率工具 #AI工具 #编程

---

## 即刻 / V2EX

**标题**

给 AI 编程工具装一套施工队规矩：分层骨架 + 开源优先关卡 + 多 AI 任务台账

**正文**

多 AI 工具混用会出三种事故：代码放到错误的层、重复造轮子、两个工具改同一个文件互相覆盖。这个插件往项目里装三样东西：

**1. 四层架构骨架**（api / service / db / shared），每层 README 登记对外接口清单。只要接口清单没变，改一层的实现不用动别处。

**2. 一个 UserPromptSubmit 钩子。** 命中"新建项目""新功能""build a new feature"这类词时，往 AI 的上下文里注入指令，强制先搜开源再动手，并汇报搜了什么、为什么不用。fail-open，脚本出错静默跳过，不会卡住会话。

**3. 多 AI 任务台账。** 一个任务一个 Markdown 文件，frontmatter 记 state / owner / claimed_at / heartbeat。占坑才准改代码，2 小时没心跳可被接管。

设计上有个取舍值得说：**没有做"工种表"**（谁负责实现、谁负责审查）。因为工种表依赖你付了哪些订阅、那个月哪个模型更强，额度一变就作废。台账不认人，谁领的谁干，AI 之间甚至不需要知道对方是谁。

安装：

```
/plugin marketplace add kxc7558/ai-crew-rules
/plugin install ai-crew@ai-crew
```

钩子随插件自动注册，不需要手改 settings.json。常驻 token 开销约 116。

MIT，中英双语。非 Claude Code 用户可以直接用仓库里的 `.cursor/rules/ai-crew.mdc` 或 `AGENTS.md`。

https://github.com/kxc7558/ai-crew-rules

---

## X / Twitter

Working with more than one AI coding tool is a hazard. Claude Code and Codex both edit export.js for different reasons — last save wins, and nobody notices until it breaks.

ai-crew-rules installs three things into a project: a four-layer architecture scaffold, a startup gate that forces an open-source search before any new code gets written, and a multi-AI task ledger so an agent claims a task before touching it.

No role tables. Those depend on which subscriptions you pay for and go stale the moment a model updates. The ledger is impersonal — whoever claims the task does it.

Two commands to install:

```
/plugin marketplace add kxc7558/ai-crew-rules
/plugin install ai-crew@ai-crew
```

MIT. Works with Claude Code, Cursor and Codex.

https://github.com/kxc7558/ai-crew-rules

---

## 发布节奏建议

| 时间 | 平台 | 内容 |
|---|---|---|
| 第 1 天 | 即刻 / V2EX | 技术向长帖，先看反馈 |
| 第 1 天 | X | 英文帖，配封面图 |
| 第 2–3 天 | 小红书 | 9 张图文，按序号发 |
| 之后 | Hacker News | 视即刻/V2EX 反馈再决定，标题要更直接 |

**回复评论时的口径**：被问到"和现成的 rules 仓库有什么不同"时，答差异在第三条（多 AI 任务台账），前两条（分层、开源优先）确实不少人有类似做法。不要贬低同类项目。

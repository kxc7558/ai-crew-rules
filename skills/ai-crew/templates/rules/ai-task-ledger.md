# Multi-AI Task Ledger

Multiple AI coding tools work on the same projects. Coordination does not
come from a fixed role table (every person's tool lineup is different) —
it comes from a **shared task ledger** that any AI can read and update.

## The Ledger

Each project keeps a task directory (default `data/ai-tasks/`).
One Markdown file per task, named `YYYY-MM-DD-short-slug.md`.
Frontmatter carries the state; the body carries the work.

```markdown
---
task: 把导出改成按月份分组
state: in-progress
owner: claude-code        # which AI holds this task
claimed_at: 2026-09-13 10:00
heartbeat: 2026-09-13 10:40   # update on every meaningful step
---
## Goal
What "done" means, in one or two sentences.

## Progress
- 10:00 claimed, reading the export module
- 10:40 decided: group by month at service layer, db untouched

## Handoff notes
(left empty until done or blocked; see below)
```

## Lifecycle

```
open ──claim──▶ in-progress ──finish──▶ done
                   │
                   └──stuck──▶ blocked ──unblock──▶ open
```

1. **Creating**: any AI (or human) may drop a new task file with `state: open`
   and a clear Goal. One task = one file; split big work into multiple tasks.
2. **Claiming**: before writing any code, set `state: in-progress`, fill
   `owner` and `claimed_at`. **If a task is `in-progress` with a heartbeat
   newer than 2 hours, it is taken — work on something else or create a
   related task for yourself.**
3. **Heartbeating**: update `heartbeat` whenever you complete a step. A stale
   heartbeat (> 2 hours) means the owner walked away; another AI may take over
   (set owner to itself, note the takeover in Progress).
4. **Finishing**: move to `done`, fill Handoff notes: what changed, where,
   and any trap you left behind. Commit the code and the ledger update together.
5. **Blocking**: stuck? Move to `blocked` and write what you're waiting for.
   A blocked task claims nothing.

## Anti-Collision Rules (the iron part)

- **Claim before code.** No ledger entry, no edits. Read-only review never
  needs to claim.
- **One task, one owner.** Two AIs never share an in-progress task.
- **Commit at every done step**, so even a collision is recoverable.
- **Handoff through the ledger**, not verbal summaries: the next AI reads
  Progress + Handoff notes + the layer READMEs' public interface lists.
- **Heartbeat or let go.** Holding a task without working on it is worse
  than not claiming.

## Where the Ledger Lives

- Single project: `data/ai-tasks/` inside the repo (version it with git).
- Across many projects on one machine: a shared directory, e.g.
  `<your-vault>/ai-tasks/`, one file per task with the project name in frontmatter.

## Why Not a Fixed Role Table?

Role tables (who is the "workhorse", who is the "specialist") are personal:
they depend on which tools you pay for and how strong each is. They also go
stale the moment a quota changes. The ledger is impersonal and self-correcting:
whoever claims a task does it; quality gates (review before release) belong
in the task's own checklist, not in someone's identity.

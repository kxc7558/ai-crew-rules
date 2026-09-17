---
name: ai-crew
description: Installs AI Crew Rules into a project — a four-layer architecture scaffold, a project startup gate (open-source-first + layering evaluation hook), and a multi-AI task ledger that prevents agents from overwriting each other. Use when the user says "set up ai-crew rules", "install AI crew rules", "add AI discipline to this project", "装 AI 施工队规矩", "给项目装规矩", or asks for layered architecture / open-source-first / multi-AI coordination conventions.
---

# AI Crew Rules Installer

You are installing "AI Crew Rules" into the user's project. Follow the steps below. **After each step, report back in one plain sentence.** Any write to the user's configuration must be explained before it happens.

## Step 0: Understand the environment

1. Confirm the target project directory (the current working directory, or one the user names).
2. Check whether the project already has git, an existing `CLAUDE.md` / `AGENTS.md` / rules files. Never overwrite — merge.
3. Ask the user once, all at once:
   - Is this a long-lived project or a one-off script? (This decides whether layering is warranted.)
   - Will more than one AI tool work on this repo? Where should the ledger live (in the repo, or a shared directory)?

## Step 1: Lay the architecture scaffold

Only when the project is long-lived. For one-off scripts, skip and say why in one line.

1. Copy the contents of `templates/layered-project/` into the project root:
   - `CLAUDE.md` — the project constitution
   - `api/README.md`, `service/README.md`, `db/README.md`, `shared/README.md` — per-layer rules
2. If the project already has a `CLAUDE.md`, merge only the "layer map and call direction" section into it. Do not replace the whole file.
3. If the directory names don't fit the project type (a pure frontend, say), rename them per the mapping note in the constitution — the direction rule stays unchanged.
4. **Immediately after copying, `git init` if needed and commit the scaffold as the first node.** Message: `feat: ai-crew layered scaffold`

## Step 2: Install the startup gate hook

**First check whether the hook is already provided.** If this skill is being read from a Claude Code plugin directory (a path containing `plugins/` or `marketplaces/`), the plugin already registers the hook through its `hooks/hooks.json`. In that case **skip this step entirely** and tell the user the hook came with the plugin — do not edit `settings.json`, or the hook will fire twice.

Otherwise, install it manually:

1. Copy `hooks/project-startup-gate.py` to the user's global hooks directory:
   - Claude Code: `~/.claude/hooks/project-startup-gate.py`
2. Edit `~/.claude/settings.json` and **merge** the following into the existing `hooks` key — never replace the file:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python \"<home>/.claude/hooks/project-startup-gate.py\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

   - On Windows use absolute paths for both `python.exe` and the script.
   - After editing, validate the file parses as JSON, then confirm to the user.
3. If the user's primary tool is not Claude Code (Codex, say), skip the hook and instead write the two hard rules — open-source-first and layering evaluation — into that tool's global rules entry point (e.g. `~/.codex/AGENTS.md`, merged if it already exists). The rule text is in Step 4.

## Step 3: Configure the rules files

1. Copy `templates/rules/layered-architecture.md` to `~/.claude/rules/common/` (create the directory if needed).
2. If the scaffold path referenced at the end of that file differs from where Step 1 actually put things, update it to the real path.

## Step 4: Configure the multi-AI task ledger

1. Copy `templates/rules/ai-task-ledger.md` to `~/.claude/rules/common/`.
2. Confirm with the user where the ledger should live (ask once):
   - Mostly one project → `data/ai-tasks/` inside that repo (travels with git, so handoffs stay traceable)
   - Many projects, switching often → a shared directory (e.g. `<vault>/ai-tasks/`), with the project name in each file's frontmatter
3. Create the ledger directory with a `_README.md` explaining usage (the Lifecycle section of `ai-task-ledger.md` is enough).
4. If the user runs other AI tools, write the same `ai-task-ledger.md` into their global rules entry point (e.g. `~/.codex/AGENTS.md`, merged). **The ledger mechanism is identical for every tool — never customize it per tool.**
5. Tell the user plainly: collisions are prevented by the ledger itself, not by assigning roles — claim a task before coding, heartbeat every step, and after two hours of silence anyone may take over.

## Step 5: Verify and report

1. Checklist:
   - [ ] Four scaffold directories plus their per-layer READMEs exist (if applicable)
   - [ ] `settings.json` is valid JSON and no pre-existing config was lost
   - [ ] The hook script exists and passes a pipe test: `echo '{"prompt":"build a new feature"}' | python <hook path>` should emit JSON containing `additionalContext`
   - [ ] Rules files are in place (layering + task ledger)
   - [ ] The ledger directory exists and contains `_README.md`
2. Commit everything if the project is a git repo.
3. Report in plain language what was installed and what each piece does. Mention that **a new session is required for it to take effect**; already-open sessions need a restart or one visit to the `/hooks` menu.

## Notes

- Fail-open throughout: if hook installation fails, do not block the conversation. Explain and continue.
- Never overwrite the user's existing configuration — merge only, and show the key points of the diff first.
- If the user is non-technical, report outcomes and analogies, not a pile of JSON, hook names, and file paths.

# Customize

## Change the startup keywords

Edit the `KEYWORDS` regex at the top of `hooks/project-startup-gate.py`:

```python
KEYWORDS = re.compile(
    r"新建项目|新项目|做项目|做个|做一个|搭一个|搭建|开发|新功能|加功能|加一个功能|"
    r"新需求|新应用|新网站|新工具|从零开始|从0开始|"
    r"\bnew (project|app|application|website|site|tool|feature|service|module|component|script|package|library)\b|"
    ...
)
```

- Too sensitive → delete the broad terms (`做项目`, `开发`, `scaffold`).
- Too quiet → add the phrasings you actually type.
- English-only workspace → keep the `\bnew (project|app|feature|...)\b` and `add a feature` patterns and drop the Chinese alternation.

After editing, run the regression suite so you don't silently break a case:

```bash
python tests/test_startup_gate.py
```

## Change the injected gate text

The `GATE` constant in the same file is the exact instruction injected into the AI's context. Rewrite it for your team's conventions, but keep the two load-bearing parts: **open-source-first as a hard gate** and **the layering evaluation**.

## Remap layer directory names

Frontend projects usually map the layers like this:

| Standard layer | Frontend mapping |
| --- | --- |
| `api/` | `pages/` or `views/` — what the user sees |
| `service/` | `store/` or `composables/` — state and logic |
| `db/` | `api-client/` or `services-data/` — data fetching |
| `shared/` | `utils/` or `components/` — generic pieces |

The direction rule is unchanged: presentation → logic → data, downward calls only. After renaming, update the layer names in each layer README and in `CLAUDE.md`.

## Adapt to another AI tool

| Tool | Global rules file | Project constitution |
| --- | --- | --- |
| Claude Code | `~/.claude/rules/common/*.md` + `~/.claude/CLAUDE.md` | `CLAUDE.md` at the repo root |
| Codex | `~/.codex/AGENTS.md` | `AGENTS.md` at the repo root |
| Cursor | `.cursor/rules/*.mdc` or `.cursorrules` | same |
| Anything else | that tool's custom instruction entry point | the matching file at the repo root |

The constitution (layer map, responsibility table, interface lists) and the ledger mechanism are plain Markdown and portable to any tool. Only the file location differs.

## Tune the task ledger

`templates/rules/ai-task-ledger.md` is meant to work as-is — it deliberately is not customized per person. Two things are worth adjusting:

1. **Where the ledger lives.** One project → `data/ai-tasks/` inside that repo, versioned with git. Many projects → a shared directory (a notes vault, say), with the project name in each file's frontmatter.
2. **The heartbeat window.** Default: two hours without an update means the owner walked away and another AI may take over. Tight, fast-moving teams can shorten it to one hour. Long-running jobs (data pipelines, training) are better at half a day, with the expected duration written into the task file.

Update the ledger directory's `_README.md` to match whatever you change.

## Contributing

Pull requests welcome: keyword tables for more languages, layer-name mappings for more project types, and adapter notes for other tools. Keep each file single-purpose and the total size small.

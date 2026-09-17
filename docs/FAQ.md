# FAQ

## Why four layers and not OSI's seven?

OSI is a network protocol model, designed for interconnecting heterogeneous devices. Copying its seven layers into code turns layering into bureaucracy: one line of change has to pass through seven layers of ceremony. Practice converged on four (interface / business / data / common) — Angular, Spring, and most mainstream frameworks land in that range. The point of layering is clear responsibility boundaries, not a large number.

## Can I adopt this in a project that already exists?

Yes, and you should not rewrite anything. Two approaches:

1. **Migrate gradually.** Put new code in the four layers, and move old code over when you happen to touch it. The scaffold's `CLAUDE.md` is an incremental constraint for the AI, not a demand to reorganize everything at once.
2. **Rules without the scaffold.** If the project structure is already settled, install only the startup gate and the task ledger and skip the scaffold. The installer walks through each piece separately.

## The hook fires too often, or not often enough

- The keyword list is the `KEYWORDS` regex at the top of `hooks/project-startup-gate.py`. Add and remove freely.
- Too trigger-happy? Delete the broad terms (`做项目`, `开发`, `scaffold`). Too quiet? Add the phrasings you actually use.
- The hook is fail-open: if the script errors it exits silently and never blocks your session.
- To check it by hand: `echo '{"prompt":"开发一个新功能"}' | python project-startup-gate.py` — JSON output means it works. The repo ships a regression suite: `python tests/test_startup_gate.py`.

## Will the gate make the AI search open source for every tiny change?

No. It only injects instructions when a message matches kickoff keywords (new project / new feature / build me). Everyday work — fixing a bug, adjusting styles, refactoring — does not trigger it. The injected text also states that one-off scripts may skip layering as long as the reason is given, so the AI keeps its judgment.

## Do multiple AIs really stop colliding?

Three mechanisms stacked:

1. **The task ledger** — claim before you code. One file per task showing who holds it, how far along it is, and when it last checked in. Nobody touches an in-progress task; two hours without a heartbeat means the owner walked away.
2. **Git nodes** — commit as soon as a piece is done, so even a bad overwrite is recoverable.
3. **Interface lists plus handoff notes** — AIs read each other's public interface lists in the layer READMEs and the handoff notes in the ledger. Nothing relies on verbal summaries.

This is *reduce the odds plus stay recoverable*, not a mathematical mutex. When a collision does happen, `git` is the undo button.

## Does it work with Cursor, Windsurf, and other tools?

The rules files (the architecture constitution, the task ledger) are plain Markdown, so any tool that supports custom rules or instruction files can use them directly. The repo ships a ready-made Cursor rule at [`.cursor/rules/ai-crew.mdc`](../.cursor/rules/ai-crew.mdc) and a generic [AGENTS.md](../AGENTS.md) that Codex and other agents read.

The hook itself is Claude Code-specific. On other tools, write the two hard rules — open-source-first and layering evaluation — into that tool's global instruction file as a substitute. The installer does this for you when it detects a non-Claude-Code primary tool.

## Is this useful if I'm not a programmer?

That is one of its design targets. The author is a non-technical product manager who maintains several projects by describing intent and letting the AI implement. Every rule here exists to make that workflow safer: layering turns bug localization into a table lookup, the open-source gate stops the AI from burning hours reinventing a wheel, and the ledger makes handoffs between tools traceable without anyone reading code.

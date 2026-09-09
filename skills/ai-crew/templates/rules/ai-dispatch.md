# Multi-AI Dispatch Rule

Multiple AI coding tools on this machine share work by quota and strength.
Fill in your actual tool lineup below.

## Job Table

| Job | Tool | Gets what work |
|-----|------|----------------|
| Odd jobs | <free/lightweight tool> | Independent, simple, single-turn: syntax lookups, <30-line snippets, translation, format conversion |
| Build crew | <main workhorse tool> | Daily driver: development, debugging, refactoring, batch ops, anything needing project context |
| Specialist | <strongest/quota-limited tool> | Hard problems: architecture, stubborn bugs, complex algorithms, key design |
| Inspector | <strongest/quota-limited tool> | Final review of important output: code review, pre-release checks |

## Dispatch Principles

1. Default to the workhorse — don't outsource to save tokens.
2. Send work to the Specialist only when: you're stuck / the user names that
   tool / important output needs final review.
3. Give the Specialist full context in one dispatch (background, file paths,
   acceptance criteria) — its quota is scarce; avoid back-and-forth.
4. Odd jobs only when it's genuinely a one-command task.

## Anti-Collision (multi-AI safety net)

- Only one AI touches a given project's code at any moment.
- Commit immediately after finishing a chunk (git nodes = undo points).
- AI-to-AI handoff goes through each layer README's "Public Interface List",
  never through verbal summaries.

## Shared Knowledge Base

All tools follow the shared knowledge-base protocol at `<your-vault-path>/`:
progress → 10-Projects, decisions → 20-Decisions, lessons → 30-Lessons.

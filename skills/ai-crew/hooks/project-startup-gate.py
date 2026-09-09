# -*- coding: utf-8 -*-
"""Project Startup Gate — UserPromptSubmit hook (ai-crew-rules)

Detects project/feature kickoff keywords in the user's prompt and injects
a "startup gate" into the AI context: (1) search open-source first before
writing anything original, (2) evaluate whether the layered architecture
scaffold is needed.

Fail-open by design: any error exits silently and never blocks the session.
Customize KEYWORDS below to fit your language / workflow.
"""
import json
import re
import sys

# Kickoff keywords — customize freely (add your language's phrasings)
KEYWORDS = re.compile(
    r"新建项目|新项目|做项目|做个|做一个|搭一个|搭建|开发|新功能|加功能|加一个功能|"
    r"新需求|新应用|新网站|新工具|从零开始|从0开始|new project|new app|build me",
    re.IGNORECASE,
)

GATE = """[Project Startup Gate] A project/feature kickoff request was detected.
Before writing ANY code, complete these two steps:

1. Open-source first (hard gate): search the open-source community (GitHub,
   npm/PyPI, HuggingFace, etc.) for existing solutions. Adoption priority:
   use as-is > port & adapt > wrap > build from scratch. You may only write
   original code after a real search confirms nothing suitable exists, and
   you must tell the user what you searched and why nothing fit.

2. Layered architecture evaluation: decide whether the four-layer layout
   (api -> service -> db -> shared) is warranted.
   - Long-lived project / growing features / more than one page or module
     -> use the layered scaffold, then `git init` and commit the scaffold
     as the first node
   - One-off script -> skipping layers is fine, state the reason in one line

Finally, report both conclusions to the user in plain non-technical language,
e.g. "Found an existing open-source solution X, adopting it" / "This project
needs long-term maintenance, so I'm building it in layers"."""


def main() -> None:
    try:
        raw = sys.stdin.buffer.read().decode("utf-8", "ignore")
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        return  # parse failure -> fail open
    prompt = str(data.get("prompt", ""))
    if KEYWORDS.search(prompt):
        out = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": GATE,
            }
        }
        # ensure_ascii avoids Windows console encoding issues
        sys.stdout.write(json.dumps(out, ensure_ascii=True))


if __name__ == "__main__":
    main()

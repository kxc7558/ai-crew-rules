# -*- coding: utf-8 -*-
"""Regression tests for the project startup gate hook.

Runs the hook exactly the way Claude Code does — JSON on stdin, JSON on
stdout — and asserts which prompts should and should not trigger the gate.

    python tests/test_startup_gate.py
"""
import json
import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "skills" / "ai-crew" / "hooks" / "project-startup-gate.py"

# Prompts that must trigger the gate: someone is starting something new.
SHOULD_FIRE = [
    # Chinese
    "帮我搭建一个新项目",
    "新建项目，用 Python 写个爬虫",
    "给这个项目加一个新功能",
    "我想做一个记账工具",
    "从零开始做一个网站",
    "开发一个新应用",
    # English
    "build me a CLI tool for resizing images",
    "build a new feature for the export module",
    "I want to create a new project for tracking expenses",
    "let's build a dashboard",
    "help me build an app",
    "set up a new project",
    "scaffold a service for payments",
    "add a feature to the settings page",
    "implement a new endpoint for uploads",
    "start a new repo",
    "write a new component",
    "we need a new tool for this",
    "bootstrap a project from scratch",
]

# Prompts that must NOT trigger the gate: ordinary work on existing code.
SHOULD_NOT_FIRE = [
    # Chinese
    "今天天气怎么样",
    "把这个函数的 bug 修一下",
    "解释一下这段代码",
    "数据库查询太慢了，优化一下",
    "把导出改成按月份分组",
    # English
    "fix the bug in export.js",
    "explain this function",
    "refactor the auth module",
    "the tests are failing, find out why",
    "switch exports to month grouping",
    "create a new branch for this",
    "add a test for the parser",
    "commit these changes",
    "what does this regex do",
]


def run_hook(prompt: str) -> str:
    """Feed one prompt to the hook the way the harness does; return stdout."""
    payload = json.dumps({"prompt": prompt})
    result = subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload.encode("utf-8"),
        capture_output=True,
    )
    return result.stdout.decode("utf-8", "ignore").strip()


def fired(stdout: str) -> bool:
    if not stdout:
        return False
    try:
        return "additionalContext" in json.loads(stdout)["hookSpecificOutput"]
    except Exception:
        return False


def main() -> int:
    failures = []

    for prompt in SHOULD_FIRE:
        if not fired(run_hook(prompt)):
            failures.append(("missed (should have fired)", prompt))

    for prompt in SHOULD_NOT_FIRE:
        if fired(run_hook(prompt)):
            failures.append(("false positive (should not fire)", prompt))

    total = len(SHOULD_FIRE) + len(SHOULD_NOT_FIRE)
    for kind, prompt in failures:
        print(f"FAIL  {kind}: {prompt}")
    print(f"\n{total - len(failures)}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

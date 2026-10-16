#!/usr/bin/env python3
"""Destructive-command guard: a PreToolUse hook for Claude Code.

Reads the hook's JSON from stdin. Exits 2, with the reason on stderr, to
block a command that cannot be undone or an edit to a locked path. Exits 0
to allow. Standard library only.

Blocked: force-push, git reset --hard, deleting branches, rm -r -f outside
the project folder, DROP TABLE / DATABASE / SCHEMA and TRUNCATE, skipping
git hooks with --no-verify, and edits to paths listed in docs/sdlc/locks.
"""
import fnmatch
import json
import os
import re
import shlex
import sys
from pathlib import Path

OPERATORS = {"&&", "||", ";", "|", "&", "(", ")"}
SQL_RE = re.compile(r"\b(drop\s+(table|database|schema)|truncate)\b", re.IGNORECASE)
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
LOCKS_FILE = Path("docs") / "sdlc" / "locks"


def simple_commands(command: str) -> list[list[str]]:
    """Split a shell command line into simple commands at shell operators."""
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        tokens = list(lexer)
    except ValueError:
        tokens = command.split()
    commands, current = [], []
    for token in tokens:
        if token in OPERATORS:
            if current:
                commands.append(current)
            current = []
        else:
            current.append(token)
    if current:
        commands.append(current)
    return commands


def strip_prefixes(words: list[str]) -> list[str]:
    """Drop leading variable assignments and wrappers such as sudo or env."""
    while words and ("=" in words[0] and not words[0].startswith("-") or words[0] in {"sudo", "env", "command", "exec"}):
        words = words[1:]
    return words


def git_reason(args: list[str]) -> str | None:
    i = 0
    while i < len(args) and args[i].startswith("-"):
        i += 2 if args[i] in {"-C", "-c"} else 1
    if i >= len(args):
        return None
    sub, rest = args[i], args[i + 1:]
    if sub == "push":
        if any(a in {"-f", "--force"} or a.startswith("--force-with-lease") for a in rest):
            return "force-push rewrites the remote history"
        if any(a in {"-d", "--delete"} or (a.startswith(":") and len(a) > 1) for a in rest):
            return "deleting a remote branch"
        if any(a.startswith("+") for a in rest):
            return "a '+' refspec is a force-push"
    if sub == "reset" and "--hard" in rest:
        return "git reset --hard discards uncommitted work"
    if sub == "branch" and any(a in {"-d", "-D", "--delete"} or re.fullmatch(r"-[a-zA-Z]*[dD][a-zA-Z]*", a) for a in rest):
        return "deleting a branch"
    if sub == "commit" and any(re.fullmatch(r"-[a-zA-Z]*n[a-zA-Z]*", a) for a in rest):
        return "git commit -n skips the git hooks"
    return None


def rm_reason(args: list[str], cwd: Path, project: Path) -> str | None:
    flags = [a for a in args if a.startswith("-") and a != "-"]
    recursive = any(a in {"--recursive", "-r", "-R"} or (not a.startswith("--") and re.search("[rR]", a)) for a in flags)
    force = any(a == "--force" or (not a.startswith("--") and "f" in a) for a in flags)
    if not (recursive and force):
        return None
    for target in (a for a in args if not a.startswith("-")):
        if "$" in target or "`" in target:
            return f"rm -rf on '{target}', which the guard cannot resolve"
        path = (cwd / os.path.expanduser(target)).resolve()
        if path == project or not path.is_relative_to(project):
            return f"rm -rf on '{target}', outside the project folder"
    return None


def bash_reason(command: str, cwd: Path, project: Path) -> str | None:
    if "--no-verify" in command:
        return "--no-verify skips the git hooks"
    if SQL_RE.search(command):
        return "dropping or truncating a table deletes data"
    for words in simple_commands(command):
        words = strip_prefixes(words)
        if not words:
            continue
        name = os.path.basename(words[0])
        if name == "git":
            reason = git_reason(words[1:])
        elif name == "rm":
            reason = rm_reason(words[1:], cwd, project)
        else:
            reason = None
        if reason:
            return reason
    return None


def locked_reason(file_path: str, cwd: Path, project: Path) -> str | None:
    locks = project / LOCKS_FILE
    if not file_path or not locks.is_file():
        return None
    path = (cwd / file_path).resolve()
    if not path.is_relative_to(project):
        return None
    rel = path.relative_to(project).as_posix()
    for line in locks.read_text(encoding="utf-8").splitlines():
        pattern = line.strip()
        if pattern and not pattern.startswith("#") and fnmatch.fnmatch(rel, pattern.lstrip("./")):
            return f"'{rel}' is locked in {LOCKS_FILE.as_posix()}"
    return None


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("guard: could not read the hook input; nothing was checked", file=sys.stderr)
        return 1
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd()).resolve()
    cwd = Path(event.get("cwd") or project).resolve()
    tool, tool_input = event.get("tool_name", ""), event.get("tool_input") or {}
    if tool == "Bash":
        reason = bash_reason(str(tool_input.get("command", "")), cwd, project)
    elif tool in EDIT_TOOLS:
        reason = locked_reason(str(tool_input.get("file_path") or tool_input.get("notebook_path") or ""), cwd, project)
    else:
        reason = None
    if reason:
        print(f"Blocked by the destructive-command guard: {reason}. This cannot be "
              "undone or is a locked path, so it is the user's call. Ask the user.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

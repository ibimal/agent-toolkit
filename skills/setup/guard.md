# Destructive-command guard

`scripts/guard.py` blocks commands that cannot be undone and edits to locked
paths. Copy it to `.claude/hooks/guard.py` in the product repo, then add
this to `.claude/settings.json`, merging with any hooks already there:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Edit|Write|MultiEdit|NotebookEdit",
        "hooks": [
          {"type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/guard.py\""}
        ]
      }
    ]
  }
}
```

It blocks:

- force-push, including `--force-with-lease`;
- `git reset --hard`;
- deleting branches, locally or on a remote;
- `rm -r -f` on a path outside the project folder, or on the folder itself;
- `DROP TABLE`, `DROP DATABASE` and `TRUNCATE`;
- skipping git hooks with `--no-verify`;
- edits to any path listed in `docs/sdlc/locks`, one path or glob per line.
  Protected paths stay in the file; a Bug fix adds its regression test while
  the fix is in progress and removes it afterwards.

Removing a block, or a line from `docs/sdlc/locks` that someone else added,
loosens a control, so it is the user's call.

For a harness other than Claude Code, register the same script with that
harness's pre-command hook if it has one, and say so in the setup report if
it has none.

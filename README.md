# agent-toolkit

Personal agent skills and an always-on style file, shared across devices
and agent harnesses (Claude Code, Codex, Gemini CLI, Cursor).

## Layout

```
agent-toolkit/
├── README.md
├── AGENTS.md                  # rules for agents working on this repo
├── CLAUDE.md                  # imports AGENTS.md for Claude Code
├── config.toml                # harness paths and link methods
├── bin/toolkit                # install | sync | uninstall | doctor | check
├── instructions/
│   └── technical-clarity.md   # always-on style rules
├── skills/                    # flat, one folder per skill
└── .github/workflows/check.yml
```

## Commands

| Command     | Effect                                                        | Writes |
|-------------|---------------------------------------------------------------|--------|
| `check`     | Validate skills: frontmatter, name matches folder, lengths.   | No     |
| `doctor`    | Report broken links, missing harnesses, name collisions.      | No     |
| `install`   | Run `check`, link skills and instructions, prune stale links. | Home   |
| `sync`      | `git pull --ff-only`, then `install`.                         | Repo, home |
| `uninstall` | Remove links into this repo and restore `.pre-toolkit` backups. | Home |

## New device

```
git clone <remote> ~/Desktop/Projects/agent-toolkit
cd ~/Desktop/Projects/agent-toolkit
bin/toolkit install
```

After that, run `bin/toolkit sync` to update.

## Add a skill

Copy an existing skill folder, rename it, update `name` and `description`,
then run `bin/toolkit check`.

## Design notes

- The repo is the only place where skills are edited. Each harness gets one
  symlink per skill, so skills installed from other sources stay untouched.
- Skills use the open Agent Skills format with spec frontmatter only.
- `skills/` is flat. Tier folders are avoided because moving a skill breaks
  the links on every device.
- Harness paths live in `config.toml`, because tools change them between
  versions.
- The style rules exist once, in `instructions/technical-clarity.md`.
  Claude Code loads it through an `@` import in `~/.claude/CLAUDE.md`;
  other harnesses get a symlink. The review skill relies on these loaded
  rules and holds no copy.
- A vendored skill records its source in `metadata` and keeps the upstream
  LICENSE file.
- The CLI uses the Python standard library only, so a new device needs no
  setup beyond Python 3.11+.

## Deferred

| Feature                   | Add when                                               |
|---------------------------|--------------------------------------------------------|
| `vendor` command          | Several upstream skills need regular updates           |
| `build` and `dist/`       | You upload skills to chat apps regularly               |
| Profiles per device       | About 15+ skills, or a device needs a subset           |
| Evals                     | You run the style comparison test                      |
| Plugin manifests          | You need a managed install on a machine without a clone |
| Decision records          | Someone else contributes                               |

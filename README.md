# agent-toolkit

Personal agent skills and an always-on style file, shared across devices
and agent harnesses (Claude Code, GitHub Copilot CLI, code-puppy).

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
├── tests/test_toolkit.py      # unittest suite for bin/toolkit
└── .github/workflows/check.yml
```

## Commands

| Command     | Effect                                                        | Writes |
|-------------|---------------------------------------------------------------|--------|
| `check`     | Validate skills, `config.toml`, and the style file.           | No     |
| `doctor`    | Report link problems and duplicate skill names. Exit 1 on a problem. | No |
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

`install` does not replace a path that did not come from this repo, such
as your own skill with the same name. It reports a conflict, installs
everything else, and exits 1.

## Tests

```
python3 -m unittest discover -s tests
```

Each test runs a copy of `bin/toolkit` against a temporary HOME.

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
- `install` never replaces a skill folder, and never writes through a
  symlink, that did not come from this repo. A backup inside a skills
  folder would be listed by the harness as a second skill, and a write
  through a symlink would change a file outside `config.toml`.
- `[skill_readers]` in `config.toml` lists the folders that each tool
  scans, so `doctor` can report a skill name that one tool finds twice.

## Deferred

| Feature                   | Add when                                               |
|---------------------------|--------------------------------------------------------|
| `vendor` command          | Several upstream skills need regular updates           |
| `build` and `dist/`       | You upload skills to chat apps regularly               |
| Profiles per device       | About 15+ skills, or a device needs a subset           |
| Evals                     | You run the style comparison test                      |
| Plugin manifests          | You need a managed install on a machine without a clone |
| Decision records          | Someone else contributes                               |
| Python 3.9 support (fallback parser for the TOML that `config.toml` uses) | A device you use cannot install Python 3.11+ |

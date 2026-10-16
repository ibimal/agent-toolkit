# agent-toolkit

Personal agent skills and an always-on style file, shared across devices
and agent harnesses (Claude Code, GitHub Copilot CLI, code-puppy).

## Layout

```
agent-toolkit/
├── README.md
├── LICENSE                    # MIT
├── AGENTS.md                  # rules for agents working on this repo
├── GLOSSARY.md                # glossary
├── CLAUDE.md                  # imports AGENTS.md for Claude Code
├── config.toml                # harness paths and instructions methods
├── rename-map                 # upstream skill names that this repo changes
├── bin/toolkit                # install | sync | uninstall | doctor | check
├── instructions/
│   └── technical-clarity.md   # always-on style rules
├── skills/                    # flat, one folder per skill
├── tests/                     # unittest suites: bin/toolkit and the skills' scripts
├── workflow/                  # AI-native SDLC design: doc, examples, walkthroughs
│   ├── ai-native-sdlc.md      # the workflow doc
│   └── src/                   # example data and the generator
└── .github/workflows/check.yml
```

## Commands

| Command     | Effect                                                        | Writes |
|-------------|---------------------------------------------------------------|--------|
| `check`     | Validate skills, `config.toml`, and the style file. Scan for leaks. | No |
| `doctor`    | Report link problems and duplicate skill names. Exit 1 on a problem. | No |
| `install`   | Run `check`, link skills and instructions, prune stale links. | Home   |
| `sync`      | `git pull --ff-only`, then `install`.                         | Repo, home |
| `uninstall` | Remove links into this repo and restore `.pre-toolkit` backups. | Home |

## New device

```
git clone https://github.com/ibimal/agent-toolkit.git ~/Desktop/Projects/agent-toolkit
cd ~/Desktop/Projects/agent-toolkit
bin/toolkit install
```

After that, run `bin/toolkit sync` to update. The device needs git and
Python 3.11+ as `python3`.

The repo is public, so the HTTPS URL needs no GitHub login, and `sync`
works on a device where you do not sign in to GitHub. To push from a
device, use `git@github.com:ibimal/agent-toolkit.git` instead.

`install` does not replace a path that did not come from this repo, such
as your own skill with the same name. It reports a conflict, installs
everything else, and exits 1.

## Tests

```
python3 -m unittest discover -s tests
```

Each `bin/toolkit` test runs a copy of the CLI against a temporary HOME.
The other suites test the scripts that skills bundle: the setup guard and
the size-impact simulation.

## Add a skill

Copy an existing skill folder, rename it, update `name` and `description`,
then run `bin/toolkit check`.

## Fork a skill

A fork is a skill copied from an upstream repo. Until the `vendor`
command exists, you update a fork by hand. Its folder holds these files:

- `SKILL.md`: this repo's frontmatter, one line that loads `local.md`,
  and the upstream body, unchanged.
- `local.md`: this repo's additions. Where they differ from the upstream
  body, they win.
- `PROVENANCE`: the upstream repo and path, the pin, the state, and a
  changelog of edits with reasons.
- `LICENSE`: the upstream licence.
- Any other upstream files that the body links to, unchanged.

To fork a skill:

1. Check that the upstream licence allows redistribution in a public
   repo.
2. Copy the upstream files at one commit, and record that commit as the
   pin.
3. Write the frontmatter from the name, trigger, and purpose that the
   workflow doc gives. A typed-only skill also sets
   `disable-model-invocation: true`.
4. Put each rule that the workflow doc adds into `local.md`.
5. If the name differs from the upstream name, add a line to
   `rename-map`.
6. Run `bin/toolkit check`.

The state compares the upstream files in the fork with the pin, after
`rename-map` is applied. `Pristine` means that they match. `Ahead` means
that the fork also edits the upstream body, and the changelog says how and
why. `PROVENANCE` is TOML; its `patterns` key names other upstream skills
that informed `local.md` without being copied.

A skill that the workflow doc marks Write has no upstream body. It records
the skills that informed it in `metadata.inspired-by`.

## Workflow design

`workflow/` holds the design for an AI-native development workflow: its
playbooks, the skills they use, and worked examples. It is the spec for
the skills that this repo will hold. See `workflow/README.md`.

## Design notes

- The repo is the only place where skills are edited. Each harness gets one
  symlink per skill, so skills installed from other sources stay untouched.
- Skills use the open Agent Skills format with spec frontmatter only,
  plus `disable-model-invocation` on typed-only skills. Claude Code reads
  that field and keeps the skill's description out of context. The
  Copilot CLI docs do not list the field.
- `skills/` is flat. Tier folders are avoided because moving a skill breaks
  the links on every device.
- Harness paths live in `config.toml`, because tools change them between
  versions.
- The style rules exist once, in `instructions/technical-clarity.md`.
  Claude Code loads it through an `@` import in `~/.claude/CLAUDE.md`;
  other harnesses get a symlink. The review skill relies on these loaded
  rules and holds no copy.
- A fork keeps the upstream body unchanged and puts this repo's additions
  in `local.md`, so that most upstream updates stay simple. It records
  its source in `PROVENANCE` and keeps the upstream LICENSE file. This
  follows section 10.2 of the workflow doc.
- The restate skill is named `plain-restate`, not `clarify`, because
  models read "clarify" as "ask clarifying questions".
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
| `vendor` command (the upstream sync in workflow doc 10.2) | Several upstream skills need regular updates |
| `build` and `dist/`       | You upload skills to chat apps regularly               |
| Profiles per device       | About 15+ skills, or a device needs a subset           |
| Evals                     | You run the style comparison test                      |
| Plugin manifests          | You need a managed install on a device without a clone |
| Decision records          | Someone else contributes                               |
| Python 3.9 support (fallback parser for the TOML that `config.toml` uses) | A device you use cannot install Python 3.11+ |

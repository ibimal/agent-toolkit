# agent-toolkit

The skills for an AI-native development workflow, an always-on style
file, and a small CLI that links them into each agent harness on each
device. The harnesses are Claude Code, GitHub Copilot CLI and code-puppy;
code-puppy cannot load skills, so it gets the style file only.

The workflow itself is described at
<https://ibimal.github.io/agent-toolkit/>.

## Layout

```
agent-toolkit/
├── README.md
├── LICENSE                    # MIT, for this repo's own work
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
└── .github/workflows/         # check.yml (CI), pages.yml (the workflow site)
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

## Skills

`skills/` holds the 55 skills that the workflow doc catalogues (section
10.1). The doc's 56th skill, `verify-app`, is written into each product
repo by `setup`. Three skills cover most days:

| Type | When |
|---|---|
| `/start <request>` | Any piece of work. On its own, it shows what is in progress and what waits for you. |
| `/huh` | You don't follow the last message, or you are back and need catching up. |
| `/polish` | Before you send a message you wrote. |

In an existing project, the first `/start` adopts the workflow before it
routes the request: section 4.6 of the workflow doc lists the steps.

14 skills start only when you type them. The other 41 can also start
when the agent needs them, inside a playbook or another skill. 40 skills
are forks of upstream skills; 15 are written from the workflow doc.

## Tests

```
python3 -m unittest discover -s tests
```

Each `bin/toolkit` test runs a copy of the CLI against a temporary HOME.
The other suites test the scripts that skills bundle: the setup guard and
the size-impact simulation.

## Add a skill

Every skill follows the workflow doc, so a new skill starts there:

1. Add the skill to `workflow/ai-native-sdlc.md`: its catalog row in
   section 10.1, and its place in sections 2 and 2.3. Name it by the
   rules in section 10.3, and check that no harness reserves the name.
2. Write the skill, or fork it as the next section describes. `/to-skill`
   can draft it.
3. Add its worked example to `workflow/src/examples_data.py`, then run
   `python3 workflow/src/build.py` and `python3 workflow/src/check_doc.py`.
4. Run `bin/toolkit check` and the tests.

## Fork a skill

A fork is a skill copied from an upstream repo. Its folder holds these
files:

- `SKILL.md`: this repo's frontmatter, a note that loads `local.md` and
  marks the skill as changed, and the upstream body with `rename-map`
  applied.
- `local.md`: this repo's additions. Where they differ from the upstream
  body, they win.
- `PROVENANCE`: the upstream repo and path, its authors, the pin, the
  state, and a changelog of edits with reasons.
- `LICENSE`: the upstream licence, plus the licence of any third-party
  text the upstream skill itself includes.
- The other upstream files, verbatim: credits, references and scripts.

To fork a skill:

1. Check that the upstream licence allows redistribution in a public
   repo.
2. Copy the upstream files at one commit. Record that commit as the pin,
   and the upstream authors, in `PROVENANCE`.
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

To update a fork, compare the pinned upstream, the new upstream and the
fork, as section 10.2 of the workflow doc describes. Run `review-skill` on
the update, record the new pin, and add a changelog entry. Updates are made
by hand; no command syncs forks.

A skill that the workflow doc marks Write has no upstream body. It records
the skills that informed it in `metadata.inspired-by`.

## Workflow design

`workflow/` holds the design for an AI-native development workflow: its
playbooks, the skills they use, and worked examples. It is the spec for
the skills that this repo holds. See `workflow/README.md`.

The design is published as a site at
<https://ibimal.github.io/agent-toolkit/>: the workflow doc is the
homepage, with the worked examples and the walkthroughs beside it.
`.github/workflows/pages.yml` rebuilds and deploys it on each push to
`main` that changes `workflow/`.

## Licences

This repo's own code and text are under the MIT licence in `LICENSE`.
Each fork in `skills/` stays under its upstream licence, in the licence
file in its folder, and `PROVENANCE` names its authors:

| Licence | Forks |
|---|---|
| MIT | Forks of mattpocock/skills, pstack, cursor-team-kit, compound-engineering, and K-Dense |
| Apache-2.0 | `explore-data`, `review-result`, `data-context`, `to-skill`, `review-skill`, `write-notebook` |
| CC BY-SA 4.0 | `second-opinion`, `review-dependency`, each as a whole, `local.md` included |

Each fork's `SKILL.md` says that it is changed, and `PROVENANCE` lists
the changes, as Apache-2.0 and CC BY-SA 4.0 require. A skill written
from the workflow doc names the skills that informed it in
`metadata.inspired-by`; it copies no text from them.

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
  other harnesses get a symlink. Skills that apply the rules, such as
  `technical-writing`, `polish` and `huh`, rely on these loaded rules and
  hold no copy.
- A fork changes the upstream body only through `rename-map` and puts
  this repo's additions in `local.md`, so that most upstream updates stay
  simple. This follows section 10.2 of the workflow doc.
- The repo is public, so `data-context` keeps its map of your data in
  `skills/data-context/map/`, which `.gitignore` excludes. Schemas and
  metric definitions never reach the public history.
- The CLI uses the Python standard library only, so a new device needs no
  setup beyond Python 3.11+.
- `install` never replaces a skill folder, and never writes through a
  symlink, that did not come from this repo. A backup inside a skills
  folder would be listed by the harness as a second skill, and a write
  through a symlink would change a file outside `config.toml`.
- `[skill_readers]` in `config.toml` lists the folders that each tool
  scans, so `doctor` can report a skill name that one tool finds twice.

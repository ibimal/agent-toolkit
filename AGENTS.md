# agent-toolkit: working rules

This repo holds personal agent skills and one always-on style file. A small
CLI links them into each agent harness on each device.

## Skills

- Follow the Agent Skills specification (agentskills.io). The folder name
  must equal the `name` field: lowercase letters, numbers, and single
  hyphens.
- Use only spec frontmatter fields: `name`, `description`, and optionally
  `license`, `compatibility`, `metadata`, `allowed-tools`. There is one
  exception: a skill that the workflow doc lists as typed only (section
  2.3) also sets `disable-model-invocation: true`.
- Keep SKILL.md under 500 lines. Keep file references one level deep.
- A fork keeps the upstream body and files unchanged. Put additions in
  `local.md`, and record the source, pin, and changes in `PROVENANCE`.
  See README.md, "Fork a skill".
- Describe actions, not harness tool names. Write "read the file", not
  "use the Read tool".
- The sibling rewrite skills (plain-restate, condense, deepen) must each
  state what they do and which sibling they are not.

## Tooling

- `bin/toolkit` is one Python 3.11+ entry point with subcommands. Use the
  standard library only; read `config.toml` with `tomllib`.
- Read-only commands: `check` (repo content), `doctor` (device state).
- Writing commands: `install`, `sync`, `uninstall`. Each supports
  `--dry-run`.
- After changing `bin/toolkit`, run `python3 -m unittest discover -s tests`.

## Safety

- Write only to paths listed in `config.toml`.
- Delete only symlinks that point into this repo.
- Before replacing an existing file, back it up with the suffix
  `.pre-toolkit`. `uninstall` restores these backups.
- Never replace a skill folder, or write through a symlink, that did not
  come from this repo. Report a conflict, skip that item, and exit 1.
- This repo is public. Never add credentials, tokens, or work-specific
  content, such as internal project names, URLs, or people.
- Test writing commands against a temporary HOME, for example
  `HOME=$(mktemp -d)`. Never test against the real home folder.

## Workflow design

- `workflow/ai-native-sdlc.md` is the design for the skills that this repo
  will hold. When you build one of its skills, use the name, trigger, and
  rules that the doc gives. If the build changes any of them, update the
  doc in the same commit.
- Edit `workflow/ai-native-sdlc.md` and the files in `workflow/src/`. Never
  edit `workflow/examples.md` or `workflow/walkthroughs.html` by hand: run
  `python3 workflow/src/build.py` to regenerate them.
- After a change to the doc, run `python3 workflow/src/check_doc.py`.

## Scope

- Deferred features are listed in README.md with their triggers. Do not
  add them unless a trigger has occurred.
- Write prose in this repo according to `instructions/technical-clarity.md`,
  and use the terms in `GLOSSARY.md`.
- Run `bin/toolkit check` before each commit.

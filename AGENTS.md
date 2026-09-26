# agent-toolkit: working rules

This repo holds personal agent skills and one always-on style file. A small
CLI links them into each agent harness on each device.

## Skills

- Follow the Agent Skills specification (agentskills.io). The folder name
  must equal the `name` field: lowercase letters, numbers, and single
  hyphens.
- Use only spec frontmatter fields: `name`, `description`, and optionally
  `license`, `compatibility`, `metadata`, `allowed-tools`.
- Keep SKILL.md under 500 lines. Keep file references one level deep.
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

## Safety

- Write only to paths listed in `config.toml`.
- Delete only symlinks that point into this repo.
- Before replacing an existing file, back it up with the suffix
  `.pre-toolkit`. `uninstall` restores these backups.
- Test writing commands against a temporary HOME, for example
  `HOME=$(mktemp -d)`. Never test against the real home folder.

## Scope

- Deferred features are listed in README.md with their triggers. Do not
  add them unless a trigger has occurred.
- Write prose in this repo according to `instructions/technical-clarity.md`.
- Run `bin/toolkit check` before each commit.

# Handoff from the claude.ai planning conversation (2026-09-26)

Delete this file when the tasks below are done. Durable decisions are in
README.md; working rules are in AGENTS.md.

## Background

The goal was LLM responses that are plain but still technically precise.
I evaluated `bro` (pstack) and `wait-what` (Matt Pocock), which uses
ASD-STE100 plus a CONTEXT.md glossary. The result is an always-on style
file, `instructions/technical-clarity.md`, that borrows selected
STE100-inspired sentence principles without the restricted dictionary.
A few corrective skills support it.

The repo layout was compared with anthropics/skills, openai/skills,
huggingface/skills, obra/superpowers, mattpocock/skills, and chezmoi-based
dotfiles, then reduced to a good default with YAGNI.

## Skill decisions

- `bro`: dropped. It overlaps with wait-what, and the always-on file covers
  most of the problem. Its conversational phrasing could be folded into
  plain-restate.
- `wait-what` becomes `plain-restate`. It was not named `clarify`, because
  models read that as "ask clarifying questions".
- `condense` and `deepen`: new siblings. Drafts are in place.
- `technical-writing-review`: holds review steps only. The rules come from
  the always-on file.

## Open questions (ask me before deciding)

1. Two suggested edits to `technical-clarity.md` are not applied yet:
   (a) remove "Use a list when its structure makes the information easier
   to understand or scan."; (b) in the noun-stack rule, change "unclear"
   to "unclear to that reader".
2. Keep the name `plain-restate`? Decided on 2026-09-27: keep it. The
   reason is in README.md.
3. Which harnesses do I use on each device? `config.toml` lists three:
   claude-code, copilot-cli, and code-puppy.
4. Codex reads `~/.agents/skills`, and other tools may read it too. Check
   whether this causes duplicate skill listings. Answered on 2026-09-27:
   Copilot CLI and VS Code read `~/.agents/skills`, so `install` never
   writes there. VS Code still finds each skill twice, in
   `~/.claude/skills` and `~/.copilot/skills`. `doctor` reports both
   cases. The details are in `config.toml`.
5. Where will the remote live (for example, a private GitHub repo)?

## Tasks, in order

1. Verify every path in `config.toml` against current official docs.
   Record the source URL in a comment next to each value.
2. Implement `bin/toolkit` as specified in README.md and AGENTS.md.
3. Add tests for `install` and `uninstall` that use a temporary HOME.
4. Compare `plain-restate` with upstream wait-what. If upstream text is
   copied, add its LICENSE file and set `metadata.upstream-ref` to the
   commit.
5. Review and finish the four skill drafts.
6. Add `.github/workflows/check.yml` that runs `bin/toolkit check`.

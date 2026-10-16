# Local additions to why

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Read-only.** Never change code.
- **The workflow's own records are an evidence category.** Investigate them
  alongside source control: change folders in `docs/sdlc/changes/` and their
  archive (spec, design, plan, bugfix and findings files), intents in
  `docs/sdlc/intents/`, ADRs in `docs/sdlc/adr/`, run trails in `.audit/`,
  incident notes, research notes in `docs/research/`, and the health ledger.
- **Connected sources.** Discover the MCP servers and tools the current
  harness exposes, instead of the Cursor `mcps/` directory.
- **Models and subagents.** Ignore the `pstack-models.mdc` rule, the default
  model slugs and the Task-tool flags in the instructions below; they belong
  to Cursor. Use the subagent mechanism of the current harness, read-only
  where the instructions say so. When `docs/sdlc/config` names models for
  this skill's roles, use them; otherwise use the harness default. Ignore
  references to the `poteto-mode` skill.

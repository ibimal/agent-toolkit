# Local additions to how

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Read-only.** Never change code.
- **Vocabulary.** Use the `codebase-design` terms for structure and the terms
  in `GLOSSARY.md` for the domain.
- **Diagrams.** Build the explanation diagram by diagram: a small diagram for
  each flow or structure that a sentence cannot carry.
- **Models and subagents.** Ignore the `pstack-models.mdc` rule, the default
  model slugs and the Task-tool flags in the instructions below; they belong
  to Cursor. Use the subagent mechanism of the current harness, read-only
  where the instructions say so. When `docs/sdlc/config` names models for
  this skill's roles, use them; otherwise use the harness default. Ignore
  references to the `poteto-mode` skill.

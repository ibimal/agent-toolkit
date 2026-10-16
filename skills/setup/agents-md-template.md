# AGENTS.md template

Keep the file under a page: it loads in every session. Point at other files
instead of copying them. `CLAUDE.md` holds the single line `@AGENTS.md`, so
every harness reads the same text.

```markdown
# <Project name>

<One or two sentences: what this product is and who it serves.>

## Commands

- Build: `<command>`
- Test: `<command>`
- Health checks: `<command from docs/sdlc/config>`
- Verify end to end: the `verify-app` skill

## Where things are

- Workflow artifacts: `docs/sdlc/` (product brief, intents, changes, ADRs)
- The project's words: `GLOSSARY.md`
- Code standards: `REVIEW.md`

## Working rules

- Start any piece of work with `/start`.
- When a reply asks more than one question, number them (Q1, Q2), so
  `/huh Q2` can point at one.
- Use the terms in `GLOSSARY.md`.
```

---
name: setup
description: "Sets a repo up for the AI-native workflow: the docs layout, the tracker link, the reachable models and reviewer ladder in docs/sdlc/config, the destructive-command guard, and AGENTS.md, CLAUDE.md and REVIEW.md stubs; once the stack is known, commands, format and lint hooks, the verify command, health checks, REVIEW.md standards and CI. In an existing project it runs the adoption path: merges existing instruction files, drafts the product brief and architecture from the code, and starts the health ledger with a full sweep. Use when /start finds no docs/sdlc/config, at New application steps 1 and 5, on a device or harness the config does not list, or when the user asks to set up a repo."
metadata:
  inspired-by: https://github.com/mattpocock/skills (setup), https://github.com/cursor/plugins (pstack setup, verification skills), https://github.com/astral-sh/claude-code-plugins (uv, ruff, ty), https://github.com/trailofbits/skills (modern-python), https://github.com/wshobson/agents (blocking --no-verify)
---

# Setup

Install the workflow's files and controls in a product repo, so that
`/start` is the only command it needs. Setup only adds controls; adding a
control needs no gate. It never loosens or removes one, and it never
overwrites a file the repo already has: it merges into it, or reports the
conflict and leaves the file alone.

## First pass: no stack needed

Run it when `docs/sdlc/config` does not exist.

1. **Say what you will add,** in a short list, and ask one question: which
   tracker to use (local files, GitHub Issues, Jira or Linear). Local files
   are the default.
2. **Docs layout.** Create the folders below as they are first needed; do
   not create empty files. In particular, never create an empty
   `GLOSSARY.md`; `glossary` creates it with the first settled term.
3. **Models and ladder.** Find the models and model CLIs reachable on this
   device and harness: the harness's own models, and the CLIs of other model
   families (such as `codex`, `gemini` or `agy`) that run here. Map the
   harness's effort scale. Write both, and the reviewer ladder, to
   `docs/sdlc/config` using [config-template.md](config-template.md).
4. **Guard.** Install the destructive-command guard: copy
   `scripts/guard.py` to `.claude/hooks/guard.py` and register it as
   [guard.md](guard.md) describes.
5. **Stubs.** Write `AGENTS.md` from
   [agents-md-template.md](agents-md-template.md), a `CLAUDE.md` that holds
   the line `@AGENTS.md`, and a `REVIEW.md` from
   [review-template.md](review-template.md).
6. **Existing project.** When the repo already has code, continue with the
   adoption path below instead of stopping here. When the expansion variant
   finds no brief, draft one from the code and docs without asking.
7. **Report** what you added and what you left alone, then commit the setup
   on a branch.

**Model check only.** When `/start` runs on a device or harness the config
does not list, repeat step 3 alone and add a section for it.

## Second pass: the stack is known

Run it at New application step 5, or when the user names the stack.

1. **Commands.** Record the build, test and run commands in `AGENTS.md`.
2. **Format and lint hooks** that run after each edit.
3. **Health command.** Put the baseline health checks behind one command,
   named in `docs/sdlc/config` (`make health` by default): format and lint,
   type check, complexity, dead code, import contracts from
   `architecture.md`, unused or missing dependencies, committed secrets, docs
   that point at missing files or symbols, failing `AGENTS.md` commands, and
   glossary synonyms. For Python, use uv, ruff, a type checker (ty or
   mypy), vulture, import-linter, deptry and a secrets scanner.
4. **Verify command and skill.** Write `.claude/skills/verify-app/SKILL.md`
   from [verify-app-template.md](verify-app-template.md), filled in with the
   one command that proves the app or pipeline works end to end.
5. **REVIEW.md standards.** Fill in the language-specific rows and the
   thresholds.
6. **CI** where the user wants it: run the test command and the health
   command on every PR.
7. **Report and commit,** as in the first pass.

## Existing project: adoption

When the repo already has code, run this path once, in order. The brief and
the architecture describe the project as it is; what should change becomes
intents later.

1. **Both passes above,** with the stack read from the repo: its build
   files, CI config and lint settings.
   - Merge, never overwrite. Move the content of an existing `CLAUDE.md`
     into `AGENTS.md`, fix or flag its stale facts (commands that fail,
     files that are gone), and leave `@AGENTS.md` in `CLAUDE.md`. Show the
     diff in the report. Keep existing CI, hooks and decision records.
   - Make the health command wrap the tools the repo already runs. Start
     `REVIEW.md` from the baseline and record the conventions the code
     already follows.
   - Link the tracker the repo already uses. Leave its open issues there;
     each becomes an intent or a Bug fix when `/start` picks it up.
2. **Verify.** Write `verify-app` from the existing test and run commands,
   and run it from a clean clone.
3. **Product brief.** Draft `docs/sdlc/product.md` from the README, docs,
   code and open issues. Grill the draft with the user (`grilling`, with
   `glossary`), and `to-product` writes it. Gate: brief accepted.
4. **Architecture.** Draft `docs/sdlc/architecture.md` from the code as it
   is. Grill the user on what the code cannot show: the intended
   boundaries, environments and deployment, and what is being retired.
   Then `to-design` in system mode finishes it. Record existing decisions
   that are hard to reverse and surprising as ADRs, and link existing
   decision records instead of moving them. Gate: architecture accepted.
5. **Baseline health.** Run `architecture-health`, then `code-health`, as a
   full sweep, so the health ledger starts with every area. Change nothing;
   the findings wait for the user's pick.
6. **Agent-readiness check.** A fresh session, given only the repo, states
   the commands, conventions and architecture and runs `verify-app`. List
   any missing control (CI, deploy, `verify-app`, guard) in the report,
   because parallel worktrees and AFK runs wait for them.

Then hand the request that started the run back to `/start`.

## Docs layout

```
AGENTS.md, CLAUDE.md               standing context, under a page
GLOSSARY.md                        the project's words; GLOSSARY-MAP.md when there are several contexts
REVIEW.md                          code standards, thresholds, precedence, review axes, severity
.claude/skills/verify-app/         project-local verification skill
.claude/hooks/guard.py             destructive-command guard
.claude/settings.json              hooks
docs/runbook.md
docs/sdlc/config                   tracker, models, reviewer ladder, health command
docs/sdlc/locks                    paths the guard protects (protected paths, regression tests)
docs/sdlc/product.md               product brief
docs/sdlc/architecture.md
docs/sdlc/intents/I-NNNN-<slug>.md
docs/sdlc/INTENTS.md               generated index
docs/sdlc/changes/C-NNNN-<slug>/   spec.md or bugfix.md, design.md, plan.md, findings.md, profile.md, preregistration.md, model-review.md, handoff.md
docs/sdlc/changes/archive/
docs/sdlc/incidents/YYYY-MM-DD-<slug>.md
docs/sdlc/specs/                   living specs
docs/sdlc/health-ledger.md
docs/sdlc/sizing/<slug>.md
docs/sdlc/ideas/<slug>.md
docs/sdlc/adr/
docs/research/<slug>.md
docs/solutions/
evals/                             incident, agent-config and agent-readiness cases
evals/skills/<name>/               eval cases for each skill, from to-skill
.scratch/<effort>/                 wayfinder map and tickets (local tracker)
.audit/<slug>.tsv                  run trail of an AFK run
```

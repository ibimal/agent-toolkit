---
name: code-health
description: "Checks existing code for hygiene and drift without changing it: runs the repo's health checks itself (no CI needed), judges the areas the coverage plan picks against REVIEW.md, checks docs, specs, comments, names, notebooks and metrics for drift from the code, and returns findings in small batches. Use when code, docs or names feel out of date, when the merge hook or a milestone review starts it (after architecture-health), or for /code-health <area> or full."
metadata:
  inspired-by: https://github.com/garrytan/gstack (test-audit, document-release, deslop-shared-libs), https://github.com/cursor/plugins (no-comments) and https://github.com/trailofbits/skills (spec-to-code-compliance)
---

# Code health

Keep existing code in shape whenever this skill runs. It never changes code:
each finding the user picks goes to `/start`, and a mechanical problem that
recurs becomes a health check.

## The run

1. **Health checks, whole repo.** Run the command `docs/sdlc/config` names
   (`make health` by default). If the repo has none, run the language's
   standard tools directly (for Python: ruff, a type checker, vulture,
   import-linter, deptry and a secrets scanner) and report the missing
   command as a finding. Slow checks, such as running notebooks or
   documented commands, run only for the chosen areas.
2. **Choose areas** by the coverage plan below.
3. **Judge each area** against the standards in `REVIEW.md` (or, if the repo
   has none, the baseline in [standards.md](standards.md)), and check it for
   the drift in the table below.
4. **Sort the findings.** A fix that would move a module boundary or change
   an interface escalates to `architecture-health`; so does a structural
   cause, such as the same logic duplicated across modules. A mechanical
   problem that recurs becomes a proposed health check. Everything else goes
   into small batches, one area each.
5. **Record coverage** in `docs/sdlc/health-ledger.md`: for every area
   reviewed, including areas with no findings, the commit, what was found,
   and what is still open. Findings the user did not pick stay open, so
   later runs do not report them as new.

## Coverage plan

Never scope by a window of recent changes: cold code collects dead code and
stale docs, upcoming work lands in code that is cold today, and guardrail
code is expensive to get wrong.

- **Areas** are the components named in `docs/sdlc/architecture.md`, plus
  repo-level docs as one area. Without an architecture doc, use the top-level
  folders.
- **Mechanical checks** cover the whole repo, every run.
- **Judgement** covers about four areas per run, chosen in this order:
  1. areas the next intents in the backlog will touch;
  2. areas with trouble signals since the last run: health-check hits,
     incidents, repeated bug fixes, escalations;
  3. guardrail areas (privacy, money, security, model behaviour) changed at
     all since their last review;
  4. other areas with the most change since their last review.
  Keep one slot for the area reviewed longest ago.
- Change in an area is counted from the commit the ledger recorded for its
  last review.
- When the user names an area (`/code-health categoriser`) or says `full`,
  that is the scope. A milestone review, or the adoption of an existing
  project, is a full sweep with no budget.
- When the merge hook starts both `-health` skills, `architecture-health`
  runs first; skip code it is about to restructure.

## Drift

| Drift | Compared | Health checks catch | Judgement catches |
|---|---|---|---|
| Docs | README, runbook, AGENTS.md, docstrings vs the code | Files, symbols and links that no longer exist; documented commands that fail | Text that no longer describes what the code does |
| Living specs | Each requirement vs the code's behaviour | — | Requirements the code contradicts or no longer meets; behaviour no spec describes |
| Comments | Each comment vs the code beside it | Commented-out code; stale TODOs | Comments describing old behaviour or restating the code; a missing "why" where the code is not obvious |
| Architecture | The code vs `architecture.md` and the ADRs | Import contracts: layers, forbidden imports, cycles | Responsibilities in the wrong module; ADRs not followed (escalate) |
| Naming | Identifiers vs `GLOSSARY.md` and the style guide | Synonyms the glossary says to avoid | One term for two concepts; new concepts missing from the glossary |
| Dependencies | Declared vs imported | Unused and missing dependencies | — |
| Notebooks | Notebooks vs the current code | Notebooks that no longer run | Results that no longer match what the code produces |
| Metrics | Queries, dashboards and notebooks vs `data-context` | — | A metric computed differently from its definition; a definition nothing uses |

## Output

Findings grouped into batches, each with its area, the evidence and the
suggested route (usually a Feature S or a Refactor), plus the proposed health
checks. In an AFK run, the report waits for the user's pick.

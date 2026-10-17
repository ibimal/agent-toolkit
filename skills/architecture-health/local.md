# Local additions to architecture-health

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Never changes code.** Its output is ranked candidates and, after the
  user's pick, a grilling. The pick goes to `/start`, usually as a Refactor,
  or as a Feature L when contracts or data change.
- **Scoping replaces the instructions below.** Do not scope by recent
  commits. Follow the coverage plan:
  - Areas are the components named in `docs/sdlc/architecture.md`, plus
    repo-level docs as one area. Without an architecture doc, use the
    top-level folders.
  - Read the health ledger, `docs/sdlc/health-ledger.md`. Change in an area
    is counted from the commit the ledger recorded for its last review.
  - Pick about four areas, in this order: areas the next backlog intents will
    touch; areas with trouble signals since the last run (health-check hits,
    incidents, repeated bug fixes, escalations from `code-health`); guardrail
    areas (privacy, money, security, model behaviour) changed at all since
    their last review; the other areas with the most change. Keep one slot
    for the area reviewed longest ago, so cold code is never skipped for
    long.
  - A milestone review, or the adoption of an existing project, is a full
    sweep with no budget.
  - When the user names an area or says `full`, that is the scope.
- **Record coverage.** Update the ledger for every area reviewed, including
  areas with no findings: the commit, what was found, and what is still open.
  Findings the user did not pick stay open, so later runs do not report them
  as new.
- **Structure or hygiene.** A finding that would move a module boundary or
  change an interface belongs here; anything else belongs to `code-health`.
  When both run together, this skill runs first, so `code-health` can skip
  code that is about to be restructured.
- **Standards and decisions.** Judge against the architecture standards in
  `REVIEW.md` and the ADRs in `docs/sdlc/adr/` (not `docs/adr/`).
- **Runs that nobody watches.** When the merge hook starts it, write the
  report and stop; the grilling waits for the user's pick.

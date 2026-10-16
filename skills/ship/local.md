# Local additions to ship

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

The instructions below cover the PR body. This file adds the rest of the
step, in order.

1. **PR body.** Add two sections to the template below. **Intent** goes
   first: the intent ID and its one-line outcome, or for Feature S a one-line
   intent linked to an existing intent when one applies. **Review** goes
   after Evidence: the reviewer rung, the reviewer model and its effort, the
   verdicts from `review-model` and `review-dependency` when they ran, and
   each blocking finding with how it was resolved. Use the terms in
   `GLOSSARY.md`.
2. **CI.** Hand a failing check to `fix-ci`. Never disable or skip a check.
3. **Merge is a gate.** Ask the user before merging to `main`, and state the
   merge danger in one line.
4. **Deploy.** Dev deploys run freely, staging is assisted, and a production
   deploy needs the user's authorisation. Know the single rollback command
   before deploying, then run the post-deploy check and report its result.
5. **After merge:**
   - Archive the change: move its folder to `docs/sdlc/changes/archive/`,
     merge its spec deltas into the living specs in `docs/sdlc/specs/`, ask
     `to-design` to merge its structural changes into `architecture.md` when
     one exists, and move its intent to measuring.
   - Delete the change's `handoff.md` if it has one.
   - Add the tables, columns, events and metric queries the change
     introduced to `data-context`.
   - Merge hook: count the merges on `main` since the commit that
     `docs/sdlc/health-ledger.md` recorded for the last health run. At about
     20, start `architecture-health`, then `code-health`, as an AFK run.

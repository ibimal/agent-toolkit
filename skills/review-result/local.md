# Local additions to review-result

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Read `data-context` before any query,** and write back what you learn
  about grain, keys, freshness and traps, with its source.
- **Seven checks,** in this order, on top of the checklist below:
  1. State the claim so it can fail: condition, metric and threshold.
  2. Compare with a baseline under the same conditions.
  3. Record the run count and the spread.
  4. Name what limits the number.
  5. Rule out what else it could be measuring: errors, caching, skipped
     work, leakage, train/test contamination, selection and survivorship
     bias, multiple comparisons, join explosions, incomplete periods, and an
     unfair or shifting denominator.
  6. Confirm it measures what the intent's success metric or the
     preregistration says, computed the way `data-context` defines it. A
     number computed with a proposed definition says so.
  7. Re-run it from a clean start (a notebook top to bottom) and get the
     same answer.
- **Verdict.** End with ready, share with caveats, or needs revision.
  Record it with the result (in `findings.md`, the PR body or the intent's
  note) together with the data snapshot, commit and seed that reproduce it.
- **Preregistration.** When `preregistration.md` exists in the change
  folder, check the result against it and report every deviation.
- **Sizing calibration.** When the result measures a driver that a sizing in
  `docs/sdlc/sizing/` estimated, write the actual beside its range there.

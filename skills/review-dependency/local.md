# Local additions to review-dependency

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Two scopes.** Inside `review-change`, check only the packages the change
  adds or upgrades. Inside `release-readiness`, run across the whole
  lockfile, as the instructions below describe.
- **Checks for a new package,** besides the report below: the name is the
  one intended and not a look-alike (typosquatting); the licence is
  acceptable; and the standard library or an existing dependency does not
  already do the job.
- **Verdict.** Add, add with limits, or do not add, with the reason, for the
  PR body.
- **Not this skill's job.** Unused or missing dependencies belong to
  `code-health`.

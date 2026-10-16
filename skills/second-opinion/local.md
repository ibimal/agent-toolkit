# Local additions to second-opinion

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Which CLIs.** Use every other model family whose CLI `docs/sdlc/config`
  lists for this device and harness. Without the config, use the providers
  the instructions below describe. If no other family is reachable, say so;
  `review-change` and `review-plan` then fall to rung 2 of the ladder.
- **More than diffs.** The input can be a diff, a plan, an architecture, an
  MVP cut, or a brainstorm. For a brainstorm, ask each model for ideas from
  its own angle, not for a review.
- **Report; never fix.** Show where the models agree and disagree, and
  record each provider's model so the PR body can name the rung.

# Local additions to review-change

These rules come from this repo's workflow doc. They add to the upstream
instructions in SKILL.md, and they win where the two differ.

- **Order.** `tidy`, `verify-app` and `review-model` (when the change ships a
  model) run before this skill.
- **Reviewer ladder.** Use the first rung available:
  1. A model from another family, through `second-opinion`, which calls that
     family's CLI as listed in `docs/sdlc/config`.
  2. Otherwise the strongest same-family model at one effort level above the
     writer's, capped at max, in a fresh context with an adversarial prompt.
     It sees only the diff and the artifacts it traces to (spec, intent,
     product brief). A writer at max gets a reviewer at max, noted as "no
     step-up".
  Record the rung, the reviewer model and its effort for the PR body.
- **Standards axis.** `REVIEW.md` is always a standards source, security
  included; it holds the same standards `code-health` applies. Check new
  names against `GLOSSARY.md`.
- **Spec axis.** Read the intent from `docs/sdlc/intents/` together with
  `spec.md` or `bugfix.md` in the change folder. For Feature S, the spec is
  the one-line intent in the PR body.
- **Blocking.** Rank findings by severity. Only findings that affect
  correctness or a stated requirement block.
- **New packages.** When the change adds or upgrades a package, run
  `review-dependency`.
- **Acting on findings** is the writer's job, through `review-feedback`.

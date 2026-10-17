---
name: fix-ci
description: "Gets a failing CI check green by fixing its cause: read the failure, reproduce it locally, fix, push, re-check, at most three attempts, never skipping or disabling a check. Use when a PR check fails or ship hands over a failure."
license: MIT
---

Read [local.md](local.md) first. It holds this repo's additions to the
instructions below, and it wins where the two differ. The instructions
below are adapted from an upstream skill and changed in this repo;
`PROVENANCE` names its authors, source and licence, and lists every
change.

# Fix CI

## Trigger

Branch or PR CI is failing and needs a fast, iterative path to green checks.

## Workflow

1. Resolve the active PR and inspect `gh pr checks --json name,bucket,state,workflow,link`.
2. Inspect failed jobs and extract the first actionable error. Use GitHub Actions logs when available; otherwise use the check link to identify the failing command or service.
3. Apply the smallest safe fix.
4. Push, re-check the PR check set, and repeat until green.

## Guardrails

- Fix one actionable failure at a time.
- Prefer minimal, low-risk changes before broader refactors.
- Keep `gh pr checks` as the source of truth for overall PR CI state.

## Output

- Primary failing job and root error
- Fixes applied in iteration order
- Current CI status and next action

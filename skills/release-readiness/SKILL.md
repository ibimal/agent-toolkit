---
name: release-readiness
description: "Checks a milestone release before production across the whole application: NFRs from the specs and the brief verified, a security review, review-dependency across the lockfile, alerts in place, backups and migrations rehearsed, rollback rehearsed, and the runbook current. Use at New application step 7 and before every milestone release."
metadata:
  inspired-by: https://docs.bmad-method.org/ and https://github.com/garrytan/gstack (cso, canary)
---

# Release readiness

Hardening is a check, not a phase: the NFRs have been in every spec since the
start, and this skill verifies them across the whole application before a
milestone release. It reports; the production deploy stays the user's gate.

## Checks

Run each check and record pass, fail or not applicable, with the evidence: a
command and its output, a file, or a link.

1. **NFRs.** Collect the NFRs from the living specs in `docs/sdlc/specs/` and
   the guardrails in `docs/sdlc/product.md`. Verify each against the running
   system or its tests, with numbers.
2. **Security.** Review authentication and authorisation, secrets handling,
   input validation at every boundary, and the threat models in the Feature
   L designs.
3. **Dependencies.** Run `review-dependency` across the whole lockfile.
4. **Alerts.** Each guardrail and each critical path has an alert, and each
   alert reaches someone. An alert hook sends alerts to `/start`.
5. **Backups and migrations.** A backup restores, and each pending migration
   has been rehearsed on a copy of production-shaped data.
6. **Rollback.** Rollback is a single command, and it has been run once.
7. **Runbook.** `docs/runbook.md` says how to deploy, roll back, restore data
   and respond to each alert, and the commands in it work.

## Output

A readiness report: the verdict first (ready, or not ready with the
blocking items), then one line per check with its evidence. A failing check
goes to `/start` as work, usually a Feature S or a Bug fix.

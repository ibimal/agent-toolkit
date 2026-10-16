---
name: to-intent
description: "Writes a grilled problem as an intent file in docs/sdlc/intents/ (why, outcome, success metric, constraints, non-goals, open questions), attaches notes to existing intents, and moves an intent through its statuses. Use when a playbook reaches to-intent, when communication about an intent arrives, or when an intent's status changes."
---

# To intent

An intent says why a change matters and how its success will be measured.
It outlives the changes that deliver it, and it never names a solution.

## Write an intent

Create `docs/sdlc/intents/I-NNNN-<slug>.md`, numbered after the highest
existing intent:

```markdown
---
id: I-NNNN
status: proposed        # proposed, accepted, active, measuring, done, dropped, superseded
revision: 1
source: user            # user, agent, or external
serves: <product outcome or guardrail>
milestone: <milestone>
depends-on: []
sizing: <docs/sdlc/sizing/<slug>.md, when one exists>
changes: []
---

# <Intent title>

## Why
## Outcome
## Success metric
## Constraints
## Non-goals
## Open questions
## Notes
```

- **Serves.** When `docs/sdlc/product.md` exists, name the outcome or
  guardrail the intent serves. If it serves none, say so; the user decides
  whether it is out of scope or the brief needs amending.
- **Success metric.** Name the metric, the target and when it will be
  measured. A metric defined in `data-context` uses that definition.
- **Revision.** Increase `revision` on every change after acceptance. A spec
  records the revision it was written against, so a later change marks that
  spec stale.
- **Feature S** creates no intent file; its intent is one line in the PR
  body.

## Attach a note

Messages, meeting notes and review findings about an existing intent go
under its **Notes**, dated, with their source. They become a new intent only
when they introduce a new outcome.

## Move the status

proposed → accepted (the user accepts it at a gate) → active (a change is
under way) → measuring (released; the success metric is being checked) →
done (the metric was checked after release). The exits are dropped and
superseded; a superseded intent names its replacement.

After any change, regenerate `docs/sdlc/INTENTS.md`, the index by milestone
and status. When `docs/sdlc/config` links a tracker, mirror the intent to a
ticket and keep the IDs on both sides.

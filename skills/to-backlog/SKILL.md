---
name: to-backlog
description: "Turns an accepted product brief into proposed capability intents, each an outcome a user or operator would notice, with dependencies and milestones, and lists the open technical decisions for wayfinder. Use at New application step 3, for a new area or milestone in the expansion variant, or when the user asks for a backlog."
metadata:
  inspired-by: https://github.com/awslabs/aidlc-workflows and https://docs.bmad-method.org/
---

# To backlog

Break the product brief into intents, before any architecture exists.

## Rules

- **Outcomes, not layers.** Each intent is something a user or operator
  would notice once it is done. "Build the API" is not an intent; "a
  household sees all its recurring payments in one list" is.
- **Trace every intent** to the product outcome or guardrail it serves. An
  intent that serves none is out of scope, or a sign the brief needs
  amending; the user decides.
- **Backlog before architecture.** Intents describe outcomes and do not
  depend on an architecture; the architecture is chosen later to serve the
  MVP intents.
- **Detail just in time.** Write each intent with `to-intent` at status
  proposed, with a one-line outcome, its milestone and its dependencies.
  Only the MVP intents are grilled now; the rest are grilled when picked up.
- **Size before cutting.** When intents compete for the MVP or a milestone,
  run `size-impact` on each, and cut by the ranges.

## Output

1. The proposed intents in `docs/sdlc/intents/`, and a regenerated
   `docs/sdlc/INTENTS.md` index by milestone and status.
2. The proposed MVP cut and order, with the reason for each intent's place.
3. The open technical decisions the intents raise. Suggest `/wayfinder` for
   any that need more than one session.

Then `review-plan` challenges the MVP's scope, and the user decides the MVP
intents, the cut and the order at a gate.

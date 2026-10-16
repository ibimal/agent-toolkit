---
name: review-plan
description: "Reviews a plan, an MVP cut or an architecture before the user accepts it: a scope challenge (expand, hold or reduce) and an engineering review of feasibility, risks, sequencing, test seams and NFR coverage, through the reviewer ladder. Use on Feature L plans, a new application's MVP cut and architecture, or when the user asks for a plan review."
metadata:
  inspired-by: https://github.com/garrytan/gstack (plan-ceo-review, plan-eng-review)
---

# Review plan

Judge the work under review before it is accepted. The reviewer sees only
that work and the artifacts it traces to: the spec, the intent and the
product brief.

## Reviewer

Use the first rung available, as in `review-change`:

1. A model from another family, through `second-opinion`.
2. Otherwise the strongest same-family model at one effort level above the
   writer's, capped at max, in a fresh context with an adversarial prompt.

Record the rung, the model and its effort.

## Scope challenge

Recommend one of three, with the reason:

- **Expand:** the plan misses something the outcome needs.
- **Hold:** the scope fits the outcome.
- **Reduce:** part of the plan does not serve the outcome, or a thinner slice
  would prove it sooner. Name what to cut.

## Engineering review

- **Feasibility:** can each part be built as described?
- **Risks:** what could go wrong, how likely, and how bad; which risk the
  plan should retire first.
- **Sequencing:** do the blocking edges hold, and does the riskiest part come
  early enough?
- **Test seams:** does each slice have a seam that proves it?
- **NFRs:** are the performance, reliability, security, privacy and cost
  requirements covered?
- **Alternatives:** an option the plan rejected, or did not consider, that
  would be simpler.
- **For an architecture,** also check that every product constraint maps to
  a choice and every open decision has an ADR or a reason to defer.

## Output

A short report: the scope call first, then findings ranked by severity, each
with the evidence. The report informs the user's gate; it never approves the
plan.

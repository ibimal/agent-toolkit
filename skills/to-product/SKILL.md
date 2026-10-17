---
name: to-product
description: "Turns a grilled product vision into docs/sdlc/product.md (vision, users, problems, outcomes with metrics, guardrails, constraints, non-goals, riskiest assumptions, milestones and the MVP), and amends it later while listing the intents each amendment affects. Use at New application step 2, when an existing project adopts the workflow, in the expansion variant, or when the user asks to write or amend the product brief."
metadata:
  inspired-by: https://docs.bmad-method.org/ and https://github.com/garrytan/gstack (office-hours)
---

# To product

Write the product brief from what the grilling settled. The brief is the
user's: the agent drafts it, and the user accepts it at a gate.

## What the brief holds

Write `docs/sdlc/product.md` with these sections:

- **Vision:** one or two sentences.
- **Users:** who they are and what they are trying to do.
- **Problems:** what gets in their way today.
- **Outcomes:** what changes for users when the product works, each with
  the metric that shows it.
- **Guardrails:** quality, reliability and cost limits the product must hold.
- **Constraints:** what is fixed, such as budget, platform, law or data
  ownership.
- **Non-goals:** what the product will not do.
- **Riskiest assumptions:** the beliefs that would sink the product if
  wrong, most dangerous first.
- **Milestones:** each with the outcomes it delivers. Define the MVP by the
  outcome it proves, not by a feature list.

The brief names no solution: no technology, no architecture, no screens.
Those come later and must serve the brief.

## An existing project

When `setup` adopts an existing project, start from its draft and describe
the product as it is today: the users it serves, the outcomes it already
delivers, and their metrics where they exist. What should change becomes
intents, not new outcomes in the brief.

## Amending the brief

Amend the brief in place, with a dated line at the end of each changed
section. Then list every intent in `docs/sdlc/intents/` that the amendment
may affect, and ask the user to re-accept, amend or drop each one. Mark each
listed intent as flagged until the user answers.

## Gate

Show the brief and wait for the user to accept it. Terms the grilling
settled are already in `GLOSSARY.md`; use them.

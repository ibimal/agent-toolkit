---
name: brainstorm
description: "Generates ideas for a goal, problem or area by widening before narrowing: frames the goal and how ideas will be judged, grounds them in the brief, backlog, data and past ideas, generates many from several angles (with other model families through second-opinion), critiques every one, and ranks a shortlist with riskiest assumptions; never writes plans or code. Use when the user needs ideas, not yet an idea: a new project, a feature area, or an improvement plan."
disable-model-invocation: true
metadata:
  inspired-by: https://github.com/EveryInc/compound-engineering-plugin (ce-ideate), https://github.com/anthropics/knowledge-work-plugins (product-brainstorming), https://github.com/K-Dense-AI/claude-scientific-skills (scientific-brainstorming)
---

# Brainstorm

Find what the user could do. `research` finds what is true; this skill finds
options. Ideas for the code's own structure come from the `-health` skills,
and ideas for how the agent works come from `retro`.

## Steps

1. **Frame.** The goal, what is off the table, and how ideas will be judged.
   Confirm the criteria with the user; they are the user's.
2. **Ground.** Read what exists, so ideas build on it instead of repeating
   it: `docs/sdlc/product.md`, the backlog with its dropped intents and their
   reasons, `data-context`, past idea files in `docs/sdlc/ideas/`, and
   `docs/solutions/`. For a new project with no repo, use `research` to check
   what already exists outside.
3. **Generate** many ideas before judging any, from several angles: the
   user's problem, the data, cost, removing something, automating it, the
   bold version, the contrarian one, and doing nothing. Ask other model
   families for ideas through `second-opinion`, because different models miss
   different things. Invite the user to add theirs.
4. **Critique every idea.** Keep or cut each one with a reason, such as
   already tried, breaks a guardrail, or serves no outcome.
5. **Rank** the survivors against the criteria, each with its riskiest
   assumption. Hand each pick on: to `size-impact` (is it worth it?), a Spike
   (will it work?), or `/start` (a proposed intent).

## Record

In a product repo, save the whole list to `docs/sdlc/ideas/<slug>.md`: the
frame, every idea with its keep-or-cut reason, the ranked shortlist with
riskiest assumptions, and where each pick went. The next brainstorm starts
from it. Never write plans or code here.

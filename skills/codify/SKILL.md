---
name: codify
description: "Turns what a change taught into the most structural fix available: a lint or Semgrep rule, a hook or a test first; a glossary entry when the lesson is about what a word means; then a skill or AGENTS.md edit; a note in docs/solutions/ last. Use at the end of every change that taught something, and when the same mistake happens twice."
metadata:
  inspired-by: https://github.com/EveryInc/compound-engineering-plugin (ce-compound), https://github.com/trailofbits/skills (semgrep-rule-creator)
---

# Codify

Make the next change easier. A lesson becomes structure before it becomes
prose, because a check holds every time and prose only guides.

## Does the change hold a lesson?

A lesson qualifies when it is not readily recoverable from the final code,
tests or docs, and losing it would likely cause the mistake again or a long
rediscovery. Ask: if this lesson disappeared, would a future engineer
reading the code still repeat the mistake? If not, write nothing and say why.

## Pick the most structural form

In this order of preference:

1. **A lint rule, hook or test** that fails when the mistake recurs. Use the
   repo's linter where it can express the rule, and a Semgrep rule where it
   cannot. Add a new mechanical check to the health command named in
   `docs/sdlc/config`, so `code-health` runs it too.
2. **A glossary entry,** through `glossary`, when the lesson is about what a
   word means (for example, one word used two ways).
3. **A skill edit,** through `to-skill`, or one line in `AGENTS.md`.
4. **A note** in `docs/solutions/<slug>.md`: the problem, the cause, the fix,
   and how to spot it next time.

A mistake made twice always gets a structural fix or an `AGENTS.md` line.

## Output

Make the change in the current branch, as part of the change that taught
the lesson, and say in one line which form you chose and why. A lesson from
an incident also becomes an eval case in `evals/`.

---
name: technical-writing-review
description: Review technical prose, such as docs, READMEs, design documents, or code comments, against the always-on style rules, and report specific issues with rewrites. Use when the user asks to review, edit, or improve technical writing. Not for rewriting your own previous response (use plain-restate, condense, or deepen).
---

# Technical writing review

Review the given prose against the always-on style rules, titled "Response
style: technical plain English". If those rules are not in your
instructions, ask the user for them before you review.

1. Read the whole text first. Identify the reader and the purpose, and
   judge terms and depth against that reader.
2. Start with a one-line verdict, such as "ready", "needs small fixes",
   or "needs restructuring".
3. Report issues in order of impact. First report anything that could
   mislead the reader: an ambiguity, a missing condition, a
   contradiction, or a claim you can see is wrong. Then report clarity
   issues, then concision issues.
4. For each issue, quote the smallest span, name the rule, and give a
   rewrite. Report a repeated issue once, with the number of occurrences
   and one example.
5. Do not change code, identifiers, commands, paths, configuration keys,
   or program output.
6. If the text has no issues worth changing, say so and stop.

If the user asks for edits instead of a review, apply the fixes and list
the changes briefly.

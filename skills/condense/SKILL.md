---
name: condense
description: Shorten the previous response without simplifying it. Keeps every fact, condition, caveat, and technical term, and removes repetition and filler. Use only when the user asks for a shorter or tighter version, for example "shorter", "tighten this", or "too long". Not for plainer wording (use plain-restate), more depth (use deepen), or a summary that leaves out details.
---

# Condense

Rewrite your previous response so that it is shorter but not simpler. If
the user points to other text, or to one part of the response, condense
that instead.

1. Keep every fact, number, condition, caveat, and technical term. Keep
   the strength of each requirement ("must" stays "must") and any stated
   uncertainty. A hedge that qualifies a claim is not filler.
2. Keep code, commands, paths, and program output exactly as they are.
   Shorten only the prose around them.
3. Remove repetition, filler, and conclusions that are stated twice.
4. Merge sentences that share a subject. Drop an example if an earlier
   example already makes the same point.
5. Do not replace exact terms with plainer ones.
6. Follow the always-on style rules, titled "Response style: technical
   plain English".

Output only the rewritten response, with no introduction. There are two
exceptions:

- If the user gives a length limit that cannot hold every fact, keep the
  facts that matter most to the user's question. Add one final line that
  names what you left out.
- If the response cannot get shorter without losing content, say so in
  one sentence instead of rewriting it.
